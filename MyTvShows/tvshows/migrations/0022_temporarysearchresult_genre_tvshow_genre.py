# Generated by Django 4.2.2 on 2023-08-16 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvshows', '0021_rename_num_episodes_temporarysearchresult_seasons_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporarysearchresult',
            name='genre',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tvshow',
            name='genre',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
