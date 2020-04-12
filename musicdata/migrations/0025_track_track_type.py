# Generated by Django 3.0 on 2020-04-11 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdata', '0024_merge_20200410_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='track_type',
            field=models.CharField(choices=[('deezer_track', 'Deezer track'), ('deezer_mp3', "Deezer user's mp3")], default='deezer_track', max_length=20),
            preserve_default=False,
        ),
    ]
