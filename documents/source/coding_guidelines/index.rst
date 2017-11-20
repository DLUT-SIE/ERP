.. coding_guidelines:

代码规范
============

- 遵循 **PEP8** 代码规范, 代码通过 **flake8** 检测
- 采用 **4空格** 缩进
- 有意义的变量命名
- 类命名采用 **帕斯卡命名法** (`class FooBar`)
- 函数、变量命名采用 **下划线命名法** (`def hello_world()`)
- 导入(`import`, `from foo import bar`) 按照 **Python内置模块(一类)**, **Django模块(二类)**, **第三方模块(三类)**, **本系统其他模块(四类)**, **本模块(四类)** 顺序进行导入, 以一个空行分隔不同类型模块, `import` 优先于 `from foo import bar`, 示例:
    .. code-block:: python
    
        import time
        from collections import defaultdict
    
        import django
        from django import utils
    
        import guardian
    
        from Core import views

- 
