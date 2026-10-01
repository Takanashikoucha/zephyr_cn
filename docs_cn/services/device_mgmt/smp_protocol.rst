.. _mcumgr_smp_protocol_specification:

SMP Protocol Specification
##########################

此为 Simple Management Protocol (SMP) 的描述（
MCUmgr 用其向 devices 传递
requests 并接收 responses。

SMP 为 application layer protocol。底层
transport layer 不在此
documentation 范围内。

.. note::
    此语境中的 SMP 指 MCUmgr 的 SMP (Simple Management Protocol)（
    与 Bluetooth 中的 SMP (Security Manager Protocol) 无关（但
    有用于 Bluetooth 的 MCUmgr SMP transport。

Frame: The envelope
*******************

每个 frame 由 header 和 data 组成。Header 中的
``Data Length`` field 若底层
transport layer 支持
fragmentation 可用于 reassembly 目的。
Fields 超过
一个 byte 长时（frames 以 "Big Endian" (Network endianness) 编码（并
取以下形式：

.. _mcumgr_smp_protocol_frame:

.. table::
    :align: center

    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |3              |2              |1              |0              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |7|6|5|4|3|2|1|0|7|6|5|4|3|2|1|0|7|6|5|4|3|2|1|0|7|6|5|4|3|2|1|0|
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | Res |Ver| OP  |      Flags    |          Data Length          |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |            Group ID           | Sequence Num  |   Command ID  |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                             Data                              |
    |                             ...                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

.. note::
    原始 specification 声明 SMP 应支持接收
    "Little-endian" 和 "Big-endian" frames（但实际
    MCUmgr library 硬编码为始终将 "Network" 侧视为
    "Big-endian"。


Data 可选（且 ``Data Length`` 为零时不存在。
Data 的编码取决于
group/ID 的 target。

各 fields 及其含义的描述：

.. table::
    :align: center

    +-------------------+---------------------------------------------------+
    | Field             | Description                                       |
    +===================+===================================================+
    | ``Res``           | This is reserved, not-used field and must be      |
    |                   | always set to 0.                                  |
    +-------------------+---------------------------------------------------+
    | ``Ver`` (Version) | This indicates the version of the protocol being  |
    |                   | used, this should be set to 0b01 to use the newer |
    |                   | SMP transport where error codes are more detailed |
    |                   | and returned in the map, otherwise left as 0b00   |
    |                   | to use the legacy SMP protocol. Versions 0b10 and |
    |                   | 0b11 are reserved for future use and should not   |
    |                   | be used.                                          |
    +-------------------+---------------------------------------------------+
    | ``OP``            | :c:enum:`mcumgr_op_t`, determines whether         |
    |                   | information is written to a device or requested   |
    |                   | from it and whether a packet contains request to  |
    |                   | an SMP server or response from it.                |
    +-------------------+---------------------------------------------------+
    | ``Flags``         | Reserved for flags; there are no flags defined    |
    |                   | yet, the field should be set to 0                 |
    +-------------------+---------------------------------------------------+
    | ``Data Length``   | Length of the ``Data`` field                      |
    +-------------------+---------------------------------------------------+
    | ``Group ID``      | :c:enum:`mcumgr_group_t`, see                     |
    |                   | :ref:`mcumgr_smp_protocol_group_ids` for further  |
    |                   | details.                                          |
    +-------------------+---------------------------------------------------+
    | ``Sequence Num``  | This is a frame sequence number.                  |
    |                   | The number is increased by one with each request  |
    |                   | frame.                                            |
    |                   | The Sequence Num of a response should match       |
    |                   | the one in the request.                           |
    +-------------------+---------------------------------------------------+
    | ``Command ID``    | This is a command, within ``Group``.              |
    +-------------------+---------------------------------------------------+
    | ``Data``          | This is data payload of the ``Data Length``       |
    |                   | size. It is optional as ``Data Length`` may be    |
    |                   | set to zero, which means that no data follows     |
    |                   | the header.                                       |
    +-------------------+---------------------------------------------------+

