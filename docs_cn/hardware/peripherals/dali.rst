.. _dali_api:

DALI
####

DALI
是
digital
addressable
lighting
interface，
专业
lighting
solutions
的
communication
standard。
这
个
API
是
unstable
的
并
可能
改变。

Basic
Operation
***************

DALI
standard
使用
基于
通过
bus
system
交换
frames
的
communication
model。
一
个
frame
是
manchester
encoded
data，
以
stop
condition
终止。
DALI
standard
要求
transmitter
和
receiver
的
特定
行为。

Configuration
Options
*********************

相关
配置
选项：

* :kconfig:option:`CONFIG_DALI`
* :kconfig:option:`CONFIG_DALI_PWM`


API
Reference
*************

.. doxygengroup::
   dali_interface
