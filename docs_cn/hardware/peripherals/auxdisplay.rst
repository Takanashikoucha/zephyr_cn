.. _auxdisplay_api:

Auxiliary
Display
（auxdisplay）
##############################

Overview
********

Auxiliary
Displays
是
text
based
的
displays
它们
有
简单
的
interfaces
用
于
显示
textual、
numeric
或
alphanumeric
data，
与
:ref:`display_api`
不同，
auxiliary
displays
不
支持
向
displays
输出
custom
graphical
output
（并且
大多数
是
monochrome），
支持
的
最
高级
的
custom
功能
是
生成
custom
characters。
这些
便宜
的
displays
常见
于
各种
配置
和
尺寸，
常见
的
display
尺寸
是
16
characters
×
2
lines。

这
个
API
是
unstable
的
并
可能
改变。

Configuration
Options
*********************

相关
配置
选项：

* :kconfig:option:`CONFIG_AUXDISPLAY`
* :kconfig:option:`CONFIG_AUXDISPLAY_INIT_PRIORITY`

API
Reference
*************

.. doxygengroup::
   auxdisplay_interface
