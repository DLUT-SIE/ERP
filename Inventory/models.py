from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from Core.models import SubWorkOrder
from Procurement.models import FakeMateriel
from Inventory import (ENTRYSTATUS_CHOICES, ENTRYSTATUS_CHOICES_PUCAHSER,
                       STORE_ITEM_STATUS_CHOICES, STORE_ITEM_STATUS_NORMAL,
                       STORE_ITEM_STATUS_SPENT, APPLYCARD_STATUS_CHOICES,
                       APPLYCARD_STATUS_APPLICANT, STOREROOM_TYPE_CHOICES,
                       STOREROOM_TYPE_WELD, STEEL_TYPES,
                       STEEL_TYPE_BOARD_STEEL, REFUNDSTATUS_CHOICES,
                       REFUNDSTATUS_REFUNDER,
                       AUXILIARY_TOOL_APPLY_STATUS_CHOICES,
                       AUXILIARY_TOOL_APPLY_STATUS_APPLICANT,
                       MATERIAL_CATEGORY_CHOICES,
                       BOUGHTIN_COMPONENT_CHOICES,
                       BOUGHTIN_COMPONENT_COOPERATION)


class WeldMaterialEntry(models.Model):
    uid = models.CharField(verbose_name='单据编号', max_length=20,
                           unique=True)
    create_date = models.DateField(verbose_name='入库时间', auto_now_add=True)
    purchaser = models.ForeignKey(User, verbose_name='采购员',
                                  related_name='weldentry_purchaser',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检验员',
                                  related_name='weldentry_inspector',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               related_name='weldentry_keeper',
                               blank=True, null=True,
                               on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='入库单状态',
                                 choices=ENTRYSTATUS_CHOICES,
                                 default=ENTRYSTATUS_CHOICES_PUCAHSER)

    class Meta:
        verbose_name = '焊材入库单'
        verbose_name_plural = '焊材入库单'

    def __str__(self):
        return self.uid

    def match_status(self, status):
        return self.entry_status == status


class WeldMaterialEntryItems(models.Model):
    entry = models.ForeignKey(WeldMaterialEntry, verbose_name='焊材入库单',
                              on_delete=models.CASCADE)
    material = models.ForeignKey(FakeMateriel, verbose_name='材料',
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, default='')
    production_date = models.DateField(verbose_name='出厂日期',
                                       blank=True, null=True)
    factory = models.CharField(verbose_name='厂家', max_length=100,
                               blank=True, null=True)
    price = models.FloatField(verbose_name='单价',
                              blank=True, null=True)
    total_weight = models.FloatField(verbose_name='公斤数', default=0)
    single_weight = models.FloatField(verbose_name='单件重量', default=0)
    count = models.FloatField(verbose_name='件数', default=0)
    material_charge_number = models.CharField(verbose_name='材料批号',
                                              max_length=20,
                                              null=True, blank=True)
    material_code = models.CharField(verbose_name='材质编号', max_length=20,
                                     null=True, blank=True)
    material_mark = models.CharField(verbose_name='牌号', max_length=50,
                                     null=True, blank=True)
    model_number = models.CharField(verbose_name='型号', max_length=50,
                                    null=True, blank=True)
    specification = models.CharField(verbose_name='规格', max_length=20,
                                     null=True, blank=True)

    class Meta:
        verbose_name = '焊材入库材料'
        verbose_name_plural = '焊材入库材料'

    def __str__(self):
        return '{}({})'.format(self.material.name, self.entry)


class WeldStoreListManager(models.Manager):
    def qualified_set(self):
        return self.filter(deadline__gte=timezone.now())


class WeldStoreList(models.Model):
    deadline = models.DateField(verbose_name='最后期限',
                                null=True, blank=True)
    count = models.FloatField(verbose_name='数量', default=0)
    entry_item = models.ForeignKey(WeldMaterialEntryItems,
                                   verbose_name='焊材入库单材料',
                                   on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='材料状态',
                                 choices=STORE_ITEM_STATUS_CHOICES,
                                 default=STORE_ITEM_STATUS_NORMAL)
    objects = WeldStoreListManager()

    class Meta:
        verbose_name = '焊材库存清单'
        verbose_name_plural = '焊材库存清单'

    def __str__(self):
        return '{}'.format(self.entry_item.specification)

    def save(self, *args, **kwargs):
        # TODO: Review this method
        if self.count > 0 and self.item_status == STORE_ITEM_STATUS_SPENT:
            self.item_status = STORE_ITEM_STATUS_NORMAL  # 退库更新状态
        if self.item_status == STORE_ITEM_STATUS_NORMAL and self.count == 0:
            self.item_status = STORE_ITEM_STATUS_SPENT  # 领用更新状态
        super(WeldStoreList, self).save(*args, **kwargs)


