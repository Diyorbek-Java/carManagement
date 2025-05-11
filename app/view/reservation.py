from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.reservation import Reservation
from app.serializers.reservations import ReservationCreateUpdateSerializer, ReservationRetrieveSerializer,ReservationPartialUpdateSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from django.core.exceptions import ValidationError
from app.models.cars import Car
import math
from rest_framework.permissions import IsAuthenticated


class ReservationViewSet(viewsets.ModelViewSet):
    parser_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return ReservationCreateUpdateSerializer
        if self.action == 'update':
            return ReservationPartialUpdateSerializer
        return ReservationRetrieveSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)

        if data.get("success") is False:  # Using .get() is safer
            return Response(data["data"], status=status.HTTP_400_BAD_REQUEST)  # Make 
        headers = self.get_success_headers(serializer.data)
        # Return with retrieve serializer
        retrieve_serializer = ReservationRetrieveSerializer(instance=serializer.instance)
        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data =  self.perform_update(serializer)
        if data.get("success") is False:
            return Response({data["data"]},status=status.HTTP_400_BAD_REQUEST)  
        # Return with retrieve serializer
        retrieve_serializer = ReservationRetrieveSerializer(instance=serializer.instance)
        return Response(retrieve_serializer.data)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        car = validated_data['car']
        pick_up_date = validated_data['pick_up_date']
        return_date = validated_data['return_date']
        branch = validated_data['branch']

        # Check date validity
        if pick_up_date >= return_date:
            return {
                "success": False,
                "data": {"message": "Pick-up date must be before return date"}
            }
        
        if pick_up_date < timezone.now():
            return {
                "success": False,
                "data": {"message": "Pick-up date cannot be in the past"}
            }
        
        # Check branch consistency
        if car.branch != branch:
            return {
                "success": False,
                "data": {"message": "Car and reservation should be in the same branch"}
            }

        # Check car availability
        conflicting_reservations = Reservation.objects.filter(
            car=car,
            status__in=[Reservation.Status.Pending, Reservation.Status.Confirmed],
            pick_up_date__lte=return_date,
            return_date__gte=pick_up_date
        )
        
        # Exclude current instance for updates
        if hasattr(self, 'instance') and self.instance:
            conflicting_reservations = conflicting_reservations.exclude(pk=self.instance.pk)
        
        if conflicting_reservations.exists():
            return {
                "success": False,
                "data": {"message": "Car is not available for the selected dates"}  # Fixed this line
            }

        # Set default status to Pending
        if 'status' not in validated_data:
            validated_data['status'] = Reservation.Status.Pending

        # Calculate total_price_renting if not provided
        if 'total_price_renting' not in validated_data:
            rental_days = math.ceil((return_date - pick_up_date).total_seconds() / (24 * 3600))
            validated_data['total_price_renting'] = car.rental_price_per_day * rental_days

        # Update car status to reserved
        car.rental_status = Car.RENTAL_STATUS_CHOICES.RESERV
        car.save()
        
        return {
            "success": True,
            "data": serializer.save()
        }

    def perform_update(self, serializer):
        instance = serializer.instance
        validated_data = serializer.validated_data
        car = validated_data.get('car', instance.car)
        pick_up_date = validated_data.get('pick_up_date', instance.pick_up_date)
        return_date = validated_data.get('return_date', instance.return_date)

        # Check date validity if dates are being updated
        if 'pick_up_date' in validated_data or 'return_date' in validated_data:
            if pick_up_date >= return_date:
                return {
                    "success":False,
                    "data":{"message": "Pick-up date must be before return date"}
                }
            if pick_up_date < timezone.now():
                return {
                    "success":False,
                    "data":{"message": "Pick-up date cannot be in the past"}
                }

        # Check branch consistency if branch or car is being updated
        branch = validated_data.get('branch', instance.branch)
        if 'car' in validated_data or 'branch' in validated_data:
            if car.branch != branch:
                return {
                    "success":False,
                    "data":{"message": "Car and reservation must be at the same branch"}
                }

        # Check car availability if car or dates are being updated
        if 'car' in validated_data or 'pick_up_date' in validated_data or 'return_date' in validated_data:
            conflicting_reservations = Reservation.objects.filter(
                car=car,
                status__in=[Reservation.Status.Pending, Reservation.Status.Confirmed],
                pick_up_date__lte=return_date,
                return_date__gte=pick_up_date
            ).exclude(pk=instance.pk)
            if conflicting_reservations.exists():
                return {
                    "success":False,
                    "data":{"message": "Car is not available for the selected dates"}
                }

        # Status transition validation
        if 'status' in validated_data:
            new_status = validated_data['status']
            current_status = instance.status

            # Define valid transitions
            valid_transitions = {
                Reservation.Status.Pending: [
                    Reservation.Status.Confirmed,
                    Reservation.Status.Cancelled,
                    Reservation.Status.Rejected
                ],
                Reservation.Status.Confirmed: [
                    Reservation.Status.Completed,
                    Reservation.Status.Cancelled
                ],
                Reservation.Status.Completed: [],
                Reservation.Status.Cancelled: [],
                Reservation.Status.Rejected: []
            }

            if new_status not in valid_transitions[current_status]:
                return {
                    "success":False,
                    "data":{"message": f"Cannot transition from {current_status} to {new_status}"}
                }

            # Update car status based on reservation status
            if new_status == Reservation.Status.Cancelled or new_status == Reservation.Status.Rejected:
                car.rental_status = Car.RENTAL_STATUS_CHOICES.BOSH
                car.save()
            elif new_status == Reservation.Status.Confirmed:
                car.rental_status = Car.RENTAL_STATUS_CHOICES.IJARADA
                car.save()

        # Calculate total_price_renting if not provided and dates or car changed
        if ('pick_up_date' in validated_data or 
            'return_date' in validated_data or 
            'car' in validated_data or 
            'total_price_renting' not in validated_data):
            rental_days = math.ceil((return_date - pick_up_date).total_seconds() / (24 * 3600))
            validated_data['total_price_renting'] = car.rental_price_per_day * rental_days
        return {
            "success":True,
            "data":serializer.save()
        }

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status in [Reservation.Status.Completed, Reservation.Status.Cancelled]:
            return {
                    "success":False,
                    "data":{"message": "Cannot delete completed or cancelled reservations"}
                }
        
        # Update car status when deleting
        car = instance.car
        car.rental_status = Car.RENTAL_STATUS_CHOICES.BOSH
        car.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)