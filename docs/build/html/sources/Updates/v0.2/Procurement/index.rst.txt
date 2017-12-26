采购模块
===============================
- 模型 **FakeMateriel** 重命名为 **ProcurementMaterial**
- 模型 **SupplierFile** 重命名为 **SupplierDocument**
- 模型 **SupplierSelect** 重命名为 **SupplyRelationship**
- 模型 **Quote** 重命名为 **Quotation**
- 删除 **BiddingSheetStatus** 模型
- 删除 **PurchaseOrderStatus** 模型
- 删除 **CommentStatus** 模型
- 删除 **MaterielPurchaseRelationSheet** 模型
- 删除 **MaterielPurchasingStatus** 模型
- **ProcurementMaterial**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        origin_materiel         process_material
        ----------------------- -----------------------
        related_materiel        merged_material
        ----------------------- -----------------------
        delivery_time           delivery_dt
        ----------------------- -----------------------
        material_category       category
        ======================= =======================

    - 修改 *delivery_dt* 为 *DateTimeField*

- **MaterialExecution**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        materiel_choice         material_type
        ----------------------- -----------------------
        tech_requirement        process_requirement
        ======================= =======================

    - 删除 *tech_feedback* 字段

- **PurchaseOrder**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        auditor                 lister
        ======================= =======================

    - 修改 *status* 为 *IntegerField*
    - 删除 *number* 字段

- **BiddingSheet**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        contract_id             contract_number
        ======================= =======================

    - 修改 *purchase_order* 为 *OneToOneField*
    - 修改 *status* 为 *IntegerField*
    - 删除 *list_date*, *audit_date*, *approve_date* 字段
    - 删除 *prepaid_amount*, *payable_amount* 属性
    - 删除 *supplier_select* 方法

- **ContractDetail**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        user                    submitter
        ----------------------- -----------------------
        submit_date             submit_dt
        ======================= =======================
    
    - 修改 *submit_dt* 为 *DateTimeField*
    - 修改 *amount* 为 *FloatField*

- **BaseComment**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        submit_date             submit_dt
        ======================= =======================

    - 修改 *submit_dt* 为 *DateTimeField*

- **SupplierDocument**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        submit_date             submit_dt
        ======================= =======================

    - 删除 *name* 字段
    - 删除 *size* 字段
    - 删除 *file_type* 字段

- **Supplier**
    - 添加 *bidding_sheets* 字段

- **SupplierCheck**
    - 修改 *status* 为 *IntegerField*
    - 修改 *estimated_price* 为 *FloatField*

- **SupplyRelationship**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        submit_date             submit_dt
        ======================= =======================

    - 修改 *price* 为 *FloatField*

- **BiddingApplication**
    - 修改 *status* 为 *IntegerField*

- **ParityRatioCard**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        apply_company           applicant
        ----------------------- -----------------------
        demand_company          requestor
        ======================= =======================

    - 修改 *status* 为 *IntegerField*

- **ArrivalInspection**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        materiel                material
        ----------------------- -----------------------
        is_pass                 passed
        ======================= =======================

    - 修改 *material* 为 *OneToOneField*
    - 删除 *bidding_sheet* 字段

- **MaterialSubApply**
    - 修改 *status* 为 *IntegerField*

- **StatusChange**
    - 修改 *original_status* 为 *IntegerField*
    - 修改 *new_status* 为 *IntegerField*

- **MaterialExecutionDetail**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        materiel                material
        ======================= =======================
