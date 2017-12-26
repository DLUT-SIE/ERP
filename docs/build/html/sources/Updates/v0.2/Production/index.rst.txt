生产模块
===============================
- 模型 *SubMateriel* 重命名为 *SubMaterial*
- 模型 *ComprehensiveDepartmentFileList* 重命名为 *ComprehensiveDepartmentFileCheck*
- **SubMaterial**
    - 字段重命名

        =============== ==========
        改动前           改动后
        --------------- ----------
        materiel        material
        =============== ==========

- **ProcessDetail**
    - 字段重命名

        ========================== ======================
        改动前                      改动后
        -------------------------- ----------------------
        sub_materiel                sub_material
        -------------------------- ----------------------
        inspection_content          remark
        ========================== ======================

- **ProductionPlan**
    - 删除 *uid* 字段
