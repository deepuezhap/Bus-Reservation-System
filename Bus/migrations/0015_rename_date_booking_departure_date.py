# Generated by Django 4.1 on 2023-03-16 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Bus", "0014_alter_booking_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="booking",
            old_name="date",
            new_name="departure_date",
        ),
    ]
