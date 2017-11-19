from django.db import models
from django.contrib.auth.models import User

from Core.models import Materiel, SubWorkOrder
from Core.utils import gen_uuid
from Procurement import (BIDDING_SHEET_STATUS_CHOICES,
                         BIDDING_SHEET_PART_STATUS_CHOICES,
                         PURCHASE_ORDER_STATUS_CHOICES, IMPLEMENT_CLASS_CHOICES,
                         INVENTORY_TYPE, INVENTORY_TYPE_NOTSET,
                         BID_APPLY_TYPE_CHOICES, COMMENT_STATUS_CHOICES,
                         MATERIEL_TYPE_CHOICES,
                         COMMENT_USER_CHOICES,
                         SUPPLIER_SELECT_C_CHOICES)


# TODO: Review this model
class BiddingSheetStatus(models.Model):
    main_status = models.IntegerField(verbose_name='标单状态',
                                      choices=BIDDING_SHEET_STATUS_CHOICES)
    # TODO: Check unique or unique_together
    status = models.IntegerField(verbose_name='状态', unique=True,
                                 choices=BIDDING_SHEET_PART_STATUS_CHOICES)
    next_status = models.ForeignKey('self', verbose_name='下一状态',
                                    null=True, blank=True)

    class Meta:
        verbose_name = '标单状态'
        verbose_name_plural = '标单状态'

    def __str__(self):
        return self.get_part_status_display()


class PurchaseOrderStatus(models.Model):
    status = models.IntegerField(verbose_name='订购单状态',
                                 choices=PURCHASE_ORDER_STATUS_CHOICES)
    next_status = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        verbose_name = '订购单状态'
        verbose_name_plural = '订购单状态'

    def __str__(self):
        return self.get_status_display()


# TODO: what's this?
# TODO: *IMPORTANT* Fields mismatch between definition and logics
class FakeMateriel(Materiel):
    related_material = models.ForeignKey('self', verbose_name='关联伪物料',
                                         null=True, blank=True,
                                         on_delete=models.CASCADE)
    origin_materiel = models.ForeignKey(Materiel, verbose_name='原始物料',
                                        null=True, blank=True,
                                        on_delete=models.CASCADE)
    # TODO: Should be ForeignKey?
    work_order = models.CharField(verbose_name='工作令号', max_length=100,
                                  blank=True, null=True)
    sub_order = models.ForeignKey(SubWorkOrder, verbose_name='子工作令',
                                  blank=True, null=True,
                                  on_delete=models.CASCADE)
    inventory_type = models.IntegerField(verbose_name='明细类型',
                                         choices=INVENTORY_TYPE,
                                         default=INVENTORY_TYPE_NOTSET)
    batch_number = models.CharField(verbose_name='炉批号', max_length=50,
                                    blank=True, null=True)
    material_number = models.CharField(verbose_name='材质编号', max_length=50,
                                       blank=True, null=True)
    # TODO: DateField?
    delivery_time = models.CharField(verbose_name='交货期', max_length=50,
                                     blank=True, null=True)
    material_category = models.CharField(verbose_name='材料分类',
                                         max_length=50, blank=True, null=True)
    finished = models.BooleanField(verbose_name='是否结束', default=False)

    class Meta:
        verbose_name = '伪物料'
        verbose_name_plural = '伪物料'

    def __str__(self):
        return '{} {}'.format(self.name, self.specification)


class CommentStatus(models.Model):
    form_type = models.IntegerField(verbose_name='表单类型',
                                    choices=BID_APPLY_TYPE_CHOICES,
                                    blank=True, null=True)
    status = models.IntegerField(verbose_name='表单状态', unique=True,
                                 choices=COMMENT_STATUS_CHOICES)
    next_status = models.ForeignKey('self', verbose_name='下一状态',
                                    null=True, blank=True,
                                    on_delete=models.CASCADE)

    class Meta:
        verbose_name = '招标申请状态'
        verbose_name_plural = '招标申请状态'

    def __str__(self):
        return self.get_status_display()


