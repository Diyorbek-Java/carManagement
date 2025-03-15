from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from ..view.branch import BranchViewSet
from ..view.cars import CarViewSet,CarFeaturesModelViewSet


from users.views import home,UserViewSet,UserRoleViewSet
app_name = "base"
router = DefaultRouter()

router.register("branchs", BranchViewSet, basename="Branches")
router.register("cars",CarViewSet,basename="Cars")
router.register("users",UserViewSet,basename="Users")
router.register("user-role",UserRoleViewSet,basename="UserRole")
router.register("car-features",CarFeaturesModelViewSet,basename="car-features")

urlpatterns = [
    path("herllo",home,name="second hoem")
]

urlpatterns += (router.urls 
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)