# TODO: Split models into different files
from django.db import models
from django.core.checks import Warning
from django.contrib.auth.models import User

from Core.models import WorkOrder, Materiel, Material, Department
from Procurement.models import MaterielExecutionDetail
from Process import (SIGNATURE_CATEGORY_CHOICES, PROCESS_CHOICES,
                  CIRCULATION_CHOICES, WELD_METHODS,
                  NONDESTRUCTIVE_INSPECTION_TYPES,
                  PROCEDURE_QUALIFICATION_INDEXS,
                  WELD_POSITION_CHOICES,
                  TRANSFER_CARD_CATEGORY_CHOICES,
                  TRANSFER_HEADER_MAP,
                  WWI_TEST_METHOD_CHOICES)


class Signature(models.Model):
    work_order = models.OneToOneField(WorkOrder, verbose_name='所属工作令',
                                      on_delete=models.CASCADE)
    # TODO: blank=False null=False
    writer = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               related_name='signature_writer',
                               on_delete=models.SET_NULL)
    # TODO: auto_now_add?
    write_date = models.DateField(verbose_name='编制日期',
                                  blank=True, null=True)
    reviewer = models.ForeignKey(User, verbose_name='审核人',
                                 blank=True, null=True,
                                 related_name='signature_reviewer',
                                 on_delete=models.SET_NULL)
    review_date = models.DateField(verbose_name='审核日期', blank=True,
                                   null=True)
    # TODO: editable=False
    category = models.IntegerField(verbose_name='签章类别',
                                   blank=True, null=True,
                                   choices=SIGNATURE_CATEGORY_CHOICES)

    class Meta:
        verbose_name = '签章'
        verbose_name_plural = '签章'
        abstract = True

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
                                 on_delete=models.SET_NULL)
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
                              on_delete=models.SET_NULL)
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


