from django.db import models
from django.core.checks import Warning
from django.contrb.auth.models import User

from Core.models import WorkOrder, Materiel, Material

from . import (SIGNATURE_CATEGORY_CHOICES, PROCESS_CHOICES,
               CIRCULATION_CHOICES, WELD_METHODS,
               NONDESTRUCTIVE_INSPECTION_TYPES,
               PROCEDURE_QUALIFICATION_INDEXS,
               WELD_POSITION_CHOICES)


class Signature(models.Model):
    work_order = models.OneToOneField(WorkOrder, verbose_name='所属工作令',
                                      on_delete=models.CASCADE)
    # TODO: blank=False null=False
    writer = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               related_name='signature_writer',
                               on_delete=models.CASCADE)
    # TODO: auto_now_add?
    write_date = models.DateField(verbose_name='编制日期',
                                  blank=True, null=True)
    reviewer = models.ForeignKey(User, verbose_name='审核人',
                                 blank=True, null=True,
                                 related_name='signature_reviewer',
                                 on_delete=models.CASCADE)
    review_date = models.DateField(verbose_name='审核日期', blank=True,
                                   null=True)
    category = models.IntegerField(verbose_name='签章类别',
                                   blank=True, null=True,
                                   choices=SIGNATURE_CATEGORY_CHOICES)

    class Meta:
        verbose_name = '签章'
        verbose_name_plural = '签章'

    def __str__(self):
        return str(self.work_order)


class AuxiliaryItem(models.Model):
    materiel = models.OneToOneField(Materiel, verbose_name='所属物料',
                                    on_delete=models.CASCADE)
    quota_coef = models.CharField(verbose_name='定额系数', max_length=100,
                                  null=True, blank=True)
    quota = models.FloatField(verbose_name='定额', null=True, blank=True)
    stardard_code = models.CharField(verbose_name='标准代码', max_length=100,
                                     null=True, blank=True)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              null=True, blank=True)
    # TODO: choices?
    category = models.CharField(verbose_name='类别', max_length=100,
                                null=True, blank=True)

    class Meta:
        verbose_name = '辅材'
        verbose_name_plural = '辅材'

    def __str__(self):
        return str(self.materiel)


class PrincipalItem(models.Model):
    work_order = models.ForeignKey(WorkOrder, verbose_name='所属工作令',
                                   on_delete=models.CASCADE)
    size = models.CharField(verbose_name='规格', max_length=100,
                            null=True, blank=True)
    count = models.CharField(verbose_name='数量', max_length=100,
                             null=True, blank=True)
    weight = models.FloatField(verbose_name='单重', null=True, blank=True)
    # TODO: material or materiel ?
    material = models.ForeignKey(Material, verbose_name='材质',
                                 null=True, blank=True,
                                 on_delete=models.CASCADE)
    stardard = models.CharField(verbose_name='执行标准', max_length=100,
                                null=True, blank=True)
    status = models.CharField(verbose_name='供货状态', max_length=100,
                              null=True, blank=True)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              null=True, blank=True)

    def total_weight(self):
        if self.count and self.weight:
            return self.weight * int(self.count)

    def stardard_status(self):
        return ' '.join((self.stardard, self.status))

    class Meta:
        verbose_name = '主材'
        verbose_name_plural = '主材'

    def __str__(self):
        return self.size


class CooperantItem(models.Model):
    materiel = models.OneToOneField(Materiel, verbose_name='所属物料',
                                    on_delete=models.CASCADE)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              null=True, blank=True)

    class Meta:
        verbose_name = '工序性外协件'
        verbose_name_plural = '工序性外协件'

    def __unicode__(self):
        return self.materiel.name


class FirstFeedingItem(models.Model):
    materiel = models.OneToOneField(Materiel, verbose_name='所属物料',
                                    on_delete=models.CASCADE)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              null=True, blank=True)

    class Meta:
        verbose_name = '先投件'
        verbose_name_plural = '先投件'

    def __str__(self):
        return self.materiel.name


