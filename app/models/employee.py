from django.db import models
from uuid import uuid4
import os
from app.models.branch import Branch

def employee_images_upload_to(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join(f'employee/{instance}/{filename}')

class Employee(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    EMPLOYMENT_TYPE_CHOICES = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
    )
    WORK_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Tatilda', "Ta'tilda"),  # Assuming it's correct, though it looks unusual
        ('Boshagan', "Bo'shagan"),
    )
    photo = models.ImageField(upload_to=employee_images_upload_to)
    fullname = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    position = models.CharField(max_length=100)
    employmentType = models.CharField(max_length=11, choices=EMPLOYMENT_TYPE_CHOICES)
    hireDate = models.DateField()
    branch = models.ForeignKey(Branch,related_name="brach_of_employee", on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    workStatus = models.CharField(max_length=50, choices=WORK_STATUS_CHOICES)

    def __str__(self):
        return self.fullname