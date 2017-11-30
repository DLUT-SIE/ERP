# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-30 04:33
from __future__ import unicode_literals

import Core.utils.hash
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Core', '0002_auto_20171130_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuxiliaryQuotaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='备注')),
                ('quota_coef', models.FloatField(verbose_name='定额系数')),
                ('quota', models.FloatField(verbose_name='定额')),
                ('stardard_code', models.CharField(blank=True, default='', max_length=50, verbose_name='标准代码')),
                ('category', models.CharField(blank=True, default='', max_length=50, verbose_name='类别')),
            ],
            options={
                'verbose_name': '辅材定额',
                'verbose_name_plural': '辅材定额',
            },
        ),
        migrations.CreateModel(
            name='BoughtInItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='备注')),
            ],
            options={
                'verbose_name': '外购件',
                'verbose_name_plural': '外购件',
            },
        ),
        migrations.CreateModel(
            name='CirculationRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('C1', models.IntegerField(blank=True, choices=[(0, 'H1'), (1, 'J'), (4, 'ZM'), (3, 'R'), (5, 'GY'), (6, 'DY'), (7, 'XZ')], null=True, verbose_name='路线1')),
                ('C2', models.IntegerField(blank=True, choices=[(0, 'H1'), (1, 'J'), (4, 'ZM'), (3, 'R'), (5, 'GY'), (6, 'DY'), (7, 'XZ')], null=True, verbose_name='路线2')),
                ('C3', models.IntegerField(blank=True, choices=[(0, 'H1'), (1, 'J'), (4, 'ZM'), (3, 'R'), (5, 'GY'), (6, 'DY'), (7, 'XZ')], null=True, verbose_name='路线3')),
                ('C4', models.IntegerField(blank=True, choices=[(0, 'H1'), (1, 'J'), (4, 'ZM'), (3, 'R'), (5, 'GY'), (6, 'DY'), (7, 'XZ')], null=True, verbose_name='路线4')),
                ('C5', models.IntegerField(blank=True, choices=[(0, 'H1'), (1, 'J'), (4, 'ZM'), (3, 'R'), (5, 'GY'), (6, 'DY'), (7, 'XZ')], null=True, verbose_name='路线5')),
                ('C6', models.IntegerField(blank=True, choices=[(0, 'H1'), (1, 'J'), (4, 'ZM'), (3, 'R'), (5, 'GY'), (6, 'DY'), (7, 'XZ')], null=True, verbose_name='路线6')),
                ('C7', models.IntegerField(blank=True, choices=[(0, 'H1'), (1, 'J'), (4, 'ZM'), (3, 'R'), (5, 'GY'), (6, 'DY'), (7, 'XZ')], null=True, verbose_name='路线7')),
                ('C8', models.IntegerField(blank=True, choices=[(0, 'H1'), (1, 'J'), (4, 'ZM'), (3, 'R'), (5, 'GY'), (6, 'DY'), (7, 'XZ')], null=True, verbose_name='路线8')),
                ('C9', models.IntegerField(blank=True, choices=[(0, 'H1'), (1, 'J'), (4, 'ZM'), (3, 'R'), (5, 'GY'), (6, 'DY'), (7, 'XZ')], null=True, verbose_name='路线9')),
                ('C10', models.IntegerField(blank=True, choices=[(0, 'H1'), (1, 'J'), (4, 'ZM'), (3, 'R'), (5, 'GY'), (6, 'DY'), (7, 'XZ')], null=True, verbose_name='路线10')),
            ],
            options={
                'verbose_name': '流转路线',
                'verbose_name_plural': '流转路线',
            },
        ),
        migrations.CreateModel(
            name='CooperantItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='备注')),
            ],
            options={
                'verbose_name': '外协件',
                'verbose_name_plural': '外协件',
            },
        ),
        migrations.CreateModel(
            name='FirstFeedingItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='备注')),
            ],
            options={
                'verbose_name': '先投件',
                'verbose_name_plural': '先投件',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='材质名称')),
                ('uid', models.CharField(max_length=20, unique=True, verbose_name='材质编号')),
                ('category', models.IntegerField(choices=[(1, '焊条'), (2, '焊丝'), (3, '焊带'), (4, '焊剂'), (5, '板材'), (6, '型材'), (7, '外购件'), (8, '辅助工具'), (0, '其他')], verbose_name='材质类别')),
            ],
            options={
                'verbose_name': '材质',
                'verbose_name_plural': '材质',
            },
        ),
        migrations.CreateModel(
            name='PrincipalQuotaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, default='', max_length=50, verbose_name='规格')),
                ('count', models.IntegerField(verbose_name='数量')),
                ('weight', models.FloatField(verbose_name='单重')),
                ('operative_norm', models.CharField(blank=True, default='', max_length=50, verbose_name='执行标准')),
                ('status', models.CharField(blank=True, default='', max_length=50, verbose_name='供货状态')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='备注')),
            ],
            options={
                'verbose_name': '主材定额',
                'verbose_name_plural': '主材定额',
            },
        ),
        migrations.CreateModel(
            name='ProcessLibrary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('write_date', models.DateField(blank=True, null=True, verbose_name='编制日期')),
                ('quota_date', models.DateField(blank=True, null=True, verbose_name='定额日期')),
                ('proofread_date', models.DateField(blank=True, null=True, verbose_name='校对日期')),
                ('statistic_date', models.DateField(blank=True, null=True, verbose_name='统计日期')),
            ],
            options={
                'verbose_name': '工艺库',
                'verbose_name_plural': '工艺库',
            },
        ),
        migrations.CreateModel(
            name='ProcessMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number', models.IntegerField(verbose_name='票号')),
                ('part_number', models.IntegerField(verbose_name='件号')),
                ('drawing_number', models.CharField(blank=True, default='', max_length=50, verbose_name='图号')),
                ('parent_drawing_number', models.CharField(blank=True, default='', max_length=50, verbose_name='所属图号')),
                ('spec', models.CharField(blank=True, default='', max_length=20, verbose_name='规格')),
                ('count', models.IntegerField(verbose_name='数量')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='名称')),
                ('net_weight', models.FloatField(verbose_name='净重')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='备注')),
            ],
            options={
                'verbose_name': '工艺物料',
                'verbose_name_plural': '工艺物料',
            },
        ),
        migrations.CreateModel(
            name='ProcessReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.CharField(blank=True, default='', max_length=200, verbose_name='存在问题')),
                ('advice', models.CharField(blank=True, default='', max_length=200, verbose_name='改进建议')),
            ],
            options={
                'verbose_name': '工艺性审查表',
                'verbose_name_plural': '工艺性审查表',
            },
        ),
        migrations.CreateModel(
            name='ProcessRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('S1', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序1')),
                ('H1', models.FloatField(blank=True, null=True, verbose_name='工时1')),
                ('S2', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序2')),
                ('H2', models.FloatField(blank=True, null=True, verbose_name='工时2')),
                ('S3', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序3')),
                ('H3', models.FloatField(blank=True, null=True, verbose_name='工时3')),
                ('S4', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序4')),
                ('H4', models.FloatField(blank=True, null=True, verbose_name='工时4')),
                ('S5', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序5')),
                ('H5', models.FloatField(blank=True, null=True, verbose_name='工时5')),
                ('S6', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序6')),
                ('H6', models.FloatField(blank=True, null=True, verbose_name='工时6')),
                ('S7', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序7')),
                ('H7', models.FloatField(blank=True, null=True, verbose_name='工时7')),
                ('S8', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序8')),
                ('H8', models.FloatField(blank=True, null=True, verbose_name='工时8')),
                ('S9', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序9')),
                ('H9', models.FloatField(blank=True, null=True, verbose_name='工时9')),
                ('S10', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序10')),
                ('H10', models.FloatField(blank=True, null=True, verbose_name='工时10')),
                ('S11', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序11')),
                ('H11', models.FloatField(blank=True, null=True, verbose_name='工时11')),
                ('S12', models.IntegerField(blank=True, choices=[(0, 'W'), (1, 'W1'), (2, 'W2'), (3, 'W3'), (4, 'W4'), (5, 'W5'), (6, 'W6'), (7, 'W25'), (8, 'P01'), (9, 'P02'), (10, 'R'), (11, 'R1'), (12, 'R2'), (13, 'Z'), (14, 'H'), (15, 'M'), (16, 'L'), (17, 'Y'), (18, 'G'), (19, 'G1'), (20, 'G2'), (21, 'G3'), (22, 'G4'), (23, 'G5'), (24, 'X'), (25, 'J'), (28, 'D'), (27, 'D2'), (26, 'K')], null=True, verbose_name='工序12')),
                ('H12', models.FloatField(blank=True, null=True, verbose_name='工时12')),
            ],
            options={
                'verbose_name': '工序路线',
                'verbose_name_plural': '工序路线',
            },
        ),
        migrations.CreateModel(
            name='ProgrammingBlankingChart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(upload_to=Core.utils.hash.DynamicHashPath('ProgrammingBlankingChart'), verbose_name='路径')),
                ('upload_dt', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
            ],
            options={
                'verbose_name': '编程套料图',
                'verbose_name_plural': '编程套料图',
            },
        ),
        migrations.CreateModel(
            name='QuotaList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('write_date', models.DateField(blank=True, null=True, verbose_name='编制日期')),
                ('review_date', models.DateField(blank=True, null=True, verbose_name='审核日期')),
                ('category', models.IntegerField(choices=[(0, '辅材定额明细表'), (1, '主材定额明细表'), (2, '工序性外协明细表'), (3, '先投件明细表'), (4, '外购件明细表'), (5, '焊缝明细表'), (8, '装箱外购件明细表'), (9, '设计库表'), (10, '焊材明细表')], verbose_name='明细表类别')),
                ('lib', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Process.ProcessLibrary', verbose_name='工艺库')),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quota_list_reviewer', to=settings.AUTH_USER_MODEL, verbose_name='审核人')),
                ('writer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quota_list_writer', to=settings.AUTH_USER_MODEL, verbose_name='编制人')),
            ],
            options={
                'verbose_name': '定额明细表',
                'verbose_name_plural': '定额明细表',
            },
        ),
        migrations.CreateModel(
            name='TransferCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(choices=[(0, '筒体流转卡'), (1, '封头流转卡'), (2, '焊接试板流转卡'), (3, '母材试板流转卡'), (4, '受压元件流转卡'), (5, '特别元件流转卡')], verbose_name='流转卡类型')),
                ('container_category', models.CharField(blank=True, default='', max_length=50, verbose_name='容器类别')),
                ('parent_name', models.CharField(blank=True, default='', max_length=50, verbose_name='所属部件名称')),
                ('welding_plate_idx', models.CharField(blank=True, default='', max_length=50, verbose_name='焊接试板图号')),
                ('parent_plate_idx', models.CharField(blank=True, default='', max_length=50, verbose_name='母材试板图号')),
                ('material_index', models.CharField(blank=True, default='', max_length=100, verbose_name='材质标记')),
                ('path', models.FileField(blank=True, null=True, upload_to=Core.utils.hash.DynamicHashPath('TransferCard'), verbose_name='文件路径')),
                ('tech_requirement', models.CharField(blank=True, default='', max_length=1000, verbose_name='技术要求')),
                ('write_date', models.DateField(blank=True, null=True, verbose_name='编制日期')),
                ('review_date', models.DateField(blank=True, null=True, verbose_name='审核日期')),
                ('proofread_date', models.DateField(blank=True, null=True, verbose_name='校对日期')),
                ('approve_date', models.DateField(blank=True, null=True, verbose_name='批准日期')),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfer_card_approver', to=settings.AUTH_USER_MODEL, verbose_name='批准人')),
                ('materiel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Process.ProcessMaterial', verbose_name='工艺物料')),
                ('proofreader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfer_card_proofreader', to=settings.AUTH_USER_MODEL, verbose_name='校对人')),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfer_card_reviewer', to=settings.AUTH_USER_MODEL, verbose_name='审核人')),
                ('writer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfer_card_writer', to=settings.AUTH_USER_MODEL, verbose_name='编制人')),
            ],
            options={
                'verbose_name': '流转卡',
                'verbose_name_plural': '流转卡',
            },
        ),
        migrations.CreateModel(
            name='TransferCardProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(verbose_name='序号')),
                ('name', models.CharField(blank=True, default='', max_length=50, verbose_name='工序名')),
                ('detail', models.CharField(blank=True, default='', max_length=100, verbose_name='工艺过程及技术要求')),
                ('transfer_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Process.TransferCard', verbose_name='流转卡')),
            ],
            options={
                'verbose_name': '流转卡工序',
                'verbose_name_plural': '流转卡工序',
            },
        ),
        migrations.CreateModel(
            name='WeldingCertification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='持证项目')),
                ('weld_method', models.IntegerField(choices=[(0, '焊条电弧焊'), (1, '埋弧焊'), (2, '气体保护焊'), (3, '氩弧焊')], verbose_name='焊接方法')),
            ],
            options={
                'verbose_name': '焊工持证项目',
                'verbose_name_plural': '焊工持证项目',
            },
        ),
        migrations.CreateModel(
            name='WeldingJointProcessAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joint_index', models.CharField(blank=True, default='', max_length=50, verbose_name='接头编号')),
                ('proc_qual_index', models.IntegerField(choices=[(0, 'RH24-13-09'), (1, 'RH24-13-36')], verbose_name='焊接工艺评定编号')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='备注')),
            ],
            options={
                'verbose_name': '焊接接头工艺分析',
                'verbose_name_plural': '焊接接头工艺分析',
            },
        ),
        migrations.CreateModel(
            name='WeldingLayerCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layer', models.IntegerField(verbose_name='层/道')),
                ('weld_method', models.IntegerField(choices=[(0, '焊条电弧焊'), (1, '埋弧焊'), (2, '气体保护焊'), (3, '氩弧焊')], verbose_name='焊接方法')),
                ('polarity', models.CharField(blank=True, default='', max_length=10, verbose_name='极性')),
                ('electricity', models.CharField(blank=True, default='', max_length=10, verbose_name='电流')),
                ('voltage', models.CharField(blank=True, default='', max_length=10, verbose_name='电流电压')),
                ('welding_speed', models.CharField(blank=True, default='', max_length=10, verbose_name='焊接速度')),
                ('heat_input', models.CharField(blank=True, default='', max_length=10, verbose_name='线能量')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='备注')),
            ],
            options={
                'verbose_name': '焊接层道卡',
                'verbose_name_plural': '焊接层道卡',
            },
        ),
        migrations.CreateModel(
            name='WeldingProcessSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_date', models.DateField(blank=True, null=True, verbose_name='编制日期')),
                ('audit_date', models.DateField(blank=True, null=True, verbose_name='审核日期')),
                ('approve_date', models.DateField(blank=True, null=True, verbose_name='批准日期')),
                ('path', models.FileField(blank=True, null=True, upload_to=Core.utils.hash.DynamicHashPath('WeldingProcSpec'), verbose_name='文件路径')),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_proc_sped_approver', to=settings.AUTH_USER_MODEL, verbose_name='批准人')),
                ('auditor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_proc_spec_auditor', to=settings.AUTH_USER_MODEL, verbose_name='审核人')),
                ('lister', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_proc_spec_lister', to=settings.AUTH_USER_MODEL, verbose_name='编制人')),
                ('work_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.WorkOrder', verbose_name='所属工作令')),
            ],
            options={
                'verbose_name': '焊接工艺规程',
                'verbose_name_plural': '焊接工艺规程',
            },
        ),
        migrations.CreateModel(
            name='WeldingQuotaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, default='', max_length=50, verbose_name='规格')),
                ('quota', models.FloatField(verbose_name='定额')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='备注')),
                ('operative_norm', models.CharField(blank=True, default='', max_length=50, verbose_name='执行标准')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Process.Material', verbose_name='材质')),
                ('quota_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Process.QuotaList', verbose_name='定额明细表')),
            ],
            options={
                'verbose_name': '焊材定额',
                'verbose_name_plural': '焊材定额',
            },
        ),
        migrations.CreateModel(
            name='WeldingSeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, default='', max_length=50, verbose_name='焊缝编号')),
                ('seam_type', models.CharField(max_length=50, verbose_name='类型名')),
                ('weld_position', models.IntegerField(choices=[(0, '平焊'), (1, '横焊'), (2, '仰焊'), (3, '立向上焊'), (4, '全位置焊')], verbose_name='焊接位置')),
                ('weld_method_1', models.IntegerField(blank=True, choices=[(0, '焊条电弧焊'), (1, '埋弧焊'), (2, '气体保护焊'), (3, '氩弧焊')], null=True, verbose_name='焊接方法_1')),
                ('weld_method_2', models.IntegerField(blank=True, choices=[(0, '焊条电弧焊'), (1, '埋弧焊'), (2, '气体保护焊'), (3, '氩弧焊')], null=True, verbose_name='焊接方法_2')),
                ('bm_1', models.CharField(blank=True, default='', max_length=50, verbose_name='母材材质_1')),
                ('bm_thick_1', models.FloatField(verbose_name='母材厚度_1')),
                ('bm_2', models.CharField(blank=True, default='', max_length=50, verbose_name='母材材质_2')),
                ('bm_thick_2', models.FloatField(verbose_name='母材厚度2')),
                ('length', models.FloatField(verbose_name='长度')),
                ('wt_1', models.CharField(blank=True, default='', max_length=100, verbose_name='焊材厚度_1')),
                ('ws_1', models.CharField(blank=True, default='', max_length=100, verbose_name='规格_1')),
                ('weight_1', models.FloatField(default=0, verbose_name='焊材重量_1')),
                ('wf_weight_1', models.FloatField(default=0, verbose_name='焊剂重量_1')),
                ('wt_2', models.CharField(blank=True, default='', max_length=200, verbose_name='焊材厚度_2')),
                ('ws_2', models.CharField(blank=True, default='', max_length=200, verbose_name='规格_2')),
                ('weight_2', models.FloatField(default=0, verbose_name='焊材重量_2')),
                ('wf_weight_2', models.FloatField(default=0, verbose_name='焊剂重量_2')),
                ('remark', models.CharField(blank=True, default='', max_length=50, verbose_name='备注')),
                ('analysis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Process.WeldingJointProcessAnalysis', verbose_name='焊接接头工艺分析')),
                ('materiel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Process.ProcessMaterial', verbose_name='物料')),
                ('wf_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_seam_flux_1', to='Process.Material', verbose_name='焊丝/焊条_1_焊剂')),
                ('wf_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_seam_flux_2', to='Process.Material', verbose_name='焊丝/焊条_2_焊剂')),
                ('wm_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_seam_material_1', to='Process.Material', verbose_name='焊丝/焊条_1_材质')),
                ('wm_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_seam_material_2', to='Process.Material', verbose_name='焊丝/焊条_2_材质')),
            ],
            options={
                'verbose_name': '焊缝',
                'verbose_name_plural': '焊缝',
            },
        ),
        migrations.CreateModel(
            name='WeldingWorkInstruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_date', models.DateField(blank=True, null=True, verbose_name='编制日期')),
                ('audit_date', models.DateField(blank=True, null=True, verbose_name='审核日期')),
                ('proofread_date', models.DateField(blank=True, null=True, verbose_name='校对日期')),
                ('approve_date', models.DateField(blank=True, null=True, verbose_name='批准日期')),
                ('path', models.FileField(blank=True, null=True, upload_to=Core.utils.hash.DynamicHashPath('WeldingWorkInstruction'), verbose_name='路径')),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_work_inst_approver', to=settings.AUTH_USER_MODEL, verbose_name='批准人')),
                ('auditor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_work_inst_auditor', to=settings.AUTH_USER_MODEL, verbose_name='审核人')),
                ('detail', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Process.WeldingJointProcessAnalysis', verbose_name='焊接接头工艺分析')),
                ('lister', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_work_inst_lister', to=settings.AUTH_USER_MODEL, verbose_name='编制人')),
                ('proofreader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weld_work_inst_proofreader', to=settings.AUTH_USER_MODEL, verbose_name='校对人')),
            ],
            options={
                'verbose_name': '焊接作业指导书',
                'verbose_name_plural': '焊接作业指导书',
            },
        ),
        migrations.CreateModel(
            name='WeldingWorkInstructionExamination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(verbose_name='序号')),
                ('surveyor', models.IntegerField(blank=True, choices=[(0, '厂内'), (1, '检验机构'), (2, '第三方或用户')], null=True, verbose_name='检验方')),
                ('instruction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Process.WeldingWorkInstruction', verbose_name='焊接作业指导书')),
            ],
            options={
                'verbose_name': '焊接作业检验',
                'verbose_name_plural': '焊接作业检验',
            },
        ),
        migrations.CreateModel(
            name='WeldingWorkInstructionProcess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(verbose_name='序号')),
                ('name', models.CharField(blank=True, default='', max_length=50, verbose_name='工序名')),
                ('detail', models.CharField(blank=True, default='', max_length=100, verbose_name='工艺过程及技术要求')),
                ('instruction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Process.WeldingWorkInstruction', verbose_name='焊接作业指导书')),
            ],
            options={
                'verbose_name': '焊接作业指导书工序',
                'verbose_name_plural': '焊接作业指导书工序',
            },
        ),
        migrations.AddField(
            model_name='weldinglayercard',
            name='instruction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Process.WeldingWorkInstruction', verbose_name='焊接作业指导书'),
        ),
        migrations.AddField(
            model_name='weldingjointprocessanalysis',
            name='spec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Process.WeldingProcessSpecification', verbose_name='焊接工艺规程'),
        ),
        migrations.AddField(
            model_name='weldingjointprocessanalysis',
            name='weld_cert_1',
            field=models.ManyToManyField(related_name='joint_analysis_cert_1', to='Process.WeldingCertification', verbose_name='焊工持证项目_1'),
        ),
        migrations.AddField(
            model_name='weldingjointprocessanalysis',
            name='weld_cert_2',
            field=models.ManyToManyField(related_name='joint_analysis_cert_2', to='Process.WeldingCertification', verbose_name='焊工持证项目_2'),
        ),
    ]