# TODO: blank and null, True or False?
class WeldingMaterialApplyCard(models.Model):
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    work_order = models.ForeignKey(SubWorkOrder, verbose_name='工作令',
                                   on_delete=models.CASCADE)
    # TODO: ForeignKey?
    department = models.CharField(verbose_name='领用单位', max_length=20,
                                  null=True, blank=True)
    create_date = models.DateField(verbose_name='填写时间', auto_now_add=True)
    weld_seam_uid = models.CharField(verbose_name='焊缝编号', max_length=20,
                                     blank=True, null=True)
    material_mark = models.CharField(verbose_name='焊材牌号', max_length=50)
    model_number = models.CharField(verbose_name='型号', max_length=50,
                                    blank=True, null=True)
    specification = models.CharField(verbose_name='规格', max_length=20)
    apply_weight = models.FloatField(verbose_name='领用重量')
    apply_count = models.FloatField(verbose_name='领用数量')
    material_code = models.CharField(verbose_name='材质标记', max_length=20,
                                     blank=True, null=True)
    actual_weight = models.FloatField(verbose_name='实发重量',
                                      blank=True, null=True)
    actual_count = models.FloatField(verbose_name='实发数量',
                                     blank=True, null=True)
    applicant = models.ForeignKey(User, verbose_name='领用人',
                                  blank=True, null=True,
                                  related_name='weld_material_apply_applicant',
                                  on_delete=models.SET_NULL)
    auditor = models.ForeignKey(User, verbose_name='审核人',
                                blank=True, null=True,
                                related_name='weld_material_apply_auditor',
                                on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检查员',
                                  blank=True, null=True,
                                  related_name='weld_material_apply_inspector',
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='发料人',
                               blank=True, null=True,
                               related_name='weld_material_apply_keeper',
                               on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='领用状态',
                                 choices=APPLYCARD_STATUS_CHOICES,
                                 default=APPLYCARD_STATUS_APPLICANT)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, null=True)
    storelist = models.ForeignKey(WeldStoreList, verbose_name='库存材料',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '焊材领用卡'
        verbose_name_plural = '焊材领用卡'

    def __str__(self):
        return self.uid


class StoreRoom(models.Model):
    name = models.CharField(verbose_name='库房名称', max_length=20)
    position = models.CharField(verbose_name='位置', max_length=50,
                                null=True, blank=True)
    material_type = models.IntegerField(verbose_name='材料类型',
                                        choices=STOREROOM_TYPE_CHOICES,
                                        default=STOREROOM_TYPE_WELD)

    class Meta:
        verbose_name = '库房'
        verbose_name_plural = '库房'

    def __str__(self):
        return str(self.name)


class WeldingMaterialHumitureRecord(models.Model):
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               on_delete=models.CASCADE)
    actual_temp_1 = models.FloatField(verbose_name='实际温度(10:00)')
    actual_humid_1 = models.FloatField(verbose_name='实际湿度(10:00)')
    actual_temp_2 = models.FloatField(verbose_name='实际温度(16:00)')
    actual_humid_2 = models.FloatField(verbose_name='实际湿度(16:00)')
    remark = models.CharField(verbose_name='备注', max_length=1000,
                              blank=True, null=True)
    date = models.DateField(verbose_name='日期', auto_now_add=True)

    def __str__(self):
        return '{}({})'.format(self.date, self.keeper)

    class Meta:
        verbose_name = '焊材库温湿度记录卡'
        verbose_name_plural = '焊材库温湿度记录卡'


