# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-26 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logreg', '0004_auto_20180326_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poke',
            name='creator',
            field=models.CharField(max_length=255),
        ),
    ]
