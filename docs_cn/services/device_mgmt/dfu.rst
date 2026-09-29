.. _dfu:

Device
Firmware
Upgrade
#######################

Overview
********

Device
Firmware
Upgrade
subsystem
provide
necessary
的
frameworks
用于
在
run
time
upgrade
Zephyr
based
的
application
的
image。
它
当前
consist
of
两
个
不同
的
modules：

*
:zephyr_file:`subsys/dfu/boot/`：
与
bootloaders
的
Interface
code
*
:zephyr_file:`subsys/dfu/img_util/`：
Image
management
code

DFU
subsystem
deal
with
image
management
但
不
deal
with
将
image
send
到
target
device
所需
的
transport
或
management
protocols
本身。
关于
这些
protocols
和
frameworks
的
information
请参考
:ref:`device_mgmt`
section。

.. _flash_img_api:

Flash
Image
===========

Flash
image
API
作为
Device
Firmware
Upgrade
（DFU）
subsystem
的
一
part
在
Flash
Stream
上面
provide
一
个
abstraction
用于
简化
将
firmware
image
chunks
write
到
flash。

API
Reference
-------------

.. doxygengroup::
   flash_img_api

.. _mcuboot_api:

MCUBoot
API
===========

MCUboot
API
被
provided
用于
get
version
information
和
boot
status
of
