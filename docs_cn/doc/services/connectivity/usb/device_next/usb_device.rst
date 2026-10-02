.. _usb_device_stack_next:

USB 设备支持
##################

概述
********

USB 设备支持由 USB 设备控制器（UDC）驱动
、:ref:`udc_api` 以及 USB 设备栈 :ref:`usbd_api` 组成。
:ref:`udc_api` 为 USB 设备控制器提供通用且与厂商无关的接口；
尽管这些层之间有明确的划分，:ref:`udc_api` 的用途是
专门服务于 Zephyr 的 USB 设备栈。

设备栈支持多个设备控制器，也就是说，如果
SoC 拥有多个控制器，它们可以同时使用。支持全速
和高速设备控制器。它还支持在运行时向配置注册多个
功能或类实例，或稍后更改配置。它内置对若干 USB
类的支持，并提供用于实现自定义 USB 功能的 API。

示例
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

* :zephyr:code-sample:`zperf` 要为设备支持构建该示例，
  请设置配置 overlay 文件
  ``-DEXTRA_CONF_FILE=overlay-usbd.conf`` 和设备树 overlay 文件
  ``-DDTC_OVERLAY_FILE=usbd_cdc_ecm.overlay``，可直接设置或通过 ``west`` 设置。

.. _usb_device_next_howto_configure:

如何配置并启用 USB 设备支持
**********************************************

对于 Zephyr 项目仓库中的 USB 设备支持示例，我们有一个
用于实例化、配置和初始化的公共文件
:zephyr_file:`samples/subsys/usb/common/sample_usbd_init.c`。下面从该文件
摘录的代码片段用作示例。USB 示例中使用的、以 ``SAMPLE_USBD_``
为前缀的 Kconfig 选项具有 Zephyr 项目特有的默认值，
其作用范围仅限于项目示例。
在下述示例中，你需要将这些 Kconfig 选项和其他
默认值替换为适合你的应用程序或硬件的值。

USB 设备栈需要一个上下文结构体来管理其属性和
运行时数据。定义设备上下文的首选方式是使用
:c:macro:`USBD_DEVICE_DEFINE` 宏。它会创建一个具有指定名称的
静态 :c:struct:`usbd_context` 变量。可以实例化任意数量的上下文。
一个 USB 控制器设备可以分配给多个上下文，
但同一时间只能有一个上下文被初始化并使用。
应用程序不得直接访问或操作上下文属性。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc device instantiation start
   :end-before: doc device instantiation end

USB 设备可能具有厂商、产品和序列号字符串
描述符。要实例化这些字符串描述符，应用程序应
使用相应的 :c:macro:`USBD_DESC_MANUFACTURER_DEFINE`、
:c:macro:`USBD_DESC_PRODUCT_DEFINE` 和
:c:macro:`USBD_DESC_SERIAL_NUMBER_DEFINE` 宏。字符串描述符
还需要使用 :c:macro:`USBD_DESC_LANG_DEFINE` 宏
对语言描述符进行单次实例化。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc string instantiation start
   :end-before: doc string instantiation end

字符串描述符必须在初始化 USB 设备之前
使用 :c:func:`usbd_add_descriptor` 添加到设备上下文。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc add string descriptor start
   :end-before: doc add string descriptor end

USB 设备至少需要为每种支持的速度提供一个配置实例。
应用程序应使用 :c:macro:`USBD_CONFIGURATION_DEFINE` 实例化
一个配置。之后，USB 设备功能被分配到配置中。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc configuration instantiation start
   :end-before: doc configuration instantiation end

每个特定速度的配置实例必须在 USB 设备初始化之前
使用 :c:func:`usbd_add_configuration` 添加到设备上下文。
注意 :c:enumerator:`USBD_SPEED_FS` 和
:c:enumerator:`USBD_SPEED_HS`。第一个全速或高速
配置的 ``bConfigurationValue`` 为 1，之后依次递增。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc configuration register start
   :end-before: doc configuration register end


尽管我们已经做了很多工作，但这个 USB 设备还没有任何功能。
一个设备可以在不同速度下拥有多个配置，
每个配置包含不同的功能集合。在 USB 设备
初始化之前，可以使用 :c:func:`usbd_register_class`
将功能或类注册到 USB 设备上。目标
配置通过 :c:enumerator:`USBD_SPEED_FS` 或
:c:enumerator:`USBD_SPEED_HS` 以及配置编号指定。对于简单场景，
可以使用 :c:func:`usbd_register_all_classes`
注册所有可用实例。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc functions register start
   :end-before: doc functions register end

