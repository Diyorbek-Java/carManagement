from rest_framework import serializers
from app.models.employee import Employee


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'photo',
            'fullname',
            'dob',
            'gender',
            'phone_number',
            'position',
            'employmentType',
            'hireDate',
            'branch',
            'salary',
            'workStatus',
        ]

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'