class OutPurchasedItem(models.Model):
    materiel = models.OneToOneField(Materiel, verbose_name='所属物料',
                                    on_delete=models.CASCADE)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              null=True, blank=True)

    class Meta:
        verbose_name = '外购件'
        verbose_name_plural = '外购件'

    def __str__(self):
        return self.materiel.name


class WeldQuota(models.Model):
    # TODO: null=False blank=False
    order = models.ForeignKey(WorkOrder, verbose_name='所属工作令',
                              null=True, blank=True,
                              on_delete=models.CASCADE)
    material = models.ForeignKey(Material, verbose_name='焊材',
                                 on_delete=models.CASCADE)
    size = models.CharField(verbose_name='规格', max_length=100,
                            null=True, blank=True)
    # TODO: FloatField default
    quota = models.FloatField(verbose_name='定额', null=True, blank=True)
    remark = models.CharField(verbose_name='备注', null=True, blank=True,
                              max_length=100)
    stardard = models.CharField(verbose_name='执行标准', max_length=100,
                                null=True, blank=True)

    class Meta:
        verbose_name = u'焊材定额'
        verbose_name_plural = u'焊材定额'

    def __str__(self):
        return self.material.name + '(%s)' % self.size


class ProcessRoute(models.Model):
    materiel = models.OneToOneField(Materiel, verbose_name='所属物料',
                                    on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'工序路线'
        verbose_name_plural = u'工序路线'

    def __str__(self):
        return self.materiel.name

    # TODO: Create Process when ProcessRoute created


class Process(models.Model):
    route = models.ForeignKey(ProcessRoute, verbose_name='工序路线',
                              on_delete=models.CASCADE)
    name = models.IntegerField(verbose_name='简称',
                               choices=PROCESS_CHOICES)
    # TODO: man_hours in numerial fields?
    man_hours = models.CharField(verbose_name='工时', max_length=20,
                                 blank=True, null=True,)

    class Meta:
        verbose_name = '工序'
        verbose_name = '工序'

    def __str__(self):
        return self.get_name_display()


class ProcessReview(models.Model):
    materiel = models.ForeignKey(Materiel, verbose_name='零件',
                                 on_delete=models.CASCADE)
    problem = models.CharField(verbose_name='存在问题', max_length=200,
                               blank=True, null=True)
    advice = models.CharField(verbose_name='改进建议', max_length=200,
                              blank=True, null=True)

    class Meta:
        verbose_name = '工艺性审查表'
        verbose_name_plural = '工艺性审查表'

    def __str__(self):
        return self.materiel.name


class CirculationRoute(models.Model):
    materiel = models.OneToOneField(Materiel, verbose_name='所属物料',
                                    on_delete=models.CASCADE)

    class Meta:
        verbose_name = '流转路线'
        verbose_name_plural = '流转路线'

    def __str__(self):
        return self.materiel.name

    # TODO: Create Circulation when CirculationRoute created


class Circulation(models.Model):
    route = models.ForeignKey(CirculationRoute, verbose_name='流转路线',
                              on_delete=models.CASCADE)
    name = models.IntegerField(verbose_name='简称',
                               choices=CIRCULATION_CHOICES)
    full_name = models.CharField(verbose_name='全称', max_length=10,
                                 blank=True, null=True)

    class Meta:
        verbose_name = '流转'
        verbose_name_plural = '流转名称'

    def __str__(self):
        return self.get_name_display()


class WeldingProcessSpecification(models.Model):
    work_order = models.ForeignKey(WorkOrder, verbose_name='所属工作令')

    lister = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               on_delete=models.CASCADE,
                               related_name='weld_proc_spec_lister')
    list_date = models.DateField(verbose_name='编制日期',
                                 blank=True, null=True)
    auditor = models.ForeignKey(User, verbose_name='审核人',
                                blank=True, null=True,
                                on_delete=models.CASCADE,
                                related_name='weld_proc_spec_auditor')
    audit_date = models.DateField(verbose_name='审核日期',
                                  blank=True, null=True)
    approver = models.ForeignKey(User, verbose_name='批准人',
                                 blank=True, null=True,
                                 on_delete=models.CASCADE,
                                 related_name='weld_proc_sped_approver')
    approve_date = models.DateField(verbose_name='批准日期',
                                    blank=True, null=True)
    path = models.FileField(verbose_name='示意图', upload_to='%Y/%m/%d',
                            null=True, blank=True)

    class Meta:
        verbose_name = '焊接工艺规程'
        verbose_name_plural = '焊接工艺规程'

    def __str__(self):
        return 'RH09-' + self.work_order.suffix()


