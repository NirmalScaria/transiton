# Generated by Django 3.2.6 on 2021-08-22 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0035_auto_20210822_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connect',
            name='pathid',
            field=models.CharField(max_length=1000, primary_key=True, serialize=False),
        ),
    ]
