# Generated by Django 3.2.6 on 2021-08-21 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210821_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus',
            name='routes',
        ),
    ]
