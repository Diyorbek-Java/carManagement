from rest_framework import viewsets
from app.models.client import Client
from app.serializers.client import ClientSerializer,ClientCreateSerializer
from ..pagination .paginations import DefaultLimitOffSetPagination
from rest_framework.permissions import IsAuthenticated

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter().order_by('-updated_at')
    serializer_class = ClientSerializer
    pagination_class = DefaultLimitOffSetPagination
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):
        if self.request.method == "POST":
            return ClientCreateSerializer  
        return ClientSerializer