.. _mcumgr_smp_transport_specification:

SMP Transport Specification
###########################

此 documents 规定实现
server 和 client
side SMP transports 所需 information。

.. _mcumgr_smp_transport_ble:

Bluetooth Low Energy (LE)
*************************

实现
SMP client 时（MCUmgr Clients 须使用以下
Bluetooth Characteristics：

- **Service UUID**: ``8D53DC1D-1DB7-4CD3-868B-8A527460AA84``
- **Characteristic UUID**: ``DA2E7828-FBCE-4E01-AE9E-261174997C48``

所有 SMP communication 使用单个 GATT characteristic。SMP request
通过 GATT Write Without Response command 发送。SMP
response 以
GATT Notification 形式发送

若 SMP request 或
response 过大无法装入单个 GATT command（
sender 将其 fragment 到多个 packets。Request 或
response 被 fragment 时不引入额外
framing；payload 简单
拆分到多个 packets 中。由于 GATT 保证
packets 的有序
delivery（第一个 fragment 中的 SMP header 包含
reassembly 所需
sufficient information。

.. _mcumgr_smp_transport_uart:

UART/serial and console
***********************

Zephyr 的 MCUmgr subsystem 的 SMP protocol specification 使用
data 的基本 framing 以
允许 UART channel 的
multiplexing。Multiplexing 需
每个 frame 前缀两个 byte marker（并以
newline 终止。当前
MCUmgr 对 frame size 施加 127 byte 限制（虽然
无真正
protocol constraints 要求该限制。
Limit 包含
prefix 和 newline character（故允许的
payload
size 实际为 124 bytes。

虽然 Zephyr 中无此
transport（但可
实现无
framing 的
MCUmgr client/server（经 UART transport（或用
hardware serial port control（或其他
framing 手段。

Frame fragmenting
=================

Serial 上的 SMP protocol 被 fragment 为
MTU size frames；每
frame 由两个 byte start marker、body 和
terminating newline
character 组成。

有四种类型的 frames：initial、partial、partial-final
和 initial-final；每种 frame 类型以
start marker 和/或 body
contents 不同。

Frame formats
-------------

Initial frame 须由
optional sequence of partial
frames 跟随（最后由
partial-final frame 跟随。
Body 始终 Base64 编码（故此处描述为
MTU - 3 的 body size 实际
能携带 N = (MTU - 3) / 4 * 3 bytes
的 raw data。

Initial frame 的 body 前缀两个 byte total packet length（
Big Endian 编码（且等于 raw body size 加
两个
bytes（
CRC16 的
size；这意味着允许装入
initial frame 的实际 body size 为 N - 2。

若 body size 小于 N - 4（则
可在
单个
frame 中携带
preceding length 和
following
CRC 的
entire body（此处称为
initial-final；initial-final
frame 的描述见下文。

Initial frame 格式：

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | Content       | Size          | Description               |
    +===============+===============+===========================+
    | 0x06 0x09     | 2 bytes       | Frame start marker        |
    +---------------+---------------+---------------------------+
    | <base64-i>    | no more than  | Base64 encoded body       |
    |               | MTU - 3 bytes |                           |
    +---------------+---------------+---------------------------+
    | 0x0a          | 1 byte        | Frame termination         |
    +---------------+---------------+---------------------------+

``<base64-i>`` 为以下形式的 Base64 编码
body：

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | Content       | Size          | Description               |
    +===============+===============+===========================+
    | total length  | 2 bytes       | Big endian 16-bit value   |
    |               |               | representing total length |
    |               |               | of body + 2 bytes for     |
    |               |               | CRC16; note that size of  |
    |               |               | total length field is not |
    |               |               | added to total length     |
    |               |               | value.                    |
    +---------------+---------------+---------------------------+
    | body          | no more than  | Raw body data fragment    |
    |               | MTU - 5       |                           |
    +---------------+---------------+---------------------------+