class WeldSeamType(models.Model):
    name = models.CharField(verbose_name='类型名', max_length=100)

    class Meta:
        verbose_name = '焊缝类型'
        verbose_name_plural = '焊缝类型'

    def __str__(self):
        return self.name


# TODO: Remove this class if needed
class WeldMethod(models.Model):
    name = models.CharField(verbose_name='方法名', choices=WELD_METHODS,
                            max_length=100)

    class Meta:
        verbose_name = '焊接方法'
        verbose_name_plural = '焊接方法'

    def __str__(self):
        return self.get_name_display()


# TODO: Remove this class if needed
class NondestructiveInspection(models.Model):
    name = models.CharField(verbose_name='探伤种类名', max_length=20,
                            choices=NONDESTRUCTIVE_INSPECTION_TYPES)

    class Meta:
        verbose_name = '无损探伤'
        verbose_name_plural = '无损探伤'

    def __str__(self):
        return self.name


class WeldCertification(models.Model):
    name = models.CharField(verbose_name='焊工持证项目', max_length=100)
    weld_method = models.ForeignKey(WeldMethod, verbose_name='所属焊接方法',
                                    on_delete=models.CASCADE)

    class Meta:
        verbose_name = '焊工持证项目'
        verbose_name_plural = '焊工持证项目'

    def __str__(self):
        return self.name


class ProcedureQualificationIndex(models.Model):
    name = models.IntegerField(verbose_name='焊接工艺评定编号',
                               choices=PROCEDURE_QUALIFICATION_INDEXS)

    class Meta:
        verbose_name = '焊接工艺评定编号'
        verbose_name_plural = '焊接工艺评定编号'

    def __str__(self):
        return self.name


class WeldPositionType(models.Model):
    name = models.IntegerField(verbose_name='焊接位置名',
                               choices=WELD_POSITION_CHOICES)

    class Meta:
        verbose_name = '焊接位置'
        verbose_name_plural = '焊接位置'

    def __str__(self):
        return self.get_name_display()


