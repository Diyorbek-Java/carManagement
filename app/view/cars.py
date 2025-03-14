from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from ..serializers.cars import CarSerializer,CarGetSerializer
from ..models.cars import Car,CarImages
from ..pagination .paginations import DefaultLimitOffSetPagination
from django.db.models import Q
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from users.models import User


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    pagination_class = DefaultLimitOffSetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return CarGetSerializer
        return CarSerializer

    # permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     user_pk = self.request.user.pk
    #     user = User.objects.get()
    #     user_branches = user.branch 
    #     queryset = Car.objects.filter(branch__in=user_branches)
    #     if user.is_superuser:
    #         return Car.objects.all()  # Superusers can access all cars
        
    #     user_branches = user.branches.all()
    #     return Car.objects.filter(branch__in=user_branches)
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            image_files = request.FILES.getlist("images")
            images = data.get("images")
            if images:
                data.pop("images")

            with transaction.atomic():
                serialized_data = CarSerializer(data=data)
                serialized_data.is_valid(raise_exception=True)
                car_instance = serialized_data.save()

                if images:
                    for image in image_files:
                        CarImages.objects.create(car_id=car_instance, photo=image)
        
        except serializers.ValidationError as e:
            error_messages = {}
            for field, errors in e.detail.items():
                error_messages[field] = ' '.join([str(err) for err in errors])
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Car Created Successfully'}, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            data = request.data
            image_files = request.FILES.getlist("images")
            images = data.get("images")
            if images:
                data.pop("images")
                
            with transaction.atomic():
                serialized_data = CarSerializer(instance, data=data, partial=True)
                serialized_data.is_valid(raise_exception=True)
                parcel_instance = serialized_data.save()

                if images:
                    for image in image_files:
                        CarImages.objects.create(
                            parcel=parcel_instance, photo=image
                        )
        except serializers.ValidationError as e:
            error_messages = {}
            for field, errors in e.detail.items():
                error_messages[field] = ' '.join([str(err) for err in errors])
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Updated'}, status=status.HTTP_200_OK)
