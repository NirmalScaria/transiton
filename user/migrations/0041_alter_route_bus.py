# Generated by Django 3.2.6 on 2021-08-22 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0040_rename_pathid_connect_connectid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='bus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='user.bus'),
        ),
    ]
