# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-06 03:21
from __future__ import unicode_literals

import Core.utils.hash
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='标题')),
                ('content', models.TextField(blank=True, verbose_name='内容')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('category', models.IntegerField(choices=[(0, '公司新闻'), (1, '重要通知'), (2, '个人消息')], verbose_name='类型')),
                ('read', models.BooleanField(default=False, verbose_name='是否阅读')),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_recipient', to=settings.AUTH_USER_MODEL, verbose_name='接收者')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_source', to=settings.AUTH_USER_MODEL, verbose_name='发送者')),
            ],
            options={
                'verbose_name': '消息',
                'verbose_name_plural': '消息',
            },
        ),
        migrations.CreateModel(
            name='MessageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(upload_to=Core.utils.hash.DynamicHashPath('MessageFile'), verbose_name='路径')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Messaging.Message', verbose_name='消息')),
            ],
            options={
                'verbose_name': '消息文件',
                'verbose_name_plural': '消息文件',
            },
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('Messaging.message',),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('Messaging.message',),
        ),
        migrations.CreateModel(
            name='PersonalMessage',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('Messaging.message',),
        ),
    ]
