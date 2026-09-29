.. _arm_scmi:

ARM
System
Control
and
Management
Interface
###########################################

Overview
********

System
Control
and
Management
Interface
（SCMI）
是
ARM
开发
的
一
个
specification，
它
描述
一
组
OS-agnostic
的
software
interfaces
用
于
执行
system
management
（例如：
clock
control、
pinctrl、
等等...）。
在
这
个
上下文
中，
Zephyr
充当
一
个
SCMI
agent。

.. note::

   Zephyr
   的
   实现
   可能
   只
   包含
   本
   文档
   中
   提到
   的
   功能
   或
   功能
   的
   子集。

Standard
protocols
******************

支持
的
**standard**
[#]_
protocols
集合
在
下面
总结：

.. list-table::
   :align:
   center

   * - ID
     - Name
     - Supported
       version

   * - 0x10
     - Base
       protocol
     - 2.1

   * - 0x11
     - Power
       domain
       management
       protocol
     - 3.1

   * - 0x12
     - System
       power
       management
       protocol
