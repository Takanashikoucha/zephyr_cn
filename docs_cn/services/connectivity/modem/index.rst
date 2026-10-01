.. _modem:

Modem modules
#############

此 service 提供与 modems 通信所需的 modules。

Modems 为 self-contained devices（实现执行 RF（Radio-Frequency）communication 所需的 hardware 和 software（包括 GNSS、Cellular、WiFi 等。

Modem modules 使用 data-in/data-out pipes 动态互连（使其可独立测试且高度灵活（确保稳定性和可扩展性。

Modem pipe
**********

此 module 用于以 thread-safe 方式抽象通过多种 mechanisms（如 UART 和 CMUX DLCI channels）的 data-in/data-out 通信。

Modem backend 内部将包含 modem_pipe structure 的实例（连同抽象其底层 mechanism 所需的任何 buffers 和额外 structures。

.. image:: images/modem_pipes.svg
        :alt: Modem pipes
        :align: center

Modem backend 初始化时返回其内部 modem_pipe structure 的 pointer（其将用于通过 modem pipe API 与 backend 交互。

.. doxygengroup:: modem_pipe

Modem PPP
*********

此 module 将 :ref:`net_l2_interface` 中描述的 L2 PPP network interface 定义并绑定到 modem backend。L2 PPP interface 发送和接收 network packets。这些 network packets 在通过 modem backend 传输前须用 PPP frames 包装。此 module 执行该包装。

.. doxygengroup:: modem_ppp

Modem CMUX
**********

此 module 为按 3GPP 27.010 specification 的 CMUX 实现。CMUX 为 multiplexing protocol（允许多个 bi-directional data streams（称为 DLCI channels。Module 附加到单个 modem backend（暴露多个 modem backends（每个代表一个 DLCI channel。

Protocol 定义简单 framing 以将每个 DLC 分割为小 data chunks。

.. image:: images/cmux_frame.svg
        :alt: CMUX basic frame
        :align: center

Zephyr 实现 basic frame 类型（build-time 可配置 MTU size。

Module 还为支持它的 modems 实现使用 CMUX Power Saving Command（PSC）的 power-saving。更多细节参见下文 :ref:`cmux-power-saving` section。

.. doxygengroup:: modem_cmux

Modem pipelink
**************

此 module 用于全局共享 modem pipes。此 module 旨在将 device drivers 中 modem pipes 的创建和 setup 与其用户解耦。参见 :zephyr_file:`drivers/modem/modem_at_shell.c` 和 :zephyr_file:`drivers/modem/modem_cellular.c` 作为如何在 device driver 和 application 之间使用 modem pipelink 的示例。

.. doxygengroup:: modem_pipelink

Modem chat
**********

此 module 实现与 modem 的 scripted AT command 通信。AT commands 组织为 **scripts**（每个 script 为 command–response exchanges 的序列。Module 通过 modem pipe 发送 command string（然后等待匹配预期 patterns 之一的 response。找到匹配时（调用带 parsed arguments 的可选 callback。

Scripts 用 :c:macro:`MODEM_CHAT_SCRIPT_DEFINE` 和 :c:macro:`MODEM_CHAT_SCRIPT_CMDS_DEFINE` macros 在 build time 定义。每个 script entry 将 request string 与一个或多个 :c:struct:`modem_chat_match` patterns 配对。Match patterns 通过指定 separator character（例如 ``","``）支持 argument parsing（使从 ``+CSQ: 20,99`` 等 responses 中提取 fields 容易。

除 scripted exchanges 外（module 持续监控 data stream 中的 **unsolicited** responses — modem 在无先前 command 时发送的 messages（例如 ``+CEREG:`` network registration updates。这些由 chat instance 初始化时注册的单独 match patterns 集合处理。

Chat module 附加到任何 modem pipe（因此可交替通过 raw UART backend 或 CMUX DLCI channel 通信。

.. doxygengroup:: modem_chat

.. _cellular-modem:

Cellular Modem
**************

