# Generated by Django 3.0 on 2020-04-23 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deezerdata', '0028_auto_20200423_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deezermp3',
            name='title',
        ),
        migrations.AlterField(
            model_name='deezeralbum',
            name='version',
            field=models.IntegerField(default=32),
        ),
    ]
