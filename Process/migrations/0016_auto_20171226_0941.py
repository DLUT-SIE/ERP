# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-26 01:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Process', '0015_auto_20171223_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='principalquotaitem',
            name='lib',
            field=models.ForeignKey(default=2012, on_delete=django.db.models.deletion.CASCADE, to='Process.ProcessLibrary', verbose_name='工艺库'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weldingquotaitem',
            name='lib',
            field=models.ForeignKey(default=20121212, on_delete=django.db.models.deletion.CASCADE, to='Process.ProcessLibrary', verbose_name='工艺库'),
            preserve_default=False,
        ),
    ]
