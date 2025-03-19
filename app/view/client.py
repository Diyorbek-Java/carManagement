from rest_framework import viewsets
from app.models.client import Client
from app.serializers.client import CleintSerializer,ClientCreateSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter().order_by('-updated_at')
    serializer_class = CleintSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ClientCreateSerializer  
        return CleintSerializer