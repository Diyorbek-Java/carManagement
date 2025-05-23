from rest_framework import serializers

class DayStatsSerializer(serializers.Serializer):
    reservations = serializers.IntegerField()
    cars = serializers.IntegerField()
    clients = serializers.IntegerField()
    staff = serializers.IntegerField()


class VehicleStatusSerializer(serializers.Serializer):
    available = serializers.IntegerField()
    rented = serializers.IntegerField()

class MostRentedCarSerializer(serializers.Serializer):
    brand_model = serializers.CharField()
    category = serializers.CharField()
    total_rentals = serializers.IntegerField()
    revenue = serializers.FloatField()
    avg_duration = serializers.FloatField()

class TopBranchSerializer(serializers.Serializer):
    name = serializers.CharField()
    reservations = serializers.IntegerField()

class BranchInsightsSerializer(serializers.Serializer):
    total_branches = serializers.IntegerField()
    top_branch = TopBranchSerializer()

class StaffPayrollSerializer(serializers.Serializer):
    total_salary = serializers.FloatField()
    active_staff = serializers.IntegerField()
    full_time = serializers.IntegerField()
    part_time = serializers.IntegerField()

class ClientMetricsSerializer(serializers.Serializer):
    new_clients = serializers.IntegerField()
    returning_rate = serializers.FloatField()
    total_returning = serializers.IntegerField()

class DashboardOverviewSerializer(serializers.Serializer):
    vehicle_status = VehicleStatusSerializer()
    most_rented_car = MostRentedCarSerializer()
    branch_insights = BranchInsightsSerializer()
    staff_payroll = StaffPayrollSerializer()
    client_metrics = ClientMetricsSerializer()
class DashboardSerializer(serializers.Serializer):
    statistics = serializers.DictField(
        child=DayStatsSerializer(),
        help_text="Daily statistics for reservations, cars, clients, and staff"
    )