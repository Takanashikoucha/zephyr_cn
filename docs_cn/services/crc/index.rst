.. _crc:

CRC
###

Overview
********

CRC
subsystem
provide
各种
Cyclic
Redundancy
Check
algorithms
的
software
implementations
用于
data
integrity
verification。
CRCs
通常
被
used
用于
detect
storage
和
communication
systems
中
data
的
accidental
changes。

Subsystem
offer
一
个
comprehensive
的
CRC
algorithms
set
包括
CRC-4、
CRC-7、
CRC-8、
CRC-16、
CRC-24、
和
CRC-32
variants
并
在
available
时
provide
optional
的
hardware
acceleration
support。

.. note::
   这
   个
   library
   与
   :ref:`CRC
   hardware
   driver
   API
   <crc_api>`
   distinct
   它
   provide
   一
   个
   interface
   到
   hardware
   CRC
   acceleration
   peripherals。

   当
   hardware
   CRC
   unit
   available
   且
   ``zephyr,crc``
   property
   在
   Devicetree
   的
   ``/chosen``
   node
   中
   被
   set
   时
   library
   functions
   default
   下
   将
   use
   hardware
   acceleration
   用于
   improved
   performance
   （可以
   通过
   set
   :kconfig:option:`CONFIG_CRC_HW_HANDLER`
   到
   ``n``
   被
   disabled）。

Usage
=====

要
compute
一
个
CRC
include
appropriate
的
header
并
call
desired
的
function：

.. code-block::
   c

   #include
   <zephyr/sys/crc.h>

   uint8_t
   data[]
   =
   {0x01,
   0x02,
   0x03,
   0x04};
   uint32_t
   checksum
   =
   crc32_ieee(data,
   sizeof(data));

对于
在
chunks
中
processed
的
streaming
data
use
"update"
variants：

.. code-block::
   c
