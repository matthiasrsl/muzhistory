# Generated by Django 3.0 on 2020-04-17 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_apis', '0004_auto_20200416_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformaccount',
            name='status',
            field=models.CharField(choices=[('act', 'Active'), ('ina', 'Inactive'), ('blo', 'Blocked')], default='act', max_length=3),
        ),
    ]