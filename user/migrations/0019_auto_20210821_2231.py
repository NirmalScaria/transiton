# Generated by Django 3.2.6 on 2021-08-21 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20210821_2231'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusInStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('getint', models.TimeField()),
                ('getoutt', models.TimeField()),
                ('ithstop', models.IntegerField(default=0)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.place')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.route')),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='stops',
            field=models.ManyToManyField(through='user.BusInStop', to='user.Place'),
        ),
    ]