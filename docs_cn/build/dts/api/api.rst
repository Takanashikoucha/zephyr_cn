.. _devicetree_api:

设备树 API
##############

本页是 ``<zephyr/devicetree.h>`` API 的参考页。该 API 基于宏。
使用这些宏对调度没有影响。它们可以在任何调用上下文以及文件作用域中使用。

其中一些宏（以 ``DT_INST_`` 开头的）要求先定义一个名为 ``DT_DRV_COMPAT`` 的
特殊宏才能使用；这些宏将在下文逐一讨论。这些宏通常用于
:ref:`设备驱动 <device_model_api>` 内部，但在使用时注意相应事项后也可以在
驱动之外使用。

.. contents:: 目录
   :local:

.. _devicetree-generic-apis:

通用 API
************

本节的 API 可以在任何地方使用，且不需要定义 ``DT_DRV_COMPAT``。

节点标识符与辅助宏
============================

*节点标识符*（node identifier）是一种在 C 预处理器阶段引用设备树节点的方式。
节点标识符不是 C 值，但你可以使用它们通过例如
:ref:`devicetree-property-access` API 以 C 右值（rvalue）形式访问设备树数据。

根节点 ``/`` 的节点标识符为 ``DT_ROOT``。你可以使用 :c:macro:`DT_PATH`、
:c:macro:`DT_NODELABEL`、:c:macro:`DT_ALIAS` 和 :c:macro:`DT_INST`
为其他设备树节点创建节点标识符。

还有 :c:macro:`DT_PARENT` 和 :c:macro:`DT_CHILD` 宏，分别可用于
创建给定节点的父节点或某个子节点的节点标识符。

以下宏用于创建或操作节点标识符。

.. doxygengroup:: devicetree-generic-id

.. _devicetree-property-access:

属性访问
==============

以下通用宏可用于访问节点属性。
访问 :ref:`devicetree-ranges-property`、
:ref:`devicetree-reg-property` 和 :ref:`devicetree-interrupts-property`
有专门的 API。

即使节点被禁用，只要它有匹配的绑定（binding），
就可以用这些宏读取其属性值。

.. doxygengroup:: devicetree-generic-prop

.. _devicetree-ranges-property:

``ranges`` 属性
===================

访问 ``ranges`` 属性时使用这些 API，而不是 :ref:`devicetree-property-access`。
由于该属性的语义由设备树规范定义，即使节点没有匹配的绑定也可以使用这些宏。
不过，当节点绑定表明它是一个 PCIe 总线节点时（定义见
`PCI Bus Binding to: IEEE Std 1275-1994 Standard for Boot (Initialization Configuration) Firmware`_），
它们具有特殊的语义。

.. _PCI Bus Binding to\: IEEE Std 1275-1994 Standard for Boot (Initialization Configuration) Firmware:
    https://www.devicetree.org/open-firmware/bindings/pci/pci2_1.pdf

.. doxygengroup:: devicetree-ranges-prop

.. _devicetree-reg-property:

``reg`` 属性
================

访问 ``reg`` 属性时使用这些 API，而不是 :ref:`devicetree-property-access`。
由于该属性的语义由设备树规范定义，即使节点没有匹配的绑定也可以使用这些宏。

.. doxygengroup:: devicetree-reg-prop

.. _devicetree-interrupts-property:

``interrupts`` 属性
======================

访问 ``interrupts`` 属性时使用这些 API，而不是 :ref:`devicetree-property-access`。

由于该属性的语义由设备树规范定义，其中一些宏即使节点没有匹配的绑定也可以使用。
这不适用于以单元格名（cell name）作为参数的宏。

.. doxygengroup:: devicetree-interrupts-prop

遍历宏
===============

:c:macro:`DT_FOREACH_ANCESTOR` 宏允许遍历设备树节点的祖先节点。
此外，:c:macro:`DT_FOREACH_CHILD` 宏允许遍历设备树节点的子节点。

