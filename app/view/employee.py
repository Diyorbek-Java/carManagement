
from rest_framework import viewsets
from app.models.employee import Employee
from app.serializers.employee import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer