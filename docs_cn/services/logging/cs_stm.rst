.. _logging_cs_stm:

使用 ARM Coresight STM 的多域日志
############################################

Arm CoreSight SoC-400 是一套用于在系统内构建调试与跟踪功能的综合组件库。STM（System Trace Macrocell，
系统跟踪宏单元）是一个被集成到 CoreSight 系统中的跟踪源，主要设计用于对嵌入在软件中的测量代码进行高带宽跟踪。这些测量代码由对 STMESP（STM Extended Stimulus Port，STM 扩展激励端口）外设寄存器的内存映射写操作组成。多个内核可以共享并直接访问 STM，而互不感知彼此。每个内核有 65536 个激励端口（相同的寄存器组），它们可以独立访问，因此当不同上下文想要记录数据时不需要加锁。

STM 扩展激励端口（STMESP）
***********************************

本地域（每个内核）可以访问自己的一组 STMESP 外设。每组包含用于写数据的寄存器（带或不带时间戳、带或不带标记）以及写标志的寄存器。
每次对 STMESP 寄存器的写操作都会导致用户数据被编码为 MIPI System Trace Protocol v2（STPv2）。硬件通过必要时向数据流中添加 Major 和 Channel 操作码，管理来自不同 STMESP 寄存器组和不同内核的数据复用。时间戳（来自所有内核的公共时钟源）和同步操作码由 STM 自主添加。

STM 生成的数据流可能流向各种接收端（sink）。例如，它可以直接发送到 TPIU（Trace Port Interface Unit，
跟踪端口接口单元），或保存到称为 ETR（Embedded Trace Router，嵌入式跟踪路由器）的 RAM 环形缓冲区中。TPIU 是一个 5 引脚接口（4 个数据引脚和一个时钟引脚），需要外部工具捕获数据（例如 J-Trace PRO）。当使用 ETR 时，系统中一个内核负责处理这些数据，例如将其通过 UART 转储到宿主。

ARM Coresight 嵌入式跟踪路由器（ETR）
*****************************************

ETR 是一个环形 RAM 缓冲区，跟踪数据被保存到其中。由于它可能包含来自各种来源的数据，因此使用额外的封装协议来复用它们。
``Coresight Trace Formatter`` 用于此目的。数据被编码为 16 字节的帧，每帧最多容纳 15 字节数据。环形 RAM 缓冲区大小限制为 4k，因此存在数据溢出的风险。如果发生溢出，数据会丢失，但由于 STPv2 数据流中存在同步操作码，同步可以恢复。

ETR 的数据在设备端处理。它可以原样转发到宿主（例如使用 UART），由宿主工具解码数据；也可以在片上解码数据，以人类可读格式输出数据。

Nordic Semiconductor NRF54H20 实现没有使用 ETR 外设获取缓冲区忙状态，而是使用自己的封装：Trace Buffer Monitor（TBM）。

STMESP 日志前端
***********************

实现了 :ref:`log_frontend` API。自定义前端假定所有所需操作都在日志宏调用的上下文中执行，同时假定前端提供时间戳。
前端利用存在多组 STMESP 寄存器这一事实，使用多组寄存器以避免加锁上下文。原子递增的通道计数器用于选择唯一的 STMESP 组，整条消息被写入该 STMESP。使用有限的寄存器组池，把大多数通道留给其他用途。

早期日志
=============

在 STM 或 ETR/TPIU 配置完成之前，不能使用 STMESP。为了支持早期日志，在基础设施就绪之前，使用一个专用 RAM 缓冲区写入数据。
当 STM 基础设施就绪被通知（:c:func:`log_frontend_stmesp_etr_ready`）时，RAM 缓冲区内容被写入 STMESP。早期日志仅适用于拥有并配置 Coresight 基础设施的内核（例如在 NRF54H20 上是 Secure 内核）。

跟踪点
=============

可能存在日志太慢（尽管它已经非常快）的情况。针对这种情况，增加了专用的 ``trace point`` API。它极快，因为只是对单个 STMESP 寄存器的一次写操作。API 中有 2 个函数：

* :c:func:`log_frontend_stmesp_tp` - 接受单个参数 - 索引。索引在 0 到 65280 之间。
* :c:func:`log_frontend_stmesp_tp_d32` - 接受两个参数 - 索引和用户数据。索引在 0 到 65280 之间。用户数据是 32 位字。

