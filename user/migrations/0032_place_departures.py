# Generated by Django 3.2.6 on 2021-08-22 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_connect'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='departures',
            field=models.ManyToManyField(related_name='_user_place_departures_+', through='user.Connect', to='user.Place'),
        ),
    ]