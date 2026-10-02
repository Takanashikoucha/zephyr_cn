.. _modem:

调制解调器模块
#############

本服务提供与调制解调器（modem）通信所需的模块。

调制解调器是自包含设备，实现了执行射频（RF）通信所需的硬件和
软件，包括 GNSS、蜂窝（Cellular）、WiFi 等。

调制解调器模块通过数据输入/数据输出管道（pipe）动态互连，
使其可独立测试且高度灵活，确保稳定性和可扩展性。

调制解调器管道
**********

本模块用于以线程安全的方式，对 UART 和 CMUX DLCI 通道等多种
机制上的数据输入/数据输出通信进行抽象。

调制解调器后端内部包含一个 modem_pipe
结构实例，以及抽象其底层机制所需的任何缓冲区和附加结构。

.. image:: images/modem_pipes.svg
        :alt: Modem pipes
        :align: center

调制解调器后端初始化后会返回指向其内部 modem_pipe
结构的指针，该指针将用于通过调制解调器管道 API
与后端交互。

.. doxygengroup:: modem_pipe

调制解调器 PPP
*********

本模块将一个 L2 PPP 网络接口（描述见
:ref:`net_l2_interface`）定义并绑定到调制解调器后端。L2 PPP 接口
发送和接收网络数据包。这些网络数据包在通过调制解调器后端
传输之前必须封装在 PPP 帧中。本模块
执行该封装。

.. doxygengroup:: modem_ppp

调制解调器 CMUX
**********

本模块是按 3GPP 27.010
规范实现的 CMUX。CMUX 是一种复用协议，允许多个
双向数据流，称为 DLCI 通道。本模块
附加到单个调制解调器后端，并暴露多个调制解调器后端，
每个代表一个 DLCI 通道。

该协议定义了简单的帧结构，用于将每个 DLC 拆分为小块数据。

.. image:: images/cmux_frame.svg
        :alt: CMUX basic frame
        :align: center

Zephyr 实现了基础帧类型，MTU 大小可在编译时配置。

本模块还为支持该功能的调制解调器实现了使用 CMUX 电源节省命令（PSC）的
省电机制。更多细节见下文 :ref:`cmux-power-saving` 一节。

.. doxygengroup:: modem_cmux

调制解调器 pipelink
**************

本模块用于全局共享调制解调器管道。本模块旨在
将设备驱动中调制解调器管道的创建与设置
和管道的使用者解耦。参见
:zephyr_file:`drivers/modem/modem_at_shell.c` 和
:zephyr_file:`drivers/modem/modem_cellular.c` 了解如何在
设备驱动与应用之间使用调制解调器 pipelink 的示例。

.. doxygengroup:: modem_pipelink

调制解调器 chat
**********

本模块实现与调制解调器的脚本化 AT 命令通信。
AT 命令组织为**脚本（script）**，每个脚本是一
系列命令—响应交互。模块通过调制解调器管道发送一条
命令字符串，然后等待匹配预期模式之一的
响应。找到匹配时，会携带解析后的参数
调用可选的回调函数。

脚本在编译时使用 :c:macro:`MODEM_CHAT_SCRIPT_DEFINE`
和 :c:macro:`MODEM_CHAT_SCRIPT_CMDS_DEFINE` 宏定义。每个脚本条目
将一个请求字符串与一个或多个 :c:struct:`modem_chat_match`
模式配对。匹配模式通过指定
分隔符（例如 ``","``）支持参数解析，从而轻松
从 ``+CSQ: 20,99`` 等响应中提取
字段。

除脚本化交互外，模块还会持续监控
数据流中的**非请求（unsolicited）**响应——即调制解调器
在没有先前命令时发送的消息（例如 ``+CEREG:`` 网络
注册状态更新）。这些由 chat 实例初始化时注册的
另一组匹配模式处理。

chat 模块可附加到任何调制解调器管道，因此可以
交替通过原始 UART 后端或 CMUX DLCI 通道
进行通信。

.. doxygengroup:: modem_chat

.. _cellular-modem:

蜂窝调制解调器
**************

