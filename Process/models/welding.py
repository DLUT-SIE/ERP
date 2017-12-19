from django.db import models
from django.contrib.auth.models import User

from Core.models import WorkOrder
from Core.utils import DynamicHashPath
from Process import (WELD_METHODS, WELD_POSITION_CHOICES,
                     PROCEDURE_QUALIFICATION_INDEXS,
                     WWI_EXAMINATION_SURVEYOR_CHOICES)
from Process.models import Material, ProcessMaterial


class WeldingProcessSpecification(models.Model):
    """
    焊接工艺规程
    """
    work_order = models.ForeignKey(WorkOrder, verbose_name='所属工作令',
                                   on_delete=models.CASCADE)
    lister = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               on_delete=models.SET_NULL,
                               related_name='weld_proc_spec_lister')
    list_date = models.DateField(verbose_name='编制日期',
                                 blank=True, null=True)
    auditor = models.ForeignKey(User, verbose_name='审核人',
                                blank=True, null=True,
                                on_delete=models.SET_NULL,
                                related_name='weld_proc_spec_auditor')
    audit_date = models.DateField(verbose_name='审核日期',
                                  blank=True, null=True)
    approver = models.ForeignKey(User, verbose_name='批准人',
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='weld_proc_sped_approver')
    approve_date = models.DateField(verbose_name='批准日期',
                                    blank=True, null=True)
    path = models.FileField(verbose_name='文件路径',
                            upload_to=DynamicHashPath('WeldingProcSpec'),
                            blank=True, null=True)

    class Meta:
        verbose_name = '焊接工艺规程'
        verbose_name_plural = '焊接工艺规程'

    def __str__(self):
        return 'RH09-{}'.format(self.work_order.uid)


class WeldingCertification(models.Model):
    """
    焊工持证项目
    """
    name = models.CharField(verbose_name='持证项目', max_length=50)
    weld_method = models.IntegerField(verbose_name='焊接方法',
                                      choices=WELD_METHODS)

    class Meta:
        verbose_name = '焊工持证项目'
        verbose_name_plural = '焊工持证项目'

    def __str__(self):
        return self.name


class WeldingJointProcessAnalysis(models.Model):
    """
    焊接接头工艺分析
    """
    spec = models.ForeignKey(WeldingProcessSpecification,
                             verbose_name='焊接工艺规程',
                             on_delete=models.CASCADE)
    joint_index = models.CharField(verbose_name='接头编号', max_length=50,
                                   blank=True, default='')
    proc_qual_index = models.IntegerField(
        verbose_name='焊接工艺评定编号',
        choices=PROCEDURE_QUALIFICATION_INDEXS)
    weld_cert_1 = models.ManyToManyField(WeldingCertification,
                                         verbose_name='焊工持证项目_1',
                                         related_name='joint_analysis_cert_1')
    weld_cert_2 = models.ManyToManyField(WeldingCertification,
                                         verbose_name='焊工持证项目_2',
                                         related_name='joint_analysis_cert_2')
    remark = models.CharField(verbose_name='备注', max_length=50,
                              blank=True, default='')

    class Meta:
        verbose_name = '焊接接头工艺分析'
        verbose_name_plural = '焊接接头工艺分析'

    def __str__(self):
        return self.joint_index


