from rest_framework import serializers
from models.models import Messagepost

class MessagepostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messagepost
        fields = '__all__'