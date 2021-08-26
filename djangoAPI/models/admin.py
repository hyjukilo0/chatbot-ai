from django.contrib import admin
from models.models import Products
from models.models import Messagepost

# Register your models here.
admin.site.register(Messagepost)
admin.site.register(Products)