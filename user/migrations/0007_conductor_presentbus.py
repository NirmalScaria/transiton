# Generated by Django 3.2.6 on 2021-08-21 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_bus_routes'),
    ]

    operations = [
        migrations.AddField(
            model_name='conductor',
            name='presentbus',
            field=models.ManyToManyField(related_name='conductorpresentbus', to='user.Bus'),
        ),
    ]
