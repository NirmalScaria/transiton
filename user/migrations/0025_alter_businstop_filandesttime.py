# Generated by Django 3.2.6 on 2021-08-21 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_alter_businstop_filandesttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businstop',
            name='filandesttime',
            field=models.TimeField(),
        ),
    ]