from django.apps import AppConfig

from tensorflow.keras.models import load_model

import os
import pickle
import numpy as np
import pandas as pd


class ModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'models'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TMODEL_FOLDER = os.path.join(BASE_DIR, 'models/trainmodels/')
    VNN_FOLDER = os.path.join(BASE_DIR, 'models/vnwords/')

    myfile = pd.read_excel(os.path.join(VNN_FOLDER, "vnnlp-data.xlsx"))
    stopwords = myfile['Stopwords'].values
    tcwords = myfile['Tcwords'].values
    with open(os.path.join(TMODEL_FOLDER, "linearsvc-001.pkl"), 'rb') as file:  
        svcmodel = pickle.load(file)
    with open(os.path.join(TMODEL_FOLDER, "linearsvc-001-entity.pkl"), 'rb') as file:  
        svcmodel_entity = pickle.load(file)
    with open(os.path.join(TMODEL_FOLDER, "tfidf.pkl"), 'rb') as file:  
        tfidf = pickle.load(file)
    with open(os.path.join(TMODEL_FOLDER, "tfidf-entity.pkl"), 'rb') as file:  
        tfidf_entity = pickle.load(file)

    imagemodel = load_model(os.path.join(TMODEL_FOLDER, 'hume_imageClassifier.h5'))

    intent = ['Changing', 'Connect', 'Done', 'Hello', 'Inform', 'Order', 'Other', 'Request', 'Return', 'feedback']
    entity = ['ID_product','color_product', 'material_product','cost_product','amount_product','Id member', 'shiping fee','height customer','weight customer','phone', 'address', 'size']
    image_id = ['D0010','D0011','D0012','D0013','D0014','D0015','D0016','D0017','D004','D005','D006','D007','D008','D009','DS001','Da','S002','S003','S004','S005','S006','S008','S009']