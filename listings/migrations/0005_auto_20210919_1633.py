# Generated by Django 3.2.7 on 2021-09-19 11:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0004_project_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='bids',
        ),
        migrations.RemoveField(
            model_name='project',
            name='views',
        ),
        migrations.AddField(
            model_name='project',
            name='views',
            field=models.ManyToManyField(related_name='views', to=settings.AUTH_USER_MODEL),
        ),
    ]
