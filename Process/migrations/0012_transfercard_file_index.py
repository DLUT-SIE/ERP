# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-21 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Process', '0011_auto_20171221_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfercard',
            name='file_index',
            field=models.IntegerField(default=0, verbose_name='文件编号'),
            preserve_default=False,
        ),
    ]
