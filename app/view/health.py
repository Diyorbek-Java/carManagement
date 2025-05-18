from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import connection


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    A simple health check endpoint that:
    1. Verifies the application is running
    2. Tests database connection
    3. Returns appropriate status code
    """
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        # If we get here, the database connection works
        return Response(
            {
                "status": "healthy",
                "database": "connected",
                "message": "System is operational"
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                "status": "unhealthy",
                "database": "disconnected",
                "message": str(e)
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
