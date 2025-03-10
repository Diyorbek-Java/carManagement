from rest_framework import viewsets

from ..serializers.cars import CarSerializer
from ..models.cars import Car

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer