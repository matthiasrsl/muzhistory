# Generated by Django 3.0.1 on 2019-12-26 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("deezerdata", "0013_auto_20191226_2300"),
    ]

    operations = [
        migrations.AddField(
            model_name="deezertrack",
            name="title_version",
            field=models.CharField(default="", max_length=1000),
            preserve_default=False,
        ),
    ]
