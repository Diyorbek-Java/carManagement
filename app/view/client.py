from rest_framework import viewsets
from app.models.client import Client
from app.serializers.client import CleintSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = CleintSerializer