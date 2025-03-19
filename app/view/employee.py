
from rest_framework import viewsets
from app.models.employee import Employee
from app.serializers.employee import EmployeeSerializer,EmployeeCreateSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.filter().order_by('-updated_at')
    serializer_class = EmployeeSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EmployeeCreateSerializer  # Used for creating employees
        return EmployeeSerializer