# Generated by Django 4.2.2 on 2023-08-17 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tvshows', '0024_remove_genre_series_remove_season_episodes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temporarysearchresult',
            old_name='imdb_id',
            new_name='tvmaze_id',
        ),
        migrations.RenameField(
            model_name='tvshow',
            old_name='imdb_id',
            new_name='tvmaze_id',
        ),
    ]
