# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-13 09:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Distribution', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': '产品', 'verbose_name_plural': '产品'},
        ),
    ]
