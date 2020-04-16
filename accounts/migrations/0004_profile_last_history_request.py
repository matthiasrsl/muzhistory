# Generated by Django 3.0 on 2020-03-25 12:36

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_delete_deezeraccount"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="last_history_request",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(1969, 12, 31, 23, 0, tzinfo=utc),
                null=True,
            ),
        ),
    ]