class WeldingSeam(models.Model):
    """
    焊缝
    """
    process_material = models.ForeignKey(ProcessMaterial,
                                         verbose_name='物料',
                                         on_delete=models.CASCADE)
    # TODO: unique?
    uid = models.CharField(verbose_name='焊缝编号', max_length=50,
                           blank=True, default='')
    # TODO: choices?
    seam_type = models.CharField(verbose_name='类型名', max_length=50)
    weld_position = models.IntegerField(verbose_name='焊接位置',
                                        choices=WELD_POSITION_CHOICES)
    weld_method_1 = models.IntegerField(verbose_name='焊接方法_1',
                                        choices=WELD_METHODS,
                                        blank=True, null=True)
    weld_method_2 = models.IntegerField(verbose_name='焊接方法_2',
                                        choices=WELD_METHODS,
                                        blank=True, null=True)
    bm_1 = models.CharField(verbose_name='母材材质_1', max_length=50,
                            default='', blank=True)
    bm_thick_1 = models.FloatField(verbose_name='母材厚度_1')
    bm_2 = models.CharField(verbose_name='母材材质_2', max_length=50,
                            default='', blank=True)
    bm_thick_2 = models.FloatField(verbose_name='母材厚度2')
    length = models.FloatField(verbose_name='长度')

    wm_1 = models.ForeignKey(Material, verbose_name='焊丝/焊条_1_材质',
                             blank=True, null=True,
                             on_delete=models.SET_NULL,
                             related_name='weld_seam_material_1')
    wf_1 = models.ForeignKey(Material, verbose_name='焊丝/焊条_1_焊剂',
                             blank=True, null=True,
                             on_delete=models.SET_NULL,
                             related_name='weld_seam_flux_1')
    wt_1 = models.CharField(verbose_name='焊材厚度_1', max_length=100,
                            blank=True, default='')
    ws_1 = models.CharField(verbose_name='规格_1', max_length=100,
                            blank=True, default='')
    weight_1 = models.FloatField(verbose_name='焊材重量_1', default=0)
    wf_weight_1 = models.FloatField(verbose_name='焊剂重量_1', default=0)

    wm_2 = models.ForeignKey(Material, verbose_name='焊丝/焊条_2_材质',
                             blank=True, null=True,
                             on_delete=models.SET_NULL,
                             related_name='weld_seam_material_2')
    wf_2 = models.ForeignKey(Material, verbose_name='焊丝/焊条_2_焊剂',
                             blank=True, null=True,
                             on_delete=models.SET_NULL,
                             related_name='weld_seam_flux_2')
    wt_2 = models.CharField(verbose_name='焊材厚度_2', max_length=200,
                            blank=True, default='')
    ws_2 = models.CharField(verbose_name='规格_2', max_length=200,
                            blank=True, default='')
    weight_2 = models.FloatField(verbose_name='焊材重量_2', default=0)
    wf_weight_2 = models.FloatField(verbose_name='焊剂重量_2', default=0)

    remark = models.CharField(verbose_name='备注', max_length=50,
                              blank=True, default='')
    analysis = models.ForeignKey(
        WeldingJointProcessAnalysis, verbose_name='焊接接头工艺分析',
        blank=True, null=True,
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '焊缝'
        verbose_name_plural = '焊缝'

    def __str__(self):
        return str(self.process_material)


class WeldingWorkInstruction(models.Model):
    """
    焊接作业指导书
    """
    detail = models.OneToOneField(WeldingJointProcessAnalysis,
                                  verbose_name='焊接接头工艺分析',
                                  on_delete=models.CASCADE)
    lister = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               on_delete=models.SET_NULL,
                               related_name='weld_work_inst_lister')
    list_date = models.DateField(verbose_name='编制日期',
                                 blank=True, null=True)
    auditor = models.ForeignKey(User, verbose_name='审核人',
                                blank=True, null=True,
                                on_delete=models.SET_NULL,
                                related_name='weld_work_inst_auditor')
    audit_date = models.DateField(verbose_name='审核日期',
                                  blank=True, null=True)
    proofreader = models.ForeignKey(User, verbose_name='校对人',
                                    blank=True, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='weld_work_inst_proofreader')
    proofread_date = models.DateField(verbose_name='校对日期',
                                      blank=True, null=True)
    approver = models.ForeignKey(User, verbose_name='批准人',
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='weld_work_inst_approver')
    approve_date = models.DateField(verbose_name='批准日期',
                                    blank=True, null=True)
    path = models.FileField(
        verbose_name='路径',
        upload_to=DynamicHashPath('WeldingWorkInstruction'),
        blank=True, null=True)

    class Meta:
        verbose_name = '焊接作业指导书'
        verbose_name_plural = '焊接作业指导书'

    def __str__(self):
        return 'RH20-{}-{}'.format(self.detail.spec.work_order, self.id)


class WeldingWorkInstructionProcess(models.Model):
    """
    焊接作业指导书工序
    """
    instruction = models.ForeignKey(WeldingWorkInstruction,
                                    verbose_name='焊接作业指导书')
    index = models.IntegerField(verbose_name='序号')
    name = models.CharField(verbose_name='工序名', max_length=50,
                            default='', blank=True)
    detail = models.CharField(verbose_name='工艺过程及技术要求',
                              max_length=100, default='', blank=True)

    class Meta:
        verbose_name = '焊接作业指导书工序'
        verbose_name_plural = '焊接作业指导书工序'

    def __str__(self):
        return '{}-{}-{}'.format(self.instruction, self.index, self.name)


class WeldingWorkInstructionExamination(models.Model):
    """
    焊接作业检验
    """
    instruction = models.ForeignKey(WeldingWorkInstruction,
                                    verbose_name='焊接作业指导书')
    index = models.IntegerField(verbose_name='序号')
    surveyor = models.IntegerField(verbose_name='检验方',
                                   null=True, blank=True,
                                   choices=WWI_EXAMINATION_SURVEYOR_CHOICES)

    class Meta:
        verbose_name = '焊接作业检验'
        verbose_name_plural = '焊接作业检验'

    def __str__(self):
        return '{}:检验_{}'.format(self.transfer_card, self.indx)


class WeldingLayerCard(models.Model):
    """
    焊接层道卡
    """
    instruction = models.ForeignKey(WeldingWorkInstruction,
                                    verbose_name='焊接作业指导书')
    layer = models.IntegerField(verbose_name='层/道')
    weld_method = models.IntegerField(verbose_name='焊接方法',
                                      choices=WELD_METHODS)
    # TODO: Field type?
    polarity = models.CharField(verbose_name='极性', max_length=10,
                                blank=True, default='')
    # TODO: IntegerField?
    electricity = models.CharField(verbose_name='电流', max_length=10,
                                   blank=True, default='')
    # TODO: IntegerField?
    voltage = models.CharField(verbose_name='电流电压', max_length=10,
                               blank=True, default='')
    # TODO: IntegerField?
    welding_speed = models.CharField(verbose_name='焊接速度', max_length=10,
                                     blank=True, default='')
    # TODO: IntegerField?
    heat_input = models.CharField(verbose_name='线能量', max_length=10,
                                  blank=True, default='')
    remark = models.CharField(verbose_name='备注', max_length=50,
                              blank=True, default='')

    class Meta:
        verbose_name = '焊接层道卡'
        verbose_name_plural = '焊接层道卡'

    def __str__(self):
        return '{}-{}'.format(self.instruction, self.layer)
