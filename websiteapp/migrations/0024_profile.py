# Generated by Django 4.2 on 2023-07-07 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('websiteapp', '0023_moviedetailpage_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dp', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('insta_url', models.CharField(blank=True, max_length=300, null=True)),
                ('fb_url', models.CharField(blank=True, max_length=300, null=True)),
                ('bio', models.TextField(blank=True, max_length=2000, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]