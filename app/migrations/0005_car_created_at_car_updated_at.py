# Generated by Django 4.2.11 on 2025-03-18 15:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_messagelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