准备阶段的最后一步是使用
:c:func:`usbd_init` 初始化设备。此后，
设备的配置将无法更改。设备可以使用 :c:func:`usbd_shutdown`
反初始化，所有实例可以重复使用，但必须
重复执行前面的步骤。因此，可以关闭设备、
注册另一类型的配置或功能，然后再次初始化。
在 USB 控制器层面，
:c:func:`usbd_init` 只执行检测 VBUS 变化所必需的步骤。
有些类型的控制器，只有在存在 VBUS 信号时
才能执行下一步。

功能或类的实现可能需要其自身的特定配置
步骤，这些步骤应在初始化 USB 设备之前完成。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc device init start
   :end-before: doc device init end

启用 USB 设备的最后一步是 :c:func:`usbd_enable`，
之后，如果 USB 设备已连接到 USB 主机控制器，
主机即可开始枚举该设备。应用程序可以使用
:c:func:`usbd_disable` 禁用 USB 设备。

.. literalinclude:: ../../../../../samples/subsys/usb/hid-keyboard/src/main.c
   :language: c
   :dedent:
   :start-after: doc device enable start
   :end-before: doc device enable end

USB 消息通知
=========================

应用程序可以使用 :c:func:`usbd_msg_register_cb` 注册回调，
以接收来自 USB 设备支持子系统的消息通知。
这些消息大多关于常见的设备状态变化，
以及来自 USB CDC ACM 实现的少数特定类型。

.. literalinclude:: ../../../../../samples/subsys/usb/common/sample_usbd_init.c
   :language: c
   :dedent:
   :start-after: doc device init-and-msg start
   :end-before: doc device init-and-msg end

辅助函数 :c:func:`usbd_msg_type_string()` 可用于将
:c:enumerator:`usbd_msg_type` 转换为人类可读形式，便于日志输出。

如果控制器支持 VBUS 状态变化检测，
电池供电的应用程序可能希望在连接到
主机时才启用 USB 设备。通用应用程序应使用
:c:func:`usbd_can_detect_vbus` 检查
该能力。

.. literalinclude:: ../../../../../samples/subsys/usb/hid-keyboard/src/main.c
   :language: c
   :dedent:
   :start-after: doc device msg-cb start
   :end-before: doc device msg-cb end

内置功能
******************

USB 设备栈内置了若干 USB 功能。一些可以通过专用 API
直接用于用户应用程序，例如 HID 或 Audio 类设备，
另一些则使用通用的 Zephyr RTOS 驱动 API，
例如 MSC 和 CDC 类实现。*Identification string*
标识一个类或功能实例（``n``），
并用作 :c:func:`usbd_register_class` 的参数。

+-----------------------------------+-------------------------+-------------------------+
| 类或功能                           | 用户 API（如有）        | Identification string   |
+===================================+=========================+=========================+
| USB Audio 2 类                    | :ref:`uac2_device`      | :samp:`uac2_{n}`        |
+-----------------------------------+-------------------------+-------------------------+
| USB CDC ACM 类                    | :ref:`uart_api`         | :samp:`cdc_acm_{n}`     |
+-----------------------------------+-------------------------+-------------------------+
| USB CDC ECM 类                    | 以太网设备（Ethernet device） | :samp:`cdc_ecm_{n}`     |
+-----------------------------------+-------------------------+-------------------------+
| USB 大容量存储类（MSC）           | :ref:`usbd_msc_device`  | :samp:`msc_{n}`         |
+-----------------------------------+-------------------------+-------------------------+
| USB 人机接口设备（HID）          | :ref:`usbd_hid_device`  | :samp:`hid_{n}`         |
+-----------------------------------+-------------------------+-------------------------+
| 蓝牙 HCI USB 传输层              | :ref:`bt_hci_raw`       | :samp:`bt_hci_{n}`      |
+-----------------------------------+-------------------------+-------------------------+
| USB 视频类（UVC）                | 视频设备（Video device）  | :samp:`uvc_{n}`         |
+-----------------------------------+-------------------------+-------------------------+
