# Generated by Django 3.2.6 on 2021-08-21 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20210821_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businstop',
            name='ithstop',
            field=models.IntegerField(),
        ),
    ]
