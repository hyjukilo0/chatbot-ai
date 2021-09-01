from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models.apps import ModelsConfig
from models.models import Messagepost, Products
from models.serializers import MessagepostSerializer

from models.order import Order

from django.core.files.storage import default_storage
from django.conf import settings

import os
import numpy as np
import re
import cv2
import underthesea
from underthesea import word_tokenize

aorder = Order()
shop_answer = []

# Create your views here.
class Classification(APIView):
    def get(self, request):
        return Response(request.data)
    
    def post(self, request):
        if request.method == 'POST':
            global aorder
            if request.POST['message']:
                mes = request.POST['message']
                
                mes = [self.cleantext(mes)]
                mes_split = mes[0].split(' ')
                print(mes_split)   
                
                mes_intent = self.embeddtext(mes, 0)
                intent = self.getintent(mes_intent)
                
                mes_entity = self.embeddtext(mes, 1)
                entity = self.getentity(mes_entity, mes_split)

                answer = "Intent: " + intent + ", " + "Entities: "
                for e in entity:
                    answer += (e + " ")

                return Response(answer)
            
            if request.FILES['image']:
                imagepost = None
                filename = request.FILES['image'].name
                pathfile = os.path.join('models/static/images/', filename)
                chunks = request.FILES['image'].chunks()
                imagepost = next(chunks)
                with default_storage.open(pathfile, 'wb+') as destination:
                    destination.write(imagepost)
                answerimage = self.getproductid(pathfile)
                print(answerimage)
                return
            return Response("None")

    def scenario(self, intent, entity):
        global aorder
        check = aorder.checkfullinfo()

        global shop_answer
        hello = False
        sizereq = False
        heightreq = False
        weightreq = False
        amountreq = False


        entities = []
        for en in entity:
            ensplit = en.split(":")
            entities.append([ensplit[0], ensplit[1]])
        

        if intent == "Hello" or intent == "Connect":
            return "Xin chào quý khách, quý khách cần giúp j ạ?"
        elif intent == "Done":
            return " Cảm ơn quý khách đã quan tâm và ủng hộ sản phẩm của shop ạ."
        
        if intent == "Request" or intent == "Other":
            if len(entity) == 0:
                if check == "productname":
                    return "Bạn muốn mua mặt hàng nào ạ"
                elif check == "color":
                    return "Bạn khách muốn chọn màu nào ạ"
                elif check == "size":    
                    return "bạn muốn lấy size nào ạ? Hoặc bạn có thể cho shop xin cân nặng và chiều cao để shop tư vấn size cho mình nha"
                elif check == "amount":
                    return "Bạn muốn đặt bao nhiêu bộ này vậy ạ?"
                elif check == "address":
                    return "{} màu {} này có giá là {} ạ. Được kiểm tra hàng trước khi nhận ạ. Bạn để lại địa chỉ và sđt nếu muốn mua nhé!!".format(aorder.productname, aorder.color, aorder.cost)
                elif check == "phone":
                    return "Bạn cho mình xin số điện thoại nhận hàng với ạ"
                else:
                    "Cám ơn bạn đã quan tâm và ủng hộ shop ạ"

        anssize = 0
        forsize = False
        for en in entities:
            if en[0] == 'height customer':
                aorder.setheight(en[1])
                anssize += 1
                forsize = True
            elif en[0] == 'weight customer':
                aorder.setweight(en[1])
                anssize += 2
                forsize = True
        
        if forsize == True:
            if anssize == 3:
                aorder.setsize('L')
                return "Với cân nặng và chiều cao này thì bạn mặc size {} nha".format(aorder.size)
            elif anssize == 1:
                if aorder.weight == None:
                    return "Cho shop xin thêm thông tin cân nặng với ạ"
                else:
                    aorder.setsize('L')
                    return "Với cân nặng này thì bạn mặc size {} nha".format(aorder.size)
            else:
                if aorder.height == None:
                    return "Cho shop xin thêm thông tin chiều cao với ạ"
                else:
                    aorder.setsize('L')
                    return "Với chiều cao này thì bạn mặc size {} nha".format(aorder.size)
        else:
            for en in entities:
                if en[0] == 'size':
                    aorder.setsize(en[1].upper())
                elif en[0] == 'color_product':
                    aorder.setcolor(en[1])
                elif en[0] == 'amount_product':
                    aorder.setamount(en[1])
                elif en[0] == 'address':
                    aorder.setaddress(en[1])
                elif en[0] == 'phone':
                    aorder.setphone(en[1])
        
        checkagain = aorder.checkfullinfo()
        if checkagain == "productname":
            return "Bạn muốn mua mặt hàng nào ạ"
        elif checkagain == "color":
            return "Bạn khách muốn chọn màu nào ạ"
        elif checkagain == "size":    
            return "bạn muốn lấy size nào ạ? Hoặc bạn có thể cho shop xin cân nặng và chiều cao để shop tư vấn size cho mình nha"
        elif checkagain == "amount":
            return "Bạn muốn đặt bao nhiêu bộ này vậy ạ?"
        elif checkagain == "address":
            return "{} màu {} này có giá là {} ạ. Được kiểm tra hàng trước khi nhận ạ. Bạn để lại địa chỉ và sđt nếu muốn mua nhé!!".format(aorder.productname, aorder.color, aorder.cost)
        elif checkagain == "phone":
            return "Bạn{} cho mình xin số điện thoại nhận hàng với ạ"
        else:
            return "Thông tin đặt hàng của bạn là: {} {} màu {} size {} có giá {}, phí ship là 30k. Tổng 220k. Thời gian ship từ 3 - 6 ngày. Số điện thoại {}, địa chỉ {}. Bạn kiểm tra lại thông tin giúp mình với nha".format(aorder.amount, aorder.productname, aorder.color, aorder.size, aorder.cost, aorder.phone, aorder.address)


        
                
                    

        


        



    def getproductid(self, image):
        global aorder
        img = cv2.imread(image)
        img = cv2.resize(img, (256, 256))
        img = img.reshape(1, 256, 256, 3)
        req = img / 255
        i = np.argmax(ModelsConfig.imagemodel.predict(req))
        getid = ModelsConfig.image_id[i]
        product = Products.objects.filter(product_id=getid).values('product_name', 'product_color', 'product_material', 'product_material_advantage')
        print(getid, product)
        aorder.setproduct(product[0]['product_name'], product[0]['product_color'], product[0]['product_material'], product[0]['product_material_advantage'], "179k")
        return getid

    
    def getentity(self, text, messplit):
        # print(ModelsConfig.svcmodel_entity.predict(text))
        entity = []
        entity_values = []
        for x in ModelsConfig.svcmodel_entity.predict(text):
            for i in range(len(x)):
                if x[i] == 1:
                    entity.append(ModelsConfig.entity[i])
        print(entity)
        mescomplete = ' '.join(messplit)
        for en in entity:
            if en == 'size':
                for we in messplit:
                    if we == 's' or we == 'm' or we == 'l':
                        entity_values.append(en + ":" + we)
            elif en == 'phone':
                for we in messplit:
                    if re.search("[0-9]+", we):
                        entity_values.append(en + ":" + we)
            elif en == 'address':
                entity_values.append(en)
            elif en == 'height customer':
                height = re.search("(1|2)?\s?(m|mét|met)\s?[0-9]+", mescomplete)
                if height:
                    entity_values.append(en + ":" + height.group().strip())
                else:
                    entity_values.append(en + ":" + "None")
            elif en == 'weight customer':
                weight = re.search("[0-9]+\s?(k|c)", mescomplete)
                if weight:
                    entity_values.append(en + ":" + weight.group().strip())
                else:
                    entity_values.append(en + ":" + "None")
            elif en == 'color_product':
                for we in messplit:
                    if re.search("(den|đen|trang|trắng|nude|xanh|hong|hồng|vàng|vang)", we):
                        entity_values.append(en + ":" + we)
            elif en == 'amount_product':
                for we in messplit:
                    if re.search("[0-9]+", we) or re.search("(mot|một)", we):
                        entity_values.append(en + ":" + we)
            elif en == 'material_product':
                entity_values.append(en)
            elif en == 'cost_product':
                entity_values.append(en)
            elif en == 'ID_product':
                entity_values.append(en)
            elif en == 'Id member':
                entity_values.append(en)
            elif en == 'shiping fee':
                entity_values.append(en)
            
        
        return entity_values

        

    def getintent(self, text):
        i = -1
        for x in ModelsConfig.svcmodel.predict(text):
            i = x
        return ModelsConfig.intent[i]

    def embeddtext(self, text, intent):
        if intent == 0:
            mess = ModelsConfig.tfidf.transform(text)
        else:
            mess = ModelsConfig.tfidf_entity.transform(text)
        mess = mess.toarray()
        return mess

    def cleantext(self, text):
        t = str(text)
        t = t.lower()
        t = re.sub('[\.\'?,:/\_\-()!*]', '', t)
        for x in ModelsConfig.tcwords:
            if type(x) is float:
                break
            x.strip()
            row = x.split(':', 1)
            wordr = row[0]
            tclist = row[1].split(',')
            for tc in tclist:
                if tc == '' or tc == ' ':
                    continue
                t = t.replace(tc, wordr)
        aword = [w for w in word_tokenize(t, format="text").split(' ') if (w not in ModelsConfig.stopwords)]
        u = ' '.join(aword)
        return u

    
    
    
