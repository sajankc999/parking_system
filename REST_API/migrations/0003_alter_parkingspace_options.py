# Generated by Django 5.0.7 on 2024-07-23 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('REST_API', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parkingspace',
            options={'ordering': ['number']},
        ),
    ]