class WeldingMaterialBakeRecord(models.Model):
    uid = models.CharField(verbose_name='编号', max_length=50, unique=True)
    date = models.DateField(verbose_name='日期')
    standard_num = models.CharField(verbose_name='标准号', max_length=50,
                                    null=True, blank=True)
    size = models.CharField(verbose_name='规格', max_length=50,
                            null=True, blank=True)
    class_num = models.CharField(verbose_name='牌号', max_length=50)
    heat_num = models.CharField(verbose_name='炉批号', max_length=50)
    codedmark = models.CharField(verbose_name='编码标记', max_length=50,
                                 null=True, blank=True)
    quantity = models.FloatField(verbose_name='数量', default=0)
    furnace_time = models.DateTimeField(verbose_name='进炉时间',
                                        blank=True, null=True)
    baking_temp = models.FloatField(verbose_name='烘焙温度', default=0)
    heating_time = models.DateTimeField(verbose_name='到达温度时间',
                                        blank=True, null=True)
    cooling_time = models.DateTimeField(verbose_name='降温时间',
                                        blank=True, null=True)
    # TODO: verbose_name?
    holding_time = models.DateTimeField(verbose_name='进保湿炉时间',
                                        blank=True, null=True)
    holding_temp = models.FloatField(verbose_name='保温温度', default=0)
    apply_time = models.DateTimeField(verbose_name='领用时间',
                                      blank=True, null=True)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               related_name='weldbake_keeper',
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    welding_engineer = models.ForeignKey(User, verbose_name='焊接工程师',
                                         related_name='weldbake_engineer',
                                         blank=True, null=True,
                                         on_delete=models.SET_NULL)
    remark = models.CharField(verbose_name='备注', max_length=1000,
                              null=True, blank=True)

    def __str__(self):
        return str(self.uid)

    class Meta:
        verbose_name = '焊材烘焙记录卡'
        verbose_name_plural = '焊材烘焙记录卡'


class SteelMaterialEntry(models.Model):
    source = models.CharField(max_length=20, verbose_name='货物来源')
    uid = models.CharField(max_length=20, verbose_name='入库单编号')
    purchaser = models.ForeignKey(User, verbose_name='采购员',
                                  blank=True, null=True,
                                  related_name='steel_entry_purchaser',
                                  on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检验员',
                                  blank=True, null=True,
                                  related_name='steel_entry_inspector',
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               blank=True, null=True,
                               related_name='steel_entry_keeper',
                               on_delete=models.SET_NULL)
    create_date = models.DateField(verbose_name='入库时间', auto_now_add=True)
    status = models.IntegerField(verbose_name='入库单状态',
                                 choices=ENTRYSTATUS_CHOICES,
                                 default=ENTRYSTATUS_CHOICES_PUCAHSER)
    steel_type = models.IntegerField(verbose_name='入库单类型',
                                     choices=STEEL_TYPES,
                                     default=STEEL_TYPE_BOARD_STEEL)
    remark = models.CharField(verbose_name='备注', max_length=100, default='')

    def __str__(self):
        return str(self.uid)

    class Meta:
        verbose_name = '钢材入库单'
        verbose_name_plural = '钢材入库单'


class SteelMaterialEntryItems(models.Model):
    material = models.ForeignKey(FakeMateriel, verbose_name='物料',
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)
    entry = models.ForeignKey(SteelMaterialEntry, verbose_name='钢材入库单',
                              on_delete=models.CASCADE)
    work_order = models.ManyToManyField(SubWorkOrder, verbose_name='工作令')
    name_spec = models.CharField(verbose_name='名称及规格', max_length=20)
    batch_number = models.CharField(verbose_name='炉批号', max_length=20,
                                    blank=True, null=True)
    material_mark = models.CharField(verbose_name='材料牌号', max_length=20,
                                     blank=True, null=True)
    # TODO: Replace with uid?
    material_code = models.CharField(max_length=20, verbose_name='标记号')
    weight = models.FloatField(verbose_name='重量')
    unit = models.CharField(verbose_name='单位', max_length=20,
                            blank=True, null=True)
    count = models.IntegerField(verbose_name='数量')
    length = models.FloatField(verbose_name='长度', blank=True, null=True)
    schematic_index = models.CharField(verbose_name='标准号或图号',
                                       max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = '钢材入库材料'
        verbose_name_plural = '钢材入库材料'

    def __str__(self):
        return str(self.name_spec)

    def show_workorder(self):
        # TODO: Necessary?
        return ', '.join(str(x) for x in self.work_order.all())


class SteelMaterialStoreList(models.Model):
    entry_item = models.ForeignKey(SteelMaterialEntryItems,
                                   verbose_name='钢材入库材料',
                                   on_delete=models.CASCADE)
    name_spec = models.CharField(verbose_name='名称及规格', max_length=50)
    steel_type = models.IntegerField(verbose_name='材料类型',
                                     choices=STEEL_TYPES)
    # TODO: blank=False null=False?
    length = models.FloatField(verbose_name='长度', blank=True, null=True)
    count = models.IntegerField(verbose_name='数量')
    weight = models.FloatField(verbose_name='重量')
    cancelling_count = models.IntegerField(verbose_name='退库次数', default=0)
    store_room = models.ForeignKey(StoreRoom, verbose_name='库房位置',
                                   blank=True, null=True,
                                   on_delete=models.SET_NULL)
    refund = models.IntegerField(verbose_name='退库单', blank=True, null=True)

    class Meta:
        verbose_name = '钢材库存材料'
        verbose_name_plural = '钢材库存材料'

    def __str__(self):
        return str(self.name_spec)


class SteelMaterialApplyCard(models.Model):
    # TODO: ForeignKey?
    department = models.CharField(verbose_name='领用单位', max_length=50)
    create_date = models.DateField(verbose_name='日期', auto_now_add=True)
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    applicant = models.ForeignKey(User, verbose_name='领料人',
                                  blank=True, null=True,
                                  related_name='steel_apply_applicant',
                                  on_delete=models.SET_NULL)
    auditor = models.ForeignKey(User, verbose_name='审核人',
                                blank=True, null=True,
                                related_name='steel_apply_auditor',
                                on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检查员',
                                  blank=True, null=True,
                                  related_name='steel_apply_inspector',
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='发料人',
                               blank=True, null=True,
                               related_name='steel_apply_keeper',
                               on_delete=models.SET_NULL)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, null=True)
    status = models.IntegerField(verbose_name='领用状态',
                                 choices=APPLYCARD_STATUS_CHOICES,
                                 default=APPLYCARD_STATUS_APPLICANT)

    class Meta:
        verbose_name = '钢材领用单'
        verbose_name_plural = '钢材领用单'

    def __str__(self):
        return str(self.uid)