class MaterielExecution(models.Model):
    uid = models.CharField(verbose_name='单据编号', max_length=100,
                           unique=True)
    lister = models.ForeignKey(User, verbose_name='制表人',
                               on_delete=models.CASCADE)
    # TODO: auto_now_add?
    list_date = models.DateField(verbose_name='制表日期')
    materiel_choice = models.CharField(verbose_name='材料选择', max_length=20,
                                       choices=MATERIEL_TYPE_CHOICES)
    saved = models.BooleanField(verbose_name='是否保存', default=False)
    tech_feedback = models.CharField(verbose_name='工艺反馈', max_length=100,
                                     blank=True, null=True)
    tech_requirement = models.CharField(
        verbose_name='工艺需求', max_length=5000, blank=True, null=True)

    class Meta:
        verbose_name = '材料执行表'
        verbose_name_plural = '材料执行表'

    def __str__(self):
        return self.uid


class PurchaseOrder(models.Model):
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    # TODO: auto_now_add
    create_date = models.DateTimeField(verbose_name='创建日期', null=True)
    list_date = models.DateTimeField(verbose_name='编制日期', null=True)
    audit_date = models.DateTimeField(verbose_name='审核日期',
                                      blank=True, null=True)
    approve_time = models.DateTimeField(verbose_name='批准日期',
                                        blank=True, null=True)
    status = models.ForeignKey(PurchaseOrderStatus, verbose_name='订购单状态',
                               on_delete=models.CASCADE)
    auditor = models.ForeignKey(User, verbose_name='编制人',
                                related_name='purchase_order_auditor',
                                null=True, blank=True,
                                on_delete=models.CASCADE)
    chief = models.ForeignKey(User, verbose_name='外采科长',
                              related_name='purchase_order_chief',
                              null=True, blank=True,
                              on_deelte=models.CASCADE)
    approver = models.ForeignKey(User, verbose_name='审批人',
                                 related_name='purchase_order_approver',
                                 null=True, blank=True,
                                 on_delete=models.CASCADE)
    tech_requirement = models.TextField(
        verbose_name='工艺需求', max_length=5000, blank=True, null=True)
    # TODO: choices?
    category = models.IntegerField(verbose_name='标单类型', default=0)
    # TODO: ForeignKey?
    work_order = models.CharField(verbose_name='工作令号', max_length=100,
                                  blank=True, null=True)
    number = models.CharField(verbose_name='编号', max_length=100,
                              blank=True, null=True)
    revised_number = models.CharField(verbose_name='修订号', max_length=100,
                                      blank=True, null=True)

    class Meta:
        verbose_name = '订购单'
        verbose_name_plural = '订购单'

    def __str__(self):
        return self.uid


class BiddingSheet(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder,
                                       verbose_name='对应订购单',
                                       null=True, blank=True,
                                       on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='标单编号', unique=True, max_length=20)
    # TODO: auto_now_add?
    create_date = models.DateField(verbose_name='创建日期',
                                   blank=True, null=True)
    list_date = models.DateField(verbose_name='编制日期',
                                 blank=True, null=True)
    audit_date = models.DateField(verbose_name='审核日期',
                                  blank=True, null=True)
    approve_date = models.DateField(verbose_name='批准日期',
                                    blank=True, null=True)
    status = models.ForeignKey(BiddingSheetStatus, verbose_name='标单状态')
    contract_id = models.CharField(verbose_name='合同编号', max_length=50,
                                   blank=True, default=gen_uuid)
    contract_amount = models.IntegerField(verbose_name='合同金额', default=0)
    billing_amount = models.IntegerField(verbose_name='开票金额', default=0)
    # TODO: Use choices?
    category = models.IntegerField(verbose_name='招标申请类型', default=0)

    class Meta:
        verbose_name = '标单'
        verbose_name_plural = '标单'

    def __str__(self):
        return self.uid

    @property
    def prepaid_amount(self):
        return sum(x.amount for x in self.contractdetail_set.all())

    @property
    def payable_amount(self):
        return self.billing_amount - self.prepaid_amount

    def supplier_select(self):
        # TODO: Is this method necessary?
        suppliers = self.supplierselect_set.all()
        return ', '.join(x.supplier.supplier_name for x in suppliers)


class ContractDetail(models.Model):
    # TODO: what's user related to?
    user = models.ForeignKey(User, verbose_name='用户',
                             on_delete=models.CASCADE)
    submit_date = models.DateField(verbose_name='提交日期', auto_now_add=True)
    amount = models.IntegerField(verbose_name='金额')
    bidding_sheet = models.ForeignKey(BiddingSheet, verbose_name='标单',
                                      on_delete=models.CASCADE)

    class Meta:
        verbose_name = '合同金额明细'
        verbose_name_plural = '合同金额明细'

    def __str__(self):
        return '{}:{}'.format(self.bidding_sheet, self.amount)