还有一些专门的遍历宏，例如
:c:macro:`DT_INST_FOREACH_STATUS_OKAY`，但它们在使用前要求定义 ``DT_DRV_COMPAT``。

.. doxygengroup:: devicetree-generic-foreach

存在性检查
================

本节记录了一些杂项宏，可用于测试节点是否存在、某类节点有多少个、
节点是否具有某些属性等。用于特殊目的的一些宏（例如
:c:macro:`DT_IRQ_HAS_IDX` 以及所有需要 ``DT_DRV_COMPAT`` 的宏）
在本页其他位置有文档。

.. doxygengroup:: devicetree-generic-exist

.. _devicetree-dep-ord:

节点间依赖
======================

``devicetree.h>`` API 对跟踪节点之间的依赖关系提供了一些支持。
依赖跟踪依赖于设备树节点之间的二元"依赖"（depends on）关系，
它被定义为以下"直接依赖"（directly depends on）关系的
`传递闭包（transitive closure）
<https://en.wikipedia.org/wiki/Transitive_closure>`_：

- 每个非根节点都直接依赖于其父节点
- 节点直接依赖于其属性通过 phandle 引用的任何节点，
  这可以通过节点绑定中的 :ref:`dt-bindings-dependency-mode` 更改
- 如果节点具有 ``interrupts`` 属性，则它直接依赖于其 ``interrupt-parent``
- 父节点继承其所有子节点的依赖

设备树的*依赖排序*（dependency ordering）是其节点的一个列表，
其中每个节点 ``n`` 都出现在依赖 ``n`` 的任何节点之前。
节点的*依赖序号*（dependency ordinal）则是它在该列表中的从零开始的索引。
因此，对于两个不同的设备树节点 ``n1`` 和 ``n2``（依赖序号分别为 ``d1`` 和 ``d2``），有：

- ``d1 != d2``
- 如果 ``n1`` 依赖于 ``n2``，则 ``d1 > d2``
- ``d1 > d2`` **并不**一定意味着 ``n1`` 依赖于 ``n2``

Zephyr 构建系统为最终的设备树选择一个依赖排序，
并为每个节点分配一个依赖序号。依赖相关信息可以通过以下宏访问。
所选择的具体依赖排序是实现细节，但循环依赖会被检测并导致错误，
因此使用这些宏时可以安全地假设不存在循环依赖。

还有基于实例编号的便捷宏；参见
:c:macro:`DT_INST_DEP_ORD` 及其后续文档。

.. doxygengroup:: devicetree-dep-ord

总线辅助宏
============

Zephyr 的设备树绑定语言支持 ``bus:`` 键，允许
绑定声明具有某个 compatible 的节点描述系统总线。
在这种情况下，子节点被视为位于给定类型的总线上，
可以使用以下 API。

.. doxygengroup:: devicetree-generic-bus

.. _devicetree-inst-apis:

基于实例的 API
******************

这些 API 推荐在设备驱动内部使用。使用时，将
``DT_DRV_COMPAT`` 定义为该设备驱动所实现支持的 compatible（小写加下划线形式）。
以下是一个设备树片段示例：

.. code-block:: devicetree

   serial@40001000 {
           compatible = "vnd,serial";
           status = "okay";
           current-speed = <115200>;
   };

使用示例，假设 ``serial@40001000`` 是 compatible 为 ``vnd,serial``
的唯一启用节点：

.. code-block:: c

   #define DT_DRV_COMPAT vnd_serial
   DT_DRV_INST(0)                  // serial@40001000 的节点标识符
   DT_INST_PROP(0, current_speed)  // 115200

.. warning::

   对实例编号做假设时要小心。API 保证参见 :c:macro:`DT_INST`。

