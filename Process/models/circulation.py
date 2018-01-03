from django.db import models
from django.contrib.auth.models import User

from Core.utils import DynamicHashPath
from Process import (PROCESS_CHOICES, CIRCULATION_CHOICES,
                     TRANSFER_CARD_CATEGORY_CHOICES, TRANSFER_HEADER_MAP)
from Process.models import ProcessMaterial


class ProcessRoute(models.Model):
    """
    工序路线
    """
    process_material = models.OneToOneField(ProcessMaterial,
                                            verbose_name='物料',
                                            on_delete=models.CASCADE)

    class Meta:
        verbose_name = '工序路线'
        verbose_name_plural = '工序路线'

    def __str__(self):
        return self.process_material.name


class ProcessStep(models.Model):
    route = models.ForeignKey(ProcessRoute, verbose_name='工序路线',
                              related_name='steps',
                              on_delete=models.CASCADE)
    step = models.IntegerField(verbose_name='工序', blank=True, null=True,
                               choices=PROCESS_CHOICES)
    man_hours = models.FloatField(verbose_name='工时', blank=True, null=True)

    class Meta:
        verbose_name = '工序步骤'
        verbose_name_plural = '工序步骤'


class CirculationRoute(models.Model):
    """
    流转路线
    """
    process_material = models.OneToOneField(ProcessMaterial,
                                            verbose_name='物料',
                                            related_name='circulation_route',
                                            on_delete=models.CASCADE)
    C1 = models.IntegerField(verbose_name='路线1', blank=True, null=True,
                             choices=CIRCULATION_CHOICES)
    C2 = models.IntegerField(verbose_name='路线2', blank=True, null=True,
                             choices=CIRCULATION_CHOICES)
    C3 = models.IntegerField(verbose_name='路线3', blank=True, null=True,
                             choices=CIRCULATION_CHOICES)
    C4 = models.IntegerField(verbose_name='路线4', blank=True, null=True,
                             choices=CIRCULATION_CHOICES)
    C5 = models.IntegerField(verbose_name='路线5', blank=True, null=True,
                             choices=CIRCULATION_CHOICES)
    C6 = models.IntegerField(verbose_name='路线6', blank=True, null=True,
                             choices=CIRCULATION_CHOICES)
    C7 = models.IntegerField(verbose_name='路线7', blank=True, null=True,
                             choices=CIRCULATION_CHOICES)
    C8 = models.IntegerField(verbose_name='路线8', blank=True, null=True,
                             choices=CIRCULATION_CHOICES)
    C9 = models.IntegerField(verbose_name='路线9', blank=True, null=True,
                             choices=CIRCULATION_CHOICES)
    C10 = models.IntegerField(verbose_name='路线10', blank=True, null=True,
                              choices=CIRCULATION_CHOICES)

    class Meta:
        verbose_name = '流转路线'
        verbose_name_plural = '流转路线'

    def __str__(self):
        return str(self.process_material)


class TransferCard(models.Model):
    """
    流转卡
    """
    file_index = models.IntegerField(verbose_name='文件编号')
    process_material = models.OneToOneField(ProcessMaterial,
                                            verbose_name='工艺物料',
                                            on_delete=models.CASCADE,
                                            related_name='transfer_card')
    category = models.IntegerField(verbose_name='流转卡类型',
                                   choices=TRANSFER_CARD_CATEGORY_CHOICES)
    container_category = models.CharField(verbose_name='容器类别',
                                          max_length=50,
                                          blank=True, default='')
    parent_name = models.CharField(verbose_name='所属部件名称', max_length=50,
                                   blank=True, default='')
    welding_plate_idx = models.CharField(verbose_name='焊接试板图号',
                                         max_length=50,
                                         blank=True, default='')
    parent_plate_idx = models.CharField(verbose_name='母材试板图号',
                                        max_length=50,
                                        blank=True, default='')
    material_index = models.CharField(verbose_name='材质标记',
                                      max_length=100,
                                      blank=True, default='')
    path = models.FileField(verbose_name='文件路径',
                            upload_to=DynamicHashPath('TransferCard'),
                            blank=True, null=True)
    tech_requirement = models.CharField(verbose_name='技术要求',
                                        max_length=1000,
                                        default='', blank=True)

    writer = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               related_name='transfer_card_writer',
                               on_delete=models.SET_NULL)
    write_dt = models.DateTimeField(verbose_name='编制日期',
                                    blank=True, null=True)
    reviewer = models.ForeignKey(User, verbose_name='审核人',
                                 blank=True, null=True,
                                 related_name='transfer_card_reviewer',
                                 on_delete=models.SET_NULL)
    review_dt = models.DateTimeField(verbose_name='审核日期', blank=True,
                                     null=True)
    proofreader = models.ForeignKey(User, verbose_name='校对人',
                                    blank=True, null=True,
                                    related_name='transfer_card_proofreader',
                                    on_delete=models.SET_NULL)
    proofread_dt = models.DateTimeField(verbose_name='校对日期',
                                        blank=True, null=True)
    approver = models.ForeignKey(User, verbose_name='批准人',
                                 blank=True, null=True,
                                 related_name='transfer_card_approver',
                                 on_delete=models.SET_NULL)
    approve_dt = models.DateTimeField(verbose_name='批准日期',
                                      blank=True, null=True)

    class Meta:
        verbose_name = '流转卡'
        verbose_name_plural = '流转卡'

    def __str__(self):
        return '{}-{:0>2d}'.format(self.basic_file_name, self.file_index)

    @property
    def status(self):
        zipped = zip(
            [self.approver, self.reviewer, self.proofreader, self.writer],
            ['已批准', '已审核', '已校对', '已编制'])
        for signed, status_name in zipped:
            if signed:
                return status_name
        return '初创建'

    @property
    def basic_file_name(self):
        header = TRANSFER_HEADER_MAP.get(self.category, 'RH05')
        return '{}-{}'.format(header,
                              self.process_material.lib.work_order.uid)


class TransferCardProcess(models.Model):
    """
    流转卡工序
    """
    transfer_card = models.ForeignKey(TransferCard, verbose_name='流转卡',
                                      on_delete=models.CASCADE)
    index = models.IntegerField(verbose_name='序号')
    name = models.CharField(verbose_name='工序名', max_length=50,
                            default='', blank=True)
    detail = models.CharField(verbose_name='工艺过程及技术要求',
                              max_length=100, default='', blank=True)

    class Meta:
        verbose_name = '流转卡工序'
        verbose_name_plural = '流转卡工序'

    def __str__(self):
        return '{}-{}-{}'.format(self.transfer_card, self.index, self.name)
