from django.db import models
from app.models.branch import Branch
from app.models.cars import Car
from django.utils.translation import gettext_lazy as _
from app.models.employee import Employee

class Reservation(models.Model):
    class Status(models.TextChoices):
        Pending = "PN",_("Pending")
        Confirmed = "CMF", _("Confirmed")
        Completed = "CMD", _("Completed")
        Cancelled = "CLD", _("Canceled")
        Rejected = "RJD", _("Rejected")
    employee = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True)
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.Pending)
    total_price_renting = models.DecimalField(max_digits=15, decimal_places=2)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    return_date = models.DateTimeField()
    pick_up_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)