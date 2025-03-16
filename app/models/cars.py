from django.db import models
from uuid import uuid4
import os
from ..models.branch import Branch


def car_images_upload_to(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join(f'cars/{instance}/{filename}')

class CarFeatures(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    
class Car(models.Model):
    COLOR_CHOICES = [
        ("red", "Red"),
        ("blue", "Blue"),
        ("black", "Black"),
        ("white", "White"),
        ("silver", "Silver"),
        ("gray", "Gray"),
    ]
    
    FUEL_CHOICES = [
        ("diesel", "Diesel"),
        ("petrol", "Petrol"),
        ("electric", "Electric"),
        ("hybrid", "Hybrid"),
    ]
    
    ENGINE_CHOICES = [
        ("0.6L", "0.6L"),
        ("1.0L", "1.0L"),
        ("1.5L", "1.5L"),
        ("2.0L", "2.0L"),
        ("2.5L", "2.5L"),
        ("3.0L", "3.0L"),
        ("3.5L", "3.5L"),
        ("4.0L", "4.0L"),
        ("5.0L", "5.0L"),
        ("6.0L", "6.0L"),
        ("7.0L+", "7.0L+")
    ]
    
    RENTAL_STATUS_CHOICES = [
        ("bosh", "Bo'sh"),
        ("ijarada", "Ijarada"),
        ("reserv qilingan", "Reserv qilingan"),
    ]
    
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20, unique=True)
    seating_capacity = models.PositiveIntegerField()
    transmission = models.CharField(max_length=50)
    mileage = models.PositiveIntegerField()
    rental_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    owner_name = models.CharField(max_length=100)
    owner_phone = models.CharField(max_length=20)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    year = models.PositiveIntegerField()
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_age = models.PositiveIntegerField()
    features = models.ManyToManyField(CarFeatures,blank=True)
    engine_size = models.CharField(max_length=10, choices=ENGINE_CHOICES)
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES)
    description = models.TextField(blank=True)
    branch = models.ForeignKey(Branch, related_name="brach_of_car", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"

class CarImages(models.Model):
    photo = models.FileField(upload_to=car_images_upload_to)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")

    def __str__(self) -> str:
        return f"{self.car_id}"