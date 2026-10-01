.. _can_shell:

CAN 外壳（Shell）
#########

.. contents::
    :local:
    :depth: 1

概述
********

CAN 外壳为 :ref:`shell <shell_api>` 模块提供带有子命令集的 ``can`` 命令。它允许在不编写专用应用的情况下，通过交互式接口测试和探索 :ref:`can_api` 驱动 API。CAN 外壳也可以在现有应用中启用，以辅助交互式调试 CAN 问题。

CAN 外壳提供对大多数 CAN 控制器特性的访问，包括检查、配置、发送和接收 CAN 帧，以及总线恢复。

要启用 CAN 外壳，必须启用以下 :ref:`Kconfig <kconfig>` 选项：

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_CAN`
* :kconfig:option:`CONFIG_CAN_SHELL`

以下 :ref:`Kconfig <kconfig>` 选项启用 ``can`` 命令的额外子命令和特性：

* :kconfig:option:`CONFIG_CAN_FD_MODE` 启用 CAN FD 特定子命令（例如用于设置 CAN FD 数据阶段的时序）。
* :kconfig:option:`CONFIG_CAN_RX_TIMESTAMP` 启用打印接收到的 CAN 帧的时间戳。
* :kconfig:option:`CONFIG_CAN_STATS` 启用在 ``can show`` 子命令中打印 CAN 控制器的各种统计信息。这也依赖于同时启用 :kconfig:option:`CONFIG_STATS`。
* :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE` 启用 ``can recover`` 子命令。

例如，为 :zephyr:board:`frdm_k64f` 构建 :zephyr:code-sample:`hello_world` 示例并启用 CAN 外壳和 CAN 统计：

.. zephyr-app-commands::
    :zephyr-app: samples/hello_world
    :board: frdm_k64f
    :gen-args: -DCONFIG_SHELL=y -DCONFIG_CAN=y -DCONFIG_CAN_SHELL=y -DCONFIG_STATS=y -DCONFIG_CAN_STATS=y
    :goals: build

关于如何连接和与 shell 交互的一般说明，参见 :ref:`shell <shell_api>` 文档。CAN 外壳带有内置帮助（除非禁用 :kconfig:option:`CONFIG_SHELL_HELP`）。向 ``can`` 命令或其任何子命令传递 ``-h`` 或 ``--help`` 即可打印内置帮助消息。所有子命令还支持其参数的 Tab 补全。

.. tip::
    所有 CAN 外壳子命令的第一个参数均为 CAN 控制器名称，并支持 Tab 补全。启用 :kconfig:option:`CONFIG_DEVICE_SHELL` 时，可使用 ``device list`` shell 命令获取所有可用设备的列表。下面的示例均使用设备名 ``can@0``。

检查
********

给定 CAN 控制器的属性可使用 ``can show`` 子命令进行检查，如下所示。属性包括核心 CAN 时钟速率、支持的最大比特率、支持的接收（RX）过滤器数量、能力、当前模式、当前状态、错误计数器、时序限制等：

.. code-block:: console

    uart:~$ can show can@0
    core clock:      144000000 Hz
    max bitrate:     5000000 bps
    max std filters: 15
    max ext filters: 15
    capabilities:    normal loopback listen-only fd
    mode:            normal
    state:           stopped
    rx errors:       0
    tx errors:       0
    timing:          sjw 1..128, prop_seg 0..0, phase_seg1 2..256, phase_seg2 2..128, prescaler 1..512
    timing data:     sjw 1..16, prop_seg 0..0, phase_seg1 1..32, phase_seg2 1..16, prescaler 1..32
    transceiver:     passive/none
    statistics:
      bit errors:    0
        bit0 errors: 0
        bit1 errors: 0
      stuff errors:  0
      crc errors:    0
      form errors:   0
      ack errors:    0
      rx overruns:   0

.. note::
    统计信息仅在启用 :kconfig:option:`CONFIG_CAN_STATS` 时打印。

配置
*************

CAN 外壳允许配置 CAN 控制器的模式和时序，以及开始和停止 CAN 帧的处理。

.. note::
    CAN 控制器的模式和时序只能在 CAN 控制器停止时更改，而停止状态正是启动时的初始设置。初始 CAN 控制器模式设置为 ``normal``，初始时序则根据 :ref:`devicetree` 属性 ``bitrate``、``sample-point``、``bitrate-data`` 和 ``sample-point-data`` 设置。

时序
======

经典 CAN 比特率 / CAN FD 仲裁阶段比特率可使用 ``can bitrate`` 子命令进行配置，如下所示。比特率以比特每秒（bps）指定。

.. code-block:: console

    uart:~$ can bitrate can@0 125000
    setting bitrate to 125000 bps

如果启用了 :kconfig:option:`CONFIG_CAN_FD_MODE`，可使用 ``can dbitrate`` 子命令配置数据阶段比特率，如下所示。比特率以比特每秒（bps）指定。

.. code-block:: console

    uart:~$ can dbitrate can@0 1000000
    setting data bitrate to 1000000 bps

这两个子命令均允许以位置参数形式指定可选的采样点（以千分比表示）和再同步跳宽（SJW，以时间量子为单位）。更多细节请参见这些子命令的交互式帮助。

