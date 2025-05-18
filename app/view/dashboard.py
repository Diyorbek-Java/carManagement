from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from app.models.reservation import Reservation
from app.models.cars import Car
from app.models.employee import Employee
from app.models.client import Client
from app.serializers.dashboard import DashboardSerializer
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_date
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import timezone as dt_timezone

class FixedDashboardAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Current date: May 13, 2025, 11:07 PM +05
        current_date = timezone.now().replace(hour=23, minute=7, second=0, microsecond=0, tzinfo=dt_timezone.utc)  # 11:07 PM +05
        start_date = current_date - timedelta(days=2)  # May 11, 2025
        end_date = current_date + timedelta(days=4)    # May 17, 2025

        # Initialize statistics dictionary
        statistics = {
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): {
                "reservations": Reservation.objects.filter(
                    created_at__date=(start_date + timedelta(days=i))
                ).count(),
                "cars": Car.objects.filter(
                    created_at__date=(start_date + timedelta(days=i))
                ).count(),
                "clients": Client.objects.filter(
                    created_at__date=(start_date + timedelta(days=i))
                ).count(),
                "staff": Employee.objects.filter(
                    created_at__date=(start_date + timedelta(days=i))
                ).count()
            } for i in range(7)
        }

        serializer = DashboardSerializer({"statistics": statistics})
        return Response(serializer.data)


class CustomDashboardAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        # Get date from query parameter
        date_str = request.query_params.get('date')
        if not date_str:
            raise ValidationError("Date parameter is required (e.g., ?date=2025-05-13)")

        try:
            base_date = parse_date(date_str)
            if not base_date:
                raise ValidationError("Invalid date format. Use YYYY-MM-DD.")
            base_date = timezone.make_aware(base_date.replace(hour=0, minute=0, second=0, microsecond=0))
        except ValueError:
            raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

        start_date = base_date - timedelta(days=2)
        end_date = base_date + timedelta(days=4)

        # Initialize statistics dictionary
        statistics = {
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): {
                "reservations": Reservation.objects.filter(
                    created_at__date=(start_date + timedelta(days=i))
                ).count(),
                "cars": Car.objects.filter(
                    created_at__date=(start_date + timedelta(days=i))
                ).count(),
                "clients": Client.objects.filter(
                    created_at__date=(start_date + timedelta(days=i))
                ).count(),
                "staff": Employee.objects.filter(
                    created_at__date=(start_date + timedelta(days=i))
                ).count()
            } for i in range(7)
        }

        serializer = DashboardSerializer({"statistics": statistics})
        return Response(serializer.data)