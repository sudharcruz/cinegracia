# Generated by Django 4.2 on 2023-08-01 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websiteapp', '0031_moviefavorite_movie_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviefavorite',
            name='movie_poster',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
