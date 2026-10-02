.. _usb_hid_common:

人机接口设备（HID）
#############################

可在 USB 支持之外使用的通用 USB HID 部分，定义在头文件 :zephyr_file:`include/zephyr/usb/class/hid.h` 中。

HID 类型参考
*******************

.. doxygengroup:: usb_hid_definitions

HID 项目参考
*******************

.. doxygengroup:: usb_hid_items

HID 鼠标和键盘报告描述符
*****************************************

预定义的鼠标和键盘报告描述符可用于 HID 设备实现，或仅作为示例使用。

.. doxygengroup:: usb_hid_mk_report_desc
