# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-26 18:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logreg', '0007_auto_20180326_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poke',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokers', to='logreg.User'),
        ),
        migrations.AlterField(
            model_name='poke',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokees', to='logreg.User'),
        ),
    ]
