# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 08:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Process', '0002_auto_20171206_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processmaterial',
            old_name='net_weight',
            new_name='piece_weight',
        ),
    ]
