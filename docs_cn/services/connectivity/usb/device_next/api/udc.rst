.. _udc_api:

USB
device
controller
（UDC）
driver
API
######################################

USB
device
controller
driver
API
在
:zephyr_file:`include/zephyr/drivers/usb/udc.h`
中
described
并
被
referred
to
作为
``UDC
driver``
API。

UDC
driver
API
是
unstable
的
并
subject
to
change
without
notice。
它
是
:ref:`usb_dc_api`
的
replacement。
如果
你
想
port
现有
的
driver
到
UDC
driver
API
或
add
新
的
driver
请
use
:zephyr_file:`drivers/usb/udc/udc_skeleton.c`
作为
starting
point。

API
reference
*************

.. doxygengroup::
   udc_api

.. doxygengroup::
   usb_buf
