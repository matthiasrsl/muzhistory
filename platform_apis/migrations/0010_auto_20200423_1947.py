# Generated by Django 3.0 on 2020-04-23 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_apis', '0009_auto_20200423_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='version',
            field=models.IntegerField(default=32),
        ),
        migrations.AlterField(
            model_name='platformaccount',
            name='version',
            field=models.IntegerField(default=32),
        ),
    ]
