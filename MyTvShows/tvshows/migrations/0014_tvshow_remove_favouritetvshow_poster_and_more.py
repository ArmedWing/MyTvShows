# Generated by Django 4.2.2 on 2023-08-16 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvshows', '0013_favouritetvshow_poster_favouritetvshow_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TVShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=10)),
                ('imdb_id', models.CharField(max_length=20, unique=True)),
                ('poster', models.URLField()),
            ],
        ),
        migrations.RemoveField(
            model_name='favouritetvshow',
            name='Poster',
        ),
        migrations.RemoveField(
            model_name='favouritetvshow',
            name='Title',
        ),
        migrations.RemoveField(
            model_name='favouritetvshow',
            name='Year',
        ),
        migrations.RemoveField(
            model_name='favouritetvshow',
            name='imdbID',
        ),
    ]
