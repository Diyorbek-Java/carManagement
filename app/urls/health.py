from django.urls import path
from app.view.health import health_check

urlpatterns = [
    path('', health_check, name='health_check'),
]
