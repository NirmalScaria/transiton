# Generated by Django 3.2.6 on 2021-08-21 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_businstop_finaldest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businstop',
            name='finaldest',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='finaldest', to='user.place'),
        ),
    ]
