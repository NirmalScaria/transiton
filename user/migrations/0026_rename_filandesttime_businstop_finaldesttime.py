# Generated by Django 3.2.6 on 2021-08-21 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_alter_businstop_filandesttime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businstop',
            old_name='filandesttime',
            new_name='finaldesttime',
        ),
    ]
