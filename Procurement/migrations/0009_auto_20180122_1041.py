# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-22 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Procurement', '0008_auto_20180118_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='category',
            field=models.IntegerField(default=0, verbose_name='标单类型'),
        ),
    ]
