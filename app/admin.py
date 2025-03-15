from django.contrib import admin


from .models.branch import Branch
from .models.cars import Car,CarImages,CarFeatures

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name"
    ]
@admin.register(CarFeatures)
class CarFeatureAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name"
    ]

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "brand"
    ]
@admin.register(CarImages)
class CarAdminAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "car_id"
    ]