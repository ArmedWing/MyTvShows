# Generated by Django 4.2.2 on 2023-08-17 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvshows', '0036_alter_temporarysearchresult_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporarysearchresult',
            name='poster',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='tvshow',
            name='poster',
            field=models.URLField(max_length=500),
        ),
    ]
