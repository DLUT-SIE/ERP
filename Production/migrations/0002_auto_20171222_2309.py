# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-22 15:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processdetail',
            name='actual_finish_date',
        ),
        migrations.RemoveField(
            model_name='processdetail',
            name='estimated_finish_date',
        ),
        migrations.RemoveField(
            model_name='processdetail',
            name='estimated_start_date',
        ),
        migrations.RemoveField(
            model_name='processdetail',
            name='inspection_date',
        ),
        migrations.RemoveField(
            model_name='productionplan',
            name='plan_date',
        ),
        migrations.RemoveField(
            model_name='submaterial',
            name='actual_finish_date',
        ),
        migrations.RemoveField(
            model_name='submaterial',
            name='estimated_finish_date',
        ),
        migrations.AddField(
            model_name='processdetail',
            name='actual_finish_dt',
            field=models.DateTimeField(blank=True, null=True, verbose_name='实际完成日期'),
        ),
        migrations.AddField(
            model_name='processdetail',
            name='estimated_finish_dt',
            field=models.DateTimeField(blank=True, null=True, verbose_name='计划完成日期'),
        ),
        migrations.AddField(
            model_name='processdetail',
            name='estimated_start_dt',
            field=models.DateTimeField(blank=True, null=True, verbose_name='计划开始日期'),
        ),
        migrations.AddField(
            model_name='processdetail',
            name='inspection_dt',
            field=models.DateTimeField(blank=True, null=True, verbose_name='检查时间'),
        ),
        migrations.AddField(
            model_name='productionplan',
            name='plan_dt',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='计划年月'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submaterial',
            name='actual_finish_dt',
            field=models.DateTimeField(blank=True, null=True, verbose_name='实际完成日期'),
        ),
        migrations.AddField(
            model_name='submaterial',
            name='estimated_finish_dt',
            field=models.DateTimeField(blank=True, null=True, verbose_name='计划完成日期'),
        ),
    ]
