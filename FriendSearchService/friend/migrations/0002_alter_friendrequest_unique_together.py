# Generated by Django 4.2.1 on 2023-05-09 23:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("friend", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="friendrequest",
            unique_together={("from_user", "to_user")},
        ),
    ]