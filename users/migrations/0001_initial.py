# Generated by Django 4.2.11 on 2025-03-09 17:13

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniqueConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_counter', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('avatar', models.FileField(blank=True, null=True, upload_to=users.models.avatar_path)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number Regex', regex='^(\\+998|998)\\d{9}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('otp_counter', models.PositiveSmallIntegerField(default=0)),
                ('otp_sent_time', models.DateTimeField(blank=True, null=True)),
                ('otp_tried', models.BooleanField(default=False)),
                ('branch', models.ManyToManyField(blank=True, to='app.branch')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('user_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role', to='users.userrole')),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
