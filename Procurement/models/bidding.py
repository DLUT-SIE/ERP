from django.db import models
from django.db.models import Sum
from Core.utils import gen_uuid
from Procurement import (BIDDING_SHEET_STATUS_CHOICES, COMMENT_STATUS_CHOICES,
                         IMPLEMENT_CLASS_CHOICES)
from Core.utils.fsm import transition, TransitionMeta
from Procurement import (
    BIDDING_SHEET_STATUS_CREATE, BIDDING_SHEET_STATUS_SELECT_SUPPLLER_APPROVED,
    BIDDING_SHEET_STATUS_INVITE_BID_APPLY_SELECT,
    BIDDING_SHEET_STATUS_INVITE_BID_FILL,
    BIDDING_SHEET_STATUS_INVITE_BID_CARRY,
    BIDDING_SHEET_STATUS_INVITE_BID_COMPLETE,
    BIDDING_SHEET_STATUS_PROCESS_FOLLOW, BIDDING_SHEET_STATUS_CHECK,
    BIDDING_SHEET_STATUS_STORE, BIDDING_SHEET_STATUS_COMPLETE,
    BIDDING_SHEET_STATUS_STOP)

from Procurement import (
    COMMENT_STATUS_APPLY_FILL,
    COMMENT_STATUS_APPLY_OPERATOR_COMMENT,
    COMMENT_STATUS_APPLY_LEAD_COMMENT,
    COMMENT_STATUS_APPLY_NEED_COMMENT,
    COMMENT_STATUS_APPLY_CENTRALIZE_COMMENT,
    COMMENT_STATUS_APPLY_LOGISTICAL_COMMENT,
    COMMENT_STATUS_APPLY_COMPANY_COMMENT,
    COMMENT_STATUS_QUALITY_FILL,
    COMMENT_STATUS_QUALITY_OPERATOR_COMMENT,
    COMMENT_STATUS_QUALITY_NEED_TECH_COMMENT,
    COMMENT_STATUS_QUALITY_NEED_LEAD_COMMENT,
    COMMENT_STATUS_QUALITY_COMPREHENSIVE_COMMENT,
    COMMENT_STATUS_QUALITY_COMPANY_COMMENT,
    COMMENT_STATUS_APPLY_FINISH,
)


