.. _coredump:

Core
Dump
#########

Core
dump
module
enable
dump
CPU
registers
和
memory
content
用于
offline
debugging。
这
个
module
在
encounter
一
个
fatal
error
时
被
called
并
根据
哪些
backends
被
enabled
print
或
store
data。

Configuration
*************

用
以下
options
configure
这
个
module。

*
``DEBUG_COREDUMP``：
enable
这
个
module。

以下
是
enable
core
dump
的
output
backends
的
options：

*
``DEBUG_COREDUMP_BACKEND_LOGGING``：
use
log
module
用于
core
dump
output。
*
``DEBUG_COREDUMP_BACKEND_LOGGING_UDP``：
与
logging
backend
相同
带
optional
的
raw
UDP
transfer
peer
是
``DEBUG_COREDUMP_LOGGING_UDP_HOST``
一
个
被
``net_ipaddr_parse()``
parsed
的
string
（IPv4
或
IPv6
optional
的
``:port``
当
omitted
时
default
的
UDP
port
是
``17777``）。
用
:zephyr_file:`scripts/coredump/coredump_udp_receiver.py`
build
:zephyr_file:`scripts/coredump/coredump_gdbserver.py`
的
binary。
*
``DEBUG_COREDUMP_BACKEND_FLASH_PARTITION``：
use
flash
partition
用于
core
dump
output。
*
``DEBUG_COREDUMP_BACKEND_NULL``：
fallback
的
core
dump
backend
如果
其他
backends
不
能
被
enabled。
所有
的
output
被
sent
到
null。

以下
是
关于
memory
dump
的
choices：

*
``DEBUG_COREDUMP_MEMORY_DUMP_MIN``：
只
dump
exception
thread
的
stack、
它
的
thread
struct、
和
其他
几
个
bare
minimal
的
data
用于
support
在
debugger
中
walk
stack。
只
在
希望
absolute
minimal
的
data
dump
时
use
这
个。

*
``DEBUG_COREDUMP_MEMORY_DUMP_THREADS``：
Dump
所有
threads
的
thread
struct
和
stack
以及
debug
threads
所需
的
所有
data。


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
   .. code-block:: console

      (gdb) bt


   Output from GDB:

   ::

      #0  0x00100459 in func_3 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:14
      #1  0x00100477 in func_2 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:21
      #2  0x00100492 in func_1 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:28
      #3  0x001004c8 in main () at zephyr/rtos/zephyr/samples/hello_world/src/main.c:42

Starting the GDB server from within GDB
---------------------------------------

You can use ``target remote |`` to start the custom GDB server from inside
GDB, instead of in a separate shell.

1. Start GDB:

   .. code-block:: console

      <path to SDK>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb build/zephyr/zephyr.elf

2. Inside GDB, start the GDB server using the ``--pipe`` option:

   .. code-block:: console

      (gdb) target remote | ./scripts/coredump/coredump_gdbserver.py --pipe build/zephyr/zephyr.elf coredump.bin


File Format
***********

The core dump binary file consists of one file header, one
architecture-specific block, zero or one threads metadata block(s),
and multiple memory blocks. All numbers in
the headers below are little endian.

File Header
-----------

The file header consists of the following fields:

.. list-table:: Core dump binary file header
   :widths: 2 1 7
   :header-rows: 1

   * - Field
     - Data Type
     - Description
   * - ID
     - ``char[2]``
     - ``Z``, ``E`` as identifier of file.
   * - Header version
     - ``uint16_t``
     - Identify the version of the header. This needs to be incremented
       whenever the header struct is modified. This allows parser to
       reject older header versions so it will not incorrectly parse
       the header.
   * - Target code
     - ``uint16_t``
     - Indicate which target (e.g. architecture or SoC) so the parser
       can instantiate the correct register block parser.
   * - Pointer size
     - 'uint8_t'
     - Size of ``uintptr_t`` in power of 2. (e.g. 5 for 32-bit,
       6 for 64-bit). This is needed to accommodate 32-bit and 64-bit
       target in parsing the memory block addresses.
   * - Flags
     - ``uint8_t``
     -
   * - Fatal error reason
     - ``unsigned int``
     - Reason for the fatal error, as the same in
       ``enum k_fatal_error_reason`` defined in
       :zephyr_file:`include/zephyr/fatal.h`

