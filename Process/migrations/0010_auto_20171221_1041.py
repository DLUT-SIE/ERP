# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-21 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Process', '0009_auto_20171219_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processlibrary',
            name='proofread_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='校对日期'),
        ),
        migrations.AlterField(
            model_name='processlibrary',
            name='quota_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='定额日期'),
        ),
        migrations.AlterField(
            model_name='processlibrary',
            name='statistic_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='统计日期'),
        ),
        migrations.AlterField(
            model_name='processlibrary',
            name='write_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='编制日期'),
        ),
        migrations.AlterField(
            model_name='quotalist',
            name='review_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='审核日期'),
        ),
        migrations.AlterField(
            model_name='quotalist',
            name='write_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='编制日期'),
        ),
        migrations.AlterField(
            model_name='transfercard',
            name='approve_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='批准日期'),
        ),
        migrations.AlterField(
            model_name='transfercard',
            name='proofread_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='校对日期'),
        ),
        migrations.AlterField(
            model_name='transfercard',
            name='review_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='审核日期'),
        ),
        migrations.AlterField(
            model_name='transfercard',
            name='write_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='编制日期'),
        ),
        migrations.AlterField(
            model_name='weldingprocessspecification',
            name='approve_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='批准日期'),
        ),
        migrations.AlterField(
            model_name='weldingprocessspecification',
            name='audit_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='审核日期'),
        ),
        migrations.AlterField(
            model_name='weldingprocessspecification',
            name='list_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='编制日期'),
        ),
        migrations.AlterField(
            model_name='weldingworkinstruction',
            name='approve_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='批准日期'),
        ),
        migrations.AlterField(
            model_name='weldingworkinstruction',
            name='audit_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='审核日期'),
        ),
        migrations.AlterField(
            model_name='weldingworkinstruction',
            name='list_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='编制日期'),
        ),
        migrations.AlterField(
            model_name='weldingworkinstruction',
            name='proofread_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='校对日期'),
        ),
    ]