# Generated by Django 3.0.1 on 2019-12-22 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deezerdata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deezeralbum',
            name='version',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='deezertrack',
            name='version',
            field=models.IntegerField(default=2),
        ),
    ]
