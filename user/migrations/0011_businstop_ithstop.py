# Generated by Django 3.2.6 on 2021-08-21 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20210821_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='businstop',
            name='ithstop',
            field=models.IntegerField(default=0),
        ),
    ]
