# Generated by Django 3.2.6 on 2021-08-21 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_alter_businstop_finaldest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='stops',
        ),
        migrations.DeleteModel(
            name='BusInStop',
        ),
    ]