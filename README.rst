TZ-ERP
==========
.. image:: https://readthedocs.org/projects/erp/badge/?version=latest
    :target: http://erp.readthedocs.io/?badge=latest
    :alt: Documentation Status
.. image:: https://travis-ci.org/DLUT-SIE/ERP.svg?branch=dev
    :target: https://travis-ci.org/DLUT-SIE/ERP
.. image:: https://coveralls.io/repos/github/DLUT-SIE/ERP/badge.svg?branch=master
    :target: https://coveralls.io/github/DLUT-SIE/ERP?branch=master

安装
----

1. 安装 Python 3.6+
2. pip install -r requirements.txt


开发说明
--------

1. 分支 **master** 被保护, 用于发布最新稳定版本代码
2. 分支 **dev** 被保护, 代表最新开发进度, 该分支请及时同步到本地
3. 个人开发单独创建分支, 请保证从最新的 **dev** 分支创建 `git checkout -b branch-name`
4. 开发完成后, 运行 `coverage run manange.py test -v 2` 进行单元测试, 如无测试错误运行 `coverage report` 查看代码覆盖度
5. 通过单元测试以及覆盖度检测的代码请在Github上发出 **Pull Request**, 向 **dev** 分支进行合并
6. 发起 **PR** 以后集成的 **Travis CI** 和 **Coveralls** 会自动执行单元测试以及覆盖度检测
7. 请在通过自动检测以后选择 **Reviewer** 进行 **Code Review**, 选择检测人为同组人员及管理员
8. 通过所有检测以后联系管理员进行代码合并
9. 代码合并仓库将在远端删除该分支, 请及时删除本地对应分支
10. 分支命名请尽量采用 **feature-xxx**, **fix-xx** 等命名方式


目录结构
---------
    .. code-block:: none

        .
        ├── Core  # 核心
        │   ├── api
        │   ├── migrations
        │   ├── models
        │   ├── serializers
        │   ├── templates
        │   ├── tests
        │   ├── utils
        │   └── views
        ├── Distribution  # 经销
        │   ├── api
        │   ├── migrations
        │   └── serializers
        ├── ERP  # 项目配置文件
        ├── Inventory  # 库存
        │   ├── migrations
        │   └── models
        ├── Messaging  # 消息
        │   ├── migrations
        │   └── tests
        ├── Process  # 工艺
        │   ├── migrations
        │   └── models
        ├── Procurement  # 采购
        │   ├── migrations
        │   └── models
        ├── Production  # 生产
        │   └── migrations
        └── documents  # 文档
            ├── build
            └── source
