# Generated by Django 4.2.11 on 2025-03-21 11:11

import app.models.employee
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0007_client_created_at_client_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='phonenumber',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='phone',
        ),
        migrations.AddField(
            model_name='client',
            name='phone_number',
            field=models.CharField(max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number Regex', regex='^(\\+998|998)\\d{9}$')]),
        ),
        migrations.AddField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number Regex', regex='^(\\+998|998)\\d{9}$')]),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='client',
            name='driverLicense',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='licenseExpiry',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='client',
            name='passportid',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('InActive', 'InActive'), ('Blacklisted', 'Blacklisted')], max_length=11),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employmentType',
            field=models.CharField(choices=[('Full_time', 'Full-time'), ('Part_time', 'Part-time'), ('Contract', 'Contract')], max_length=11),
        ),
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to=app.models.employee.employee_images_upload_to),
        ),
        migrations.AlterField(
            model_name='employee',
            name='workStatus',
            field=models.CharField(choices=[('Active', 'Active'), ('Vacation', 'Vacatio'), ('Fired', 'Fired')], max_length=50),
        ),
    ]
