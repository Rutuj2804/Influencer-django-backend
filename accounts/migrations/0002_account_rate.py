# Generated by Django 3.2.7 on 2021-09-12 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='rate',
            field=models.IntegerField(default=0),
        ),
    ]