# TODO: better design?
class WeldJointTechDetail(models.Model):
    specification = models.ForeignKey(WeldingProcessSpecification,
                                      verbose_name='焊接工艺规程',
                                      on_delete=models.CASCADE)
    joint_index = models.CharField(verbose_name='接头编号', max_length=100,
                                   blank=True, null=True)
    bm_texture_1 = models.CharField(verbose_name='母材材质_1', max_length=100,
                                    blank=True, null=True)
    bm_spec_1 = models.CharField(verbose_name='母材规格_1', max_length=100,
                                 blank=True, null=True)
    bm_texture_2 = models.CharField(verbose_name='母材材质_2', max_length=100,
                                    blank=True, null=True)
    bm_spec_2 = models.CharField(verbose_name='母材规格_2', max_length=100,
                                 blank=True, null=True)
    weld_position = models.ForeignKey(WeldPositionType,
                                      verbose_name='焊接位置',
                                      on_delete=models.CASCADE)
    weld_method_1 = models.ForeignKey(WeldMethod, verbose_name='焊接方法_1',
                                      null=True, blank=True,
                                      on_delete=models.CASCADE,
                                      related_name='joint_detail_method_1')
    weld_method_2 = models.ForeignKey(WeldMethod, verbose_name=u'焊接方法_2',
                                      null=True, blank=True,
                                      on_delete=models.CASCADE,
                                      related_name='joint_detail_method_2')
    # TODO: ForeignKey?
    proc_qual_index = models.CharField(
        verbose_name=u'焊接工艺评定编号', max_length=100,
        blank=True, null=True)
    weld_cert_1 = models.ManyToManyField(WeldCertification,
                                         verbose_name=u'焊工持证项目_1',
                                         related_name='joint_detail_cert_1')
    weld_cert_2 = models.ManyToManyField(WeldCertification,
                                         verbose_name=u'焊工持证项目_2',
                                         related_name='joint_detail_cert_2')
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, null=True)

    class Meta:
        verbose_name = '焊接接头工艺分析'
        verbose_name_plural = '焊接接头工艺分析'

    def __str__(self):
        return self.joint_index

    def weld_method(self):
        if self.weld_method_2:
            return '{} + {}'.format(self.weld_method_1.get_name_display(),
                                    self.weld_method_2.get_name_display())
        else:
            return self.weld_method_1.get_name_display()

    def get_weld_certification1(self):
        raise Warning('Deprecated: This will be removed soon, '
                      'use get_weld_cert_1() instead')
        return self.get_weld_cert_1()

    def get_weld_cert_1(self):
        return '或'.join([str(x) for x in self.weld_cert_1.all()])

    def get_weld_certification2(self):
        raise Warning('Deprecated: This will be removed soon, '
                      'use get_weld_cert_2() instead')
        return self.get_weld_cert_2()

    def get_weld_cert_2(self):
        return '或'.join([str(x) for x in self.weld_cert_2.all()])


class WeldingWorkInstruction(models.Model):
    detail = models.OneToOneField(WeldJointTechDetail, verbose_name='所属接头分析',
                                  on_delete=models.CASCADE)
    lister = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               on_delete=models.CASCADE,
                               related_name='weld_work_inst_lister')
    list_date = models.DateField(verbose_name='编制日期',
                                 blank=True, null=True)
    auditor = models.ForeignKey(User, verbose_name='审核人',
                                blank=True, null=True,
                                on_delete=models.CASCADE,
                                related_name='weld_work_inst_auditor')
    audit_date = models.DateField(verbose_name='审核日期',
                                  blank=True, null=True)
    proofreader = models.ForeignKey(User, verbose_name='校对人',
                                    blank=True, null=True,
                                    on_delete=models.CASCADE,
                                    related_name='weld_work_inst_proofreader')
    proofread_date = models.DateField(verbose_name='校对日期',
                                      blank=True, null=True)
    approver = models.ForeignKey(User, verbose_name='批准人',
                                 blank=True, null=True,
                                 on_delete=models.CASCADE,
                                 related_name='weld_work_inst_approver')
    approve_date = models.DateField(verbose_name='批准日期',
                                    blank=True, null=True)
    identifier = models.CharField(verbose_name='文件编号', max_length=100,
                                  blank=True, null=True)
    path = models.FileField(verbose_name='简图', upload_to='%Y/%m/%d',
                            null=True, blank=True)

    class Meta:
        verbose_name = '焊接作业指导书'
        verbose_name_plural = '焊接作业指导书'

    def __str__(self):
        return 'RH20-{}-{}'.format(
            self.detail.specification.work_order.suffix(),
            self.identifier)


