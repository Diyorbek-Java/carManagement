from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from ..view.branch import BranchViewSet
from ..view.cars import CarViewSet

app_name = "base"
router = DefaultRouter()

router.register("branchs", BranchViewSet, basename="Branches")
router.register("cars",CarViewSet,basename="Cars")

urlpatterns = []

urlpatterns += (router.urls 
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)