通用 cellular modem driver :zephyr_file:`drivers/modem/modem_cellular.c` 将上述所有 modules 组合以实现完整、hardware-agnostic 的 cellular data connection。其暴露标准 Zephyr network interface（使 applications 无需任何 modem-specific code 即可使用 :ref:`BSD sockets API <bsd_sockets_interface>`。

Architecture overview
=====================

Driver 将 modem modules 组装为分层 pipe architecture：

#. **UART backend** — :c:struct:`modem_backend_uart` 实例提供最低层 modem pipe。其将物理 UART peripheral 抽象为 modem pipe API（执行 thread-safe、interrupt-driven 的 transfers。

#. **CMUX** — :c:struct:`modem_cmux` 实例附加到 UART pipe（按 3GPP 27.010 specification 将其 multiplex 为两个 DLCI channels。

#. **DLCI channel 1（data）** — 此 pipe 在初始化期间承载 AT command traffic（或在 connection 建立后承载 PPP-framed IP data。

#. **DLCI channel 2（commands）** — 此 pipe 在 data connection 激活时专用于 AT command traffic（允许 driver 在不打断 data flow 的情况下查询 signal quality、registration status 和其他 parameters。

#. **Modem chat** — :c:struct:`modem_chat` 实例执行 AT command scripts。CMUX 启动前其直接附加到 UART pipe；之后其移到 DLCI 1 用于 initialization scripts（然后移到 DLCI 2 用于 periodic monitoring。

#. **Modem PPP** — :c:struct:`modem_ppp` 实例将 Zephyr IP packets 包装为 PPP frames（通过 DLCI 1 发送。接收方向其剥离 PPP framing（将 packets 交付给 network stack。

两个 DLCI channels 的同时使用为关键使能：modem 可在 DLCI 1 上以全速传输 IP data（同时 driver 继续在 DLCI 2 上后台交换 AT commands。

Connection lifecycle
====================

Driver 围绕内部 state machine 构建（其经历以下 phases：

Power-on and hardware reset
----------------------------

Driver 脉冲 modem 的 reset 和 power GPIOs（若在 Device Tree 中定义）（并等待 modem 变为 responsive。

Initial AT configuration
------------------------

Modem chat module 直接附加到 UART pipe（并运行 modem-specific 的 ``init_chat_script``。此 script 通常禁用 echo、查询 IMEI、model、firmware version（并配置 unsolicited response reporting。此阶段所有通信为 UART 上的 plain AT — CMUX 尚未激活。

CMUX bring-up
--------------

Init script 成功后（driver 发送 ``AT+CMUX`` 命令将 modem 切换到 multiplexed mode。CMUX module 附加到 UART pipe（并打开 DLCI 1 和 DLCI 2。从此所有通信在 CMUX 内 framing。

APN configuration and dialing
------------------------------

Driver 将 modem chat 附加到 DLCI 1（并运行动态构建的 APN script（``AT+CGDCONT``）后跟 dial script（``ATD*99#`` 或等效。成功时（modem 在 DLCI 1 上进入 data mode。

Data connection
----------------

Modem PPP module 附加到 DLCI 1 pipe（且 modem chat 移到 DLCI 2。Driver 在 ``+CEREG``（或 ``+CREG`` / ``+CGREG``）unsolicited response 指示 modem 已在 network 上注册时调用 ``net_if_carrier_on()``。

此时 Zephyr network stack 在 DLCI 1 上协商 PPP session（且 application 可正常使用 sockets。同时（DLCI 2 上的 periodic chat scripts 监控 signal quality 和 registration status。

Shutdown
---------

Driver 运行 shutdown script（并脉冲 power-off GPIO 以干净地关闭 modem。State machine 返回 idle state。

Adding support for a new modem
==============================

通用 cellular driver 使用通过 Device Tree compatible bindings 和关联 chat scripts 提供的 per-modem configuration。添加新 modem 需三个 artifacts：

#. 包含通用 cellular modem base binding 的 **Device Tree binding**。

#. 定义 initialization、dialing、periodic monitoring 和（可选）shutdown 的 AT command 序列的 **Chat scripts**。

