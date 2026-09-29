.. _biometrics_api:

Biometrics
##########

Overview
********

Biometrics
API
为
biometric
sensors
提供
统一
的
interface
如
fingerprint
scanners、
iris
scanners、
和
face
recognition
modules。
这些
sensors
常见
于
embedded
systems
中
的
secure
authentication、
access
control
devices、
和
IoT
applications。

API
支持
biometric
operations
的
完整
lifecycle
包括
enrollment、
template
management、
和
matching。
Sensors
可以
根据
hardware
capability
将
templates
存储
在
on-device
或
on
host
system。

典型
的
fingerprint
enrollment
process
需要
捕获
同一
手指
的
多
个
samples
来
创建
可靠
的
template。
Matching
process
将
捕获
的
sample
与
存储
的
templates
比较
以
验证
身份。

Configuration
Options
*********************

相关
配置
选项：

* :kconfig:option:`CONFIG_BIOMETRICS`
* :kconfig:option:`CONFIG_BIOMETRICS_INIT_PRIORITY`

API
Reference
*************

.. doxygengroup::
   biometrics_interface
