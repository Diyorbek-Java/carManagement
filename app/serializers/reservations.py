from rest_framework import serializers
from django.utils import timezone
from app.models.reservation import Reservation
from app.serializers.employee import EmpliyeeContectGetSerilairzer
from app.serializers.cars import CarGetSerializer
from app.serializers.branch import BrachNameSerializer
from app.serializers.client  import ClientSerializer
class ReservationCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'employee',
            'car',
            'pick_up_date',
            'return_date',
            'client',
            'total_price_renting',
            'branch',
            'status'
        ]
        extra_kwargs = {
            'total_price_renting': {'required': False},
            'client': {'required': True},
            }
        

    def validate(self, data):
        errors = {}

        # Validate pick_up_date and return_date are not in the past
        now = timezone.now()
        if 'pick_up_date' in data and data['pick_up_date'] < now:
            errors['pick_up_date'] = "Pick up date cannot be in the past."
        
        if 'return_date' in data and data['return_date'] < now:
            errors['return_date'] = "Return date cannot be in the past."
        
        # Validate return_date is after pick_up_date
        if 'pick_up_date' in data and 'return_date' in data:
            if data['return_date'] <= data['pick_up_date']:
                errors['return_date'] = "Return date must be after pick up date."

        # Validate employee is from the same branch
        if 'employee' in data and 'branch' in data:
            if data['employee'] and data['employee'].branch != data['branch']:
                errors['employee'] = "Selected employee must belong to the selected branch."

        if errors:
            raise serializers.ValidationError(errors)
        
        return data
    

class ReservationRetrieveSerializer(serializers.ModelSerializer):
    employee = EmpliyeeContectGetSerilairzer()
    car = CarGetSerializer()
    branch = BrachNameSerializer()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    client = ClientSerializer( read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id',
            'employee',
            'car',
            'status',
            'status_display',
            'total_price_renting',
            'branch',
            'client',
            'return_date',
            'pick_up_date',
            'created_at',
            'updated_at'
        ]


class ReservationPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'employee',
            'car',
            'pick_up_date',
            'return_date',
            'total_price_renting',
            'branch',
            'status'
        ]
        extra_kwargs = {
            'employee': {'required': False},
            'car': {'required': False},
            'pick_up_date': {'required': False},
            'return_date': {'required': False},
            'total_price_renting': {'required': False},
            'branch': {'required': False},
            'status': {'required': False}
        }

    def validate(self, data):
        errors = {}
        now = timezone.now()

        # Only validate dates if they are provided in the update
        if 'pick_up_date' in data and data['pick_up_date'] < now:
            errors['pick_up_date'] = "Pick up date cannot be in the past."
        
        if 'return_date' in data and data['return_date'] < now:
            errors['return_date'] = "Return date cannot be in the past."
        
        # Validate return_date is after pick_up_date only if both are provided
        if 'pick_up_date' in data and 'return_date' in data:
            if data['return_date'] <= data['pick_up_date']:
                errors['return_date'] = "Return date must be after pick up date."

        # Validate employee is from the same branch only if both are provided
        if 'employee' in data and 'branch' in data:
            if data['employee'] and data['branch'] and data['employee'].branch != data['branch']:
                errors['employee'] = "Selected employee must belong to the selected branch."

        if errors:
            raise serializers.ValidationError(errors)
        
        return data