也可以使用 ``can timing`` 和 ``can dtiming`` 子命令配置原始位时序。所需参数的细节请参见这些子命令的交互式帮助输出。

模式
====

CAN 外壳可使用 ``can mode`` 子命令设置 CAN 控制器的模式。下面给出一个启用回环模式的示例。

.. code-block:: console

    uart:~$ can mode can@0 loopback
    setting mode 0x00000001

该子命令接受在同一命令行上给出的多个模式（例如 ``can mode can@0 fd loopback`` 用于设置 CAN FD 和回环模式）。厂商特定的模式可以十六进制形式指定。

启动和停止
=====================

在按需配置好时序和模式之后，可使用 ``can start`` 子命令启动 CAN 控制器，如下所示。这将启用 CAN 帧的接收和发送。

.. code-block:: console

    uart:~$ can start can@0
    starting can@0

在重新配置时序或模式之前，需要先用 ``can stop`` 子命令停止 CAN 控制器，如下所示：

.. code-block:: console

    uart:~$ can stop can@0
    stopping can@0

接收
*********

要接收 CAN 帧，需要配置一个或多个 CAN 接收（RX）过滤器。CAN 接收过滤器使用 ``can filter add`` 子命令添加，如下所示。该子命令接受十六进制格式的 CAN ID，以及可选的 CAN ID 掩码（同样为十六进制格式），用于设置 CAN ID 中哪些位需要匹配。支持的参数的更多细节请参见该子命令的交互式帮助输出。

.. code-block:: console

    uart:~$ can filter add can@0 010
    adding filter with standard (11-bit) CAN ID 0x010, CAN ID mask 0x7ff, data frames 1, RTR frames 0, CAN FD frames 0
    filter ID: 0

返回的过滤器 ID（上例中为 0）在移除 CAN 接收过滤器时使用。

匹配已添加过滤器的接收到的 CAN 帧会打印到 shell。下面给出几个示例：

.. code-block:: console

    # Dev Flags    ID   Size  Data bytes
    can0  --       010   [8]  01 02 03 04 05 06 07 08
    can0  B-       010  [08]  01 02 03 04 05 06 07 08
    can0  BP       010  [03]  01 aa bb
    can0  --  00000010   [0]
    can0  --       010   [1]  20
    can0  --       010   [8]  remote transmission request

各列的含义如下：

* Dev

  * 接收该帧的设备名称。

* Flags

  * ``B``：帧设置了 CAN FD 波特率切换（BRS）标志。
  * ``P``：帧设置了 CAN FD 错误状态指示器（ESI）标志。发送节点处于错误被动（error-passive）状态。
  * ``-``：未设置的标志。

* ID

  * ``010``：帧的标准（11 位）CAN ID，十六进制格式，此处为 10h。
  * ``00000010``：帧的扩展（29 位）CAN ID，十六进制格式，此处为 10h。

* Size

  * ``[8]``：帧数据字节的数量，十进制格式，此处为带 8 个数据字节的经典 CAN 帧。
  * ``[08]``：帧数据字节的数量，十进制格式，此处为带 8 个数据字节的 CAN FD 帧。

* Data bytes

  * ``01 02 03 04 05 06 07 08``：帧的数据字节，十六进制格式，此处为 1 到 8 的数字。
  * ``remote transmission request``：帧为远程传输请求（RTR）帧，因此不携带数据字节。

.. tip::
    如果启用了 :kconfig:option:`CONFIG_CAN_RX_TIMESTAMP`，每一行的开头都会加上来自 CAN 控制器中自由运行时间戳计数器的时间戳。

已配置的 CAN 接收过滤器可使用 ``can filter remove`` 子命令再次移除，如下所示。过滤器 ID 即 ``can filter add`` 子命令返回的 ID（下例中为 0）。

.. code-block:: console

    uart:~$ can filter remove can@0 0
    removing filter with ID 0

另一个选项是使用 ``can dump`` 子命令：它会添加匹配任意接收帧的标准（11 位）和扩展（29 位）CAN 过滤器，启动 CAN 控制器，并将所有接收到的 CAN 帧打印到 shell：

.. code-block:: console

    uart:~$ can dump can@0
    dumping CAN RX frames on device can@0, press Ctrl+C to exit

按下 Ctrl+C 退出 ``can dump`` 子命令后，所添加的过滤器会被自动移除，CAN 控制器也会再次停止。

发送
*******

CAN 帧可使用 ``can send`` 子命令加入发送队列，如下所示。该子命令接受十六进制格式的 CAN ID，以及可选的数据字节数量（同样以十六进制指定）。支持的参数的更多细节请参见该子命令的交互式帮助输出。

.. code-block:: console

    uart:~$ can send can@0 010 1 2 3 4 5 6 7 8
    enqueuing CAN frame #2 with standard (11-bit) CAN ID 0x010, RTR 0, CAN FD 0, BRS 0, DLC 8
    CAN frame #2 successfully sent

总线恢复
************

``can recover`` 子命令可用于发起从 CAN 总线关闭（bus-off）事件的恢复，如下所示：

.. code-block:: console

    uart:~$ can recover can@0
    recovering, no timeout

该子命令接受可选的总线恢复超时（以毫秒为单位）。如果未指定超时，命令将无限期等待总线恢复成功。

.. note::
    ``recover`` 子命令仅在启用 :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE` 时可用。
