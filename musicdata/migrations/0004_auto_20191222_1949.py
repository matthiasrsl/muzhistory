# Generated by Django 3.0.1 on 2019-12-22 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("musicdata", "0003_auto_20191222_1932"),
    ]

    operations = [
        migrations.RenameField(
            model_name="artist", old_name="soptify_id", new_name="spotify_id",
        ),
    ]
