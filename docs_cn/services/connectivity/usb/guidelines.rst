.. _usb_guidelines:

Common guidelines for USB tests and samples
###########################################

Overview
********

通常（所有 USB samples 和 tests 为 platform agnostic（且不应需
platform-specific overlay。尽管 tree 中可能已有例外（
目标为避免 platform-specific overlays。USB sample 或
USB test 无义务支持特定 platform。

Board configuration
*******************

Default USB device and host controller
======================================

USB 支持用 ``zephyr_udc0`` node label 分配默认 USB device controller
（用 ``zephyr_uhc0`` node label 分配默认 USB host controller。取决于
board 支持什么（其须分配这些 node labels 以
能执行 tree 中的 samples 和
tests。

Supported features for the board metadata
=========================================

board metadata file 仅有 Twister 用于选取 sample 或 test 的两个
supported features。对支持 device
mode 的 USB controller 的 board（feature 为 ``usbd``。对支持 host mode 的 USB controller 的 board（
feature 为 ``usbh``。

更多细节参见 :ref:`twister_board_configuration`。

Deprecated features
-------------------

Feature ``usb_device`` 不应再使用。此 feature 属于 legacy
USB device stack（其已 deprecated 且将被移除。

Tests Twister configuration
***************************

USB tests 可能需额外 hardware 或 software setup。这些 tests 应使用
下表描述的 :ref:`fixtures <twister_fixtures>`。

+-----------------------------+-------------------------------------------------------------+
| Fixture                     | Use case                                                    |
+=============================+=============================================================+
| ``usb_host_connected``      | The test implements USB device functionality, and requires  |
|                             | a USB host to be connected to the board under test.         |
+-----------------------------+-------------------------------------------------------------+
| ``usb_device_connected``    | The test implements USB host functionality, and requires    |
|                             | a USB device to be connected to the board under test.       |
+-----------------------------+-------------------------------------------------------------+
