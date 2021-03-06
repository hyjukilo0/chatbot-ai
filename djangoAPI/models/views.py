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
                if mes == "x":
                    aorder = Order()
                    return Response("")
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
                print(answer)

                return Response(self.scenario(intent, entity))
            
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
                return Response("")
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
            return "Xin ch??o qu?? kh??ch, qu?? kh??ch c???n gi??p j ????"
        elif intent == "Done":
            return " C???m ??n qu?? kh??ch ???? quan t??m v?? ???ng h??? s???n ph???m c???a shop ???."
        
        if intent == "Request" or intent == "Other":
            if len(entity) == 0:
                if check == "productname":
                    return "B???n mu???n mua m???t h??ng n??o ???"
                elif check == "color":
                    return "B???n kh??ch mu???n ch???n m??u n??o ???"
                elif check == "size":    
                    return "{} n??y b???n mu???n l???y size n??o ???? ho???c b???n c?? th??? cho shop xin c??n n???ng v?? chi???u cao ????? shop t?? v???n size cho m??nh nha".format(aorder.productname)
                elif check == "amount":
                    return "B???n mu???n ?????t bao nhi??u b??? n??y v???y ????"
                elif check == "address":
                    return "{} m??u {} n??y c?? gi?? l?? {} ???. ???????c ki???m tra h??ng tr?????c khi nh???n ???. B???n ????? l???i ?????a ch??? v?? s??t n???u mu???n mua nh??!!".format(aorder.productname, aorder.color, aorder.cost)
                elif check == "phone":
                    return "B???n cho m??nh xin s??? ??i???n tho???i nh???n h??ng v???i ???"
                else:
                    "C??m ??n b???n ???? quan t??m v?? ???ng h??? shop ???"

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
                return "V???i c??n n???ng v?? chi???u cao n??y th?? b???n m???c size {} nha".format(aorder.size)
            elif anssize == 1:
                if aorder.weight == None:
                    return "Cho shop xin th??m th??ng tin c??n n???ng v???i ???"
                else:
                    aorder.setsize('L')
                    return "V???i c??n n???ng n??y th?? b???n m???c size {} nha".format(aorder.size)
            else:
                if aorder.height == None:
                    return "Cho shop xin th??m th??ng tin chi???u cao v???i ???"
                else:
                    aorder.setsize('L')
                    return "V???i chi???u cao n??y th?? b???n m???c size {} nha".format(aorder.size)
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
            return "B???n mu???n mua m???t h??ng n??o ???"
        elif checkagain == "color":
            return "B???n kh??ch mu???n ch???n m??u n??o ???"
        elif checkagain == "size":    
            return "b???n mu???n l???y size n??o ???? Ho???c b???n c?? th??? cho shop xin c??n n???ng v?? chi???u cao ????? shop t?? v???n size cho m??nh nha"
        elif checkagain == "amount":
            return "B???n mu???n ?????t bao nhi??u b??? n??y v???y ????"
        elif checkagain == "address":
            return "{} m??u {} n??y c?? gi?? l?? {} ???. ???????c ki???m tra h??ng tr?????c khi nh???n ???. B???n ????? l???i ?????a ch??? v?? s??t n???u mu???n mua nh??!!".format(aorder.productname, aorder.color, aorder.cost)
        elif checkagain == "phone":
            return "B???n{} cho m??nh xin s??? ??i???n tho???i nh???n h??ng v???i ???"
        else:
            return "Th??ng tin ?????t h??ng c???a b???n l??: {} {} m??u {} size {} c?? gi?? {}, ph?? ship l?? 30k. T???ng 220k. Th???i gian ship t??? 3 - 6 ng??y. S??? ??i???n tho???i {}, ?????a ch??? {}. B???n ki???m tra l???i th??ng tin gi??p m??nh v???i nha".format(aorder.amount, aorder.productname, aorder.color, aorder.size, aorder.cost, aorder.phone, aorder.address)


        
                
                    

        


        



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
                height = re.search("(1|2)?\s?(m|m??t|met)\s?[0-9]+", mescomplete)
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
                    if re.search("(den|??en|trang|tr???ng|nude|xanh|hong|h???ng|v??ng|vang)", we):
                        entity_values.append(en + ":" + we)
            elif en == 'amount_product':
                for we in messplit:
                    if re.search("[0-9]+", we) or re.search("(mot|m???t)", we):
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

    
    
    
