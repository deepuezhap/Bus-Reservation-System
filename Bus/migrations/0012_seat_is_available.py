# Generated by Django 4.1 on 2023-03-15 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Bus", "0011_seat"),
    ]

    operations = [
        migrations.AddField(
            model_name="seat",
            name="is_available",
            field=models.BooleanField(default=True),
        ),
    ]