如前所述，``DT_INST_*`` API 是按实例编号寻址节点的便捷宏。
它们几乎全部由
:ref:`devicetree-generic-apis` 之一定义。要找到等价的通用 API，
只需从宏名中去除 ``INST_`` 即可。例如，``DT_INST_PROP(inst,
prop)`` 等价于 ``DT_PROP(DT_DRV_INST(inst), prop)``。类似地，
``DT_INST_REG_ADDR(inst)`` 等价于 ``DT_REG_ADDR(DT_DRV_INST(inst))``，
依此类推。有一些例外：:c:macro:`DT_ANY_INST_ON_BUS_STATUS_OKAY`
和 :c:macro:`DT_INST_FOREACH_STATUS_OKAY` 是没有直接通用等价物的专用辅助宏。

由于 ``DT_DRV_INST()`` 要求定义 ``DT_DRV_COMPAT``，
未定义该宏就使用其中任何宏都是错误。

注意还有针对特定硬件的辅助宏可用；
其文档见 :ref:`devicetree-hw-api`。

.. doxygengroup:: devicetree-inst

.. _devicetree-hw-api:

硬件特定 API
**********************

以下 API 也可以通过包含 ``<devicetree.h>`` 使用；
无需额外的包含。

.. _devicetree-can-api:

CAN
===

这些便捷宏可用于描述 CAN 控制器/收发器的节点，
以及与之相关的属性。

.. doxygengroup:: devicetree-can

时钟（Clocks）
======

这些便捷宏可用于描述时钟源的节点，
以及与之相关的属性。

.. doxygengroup:: devicetree-clocks

DMA
===

这些便捷宏可用于描述直接内存访问（DMA）控制器或通道的节点，
以及与之相关的属性。

.. doxygengroup:: devicetree-dmas

.. _devicetree-display-api:

显示（Display）
=======

这些便捷宏可用于描述显示控制器的节点，
以及与之相关的属性。

.. doxygengroup:: devicetree-display

.. _devicetree-flash-api:

固定与映射的 flash 分区
================================

这些便捷宏可用于专用的 ``fixed-partitions``
和 ``zephyr,mapped-partition`` compatible，
它们用于在设备树中编码 flash 存储器分区信息。
详见 :dtcompatible:`fixed-partitions`
和 :dtcompatible:`zephyr,mapped-partition`。

.. doxygengroup:: devicetree-fixed-partition

.. _devicetree-gpio-api:

GPIO
====

这些便捷宏可用于描述 GPIO 控制器/引脚的节点，
以及与之相关的属性。

.. doxygengroup:: devicetree-gpio

.. _devicetree-hwspinlock-api:

HWSpinlock
==========

这些便捷宏可用于描述硬件自旋锁（hardware spinlock）的节点，
以及与之相关的属性。

.. doxygengroup:: devicetree-hwspinlock

IO 通道
===========

这些宏通常被需要使用 IO 通道（例如 ADC 或 DAC 通道）
进行转换的设备驱动使用。

.. doxygengroup:: devicetree-io-channels

.. _devicetree-mbox-api:

MBOX
====

这些便捷宏可用于描述 MBOX 控制器/使用者的节点，
以及与之相关的属性。

.. doxygengroup:: devicetree-mbox

.. _devicetree-mux-api:

MUX
===

这些便捷宏可用于描述 MUX 控制器/消费者的节点，
以及与之相关的属性。

.. doxygengroup:: devicetree-mux

.. _devicetree-nvmem-api:

NVMEM
=====

这些便捷宏可用于描述非易失性存储器（Non-Volatile Memory）的节点，
以及与之相关的属性。

.. doxygengroup:: devicetree-nvmem

.. _devicetree-ordinals-api:

序号（Ordinals）
========

这些便捷宏可用于描述依赖跟踪（Dependency tracking）的节点，
以及与之相关的属性。

.. doxygengroup:: devicetree-dep-ord

.. _devicetree-pinctrl-api:

Pinctrl（引脚控制）
=====================

这些宏用于按名称或索引访问引脚控制属性。

