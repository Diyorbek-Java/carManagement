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
from app.serializers.dashboard import DashboardSerializer,DashboardOverviewSerializer
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_date
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import timezone as dt_timezone
from rest_framework import status
from django.db.models import Count, Sum, Avg
from app.models.branch import Branch
from django.db.models import F
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.db.models import ExpressionWrapper, DurationField, F, FloatField
from django.db.models.functions import Extract

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


class RentalDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
    
        try:
            # Validate year and month
            if not (1 <= month <= 12):
                raise ValidationError("Month must be between 1 and 12")
            start_date = datetime(year, month, 1, tzinfo=dt_timezone.utc)
            end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(seconds=1)

            # Vehicle Status Overview
            total_cars = Car.objects.count()
            rented_cars = Car.objects.filter(rental_status='ijarada').count()
            available_cars = total_cars - rented_cars

            # Most Rented Car This Month
            most_rented = Reservation.objects.filter(
                pick_up_date__gte=start_date,
                pick_up_date__lte=end_date,
                status='CMD'
            ).values('car__brand', 'car__model', 'car__category__name').annotate(
                total_rentals=Count('id'),
                total_revenue=Sum('total_price_renting'),
                avg_duration=Avg(
                    ExpressionWrapper(
                        (Extract(F('return_date'), 'epoch') - Extract(F('pick_up_date'), 'epoch')) / 86400,
                        output_field=FloatField()
                    )
                )
            ).order_by('-total_rentals').first()

            # Branch Insights
            total_branches = Branch.objects.count()
            branch_reservations = Reservation.objects.filter(
                pick_up_date__gte=start_date,
                pick_up_date__lte=end_date
            ).values('branch__name').annotate(
                reservations=Count('id')
            ).order_by('-reservations').first()

            # Staff & Payroll
            total_salary = Employee.objects.aggregate(Sum('salary'))['salary__sum'] or 0
            active_staff = Employee.objects.filter(workStatus='Active').count()
            full_time = Employee.objects.filter(employmentType='Full_time').count()
            part_time = Employee.objects.filter(employmentType='Part_time').count()

            # Client Metrics
            new_clients = Client.objects.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            ).count()
            total_clients = Client.objects.count()
            returning_clients = Client.objects.filter(
                reservation__pick_up_date__gte=start_date,
                reservation__pick_up_date__lte=end_date
            ).distinct().count()
            returning_rate = (returning_clients / total_clients * 100) if total_clients > 0 else 0

            data = {
                'vehicle_status': {'available': available_cars, 'rented': rented_cars},
                'most_rented_car': {
                    'brand_model': f"{most_rented['car__brand']} {most_rented['car__model']}" if most_rented else 'N/A',
                    'category': most_rented['car__category__name'] if most_rented else 'N/A',
                    'total_rentals': most_rented['total_rentals'] if most_rented else 0,
                    'revenue': float(most_rented['total_revenue']) if most_rented else 0,
                    'avg_duration': float(most_rented['avg_duration']) if most_rented else 0
                },
                'branch_insights': {
                    'total_branches': total_branches,
                    'top_branch': {
                        'name': branch_reservations['branch__name'] if branch_reservations else 'N/A',
                        'reservations': branch_reservations['reservations'] if branch_reservations else 0
                    }
                },
                'staff_payroll': {
                    'total_salary': float(total_salary),
                    'active_staff': active_staff,
                    'full_time': full_time,
                    'part_time': part_time
                },
                'client_metrics': {
                    'new_clients': new_clients,
                    'returning_rate': round(returning_rate, 2),
                    'total_returning': returning_clients
                }
            }

            serializer = DashboardOverviewSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response({"error": "Invalid year or month"}, status=status.HTTP_400_BAD_REQUEST)