class BaseComment(models.Model):
    user = models.ForeignKey(User, verbose_name='用户',
                             on_delete=models.CASCADE)
    comment = models.CharField(verbose_name='审批意见', max_length=400)
    submit_date = models.DateField(verbose_name='提交日期', auto_now_add=True)

    class Meta:
        abstract = True


class BiddingComment(BaseComment):
    bidding_sheet = models.ForeignKey(BiddingSheet, verbose_name='标单',
                                      on_delete=models.CASCADE)
    user_title = models.IntegerField(verbose_name='审批人属性',
                                     choices=COMMENT_USER_CHOICES)

    class Meta:
        verbose_name = '标单评审意见'
        verbose_name_plural = '标单评审意见'

    def __str__(self):
        return '{}:{}'.format(self.bidding_sheet, self.user)


class MaterielPurchaseRelationSheet(models.Model):
    materiel = models.OneToOneField(FakeMateriel, verbose_name='物料',
                                    on_delete=models.CASCADE)
    # TODO: blank=False, null=False
    purchase_order = models.ForeignKey(PurchaseOrder, verbose_name='订购单',
                                       blank=True, null=True,
                                       on_delete=models.CASCADE)
    # TODO: blank=False, null=False
    bidding_sheet = models.ForeignKey(BiddingSheet, verbose_name='标单',
                                      blank=True, null=True,
                                      on_delete=models.CASCADE)
    count = models.CharField(verbose_name='需求数量',
                             blank=True, null=True, max_length=20)
    # TODO: Rename?
    purchasing = models.CharField(verbose_name='采购', max_length=20,
                                  blank=True, null=True)

    class Meta:
        verbose_name = '物料-采购关联表'
        verbose_name_plural = '物料-采购关联表'

    def __str__(self):
        # TODO: New representation
        return '{} {}'.format(self.materiel.name, self.materiel.specification)


class BiddingApplication(models.Model):
    uid = models.CharField(verbose_name='标单申请编号', max_length=50,
                           unique=True)
    applicant = models.CharField(verbose_name='申请单位', max_length=40,
                                 blank=True, null=True)
    requestor = models.CharField(verbose_name='需求单位', max_length=40,
                                 blank=True, null=True)
    amount = models.IntegerField(verbose_name='数量', default=0)
    # TODO: ForeignKey?
    work_order = models.CharField(verbose_name='工作令', max_length=100,
                                  blank=True, null=True)
    plan_project = models.CharField(verbose_name='拟招(议)项目', max_length=40,
                                    blank=True, null=True)
    plan_date = models.DateField(verbose_name='拟招(议)标时间',
                                 blank=True, null=True)
    model = models.CharField(verbose_name='规格、型号', max_length=40,
                             null=True, blank=True)
    is_core_part = models.BooleanField(verbose_name='是否为核心件',
                                       default=False)
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    category = models.CharField(verbose_name='项目类别', max_length=40,
                                null=True, blank=True)
    # TODO: The original version is auto_now_add,
    # but I dont't think it should be
    tender_date = models.DateField(verbose_name='招(议)标时间',
                                   null=True, blank=True)
    # TODO: The original version is auto_now_add,
    # but I dont't think it should be
    delivery_date = models.DateField(verbose_name='标书递送时间',
                                     null=True, blank=True)
    place = models.CharField(verbose_name='地点', max_length=40,
                             null=True, blank=True)
    status = models.ForeignKey(CommentStatus, verbose_name='招标申请表状态',
                               on_delete=models.CASCADE)
    implement_class = models.IntegerField(verbose_name='实施类别',
                                          choices=IMPLEMENT_CLASS_CHOICES)

    class Meta:
        verbose_name = '标单申请表'

    def __str__(self):
        return str(self.bidding_sheet.uid)


