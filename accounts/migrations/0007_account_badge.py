# Generated by Django 3.2.7 on 2021-12-04 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211005_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='badge',
            field=models.IntegerField(default=1),
        ),
    ]
