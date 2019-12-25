# Generated by Django 3.0.1 on 2019-12-22 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdata', '0002_genre_market'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='version',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='genre',
            name='version',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='market',
            name='version',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='recording',
            name='version',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='recordingcontribution',
            name='version',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='releasegroup',
            name='version',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='releasegroupcontribution',
            name='version',
            field=models.IntegerField(default=2),
        ),
    ]