.. _shields:

Shields
#######

Shields
也
称为
"add
on"
或
"daughter
boards"
附加
到
board
上
以
扩展
其
features
和
services
用于
更
轻松
和
modularized
的
prototyping。
在
Zephyr
中
shield
feature
提供
Zephyr
formatted
的
shield
descriptions
用于
更
轻松
的
与
applications
兼容。

Shield
activation
*****************

通过
向
west
command
添加
匹配
的
``--shield``
arguments
启用
一
个
或
多
个
shields
的
支持：

  .. zephyr-app-commands::
     :app:
     your_app
     :board:
     your_board
     :shield:
     x_nucleo_idb05a1,x_nucleo_iks01a1
     :goals:
     build


或者
可以
在
project
的
CMakeLists.txt
中
默认
设置：

.. code-block:: cmake

   set(SHIELD
   x_nucleo_iks01a1)

.. _shield-interfaces:

Shield
interfaces
*****************

一
个
shield
由
两
个
关键
characteristics
定义：

#. **Physical
   connectors**
   -
   mechanical
   interface
#. **Electrical
   signals**
   -
   每个
   pin
   实际
   做
   什么

Shield
和
board
之间
的
connection
通过
Devicetree
files
发生：
