# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-24 20:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Procurement', '0004_auto_20171223_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotations', to='Procurement.Supplier', verbose_name='供应商'),
        ),
        migrations.AlterField(
            model_name='supplierdocument',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docs', to='Procurement.Supplier', verbose_name='供应商'),
        ),
    ]