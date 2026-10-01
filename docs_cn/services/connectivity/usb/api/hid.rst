.. _usb_hid_common:

Human Interface Devices (HID)
#############################

可在 USB support 外使用的通用 USB HID 部分（定义在
header file :zephyr_file:`include/zephyr/usb/class/hid.h`。

HID types reference
*******************

.. doxygengroup:: usb_hid_definitions

HID items reference
*******************

.. doxygengroup:: usb_hid_items

HID Mouse and Keyboard report descriptors
*****************************************

预定义的 Mouse 和 Keyboard report descriptors 可由
HID device implementation 使用（或仅作示例。

.. doxygengroup:: usb_hid_mk_report_desc
