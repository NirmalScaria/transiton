# Generated by Django 3.2.6 on 2021-08-21 18:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_conductor_presentbus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='getints',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), size=None),
        ),
        migrations.AlterField(
            model_name='route',
            name='getoutts',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(), size=None),
        ),
    ]