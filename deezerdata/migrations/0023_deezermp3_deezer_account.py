# Generated by Django 3.0 on 2020-04-16 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deezerdata', '0022_auto_20200416_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='deezermp3',
            name='deezer_account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='deezerdata.DeezerAccount'),
            preserve_default=False,
        ),
    ]