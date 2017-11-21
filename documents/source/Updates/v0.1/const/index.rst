const模块
===============================
.. toctree::
   :maxdepth: 2

- 模块重命名为 **Core**
- 添加模型 **UserInfo**
- 添加模型 **Department**
- 移出 **BidFormStatus**, **OrderFormStatus**, 至 **Procurement(原purchasing)** 模块
- 删除 **ImplementClassChoices**, **InventoryType** 模型
- **WorkOrder**
    - 字段重命名

        =============== ==========
        改动前           改动后
        --------------- ----------
        index           uid
        --------------- ----------
        client_name     client
        --------------- ----------
        project_name    project
        --------------- ----------
        product_name    product
        --------------- ----------
        is_finish       finished
        =============== ==========

    - *count* 类型更改为 *IntegerField*

- **SubWorkOrder**
    - 字段重命名

        =============== ===========
        改动前           改动后
        --------------- -----------
        order           work_order
        --------------- -----------
        is_finish       finished
        =============== ===========

    - *index* 类型更改为 *IntegerField*


- **Material**
    - 字段重命名

        =============== ===========
        改动前           改动后
        --------------- -----------
        order           work_order
        --------------- -----------
        categories      category
        --------------- -----------
        is_finish       finished
        =============== ===========

    - *category* 类型更改为 *IntegerField*
