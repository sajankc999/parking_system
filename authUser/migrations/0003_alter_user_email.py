# Generated by Django 5.0.7 on 2024-07-18 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authUser', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]