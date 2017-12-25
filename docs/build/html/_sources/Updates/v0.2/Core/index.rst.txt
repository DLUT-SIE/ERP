核心模块
===============================
- 移出 **Material** 和 **Materiel** 至 **Process** 模块
- **WorkOrder**
    - 修改 *product* 字段为 *ForeignKey*
    - 删除 *suffix* 方法
    - 删除 *getSellType* 方法


- **SubWorkOrder**
    - 删除 *name* 字段


- **Department**
    - 添加 *group* 字段, 与Django的Group对象进行连接
    - 添加 *superior* 字段, 指示上级部门
    - 删除 *name* 字段