class ParityRatioCard(models.Model):
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    # TODO: Are these fields Necessay?
    apply_id = models.CharField(verbose_name='标单申请编号', max_length=20,
                                blank=True, null=True)
    apply_company = models.CharField(verbose_name='申请单位', max_length=40,
                                     blank=True, null=True)
    demand_company = models.CharField(verbose_name='需求单位', max_length=40,
                                      null=True, blank=True)
    # TODO: ForeignKey?
    work_order = models.CharField(verbose_name='工作令', max_length=50,
                                  null=True, blank=True)
    amount = models.IntegerField(verbose_name='数量', null=True, blank=True)
    unit = models.CharField(verbose_name='单位', max_length=40,
                            blank=True, null=True)
    content = models.CharField(verbose_name='内容', max_length=40,
                               blank=True, null=True)
    material = models.CharField(verbose_name='材质', max_length=40,
                                blank=True, null=True)
    delivery_period = models.CharField(verbose_name='交货期', max_length=40,
                                       blank=True, null=True)
    status = models.ForeignKey(CommentStatus, verbose_name='招标申请表状态',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = '比质比价卡'

    def __str__(self):
        return str(self.bidding_sheet.uid)


class SupplierCheck(models.Model):
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    applicant = models.CharField(verbose_name='申请单位', max_length=40,
                                 blank=True, null=True)
    application_date = models.DateField(verbose_name='申请日期',
                                        null=True, blank=True)
    project = models.CharField(verbose_name='项目名称', max_length=40,
                               null=True, blank=True)
    # TODO: IntegerField?
    estimated_price = models.CharField(verbose_name='估算价格', max_length=40,
                                       null=True, blank=True)
    basic_situation = models.CharField(verbose_name='招（议）标项目基本情况',
                                       max_length=100,
                                       null=True, blank=True)
    status = models.ForeignKey(CommentStatus, verbose_name='招标申请表状态',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = '供应商审核'
        verbose_name_plural = '供应商审核'

    def __str__(self):
        return str(self.bidding_sheet.uid)


class Supplier(models.Model):
    uid = models.CharField(verbose_name='供应商编号', max_length=20,
                           unique=True)
    name = models.CharField(verbose_name='供应商名称', max_length=50)

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = '供应商'

    def __str__(self):
        return self.name


class SupplierFile(models.Model):
    supplier = models.ForeignKey(Supplier, verbose_name='供应商',
                                 on_delete=models.CASCADE)
    name = models.CharField(verbose_name='名称', max_length=100)
    path = models.FileField(verbose_name='路径', upload_to='%Y/%m/%d')
    upload_dt = models.DateTimeField(verbose_name='上传时间',
                                     auto_now_add=True)
    # TODO: IntegerField?
    size = models.CharField(verbose_name='大小', max_length=50,
                            blank=True, null=True, default=None)
    # TODO: necessary?
    file_type = models.CharField(verbose_name='文件类型', max_length=50,
                                 blank=True, null=True, default=None)

    class Meta:
        verbose_name = '供应商文件'
        verbose_name_plural = '供应商文件'

    def __str__(self):
        return self.name


class ArrivalInspection(models.Model):
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    materiel = models.ForeignKey(FakeMateriel, verbose_name='材料')
    material_confirm = models.BooleanField(verbose_name='实物确认',
                                           default=False)
    soft_confirm = models.BooleanField(verbose_name='软件确认',
                                       default=False)
    inspection_confirm = models.BooleanField(verbose_name='检验通过',
                                             default=False)
    is_pass = models.BooleanField(verbose_name='是否通过', default=False)

    class Meta:
        verbose_name = '到货检验'
        verbose_name_plural = '到货检验'

    def __str__(self):
        return '{}({})'.format(self.bidding_sheet.uid, self.material.name)


class MaterielPurchasingStatus(models.Model):
    materiel = models.OneToOneField(FakeMateriel, verbose_name='物料',
                                    on_delete=models.CASCADE)
    # TODO: what's add_to_detail?
    add_to_detail = models.BooleanField(default=False, verbose_name='未设置')

    class Meta:
        verbose_name = '物料采购状态'
        verbose_name_plural = '物料采购状态'

    def __str__(self):
        return '{} {}'.format(self.materiel.name, self.materiel.specification)


# TODO: Rethink this model
class SupplierSelect(models.Model):
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, verbose_name='供应商',
                                 on_delete=models.CASCADE)
    # TODO: what are these fields?
    A = models.BooleanField(verbose_name='A', blank=True, default=False)
    B = models.BooleanField(verbose_name='B', blank=True, default=False)
    C = models.IntegerField(verbose_name='C',
                            choices=SUPPLIER_SELECT_C_CHOICES,
                            blank=True, null=True)
    D = models.BooleanField(verbose_name='D', blank=True, default=False)
    E = models.BooleanField(verbose_name='E', blank=True, default=False)
    F = models.BooleanField(verbose_name='F', blank=True, default=False)
    G = models.BooleanField(verbose_name='G', blank=True, default=False)
    scope = models.CharField(verbose_name='认定业务范围', max_length=40,
                             blank=True, null=True)
    supplier_code = models.CharField(verbose_name='供方代码', max_length=40,
                                     blank=True, null=True)
    price = models.CharField(verbose_name='价格', max_length=40,
                             blank=True, null=True)
    status = models.CharField(verbose_name='厂家协作能力质量情况及业绩',
                              max_length=200, blank=True, null=True)
    delivery_payment = models.CharField(verbose_name='交货及支付条件',
                                        max_length=40, blank=True, null=True)

    class Meta:
        verbose_name = '供应商选择'
        verbose_name_plural = '供应商选择'
        unique_together = (('bidding_sheet', 'supplier'))

    def __str__(self):
        return '{} 选择 {}'.format(self.bidding_sheet.uid, self.supplier.name)


class MaterialSubApply(models.Model):
    uid = models.CharField(verbose_name='单据编号', max_length=100,
                           unique=True)
    figure_code = models.CharField(verbose_name='图号', max_length=100,
                                   blank=True, null=True)
    # TODO: ForeignKey?
    work_order = models.CharField(verbose_name='工作令', max_length=50,
                                  blank=True, null=True)
    # TODO: ForeignKey?
    production = models.CharField(verbose_name='产品名称', max_length=50,
                                  blank=True, null=True)
    reason = models.CharField(verbose_name='代用原因和理由', max_length=1000,
                              blank=True, null=True)
    applicant = models.ForeignKey(User, verbose_name='申请人',
                                  null=True, blank=True,
                                  on_delete=models.CASCADE)
    status = models.ForeignKey(CommentStatus, verbose_name='招标申请表状态',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = '材料代用申请单'
        verbose_name_plural = '材料代用申请单'

    def __str__(self):
        return self.uid


class SubApplyComment(BaseComment):
    sub_apply = models.ForeignKey(MaterialSubApply,
                                  verbose_name='材料代用申请单',
                                  on_delete=models.CASCADE)
    user_title = models.IntegerField(verbose_name='审批人属性',
                                     choices=COMMENT_USER_CHOICES)

    class Meta:
        verbose_name = '材料代用评审意见'
        verbose_name_plural = '材料代用评审意见'

    def __str__(self):
        return '{}:{}'.format(self.sub_apply, self.user)


class MaterialSubApplyItems(models.Model):
    sub_apply = models.ForeignKey(MaterialSubApply,
                                  verbose_name='材料代用申请单',
                                  on_delete=models.CASCADE)
    part_figure_code = models.CharField(verbose_name='部件图号',
                                        max_length=100)
    # TODO: Duplicate with previous one?
    part_ticket_code = models.CharField(verbose_name='零件图号或票号',
                                        max_length=100)
    old_name = models.CharField(verbose_name='原材料名称',
                                max_length=100)
    old_standard = models.CharField(verbose_name='原材料标准',
                                    max_length=100)
    old_size = models.CharField(verbose_name='原材料规格和尺寸',
                                max_length=100)
    new_name = models.CharField(verbose_name='拟用材料名称', max_length=100)
    new_standard = models.CharField(verbose_name='拟用材料标准',
                                    max_length=100)
    new_size = models.CharField(verbose_name='拟用材料规格和尺寸',
                                max_length=100)

    class Meta:
        verbose_name = '材料代用申请条目'
        verbose_name_plural = '材料代用申请条目'

    def __str__(self):
        return '{}({})'.format(self.sub_apply.uid, self.part_figure_code)


class ProcessFollowingInfo(models.Model):
    bidding_sheet = models.ForeignKey(BiddingSheet, verbose_name='标单',
                                      on_delete=models.CASCADE)
    following_date = models.DateField(verbose_name='跟踪日期')
    following_method = models.CharField(verbose_name='跟踪方式', max_length=20)
    following_feedback = models.CharField(verbose_name='跟踪反馈',
                                          max_length=500)
    path = models.FileField(verbose_name='文件对象',
                            null=True, blank=True, upload_to='%Y/%m/%d')
    executor = models.ForeignKey(User, verbose_name='执行人',
                                 on_delete=models.CASCADE)
    inform_process = models.BooleanField(verbose_name='是否通知工艺',
                                         default=False)

    class Meta:
        verbose_name = '过程跟踪记录'
        verbose_name_plural = '过程跟踪记录'

    def __str__(self):
        return self.bidding_sheet.uid


class StatusChange(models.Model):
    bidding_sheet = models.ForeignKey(BiddingSheet, verbose_name='标单',
                                      on_delete=models.CASCADE)
    original_status = models.ForeignKey(BiddingSheetStatus,
                                        verbose_name='原状态',
                                        related_name='status_change_original',
                                        on_delete=models.CASCADE)
    new_status = models.ForeignKey(BiddingSheetStatus, verbose_name='新状态',
                                   related_name='status_change_new',
                                   on_delete=models.CASCADE)
    change_user = models.ForeignKey(User, verbose_name='更改用户',
                                    on_delete=models.CASCADE)
    change_time = models.DateTimeField(verbose_name='更改时间',
                                       auto_now_add=True)
    normal_change = models.BooleanField(verbose_name='是否正常更改',
                                        default=True)
    reason = models.CharField(verbose_name='回溯原因',
                              max_length=1000,
                              blank=True, null=True)

    class Meta:
        verbose_name = '状态更改'
        verbose_name_plural = '状态更改'

    def __str__(self):
        return '{}({}:{})'.format(self.bidding_sheet,
                                  self.original_status,
                                  self.new_status)


class MaterielExecutionDetail(models.Model):
    # TODO: on_delete?
    materiel_execution = models.ForeignKey(MaterielExecution,
                                           verbose_name='材料执行',
                                           null=True, blank=True,
                                           on_delete=models.SET_NULL)
    materiel = models.ForeignKey(FakeMateriel, verbose_name='物料',
                                 on_delete=models.CASCADE)
    batch_number = models.CharField(verbose_name='出厂批号', max_length=50,
                                    null=True, blank=True)
    quota = models.CharField(verbose_name='定额', max_length=50,
                             null=True, blank=True)
    part = models.CharField(verbose_name='零件', max_length=50,
                            null=True, blank=True)
    oddments = models.CharField(verbose_name='余料', max_length=50,
                                null=True, blank=True)
    remark = models.CharField(verbose_name='备注', max_length=200,
                              null=True, blank=True)

    class Meta:
        verbose_name = '材料执行表详细情况'
        verbose_name_plural = '材料执行表详细情况'

    def __str__(self):
        return '{}-{}'.format(self.materiel_execution, self.materiel)


class BiddingAcceptance(models.Model):
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    # TODO: unique?
    uid = models.CharField(verbose_name='标书编号', max_length=50,
                           blank=True, null=True)
    # TODO: auto relate?
    requestor = models.CharField(verbose_name='招（议）标单位', max_length=40,
                                 blank=True, null=True)
    content = models.CharField(verbose_name='招（议）标内容', max_length=40,
                               blank=True, null=True)
    # TODO: IntegerField?
    amount = models.CharField(verbose_name='数量', null=True, max_length=40)
    accept_date = models.DateField(verbose_name='中标日期',
                                   null=True, blank=True)
    accept_money = models.CharField(verbose_name='中标金额', max_length=40,
                                    null=True, blank=True)
    accept_supplier = models.ForeignKey(Supplier, verbose_name='中标单位',
                                        null=True, blank=True,
                                        on_delete=models.CASCADE)
    contact = models.CharField(verbose_name='联系人', max_length=40,
                               null=True, blank=True)
    contact_phone = models.CharField(verbose_name='联系电话', max_length=40,
                                     null=True, blank=True)

    class Meta:
        verbose_name = '中标通知书'
        verbose_name_plural = '中标通知书'

    def __str__(self):
        return '{}'.format(self.bidding_sheet.uid)


class Quote(models.Model):
    inventory_type = models.IntegerField(verbose_name='明细类型',
                                         choices=INVENTORY_TYPE,
                                         default=INVENTORY_TYPE_NOTSET)
    name_spec = models.CharField(verbose_name='规格及名称', max_length=50,
                                 blank=True, null=True)
    material_mark = models.CharField(verbose_name='材质或牌号', max_length=50,
                                     blank=True, null=True)
    unit_price = models.CharField(verbose_name='单价', max_length=50,
                                  blank=True, null=True)
    unit = models.CharField(verbose_name='单位', max_length=50,
                            blank=True, null=True)
    supplier = models.ForeignKey(Supplier, verbose_name='供应商',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = '报价单'
        verbose_name_plural = '报价单'

    def __str__(self):
        return '{}-{}:{}({})'.format(self.name_spec, self.material_mark,
                                     self.supplier, self.unit_price)