设备树节点可以具有指定引脚控制（有时称为引脚复用，pin mux）设置的属性。
这些属性通过节点内的 ``pinctrl-<index>`` 属性表示，
其中 ``<index>`` 值是从 0 开始的连续整数。
它们还可以使用 ``pinctrl-names`` 属性命名。

以下是一个示例：

.. code-block:: DTS

   node {
       ...
       pinctrl-0 = <&foo &bar ...>;
       pinctrl-1 = <&baz ...>;
       pinctrl-names = "default", "sleep";
   };

在上面，``pinctrl-0`` 的名称是 ``"default"``，``pinctrl-1`` 的名称
是 ``"sleep"``。``pinctrl-<index>`` 属性值包含 phandle。
属性内的 ``&foo``、``&bar`` 等 phandle 指向的节点
内容因平台而异，它们描述该节点的引脚配置。

.. doxygengroup:: devicetree-pinctrl

PWM
===

这些便捷宏可用于描述 PWM 控制器的节点
以及与之相关的属性。

.. doxygengroup:: devicetree-pwms

复位控制器（Reset Controller）
================

这些便捷宏可用于描述复位控制器的节点
以及与之相关的属性。

.. doxygengroup:: devicetree-reset-controller

SPI
===

这些便捷宏可用于描述 SPI 控制器或设备的节点，
视具体情况而定。

.. doxygengroup:: devicetree-spi

.. _devicetree-chosen-nodes:

Chosen 节点
************

特殊的 ``/chosen`` 节点包含描述系统级设置的属性。
:c:macro:`DT_CHOSEN()` 宏可用于获取 chosen 节点的节点标识符。

.. doxygengroup:: devicetree-generic-chosen

.. _devicetree-zephyr-chosen-nodes:

Zephyr 特定的 chosen 节点
****************************

下表记录了一些常用的 Zephyr 特定 chosen 节点。

有时，chosen 节点的 label 属性会被用于设置某个 Kconfig 选项的默认值，
该选项进而配置某个硬件特定设备。这通常用于向后兼容，
即 Kconfig 选项早于 Zephyr 的设备树支持的情况。在其他情况下，
没有对应的 Kconfig 选项，设备树节点直接在源代码中用于选择设备。

.. Keep list sorted by property name:
.. zephyr-keep-sorted-start re(^\s+\* - \w+,\w+)

