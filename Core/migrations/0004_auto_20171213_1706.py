# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-13 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_auto_20171212_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Distribution.Product', verbose_name='产品'),
        ),
    ]
