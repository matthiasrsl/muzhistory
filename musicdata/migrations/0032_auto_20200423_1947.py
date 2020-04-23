# Generated by Django 3.0 on 2020-04-23 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdata', '0031_auto_20200423_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='version',
            field=models.IntegerField(default=32),
        ),
        migrations.AlterField(
            model_name='genre',
            name='version',
            field=models.IntegerField(default=32),
        ),
        migrations.AlterField(
            model_name='recording',
            name='version',
            field=models.IntegerField(default=32),
        ),
        migrations.AlterField(
            model_name='recordingcontribution',
            name='version',
            field=models.IntegerField(default=32),
        ),
        migrations.AlterField(
            model_name='releasegroup',
            name='version',
            field=models.IntegerField(default=32),
        ),
        migrations.AlterField(
            model_name='releasegroupcontribution',
            name='version',
            field=models.IntegerField(default=32),
        ),
        migrations.AlterField(
            model_name='track',
            name='version',
            field=models.IntegerField(default=32),
        ),
    ]
