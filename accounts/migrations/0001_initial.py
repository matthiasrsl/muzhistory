# Generated by Django 3.0.1 on 2020-01-01 22:13

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("platform_apis", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("version", models.IntegerField(default=9)),
                ("track_location", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeezerAccount",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.CharField(max_length=100)),
                (
                    "access_token",
                    models.CharField(blank=True, max_length=150, null=True),
                ),
                ("email", models.EmailField(max_length=254)),
                (
                    "last_history_request",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(
                            1969, 12, 31, 23, 0, tzinfo=utc),
                        null=True,
                    ),
                ),
                ("name", models.CharField(max_length=300)),
                ("version", models.IntegerField(default=9)),
                ("lastname", models.CharField(max_length=300)),
                ("firstname", models.CharField(max_length=300)),
                ("status", models.IntegerField(blank=True, null=True)),
                ("birthday", models.DateField(blank=True, null=True)),
                ("inscription_date", models.DateField(blank=True, null=True)),
                ("gender", models.CharField(max_length=1)),
                ("link", models.URLField(max_length=2000)),
                ("picture_small", models.URLField(max_length=2000)),
                ("picture_medium", models.URLField(max_length=2000)),
                ("picture_big", models.URLField(max_length=2000)),
                ("picture_xl", models.URLField(max_length=2000)),
                ("lang", models.CharField(max_length=2)),
                ("is_kid", models.BooleanField(null=True)),
                ("explicit_content_level", models.CharField(max_length=100)),
                ("flow_url", models.URLField(max_length=2000)),
                (
                    "market",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="platform_apis.Market",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.Profile",
                    ),
                ),
            ],
            options={"abstract": False, },
        ),
    ]