class SteelMaterialApplyCardItems(models.Model):
    storelist = models.ForeignKey(SteelMaterialStoreList,
                                  verbose_name='库存材料',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    apply_card = models.ForeignKey(SteelMaterialApplyCard,
                                   verbose_name='钢材领用单',
                                   on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='申请数量')
    material_mark = models.CharField(verbose_name='钢号', max_length=20)
    material_code = models.CharField(verbose_name='材质编号', max_length=20)
    component = models.CharField(verbose_name='零件编号', max_length=100,
                                 blank=True, null=True)
    work_order = models.ForeignKey(SubWorkOrder, verbose_name='工作令',
                                   on_delete=models.CASCADE)
    materiel = models.ForeignKey(FakeMateriel, verbose_name='工作票',
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL)
    specification = models.CharField(verbose_name='规格', max_length=50)

    class Meta:
        verbose_name = '钢材领用单材料'
        verbose_name_plural = '钢材领用单材料'

    def __str__(self):
        return '{}({})'.format(self.material_mark, self.specification)


class SteelMaterialRefundCard(models.Model):
    apply_card = models.ForeignKey(SteelMaterialApplyCard,
                                   verbose_name='领用单',
                                   blank=True, null=True,
                                   on_delete=models.SET_NULL)
    # TODO: Duplicate with apply_card's work_order?
    work_order = models.ForeignKey(SubWorkOrder, verbose_name='工作令',
                                   on_delete=models.CASCADE)
    create_date = models.DateField(verbose_name='日期', auto_now_add=True)
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    refunder = models.ForeignKey(User, verbose_name='退料人',
                                 blank=True, null=True,
                                 related_name='steel_refund_refunder',
                                 on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检查员',
                                  blank=True, null=True,
                                  related_name='steel_refund_inspector',
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               blank=True, null=True,
                               related_name='steel_refund_keeper',
                               on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='退库单状态',
                                 choices=REFUNDSTATUS_CHOICES,
                                 default=REFUNDSTATUS_REFUNDER)
    # TODO: Duplicate with apply_card.storelist.steel_type?
    steel_type = models.IntegerField(verbose_name='钢材类型',
                                     choices=STEEL_TYPES,
                                     default=STEEL_TYPE_BOARD_STEEL)

    class Meta:
        verbose_name = '钢材退库单'
        verbose_name_plural = '钢材退库单'

    def __str__(self):
        return str(self.uid)

    # TODO: Rename arg names
    def set_attr(self, apply_card, apply_card_item, refund_code):
        self.work_order = apply_card_item.work_order
        self.refund_code = refund_code
        self.apply_card = apply_card
        self.steel_type = apply_card_item.storelist.steel_type


class BoardSteelMaterialRefundItems(models.Model):
    applyitem = models.ForeignKey(SteelMaterialApplyCardItems,
                                  verbose_name='申请材料',
                                  on_delete=models.CASCADE)
    name = models.CharField(verbose_name='名称', max_length=20,
                            blank=True, null=True)
    refund_card = models.OneToOneField(SteelMaterialRefundCard,
                                       verbose_name='退库单表头',
                                       on_delete=models.CASCADE)
    status = models.CharField(verbose_name='状态', max_length=20)
    # TODO: Duplicate?
    specification = models.CharField(verbose_name='规格', max_length=50,
                                     blank=True, null=True)
    # TODO: Duplicate?
    count = models.IntegerField(verbose_name='数量')
    weight = models.FloatField(verbose_name='重量',
                               blank=True, null=True)
    graph_path = models.FileField(verbose_name='套料图', upload_to='%Y/%m/%d',
                                  blank=True, null=True)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              default='')

    class Meta:
        verbose_name = '板材退库材料'
        verbose_name_plural = '板材退库单材料'

    def __str__(self):
        return str(self.refund_card)

    def set_attr(self, refund_card, apply_card_item):
        self.applyitem = apply_card_item
        self.card_info = refund_card
        self.specification = apply_card_item.storelist.specification
        self.count = apply_card_item.storelist.count


