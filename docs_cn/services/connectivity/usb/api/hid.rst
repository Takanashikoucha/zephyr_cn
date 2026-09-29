.. _usb_hid_common:

Human
Interface
Devices
（HID）
#############################

Common
的
USB
HID
part
它
可
被
used
在
USB
support
之外
它
defined
在
header
file
:zephyr_file:`include/zephyr/usb/class/hid.h`
中。

HID
types
reference
*******************

.. doxygengroup::
   usb_hid_definitions

HID
items
reference
*******************

.. doxygengroup::
   usb_hid_items

HID
Mouse
and
Keyboard
report
descriptors
*****************************************

Pre
defined
的
Mouse
和
Keyboard
report
descriptors
可以
被
HID
device
implementation
used
或
简单
作为
examples。

.. doxygengroup::
   usb_hid_mk_report_desc
