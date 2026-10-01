.. _udc_api:

USB device controller (UDC) driver API
######################################

USB device controller driver API 描述在
:zephyr_file:`include/zephyr/drivers/usb/udc.h` 中（称为
``UDC driver`` API。

UDC driver API 不稳定（且可能不经通知变更。
其为 :ref:`usb_dc_api` 的替代。若要移植现有
driver 到 UDC driver API（或添加新 driver（请用
:zephyr_file:`drivers/usb/udc/udc_skeleton.c` 作为起点。

API reference
*************

.. doxygengroup:: udc_api

.. doxygengroup:: usb_buf
