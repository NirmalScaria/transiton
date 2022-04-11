# Generated by Django 3.2.6 on 2021-08-23 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0047_route_nstops'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoubleSearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price1', models.IntegerField(default=99)),
                ('price2', models.IntegerField(default=99)),
                ('fromgetint1', models.DateTimeField()),
                ('togetint1', models.DateTimeField()),
                ('fromgetoutt1', models.DateTimeField()),
                ('togetoutt1', models.DateTimeField()),
                ('fromgetint2', models.DateTimeField()),
                ('togetint2', models.DateTimeField()),
                ('fromgetoutt2', models.DateTimeField()),
                ('togetoutt2', models.DateTimeField()),
                ('con1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='con1', to='user.connect')),
                ('con2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='con2', to='user.connect')),
                ('getinp1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gi1d', to='user.place')),
                ('getinp2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gi2d', to='user.place')),
                ('getoutp1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='go1d', to='user.place')),
                ('getoutp2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='go2d', to='user.place')),
                ('route1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r1d', to='user.route')),
                ('route2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r2d', to='user.route')),
            ],
        ),
        migrations.DeleteModel(
            name='SingleSearchResult',
        ),
    ]