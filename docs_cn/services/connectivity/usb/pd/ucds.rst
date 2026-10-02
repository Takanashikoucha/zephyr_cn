.. _usbc_api:

USB-C 设备栈
##################

USB-C 设备栈是 Type-C 端口控制器（TCPC）与客户应用之间的硬件无关接口。它是
Google ChromeOS Type-C 端口管理器（TCPM）栈的移植版本。
它提供以下功能：

* 使用 Type-C 端口控制器驱动程序提供的 API 与
  Type-C 端口控制器交互。
* 提供供客户应用使用的编程接口。
  这些 API 在
  :zephyr_file:`include/zephyr/usb_c/usbc.h` 中有描述

配置选项
**********************************************************

USB-C 设备栈支持实现仅 Sink、仅 Source
和双角色电源（DRP）设备。

- :kconfig:option:`CONFIG_USBC_CSM_SINK_ONLY`：Sink USB-C 连接状态机
- :kconfig:option:`CONFIG_USBC_CSM_SOURCE_ONLY`：Source USBC 连接状态机
- :kconfig:option:`CONFIG_USBC_CSM_DRP`：双角色电源（DRP）USB-C 连接状态机

不同用途的 :zephyr:code-sample-category:`示例列表<usbc>`。

实现 Sink Type-C 和 USB-C 电源传输（Power Delivery）设备
**********************************************************

USB-C 设备的配置在栈层和设备树（devicetree）中完成。

需要定义以下设备树节点、结构和回调：

* 设备树中引用 TCPC 的 usb-c-connector 节点
* 设备树中引用 VBUS 测量设备的 vbus 节点
* 封装应用特定数据的用户自定义结构
* 策略回调

例如，对于示例 USB-C Sink 应用：

每个物理 Type-C 端口在设备树中由一个 usb-c-connector
兼容（compatible）节点表示：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/boards/b_g474e_dpow1.overlay
   :language: dts
   :start-after: usbc.rst usbc-port start
   :end-before: usbc.rst usbc-port end
   :linenos:

VBUS 由设备树中一个
usb-c-vbus-adc 兼容节点所引用的设备来测量：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/boards/b_g474e_dpow1.overlay
   :language: dts
   :start-after: usbc.rst vbus-voltage-divider-adc start
   :end-before: usbc.rst vbus-voltage-divider-adc end
   :linenos:


用户自定义结构被定义后向子系统注册，
并可通过 API 从回调中访问：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst port data object start
   :end-before: usbc.rst port data object end
   :linenos:

这些回调供子系统设置或获取应用特定数据：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst callbacks start
   :end-before: usbc.rst callbacks end
   :linenos:

该回调供子系统查询某个操作是否可以执行：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst check start
   :end-before: usbc.rst check end
   :linenos:

该回调供子系统向应用通知事件：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst notify start
   :end-before: usbc.rst notify end
   :linenos:

注册回调：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst register start
   :end-before: usbc.rst register end
   :linenos:

注册用户自定义结构：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst user data start
   :end-before: usbc.rst user data end
   :linenos:

启动 USB-C 子系统：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst usbc start
   :end-before: usbc.rst usbc end
   :linenos:

实现 Source Type-C 和 USB-C 电源传输（Power Delivery）设备
************************************************************

USB-C 设备的配置在栈层和设备树（devicetree）中完成。

定义以下设备树节点、结构和回调：

* 设备树中引用 TCPC 的 ``usb-c-connector`` 节点
* 设备树中引用 VBUS 测量设备的 ``vbus`` 节点
* 用于 VBUS 和 VCONN 电源控制的设备树 ``pwrctrl`` 节点
* 封装应用特定数据的用户自定义结构
* 策略回调

例如，对于示例 USB-C Source 应用：

每个物理 Type-C 端口在设备树中由一个 ``usb-c-connector``
兼容节点表示：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/boards/stm32g081b_eval.overlay
   :language: dts
   :start-after: usbc.rst usbc-port start
   :end-before: usbc.rst usbc-port end
   :linenos:

VBUS 由设备树中一个
``usb-c-vbus-adc`` 兼容节点所引用的设备来测量：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/boards/stm32g081b_eval.overlay
   :language: dts
   :start-after: usbc.rst vbus-voltage-divider-adc start
   :end-before: usbc.rst vbus-voltage-divider-adc end
   :linenos:

VBUS 和 VCONN 的电源控制可以由设备树中
``zephyr,usb-c-pwrctrl`` 兼容节点所引用的设备来管理：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/boards/stm32g081b_eval.overlay
   :language: dts
   :start-after: usbc.rst pwrctrl start
   :end-before: usbc.rst pwrctrl end
   :linenos:

用户自定义结构被定义后向子系统注册，
并可通过 API 从回调中访问：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst port data object start
   :end-before: usbc.rst port data object end
   :linenos:

这些回调供子系统设置或获取应用特定数据：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst callbacks start
   :end-before: usbc.rst callbacks end
   :linenos:

该回调供子系统查询某个操作是否可以执行：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst check start
   :end-before: usbc.rst check end
   :linenos:

该回调供子系统向应用通知事件：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst notify start
   :end-before: usbc.rst notify end
   :linenos:

注册回调：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst register start
   :end-before: usbc.rst register end
   :linenos:

注册用户自定义结构：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst user data start
   :end-before: usbc.rst user data end
   :linenos:

启动 USB-C 子系统：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst usbc start
   :end-before: usbc.rst usbc end
   :linenos:

实现双角色电源（DRP）USB-C 设备
**************************************************

DRP 设备可以既作为 Source 又作为 Sink 运行，自动与端口对端协商
合适的角色。在未连接时，设备在 Source（Rp）和 Sink（Rd）CC 线广播之间
切换，以检测并连接任意类型的对端。一旦检测到连接，设备进入
相应的已连接状态（Attached.SRC 或 Attached.SNK），并启动
相应的策略引擎状态机（PE_SRC 或 PE_SNK）来协商
电源传输。

配置与 Source 和 Sink 设备类似，主要区别如下：

* 在设备树 ``usb-c-connector`` 节点中设置 ``power-role = "dual"``
* 实现 Source 和 Sink 两种操作的回调

DRP 切换行为可通过 Kconfig 配置：

- :kconfig:option:`CONFIG_USBC_DRP_PERIOD_MS`：切换周期（50-100ms，默认 75ms）
- :kconfig:option:`CONFIG_USBC_DRP_DUTY_CYCLE`：作为 Source 的时间百分比（30-70%，默认 50%）

完整示例参见 :zephyr:code-sample:`usb-c-drp`。

API 参考
*************

.. doxygengroup:: _usbc_device_api

SINK 回调参考
***********************

.. doxygengroup:: sink_callbacks

SOURCE 回调参考
*************************

.. doxygengroup:: source_callbacks
