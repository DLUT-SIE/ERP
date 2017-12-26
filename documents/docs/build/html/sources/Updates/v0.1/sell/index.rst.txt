sell模块
===============================
.. toctree::
   :maxdepth: 2

- 模块重命名为 **Distribution**
- 模型 **BidFile** 重命名为 **BiddingDocument**
- **BiddingDocument**
    - 字段重命名

        =============== ==========
        改动前           改动后
        --------------- ----------
        file_obj        path
        --------------- ----------
        file_size       size
        --------------- ----------
        upload_date     upload_dt
        --------------- ----------
        is_approval     approved
        =============== ==========

    - 添加 *product* 字段, 指示关联产品
    - 添加 *src*, *dst* 字段, 指示来源部门以及接收部门
    - 修改 *upload_dt* 为 *auto_now_add*
    - 删除 *recv_group*, *file_type* 字段

- **Product**
    - 字段重命名

        =============== ==========
        改动前           改动后
        --------------- ----------
        is_approval     approved
        --------------- ----------
        is_finish       terminated
        --------------- ----------
        upload_date     upload_dt
        --------------- ----------
        is_approval     approved
        =============== ==========

    - 删除 *manufacture_file_down*, *manufacture_file_up* 等字段, 转而使用外键关系
