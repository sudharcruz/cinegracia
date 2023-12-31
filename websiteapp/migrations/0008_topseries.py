# Generated by Django 4.2 on 2023-06-17 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websiteapp', '0007_topmovies'),
    ]

    operations = [
        migrations.CreateModel(
            name='topseries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seriesname', models.CharField(max_length=100)),
                ('release', models.CharField(max_length=100)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('image', models.ImageField(upload_to='')),
                ('duration', models.SlugField(max_length=100)),
            ],
        ),
    ]