class BarSteelMaterialRefundItems(models.Model):
    applyitem = models.ForeignKey(SteelMaterialApplyCardItems,
                                  verbose_name='申请材料',
                                  on_delete=models.CASCADE)
    name = models.CharField(verbose_name='名称', max_length=20,
                            blank=True, null=True)
    refund_card = models.ForeignKey(SteelMaterialRefundCard,
                                    verbose_name='退库单表头',
                                    on_delete=models.CASCADE)
    status = models.CharField(verbose_name='状态', max_length=20)
    specification = models.CharField(verbose_name='规格', max_length=50,
                                     blank=True, null=True)
    count = models.IntegerField(verbose_name='数量')
    weight = models.FloatField(verbose_name='重量', blank=True, null=True)
    length = models.FloatField(verbose_name='退库长度', blank=True, null=True)
    remark = models.CharField(verbose_name='备注', max_length=100, default='')

    class Meta:
        verbose_name = '型材退库单材料'
        verbose_name_plural = '型材退库单材料'

    def __str__(self):
        return str(self.refund_card)

    def set_attr(self, refund_card, apply_card_item):
        self.applyitem = apply_card_item
        self.refund_card = refund_card
        self.specification = apply_card_item.storelist.specification
        self.count = apply_card_item.storelist.count


