# Generated by Django 4.2.2 on 2023-08-13 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvshows', '0008_delete_seasonepisodes'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='episode_number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
