# Generated by Django 4.2 on 2023-06-16 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websiteapp', '0005_alter_newmovies_duration_alter_newmovies_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='toprated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bgimage', models.ImageField(upload_to='')),
                ('movieimage', models.ImageField(upload_to='')),
                ('newrel', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('res', models.SlugField()),
                ('genre', models.CharField(max_length=200)),
                ('release', models.DateField()),
                ('duration', models.SlugField()),
                ('plot', models.TextField(max_length=2000)),
                ('ott', models.CharField(max_length=50)),
            ],
        ),
    ]
