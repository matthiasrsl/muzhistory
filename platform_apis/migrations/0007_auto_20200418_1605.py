# Generated by Django 3.0 on 2020-04-18 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_apis', '0006_auto_20200417_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='version',
            field=models.IntegerField(default=13),
        ),
        migrations.AlterField(
            model_name='platformaccount',
            name='version',
            field=models.IntegerField(default=13),
        ),
    ]