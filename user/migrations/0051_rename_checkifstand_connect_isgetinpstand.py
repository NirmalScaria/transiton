# Generated by Django 3.2.6 on 2021-08-24 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0050_connect_checkifstand'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connect',
            old_name='checkifstand',
            new_name='isgetinpstand',
        ),
    ]
