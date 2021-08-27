from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models.apps import ModelsConfig
from models.models import Messagepost, Products
from models.serializers import MessagepostSerializer

from django.core.files.storage import default_storage
from django.conf import settings

import os
import numpy as np
import re
import cv2
import underthesea
from underthesea import word_tokenize

# Create your views here.
class Classification(APIView):

    def get(self, request):
        return Response(request.data)
    
    def post(self, request):
        if request.method == 'POST':
            if request.POST['message']:
                mes = request.POST['message']
                
                mes = [self.cleantext(mes)]         
                
                mes_intent = self.embeddtext(mes, 0)
                intent = self.getintent(mes_intent)
                
                mes_entity = self.embeddtext(mes, 1)
                entity = self.getentity(mes_entity)
                
                answer = "Intent: " + intent + ", " + "Entities: "
                for e in entity:
                    answer += (e + " ")
                print(answer)

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
                return Response(answerimage)
            return Response("None")

    def getproductid(self, image):
        img = cv2.imread(image)
        img = cv2.resize(img, (256, 256))
        img = img.reshape(1, 256, 256, 3)
        req = img / 255
        i = np.argmax(ModelsConfig.imagemodel.predict(req))
        getid = ModelsConfig.image_id[i]
        productname = Products.objects.filter(product_id=getid).values('product_name')
        print(getid, productname)
        return getid + ": " + productname[0]['product_name']

    
    def getentity(self, text):
        # print(ModelsConfig.svcmodel_entity.predict(text))
        entity = []
        for x in ModelsConfig.svcmodel_entity.predict(text):
            for i in range(len(x)):
                if x[i] == 1:
                    entity.append(ModelsConfig.entity[i])
        print(entity)
        return entity

        

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

    
    
    
