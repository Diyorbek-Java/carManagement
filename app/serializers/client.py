from rest_framework import serializers
from app.models.client import Client

class CleintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
