# Generated by Django 4.2 on 2023-07-04 08:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('websiteapp', '0022_remove_moviedetailpage_rating_userrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviedetailpage',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]
