# Generated by Django 4.1 on 2023-03-12 13:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Bus", "0009_alter_userprofile_contact"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UserProfile",
            new_name="Profile",
        ),
    ]