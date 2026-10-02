.. _bluetooth-arch:

协议栈架构
##################

概述
********

本页描述 Zephyr 蓝牙协议栈的软件架构。

.. note::
   Zephyr 主要支持蓝牙低功耗（Bluetooth Low Energy，LE），即蓝牙规范的低功耗版本。Zephyr 对 BR/EDR Host 的部分功能也提供有限支持。

.. _bluetooth-layers:

蓝牙 LE 层次
===================

构成一个完整蓝牙低功耗协议栈的共有 3 个主要层次：

* **Host（主机）**：该层位于应用的正下方，由多个（非实时）网络与传输协议组成，使应用能够以标准且可互操作的方式与对端设备通信。
* **Controller（控制器）**：控制器实现链路层（LE LL），这是一个低层、实时协议，与射频硬件配合提供标准可互操作的空中通信。LL 负责调度数据包的接收与发送、保证数据交付，并处理所有 LL 控制流程。
* **Radio Hardware（射频硬件）**：硬件实现所需的模拟与数字基带功能模块，使链路层固件能够在 2.4GHz 频段内收发数据。

.. _bluetooth-hci:

主机控制器接口
=========================

`Bluetooth Specification`_ 规定了 Host 必须与 Controller 通信的格式，即主机控制器接口（HCI）协议。HCI 可以实现在 UART、SPI 或 USB 等多种不同的物理传输层之上。该协议定义了 Host 可以发送给 Controller 的命令、其可以预期收到的事件，以及需要经空中传输的用户与协议数据的格式。HCI 保证了不同的 Host 与 Controller 实现能够以标准方式通信，从而可以将来自不同厂商的 Host 与 Controller 组合使用。

.. _bluetooth-configs:

配置
=============

协议中三个相互独立的层次以及标准化接口，使得 Host 与 Controller 可以在不同平台上实现。以下两种配置最为常用：

* **单芯片配置**：在此配置中，单个微控制器实现全部三个层次以及应用本身。这也可以称为片上系统（SoC）实现。在这种情况下，蓝牙 Host 与蓝牙 Controller 通过 RAM 中的函数调用和队列直接通信。蓝牙规范未规定单芯片配置中 HCI 的实现方式，因此 HCI 命令、事件和数据在两者之间如何流动可以是实现相关的。该配置非常适合那些需要小占用面积和尽可能低功耗的应用与设计，因为所有组件都运行在单一 IC 上。
* **双芯片配置**：该配置使用两颗独立的 IC，一颗运行应用和 Host，另一颗运行 Controller 和射频硬件。这有时也被称为连接芯片（connectivity-chip）配置。当使用 Zephyr OS 作为 Controller 时，该配置允许更广泛的 Host 组合。由于 HCI 保证了 Host 与 Controller 实现之间的互操作性，包括 Zephyr 自身的蓝牙 Host 与 Controller，Zephyr Controller 的用户可以选择在任何其偏好的平台上运行任意 Host。例如，Host 可以是运行在任何支持 Linux 的处理器上的 Linux 蓝牙 Host 协议栈（BlueZ）。Host 处理器当然也可以运行 Zephyr 和 Zephyr OS 蓝牙 Host。反过来，将运行 Zephyr Host 的 IC 与不运行 Zephyr 的外部 Controller 组合也是支持的。

.. _bluetooth-build-types:

构建类型
===========

Zephyr 软件栈作为 RTOS 具有高度可配置性，尤其是蓝牙子系统可以在构建过程中以多种方式配置，仅包含所需的特性和层次，以减少 RAM 和 ROM 占用以及功耗。以下是从 Zephyr 项目代码库可以生成的几种不同蓝牙构建的简要列表：

* **仅 Controller 构建**：构建为蓝牙 Controller 时，Zephyr 包含链路层和一个特殊应用。该应用根据为 HCI 选择的物理传输层而有所不同：

  * :zephyr:code-sample:`bluetooth_hci_uart`
  * :zephyr:code-sample:`bluetooth_hci_usb`
  * :zephyr:code-sample:`bluetooth_hci_spi`

  该应用充当 UART、SPI 或 USB 外设与 Controller 子系统之间的桥梁，监听 HCI 命令、发送应用数据，并以事件和接收到的数据作出响应。此类构建设置以下 Kconfig 选项值：

  * :kconfig:option:`CONFIG_BT` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI_RAW` ``=y``

  控制器本身也需要启用，通常通过确保对应的设备树节点已启用来实现。

* **仅 Host 构建**：Zephyr OS Host 构建包含应用、蓝牙 Host，以及一个 HCI 驱动（UART 或 SPI），用于与外部 Controller 芯片对接。
  此类构建设置以下 Kconfig 选项值：

  * :kconfig:option:`CONFIG_BT` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI` ``=y``

  此外，如果平台还支持本地控制器，则需要将其禁用，通常通过禁用对应的设备树节点来实现。这需要在启用某个其他 HCI 驱动的设备树节点的同时进行，并确保 ``zephyr,bt-hci`` 设备树 chosen 属性指向该节点。

  ``samples/bluetooth`` 中的所有示例（用于仅 Controller 构建的除外）都可以作为仅 Host 构建来构建。