class WeldRefund(models.Model):
    # TODO: ForeignKey?
    department = models.CharField(verbose_name='领用单位', max_length=20)
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    create_date = models.DateField(verbose_name='日期', auto_now_add=True)
    apply_card = models.OneToOneField(WeldingMaterialApplyCard,
                                      verbose_name='领用单编号',
                                      on_delete=models.CASCADE)
    weight = models.FloatField(verbose_name='退库量（重量）')
    count = models.FloatField(verbose_name='退库量（数量）',
                              null=True, blank=True)
    status = models.IntegerField(verbose_name='退库单状态',
                                 default=REFUNDSTATUS_REFUNDER,
                                 choices=REFUNDSTATUS_CHOICES)
    refunder = models.ForeignKey(User, verbose_name='退库人',
                                 null=True, blank=True,
                                 related_name='weldrefund_refunder',
                                 on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管人',
                               null=True, blank=True,
                               related_name='weldrefund_keeper',
                               on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '焊接材料退库卡'
        verbose_name_plural = '焊接材料退库卡'

    def __str__(self):
        return str(self.apply_card)

    # TODO: applycarditem?
    def set_attr(self, apply_card, applycarditem, uid):
        self.uid = uid
        self.apply_card = apply_card


class AuxiliaryToolEntry(models.Model):
    create_date = models.DateField(verbose_name='入库时间', auto_now_add=True)
    purchaser = models.ForeignKey(User, verbose_name='采购员',
                                  blank=True, null=True,
                                  related_name='au_purchaser',
                                  on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检验员',
                                  blank=True, null=True,
                                  related_name='au_inspector',
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               blank=True, null=True,
                               related_name='au_keeper',
                               on_delete=models.SET_NULL)
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    status = models.IntegerField(choices=ENTRYSTATUS_CHOICES,
                                 default=ENTRYSTATUS_CHOICES_PUCAHSER,
                                 verbose_name='入库单状态')

    class Meta:
        verbose_name = '辅助材料入库单'
        verbose_name_plural = '辅助材料入库单'

    def __str__(self):
        return str(self.uid)


class AuxiliaryToolEntryItems(models.Model):
    entry = models.ForeignKey(AuxiliaryToolEntry,
                              verbose_name='辅助工具入库单',
                              on_delete=models.CASCADE)
    name = models.CharField(verbose_name='名称', max_length=50)
    specification = models.CharField(verbose_name='规格', max_length=50,
                                     blank=True)
    count = models.FloatField(verbose_name='入库数量')
    unit = models.CharField(verbose_name='单位', max_length=50, blank=True)
    factory = models.CharField(verbose_name='厂家', max_length=100,
                               blank=True, null=True)
    # TODO: ForeignKey?
    supplier = models.CharField(verbose_name='供货商', max_length=100,
                                blank=True, null=True)
    remark = models.CharField(verbose_name='备注', max_length=100, default='')

    class Meta:
        verbose_name = '辅助材料入库材料'
        verbose_name_plural = '辅助材料入库材料'

    def __str__(self):
        return '{}({})'.format(self.name, self.specification)


class AuxiliaryToolStoreList(models.Model):
    entry_item = models.ForeignKey(AuxiliaryToolEntryItems,
                                   verbose_name='辅助工具入库材料',
                                   on_delete=models.CASCADE)
    count = models.FloatField(verbose_name='数量', blank=True, null=True)
    status = models.IntegerField(verbose_name='材料状态',
                                 choices=STORE_ITEM_STATUS_CHOICES,
                                 default=STORE_ITEM_STATUS_NORMAL)

    class Meta:
        verbose_name = '辅助库存材料'
        verbose_name_plural = '辅助库存材料'

    def __str__(self):
        return str(self.entry_item)

    def save(self, *args, **kwargs):
        # TODO: Whats's these?
        if self.count > 0 and self.item_status == STORE_ITEM_STATUS_SPENT:
            self.item_status = STORE_ITEM_STATUS_NORMAL  # 退库更新状态
        if self.item_status == STORE_ITEM_STATUS_NORMAL and self.count == 0:
            self.item_status = STORE_ITEM_STATUS_SPENT  # 领用更新状态
        super(AuxiliaryToolStoreList, self).save(*args, **kwargs)


class AuxiliaryToolApplyCard(models.Model):
    create_date = models.DateField(verbose_name='申请时间', auto_now_add=True)
    # TODO: ForeignKey?
    department = models.CharField(verbose_name='领用单位', max_length=50,
                                  blank=True, null=True)
    uid = models.CharField(verbose_name='料单编号', max_length=20, unique=True)
    apply_storelist = models.ForeignKey(AuxiliaryToolStoreList,
                                        verbose_name='申请材料',
                                        related_name='auap_apply_storelist',
                                        on_delete=models.CASCADE)
    apply_count = models.IntegerField(verbose_name='申请数量')
    actural_storelist = models.ForeignKey(AuxiliaryToolStoreList,
                                          verbose_name='实发材料',
                                          null=True, blank=True,
                                          related_name='auap_actual_storelist',
                                          on_delete=models.SET_NULL)
    actual_count = models.IntegerField(verbose_name='实发数量',
                                       null=True, blank=True)
    status = models.IntegerField(verbose_name='领用单状态',
                                 choices=AUXILIARY_TOOL_APPLY_STATUS_CHOICES,
                                 default=AUXILIARY_TOOL_APPLY_STATUS_APPLICANT)
    applicant = models.ForeignKey(User, verbose_name='领料',
                                  blank=True, null=True,
                                  related_name='at_applicants',
                                  on_delete=models.SET_NULL)
    auditor = models.ForeignKey(User, verbose_name='主管',
                                null=True, blank=True,
                                related_name='at_auditor',
                                on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='发料',
                               blank=True, null=True,
                               related_name='at_keeper',
                               on_delete=models.SET_NULL)
    remark = models.CharField(verbose_name='备注', default='', max_length=200)

    class Meta:
        verbose_name = '辅助材料领用卡'
        verbose_name_plural = '辅助材料领用卡'

    def __str__(self):
        return str(self.apply_storelist.entry_item)


class WeldStoreThreshold(models.Model):
    specification = models.CharField(verbose_name='规格', max_length=50)
    count = models.FloatField(verbose_name='数量')
    category = models.IntegerField(verbose_name='材料种类',
                                   choices=MATERIAL_CATEGORY_CHOICES)

    class Meta:
        verbose_name = '库存安全量'
        verbose_name_plural = '库存安全量'

    def __str__(self):
        return str(self.specification)


class OutsideStandardEntry(models.Model):
    purchaser = models.ForeignKey(User, verbose_name='采购员',
                                  blank=True, null=True,
                                  related_name='outside_entry_purchaser',
                                  on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检验员',
                                  blank=True, null=True,
                                  related_name='outside_entry_inspector',
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               blank=True, null=True,
                               related_name='outside_entry_keeper',
                               on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='入库单状态',
                                 choices=ENTRYSTATUS_CHOICES,
                                 default=ENTRYSTATUS_CHOICES_PUCAHSER)
    source = models.CharField(verbose_name='货物来源', max_length=50,
                              blank=True, null=True)
    # TODO: ForeignKey?
    bidding_sheet_uid = models.CharField(verbose_name='订购单编号',
                                         max_length=20,
                                         blank=True, null=True)
    inspection_record = models.CharField(verbose_name='接收检查记录表',
                                         max_length=20,
                                         blank=True, null=True)
    uid = models.CharField(verbose_name='编号', max_length=20,
                           blank=True, null=True)
    change_code = models.CharField(verbose_name='修改号', max_length=20,
                                   blank=True, null=True)
    sample_report = models.CharField(verbose_name='样表', max_length=20,
                                     blank=True, null=True)
    create_date = models.DateField(verbose_name='入库时间', auto_now_add=True)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, null=True)
    outside_type = models.IntegerField(verbose_name='外购件类型',
                                       choices=BOUGHTIN_COMPONENT_CHOICES,
                                       default=BOUGHTIN_COMPONENT_COOPERATION)

    class Meta:
        verbose_name = '外购件入库单'
        verbose_name_plural = '外购件入库单'

    def __str__(self):
        return str(self.uid)


