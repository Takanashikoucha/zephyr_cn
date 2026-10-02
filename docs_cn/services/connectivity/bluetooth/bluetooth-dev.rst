.. _bluetooth-dev:

应用开发
#######################

蓝牙应用使用文档 :ref:`application` 一节中描述的通用基础设施和方式开发。

仅与蓝牙应用相关的附加信息可在本页找到。

.. contents::
    :local:
    :depth: 2

线程安全
*************

调用蓝牙 API 应当是线程安全的，除非 API 函数的文档中另有说明。确保所有 API 调用都满足这一点的努力仍在持续进行，但总体目标在本段中正式陈述。欢迎提交有助于推动子系统向该目标迈进的 Bug 报告和 Pull Request。

.. _bluetooth-hw-setup:

硬件设置
**************

本节描述在 Zephyr 中构建和调试蓝牙应用时你可选择的方案。根据你可用的硬件、你的需求以及你偏好的开发类型，你可以选择某一种或另一种设置来匹配你的需求。

共有 3 种可能的设置：

#. :ref:`嵌入式 <bluetooth-hw-setup-embedded>`
#. :ref:`外部控制器 <bluetooth-hw-setup-external-ll>`

   - :ref:`QEMU host <bluetooth-hw-setup-qemu-host>`
   - :ref:`native_sim host <bluetooth-hw-setup-native-sim-host>`

#. :ref:`使用 BabbleSim 的仿真 nRF5x <bluetooth-hw-setup-bsim>`

.. _bluetooth-hw-setup-embedded:

嵌入式
========

该设置依赖所有软件直接运行在应用所针对的嵌入式平台上。
支持所有 :ref:`bluetooth-configs` 和 :ref:`bluetooth-build-types`，但如果你使用双芯片配置，或者你的 SoC 有多个核心且每个核心运行不同的构建类型（例如一个运行 Host，另一个运行 Controller），你可能需要多次构建 Zephyr。

要开始使用该设置进行开发，请遵循 :ref:`入门指南
<getting_started>`，选择一块（如果使用双芯片方案则选择多块）支持蓝牙的板子，然后 :ref:`运行应用
<application_run_board>`)。

有一种方式可以访问 Host 与 Controller 之间的 :ref:`HCI <bluetooth-hci>` 流量，即使没有物理传输层。说明参见 :ref:`嵌入式 HCI 跟踪 <bluetooth-embedded-hci-tracing>`。

.. _bluetooth-hw-setup-external-ll:

Linux 上的 Host 搭配外部 Controller
=========================================

.. note::
   目前仅在 GNU/Linux 上可用

该设置依赖“双芯片” :ref:`配置 <bluetooth-configs>`
，由以下设备组成：

#. 运行在 :ref:`QEMU <application_run_qemu>` 模拟器或 Zephyr 的 :zephyr:board:`native_sim <native_sim>` 原生
   移植上的 :ref:`仅 Host <bluetooth-build-types>` 应用
#. 一个 Controller，可以是以下类型之一：

   * 商业可用的 Controller
   * Zephyr 的 :ref:`仅 Controller <bluetooth-build-types>` 构建
   * :ref:`虚拟控制器 <bluetooth_virtual_posix>`

.. warning::
   某些外部 Controller 要么无法接受 Zephyr 默认设置的 Host 到
   Controller 流控参数（Qualcomm），要么不从 Controller 向 Host 传输任何数据（Realtek）。如果你
   在启动所选示例时看到类似::

     <wrn> bt_hci_core: opcode 0x0c33 status 0x12

   的消息（运行示例前请确保已在 :file:`prj.conf` 中启用
   :kconfig:option:`CONFIG_LOG`），或者 Controller 到 Host 没有数据流动，则
   你需要禁用 Host 到 Controller 的流控。为此，在 :file:`prj.conf` 中设置
   ``CONFIG_BT_HCI_ACL_FLOW_CONTROL=n``。

.. _bluetooth-hw-setup-qemu-host:

QEMU
----

你可以在 :ref:`QEMU 模拟器<application_run_qemu>` 上运行 Zephyr Host，
并让它与物理外部蓝牙 Controller 交互。

有关如何在该设置下构建和运行应用的完整说明，参见 :ref:`bluetooth_qemu_native`。

.. _bluetooth-hw-setup-native-sim-host:

native_sim
----------

.. note::
   目前仅在 GNU/Linux 上可用

:zephyr:board:`native_sim <native_sim>` 目标使用 Zephyr 内核和少量硬件仿真，将你的 Zephyr 应用构建为原生 Linux 可执行文件。

该可执行文件是一个普通的 Linux 程序，可以像其他任何程序一样进行调试和插桩，并与物理或虚拟外部 Controller 通信。参见：

- 物理控制器参见 :ref:`bluetooth_qemu_native`
- 虚拟控制器参见 :ref:`bluetooth_virtual_posix`

.. _bluetooth-hw-setup-bsim:

使用 BabbleSim 的仿真 nRF5x
==============================

.. note::
   目前仅在 GNU/Linux 上可用

:ref:`nrf52_bsim <nrf52_bsim>` 和 :ref:`nrf5340bsim <nrf5340bsim>` 板子
是仿真目标板
，仿真 nRF52/53 SoC 所需的必要外设，以便开发和测试蓝牙 LE 应用。
这些板子使用：

   * `BabbleSim`_ 仿真 nRF5x 调制解调器和射频环境。
   * POSIX 架构和原生模拟器仿真处理器，并在你的主机上原生运行。
   * `nrf5x HW 模型 <https://github.com/BabbleSim/ext_NRF_hw_models/>`_

与 :zephyr:board:`native_sim <native_sim>` 目标一样，构建结果是一个普通的 Linux 可执行文件。
有关如何运行单个或多个设备仿真的更多信息，可在 :ref:`这些板子的文档 <nrf52bsim_build_and_run>` 中找到。

使用 :ref:`nrf52_bsim <nrf52_bsim>` 时，通常进行 :ref:`组合构建
<bluetooth-build-types>`，但也可以在另一个仿真设备上用 H4 驱动替代集成控制器构建 host，
在一个仿真设备上用 :zephyr:code-sample:`bluetooth_hci_uart` 示例构建控制器。

使用 :ref:`nrf5340bsim <nrf5340bsim>` 时，你可以选择在其网络核心上构建控制器和 host 两者，
或者让网络核心仅运行控制器、应用核心运行 host 和你的应用，
HCI 传输基于 IPC。

初始化
**************

蓝牙子系统使用 :c:func:`bt_enable`
函数初始化。调用者应通过检查返回码是否有错误来确保该函数成功。如果向
:c:func:`bt_enable` 传递了函数指针，则初始化异步进行，
完成通过给定函数通知。

蓝牙应用示例
*****************************

下面展示了一个简单的蓝牙 beacon 应用。该应用
初始化蓝牙子系统并启用不可连接广播，
实际上充当蓝牙低功耗广播器。

.. literalinclude:: ../../../../samples/bluetooth/beacon/src/main.c
   :language: c
   :lines: 19-
   :linenos:

beacon 示例使用的关键 API 是 :c:func:`bt_enable`
（用于初始化蓝牙），然后使用 :c:func:`bt_le_adv_start`
（用于开始广播特定的广播数据与扫描响应数据的组合）。

更多示例
*************

更多 :zephyr:code-sample-category:`蓝牙示例应用 <bluetooth>` 可在
``samples/bluetooth/`` 中找到。

.. _BabbleSim: https://babblesim.github.io/
