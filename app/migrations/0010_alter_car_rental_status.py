# Generated by Django 4.2.11 on 2025-03-23 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_carcategory_car_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='rental_status',
            field=models.CharField(choices=[('bosh', "Bo'sh"), ('ijarada', 'Ijarada'), ('reserved', 'Reserv qilingan')], default='bosh', max_length=20),
        ),
    ]
