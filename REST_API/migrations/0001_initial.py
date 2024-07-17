# Generated by Django 5.0.7 on 2024-07-16 11:31

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingSpace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('rate', models.IntegerField()),
                ('occupied', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('plate_no', models.CharField(max_length=10)),
                ('parked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ParkingDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=uuid.uuid4, max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('checkin_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('checkout_time', models.DateTimeField()),
                ('parking_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='REST_API.parkingspace')),
                ('vehicle_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='REST_API.vehicle_info')),
            ],
        ),
    ]