Architecture-specific Block
---------------------------

The architecture-specific block contains the byte stream of data specific
to the target architecture (e.g. CPU registers)

.. list-table:: Architecture-specific Block
   :widths: 2 1 7
   :header-rows: 1

   * - Field
     - Data Type
     - Description
   * - ID
     - ``char``
     - ``A`` to indicate this is a architecture-specific block.
   * - Header version
     - ``uint16_t``
     - Identify the version of this block. To be interpreted by the target
       architecture specific block parser.
   * - Number of bytes
     - ``uint16_t``
     - Number of bytes following the header which contains the byte stream
       for target data. The format of the byte stream is specific to
       the target and is only being parsed by the target parser.
   * - Register byte stream
     - ``uint8_t[]``
     - Contains target architecture specific data.

Threads Metadata Block
---------------------------

The threads metadata block contains the byte stream of data necessary
for debugging threads.

.. list-table:: Threads Metadata Block
   :widths: 2 1 7
   :header-rows: 1

   * - Field
     - Data Type
     - Description
   * - ID
     - ``char``
     - ``T`` to indicate this is a threads metadata block.
   * - Header version
     - ``uint16_t``
     - Identify the version of the header. This needs to be incremented
       whenever the header struct is modified. This allows parser to
       reject older header versions so it will not incorrectly parse
       the header.
   * - Number of bytes
     - ``uint16_t``
     - Number of bytes following the header which contains the byte stream
       for target data.
   * - Byte stream
     - ``uint8_t[]``
     - Contains data necessary for debugging threads.

Memory Block
------------

The memory block contains the start and end addresses and the data within
the memory region.

.. list-table:: Memory Block
   :widths: 2 1 7
   :header-rows: 1

   * - Field
     - Data Type
     - Description
   * - ID
     - ``char``
     - ``M`` to indicate this is a memory block.
   * - Header version
     - ``uint16_t``
     - Identify the version of the header. This needs to be incremented
       whenever the header struct is modified. This allows parser to
       reject older header versions so it will not incorrectly parse
       the header.
   * - Start address
     - ``uintptr_t``
     - The start address of the memory region.
   * - End address
     - ``uintptr_t``
     - The end address of the memory region.
   * - Memory byte stream
     - ``uint8_t[]``
     - Contains the memory content between the start and end addresses.

Adding New Target
*****************

The architecture-specific block is target specific and requires new
dumping routine and parser for new targets. To add a new target,
the following needs to be done:

#. Add a new target code to the ``enum coredump_tgt_code`` in
   :zephyr_file:`include/zephyr/debug/coredump.h`.
#. Implement :c:func:`arch_coredump_tgt_code_get` simply to return
   the newly introduced target code.
#. Implement :c:func:`arch_coredump_info_dump` to construct
   a target architecture block and call :c:func:`coredump_buffer_output`
   to output the block to core dump backend.
#. Add a parser to the core dump GDB stub scripts under
   ``scripts/coredump/gdbstubs/``

   #. Extends the ``gdbstubs.gdbstub.GdbStub`` class.
   #. During ``__init__``, store the GDB signal corresponding to
      the exception reason in ``self.gdb_signal``.
   #. Parse the architecture-specific block from
      ``self.logfile.get_arch_data()``. This needs to match the format
      as implemented in step 3 (inside :c:func:`arch_coredump_info_dump`).
   #. Implement the abstract method ``handle_register_group_read_packet``
      where it returns the register group as GDB expected. Refer to
      GDB's code and documentation on what it is expecting for
      the new target.
   #. Optionally implement ``handle_register_single_read_packet``
      for registers not covered in the ``g`` packet.

#. Extend ``get_gdbstub()`` in
   :zephyr_file:`scripts/coredump/gdbstubs/__init__.py` to return
   the newly implemented GDB stub.

UDP logging backend sample
**************************

Sample README pages that exercise the UDP coredump path are linked into this chapter so Sphinx
includes them in the documentation tree:

.. toctree::
   :maxdepth: 1
   :hidden:

   ../../samples/subsys/debug/coredump_udp_demos/demo_shell/README

API documentation
*****************

.. doxygengroup:: coredump_apis

.. doxygengroup:: arch-coredump