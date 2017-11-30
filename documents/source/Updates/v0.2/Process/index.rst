工艺模块
===============================
- 从 **Core** 模块移动模型 **Materiel**
- 添加 **ProcessLibrary** 模型, 用以分离工艺物料与工作令之间的关系
- 添加 **QuotaList** 模型, 用以关联定额明细与工艺物料
- 模型 **Materiel** 重命名为 **ProcessMaterial**
- 模型 **AuxiliaryItem** 重命名为 **AuxiliaryQuotaItem**
- 模型 **PrincipalItem** 重命名为 **PrincipalQuotaItem**
- 模型 **WeldQuota** 重命名为 **WeldingQuotaItem**
- 模型 **WeldJointTechDetail** 重命名为 **WeldingJointProcessAnalysis**
- 模型 **WeldCertification** 重命名为 **WeldingCertification**
- 模型 **WeldSeam** 重命名为 **WeldingSeam**
- 模型 **WeldingWorkInstructionTest** 重命名为 **WeldingWorkInstructionExamination**
- 模型 **ProgramingNestingChart** 重命名为 **ProgrammingBlankingChart**
- 模型 **WeldingStep** 重命名为 **WeldingLayerCard**
- 模型 **OutPurchasedItem** 重命名为 **BoughtInItem**
- 删除 **Signature** 模型
- 删除 **ProcessStep** 模型
- 删除 **Circulation** 模型
- 删除 **TransferCardSignature** 模型
- 删除 **ProcessLibrarySignature** 模型
- **Material**
    - 字段重命名

        ======================= ===============
        改动前                  改动后
        ----------------------- ---------------
        material_id             uid
        ======================= ===============

    - 删除 *display_material_name* 方法

- **ProcessMaterial**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        index                   ticket_number
        ----------------------- -----------------------
        sub_index               part_number
        ----------------------- -----------------------
        schematic_index         drawing_number
        ----------------------- -----------------------
        parent_schematic_index  parent_drawing_number
        ----------------------- -----------------------
        parent_name             name
        ----------------------- -----------------------
        specification           spec
        ----------------------- -----------------------
        net_weight              piece_weight
        ======================= =======================

    - 修改 *ticket_number* 为 *IntegerField*
    - 修改 *part_number* 为 *IntegerField*
    - 修改 *count* 为 *IntegerField*
    - 删除 *total_weight* 字段
    - 删除 *quota* 字段
    - 删除 *quota_coefficient* 字段
    - 删除 *standard* 字段
    - 删除 *unit* 字段
    - 删除 *status* 字段
    - 删除 *press* 字段
    - 删除 *recheck* 字段
    - 删除 *detection_level* 字段
    - 删除 *total_weight_cal* 方法
    - 删除 *route* 方法

- **AuxiliaryQuotaItem**
    - 修改 *quota_coef* 为 *FloatField*

- **PrincipalQuotaItem**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        stardard                operative_norm
        ======================= =======================

    - 添加 *quota_list* 字段
    - 修改 *count* 为 *IntegerField*
    - 删除 *work_order* 字段
    - 删除 *total_weight* 方法
    - 删除 *stadard_status* 方法

- **WeldQuotaItem**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        order                   work_order
        ----------------------- -----------------------
        stardard                operative_norm
        ======================= =======================

    - 添加 *quota_list* 字段
    - 修改 *quota* 为 *FloatField*
    - 删除 *work_order* 字段

- **ProcessRoute**
    - 使用 `Sx` 和 `Hx` 来代表工序和工时, x取值范围为[1, 12]
    - 修改 *Hx* 为 *FloatField*

- **CirculationRoute**
    - 使用 `Cx` 来代表流转, x取值范围为[1, 10]
    - 删除 *full_name* 字段

- **TransferCard**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        weld_test_plate_index   welding_plate_idx
        ----------------------- -----------------------
        parent_test_plate_index parent_plate_idx
        ======================= =======================

    - 添加 *writer*, *write_date*, *reviewer*, *review_date*, *proofreader*, *proofread_date*, *approver*, *approve_date* 字段
    - 添加 *status* 属性
    - 删除 *uid* 字段

- **TransferCardProcess**
    - 修改 *index* 为 *IntegerField*

- **WeldingCertification**
    - 修改 *weld_method* 为 *IntegerField*

- **WeldingJointProcessAnalysis**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        specification           spec
        ======================= =======================

    - 修改 *weld_position* 为 *IntegerField*
    - 修改 *weld_method_1* 和 *weld_method_2* 为 *IntegerField*
    - 修改 *proc_qual_index* 为 *IntegerField*
    - 删除 *bm_texture_1* 字段
    - 删除 *bm_spec_1* 字段
    - 删除 *bm_texture_2* 字段
    - 删除 *bm_spec_2* 字段
    - 删除 *weld_position* 字段
    - 删除 *weld_method_1* 字段
    - 删除 *weld_method_2* 字段
    - 删除 *weld_method* 方法
    - 删除 *get_weld_certification1* 方法
    - 删除 *get_weld_cert_1* 方法
    - 删除 *get_weld_certification2* 方法
    - 删除 *get_weld_cert_2* 方法

- **WeldingSeam**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        base_metal_1            bm_1
        ----------------------- -----------------------
        base_metal_2            bm_2
        ----------------------- -----------------------
        base_metal_thick_1      bm_thick_1
        ----------------------- -----------------------
        base_metal_thick_2      bm_thick_2
        ----------------------- -----------------------
        weld_material_1         wm_1
        ----------------------- -----------------------
        weld_flux_1             wf_1
        ----------------------- -----------------------
        thick_1                 wt_1
        ----------------------- -----------------------
        size_1                  ws_1
        ----------------------- -----------------------
        flux_weight_1           wf_weight_1
        ----------------------- -----------------------
        weld_material_2         wm_2
        ----------------------- -----------------------
        weld_flux_2             wf_2
        ----------------------- -----------------------
        thick_2                 wt_2
        ----------------------- -----------------------
        size_2                  ws_2
        ----------------------- -----------------------
        flux_weight_2           wf_weight_2
        ----------------------- -----------------------
        weld_joint_detail       analysis
        ======================= =======================

    - 修改 *seam_type* 为 *CharField*
    - 修改 *base_metal_thick_1* 和 *base_metal_thick_2* 为 *FloatField*
    - 修改 *length* 为 *FloatField*
    - 删除 *groove_inspction* 字段
    - 删除 *welded_status_inspection* 字段
    - 删除 *heat_treatment_inspection* 字段
    - 删除 *pressure_test_inspection* 字段

- **WeldingWorkInstruction**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        detail                  analysis
        ======================= =======================

    - 删除 *uid* 字段

- **WeldingWorkInstructionProcess**
    - 修改 *index* 为 *IntegerField*

- **WeldingWorkInstructionExamination**
    - 字段重命名

        ======================= =======================
        改动前                  改动后
        ----------------------- -----------------------
        test_method             surveyor
        ======================= =======================

    - 修改 *index* 为 *IntegerField*

- **ProgrammingBlankingChart**
    - 删除 *name* 字段
    - 删除 *size* 字段
    - 删除 *file_type* 字段

- **ProgrammingBlankingChart**
    - 修改 *layer* 为 *IntegerField*
    - 修改 *weld_method* 为 *IntegerField*
