库存模块
===============================
- 添加模型 **AbstractEntry**, 抽象入库单
- 添加模型 **AbstractEntryDetail**, 抽象入库单明细
- 添加模型 **AbstractInventoryDetail**, 抽象库存明细
- 添加模型 **AbstractApplyCard**, 抽象领用明细
- 添加模型 **AbstractRefundCard**, 抽象退库单
- 添加模型 **AbstractSteelMaterialRefundDetail**, 抽象钢材退库明细
- 添加模型 **WeldingMaterialApplyDetail**
- 添加模型 **AuxiliaryMaterialApplyDetail**
- 添加模型 **WeldingMaterialRefundDetail**
- 所有入库单继承自 **AbstractEntry**, 字段重新设计
- 所有入库单明细继承自 **AbstractEntryDetail**, 字段重新设计
- 所有库存明细继承自 **AbstractInventoryDetail**, 字段重新设计
- 所有领用单继承自 **AbstractApplyCard**, 字段重新设计
- 所有退库单继承自 **AbstractRefundCard**, 字段重新设计
- 模型 **WeldMaterialEntry** 重命名为 **WeldingMaterialEntry**
- 模型 **AuxiliaryToolEntry** 重命名为 **AuxiliaryMaterialEntry**
- 模型 **OutsideStandardEntry** 重命名为 **BoughtInComponentEntry**
- 模型 **WeldMaterialEntryItems** 重命名为 **WeldingMaterialEntryDetail**
- 模型 **SteelMaterialEntryItems** 重命名为 **SteelMaterialEntryDetail**
- 模型 **AuxiliaryToolEntryItems** 重命名为 **AuxiliaryMaterialEntryDetail**
- 模型 **OutsideStandardItems** 重命名为 **BoughtInComponentEntryDetail**
- 模型 **WeldStoreList** 重命名为 **WeldingMaterialInventoryDetail**
- 模型 **SteelMaterialStoreList** 重命名为 **SteelMaterialInventoryDetail**
- 模型 **AuxiliaryToolStoreList** 重命名为 **AuxiliaryMaterialInventoryDetail**
- 模型 **OutsideStorageList** 重命名为 **BoughtInComponentInventoryDetail**
- 模型 **StoreRoom** 重命名为 **Warehouse**
- 模型 **WeldStoreThreshold** 重命名为 **WeldingWarehouseThreshold**
- 模型 **CardStatusStopRecord** 重命名为 **InventoryTerminationRecord**
- 模型 **AuxiliaryToolApplyCard** 重命名为 **AuxiliaryMaterialApplyCard**
- 模型 **OutsideApplyCard** 重命名为 **BoughtInComponentApplyCard**
- 模型 **SteelMaterialApplyCardItems** 重命名为 **SteelMaterialApplyDetail**
- 模型 **OutsideApplyCardItems** 重命名为 **BoughtInComponentApplyDetail**
- 模型 **WeldRefund** 重命名为 **WeldingMaterialRefundCard**
- 模型 **OutsideRefundCard** 重命名为 **BoughtInComponentRefundCard**
- 模型 **BoardSteelMaterialRefundItems** 重命名为 **BoardSteelMaterialRefundDetail**
- 模型 **BarSteelMaterialRefundItems** 重命名为 **BarSteelMaterialRefundDetail**
- 模型 **OutsideRefundCardItems** 重命名为 **BoughtInComponentRefundDetail**
- 删除 **MaterielPurchasingStatus** 模型
- **BoughtInComponentEntry**
    - 字段重命名

        ===================== ===============
        改动前                  改动后
        --------------------- ---------------
        outside_type            category
        ===================== ===============

- **WeldingMaterialEntryDetail**
    - 字段重命名

        =========================== ===============
        改动前                      改动后
        --------------------------- ---------------
        single_weight               weight
        =========================== ===============

    - 删除 *material_charge_number* 字段
    - 删除 *total_weight* 字段
    - 删除 *price* 字段
    - 删除 *material_code* 字段
    - 删除 *material_mark* 字段
    - 删除 *model_number* 字段
    - 删除 *specification* 字段

- **SteelMaterialEntryDetail**
    - 删除 *work_order* 字段
    - 删除 *name_spec* 字段
    - 删除 *batch_number* 字段
    - 删除 *material_mark* 字段
    - 删除 *material_code* 字段
    - 删除 *schematic_index* 字段
    - 删除 *show_workorder* 方法

- **AuxiliaryMaterialEntryDetail**
    - 删除 *name* 字段
    - 删除 *specification* 字段
    - 删除 *supplier* 字段

