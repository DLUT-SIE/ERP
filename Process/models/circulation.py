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
    materiel = models.OneToOneField(ProcessMaterial, verbose_name='物料',
                                    on_delete=models.CASCADE)
    S1 = models.IntegerField(verbose_name='工序1', blank=True, null=True,
                             choices=PROCESS_CHOICES)
    H1 = models.FloatField(verbose_name='工时1', blank=True, null=True)
    S2 = models.IntegerField(verbose_name='工序2', blank=True, null=True,
                             choices=PROCESS_CHOICES)
    H2 = models.FloatField(verbose_name='工时2', blank=True, null=True)
    S3 = models.IntegerField(verbose_name='工序3', blank=True, null=True,
                             choices=PROCESS_CHOICES)
    H3 = models.FloatField(verbose_name='工时3', blank=True, null=True)
    S4 = models.IntegerField(verbose_name='工序4', blank=True, null=True,
                             choices=PROCESS_CHOICES)
    H4 = models.FloatField(verbose_name='工时4', blank=True, null=True)
    S5 = models.IntegerField(verbose_name='工序5', blank=True, null=True,
                             choices=PROCESS_CHOICES)
    H5 = models.FloatField(verbose_name='工时5', blank=True, null=True)
    S6 = models.IntegerField(verbose_name='工序6', blank=True, null=True,
                             choices=PROCESS_CHOICES)
    H6 = models.FloatField(verbose_name='工时6', blank=True, null=True)
    S7 = models.IntegerField(verbose_name='工序7', blank=True, null=True,
                             choices=PROCESS_CHOICES)
    H7 = models.FloatField(verbose_name='工时7', blank=True, null=True)
    S8 = models.IntegerField(verbose_name='工序8', blank=True, null=True,
                             choices=PROCESS_CHOICES)
    H8 = models.FloatField(verbose_name='工时8', blank=True, null=True)
    S9 = models.IntegerField(verbose_name='工序9', blank=True, null=True,
                             choices=PROCESS_CHOICES)
    H9 = models.FloatField(verbose_name='工时9', blank=True, null=True)
    S10 = models.IntegerField(verbose_name='工序10', blank=True, null=True,
                              choices=PROCESS_CHOICES)
    H10 = models.FloatField(verbose_name='工时10', blank=True, null=True)
    S11 = models.IntegerField(verbose_name='工序11', blank=True, null=True,
                              choices=PROCESS_CHOICES)
    H11 = models.FloatField(verbose_name='工时11', blank=True, null=True)
    S12 = models.IntegerField(verbose_name='工序12', blank=True, null=True,
                              choices=PROCESS_CHOICES)
    H12 = models.FloatField(verbose_name='工时12', blank=True, null=True)

    class Meta:
        verbose_name = '工序路线'
        verbose_name_plural = '工序路线'

    def __str__(self):
        return self.materiel.name


class CirculationRoute(models.Model):
    """
    流转路线
    """
    materiel = models.OneToOneField(ProcessMaterial, verbose_name='物料',
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
        return str(self.materiel)


class TransferCard(models.Model):
    """
    流转卡
    """
    materiel = models.ForeignKey(ProcessMaterial, verbose_name='工艺物料',
                                 on_delete=models.CASCADE)
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
    write_date = models.DateField(verbose_name='编制日期',
                                  blank=True, null=True)
    reviewer = models.ForeignKey(User, verbose_name='审核人',
                                 blank=True, null=True,
                                 related_name='transfer_card_reviewer',
                                 on_delete=models.SET_NULL)
    review_date = models.DateField(verbose_name='审核日期', blank=True,
                                   null=True)
    proofreader = models.ForeignKey(User, verbose_name='校对人',
                                    blank=True, null=True,
                                    related_name='transfer_card_proofreader',
                                    on_delete=models.SET_NULL)
    proofread_date = models.DateField(verbose_name='校对日期',
                                      blank=True, null=True)
    approver = models.ForeignKey(User, verbose_name='批准人',
                                 blank=True, null=True,
                                 related_name='transfer_card_approver',
                                 on_delete=models.SET_NULL)
    approve_date = models.DateField(verbose_name='批准日期',
                                    blank=True, null=True)

    class Meta:
        verbose_name = '流转卡'
        verbose_name_plural = '流转卡'

    def __str__(self):
        header = TRANSFER_HEADER_MAP.get(self.category, 'RH05')
        return '{}-{}-{}'.format(header,
                                 self.materiel.work_order.uid,
                                 self.uid)

    @property
    def status(self):
        zipped = zip(
            [self.approver, self.reviewer, self.proofreader, self.writer],
            ['已批准', '已审核', '已校对', '已编制'])
        for signed, status_name in zipped:
            if signed:
                return status_name
        return '初创建'


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
