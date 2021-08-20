from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models.apps import ModelsConfig
from models.models import Messagepost
from models.serializers import MessagepostSerializer

import numpy as np
#import pandas as pd
#import underthesea
#from underthesea import word_tokenize

# Create your views here.
class Classification(APIView):

    def get(self, request):
        return Response(request.data)
    
    def post(self, request):
        if request.method == 'POST':
            mess = MessagepostSerializer(data = request.data)
            print(mess.data)
            for x in request.data:
                mes = [x]
            #mes = self.cleantext(mes)
            #print(mes)
            mes = ModelsConfig.tfidf.transform(mes)
            mes.toarray()
            #print(mes)
            for x in ModelsConfig.svcmodel.predict(mes):
                i = x
            print(ModelsConfig.intent[i])
            return Response(ModelsConfig.intent[i])
    
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
        #aword = [w for w in word_tokenize(t, format="text").split(' ')  if (w not in ModelsConfig.stopwords)]
        u = ' '.join(aword)
        return u
