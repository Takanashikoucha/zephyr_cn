.. _west-config:

配置
#############

本
页
记录
west
的
配置
文件
系统、
``west
config``
命令
和
内置
命令
使用
的
配置
选项。
对
``west.configuration``
模块
的
API
文档，
参考
:ref:`west-apis-configuration`。

West
配置
文件
------------------------

West
的
配置
文件
语法
是
INI-like；
这里
是
一
个
示例
文件：

.. code-block:: ini

   [manifest]
   path
   =
   zephyr

   [zephyr]
   base
   =
   zephyr

上面，
``manifest``
section
有
选项
``path``
设置
为
``zephyr``。
说
同一
件事
的
另一
种
方式
是
在这
个
文件
中
``manifest.path``
是
``zephyr``。

有
三
种
类型
的
配置
文件：

1. **System**：
   这
   个
   文件
   中
   的
   设置
   影响
   west
   的
   行为
   对
   登录
   到
   电脑
   的
   每个
   用户。
   其
   位置
   取决于
   平台：

   - Linux:
     :file:`/etc/westconfig`
   - macOS:
     :file:`/usr/local/etc/westconfig`
   - Windows:
     :file:`%PROGRAMDATA%\\west\\config`

2. **Global**
   （per
   user）：
   这
   个
   文件
   中
   的
   设置
   影响
   west
   在
   电脑
   上
   被
   特定
   用户
   运行
   时
   如何
   行为。

   - All
     platforms:
     默认
     是
     用户
     home
     目录
     中
     的
     :file:`.westconfig`。
