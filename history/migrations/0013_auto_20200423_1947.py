# Generated by Django 3.0 on 2020-04-23 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0012_auto_20200423_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyentry',
            name='version',
            field=models.IntegerField(default=32),
        ),
    ]
