# Generated by Django 4.2.2 on 2023-08-17 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvshows', '0038_alter_temporarysearchresult_poster_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvshow',
            name='tvmaze_id',
            field=models.CharField(max_length=20),
        ),
    ]
