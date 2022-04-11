# Generated by Django 3.2.6 on 2021-08-21 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_sotptype_place_stoptype'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='district',
            field=models.CharField(default='UNKNOWN', max_length=200),
        ),
        migrations.AddField(
            model_name='place',
            name='gplaceid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='place',
            name='state',
            field=models.CharField(default='Kerala', max_length=200),
        ),
    ]