.. note::
    ``Data`` 的内容取决于 ``OP``、``Group ID``
    和 ``Command ID`` 的值。

.. _mcumgr_smp_protocol_group_ids:

Management ``Group ID``'s
=========================

SMP protocol 支持预定义 common groups（并允许
user defined
groups。以下表格列出
common groups 的列表：


.. table::
    :align: center

    +---------------+-----------------------------------------------+
    | Decimal ID    | Group description                             |
    +===============+===============================================+
    | ``0``         | :ref:`mcumgr_smp_group_0`                     |
    +---------------+-----------------------------------------------+
    | ``1``         | :ref:`mcumgr_smp_group_1`                     |
    +---------------+-----------------------------------------------+
    | ``2``         | :ref:`mcumgr_smp_group_2`                     |
    +---------------+-----------------------------------------------+
    | ``3``         | :ref:`mcumgr_smp_group_3`                     |
    +---------------+-----------------------------------------------+
    | ``4``         | Application/system log management             |
    |               | (currently not used by Zephyr)                |
    +---------------+-----------------------------------------------+
    | ``5``         | Run-time tests                                |
    |               | (unused by Zephyr)                            |
    +---------------+-----------------------------------------------+
    | ``6``         | Split image management                        |
    |               | (unused by Zephyr)                            |
    +---------------+-----------------------------------------------+
    | ``7``         | Test crashing application                     |
    |               | (unused by Zephyr)                            |
    +---------------+-----------------------------------------------+
    | ``8``         | :ref:`mcumgr_smp_group_8`                     |
    +---------------+-----------------------------------------------+
    | ``9``         | :ref:`mcumgr_smp_group_9`                     |
    +---------------+-----------------------------------------------+
    | ``63``        | :ref:`mcumgr_smp_group_63`                    |
    +---------------+-----------------------------------------------+
    | ``64``        | This is the base group for defining           |
    |               | an application specific management groups.    |
    +---------------+-----------------------------------------------+

上述 groups 的 payload（user groups（``64`` 及以上）除外）
始终 CBOR 编码。Group
``64`` 及以上可定义自己的
data communication scheme。

Minimal response
****************

无论发出何种 command（只要
request 的另一侧有 SMP client（就应发出
response（包含
header 后跟 CBOR map container。
仅在无 SMP service 或
device 无响应时允许
response 缺失。

Minimal response SMP data
=========================

Minimal response 为：

.. tabs::

   .. group-tab:: SMP version 2

      .. code-block:: none

          {
              (str)"err" : {
                  (str)"group"    : (uint)
                  (str)"rc"       : (uint)
              }
          }

   .. group-tab:: SMP version 1 (and non-group SMP version 2)

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

其中：

.. table::
    :align: center

    +------------------+-------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` group of the group-based error code. Only      |
    |                  | appears if an error is returned when using SMP version 2.               |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if       |
    |                  | non-zero (error condition) when using SMP version 2.                    |
    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when  |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.         |
    +------------------+-------------------------------------------------------------------------+

注意成功 command 时返回空 map（``rc``/``err``
仅在
error condition 时返回（因此若仅返回空 map 或
response 缺少这些（request 可视为成功。对 SMP version 2（
与 SMP 本身相关且非
group specific 的 errors 仍以 ``rc``
errors 返回（故 SMP version 2 clients 须
能处理两种类型的 errors。

Specifications of management groups supported by Zephyr
*******************************************************

.. toctree::
    :maxdepth: 1

    smp_groups/smp_group_0.rst
    smp_groups/smp_group_1.rst
    smp_groups/smp_group_2.rst
    smp_groups/smp_group_3.rst
    smp_groups/smp_group_8.rst
    smp_groups/smp_group_9.rst
    smp_groups/smp_group_10.rst
    smp_groups/smp_group_11.rst
    smp_groups/smp_group_63.rst
