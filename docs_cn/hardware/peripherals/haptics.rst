.. _haptics_api:

Haptics
#######

Overview
********

Haptics
API
允许
控制
haptic
driver
devices
用于
执行
haptic
feedback
events。

在
haptic
feedback
event
期间
haptic
device
向
actuator
驱动
一
个
signal。
Haptic
event
signal
的
source
根据
haptic
device
的
capability
变化。

Haptic
signal
sources
的
一些
示例
是
analog
signals、
preprogrammed
（ROM）
wavetables、
synthesized
（RAM）
wavetables、
和
digital
audio
streams。

此外，
haptic
driver
devices
通常
提供
controls
调整
和
tuning
drive
signal
以
满足
它们
各自
actuators
的
electrical
requirements。

API
Reference
*************

.. doxygengroup::
   haptics_interface
