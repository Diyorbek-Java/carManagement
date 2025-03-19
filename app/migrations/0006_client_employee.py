# Generated by Django 4.2.11 on 2025-03-19 09:09

import app.models.employee
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_car_created_at_car_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phonenumber', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('passportid', models.CharField(max_length=255)),
                ('driverLicense', models.CharField(max_length=255)),
                ('licenseExpiry', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('blacklisted', 'Blacklisted')], max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=app.models.employee.employee_images_upload_to)),
                ('fullname', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('phone', models.CharField(max_length=15)),
                ('position', models.CharField(max_length=100)),
                ('employmentType', models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract')], max_length=11)),
                ('hireDate', models.DateField()),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('workStatus', models.CharField(choices=[('Active', 'Active'), ('Tatilda', "Ta'tilda"), ('Boshagan', "Bo'shagan")], max_length=50)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brach_of_employee', to='app.branch')),
            ],
        ),
    ]
