.. _usb_device_stack_next:

USB device support
##################

Overview
********

USB device 支持由 USB device controller (UDC) drivers
（:ref:`udc_api`）和 USB device stack（:ref:`usbd_api`）组成。
:ref:`udc_api` 为 USB
device controllers 提供通用且 vendor independent 的 interface（且尽管
这些 layers 间有清晰分离（:ref:`udc_api` 的用途为专属服务 Zephyr 的 USB device stack。

Device stack 支持多个 device controllers（意味着
SoC 有多个 controllers 时可同时使用。支持 Full 和
high-speed device controllers。其还支持
在 runtime 向 configuration 注册多个 function 或 class instances（
或稍后更改 configuration。其内置支持若干 USB
classes（并提供实现自定义 USB functions 的 API。

Samples
=======

* :zephyr:code-sample:`usb-hid-keyboard`

* :zephyr:code-sample:`uac2-explicit-feedback`

* :zephyr:code-sample:`uac2-implicit-feedback`

* :zephyr:code-sample:`uvc`

* :zephyr:code-sample:`bluetooth_hci_usb`

* :zephyr:code-sample:`usb-cdc-acm`

* :zephyr:code-sample:`usb-cdc-acm-console`

* :zephyr:code-sample:`usb-mass`

* :zephyr:code-sample:`usb-hid-mouse`

* :zephyr:code-sample:`zperf` 要为 device support 构建 sample（
  设置 configuration overlay file
  ``-DEXTRA_CONF_FILE=overlay-usbd.conf``（devicetree overlay file
  ``-DDTC_OVERLAY_FILE=usbd_cdc_ecm.overlay``（直接或通过 ``west``。

.. _usb_device_next_howto_configure:

How to configure and enable USB device support
**********************************************

对 Zephyr project repository 中的 USB device 支持 samples（有
用于 instantiation、configuration 和 initialization 的
通用 file
:zephyr_file:`samples/subsys/usb/common/sample_usbd_init.c`。以下来自
此 file 的 code
snippets 用作示例。USB samples 中使用的 USB Samples Kconfig options
（以 ``SAMPLE_USBD_`` 为 prefix）有 Zephyr project 特定的默认值
（且 scope 限于 project samples。
以下示例中（须将这些 Kconfig options 和
其他 defaults 替换为适合 application 或 hardware 的值。

USB device stack 需 context structure 管理其 properties 和
runtime data。定义 device context 的首选方式为用
:c:macro:`USBD_DEVICE_DEFINE` macro。这创建给定名称的静态
:c:struct:`usbd_context` variable。可实例化任意数量 contexts。USB controller device 可分配给多个 contexts（
但一次仅一个 context 可被初始化并使用。Context properties
不得由 application 直接访问或操作。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc device instantiation start
   :end-before: doc device instantiation end

USB device 可有 manufacturer、product 和 serial number string
descriptors。要实例化这些 string descriptors（application 应
用相应 :c:macro:`USBD_DESC_MANUFACTURER_DEFINE`、
:c:macro:`USBD_DESC_PRODUCT_DEFINE` 和
:c:macro:`USBD_DESC_SERIAL_NUMBER_DEFINE` macros。String descriptors 还
须用
:c:macro:`USBD_DESC_LANG_DEFINE` macro 单次实例化 language descriptor。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc string instantiation start
   :end-before: doc string instantiation end

String descriptors 须用 :c:func:`usbd_add_descriptor` 在
初始化 USB device 前于 runtime 添加到 device context。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc add string descriptor start
   :end-before: doc add string descriptor end

USB device 须每个支持的 speed 至少一个 configuration instance。
Application 应用 :c:macro:`USBD_CONFIGURATION_DEFINE` 实例化
configuration。稍后（USB device functions 被分配给 configuration。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc configuration instantiation start
   :end-before: doc configuration instantiation end

特定 speed 的每个 configuration instance 须用
:c:func:`usbd_add_configuration` 在 USB device 初始化前于 runtime 添加到 device
context。注意 :c:enumerator:`USBD_SPEED_FS` 和
:c:enumerator:`USBD_SPEED_HS`。第一个 full-speed 或 high-speed
configuration 获得 ``bConfigurationValue`` 1（然后依次向上。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc configuration register start
   :end-before: doc configuration register end


