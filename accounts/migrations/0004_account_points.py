# Generated by Django 3.2.7 on 2021-09-19 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_raters_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