通用蜂窝调制解调器驱动
:zephyr_file:`drivers/modem/modem_cellular.c` 将上述所有
模块组合起来，实现一个完整的、与硬件无关的
蜂窝数据连接。它暴露一个标准 Zephyr 网络
接口，使应用无需任何调制解调器专用代码即可使用 :ref:`BSD sockets API <bsd_sockets_interface>`。

架构概览
=====================

驱动将调制解调器模块组装为分层管道架构：

#. **UART 后端** — :c:struct:`modem_backend_uart` 实例提供
   最低层的调制解调器管道。它将物理 UART
   外设抽象为调制解调器管道 API，执行线程安全的、
   中断驱动的传输。

#. **CMUX** — :c:struct:`modem_cmux` 实例附加到 UART
   管道，并按 3GPP 27.010
   规范将其复用为两个 DLCI 通道。

#. **DLCI 通道 1（数据）** — 此管道在初始化期间承载
   AT 命令流量，或在连接建立后承载
   PPP 帧封装的 IP 数据。

#. **DLCI 通道 2（命令）** — 此管道在数据连接
   激活时专用于 AT
   命令流量，使驱动能够
   查询信号质量、注册状态及其他
   参数而不中断数据流。

#. **调制解调器 chat** — :c:struct:`modem_chat` 实例执行 AT
   命令脚本。CMUX 启动前它直接附加到
   UART 管道；之后移到 DLCI 1 用于初始化脚本，
   然后移到 DLCI 2 用于周期性监控。

#. **调制解调器 PPP** — :c:struct:`modem_ppp` 实例将 Zephyr IP
   数据包封装为 PPP 帧，并通过 DLCI 1 发送。在接收
   方向，它剥离 PPP 帧封装，将数据包交付给
   网络协议栈。

两个 DLCI 通道的同时使用是关键使能因素：
调制解调器可以在 DLCI 1 上以全速传输 IP 数据，同时驱动
继续在 DLCI 2 上后台交换 AT 命令。

连接生命周期
====================

驱动围绕一个内部状态机构建，依次
经历以下阶段：

上电与硬件复位
-----------------------------

驱动脉冲调制解调器的复位和电源 GPIO（若在
设备树中已定义），并等待调制解调器
变为可响应状态。

初始 AT 配置
------------------------

调制解调器 chat 模块直接附加到 UART 管道，并运行
调制解调器专用的 ``init_chat_script``。该脚本通常禁用
回显（echo）、查询 IMEI、型号、固件版本，并配置
非请求响应上报。此阶段的所有通信都是
UART 上的纯 AT 命令——CMUX 尚未激活。

CMUX 启动
--------------

init 脚本成功后，驱动发送 ``AT+CMUX``
命令将调制解调器切换到复用模式。CMUX 模块
附加到 UART 管道并打开 DLCI 1 和 DLCI 2。从这
一点起，所有通信都封装在 CMUX 帧中。

APN 配置与拨号
------------------------------

驱动将调制解调器 chat 附加到 DLCI 1，并运行一个动态
构建的 APN 脚本（``AT+CGDCONT``），随后运行拨号脚本
（``ATD*99#`` 或等效命令）。成功后，调制解调器
在 DLCI 1 上进入数据模式。

数据连接
----------------

调制解调器 PPP 模块附加到 DLCI 1 管道，调制解调器
chat 移到 DLCI 2。当
``+CEREG``（或 ``+CREG`` / ``+CGREG``）非请求响应指示
调制解调器已在网络上注册时，驱动调用 ``net_if_carrier_on()``。

此时，Zephyr 网络协议栈在 DLCI 1 上
协商一个 PPP 会话，应用即可正常使用套接字。与此同时，
DLCI 2 上的周期性 chat 脚本监控信号质量和
注册状态。

关闭
---------

驱动运行关闭脚本，并脉冲断电 GPIO 以
干净地关闭调制解调器。状态机返回空闲
状态。

添加对新调制解调器的支持
==============================

通用蜂窝驱动使用通过设备树兼容（compatible）绑定
和关联 chat 脚本提供的每调制解调器配置。
添加新调制解调器需要三个交付物：

#. 一个包含通用蜂窝调制解调器
   基础绑定的**设备树绑定**。

#. 定义初始化、拨号、周期性监控
   和（可选）关机 AT 命令序列的**chat 脚本**。

#. 一个将 chat 脚本与
   硬件配置绑定在一起的**设备实例化宏**。

