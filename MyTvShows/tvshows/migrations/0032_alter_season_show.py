# Generated by Django 4.2.2 on 2023-08-17 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tvshows', '0031_season_num_episodes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvshows.temporarysearchresult'),
        ),
    ]
