# Generated by Django 3.0.1 on 2019-12-25 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("deezerdata", "0006_auto_20191223_0032"),
    ]

    operations = [
        migrations.RemoveField(model_name="deezertrack", name="title_short",),
        migrations.RemoveField(model_name="deezertrack",
                               name="title_version",),
    ]
