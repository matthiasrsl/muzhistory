# Generated by Django 3.0 on 2020-04-18 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0009_auto_20200417_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyentry',
            name='version',
            field=models.IntegerField(default=13),
        ),
    ]