Initial-final frame 格式类似 initial frame 格式（
但以 ``<base64-i>`` 定义不同。

Initial-final frame 的 ``<base64-i>`` 为取
以下形式的 Base64 编码
data：

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | Content       | Size          | Description               |
    +===============+===============+===========================+
    | total length  | 2 bytes       | Big endian 16-bit value   |
    |               |               | representing total length |
    |               |               | of body + 2 bytes for     |
    |               |               | CRC16; note that size of  |
    |               |               | total length field is not |
    |               |               | added to total length     |
    |               |               | value.                    |
    +---------------+---------------+---------------------------+
    | body          | no more than  | Raw body data fragment    |
    |               | MTU - 7       |                           |
    +---------------+---------------+---------------------------+
    | crc16         | 2 bytes       | CRC16 of entire packet    |
    |               |               | body, preceding length    |
    |               |               | not included.             |
    +---------------+---------------+---------------------------+

Partial frame 为
preceding initial 或其他
partial
frame 后的
continuation。Partial frame 取
以下形式：

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | Content       | Size          | Description               |
    +===============+===============+===========================+
    | 0x04 0x14     | 2 bytes       | Frame start marker        |
    +---------------+---------------+---------------------------+
    | <base64-i>    | no more than  | Base64 encoded body       |
    |               | MTU - 3 bytes |                           |
    +---------------+---------------+---------------------------+
    | 0x0a          | 1 byte        | Frame termination         |
    +---------------+---------------+---------------------------+

Partial frame 的 ``<base64-i>`` 为
data 的 Base64 编码（取
以下形式：

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | Content       | Size          | Description               |
    +===============+===============+===========================+
    | body          | no more than  | Raw body data fragment    |
    |               | MTU - 3       |                           |
    +---------------+---------------+---------------------------+

Partial-final frame 的 ``<base64-i>`` 为
data 的 Base64 编码（取
以下形式：

.. table::
    :align: center

    +---------------+---------------+---------------------------+
    | Content       | Size          | Description               |
    +===============+===============+===========================+
    | body          | no more than  | Raw body data fragment    |
    |               | MTU - 5       |                           |
    +---------------+---------------+---------------------------+
    | crc16         | 2 bytes       | CRC16 of entire packet    |
    |               |               | body, preceding length    |
    |               |               | not included.             |
    +---------------+---------------+---------------------------+


CRC Details
-----------

Final 类型 frames 中包含的
CRC16 仅对
raw data 计算（不包含
packet length。
CRC16 多项式为 0x1021（初始值为 0。

.. _mcumgr_smp_transport_raw_uart:

Raw UART/serial (without console)
*********************************

在 Zephyr 中（UART 有
可用替代
transport（其不用
Base64（而 SMP
over console transport 用（这允许
更小 code size 和更快
transfers - 但
不能用于在同一 UART 上有
shell 或 log output 的
devices（或连接到
显示 ASCII data 的
terminals（因为所有
communication 均用
raw binary
SMP protocol 进行。

要用此 protocol（用 :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_RAW_UART`（其需
MCUmgr UART console driver 以
raw mode 启用。

Timeout
=======

由于用此
transport 时无
framing（UART 上可能
接收到
invalid
data（使
system 等待（如
永不
到达的
非常
长
packet。为防止此（有
timeout
system（若
特定
timeframe 内
未
接收
完整
packet（整个
receive
buffer 被
清除。建议
UART ports 上
启用
此
option（对
USB CDC 等
"virtual"
UART 的
transports（data 在
传递
前可
验证（此
option 不
需要。此
option 可用
:kconfig:option:`CONFIG_MCUMGR_TRANSPORT_RAW_UART_INPUT_TIMEOUT` 启用（其
timeout 可用
:kconfig:option:`CONFIG_MCUMGR_TRANSPORT_RAW_UART_INPUT_TIMEOUT_TIME_MS` 设置。

API Reference
*************

.. doxygengroup:: mcumgr_transport_smp
