# Generated by Django 5.0.6 on 2024-07-03 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_module", "0002_rename_car_carmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carmodel",
            name="VIN_number",
            field=models.IntegerField(
                max_length=20, unique=True, verbose_name="شماره VIN"
            ),
        ),
    ]
