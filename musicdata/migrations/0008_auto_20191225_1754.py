# Generated by Django 3.0.1 on 2019-12-25 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("musicdata", "0007_auto_20191223_0012"),
    ]

    operations = [
        migrations.AddField(
            model_name="recording",
            name="title_refine",
            field=models.CharField(default="", max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recording",
            name="title_short",
            field=models.CharField(default="", max_length=1000),
            preserve_default=False,
        ),
    ]