驱动自动处理所有管道布线、CMUX 管理、PPP 帧封装
和状态机逻辑。

受支持的调制解调器
----------------

以下调制解调器已在
:zephyr_file:`drivers/modem/modem_cellular.c` 中受支持：

* Fibocom LE250
* Quectel BG95、BG96
* Quectel EG25-G、EG800Q
* SIMCom SIM7080、A76xx
* u-blox SARA-R4、SARA-R5、LARA-R6
* Sierra Wireless HL7800
* Telit ME910G1、ME310G1、LE910C1 Thread-x、LEx10Q1
* Nordic Semiconductor nRF91 SLM
* Sequans GM02S

每个受支持的调制解调器都使用同一组宏
（``MODEM_CHAT_SCRIPT_CMDS_DEFINE``、``MODEM_CHAT_SCRIPT_DEFINE``、
``MODEM_CELLULAR_DEFINE_INSTANCE`` 等）定义。参见
:zephyr_file:`drivers/modem/modem_cellular.c` 了解 init、dial、periodic
和 shutdown chat 脚本的完整示例。所有调制解调器
共享的通用基础设备树属性在
:zephyr_file:`dts/bindings/modem/zephyr,cellular-modem-device.yaml` 中有文档说明。

树外（Out-of-tree）调制解调器
-----------------

驱动宏和数据结构通过
:zephyr_file:`include/zephyr/drivers/modem/modem_cellular.h` 导出，
因此可以完全在 Zephyr 树**之外**定义
一个全新调制解调器——
例如在应用源码中——而无需修改任何上游
文件。这对于为特定用例微调 AT 命令序列，或
在提交上游之前开发对新调制解调器的支持非常有用。

首先创建一个包含通用基础
绑定的设备树绑定，然后使用
``modem_cellular.h`` 中的宏编写驱动源文件。以下三个文件即为所需全部。

**设备树绑定** — ``app/dts/bindings/my,modem.yaml``：

.. code-block:: yaml

   compatible: "my,modem"

   include: zephyr,cellular-modem-device.yaml

**设备树 overlay** — ``app.overlay``（部分）：

.. code-block:: devicetree

   &uart30 {
       modem: modem {
           compatible = "my,modem";
           status = "okay";
           mdm-power-gpios = <&gpio1 13 GPIO_ACTIVE_HIGH>;
       };
   };

**驱动源文件** — ``app/src/my_modem.c``：

.. code-block:: c

   #include <zephyr/drivers/modem/modem_cellular.h>
   #include <zephyr/device.h>

   MODEM_CELLULAR_COMMON_CHAT_MATCHES();
   MODEM_CHAT_MATCHES_DEFINE(my_modem_unsol,
       MODEM_CELLULAR_COMMON_UNSOL_MATCHES);

   /* Init script — configure the modem, enable unsolicited LTE
    * registration notifications, then switch to CMUX.
    */
   MODEM_CHAT_SCRIPT_CMDS_DEFINE(init_chat_script_cmds,
       MODEM_CHAT_SCRIPT_CMD_RESP("ATE0",              ok_match),
       MODEM_CHAT_SCRIPT_CMD_RESP("AT+CEREG=1",        ok_match),
       MODEM_CHAT_SCRIPT_CMD_RESP("AT+CMUX=0,0,5,127", ok_match));

   MODEM_CHAT_SCRIPT_DEFINE(init_chat_script, init_chat_script_cmds,
       abort_matches, modem_cellular_chat_callback_handler, 1);

   /* Dial script — enable the radio and open data mode */
   MODEM_CHAT_SCRIPT_CMDS_DEFINE(dial_chat_script_cmds,
       MODEM_CHAT_SCRIPT_CMD_RESP("AT+CFUN=1", ok_match),
       MODEM_CHAT_SCRIPT_CMD_RESP("ATD*99#",   connect_match));

   MODEM_CHAT_SCRIPT_DEFINE(dial_chat_script, dial_chat_script_cmds,
       dial_abort_matches, modem_cellular_chat_callback_handler, 60);

   static const struct modem_cellular_vendor_config my_modem_vendor = {
       .scripts = {
           .init = &init_chat_script,
           .dial = &dial_chat_script,
       },
       .unsol_matches = {
           .matches = my_modem_unsol,
           .size = ARRAY_SIZE(my_modem_unsol),
       },
       .chat_delimiter = "\r",
       .chat_filter = "\n",
       .power_pulse_duration_ms = 1000,
       .reset_pulse_duration_ms = 100,
       .startup_time_ms = 5000,
       .shutdown_time_ms = 5000,
   };

   /* Macro for defining a DT instance */
   #define MY_MODEM_DEVICE(inst)                                                   \
       MODEM_DT_INST_PPP_DEFINE(inst,                                              \
           MODEM_CELLULAR_INST_NAME(ppp, inst), NULL, 1500, 64);                   \
                                                                                   \
       static struct modem_cellular_data                                           \
           MODEM_CELLULAR_INST_NAME(data, inst);                                   \
                                                                                   \
       MODEM_CELLULAR_DEFINE_AND_INIT_USER_PIPES(inst,                             \
           (user_pipe_0, 3), (user_pipe_1, 4))                                     \
                                                                                   \
       MODEM_CELLULAR_DEFINE_INSTANCE(inst, &my_modem_vendor, NULL)

   #define DT_DRV_COMPAT my_modem
   DT_INST_FOREACH_STATUS_OKAY(MY_MODEM_DEVICE)
   #undef DT_DRV_COMPAT

