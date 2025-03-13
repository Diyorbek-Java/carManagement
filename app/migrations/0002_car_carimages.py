# Generated by Django 4.2.11 on 2025-03-13 21:17

import app.models.cars
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('license_plate', models.CharField(max_length=20, unique=True)),
                ('seating_capacity', models.PositiveIntegerField()),
                ('transmission', models.CharField(max_length=50)),
                ('mileage', models.PositiveIntegerField()),
                ('rental_price_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
                ('owner_name', models.CharField(max_length=100)),
                ('owner_phone', models.CharField(max_length=20)),
                ('color', models.CharField(choices=[('red', 'Red'), ('blue', 'Blue'), ('black', 'Black'), ('white', 'White'), ('silver', 'Silver'), ('gray', 'Gray')], max_length=10)),
                ('fuel_type', models.CharField(choices=[('diesel', 'Diesel'), ('petrol', 'Petrol'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], max_length=10)),
                ('year', models.PositiveIntegerField()),
                ('deposit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('minimum_age', models.PositiveIntegerField()),
                ('features', models.TextField(blank=True)),
                ('engine_size', models.CharField(choices=[('0.6L', '0.6L'), ('1.0L', '1.0L'), ('1.5L', '1.5L'), ('2.0L', '2.0L'), ('2.5L', '2.5L'), ('3.0L', '3.0L'), ('3.5L', '3.5L'), ('4.0L', '4.0L'), ('5.0L', '5.0L'), ('6.0L', '6.0L'), ('7.0L+', '7.0L+')], max_length=10)),
                ('rental_status', models.CharField(choices=[('bosh', "Bo'sh"), ('ijarada', 'Ijarada'), ('reserv qilingan', 'Reserv qilingan')], max_length=20)),
                ('description', models.TextField(blank=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brach_of_car', to='app.branch')),
            ],
        ),
        migrations.CreateModel(
            name='CarImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(upload_to=app.models.cars.car_images_upload_to)),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app.car')),
            ],
        ),
    ]
