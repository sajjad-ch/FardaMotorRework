# Generated by Django 5.0.6 on 2024-07-03 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("car_module", "0001_initial"),
        ("rework_module", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="car",
            new_name="CarModel",
        ),
    ]
