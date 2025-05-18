from rest_framework import serializers

class DayStatsSerializer(serializers.Serializer):
    reservations = serializers.IntegerField()
    cars = serializers.IntegerField()
    clients = serializers.IntegerField()
    staff = serializers.IntegerField()
class DashboardSerializer(serializers.Serializer):
    statistics = serializers.DictField(
        child=DayStatsSerializer(),
        help_text="Daily statistics for reservations, cars, clients, and staff"
    )