class BiddingSheet(models.Model, metaclass=TransitionMeta):
    """
    标单
    """
    purchase_order = models.OneToOneField('PurchaseOrder',
                                          verbose_name='对应订购单',
                                          on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='标单编号', unique=True, max_length=20)
    # TODO: auto_now_add?
    create_dt = models.DateTimeField(verbose_name='创建时间',
                                     blank=True, null=True)
    status = models.IntegerField(verbose_name='标单状态', unique=True,
                                 choices=BIDDING_SHEET_STATUS_CHOICES)
    contract_number = models.CharField(verbose_name='合同编号', max_length=50,
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
        if not hasattr(self, '__prepaid_amount'):
            self.__prepaid_amount = self.contractdetail_set.aggregate(
                Sum('amount'))['amount__sum'] or 0
        return self.__prepaid_amount

    @property
    def payable_amount(self):
        return self.billing_amount - self.prepaid_amount

    @transition(field='status', source=BIDDING_SHEET_STATUS_CREATE,
                target=BIDDING_SHEET_STATUS_SELECT_SUPPLLER_APPROVED)
    def select_supplier_approved():
        # TODO
        pass

    @transition(
        field='status', source=BIDDING_SHEET_STATUS_SELECT_SUPPLLER_APPROVED,
        target=BIDDING_SHEET_STATUS_INVITE_BID_APPLY_SELECT)
    def invite_bid_apply_selected():
        # TODO
        pass

    @transition(
        field='status', source=BIDDING_SHEET_STATUS_INVITE_BID_APPLY_SELECT,
        target=BIDDING_SHEET_STATUS_INVITE_BID_FILL)
    def invite_bid_filled():
        # TODO
        pass

    @transition(field='status', source=BIDDING_SHEET_STATUS_INVITE_BID_FILL,
                target=BIDDING_SHEET_STATUS_INVITE_BID_CARRY)
    def invite_bid_carried():
        # TODO
        pass

    @transition(field='status', source=BIDDING_SHEET_STATUS_INVITE_BID_CARRY,
                target=BIDDING_SHEET_STATUS_INVITE_BID_COMPLETE)
    def invite_bid_completed():
        # TODO
        pass

    @transition(
        field='status', source=BIDDING_SHEET_STATUS_INVITE_BID_COMPLETE,
        target=BIDDING_SHEET_STATUS_PROCESS_FOLLOW)
    def process_followed():
        # TODO
        pass

    @transition(field='status', source=BIDDING_SHEET_STATUS_PROCESS_FOLLOW,
                target=BIDDING_SHEET_STATUS_CHECK)
    def checked():
        # TODO
        pass

    @transition(field='status', source=BIDDING_SHEET_STATUS_CHECK,
                target=BIDDING_SHEET_STATUS_STORE)
    def stored():
        # TODO
        pass

    @transition(field='status', source=BIDDING_SHEET_STATUS_STORE,
                target=BIDDING_SHEET_STATUS_COMPLETE)
    def completed():
        # TODO
        pass

    @transition(field='status', source=BIDDING_SHEET_STATUS_COMPLETE,
                target=BIDDING_SHEET_STATUS_STOP)
    def stopped():
        # TODO
        pass

    # 状态回溯
    @transition(field='status', source=BIDDING_SHEET_STATUS_STOP,
                target=BIDDING_SHEET_STATUS_COMPLETE)
    def completed_rollback():
        # TODO
        pass

    @transition(
        field='status', source=BIDDING_SHEET_STATUS_COMPLETE,
        target=BIDDING_SHEET_STATUS_STORE)
    def stored_rollback():
        # TODO
        pass

    @transition(
        field='status', source=BIDDING_SHEET_STATUS_STORE,
        target=BIDDING_SHEET_STATUS_CHECK)
    def checked_rollback():
        # TODO
        pass

    @transition(field='status', source=BIDDING_SHEET_STATUS_CHECK,
                target=BIDDING_SHEET_STATUS_PROCESS_FOLLOW)
    def process_follow_rollbacked():
        # TODO
        pass

    @transition(field='status', source=BIDDING_SHEET_STATUS_PROCESS_FOLLOW,
                target=BIDDING_SHEET_STATUS_INVITE_BID_COMPLETE)
    def invite_bid_completed_rollback():
        # TODO
        pass

    @transition(
        field='status', source=BIDDING_SHEET_STATUS_INVITE_BID_COMPLETE,
        target=BIDDING_SHEET_STATUS_INVITE_BID_CARRY)
    def invite_bid_carried_rollback():
        # TODO
        pass

    @transition(field='status', source=BIDDING_SHEET_STATUS_INVITE_BID_CARRY,
                target=BIDDING_SHEET_STATUS_INVITE_BID_FILL)
    def invite_bid_filled_rollback():
        # TODO
        pass

    @transition(field='status', source=BIDDING_SHEET_STATUS_INVITE_BID_FILL,
                target=BIDDING_SHEET_STATUS_INVITE_BID_APPLY_SELECT)
    def invite_bid_apply_selected_rollback():
        # TODO
        pass

    @transition(
        field='status', source=BIDDING_SHEET_STATUS_INVITE_BID_APPLY_SELECT,
        target=BIDDING_SHEET_STATUS_SELECT_SUPPLLER_APPROVED)
    def select_supplier_approved_rollback():
        # TODO
        pass

    @transition(
        field='status', source=BIDDING_SHEET_STATUS_SELECT_SUPPLLER_APPROVED,
        target=BIDDING_SHEET_STATUS_CREATE)
    def created_rollback():
        # TODO
        pass


# TODO: Require all fields when necessary
class BiddingApplication(models.Model, metaclass=TransitionMeta):
    """
    标单申请表
    """
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='标单申请编号', max_length=50,
                           unique=True)
    applicant = models.CharField(verbose_name='申请单位', max_length=40)
    requestor = models.CharField(verbose_name='需求单位', max_length=40)
    amount = models.IntegerField(verbose_name='数量', default=0)
    # TODO: ForeignKey?
    work_order = models.CharField(verbose_name='工作令', max_length=100,
                                  blank=True, null=True)
    plan_project = models.CharField(verbose_name='拟招(议)项目', max_length=40,
                                    blank=True, null=True)
    plan_dt = models.DateTimeField(verbose_name='拟招(议)标时间',
                                   blank=True, null=True)
    model = models.CharField(verbose_name='规格、型号', max_length=40,
                             null=True, blank=True)
    is_core_part = models.BooleanField(verbose_name='是否为核心件',
                                       default=False)
    category = models.CharField(verbose_name='项目类别', max_length=40,
                                null=True, blank=True)
    tender_dt = models.DateTimeField(verbose_name='招(议)标时间',
                                     null=True, blank=True)
    delivery_dt = models.DateTimeField(verbose_name='标书递送时间',
                                       null=True, blank=True)
    place = models.CharField(verbose_name='地点', max_length=40,
                             null=True, blank=True)
    status = models.IntegerField(verbose_name='状态',
                                 choices=COMMENT_STATUS_CHOICES)
    implement_class = models.IntegerField(verbose_name='实施类别',
                                          choices=IMPLEMENT_CLASS_CHOICES)

    class Meta:
        verbose_name = '标单申请表'
        verbose_name_plural = '标单申请表'

    def __str__(self):
        return str(self.bidding_sheet)

    @transition(
        field='status', source=COMMENT_STATUS_APPLY_FILL,
        target=COMMENT_STATUS_APPLY_OPERATOR_COMMENT)
    def operator_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_APPLY_OPERATOR_COMMENT,
        target=COMMENT_STATUS_APPLY_LEAD_COMMENT)
    def lead_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_APPLY_LEAD_COMMENT,
        target=COMMENT_STATUS_APPLY_NEED_COMMENT)
    def need_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_APPLY_NEED_COMMENT,
        target=COMMENT_STATUS_APPLY_CENTRALIZE_COMMENT)
    def centralize_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_APPLY_CENTRALIZE_COMMENT,
        target=COMMENT_STATUS_APPLY_LOGISTICAL_COMMENT)
    def logistical_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_APPLY_LOGISTICAL_COMMENT,
        target=COMMENT_STATUS_APPLY_COMPANY_COMMENT)
    def company_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_APPLY_COMPANY_COMMENT,
        target=COMMENT_STATUS_APPLY_FINISH)
    def finish():
        # TODO
        pass


