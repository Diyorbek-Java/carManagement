from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework.permissions import AllowAny
from users.views import get_user_data, home
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # API endpoints
    path("api/v1/", include("app.urls.base_urls")),
    
    # Authentication endpoints from carManagement-master
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/request-user-data/", get_user_data, name="Request User data"),

    # Modern API documentation endpoints from drf-spectacular
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Health check endpoint (retained for CI/CD monitoring)
    path("health/", include("app.urls.health")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
