# Generated by Django 3.0 on 2020-04-17 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_profile_last_history_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='version',
            field=models.IntegerField(default=11),
        ),
    ]
