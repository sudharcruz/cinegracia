# Generated by Django 4.2 on 2023-06-27 13:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('websiteapp', '0015_postcomment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviedetailpage',
            name='favourite',
            field=models.ManyToManyField(blank=True, related_name='favourite', to=settings.AUTH_USER_MODEL),
        ),
    ]