class ParityRatioCard(models.Model, metaclass=TransitionMeta):
    """
    比质比价卡
    """
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    apply_id = models.CharField(verbose_name='标单申请编号', max_length=20)
    applicant = models.CharField(verbose_name='申请单位', max_length=40)
    requestor = models.CharField(verbose_name='需求单位', max_length=40)
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
    status = models.IntegerField(verbose_name='状态',
                                 choices=COMMENT_STATUS_CHOICES)

    class Meta:
        verbose_name = '比质比价卡'
        verbose_name_plural = '比质比价卡'

    def __str__(self):
        return str(self.bidding_sheet)

    @transition(
        field='status', source=COMMENT_STATUS_QUALITY_FILL,
        target=COMMENT_STATUS_QUALITY_OPERATOR_COMMENT)
    def operator_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_QUALITY_OPERATOR_COMMENT,
        target=COMMENT_STATUS_QUALITY_NEED_TECH_COMMENT)
    def need_tech_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_QUALITY_NEED_TECH_COMMENT,
        target=COMMENT_STATUS_QUALITY_NEED_LEAD_COMMENT)
    def need_lead_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_QUALITY_NEED_LEAD_COMMENT,
        target=COMMENT_STATUS_QUALITY_COMPREHENSIVE_COMMENT)
    def comprehensive_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_QUALITY_COMPREHENSIVE_COMMENT,
        target=COMMENT_STATUS_QUALITY_COMPANY_COMMENT)
    def company_comment():
        # TODO
        pass


class BiddingAcceptance(models.Model):
    """
    中标通知书
    """
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='标书编号', max_length=50, unique=True)
    # TODO: auto relate?
    requestor = models.CharField(verbose_name='招（议）标单位', max_length=40,
                                 blank=True, default='')
    content = models.CharField(verbose_name='招（议）标内容', max_length=40,
                               blank=True, default='')
    # TODO: IntegerField?
    amount = models.CharField(verbose_name='数量', null=True, max_length=40)
    accept_dt = models.DateTimeField(verbose_name='中标时间',
                                     null=True, blank=True)
    accept_money = models.CharField(verbose_name='中标金额', max_length=40,
                                    null=True, blank=True)
    accept_supplier = models.ForeignKey('Supplier', verbose_name='中标单位',
                                        null=True, blank=True,
                                        on_delete=models.SET_NULL)
    contact = models.CharField(verbose_name='联系人', max_length=40,
                               null=True, blank=True)
    contact_phone = models.CharField(verbose_name='联系电话', max_length=40,
                                     null=True, blank=True)

    class Meta:
        verbose_name = '中标通知书'
        verbose_name_plural = '中标通知书'

    def __str__(self):
        return '{}'.format(self.bidding_sheet.uid)
