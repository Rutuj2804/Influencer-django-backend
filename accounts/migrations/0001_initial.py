# Generated by Django 3.2.7 on 2021-09-02 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('link', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=500, unique=True, verbose_name='Email')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('instagram', models.CharField(max_length=500)),
                ('facebook', models.CharField(max_length=500)),
                ('youtube', models.CharField(max_length=500)),
                ('isCompany', models.BooleanField(default=False, verbose_name='Is Company')),
                ('photo', models.ImageField(upload_to='display-pictures')),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=100)),
                ('online', models.BooleanField(default=False)),
                ('description', models.TextField(verbose_name='Description')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('links', models.ManyToManyField(to='accounts.Link')),
                ('skills', models.ManyToManyField(to='accounts.Skill')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