class WeldSeam(models.Model):
    materiel = models.ForeignKey(Materiel, verbose_name='所属物料',
                                 on_delete=models.CASCADE)
    identifier = models.CharField(verbose_name='焊缝编号', max_length=100,
                                  blank=True, null=True)
    seam_type = models.ForeignKey(WeldSeamType, verbose_name='焊缝类型',
                                  on_delete=models.CASCADE)
    weld_position = models.ForeignKey(WeldPositionType,
                                      verbose_name='焊接位置',
                                      on_delete=models.CASCADE)
    weld_method_1 = models.ForeignKey(WeldMethod, verbose_name='焊接方法_1',
                                      null=True, blank=True,
                                      on_delete=models.CASCADE,
                                      related_name='weld_seam_method_1')
    weld_method_2 = models.ForeignKey(WeldMethod, verbose_name='焊接方法_2',
                                      null=True, blank=True,
                                      on_delete=models.CASCADE,
                                      related_name='weld_method_2')
    base_metal_1 = models.CharField(verbose_name='母材材质_1', max_length=100,
                                    null=True, blank=True)
    base_metal_2 = models.CharField(verbose_name='母材材质_2', max_length=100,
                                    null=True, blank=True)
    base_metal_thin_1 = models.CharField(verbose_name='母材厚度_1',
                                         max_length=100,
                                         blank=True, null=True)
    base_metal_thin_2 = models.CharField(verbose_name='母材厚度2',
                                         max_length=100,
                                         blank=True, null=True)
    length = models.CharField(verbose_name='长度', max_length=100)
    # TODO: weld_material as Model?
    weld_material_1 = models.ForeignKey(Material, verbose_name='焊丝/焊条_1',
                                        blank=True, null=True,
                                        on_delete=models.CASCADE,
                                        related_name='weld_seam_material_1')
    weld_flux_1 = models.ForeignKey(Material, verbose_name='焊剂_1',
                                    blank=True, null=True,
                                    on_delete=models.CASCADE,
                                    related_name='weld_seam_flux_1')
    thin_1 = models.CharField(verbose_name='焊材厚度_1', max_length=100,
                              blank=True, null=True)
    size_1 = models.CharField(verbose_name='规格_1', max_length=100,
                              blank=True, null=True)
    weight_1 = models.FloatField(verbose_name='重量_1', blank=True, default=0)
    flux_weight_1 = models.FloatField(verbose_name='焊剂重量_1',
                                      blank=True, default=0)
    weld_material_2 = models.ForeignKey(Material, verbose_name='焊丝/焊条_2',
                                        blank=True, null=True,
                                        on_delete=models.CASCADE,
                                        related_name='weld_seam_material_2')
    weld_flux_2 = models.ForeignKey(Material, verbose_name='焊剂_2',
                                    blank=True, null=True,
                                    related_name='weld_seam_flux_2')
    thin_2 = models.CharField(verbose_name='焊材厚度_2', max_length=100,
                              blank=True, null=True)
    size_2 = models.CharField(verbose_name='规格_2', max_length=100,
                              blank=True, null=True)
    weight_2 = models.FloatField(verbose_name='重量_2', blank=True, default=0)
    flux_weight_2 = models.FloatField(verbose_name='焊剂重量_2',
                                      blank=True, default=0)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, null=True)
    weld_joint_detail = models.ForeignKey(
        WeldJointTechDetail, verbose_name='焊接接头', blank=True, null=True,
        on_delete=models.SET_NULL)
    groove_inspction = models.ManyToManyField(
        NondestructiveInspection, verbose_name='坡口探伤', blank=True,
        related_name='weld_seam_groove_inspction')
    welded_status_inspection = models.ManyToManyField(
        NondestructiveInspection, verbose_name='焊态探伤', blank=True,
        related_name='weld_seam_welded_status_inspection')
    heat_treatment_inspection = models.ManyToManyField(
        NondestructiveInspection, verbose_name='热处理后探伤', blank=True,
        related_name='weld_seam_heat_treatment_inspection')
    pressure_test_inspection = models.ManyToManyField(
        NondestructiveInspection, verbose_name='试压后探伤', blank=True,
        related_name='weld_seam_pressure_test_inspection')

    class Meta:
        verbose_name = '焊缝'
        verbose_name_plural = '焊缝'

    def __str__(self):
        return self.materiel.name
