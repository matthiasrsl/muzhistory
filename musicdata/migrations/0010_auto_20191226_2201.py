# Generated by Django 3.0.1 on 2019-12-26 21:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("deezerdata", "0009_auto_20191226_2201"),
        ("musicdata", "0009_auto_20191226_2034"),
    ]

    operations = [
        migrations.AddField(
            model_name="recording",
            name="deezer_track",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="deezerdata.DeezerTrack",
            ),
        ),
        migrations.AlterField(
            model_name="artist", name="version", field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name="genre", name="version", field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name="market", name="version", field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name="recording",
            name="version",
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name="recordingcontribution",
            name="version",
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name="releasegroup",
            name="version",
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name="releasegroupcontribution",
            name="version",
            field=models.IntegerField(default=3),
        ),
    ]
