# Generated by Django 3.0 on 2020-04-17 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_apis', '0005_platformaccount_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='version',
            field=models.IntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='platformaccount',
            name='version',
            field=models.IntegerField(default=12),
        ),
    ]