在 NRF54H20 上记录单个跟踪点耗时不到 100 ns，比最快的日志消息快约 7 倍。

使用 STM 记录日志
*****************

STM 日志有 2 种工作模式：

* 基于字典 - 辅助模式，使用基于字典的日志。在此模式下，日志字符串可以从二进制文件中移除，因为它们仅用于解码，而解码由宿主工具执行。此模式占用内存更少、速度更快（快 2-3 倍）。写入的数据更少，因此 ETR 缓冲区数据溢出的可能性更小。
* 独立 - 数据在片上解码，打印人类可读字符串。此模式需要更多设备资源和处理能力。

下图展示了使用 ARM Coresight STM 的多域日志。

.. figure:: images/coresight_architecture.png

每个内核（本地域）使用日志前端，将日志数据写入 STMESP 寄存器。

如果使用 TPIU 作为输出，则不再需要软件组件。STPv2 数据流由 STM 组成并通过 TPIU 发送。

如果使用 ETR RAM 缓冲区，则缓冲区所有者的内核（``proxy``）负责处理这些数据。如果使用基于字典的日志，proxy 只是将数据原样通过 UART 发送。
如果使用独立日志，proxy 使用 :ref:`cs_trace_defmt` 和 :ref:`mipi_stp_decoder` 解码数据并解复用消息。消息使用日志 :ref:`log_output` 格式化为人类可读字符串。

基于字典的日志
========================

辅助多核日志使用基于字典的日志向 STM 发送不含冗余字符串的消息，基于 Zephyr 提供的日志 API 的 :ref:`logging_guide_dictionary` 特性。
它不在日志消息中包含格式字符串，而是记录字符串存储位置（消息 ID）的地址，从而减小日志子系统的大小。如果数据进入 ETR 缓冲区，proxy 内核的职责是转储这些数据。配备解码工具的宿主 PC 使用构建过程中生成的 JSON 数据库，将这些地址转换回人类可读文本。

使用日志时，此方法具有以下优势：

* 它减小了二进制文件的大小，因为日志消息中使用的字符串不存储在二进制文件本身中。日志基础设施也非常有限。在本地域上只是前端，甚至不需要字符串格式化函数。
* 它减少了需要发送和由应用内核处理的数据量，因为字符串格式化被卸载到宿主端。
* 日志很快。在 NRF54H20 上记录一条简单消息（最多 2 个参数）耗时不到 1 us。

Proxy 内核使用 Nordic 专用外设（TBM）获取 ETR 缓冲区忙状态并通过 UART 发送数据。Nordic
 专用的 ETR 缓冲区驱动位于 :zephyr_file:`drivers/debug/debug_nrf_etr.c`。

配置
-------------

对于 Nordic SoC，应使用专用片段（:ref:`nordic-log-stm-dict`）启用日志。每个内核应使用该片段构建。
如果任何内核想使用它，则应用内核也需要启用它，因为它充当 proxy（ETR 缓冲区处理）。所有内核必须使用相同的日志配置。

读取日志
----------------

要读取基于字典的 STM 日志输出，请执行以下操作：

1. 设置日志捕获。

   使用 ``nrfutil trace stm`` 命令开始从设备捕获日志，为每个域 ID 指定数据库配置，以及串行端口、波特率和输出文件名::

      nrfutil trace stm --database-config 34:build/zephyr/log_dictionary.json,35:build_rad/zephyr/log_dictionary.json --input-serialport /dev/ttyACM1 --baudrate 115200 --output-ascii out.txt

#. 捕获并解码日志。

   nrfutil 将从指定的 UART 端口捕获日志数据，并使用提供的字典数据库将日志解码为人类可读格式。解码后的日志将保存到指定的输出文件（前一示例中的 :file:`out.txt` 文件）。

#. 打开输出文件查看解码后的日志消息。

   文件将包含时间戳和人类可读格式的日志消息。

如果日志捕获未能找到同步，请重新运行捕获过程。

.. note::
   重新运行过程时可能出现解码伪影或不正确的时间戳。

每条日志行都包含位于日志级别和模块名之间的与域相关或与内核相关的前缀，指示生成该日志条目的内核。以下是用于指示内核的前缀：

.. csv-table:: nRF54H20 日志前缀
   :header: "内核", "前缀", "ID"

   Secure 域, ``sec``, 0x21
   应用内核, ``app``, 0x22
   Radio 内核, ``rad``, 0x23
   系统控制器（SysCtrl）, ``sys``, 0x2c
   快速轻量级处理器（FLPR）, ``flpr``, 0x2d
   外设处理器（PPR）, ``ppr``, 0x2e
    , ``mod``, 0x24