class ProcessStep(models.Model):
    route = models.ForeignKey(ProcessRoute, verbose_name='工序路线',
                              on_delete=models.CASCADE)
    name = models.IntegerField(verbose_name='工序',
                               choices=PROCESS_CHOICES)
    # TODO: man_hours in numerial fields?
    man_hours = models.CharField(verbose_name='工时', max_length=20,
                                 blank=True, null=True,)

    class Meta:
        verbose_name = '工序步骤'
        verbose_name = '工序步骤'

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
                                      on_delete=models.SET_NULL,
                                      related_name='joint_detail_method_1')
    weld_method_2 = models.ForeignKey(WeldMethod, verbose_name=u'焊接方法_2',
                                      null=True, blank=True,
                                      on_delete=models.SET_NULL,
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
    # TODO: unique?
    uid = models.CharField(verbose_name='文件编号', max_length=100,
                           blank=True, null=True)
    path = models.FileField(verbose_name='简图', upload_to='%Y/%m/%d',
                            null=True, blank=True)

    class Meta:
        verbose_name = '焊接作业指导书'
        verbose_name_plural = '焊接作业指导书'

    def __str__(self):
        return 'RH20-{}-{}'.format(
            self.detail.specification.work_order.suffix(), self.uid)


class WeldSeam(models.Model):
    materiel = models.ForeignKey(Materiel, verbose_name='所属物料',
                                 on_delete=models.CASCADE)
    # TODO: unique?
    uid = models.CharField(verbose_name='焊缝编号', max_length=100,
                           blank=True, null=True)
    seam_type = models.ForeignKey(WeldSeamType, verbose_name='焊缝类型',
                                  on_delete=models.CASCADE)
    weld_position = models.ForeignKey(WeldPositionType,
                                      verbose_name='焊接位置',
                                      on_delete=models.CASCADE)
    weld_method_1 = models.ForeignKey(WeldMethod, verbose_name='焊接方法_1',
                                      null=True, blank=True,
                                      on_delete=models.SET_NULL,
                                      related_name='weld_seam_method_1')
    weld_method_2 = models.ForeignKey(WeldMethod, verbose_name='焊接方法_2',
                                      null=True, blank=True,
                                      on_delete=models.SET_NULL,
                                      related_name='weld_method_2')
    base_metal_1 = models.CharField(verbose_name='母材材质_1', max_length=100,
                                    null=True, blank=True)
    base_metal_2 = models.CharField(verbose_name='母材材质_2', max_length=100,
                                    null=True, blank=True)
    base_metal_thick_1 = models.CharField(verbose_name='母材厚度_1',
                                          max_length=100,
                                          blank=True, null=True)
    base_metal_thick_2 = models.CharField(verbose_name='母材厚度2',
                                          max_length=100,
                                          blank=True, null=True)
    length = models.CharField(verbose_name='长度', max_length=100)
    # TODO: weld_material as Model?
    weld_material_1 = models.ForeignKey(Material, verbose_name='焊丝/焊条_1',
                                        blank=True, null=True,
                                        on_delete=models.SET_NULL,
                                        related_name='weld_seam_material_1')
    weld_flux_1 = models.ForeignKey(Material, verbose_name='焊剂_1',
                                    blank=True, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='weld_seam_flux_1')
    thick_1 = models.CharField(verbose_name='焊材厚度_1', max_length=100,
                               blank=True, null=True)
    size_1 = models.CharField(verbose_name='规格_1', max_length=100,
                              blank=True, null=True)
    weight_1 = models.FloatField(verbose_name='重量_1', blank=True, default=0)
    flux_weight_1 = models.FloatField(verbose_name='焊剂重量_1',
                                      blank=True, default=0)

    weld_material_2 = models.ForeignKey(Material, verbose_name='焊丝/焊条_2',
                                        blank=True, null=True,
                                        on_delete=models.SET_NULL,
                                        related_name='weld_seam_material_2')
    weld_flux_2 = models.ForeignKey(Material, verbose_name='焊剂_2',
                                    blank=True, null=True,
                                    related_name='weld_seam_flux_2')
    thick_2 = models.CharField(verbose_name='焊材厚度_2', max_length=100,
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


class TransferCard(models.Model):
    # TODO: unique?
    uid = models.CharField(verbose_name='文件编号', max_length=100,
                           null=True, blank=True)
    materiel = models.ForeignKey(Materiel, verbose_name='所属零件')
    category = models.IntegerField(verbose_name='流转卡类型',
                                   choices=TRANSFER_CARD_CATEGORY_CHOICES)
    container_category = models.CharField(verbose_name='容器类别',
                                          max_length=100,
                                          blank=True, null=True)
    parent_name = models.CharField(verbose_name='所属部件名称', max_length=100,
                                   blank=True, null=True)
    weld_test_plate_index = models.CharField(verbose_name='焊接试板图号',
                                             max_length=100,
                                             blank=True, null=True)
    parent_test_plate_index = models.CharField(verbose_name='母材试板图号',
                                               max_length=100,
                                               blank=True, null=True)
    material_index = models.CharField(verbose_name='材质标记',
                                      max_length=100,
                                      blank=True, null=True)
    path = models.FileField(verbose_name='文件路径', upload_to='%Y/%m/%d',
                            null=True, blank=True)
    tech_requirement = models.CharField(verbose_name='技术要求',
                                        max_length=1000,
                                        null=True, blank=True)

    class Meta:
        verbose_name = '流转卡'
        verbose_name_plural = '流转卡'

    def __str__(self):
        header = TRANSFER_HEADER_MAP.get(self.category, 'RH05')
        return '{}-{}- -{}'.format(header,
                                   self.materiel.work_order.suffix(),
                                   self.uid)


class WeldingWorkInstructionProcess(models.Model):
    instruction = models.ForeignKey(WeldingWorkInstruction,
                                    verbose_name='焊接作业指导书')
    index = models.CharField(verbose_name='序号', max_length=100,
                             null=True, blank=True)
    name = models.CharField(verbose_name='工序名', max_length=100,
                            null=True, blank=True)
    detail = models.CharField(verbose_name='工艺过程及技术要求',
                              max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = '焊接作业指导书工序'
        verbose_name_plural = '焊接作业指导书工序'

    def __str__(self):
        return '{}-{}-{}'.format(self.instruction, self.index, self.name)


class WeldingWorkInstructionTest(models.Model):
    instruction = models.ForeignKey(WeldingWorkInstruction,
                                    verbose_name='焊接作业指导书')
    index = models.CharField(verbose_name='序号', max_length=100,
                             null=True, blank=True)
    test_method = models.IntegerField(verbose_name='检验方',
                                      null=True, blank=True,
                                      choices=WWI_TEST_METHOD_CHOICES)

    class Meta:
        verbose_name = '焊接作业检验'
        verbose_name_plural = '焊接作业检验'

    def __str__(self):
        return '{}:检验_{}'.format(self.transfer_card, self.indx)


class TransferCardProcess(models.Model):
    transfer_card = models.ForeignKey(TransferCard,
                                      verbose_name='流转卡')
    index = models.CharField(verbose_name='序号', max_length=100,
                             null=True, blank=True)
    name = models.CharField(verbose_name='工序名', max_length=100,
                            null=True, blank=True)
    detail = models.CharField(verbose_name='工艺过程及技术要求',
                              max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = '流转卡工序'
        verbose_name_plural = '流转卡工序'

    def __str__(self):
        return '{}-{}-{}'.format(self.transfer_card, self.index, self.name)


# TODO: Any better design to inherit from Signature?
class TransferCardSignature(models.Model):
    transfer_card = models.OneToOneField(TransferCard,
                                         verbose_name='所属流转卡',
                                         on_delete=models.CASCADE)
    # TODO: blank=False null=False, Sign when created?
    writer = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               related_name='transfer_card_signature_writer',
                               on_delete=models.SET_NULL)
    # TODO: auto_now_add?
    write_date = models.DateField(verbose_name='编制日期',
                                  blank=True, null=True)
    reviewer = models.ForeignKey(User, verbose_name='审核人',
                                 blank=True, null=True,
                                 related_name=('transfer_card_signature'
                                               '_reviewer'),
                                 on_delete=models.SET_NULL)
    review_date = models.DateField(verbose_name='审核日期', blank=True,
                                   null=True)
    proofreader = models.ForeignKey(User, verbose_name='校对人',
                                    blank=True, null=True,
                                    related_name=('transfer_card_signature'
                                                  '_proofreader'),
                                    on_delete=models.SET_NULL)
    proofread_date = models.DateField(verbose_name='校对日期',
                                      blank=True, null=True)
    approver = models.ForeignKey(User, verbose_name='批准人',
                                 blank=True, null=True,
                                 related_name=('transfer_card_signature'
                                               '_approver'),
                                 on_delete=models.SET_NULL)
    approve_date = models.DateField(verbose_name='批准日期',
                                    blank=True, null=True)

    class Meta:
        verbose_name = '流转卡签章'
        verbose_name_plural = '流转卡签章'

    def __str__(self):
        return str(self.card)

    @property
    def status(self):
        zipped = zip(
            [self.approver, self.reviewer, self.proofreader, self.writer],
            ['已批准', '已审核', '已校对', '已编制'])
        for signed, status_name in zipped:
            if signed:
                return status_name
        return '初创建'


class ProcessLibrarySignature(models.Model):
    work_order = models.OneToOneField(WorkOrder, verbose_name='所属工作令',
                                      on_delete=models.CASCADE)
    # TODO: blank=False null=False
    writer = models.ForeignKey(User, verbose_name='工艺员',
                               blank=True, null=True,
                               related_name='process_lib_signature_writer',
                               on_delete=models.SET_NULL)
    # TODO: auto_now_add?
    write_date = models.DateField(verbose_name='编制日期',
                                  blank=True, null=True)
    quota_clerk = models.ForeignKey(User, verbose_name='定额员',
                                    blank=True, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='process_lib_quota_clerk')
    quota_date = models.DateField(verbose_name='定额日期',
                                  blank=True, null=True)
    proofreader = models.ForeignKey(User, verbose_name='校对人',
                                    blank=True, null=True,
                                    related_name='process_lib_proofreader',
                                    on_delete=models.SET_NULL)
    proofread_date = models.DateField(verbose_name='校对日期',
                                      blank=True, null=True)
    statistician = models.ForeignKey(User, verbose_name='统计员',
                                     blank=True, null=True,
                                     related_name='process_lib_statistician',
                                     on_delete=models.SET_NULL)
    statistic_date = models.DateField(verbose_name='统计日期',
                                      blank=True, null=True)

    class Meta:
        verbose_name = '工艺库签章'
        verbose_name_plural = '工艺库签章'

    def __str__(self):
        return str(self.work_order)


class ProgramingNestingChart(models.Model):
    execution_detail = models.ForeignKey(MaterielExecutionDetail,
                                         verbose_name='所属执行',
                                         on_delete=models.CASCADE)
    name = models.CharField(verbose_name='文件名称', max_length=100)
    path = models.FileField(verbose_name='文件路径', upload_to='%Y/%m/%d')
    upload_dt = models.DateTimeField(verbose_name='上传时间',
                                     auto_now_add=True)
    # TODO: size as IntegerField
    size = models.CharField(verbose_name='文件大小', max_length=50,
                            blank=True, null=True, default=None)
    # TODO: Review: Is this needed?
    file_type = models.CharField(verbose_name='文件类型', max_length=50,
                                 blank=True, null=True, default=None)

    class Meta:
        verbose_name = '编程套料图'
        verbose_name_plural = '编程套料图'

    def __str__(self):
        return self.name


class HeatTreatmentTechCard(models.Model):
    # TODO: unique
    uid = models.CharField(verbose_name='文件编号', max_length=100,
                           blank=True, null=True)
    writer = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               related_name='heat_treat_tech_card_writer')
    write_date = models.DateField(verbose_name='编制日期',
                                  blank=True, null=True)
    reviewer = models.ForeignKey(User, verbose_name='审核人',
                                 blank=True, null=True,
                                 related_name='heat_treat_tech_card_reviewer')
    review_date = models.DateField(verbose_name='审核日期',
                                   blank=True, null=True)
    furnace_temp = models.CharField(verbose_name='进炉温度', max_length=20,
                                    null=True, blank=True)
    tapping_temp = models.CharField(verbose_name='出炉温度', max_length=20,
                                    null=True, blank=True)
    maximum_temp = models.CharField(verbose_name='最高温度', max_length=20,
                                    null=True, blank=True)
    heating_rate = models.CharField(verbose_name='升温速率', max_length=20,
                                    null=True, blank=True)
    cooling_rate = models.CharField(verbose_name='降温速率', max_length=20,
                                    null=True, blank=True)
    holding_time = models.CharField(verbose_name='保温时间', max_length=20,
                                    null=True, blank=True)

    class Meta:
        verbose_name = '热处理工艺卡'
        verbose_name_plural = u'热处理工艺卡'

    def __str__(self):
        return 'RR01-{}'.format(self.uid)


class HeatTreatmentPart(models.Model):
    materiel = models.ForeignKey(Materiel, verbose_name='零件',
                                 on_delete=models.CASCADE)
    max_heat_treat_thick = models.CharField(
        verbose_name='最大热处理厚度', max_length=20, null=True, blank=True)
    heat_test = models.CharField(verbose_name='热处理检验', max_length=100,
                                 null=True, blank=True)
    operator = models.ForeignKey(User, verbose_name='操作者',
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL)
    test_result = models.CharField(verbose_name='检验结果', max_length=100,
                                   null=True, blank=True)
    card_belong = models.ForeignKey(HeatTreatmentTechCard,
                                    verbose_name='所属工艺卡',
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '热处理件'
        verbose_name_plural = '热处理件'

    def __str__(self):
        return str(self.materiel)


class HeatTreatmentTempMeasuringPointLayout(models.Model):
    # TODO: unique
    uid = models.CharField(verbose_name='文件编号', max_length=100,
                           blank=True, null=True)
    tech_card = models.OneToOneField(HeatTreatmentTechCard,
                                     verbose_name='所属工艺卡',
                                     on_delete=models.CASCADE)
    writer = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               related_name='HTTMPL_writer',
                               on_delete=models.SET_NULL)
    write_date = models.DateField(verbose_name='编制日期',
                                  blank=True, null=True)
    reviewer = models.ForeignKey(User, verbose_name='审核人',
                                 blank=True, null=True,
                                 related_name='HTTMPL_reviewer',
                                 on_delete=models.SET_NULL)
    review_date = models.DateField(verbose_name='审核日期',
                                   blank=True, null=True)
    path = models.FileField(verbose_name='文件路径', upload_to='%Y/%m/%d')

    class Meta:
        verbose_name = '热处理测温点布置'
        verbose_name_plural = '热处理测温点布置'

    def __str__(self):
        return 'RR02-{}'.format(self.uid)


class TechPlan(models.Model):
    # TODO: blank=False, null=False
    work_order = models.ForeignKey(WorkOrder, verbose_name='所属工作令',
                                   blank=True, null=True,
                                   on_delete=models.SET_NULL)
    detail = models.CharField(verbose_name='详细内容', max_length=100,
                              blank=True, null=True)
    department = models.ForeignKey(Department, verbose_name='下发部门',
                                   on_delete=models.CASCADE)
    estimated_finish_date = models.DateField(verbose_name='计划完成时间')
    month = models.IntegerField(verbose_name='所属月份')
    year = models.IntegerField(verbose_name='所属年份')

    class Meta:
        verbose_name = '技术准备计划'
        verbose_name_plural = '技术准备计划'

    def __str__(self):
        return str(self.work_order)


class ConnectOrientation(models.Model):
    work_order = models.ForeignKey(WorkOrder, verbose_name='所属工作令',
                                   on_delete=models.CASCADE)
    name = models.CharField(verbose_name='文件名称', max_length=100)
    path = models.FileField(verbose_name='文件路径', upload_to='%Y/%m/%d')
    upload_dt = models.DateTimeField(verbose_name='上传时间',
                                     auto_now_add=True)
    # TODO: file size as IntegerField
    size = models.CharField(verbose_name='文件大小', max_length=50,
                            blank=True, null=True, default=None)
    # TODO: Review: Is this needed?
    file_type = models.CharField(verbose_name='文件类型', max_length=50,
                                 blank=True, null=True, default=None)

    class Meta:
        verbose_name = '管口方位图'
        verbose_name_plural = '管口方位图'

    def __str__(self):
        return self.name


class WeldingStep(models.Model):
    layer = models.CharField(verbose_name='层/道', max_length=100,
                             blank=True, null=True)
    weld_method = models.ForeignKey(WeldMethod, verbose_name='所属焊接方法',
                                    blank=True, null=True,
                                    on_delete=models.SET_NULL)
    instruction = models.ForeignKey(WeldingWorkInstruction,
                                    verbose_name='焊接作业指导书')
    # TODO: Field type?
    polarity = models.CharField(verbose_name='极性', max_length=100,
                                blank=True, null=True)
    # TODO: IntegerField?
    electricity = models.CharField(verbose_name='电流', max_length=100,
                                   blank=True, null=True)
    # TODO: IntegerField?
    voltage = models.CharField(verbose_name='电流电压', max_length=100,
                               blank=True, null=True)
    # TODO: IntegerField?
    welding_speed = models.CharField(verbose_name='焊接速度', max_length=100,
                                     blank=True, null=True)
    # TODO: IntegerField?
    heat_input = models.CharField(verbose_name='线能量', max_length=100,
                                  blank=True, null=True)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, null=True)

    class Meta:
        verbose_name = '焊接层道卡'
        verbose_name_plural = '焊接层道卡'

    def __str__(self):
        return self.layer
