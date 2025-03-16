# Generated by Django 4.2.11 on 2025-03-16 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_carfeatures_remove_car_features_car_features'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_by', models.CharField(max_length=255)),
                ('recipient', models.CharField(max_length=255)),
                ('message_type', models.CharField(choices=[('email', 'Email'), ('sms', 'SMS')], max_length=10)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
            ],
        ),
    ]