独立日志
==================

前端写入 STMESP 寄存器。消息格式与 :zephyr_file:`subsys/logging/frontends/log_frontend_stmesp_demux.c` 中的片上解码器一致。

``Proxy`` 使用 Nordic 专用外设（TBM）获取 ETR 缓冲区忙状态，读取并解码数据，通过 UART 发送人类可读数据。Nordic 专用的 ETR 缓冲区驱动位于 :zephyr_file:`drivers/debug/debug_nrf_etr.c`。它使用 :ref:`cs_trace_defmt` 和 :ref:`mipi_stp_decoder` 以及上述解复用器解码消息。

日志消息包含日志宏中使用的只读格式字符串，因此无法从二进制文件中移除。此模式使用更多只读内存，吞吐量更低，因为消息更长且处理耗时。与基于字典的模式相比，日志慢 2-3 倍。

配置
-------------

对于 Nordic SoC，应使用专用片段（:ref:`nordic-log-stm`）启用日志。每个内核应使用该片段构建。
如果任何内核想使用它，则应用内核也需要启用它，因为它充当 proxy（ETR 缓冲区处理）。所有内核必须使用相同的日志配置。

读取日志
----------------

日志使用 Console UART 打印。

.. note::
   要在应用中使用 UART，UART 的节点必须在设备树中描述。更多细节参见 :ref:`devicetree-intro`。

以下是示例日志输出::

   [00:00:00.154,790] <inf> app/spsc_pbuf: alloc in 0x2f0df800
   [00:00:00.163,319] <inf> app/spsc_pbuf: alloc 0x2f0df800 wr_idx:20
   [00:00:00.181,112] <inf> app/spsc_pbuf: commit in 0x2f0df800
   [00:00:00.189,090] <inf> app/spsc_pbuf: commit 0x2f0df800, len:20 wr_idx: 44
   [00:00:00.202,577] <inf> rad/icmsg: mbox_callback
   [00:00:00.214,750] <inf> rad/spsc_pbuf: claim 0x2f0df800 rd_idx:20
   [00:00:00.235,823] <inf> rad/spsc_pbuf: free 0x2f0df800 len:20 rd_idx: 44
   [00:00:00.244,507] <inf> rad/spsc_pbuf: read done 0x2f0df800 len:20
   [00:00:00.272,444] <inf> rad/host: ep recv 0x330021f0, len:20
   [00:00:00.283,939] <inf> rad/host: rx:00 exp:00
   [00:00:00.292,200] <inf> rad/icmsg: read 0
   [00:00:05.077,026] <inf> rad/spsc_pbuf: alloc in 0x2f0df000
   [00:00:05.077,068] <inf> rad/spsc_pbuf: alloc 0x2f0df000 wr_idx:44
   [00:00:05.077,098] <inf> rad/spsc_pbuf: commit in 0x2f0df000
   [00:00:05.077,134] <inf> rad/spsc_pbuf: commit 0x2f0df000, len:20 wr_idx

每条日志行都包含位于日志级别和模块名之间的与域相关或与内核相关的前缀，指示生成该日志条目的内核。以下是用于指示内核的前缀：

.. csv-table:: nRF54H20 日志前缀
   :header: "内核", "前缀"

   Secure 域, ``sec``
   应用内核, ``app``
   Radio 内核, ``rad``
   系统控制器（SysCtrl）, ``sys``
   快速轻量级处理器（FLPR）, ``flpr``
   外设处理器（PPR）, ``ppr``

其他注意事项
=========================

使用 STM 日志时，请考虑以下事项：

* 使用优化的日志宏（最多 2 个字大小数值参数，如 ``LOG_INF("%d %c", (int)x, (char)y)``）以改善日志的大小和速度。
* 对于内存受限的应用（例如在 PPR 内核上运行时），在项目配置中将 :kconfig:option:`CONFIG_PRINTK` 和 :kconfig:option:`CONFIG_BOOT_BANNER` Kconfig 选项都设置为 ``n``，禁用 ``printk()`` 函数。
* 处理多个域（例如 Radio 内核和应用内核）时，确保每个数据库都带有正确的域 ID 前缀。
* 由于存储 STM 日志的 RAM 缓冲区大小有限，一些日志消息可能被丢弃。
