# Generated by Django 3.0 on 2020-04-24 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20200423_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='version',
            field=models.IntegerField(default=33),
        ),
    ]