class OutsideStandardItems(models.Model):
    entry = models.ForeignKey(OutsideStandardEntry, verbose_name='入库单',
                              on_delete=models.CASCADE)
    materiel = models.ForeignKey(FakeMateriel, verbose_name='物料',
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)
    work_order = models.ForeignKey(SubWorkOrder, verbose_name='工作令',
                                   on_delete=models.CASCADE)
    schematic_index = models.CharField(verbose_name='标准号或图号',
                                       max_length=50,
                                       blank=True, null=True)
    specification = models.CharField(verbose_name='名称及规格', max_length=50,
                                     blank=True, null=True)
    material_mark = models.CharField(verbose_name='材料牌号', max_length=50,
                                     blank=True, null=True)
    batch_number = models.CharField(verbose_name='炉批号', max_length=50,
                                    blank=True, null=True)
    material_code = models.CharField(verbose_name='标记号', max_length=20,
                                     blank=True, null=True)
    unit = models.CharField(verbose_name='单位', max_length=20,
                            blank=True, null=True)
    count = models.IntegerField(verbose_name='数量', default=0)
    weight = models.FloatField(verbose_name='净重', null=True, blank=True)
    heatnum = models.CharField(verbose_name='熔炼号', max_length=50,
                               null=True, blank=True)
    remark = models.CharField(verbose_name='备注', max_length=50,
                              blank=True, null=True)
    factory = models.CharField(verbose_name='生产厂家', max_length=50,
                               blank=True, null=True)
    ticket_number = models.CharField(verbose_name='票号', max_length=50,
                                     blank=True, null=True)

    class Meta:
        verbose_name = '外购件入库材料'
        verbose_name_plural = '外购件入库材料'

    def __str__(self):
        return str(self.specification)


class OutsideStorageList(models.Model):
    entry_item = models.OneToOneField(OutsideStandardItems,
                                      verbose_name='入库材料',
                                      on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='数量', default=0)
    category = models.IntegerField(verbose_name='外购件类型',
                                   choices=BOUGHTIN_COMPONENT_CHOICES,
                                   default=BOUGHTIN_COMPONENT_COOPERATION)

    class Meta:
        verbose_name = '外购件库存材料'
        verbose_name_plural = '外购件库存材料'

    def __str__(self):
        return str(self.entry_item)