* **组合构建**：该构建包含应用、Host 和 Controller，专门用于单芯片（SoC）配置。
  此类构建设置以下 Kconfig 选项值：

  * :kconfig:option:`CONFIG_BT` ``=y``
  * :kconfig:option:`CONFIG_BT_HCI` ``=y``

  控制器本身也需要启用，通常通过确保对应的设备树节点已启用来实现。

  ``samples/bluetooth`` 中的所有示例（用于仅 Controller 构建的除外）都可以作为组合构建来构建。

下图展示了使用 Zephyr 组合构建（同一固件镜像中同时包含蓝牙 Host 和 Controller，并烧录到芯片上的构建）时的 SoC 或单芯片配置：

.. figure:: img/ble_cfg_single.png
   :align: center
   :alt: Bluetooth Combined build on a single chip

   单芯片配置上的组合构建

当使用连接芯片或双芯片配置时，存在多种 Host 与 Controller 的组合，其中一些如下图所示：

.. figure:: img/ble_cfg_dual.png
   :align: center
   :alt: Bluetooth dual-chip configuration builds

   双芯片配置上的仅 Host 与仅 Controller 构建

当使用 Zephyr Host（图像左侧）时，必须用不同的配置构建两个 Zephyr OS 实例，得到两个独立的镜像，分别烧录到各自的芯片上。Host 构建镜像包含应用、蓝牙 Host 和所选的 HCI 驱动（UART 或 SPI），而 Controller 构建运行 :zephyr:code-sample:`bluetooth_hci_uart` 或 :zephyr:code-sample:`bluetooth_hci_spi` 应用，为蓝牙 Controller 提供接口。

该配置并不限于使用 Zephyr OS Host，如图像右侧所示。实际上，可以选用众多现有的 GNU/Linux 发行版（其中大多数包含 Linux 自身的蓝牙 Host（BlueZ）），通过 UART 或 USB 将其连接到一个或多个 Zephyr OS Controller 构建实例。作为 Host 的 BlueZ 支持同时使用多个 Controller，适用于需要多个蓝牙射频同时工作但共享同一 Host 协议栈的应用。

源码树布局
******************

协议栈在源码树中的划分如下：

:zephyr_file:`subsys/bluetooth/host`
  :ref:`Host 协议栈 <bluetooth_le_host>`。HCI 命令与事件处理以及连接跟踪在此进行。L2CAP、ATT、SMP 等核心协议的实现也位于此处。

:zephyr_file:`subsys/bluetooth/controller`
  :ref:`蓝牙 LE Controller <bluetooth-ctlr-arch>` 实现。
  实现 HCI 的控制器侧、链路层以及射频收发器的访问。

:zephyr_file:`include/zephyr/bluetooth/`
  :ref:`公共 API <bluetooth_api>` 头文件。这些是应用为使用蓝牙功能而需要包含的头文件。

:zephyr_file:`drivers/bluetooth/`
  HCI 传输驱动。每种 HCI 传输都需要自己的驱动。例如，两种常见的 UART 传输协议（3-Wire 和 5-Wire）各有自己的驱动。

:zephyr_file:`samples/bluetooth/`
  :zephyr:code-sample-category:`蓝牙示例代码 <bluetooth>`。这是开始蓝牙应用开发的良好参考。

:zephyr_file:`tests/bluetooth/`
  测试应用。这些应用用于验证蓝牙协议栈的功能，但不一定是示例代码的最佳来源（请参见 :zephyr_file:`samples/bluetooth`）。

:zephyr_file:`doc/services/connectivity/bluetooth/`
  其他文档，例如 PICS 文档。

.. _Bluetooth Specification: https://www.bluetooth.com/specifications/bluetooth-core-specification
