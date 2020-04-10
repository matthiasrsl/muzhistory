# Generated by Django 3.0.1 on 2019-12-22 23:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("musicdata", "0007_auto_20191223_0012"),
        ("deezerdata", "0005_auto_20191222_2335"),
    ]

    operations = [
        migrations.AlterField(
            model_name='deezeralbum',
            name='release_group',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='musicdata.ReleaseGroup'),
        ),
        migrations.AlterField(
            model_name='deezertrack',
            name='recording',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='musicdata.Recording'),
        ),
    ]
