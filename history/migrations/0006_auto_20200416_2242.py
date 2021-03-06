# Generated by Django 3.0 on 2020-04-16 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0005_auto_20200416_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyentry',
            name='entry_type',
            field=models.CharField(choices=[('listening', 'Track listening'), ('err_deezer', 'Deezer error'), ('ellipsis_deezer', 'History Ellipsis (Deezer)')], default='listening', max_length=100),
        ),
    ]