#. 将 chat scripts 和 hardware configuration 绑定的 **device instantiation macro**。

Driver 自动处理所有 pipe plumbing、CMUX management、PPP framing 和 state machine logic。

Supported modems
----------------

以下 modems 已在 :zephyr_file:`drivers/modem/modem_cellular.c` 中支持：

* Fibocom LE250
* Quectel BG95、BG96
* Quectel EG25-G、EG800Q
* SIMCom SIM7080、A76xx
* u-blox SARA-R4、SARA-R5、LARA-R6
* Sierra Wireless HL7800
* Telit ME910G1、ME310G1、LE910C1 Thread-x、LEx10Q1
* Nordic Semiconductor nRF91 SLM
* Sequans GM02S

每个支持的 modem 用同一组 macros（``MODEM_CHAT_SCRIPT_CMDS_DEFINE``、``MODEM_CHAT_SCRIPT_DEFINE``、``MODEM_CELLULAR_DEFINE_INSTANCE`` 等）定义。参见 :zephyr_file:`drivers/modem/modem_cellular.c` 作为 init、dial、periodic 和 shutdown chat scripts 的完整示例。所有 modems 共享的通用 base Device Tree properties 在 :zephyr_file:`dts/bindings/modem/zephyr,cellular-modem-device.yaml` 中文档化。

Out-of-tree modem
-----------------

Driver macros 和 data structures 通过 :zephyr_file:`include/zephyr/drivers/modem/modem_cellular.h` 导出（因此完全新的 modem 可在 Zephyr tree **之外**定义 — 例如在 application source 中 — 而不修改任何 upstream files。这对为特定 use case 微调 AT command 序列或在提交 upstream 前开发新 modem 支持有用。

从创建包含通用 base binding 的 Device Tree binding 开始（然后用 ``modem_cellular.h`` 中的 macros 编写 driver source file。以下三个文件即为所需全部。

**Device Tree binding** — ``app/dts/bindings/my,modem.yaml``：

.. code-block:: yaml

   compatible: "my,modem"

   include: zephyr,cellular-modem-device.yaml

**Device Tree overlay** — ``app.overlay``（部分）：

.. code-block:: devicetree

   &uart30 {
       modem: modem {
           compatible = "my,modem";
           status = "okay";
           mdm-power-gpios = <&gpio1 13 GPIO_ACTIVE_HIGH>;
       };
   };

**Driver source** — ``app/src/my_modem.c``：

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

上述示例为最小化但足以在通用 cellular modem 上启动 PPP connection。参见 :zephyr_file:`drivers/modem/modem_cellular.c` 作为更完整的示例。

Board-specific init script
==========================

Init、network 和 dial scripts 为 vendor-scoped（键控到 devicetree compatible）（因此使用相同 modem 的 boards 之间不同的 configuration（例如 RF tuner band routing（否则须 fork vendor driver。Board 可改用 :c:macro:`MODEM_CELLULAR_BOARD_INIT_DEFINE` 注册自己的 chat script。Script 在 CMUX 建立后且 APN 和 network configuration 前在 AT control channel 上运行。未注册 script 的 boards 不添加 ROM 或 RAM footprint。

Driver 用推进 connect sequence 的 callback 覆盖 script 的 completion callback（因此 script 上设置的任何 callback 被忽略。

.. code-block:: c

   MODEM_CHAT_MATCH_DEFINE(board_init_ok_match, "OK", "", NULL);
   MODEM_CHAT_SCRIPT_CMDS_DEFINE(board_init_cmds,
       MODEM_CHAT_SCRIPT_CMD_RESP("AT+QCFG=\"rf/tuner_cfg\",0,\"12,28\"", board_init_ok_match));
   MODEM_CHAT_SCRIPT_NO_ABORT_DEFINE(board_init, board_init_cmds, NULL, 10);

   MODEM_CELLULAR_BOARD_INIT_DEFINE(DT_NODELABEL(modem), &board_init);

.. _cmux-power-saving:

CMUX Power Saving
*****************

