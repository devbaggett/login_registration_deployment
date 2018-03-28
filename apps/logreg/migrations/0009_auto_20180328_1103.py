# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-28 18:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logreg', '0008_auto_20180326_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='poke',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='poke',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='user',
            name='alias',
        ),
        migrations.DeleteModel(
            name='Poke',
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='logreg.User'),
        ),
    ]