上述示例是最小化的，但足以在通用蜂窝调制解调器上启动一个 PPP 连接。
参见 :zephyr_file:`drivers/modem/modem_cellular.c` 了解更完整的示例。

板级专用 init 脚本
==========================

init、网络与拨号脚本是按厂商范围的（键控到设备树
compatible），因此使用同一调制解调器的不同板级
配置（例如射频调谐器频段路由）否则就需要
分叉（fork）厂商驱动。板级可以改用
:c:macro:`MODEM_CELLULAR_BOARD_INIT_DEFINE` 注册自己的 chat 脚本。该脚本在 CMUX 建立后、
APN 和网络配置之前的 AT 控制通道上运行。
未注册脚本的板级不会增加任何 ROM 或 RAM 开销。

驱动会用推进连接序列的回调
覆盖脚本的完成回调，因此脚本上设置的任何回调都会被忽略。

.. code-block:: c

   MODEM_CHAT_MATCH_DEFINE(board_init_ok_match, "OK", "", NULL);
   MODEM_CHAT_SCRIPT_CMDS_DEFINE(board_init_cmds,
       MODEM_CHAT_SCRIPT_CMD_RESP("AT+QCFG=\"rf/tuner_cfg\",0,\"12,28\"", board_init_ok_match));
   MODEM_CHAT_SCRIPT_NO_ABORT_DEFINE(board_init, board_init_cmds, NULL, 10);

   MODEM_CELLULAR_BOARD_INIT_DEFINE(DT_NODELABEL(modem), &board_init);

.. _cmux-power-saving:

CMUX 电源节省
*****************

3GPP TS 27.010 规定了 CMUX 的电源节省机制，当
调制解调器支持时可在 Zephyr 中使用。

该电源节省机制涵盖规范中的以下章节：

* 5.2.5 Inter-frame Fill
* 5.4.6.3.2 Power Saving Control (PSC) message
* 5.4.7 Power Control and Wake-up Mechanisms

该电源节省机制允许对 CMUX 模块
使用的 UART 设备进行运行时电源管理。当所有
DLCI 通道都没有数据需要发送或接收时，CMUX 模块会在
可配置的超时后进入空闲状态。在空闲状态下，CMUX 模块会向
调制解调器发送一条电源节省控制消息，
请求其进入低功耗状态。随后 CMUX 模块
可以关闭管道设备，从而在启用运行时电源管理时
将 UART 设备断电。

当任何 DLCI 通道有数据需要发送或接收时，CMUX 模块
会退出空闲状态，并通过发送标志字符（flag character）
唤醒调制解调器，直到从调制解调器收到
标志字符为止。

对于通过 CMUX 之外的硬件线路（而非带内协议）
驱动休眠与唤醒的调制解调器，``cmux-no-powersave-handshake``
属性使握手在两端都退出。进入时，CMUX 跳过
PSC 帧交换，直接转入省电状态。退出时
CMUX 跳过标志字符交换，管道
重新打开后直接转入已连接状态。下一帧发出的
帧会自行重新同步帧结构。

