.. _usbd_vid_pid:

USB Vendor and Product identifiers
**********************************

Zephyr project 的 USB Vendor ID 为 ``0x2FE3``。当 vendor 将 Zephyr USB device
支持集成到其自己的 product 时（不得
使用 Zephyr USB Vendor ID。

每个 USB :zephyr:code-sample-category:`sample<usb>` 有其自己的唯一 Product ID。
USB maintainer（若已指派）（否则 Zephyr Technical
Steering Committee（可基于有充分动机且
有记录的 requests 分配其他 USB Product IDs。

当前使用的 Product IDs 如下：

+----------------------------------------------------+--------+
| Sample                                             | PID    |
+====================================================+========+
| :zephyr:code-sample:`usb-cdc-acm`                  | 0x0001 |
+----------------------------------------------------+--------+
| Reserved (previously: usb-cdc-acm-composite)       | 0x0002 |
+----------------------------------------------------+--------+
| Reserved (previously: usb-hid-cdc)                 | 0x0003 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`usb-cdc-acm-console`          | 0x0004 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`usb-dfu` (Run-Time)           | 0x0005 |
+----------------------------------------------------+--------+
| Reserved (previously: usb-hid)                     | 0x0006 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`usb-hid-mouse`                | 0x0007 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`usb-mass`                     | 0x0008 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`testusb-app`                  | 0x0009 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`webusb`                       | 0x000A |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`bluetooth_hci_usb`            | 0x000B |
+----------------------------------------------------+--------+
| Reserved (previously: bluetooth_hci_usb_h4)        | 0x000C |
+----------------------------------------------------+--------+
| Reserved (previously: wpan-usb)                    | 0x000D |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`uac2-explicit-feedback`       | 0x000E |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`uac2-implicit-feedback`       | 0x000F |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`uvc`                          | 0x0011 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`fido2`                        | 0x0012 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`i2c-tiny-usb`                 | 0x0013 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`usb-dfu` (DFU Mode)           | 0xFFFF |
+----------------------------------------------------+--------+
