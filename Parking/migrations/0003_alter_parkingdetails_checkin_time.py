# Generated by Django 4.2.6 on 2024-07-15 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Parking', '0002_remove_vehicle_info_checkin_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingdetails',
            name='checkin_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
