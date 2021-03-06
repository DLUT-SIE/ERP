# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-03 07:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0004_auto_20171229_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractsteelmaterialrefunddetail',
            name='status',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='auxiliarymaterialapplycard',
            name='apply_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='申请数量'),
        ),
        migrations.AlterField(
            model_name='auxiliarymaterialapplycard',
            name='apply_inventory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apply_inventory', to='Inventory.AuxiliaryMaterialInventoryDetail', verbose_name='库存明细'),
        ),
        migrations.AlterField(
            model_name='boughtincomponentapplydetail',
            name='count',
            field=models.IntegerField(blank=True, null=True, verbose_name='数量'),
        ),
        migrations.AlterField(
            model_name='steelmaterialapplydetail',
            name='count',
            field=models.IntegerField(blank=True, null=True, verbose_name='申请数量'),
        ),
        migrations.AlterField(
            model_name='weldingmaterialapplycard',
            name='apply_count',
            field=models.FloatField(blank=True, null=True, verbose_name='领用数量'),
        ),
        migrations.AlterField(
            model_name='weldingmaterialapplycard',
            name='apply_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='领用重量'),
        ),
        migrations.AlterField(
            model_name='weldingmaterialrefundcard',
            name='weight',
            field=models.FloatField(blank=True, null=True, verbose_name='退库量（重量）'),
        ),
    ]
