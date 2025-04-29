from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.reservation import Reservation
from app.serializers.reservations import ReservationCreateUpdateSerializer, ReservationRetrieveSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReservationCreateUpdateSerializer
        return ReservationRetrieveSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set default status to Pending if not provided
        if 'status' not in serializer.validated_data:
            serializer.validated_data['status'] = Reservation.Status.Pending
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Return the created reservation with the retrieve serializer
        retrieve_serializer = ReservationRetrieveSerializer(instance=serializer.instance)
        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return the updated reservation with the retrieve serializer
        retrieve_serializer = ReservationRetrieveSerializer(instance=serializer.instance)
        return Response(retrieve_serializer.data)

    def perform_create(self, serializer):
        # You can add any additional logic here before saving
        serializer.save()

    def perform_update(self, serializer):
        # You can add any additional logic here before saving
        serializer.save()