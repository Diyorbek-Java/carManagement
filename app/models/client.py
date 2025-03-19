from django.db import models

class Client(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phonenumber = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    passportid = models.CharField(max_length=255)
    driverLicense = models.CharField(max_length=255)
    licenseExpiry = models.CharField(max_length=255)
    age = models.IntegerField()
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
    ]
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True) 
