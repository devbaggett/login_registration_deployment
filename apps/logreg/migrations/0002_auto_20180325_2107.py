# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-26 04:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logreg', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]