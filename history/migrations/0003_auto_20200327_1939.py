# Generated by Django 3.0 on 2020-03-27 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_historyentry_entry_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyentry',
            name='version',
            field=models.IntegerField(default=10),
        ),
    ]