- **BoughtInComponentEntryDetail**
    - 字段重命名

        =========================== ===============
        改动前                      改动后
        --------------------------- ---------------
        heatnum                     heat_number
        =========================== ===============

    - 删除 *work_order* 字段
    - 删除 *schematic_index* 字段
    - 删除 *specification* 字段
    - 删除 *material_mark* 字段
    - 删除 *batch_number* 字段
    - 删除 *material_code* 字段
    - 删除 *heat_number* 字段
    - 删除 *ticket_number* 字段

- **WeldingInventoryDetail**
    - 字段重命名

        =========================== ===============
        改动前                      改动后
        --------------------------- ---------------
        entry_item                  entry_detail
        =========================== ===============

- **SteelMaterialInventoryDetail**
    - 字段重命名

        =========================== ===============
        改动前                      改动后
        --------------------------- ---------------
        entry_item                  entry_detail
        --------------------------- ---------------
        store_room                  warehouse
        --------------------------- ---------------
        cancelling_count            refund_times
        =========================== ===============

    - 删除 *name_spec* 字段
    - 删除 *steel_type* 字段
    - 删除 *refund* 字段

- **AuxiliaryMaterialInventoryDetail**
    - 字段重命名

        =========================== ===============
        改动前                      改动后
        --------------------------- ---------------
        entry_item                  entry_detail
        =========================== ===============

- **Warehouse**
    - 字段重命名

        =========================== ===============
        改动前                      改动后
        --------------------------- ---------------
        entry_item                  entry_detail
        --------------------------- ---------------
        material_type               category
        =========================== ===============

- **WeldingMaterialHumitureRecord**
    - 字段重命名

        =========================== ===============
        改动前                      改动后
        --------------------------- ---------------
        date                        created
        =========================== ===============

    - 修改 *created* 为 *DateTimeField*

- **WeldingMaterialBakeRecord**
    - 字段重命名

        =========================== ===============
        改动前                      改动后
        --------------------------- ---------------
        date                        created
        =========================== ===============

    - 修改 *created* 为 *DateTimeField*
    - 删除 *uid* 字段

- **WeldingWarehouseThreshold**
    - 字段重命名

        =========================== ===============
        改动前                      改动后
        --------------------------- ---------------
        date                        created
        =========================== ===============

- **InventoryTerminationRecord**
    - 字段重命名

        =========================== ===============
        改动前                      改动后
        --------------------------- ---------------
        create_date                 created
        --------------------------- ---------------
        remark                      reason
        =========================== ===============

    - 修改 *created* 为 *DateTimeField*
    - 修改 *category* 为 *IntegerField*

- **WeldingMaterialApplyCard**
    - 字段重命名

        =========================== ===================
        改动前                      改动后
        --------------------------- -------------------
        storelist                   inventory
        =========================== ===================

    - 移动多个字段至焊材领用单明细

- **AuxiliaryMaterialApplyCard**
    - 删除 *apply_inventory* 字段
    - 删除 *apply_count* 字段
    - 删除 *actual_inventory* 字段
    - 删除 *actual_count* 字段

- **BoughtInComponentApplyCard**
    - 字段重命名

        =========================== ===================
        改动前                      改动后
        --------------------------- -------------------
        change_code                 revised_number
        --------------------------- -------------------
        materiel                    material
        =========================== ===================

    - 删除 *applycard_code* 字段

- **SteelMaterialApplyDetail**
    - 字段重命名

        =========================== ===================
        改动前                      改动后
        --------------------------- -------------------
        change_code                 revised_number
        --------------------------- -------------------
        work_order                  sub_order
        =========================== ===================

    - 删除 *storelist* 字段

- **BoughtInComponentApplyDetail**
    - 字段重命名

        =========================== ===================
        改动前                      改动后
        --------------------------- -------------------
        storelist                   inventory
        =========================== ===================

    - 删除 *schematic_index* 字段
    - 删除 *name_spec* 字段
    - 删除 *material_mark* 字段
    - 删除 *material_code* 字段
    - 删除 *unit* 字段

- **SteelMaterialRefundCard**
    - 字段重命名

        =========================== ===================
        改动前                      改动后
        --------------------------- -------------------
        create_date                 created
        =========================== ===================

    - 修改 *created* 为 *DateTimeField*
    - 删除 *work_order* 字段
    - 删除 *steel_type* 字段
    - 删除 *set_attr* 方法

- **WeldingMaterialRefundCard**
    - 删除 *set_attr* 方法

- **BoughtInComponentRefundCard**
    - 删除 *set_attr* 方法

- **BoardSteelMaterialRefundDetail**
    - 删除 *set_attr* 方法

- **BarSteelMaterialRefundDetail**
    - 删除 *set_attr* 方法

- **BoughtInComponentRefundCard**
    - 删除 *set_attr* 方法
