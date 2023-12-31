# Generated by Django 4.2.2 on 2023-07-16 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tvshows', '0004_alter_show_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonEpisodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_episodes', models.PositiveIntegerField()),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvshows.season')),
            ],
        ),
    ]