某些调制解调器仅在 DTR（Data Terminal Ready，数据终端就绪）
信号被去断言时才允许将 UART 断电。在这种情况下，
支持 DTR 的 UART 设备可以与 CMUX 模块
配合使用，根据 UART 的电源状态控制 DTR 信号。

UART 断电时通过 incoming 数据唤醒，需要一个支持
RING 信号唤醒主机的调制解调器。
RING 信号由调制解调器驱动处理，当检测到
RING 信号时，它打开管道设备，
使 CMUX 模块能够唤醒调制解调器并
处理 incoming 数据。

:zephyr_file:`subsys/modem/modem_cmux.c` 模块使用以下状态机实现电源节省机制。

.. image:: images/cmux_state_machine.svg
        :alt: CMUX state machine when using power saving
        :align: center

在已连接（connected）状态内，``modem_cmux_process_received_byte()`` 须按规范 5.2.5 Inter-frame Fill 的描述回复重复的标志字符。
空闲定时器保持运行，并在每发送或接收一帧时清零。定时器到期将触发向省电模式转换。

在 POWERSAVE 状态内，所有 DLC 管道保持打开，但朝向 UART 的管道被阻塞或关闭，因此所有数据都缓存在 CMUX 环形缓冲区中等待唤醒。
在此状态内，重复的标志字符同样会被回复，以便远端按 5.4.7 的描述继续执行唤醒流程。
如果管道被关闭，则在启用运行时电源管理时允许将 UART 设备断电。

当 CONNECTED 状态的空闲定时器到期时，CMUX 状态机阻塞所有 DLC 管道，并发送 PSC 命令，使远端启动向 POWERSAVE 状态的转换。
当 PSC 命令被回复时，CMUX 转入 POWERSAVE 模式。

在 CONNECTED 状态内，远端可能发送 PSC 命令以启动向省电模式的转换。CMUX 阻塞所有 DLC 管道并发送 PSC 响应。
当 TX 缓冲区清空后，CMUX 进入 POWERSAVE 状态。

当任何 DLC 管道在 POWERSAVE 状态期间尝试发送数据时，CMUX 将其缓存，并转入 WAKEUP 状态，按 5.4.7 的规定通过发送连续的标志字符流启动唤醒流程。
远端回复标志字符，表示其已准备好接收数据。随后 CMUX 停止发送标志字符，转回 CONNECTED 状态，恢复正常运行。

CMUX 电源节省机制可使用以下设备树属性进行配置：

.. code-block:: yaml

  cmux-enable-runtime-power-save:
    type: boolean
    description: Enable runtime power saving using CMUX PSC commands.
                 This requires modem to support CMUX and PSC commands while keeping the data
                 connection active.
  cmux-close-pipe-on-power-save:
    type: boolean
    description: Close the modem pipe when entering power save mode.
                When runtime power management is enabled, this closes the UART.
                This requires modem to support waking up the UART using RING signal.
  cmux-idle-timeout-ms:
    type: int
    description: Time in milliseconds after which CMUX will enter power save mode.
    default: 10000

CMUX 带电源节省的示例设备树配置：

.. code-block:: devicetree

  &uart1 {
    status = "okay";
    zephyr,pm-device-runtime-auto;

    uart_dtr: uart-dtr {
      compatible = "zephyr,uart-dtr";
      dtr-gpios = <&interface_to_nrf9160 4 GPIO_ACTIVE_LOW>;
      status = "okay";
      zephyr,pm-device-runtime-auto;

      modem: modem {
        compatible = "nordic,nrf91-slm";
        status = "okay";
        mdm-ring-gpios = <&interface_to_nrf9160 5 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>;
        zephyr,pm-device-runtime-auto;
        cmux-enable-runtime-power-save;
        cmux-close-pipe-on-power-save;
        cmux-idle-timeout-ms = <5000>;
      };
    };
  };

上述示例展示了一个支持 DTR 的 UART 设备被一个支持 CMUX 和 PSC 命令的调制解调器使用。DTR 信号用于控制 UART 的电源状态。
调制解调器的 RING 信号用于在其断电时唤醒调制解调器子系统。
