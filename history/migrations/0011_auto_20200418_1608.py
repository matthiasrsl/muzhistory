# Generated by Django 3.0 on 2020-04-18 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0010_auto_20200418_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyentry',
            name='version',
            field=models.IntegerField(default=14),
        ),
    ]
