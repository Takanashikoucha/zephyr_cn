.. _udc_api:

USB 设备控制器（UDC）驱动 API
######################################

USB 设备控制器驱动 API 描述在 :zephyr_file:`include/zephyr/drivers/usb/udc.h` 中，称为 ``UDC 驱动`` API。

UDC 驱动 API 是不稳定的，可能会在不通知的情况下变更。它是 :ref:`usb_dc_api` 的替代方案。如果您希望将现有驱动移植到 UDC 驱动 API，或添加新驱动，请使用 :zephyr_file:`drivers/usb/udc/udc_skeleton.c` 作为起点。

API 参考
*************

.. doxygengroup:: udc_api

.. doxygengroup:: usb_buf
