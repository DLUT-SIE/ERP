ENTRYSTATUS_CHOICES_STOP = -1
ENTRYSTATUS_CHOICES_PUCAHSER = 0
ENTRYSTATUS_CHOICES_INSPECTOR = 1
ENTRYSTATUS_CHOICES_KEEPER = 2
ENTRYSTATUS_CHOICES_END = 3
ENTRYSTATUS_CHOICES = (
    (ENTRYSTATUS_CHOICES_PUCAHSER, '待采购员确认'),
    (ENTRYSTATUS_CHOICES_INSPECTOR, '待检查确认'),
    (ENTRYSTATUS_CHOICES_KEEPER, '待库管确认'),
    (ENTRYSTATUS_CHOICES_END, '入库完成'),
    (ENTRYSTATUS_CHOICES_STOP, '入库终止'),
)

STORE_ITEM_STATUS_NORMAL = 0
STORE_ITEM_STATUS_SPENT = 1
STORE_ITEM_STATUS_OVERDUE = 2
STORE_ITEM_STATUS_SCRAPPED = 3
STORE_ITEM_STATUS_CHOICES = (
    (STORE_ITEM_STATUS_NORMAL, '正常使用'),
    (STORE_ITEM_STATUS_SPENT, '已用完'),
    (STORE_ITEM_STATUS_OVERDUE, '已过期'),
    (STORE_ITEM_STATUS_SCRAPPED, '已报废'),
)

APPLYCARD_STATUS_STOP = -1
APPLYCARD_STATUS_APPLICANT = 0
APPLYCARD_STATUS_AUDITOR = 1
APPLYCARD_STATUS_INSPECTOR = 2
APPLYCARD_STATUS_KEEPER = 3
APPLYCARD_STATUS_END = 4
APPLYCARD_STATUS_CHOICES = (
    (APPLYCARD_STATUS_APPLICANT, '领用申请'),
    (APPLYCARD_STATUS_AUDITOR, '领用审核'),
    (APPLYCARD_STATUS_INSPECTOR, '领用检查'),
    (APPLYCARD_STATUS_KEEPER, '领用发料'),
    (APPLYCARD_STATUS_END, '领用完成'),
    (APPLYCARD_STATUS_STOP, '领用终止'),
)

STOREROOM_TYPE_WELD = 0
STOREROOM_TYPE_STEEL = 1
STOREROOM_TYPE_AUXILIARY_TOOL = 2
STOREROOM_TYPE_OUTSIDEBUY = 3

STOREROOM_TYPE_CHOICES = (
    (STOREROOM_TYPE_WELD, '焊材'),
    (STOREROOM_TYPE_STEEL, '钢材'),
    (STOREROOM_TYPE_AUXILIARY_TOOL, '辅助工具'),
    (STOREROOM_TYPE_OUTSIDEBUY, '外购件'),
)

STEEL_TYPE_BOARD_STEEL = 0
STEEL_TYPE_BAR_STEEL = 1
STEEL_TYPES = (
    (STEEL_TYPE_BOARD_STEEL, '板材'),
    (STEEL_TYPE_BAR_STEEL, '型材'),
)

# TODO: Review names
REFUNDSTATUS_STOP = -1
REFUNDSTATUS_REFUNDER = 0
REFUNDSTATUS_INSPECTOR = 1
REFUNDSTATUS_KEEPER = 2
REFUNDSTATUS_END = 3
REFUNDSTATUS_CHOICES = (
    (REFUNDSTATUS_REFUNDER, '退库人'),
    (REFUNDSTATUS_INSPECTOR, '检查员'),
    (REFUNDSTATUS_KEEPER, '库管员'),
    (REFUNDSTATUS_END, '结束'),
    (REFUNDSTATUS_STOP, '终止'),
)

AUXILIARY_TOOL_APPLY_STATUS_STOP = -1
AUXILIARY_TOOL_APPLY_STATUS_APPLICANT = 0
AUXILIARY_TOOL_APPLY_STATUS_AUDITOR = 1
AUXILIARY_TOOL_APPLY_STATUS_KEEPER = 2
AUXILIARY_TOOL_APPLY_STATUS_END = 3
AUXILIARY_TOOL_APPLY_STATUS_CHOICES = (
    (AUXILIARY_TOOL_APPLY_STATUS_APPLICANT, '领料'),
    (AUXILIARY_TOOL_APPLY_STATUS_AUDITOR, '主管'),
    (AUXILIARY_TOOL_APPLY_STATUS_KEEPER, '发料'),
    (AUXILIARY_TOOL_APPLY_STATUS_END, '完成'),
    (AUXILIARY_TOOL_APPLY_STATUS_STOP, '终止'),
)

MATERIAL_CATEGORY_WELD_ROD = 0
MATERIAL_CATEGORY_WELD_WIRE = 1
MATERIAL_CATEGORY_WELD_RIBBON = 2
MATERIAL_CATEGORY_WELD_FLUX = 3
MATERIAL_CATEGORY_WELD = 4
MATERIAL_CATEGORY_SHEET = 5
MATERIAL_CATEGORY_PROFILE = 6
MATERIAL_CATEGORY_PURCHASED = 7
MATERIAL_CATEGORY_OTHER = 8
MATERIAL_CATEGORY_STEEL = 9
MATERIAL_CATEGORY_AUXILIARY_TOOL = 10
MATERIAL_CATEGORY_CHOICES = (
    (MATERIAL_CATEGORY_WELD_ROD, '焊条'),
    (MATERIAL_CATEGORY_WELD_WIRE, '焊丝'),
    (MATERIAL_CATEGORY_WELD_RIBBON, '焊带'),
    (MATERIAL_CATEGORY_WELD_FLUX, '焊剂'),
    (MATERIAL_CATEGORY_SHEET, '板材'),
    (MATERIAL_CATEGORY_PROFILE, '型材'),
    (MATERIAL_CATEGORY_PURCHASED, '外购件'),
    (MATERIAL_CATEGORY_AUXILIARY_TOOL, '辅助工具'),
    (MATERIAL_CATEGORY_OTHER, '其他'),
)

BOUGHTIN_COMPONENT_COOPERATION = 0
BOUGHTIN_COMPONENT_STANDARD = 1
BOUGHTIN_COMPONENT_FORGING = 2
BOUGHTIN_COMPONENT_CHOICES = (
    (BOUGHTIN_COMPONENT_COOPERATION, '外协加工'),
    (BOUGHTIN_COMPONENT_STANDARD, '标准件'),
    (BOUGHTIN_COMPONENT_FORGING, '锻件'),
)