.. list-table:: Zephyr 特定的 chosen 属性
   :header-rows: 1
   :widths: 25 75

   * - 属性
     - 用途
   * - mcuboot,ram-load-dev
     - 当 Zephyr 应用被构建为由 MCUboot 加载到 RAM 时
       （:kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_MODE_SINGLE_APP_RAM_LOAD`），
       该属性用于告诉 MCUboot 镜像的加载地址，
       即 chosen 节点的 ``reg``。
   * - zephyr,boot-mode
     - 用于 :ref:`boot_mode_api` 选择，是 :ref:`retention_api` 的一部分，
       指定设备上应启动哪个镜像。
   * - zephyr,bootloader-info
     - 选择用于与引导加载程序（bootloader）共享信息的 :ref:`retention_api` 区域。
   * - zephyr,bt-c2h-uart
     - 选择 :zephyr:code-sample:`bluetooth_hci_uart`
       中用于主机通信的 UART
   * - zephyr,bt-hci
     - 选择 Bluetooth 主机协议栈使用的 HCI 设备
   * - zephyr,bt-hci-ipc
     - 选择 :zephyr:code-sample:`bluetooth_hci_ipc` 示例中
       用于将 Bluetooth 控制器暴露给另一个设备或 CPU 的 IPC 设备。
   * - zephyr,bt-mon-uart
     - 设置用于 Bluetooth 监控日志的 UART 设备
   * - zephyr,camera
     - 视频输入设备，通常是摄像头。
   * - zephyr,canbus
     - 设置默认的 CAN 控制器
   * - zephyr,code-partition
     - Zephyr 镜像的 text 段应链接到的 flash 分区
   * - zephyr,console
     - 设置控制台驱动使用的 UART 设备
   * - zephyr,cpu-load-counter
     - 选择用于跟踪 CPU 空闲时间的 :ref:`counter_api` 设备。
   * - zephyr,crc
     - 选择 CRC 子系统用作加速器的 CRC 设备
   * - zephyr,display
     - 设置默认的显示控制器
   * - zephyr,dtcm
     - 某些 Arm SoC 上的数据紧耦合存储器（Data Tightly Coupled Memory）节点
   * - zephyr,edac
     - 选择 EDAC 子系统使用的 :ref:`edac_api` 设备。
   * - zephyr,entropy
     - 可用作系统级熵源的设备
   * - zephyr,flash
     - 其 ``reg`` 有时用于设置
       :kconfig:option:`CONFIG_FLASH_BASE_ADDRESS` 和 :kconfig:option:`CONFIG_FLASH_SIZE`
       默认值的节点
   * - zephyr,flash-controller
     - 对应 ``zephyr,flash`` 节点 flash 控制器设备的节点
   * - zephyr,gdbstub-uart
     - 设置 :ref:`gdbstub` 子系统使用的 UART 设备
   * - zephyr,hdlc-rcp-if
     - 选择 OpenThread HDLC RCP 接口使用的无线电设备。
       该设备的 ``api`` 必须是 :c:struct:`hdlc_api`。
   * - zephyr,host-cmd-espi-backend
     - 参见 :ref:`ec_host_cmd_backend_api` API 文档。
   * - zephyr,host-cmd-shi-backend
     - 参见 :ref:`ec_host_cmd_backend_api` API 文档。
   * - zephyr,host-cmd-spi-backend
     - 参见 :ref:`ec_host_cmd_backend_api` API 文档。
   * - zephyr,host-cmd-uart-backend
     - 参见 :ref:`ec_host_cmd_backend_api` API 文档。
   * - zephyr,ieee802154
     - 网络子系统用于设置 IEEE 802.15.4 设备
   * - zephyr,ipc
     - OpenAMP 子系统用于指定进程间通信（IPC）设备
   * - zephyr,ipc_rsc_table
     - 指定将用于 OpenAMP 资源表的内存区域。
       仅在启用 :kconfig:option:`CONFIG_OPENAMP_COPY_RSC_TABLE` 时需要。
   * - zephyr,ipc_rx
     - ``zephyr,ipc`` 的替代方案。当收发使用不同设备时，
       选择用于接收的 IPC 设备。必须同时提供 ``zephyr,ipc_tx``，
       它选择用于发送的 IPC 设备。当提供此 chosen 和 ``zephyr,ipc_tx`` 时，
       单设备 ``zephyr,ipc`` compatible **不得**提供。
   * - zephyr,ipc_shm
     - 其 ``reg`` 被 OpenAMP 子系统用于确定可用于
       进程间通信（IPC）的共享内存（SHM）的基址和大小的节点
   * - zephyr,ipc_tx
     - 参见 ``zephyr,ipc_rx`` 的说明。
   * - zephyr,itcm
     - 某些 Arm SoC 上的指令紧耦合存储器（Instruction Tightly Coupled Memory）节点
   * - zephyr,led-strip
     - 用于确定 WS2812 GPIO 驱动时序的 LED 灯带节点
   * - zephyr,log-ipc
     - 选择日志子系统 IPC 服务后端使用的 IPC 设备。
   * - zephyr,log-uart
     - 设置日志子系统 UART 后端使用的 UART 设备。
       如果定义，UART 日志后端将输出到该节点列出的设备。
   * - zephyr,modem-uart
     - 选择 :zephyr:code-sample:`at_client` 示例使用的调制解调器 UART。
   * - zephyr,ocm
     - Xilinx Zynq-7000 和 ZynqMP SoC 上的片上存储器（On-chip memory）节点
   * - zephyr,openthread-counter
     - 当启用 :kconfig:option:`CONFIG_OPENTHREAD_ALARM_COUNTER` 时，
       选择 OpenThread 平台用于微秒报警定时器的计数器设备。
   * - zephyr,osdp-uart
     - 设置 OSDP 子系统使用的 UART 设备
   * - zephyr,ot-uart
     - OpenThread 用于指定 Spinel 协议 UART 设备
   * - zephyr,pcie-controller
     - 对应 PCIe 控制器的节点
   * - zephyr,ppp-uart
     - 设置 PPP 使用的 UART 设备
   * - zephyr,ram-console
     - 选择 :dtcompatible:`RAM section <zephyr,memory-region>`，
       控制台子系统的 RAM 后端应将其缓冲区放置在该区域
   * - zephyr,rtc
     - 设置默认的 RTC 设备（例如 :ref:`SNTP library <sntp_interface>`
       在启用 :kconfig:option:`CONFIG_NET_CONFIG_CLOCK_SNTP_SET_RTC` 时
       用于设置系统时间）
   * - zephyr,rtk-serial
     - 选择串行 GNSS RTK 客户端使用的 :ref:`uart_api` 设备。
   * - zephyr,secure-storage-its-partition
     - 固定分区节点。选择 Secure Storage ZMS 后端使用的分区。
   * - zephyr,sensor-clock
     - 选择用作传感器时间源的 :ref:`counter_api` 设备。
   * - zephyr,settings-partition
     - 固定分区节点。如果定义，选择
       NVS 和 FCB 设置后端使用的分区。
   * - zephyr,shell-uart
     - 设置串行 shell 后端使用的 UART 设备
   * - zephyr,sram
     - 其 ``reg`` 设置 Zephyr 镜像可用 SRAM 存储器基址和大小的节点，
       链接时使用
   * - zephyr,system-timer
     - 选择用作 Zephyr 系统定时器的硬件定时器实例，
       它是一个系统级单例功能。当选定的系统定时器驱动对应
       可能存在多个实例的定时器硬件时，需要此 chosen：
       它选择一个实例作为系统定时器，并允许将其他实例
       用于其他 API。当选定的系统定时器驱动对应
       永远只可能有一个实例的定时器硬件（例如 Cortex-M SysTick 定时器）时，
       此 chosen 被忽略；否则，它必须对应
       选定的系统定时器驱动可以操作的节点。
       （注意：Zephyr 系统定时器*驱动*是通过 Kconfig 选项
       （如 :kconfig:option:`CONFIG_CORTEX_M_SYSTICK`）选择的
       —— 而不是通过设备树！）
   * - zephyr,system-timer-companion
     - 选择在主系统定时器处于低功耗状态不活跃时
       用于保持计时的设备。它必须实现 :ref:`counter_api` API。
   * - zephyr,tflm-storage
     - 选择 :zephyr:code-sample:`tflite-ethosu` 示例使用的
       :dtcompatible:`memory region <zephyr,memory-region>`。
   * - zephyr,touch
     - 触摸屏控制器设备节点。当使用 LVGL 时，如果
       启用 :kconfig:option:`CONFIG_LV_Z_POINTER_FROM_CHOSEN_TOUCH`，
       将创建一个 LVGL 指针输入设备，
       以触摸屏控制器作为其输入源。
   * - zephyr,tracing-uart
     - 设置 tracing 子系统使用的 UART 设备
   * - zephyr,uart-mcumgr
     - 用于 :ref:`device_mgmt` 的 UART
   * - zephyr,uart-pipe
     - 设置串行管道（pipe）驱动使用的 UART 设备
   * - zephyr,videoenc
     - 视频编码器设备，通常是 H264 或 MJPEG 视频编码器。

.. zephyr-keep-sorted-stop
