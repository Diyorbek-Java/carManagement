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
    permission_classes = [IsAuthenticated]
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

        if data.get("success") is False:
            return Response(data["data"], status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        retrieve_serializer = ReservationRetrieveSerializer(instance=serializer.instance)
        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = self.perform_update(serializer)
        if data.get("success") is False:
            return Response(data["data"], status=status.HTTP_400_BAD_REQUEST)  # Fixed: Removed extra braces
        retrieve_serializer = ReservationRetrieveSerializer(instance=serializer.instance)
        return Response(retrieve_serializer.data)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        car = validated_data['car']
        pick_up_date = validated_data['pick_up_date']
        return_date = validated_data['return_date']
        branch = validated_data['branch']

        if pick_up_date >= return_date:
            return {"success": False, "data": {"message": "Pick-up date must be before return date"}}
        if pick_up_date < timezone.now():
            return {"success": False, "data": {"message": "Pick-up date cannot be in the past"}}
        if car.branch != branch:
            return {"success": False, "data": {"message": "Car and reservation should be in the same branch"}}

        conflicting_reservations = Reservation.objects.filter(
            car=car,
            status__in=[Reservation.Status.Pending, Reservation.Status.Confirmed],
            pick_up_date__lte=return_date,
            return_date__gte=pick_up_date
        )
        if conflicting_reservations.exists():
            return {"success": False, "data": {"message": "Car is not available for the selected dates"}}

        if 'status' not in validated_data:
            validated_data['status'] = Reservation.Status.Pending

        if 'total_price_renting' not in validated_data:
            rental_days = math.ceil((return_date - pick_up_date).total_seconds() / (24 * 3600))
            validated_data['total_price_renting'] = car.rental_price_per_day * rental_days

        car.rental_status = Car.RENTAL_STATUS_CHOICES.RESERV
        car.save()
        return {"success": True, "data": serializer.save()}
    def perform_update(self, serializer):
        instance = serializer.instance
        validated_data = serializer.validated_data
        car = validated_data.get('car', instance.car)
        pick_up_date = validated_data.get('pick_up_date', instance.pick_up_date)
        return_date = validated_data.get('return_date', instance.return_date)
        branch = validated_data.get('branch', instance.branch)

        # Check date validity if dates are updated
        if 'pick_up_date' in validated_data or 'return_date' in validated_data:
            if pick_up_date >= return_date:
                return {"success": False, "data": {"message": "Pick-up date must be before return date"}}
            if pick_up_date < timezone.now():
                return {"success": False, "data": {"message": "Pick-up date cannot be in the past"}}

        # Check branch consistency if car or branch is updated
        if 'car' in validated_data or 'branch' in validated_data:
            if car.branch != branch:
                return {"success": False, "data": {"message": "Car and reservation must be at the same branch"}}

        # Check car availability if car or dates are updated
        if 'car' in validated_data or 'pick_up_date' in validated_data or 'return_date' in validated_data:
            conflicting_reservations = Reservation.objects.filter(
                car=car,
                status__in=[Reservation.Status.Pending, Reservation.Status.Confirmed],
                pick_up_date__lte=return_date,
                return_date__gte=pick_up_date
            ).exclude(pk=instance.pk)
            if conflicting_reservations.exists():
                return {"success": False, "data": {"message": "Car is not available for the selected dates"}}

        # Determine the reservation's status (use new status if provided, otherwise use current)
        new_status = validated_data.get('status', instance.status)

        # Update car rental_status based on the reservation's status
        if new_status in [Reservation.Status.Cancelled, Reservation.Status.Rejected]:
            car.rental_status = Car.RENTAL_STATUS_CHOICES.BOSH
        elif new_status == Reservation.Status.Confirmed:
            car.rental_status = Car.RENTAL_STATUS_CHOICES.IJARADA
        elif new_status == Reservation.Status.Pending:
            car.rental_status = Car.RENTAL_STATUS_CHOICES.RESERV
        car.save()

        # Status transition validation (only if status is being updated)
        # if 'status' in validated_data:
        #     current_status = instance.status
        #     valid_transitions = {
        #         Reservation.Status.Pending: [Reservation.Status.Confirmed, Reservation.Status.Cancelled, Reservation.Status.Rejected],
        #         Reservation.Status.Confirmed: [Reservation.Status.Completed, Reservation.Status.Cancelled],
        #         Reservation.Status.Completed: [],
        #         Reservation.Status.Cancelled: [],
        #         Reservation.Status.Rejected: []
        #     }
        #     if new_status not in valid_transitions[current_status]:
        #         return {"success": False, "data": {"message": f"Cannot transition from {current_status} to {new_status}"}}

        # Recalculate total_price_renting if necessary
        if ('pick_up_date' in validated_data or 'return_date' in validated_data or 
            'car' in validated_data or 'total_price_renting' not in validated_data):
            rental_days = math.ceil((return_date - pick_up_date).total_seconds() / (24 * 3600))
            validated_data['total_price_renting'] = car.rental_price_per_day * rental_days

        # Ensure serializer.save() is called and handled
        try:
            saved_instance = serializer.save()
            return {"success": True, "data": saved_instance}
        except Exception as e:
            return {"success": False, "data": {"message": str(e)}}

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