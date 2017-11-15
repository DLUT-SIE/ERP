SELL_TYPES = (
    (0, '内销'),
    (1, '外销'),
)

WELD_ROD = 1
WELD_WIRE = 2
WELD_RIBBON = 3
WELD_FLUX = 4
SHEET = 5
PROFILE = 6
PURCHASED = 7
AUXILIARY_TOOL = 8
OTHER = 0
MATERIAL_CATEGORY_CHOICES = (
    (WELD_ROD, "焊条"),
    (WELD_WIRE, "焊丝"),
    (WELD_RIBBON, "焊带"),
    (WELD_FLUX, "焊剂"),
    (SHEET, "板材"),
    (PROFILE, "型材"),
    (PURCHASED, "外购件"),
    (AUXILIARY_TOOL, "辅助工具"),
    (OTHER, "其他"),
)

GENDER_CHOICES = (
    (0, '男'),
    (1, '女'),
)

ROLE_CHOICES = (
    (-1, '未设置'),
)
