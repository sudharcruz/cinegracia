# Generated by Django 4.2 on 2023-06-20 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websiteapp', '0011_topseries_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviedetailpage',
            name='video',
            field=models.FileField(null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='topseries',
            name='video',
            field=models.FileField(null=True, upload_to='media/'),
        ),
    ]