class OutsideApplyCard(models.Model):
    applicant = models.ForeignKey(User, verbose_name='领用人',
                                  related_name='out_apply_applicant',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    auditor = models.ForeignKey(User, verbose_name='审核人',
                                related_name='out_apply_auditor',
                                blank=True, null=True,
                                on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检验员',
                                  related_name='out_apply_inspector',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               related_name='out_apply_keeper',
                               blank=True, null=True,
                               on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='领用单状态',
                                 choices=APPLYCARD_STATUS_CHOICES,
                                 default=APPLYCARD_STATUS_APPLICANT)
    change_code = models.CharField(verbose_name='修改号', max_length=50,
                                   blank=True, null=True)
    sample_report = models.CharField(verbose_name='样表', max_length=50,
                                     blank=True, null=True)
    applycard_code = models.CharField(verbose_name='编号', max_length=20)
    work_order = models.ForeignKey(SubWorkOrder, verbose_name='工作令',
                                   on_delete=models.CASCADE)
    materiel = models.ForeignKey(FakeMateriel, verbose_name='工作票',
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL)
    create_date = models.DateField(verbose_name='日期', auto_now_add=True)
    department = models.CharField(verbose_name='领用单位', max_length=20,
                                  null=True, blank=True)

    class Meta:
        verbose_name = '外购件领用单'
        verbose_name_plural = '外购件领用单'

    def __str__(self):
        return str(self.applycard_code)


class OutsideApplyCardItems(models.Model):
    apply_card = models.ForeignKey(OutsideApplyCard, verbose_name='领用单',
                                   on_delete=models.CASCADE)
    storelist = models.ForeignKey(OutsideStorageList,
                                  verbose_name='外购件库存材料',
                                  null=True, blank=True,
                                  on_delete=models.SET_NULL)
    schematic_index = models.CharField(verbose_name='标准号或图号',
                                       max_length=50,
                                       blank=True, null=True)
    name_spec = models.CharField(verbose_name='名称及规格', max_length=50,
                                 blank=True, null=True)
    material_mark = models.CharField(verbose_name='材料牌号', max_length=50,
                                     blank=True, null=True)
    material_code = models.CharField(verbose_name='标记号', max_length=20,
                                     blank=True, null=True)
    unit = models.CharField(verbose_name='单位', max_length=20,
                            blank=True, null=True)
    count = models.IntegerField(verbose_name='数量', default=0)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, null=True)

    class Meta:
        verbose_name = '外购件领用单材料'
        verbose_name_plural = '外购件领用单材料'

    def __str__(self):
        return '{}({})'.format(self.name_spec, self.apply_card)


class OutsideRefundCard(models.Model):
    refunder = models.ForeignKey(User, verbose_name='退库人',
                                 blank=True, null=True,
                                 related_name='out_refund_refunder',
                                 on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               blank=True, null=True,
                               related_name='out_refund_keeper',
                               on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='退库单状态',
                                 choices=REFUNDSTATUS_CHOICES,
                                 default=REFUNDSTATUS_REFUNDER)
    apply_card = models.ForeignKey(OutsideApplyCard,
                                   verbose_name='外购件领用单',
                                   on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='退库单编号', max_length=20,
                           unique=True)
    # TODO: Duplicate?
    work_order = models.ForeignKey(SubWorkOrder, verbose_name='工作令',
                                   on_delete=models.CASCADE)
    create_date = models.DateField(verbose_name='日期', auto_now_add=True)

    class Meta:
        verbose_name = '外购件退库单'
        verbose_name_plural = '外购件退库单'

    def __str__(self):
        return str(self.refund_code)
        return self.refund_code

    def set_attr(self, apply_card, applycard_item, uid):
        self.uid = uid
        self.apply_card = apply_card
        self.work_order = apply_card.work_order


class OutsideRefundCardItems(models.Model):
    refund_card = models.ForeignKey(OutsideRefundCard, verbose_name='退库单',
                                    on_delete=models.CASCADE)
    applyitem = models.ForeignKey(OutsideApplyCardItems,
                                  verbose_name='领用材料',
                                  on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='数量', default=0)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, null=True)

    class Meta:
        verbose_name = '外购件退库单材料'
        verbose_name_plural = '外购件退库单材料'

    def __str__(self):
        return str(self.applyitem.specification)

    def set_attr(self, refund_card, applycarditem):
        self.applyitem = applycarditem
        self.refundcard = refund_card
        self.count = applycarditem.storelist.count


class CardStatusStopRecord(models.Model):
    user = models.ForeignKey(User, verbose_name='操作者',
                             on_delete=models.CASCADE)
    create_date = models.DateField(verbose_name='日期', auto_now_add=True)
    category = models.CharField(verbose_name='单据类型', max_length=20)
    uid = models.CharField(verbose_name='单据ID', max_length=20,
                           unique=True)
    remark = models.CharField(verbose_name='原因', max_length=1000)

    class Meta:
        verbose_name = '单据终止记录'
        verbose_name_plural = '单据终止记录'

    def __str__(self):
        return '{}({})'.format(self.uid, self.category)
