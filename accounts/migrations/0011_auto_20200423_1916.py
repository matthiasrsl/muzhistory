# Generated by Django 3.0 on 2020-04-23 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20200418_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='version',
            field=models.IntegerField(default=30),
        ),
    ]