尽管已做很多（此 USB device 无 function。Device
可在不同 speeds 有带不同 function 集合的多个 configurations。Function 或 class 可在
USB device 初始化前用 :c:func:`usbd_register_class` 注册。期望的
configuration 用 :c:enumerator:`USBD_SPEED_FS` 或
:c:enumerator:`USBD_SPEED_HS`（以及 configuration number 指定。对简单情况（
:c:func:`usbd_register_all_classes` 可用于注册所有可用
instances。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc functions register start
   :end-before: doc functions register end

准备中最后一步为用
:c:func:`usbd_init` 初始化 device。此后（device 的 configuration
不可更改。Device 可用 :c:func:`usbd_shutdown` 反初始化（且所有
instances 可复用（但须重复前几步。故
可 shutdown device（注册另一类型 configuration 或
function（并再次初始化。在 USB controller 层（
:c:func:`usbd_init` 仅做检测 VBUS 变更所需的事。
有 controller types 下一步仅在存在 VBUS signal 时可能。

Function 或 class 实现可能需其自己的特定 configuration
steps（应在初始化 USB device 前执行。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc device init start
   :end-before: doc device init end

启用 USB device 的最后一步为 :c:func:`usbd_enable`（此后（
若 USB device 连接到 USB host controller（host 可开始
枚举 device。Application 可用
:c:func:`usbd_disable` 禁用 USB device。

.. literalinclude:: ../../../../../samples/subsys/usb/hid-keyboard/src/main.c
   :language: c
   :dedent:
   :start-after: doc device enable start
   :end-before: doc device enable end

USB Message notifications
=========================

Application 可用 :c:func:`usbd_msg_register_cb` 注册 callback
以从 USB device 支持 subsystem 接收 message notification。
Messages 大多关于通用 device state 变更（以及 USB CDC ACM 实现的若干特定
types。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc device init-and-msg start
   :end-before: doc device init-and-msg end

Helper function :c:func:`usbd_msg_type_string()` 可用于将
:c:enumerator:`usbd_msg_type` 转为 logging 用的 human readable form。

若 controller 支持 VBUS state 变更检测（battery-powered
application 可能想仅在连接到
host 时启用 USB device。通用 application 应用 :c:func:`usbd_can_detect_vbus` 检查
此 capability。

.. literalinclude:: ../../../../../samples/subsys/usb/hid-keyboard/src/main.c
   :language: c
   :dedent:
   :start-after: doc device msg-cb start
   :end-before: doc device msg-cb end

Built-in functions
******************

USB device stack 有内置 USB functions。某些可通过特殊 API 直接在
user application 中使用（如 HID 或 Audio class devices（
而另一些用通用 Zephyr RTOS driver API（如 MSC 和 CDC class
implementations。*Identification string* 标识 class 或 function
instance（``n``）（并用作 :c:func:`usbd_register_class` 的 argument。

+-----------------------------------+-------------------------+-------------------------+
| Class or function                 | User API (if any)       | Identification string   |
+===================================+=========================+=========================+
| USB Audio 2 class                 | :ref:`uac2_device`      | :samp:`uac2_{n}`        |
+-----------------------------------+-------------------------+-------------------------+
| USB CDC ACM class                 | :ref:`uart_api`         | :samp:`cdc_acm_{n}`     |
+-----------------------------------+-------------------------+-------------------------+
| USB CDC ECM class                 | Ethernet device         | :samp:`cdc_ecm_{n}`     |
+-----------------------------------+-------------------------+-------------------------+
| USB Mass Storage Class (MSC)      | :ref:`usbd_msc_device`  | :samp:`msc_{n}`         |
+-----------------------------------+-------------------------+-------------------------+
| USB Human Interface Devices (HID) | :ref:`usbd_hid_device`  | :samp:`hid_{n}`         |
+-----------------------------------+-------------------------+-------------------------+
| Bluetooth HCI USB transport layer | :ref:`bt_hci_raw`       | :samp:`bt_hci_{n}`      |
+-----------------------------------+-------------------------+-------------------------+
| USB Video Class (UVC)             | Video device            | :samp:`uvc_{n}`         |
+-----------------------------------+-------------------------+-------------------------+
