# Generated by Django 4.2.6 on 2024-07-16 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parking', '0005_alter_parkingdetails_checkin_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle_info',
            name='parked',
            field=models.BooleanField(default=False),
        ),
    ]