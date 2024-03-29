# Generated by Django 3.2.7 on 2021-09-11 05:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('type', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('place', models.CharField(max_length=500)),
                ('payment', models.IntegerField()),
                ('views', models.IntegerField(default=0)),
                ('bids', models.IntegerField(default=0)),
                ('target', models.IntegerField()),
                ('requirements', models.ManyToManyField(to='accounts.Skill')),
                ('reward', models.ManyToManyField(to='listings.Reward')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('work_description', models.ManyToManyField(to='listings.WorkDescription')),
            ],
        ),
    ]
