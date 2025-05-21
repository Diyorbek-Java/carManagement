from rest_framework import serializers
from app.models.client import Client

class ClientCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = Client
        fields = [
            'fullname', 'email', 'phone_number', 'address', 
            'passportid', 'driverLicense', 'licenseExpiry', 
            'age', 'status'
        ] 

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
