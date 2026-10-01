.. _usbc_api:

USB-C device stack
##################

USB-C device stack 为
Type-C Port Controller (TCPC) 与 customer applications 间的 hardware independent interface。其为
Google ChromeOS Type-C Port Manager (TCPM) stack 的移植。
其提供以下 functionalities：

* 用 Type-C Port Controller drivers 提供的 APIs 与
  Type-C Port Controller 交互。
* 提供 customer applications 使用的 programming interface。
  APIs 描述在
  :zephyr_file:`include/zephyr/usb_c/usbc.h`

Configuration options
**********************************************************

USB-C device stack 支持实现 Sink only、Source only、
和 Dual Role Power (DRP) devices。

- :kconfig:option:`CONFIG_USBC_CSM_SINK_ONLY`: Sink USB-C Connection State Machine
- :kconfig:option:`CONFIG_USBC_CSM_SOURCE_ONLY`: Source USBC Connection State Machine
- :kconfig:option:`CONFIG_USBC_CSM_DRP`: Dual Role Power (DRP) USB-C Connection State Machine

:zephyr:code-sample-category:`List<usbc>` 不同用途的 samples。

Implementing a Sink Type-C and Power Delivery USB-C device
**********************************************************

USB-C Device 的 configuration 在 stack 层和 devicetree 中完成。

须定义以下 devicetree、structures 和 callbacks：

* Devicetree usb-c-connector node（引用一个 TCPC
* Devicetree vbus node（引用一个 VBUS measurement device
* 封装 application 特定 data 的 user defined structure
* Policy callbacks

例如（对 Sample USB-C Sink application：

每个 Physical Type-C port 在 devicetree 中由 usb-c-connector
compatible node 表示：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/boards/b_g474e_dpow1.overlay
   :language: dts
   :start-after: usbc.rst usbc-port start
   :end-before: usbc.rst usbc-port end
   :linenos:

VBUS 由 devicetree 中由
usb-c-vbus-adc compatible node 引用的 device 测量：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/boards/b_g474e_dpow1.overlay
   :language: dts
   :start-after: usbc.rst vbus-voltage-divider-adc start
   :end-before: usbc.rst vbus-voltage-divider-adc end
   :linenos:


User defined structure 被定义（稍后注册到 subsystem（且可
通过 callback 中的 API 访问：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst port data object start
   :end-before: usbc.rst port data object end
   :linenos:

这些 callbacks 由 subsystem 用于设置或获取 application 特定 data：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst callbacks start
   :end-before: usbc.rst callbacks end
   :linenos:

此 callback 由 subsystem 用于查询某 action 能否执行：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst check start
   :end-before: usbc.rst check end
   :linenos:

此 callback 由 subsystem 用于向 application 通知 event：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst notify start
   :end-before: usbc.rst notify end
   :linenos:

注册 callbacks：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst register start
   :end-before: usbc.rst register end
   :linenos:

注册 user defined structure：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst user data start
   :end-before: usbc.rst user data end
   :linenos:

启动 USB-C subsystem：

.. literalinclude:: ../../../../../samples/subsys/usb_c/sink/src/main.c
   :language: c
   :start-after: usbc.rst usbc start
   :end-before: usbc.rst usbc end
   :linenos:

Implementing a Source Type-C and Power Delivery USB-C device
************************************************************

USB-C Device 的 configuration 在 stack 层和 devicetree 中完成。

定义以下 devicetree、structures 和 callbacks：

* Devicetree ``usb-c-connector`` node（引用一个 TCPC
* Devicetree ``vbus`` node（引用一个 VBUS measurement device
* VBUS 和 VCONN power control 的 Devicetree ``pwrctrl`` node
* 封装 application 特定 data 的 user defined structure
* Policy callbacks

例如（对 Sample USB-C Source application：

每个 Physical Type-C port 在 devicetree 中由 ``usb-c-connector``
compatible node 表示：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/boards/stm32g081b_eval.overlay
   :language: dts
   :start-after: usbc.rst usbc-port start
   :end-before: usbc.rst usbc-port end
   :linenos:

VBUS 由 devicetree 中由
``usb-c-vbus-adc`` compatible node 引用的 device 测量：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/boards/stm32g081b_eval.overlay
   :language: dts
   :start-after: usbc.rst vbus-voltage-divider-adc start
   :end-before: usbc.rst vbus-voltage-divider-adc end
   :linenos:

VBUS 和 VCONN 的 Power control 可由 devicetree 中由
``zephyr,usb-c-pwrctrl`` compatible node 引用的 device 管理：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/boards/stm32g081b_eval.overlay
   :language: dts
   :start-after: usbc.rst pwrctrl start
   :end-before: usbc.rst pwrctrl end
   :linenos:

User defined structure 被定义（稍后注册到 subsystem（且可
通过 callback 中的 API 访问：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst port data object start
   :end-before: usbc.rst port data object end
   :linenos:

这些 callbacks 由 subsystem 用于设置或获取 application 特定 data：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst callbacks start
   :end-before: usbc.rst callbacks end
   :linenos:

此 callback 由 subsystem 用于查询某 action 能否执行：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst check start
   :end-before: usbc.rst check end
   :linenos:

此 callback 由 subsystem 用于向 application 通知 event：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst notify start
   :end-before: usbc.rst notify end
   :linenos:

注册 callbacks：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst register start
   :end-before: usbc.rst register end
   :linenos:

注册 user defined structure：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst user data start
   :end-before: usbc.rst user data end
   :linenos:

启动 USB-C subsystem：

.. literalinclude:: ../../../../../samples/subsys/usb_c/source/src/main.c
   :language: c
   :start-after: usbc.rst usbc start
   :end-before: usbc.rst usbc end
   :linenos:

Implementing a Dual Role Power (DRP) USB-C device
**************************************************

DRP devices 可工作为 Source 和 Sink（自动与
port partner 协商适当 role。未连接时（device 在
Source (Rp) 和 Sink (Rd) CC line advertisements 间切换（以检测并
连接任何 partner type。检测到 attach 后（device 进入
适当 attached state (Attached.SRC 或 Attached.SNK)（并启动
相应 Policy Engine state machine (PE_SRC 或 PE_SNK) 以协商
power delivery。

Configuration 类似 Source 和 Sink devices（有以下关键
差异：

* 在 devicetree ``usb-c-connector`` node 中设置 ``power-role = "dual"``
* 实现 Source 和 Sink 两种操作的 callbacks

DRP toggle 行为可用 Kconfig 配置：

- :kconfig:option:`CONFIG_USBC_DRP_PERIOD_MS`: Toggle period (50-100ms, default 75ms)
- :kconfig:option:`CONFIG_USBC_DRP_DUTY_CYCLE`: Percentage of time as Source (30-70%, default 50%)

完整示例参见 :zephyr:code-sample:`usb-c-drp`。

API reference
*************

.. doxygengroup:: _usbc_device_api

SINK callback reference
***********************

.. doxygengroup:: sink_callbacks

SOURCE callback reference
*************************

.. doxygengroup:: source_callbacks