3GPP TS 27.010 指定 CMUX 的 power saving mechanism（当 modem 支持时可在 Zephyr 中使用。

Power saving mechanism 涵盖 specification 以下 sections：

* 5.2.5 Inter-frame Fill
* 5.4.6.3.2 Power Saving Control（PSC）message
* 5.4.7 Power Control and Wake-up Mechanisms

Power saving mechanism 允许 CMUX module 使用的 UART device 的 runtime power management。当任何 DLCI channel 无 data 发送或接收时（CMUX module 在可配置 timeout 后进入 idle state。Idle state 中（CMUX module 向 modem 发送 Power Saving Control message（请求其进入 low power state。CMUX module 然后可关闭 pipe device（允许在启用 runtime power management 时关闭 UART device。

当任何 DLCI channel 有 data 发送或接收时（CMUX module 退出 idle state（通过发送 flag characters 唤醒 modem（直到从 modem 收到 flag character。

对于从 CMUX 之外的 hardware line 而非通过 in-band protocol 驱动 sleep 和 wake 的 modems（``cmux-no-powersave-handshake`` property 使两半都 opt out 握手。Entry 时 CMUX 跳过 PSC frame exchange（直接转换到 power save。Exit 时 CMUX 跳过 flag-character exchange（pipe 重新打开后直接转换到 connected。下一个 outgoing frame 自行重新同步 framing。

某些 modems 仅当 DTR（Data Terminal Ready）signal 去断言时允许关闭 UART 电源。此情况下（支持 DTR 的 UART device 可与 CMUX module 一起使用以基于 UART 的 power state 控制 DTR signal。

UART 关闭时收到 incoming data 唤醒需要支持 RING signal 唤醒 host 的 modem。RING signal 由 modem driver 处理（其在检测到 RING signal 时打开 pipe device（允许 CMUX module 唤醒 modem 并处理 incoming data。

:zephyr_file:`subsys/modem/modem_cmux.c` module 用以下 state machine 实现 power saving mechanism。

.. image:: images/cmux_state_machine.svg
        :alt: CMUX state machine when using power saving
        :align: center

Connected state 内（``modem_cmux_process_received_byte()`` 须按 specification 5.2.5 Inter-frame Fill 描述回复重复 flag characters。Idle timer 保持运行（且每个发送或接收的 frame 清除。Timer 过期将启动转换到 power saving modes。

POWERSAVE state 内（所有 DLC pipes 保持打开（但朝向 UART 的 pipe 被 blocked 或 closed（因此所有 data 在 CMUX ringbuffers 中缓冲以等待唤醒。此 state 内（重复 flag characters 也被回复（允许远端按 5.4.7 描述继续 wake-up procedure。若 pipe 被 closed（允许在启用 runtime power management 时关闭 UART device。

CONNECTED state 中 idle timer 过期时（CMUX state machine 阻塞所有 DLC pipes（并发送 PSC command 使远端启动转换到 POWERSAVE state。PSC command 被回复时（CMUX 转换到 POWERSAVE mode。

CONNECTED state 中（远端可能发送 PSC command 以启动转换到 power saving mode。CMUX 阻塞所有 DLC pipes（并发送 PSC response。TX buffers 清空时（CMUX 进入 POWERSAVE state。

POWERSAVE state 中任何 DLC pipes 尝试发送 data 时（CMUX 缓冲它（并移到 WAKEUP state（其按 5.4.7 指定通过发送重复 flag characters 流启动 wake-up procedure。远端回复 flag characters 以指示其准备好接收 data。CMUX 然后停止发送 flag characters（并移回 CONNECTED state（恢复正常运行。

CMUX power saving mechanism 可用以下 Device Tree properties 配置：

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


CMUX 带 power saving 的示例 Device Tree setup：

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

上述示例展示支持 CMUX 和 PSC commands 的 modem 使用支持 DTR 的 UART device。DTR signal 用于控制 UART 的 power state。Modem 的 RING signal 用于在 modem 子系统关闭电源时唤醒它。
