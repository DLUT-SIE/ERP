.. Coding_guidelines:

代码规范
============

基本要求
------------
- 遵循 **PEP8** 代码规范, 代码通过 **flake8** 检测
- 采用 **4空格** 缩进
- 导入(`import`, `from foo import bar`) 按照 **Python内置模块(一类)**, **Django模块(二类)**, **第三方模块(三类)**, **本系统其他模块(四类)**, **本模块(四类)** 顺序进行导入, 以一个空行分隔不同类型模块, `import` 优先于 `from foo import bar`, 示例:
    .. code-block:: python
    
        import time
        from collections import defaultdict
    
        import django
        from django import utils
    
        import guardian
    
        from Core import views
- 使用带有完整模块名的导入, 不使用类似 `from . import x` 等使用一个或两个点指示路径的导入方式


命名要求
-----------
- 类命名采用 **帕斯卡命名法** ( `class FooBar` ), 单词首字母大写
- 函数、变量命名采用 **下划线命名法** ( `def hello_world()` ), 均采用小写
- 有意义的变量命名


文档与测试要求
--------------
- 编写必要的文档对类, 方法, 函数等进行说明, 文档语言使用 `ReStructuredText` , 使用参见 `A ReStructuredText Primer`_ , 文档风格使用 `Numpy` 风格， 参见 `Numpy风格1`_ , `Numpy风格2`_
- 编写完整的测试用例对代码进行测试, 测试采用单元测试方式, 参见 `Testing a Django web application`_ , `Testing in Django (Part 1)`_
- 测试内容: **Model**, **Form**, **View**, **Util**, **覆盖度**

.. _Testing a Django web application : https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
.. _Testing in Django (Part 1) : https://realpython.com/blog/python/testing-in-django-part-1-best-practices-and-examples/
.. _Numpy风格1 : http://www.sphinx-doc.org/en/stable/ext/napoleon.html
.. _Numpy风格2 : https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _A ReStructuredText Primer : http://docutils.sourceforge.net/docs/user/rst/quickstart.html
