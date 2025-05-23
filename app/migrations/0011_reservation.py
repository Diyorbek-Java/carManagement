# Generated by Django 4.2.11 on 2025-04-30 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_car_rental_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PN', 'Pending'), ('CMF', 'Confirmed'), ('CMD', 'Completed'), ('CLD', 'Canceled'), ('RJD', 'Rejected')], default='PN', max_length=50)),
                ('total_price_renting', models.DecimalField(decimal_places=2, max_digits=15)),
                ('return_date', models.DateTimeField()),
                ('pick_up_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.branch')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.car')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.employee')),
            ],
        ),
    ]
