# Generated by Django 3.0.1 on 2019-12-22 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("musicdata", "0005_artist_nb_fans_deezer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artist",
            name="image_url_deezer_large",
            field=models.URLField(default="", max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="artist",
            name="image_url_deezer_medium",
            field=models.URLField(default="", max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="artist",
            name="image_url_deezer_small",
            field=models.URLField(default="", max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="artist",
            name="image_url_deezer_xl",
            field=models.URLField(default="", max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="artist",
            name="image_url_spotify_largest",
            field=models.URLField(default="", max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="artist",
            name="image_url_spotify_medium",
            field=models.URLField(default="", max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="artist",
            name="nb_fans_deezer",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="recording",
            name="audio_analysis",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="recording",
            name="audio_features",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
