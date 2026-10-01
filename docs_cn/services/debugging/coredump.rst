.. _coredump:

Core Dump
#########

Core dump module 启用 dump CPU registers 和 memory content
用于离线调试。此 module 在遇到 fatal error 时调用（并按启用
backends 打印或存储 data。

Configuration
*************

用以下 options 配置此 module。

* ``DEBUG_COREDUMP``: 启用 module。

启用 core dump 输出 backends 的 options：

* ``DEBUG_COREDUMP_BACKEND_LOGGING``: 用 log module 作为 core dump 输出。
* ``DEBUG_COREDUMP_BACKEND_LOGGING_UDP``: 与 logging backend 相同但带可选
  raw UDP transfer；peer 为 ``DEBUG_COREDUMP_LOGGING_UDP_HOST``（由 ``net_ipaddr_parse()`` 解析的 string
  （IPv4 或 IPv6（可选 ``:port``（省略时默认
  UDP port ``17777``）。用
  :zephyr_file:`scripts/coredump/coredump_udp_receiver.py` 构建
  :zephyr_file:`scripts/coredump/coredump_gdbserver.py` 的
  binary。
* ``DEBUG_COREDUMP_BACKEND_FLASH_PARTITION``: 用 flash partition 作为 core
  dump 输出。
* ``DEBUG_COREDUMP_BACKEND_NULL``: 其他
  backends 不能启用时的 fallback core dump backend。所有输出发送到 null。

memory dump 的 choices：

* ``DEBUG_COREDUMP_MEMORY_DUMP_MIN``: 仅 dump exception
  thread 的 stack、其 thread struct 和其他支持
  在 debugger 中 walk stack 的 bare minimal data。仅在
  期望绝对最小 data
  dump 时使用。

* ``DEBUG_COREDUMP_MEMORY_DUMP_THREADS``: Dump 所有
  threads 的 thread struct 和 stack 以及调试 threads 所需所有 data。

* ``DEBUG_COREDUMP_MEMORY_DUMP_LINKER_RAM``: Dump
  _image_ram_start[] 和 _image_ram_end[] 间的 memory region。这至少包括 data、noinit、
  和 BSS sections。此为默认。

额外 memory 可被包含在 dump 中（即使选择
"DEBUG_COREDUMP_MEMORY_DUMP_MIN"
config）（通过一个或多个 :ref:`coredump devices <coredump_device_api>`

Usage
*****

启用 core dump module 时（fatal error 期间（CPU registers
和 memory content 按启用
backends 打印或存储。此 core dump data 可输入
自制 GDB server 作为 GDB（及其他 GDB compatible debuggers）的 remote target。CPU registers、
memory content 和 stack 可在 debugger 中检查。

这通常涉及以下步骤：

1. 按启用 backends 从 device 获取 core dump log。
   例如（若用 log module backend（从
   log module backend 获取 log 输出。

2. 将 core dump log 转为 GDB server 可解析的
   binary 格式。例如（
   :zephyr_file:`scripts/coredump/coredump_serial_log_parser.py` 可用于
   将 serial console log 转为 binary file。
   若启用 UDP coredump backend
   （``DEBUG_COREDUMP_BACKEND_LOGGING_UDP``）（在
   collector
   host 上运行 :zephyr_file:`scripts/coredump/coredump_udp_receiver.py` 将 UDP datagrams 重组为 **相同** raw binary 格式。

3. 用 core dump
   binary log file 和 Zephyr ELF file 作为 parameters 用 script
   :zephyr_file:`scripts/coredump/coredump_gdbserver.py` 启动
   自定义 GDB server。GDB server
   也可从 GDB 内部启动（见下文。

4. 启动与 target architecture 对应的 debugger。

.. note::
   使用
   ``ZEPHYR_TOOLCHAIN_VARIANT=zephyr`` 的 Intel ADSP CAVS 15-25 platforms 的 Developers
   应使用 SDK 的
   ``xtensa-intel_apl_adsp`` toolchain 中的 debugger。

5. 启用 ``DEBUG_COREDUMP_BACKEND_FLASH_PARTITION`` 时（core dump
   data 存储在 flash partition 中。Flash partition 须
   在 device tree 中定义：

   .. code-block:: devicetree

      &flash0 {
         partitions {
            coredump_partition: partition@255000 {
               label = "coredump-partition";
               reg = <0x255000 DT_SIZE_K(4)>;
            };
         };
      };

Example
-------

此示例用绑定 serial console 的 log module backend。
这在 :zephyr:board:`qemu_x86` 上完成（其中 null pointer 被 dereferenced。

此为 serial console 的 core dump log（存储
在 :file:`coredump.log`：

::

   Booting from ROM..*** Booting Zephyr OS build zephyr-v2.3.0-1840-g7bba91944a63  ***
   Hello World! qemu_x86
   E: Page fault at address 0x0 (error code 0x2)
   E: Linear address not present in page tables
   E:   PDE: 0x0000000000115827 Writable, User, Execute Enabled
   E:   PTE: Non-present
   E: EAX: 0x00000000, EBX: 0x00000000, ECX: 0x00119d74, EDX: 0x000003f8
   E: ESI: 0x00000000, EDI: 0x00101aa7, EBP: 0x00119d10, ESP: 0x00119d00
   E: EFLAGS: 0x00000206 CS: 0x0008 CR3: 0x00119000
   E: call trace:
   E: EIP: 0x00100459
   E:      0x00100477 (0x0)
   E:      0x00100492 (0x0)
   E:      0x001004c8 (0x0)
   E:      0x00105465 (0x105465)
   E:      0x00101abe (0x0)
   E: >>> ZEPHYR FATAL ERROR 0: CPU exception on CPU 0
   E: Current thread: 0x00119080 (unknown)
   E: #CD:BEGIN#
   E: #CD:5a4501000100050000000000
   E: #CD:4101003800
   E: #CD:0e0000000200000000000000749d1100f803000000000000009d1100109d1100
   E: #CD:00000000a71a100059041000060200000800000000901100
   E: #CD:4d010080901100e0901100
   E: #CD:010000000000000000000000018000000000000000000000000000000000000
   E: #CD:00000000000000000000000000000000e364100000000000000000004c9c1100
   E: #CD:000000000000000000000000b49911000004000000000000fc03000000000000
   E: #CD:4d0100b4991100b49d1100
   E: #CD:f8030000020000000200000002000000f8030000fd03000a02000000dc9e1100
   E: #CD:149a1160fd03000002000000dc9e1100249a110087201000049f11000a000000
   E: #CD:349a11000a4f1000049f11000a9e1100449a11000a8b10000200000002000000
   E: #CD:449a1100388b1000049f11000a000000549a1100ad201000049f11000a000000
   E: #CD:749a11000a201000049f11000a000000649a11000a201000049f11000a000000
   E: #CD:749a1100e8201000049f11000a000000949a1100890b10000a0000000a000000
   E: #CD:a49a1100890b10000a0000000a000000f8030000189b11000200000002000000
   E: #CD:f49a1100289b11000a000000189b1100049b11009b0710000a000000289b1100
   E: #CD:f49a110087201000049f110045000000f49a1100509011000a00000020901100
   E: #CD:f49a110060901100049f1100ffffffff0000000000000000049f1100ffffffff
   E: #CD:0000000000000000630b1000189b1100349b1100af0b1000630b1000289b1100
   E: #CD:55891000789b11000000000020901100549b1100480000004a891000609b1100
   E: #CD:649b1100d00b10004a891000709b110000000000609b11000a00000000000000
   E: #CD:849b1100709b11004a89100000000000949b1100794a10000000000058901100
   E: #CD:20901100c34a10000a00001734020000d001000000000000d49b110038000000
   E: #CD:c49b110078481000b49911000004000000000000000000000c9c11000c9c1100
   E: #CD:149c110000000000d49b110038000000f49b1100da481000b499110000040000
   E: #CD:0e0000000200000000000000744d0100b4991100b49d1100009d1100109d1100
   E: #CD:149c110099471000b4991100000400000800000000901100ad861000409c1100
   E: #CD:349c1100e94710008090110000000000349c1100b64710008086100045000000
   E: #CD:849c11002d53100000000000d09c11008090110020861000f5ffffff8c9c1100
   E: #CD:000000000000000000000000a71a1000a49c1100020200008090110000000000
   E: #CD:a49c1100020200000800000000000000a49c11001937100000000000d09c1100
   E: #CD:0c9d0000bc9c0000b49d1100b4991100c49c1100ae37100000000000d09c1100
   E: #CD:0800000000000000c888100000000000109d11005d031000d09c1100009d1100
   E: #CD:109d11000000000000000000a71a1000f803000000000000749d110002000000
   E: #CD:5904100008000000060200000e0000000202000002020000000000002c9d1100
   E: #CD:7704100000000000d00b1000c9881000549d110000000000489d110092041000
   E: #CD:00000000689d1100549d11000000000000000000689d1100c804100000000000
   E: #CD:c0881000000000007c9d110000000000749d11007c9d11006554100065541000
   E: #CD:00000000000000009c9d1100be1a100000000000000000000000000038041000
   E: #CD:08000000020200000000000000000000f4531000000000000000000000000000
   E: #CD:END#
   E: Halting system


1. 运行 core dump serial log converter：

   .. code-block:: console

      ./scripts/coredump/coredump_serial_log_parser.py coredump.log coredump.bin

2. 启动自定义 GDB server：

   .. code-block:: console

      ./scripts/coredump/coredump_gdbserver.py build/zephyr/zephyr.elf coredump.bin

3. 启动 GDB：

   .. code-block:: console

      <path to SDK>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb build/zephyr/zephyr.elf

4. GDB 内部（通过 port 1234 连接 GDB server：

   .. code-block:: console

      (gdb) target remote localhost:1234

5. 检查 CPU registers：

   .. code-block:: console

      (gdb) info registers

   GDB 输出：

   ::

      eax            0x0                 0
      ecx            0x119d74            1154420
      edx            0x3f8               1016
      ebx            0x0                 0
      esp            0x119d00            0x119d00 <z_main_stack+844>
      ebp            0x119d10            0x119d10 <z_main_stack+860>
      esi            0x0                 0
      edi            0x101aa7            1055399
      eip            0x100459            0x100459 <func_3+16>
      eflags         0x206               [ PF IF ]
      cs             0x8                 8
      ss             <unavailable>
      ds             <unavailable>
      es             <unavailable>
      fs             <unavailable>
      gs             <unavailable>

6. 检查 backtrace：

   .. code-block:: console

      (gdb) bt


   GDB 输出：

   ::

      #0  0x00100459 in func_3 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:14
      #1  0x00100477 in func_2 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:21
      #2  0x00100492 in func_1 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:28
      #3  0x001004c8 in main () at zephyr/rtos/zephyr/samples/hello_world/src/main.c:42

Starting the GDB server from within GDB
---------------------------------------

可用 ``target remote |`` 从 GDB 内部启动
自定义 GDB server（而非在单独 shell 中。

1. 启动 GDB：

   .. code-block:: console

      <path to SDK>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb build/zephyr/zephyr.elf

2. GDB 内部（用 ``--pipe`` option 启动 GDB server：

   .. code-block:: console

      (gdb) target remote | ./scripts/coredump/coredump_gdbserver.py --pipe build/zephyr/zephyr.elf coredump.bin


File Format
***********

Core dump binary file 由一个 file header、一个
architecture-specific block、零或一个 threads metadata block(s)
和多个 memory blocks 组成。以下
headers 中所有数字为 little endian。

File Header
-----------

File header 由以下 fields 组成：

.. list-table:: Core dump binary file header
   :widths: 2 1 7
   :header-rows: 1

   * - Field
     - Data Type
     - Description
   * - ID
     - ``char[2]``
     - ``Z``、``E`` 作为 file 的 identifier。
   * - Header version
     - ``uint16_t``
     - 标识 header 的 version。每次修改
       header struct 时须递增。这允许 parser
       拒绝较旧 header versions（从而不会错误解析
       header。
   * - Target code
     - ``uint16_t``
     - 指示哪个 target（如 architecture 或 SoC）（使 parser
       可实例化正确 register block parser。
   * - Pointer size
     - 'uint8_t'
     - ``uintptr_t`` 的 size（2 的幂。（如 32-bit 为 5、
       64-bit 为 6。解析 memory block addresses 时需兼容 32-bit 和 64-bit
       target。
   * - Flags
     - ``uint8_t``
     -
   * - Fatal error reason
     - ``unsigned int``
     - Fatal error 的原因（与
       :zephyr_file:`include/zephyr/fatal.h` 中定义的
       ``enum k_fatal_error_reason`` 相同

Architecture-specific Block
---------------------------

Architecture-specific block 包含特定
于 target architecture（如 CPU registers）的 data byte stream

.. list-table:: Architecture-specific Block
   :widths: 2 1 7
   :header-rows: 1

   * - Field
     - Data Type
     - Description
   * - ID
     - ``char``
     - ``A`` 表示此为 architecture-specific block。
   * - Header version
     - ``uint16_t``
     - 标识此 block 的 version。由 target
       architecture specific block parser 解释。
   * - Number of bytes
     - ``uint16_t``
     - Header 后包含 target data byte stream
       的 byte 数量。Byte stream 的格式特定于
       target（且仅由 target parser 解析。
   * - Register byte stream
     - ``uint8_t[]``
     - 包含 target architecture 特定 data。

Threads Metadata Block
---------------------------

Threads metadata block 包含
调试 threads 所需 data 的 byte stream。

.. list-table:: Threads Metadata Block
   :widths: 2 1 7
   :header-rows: 1

   * - Field
     - Data Type
     - Description
   * - ID
     - ``char``
     - ``T`` 表示此为 threads metadata block。
   * - Header version
     - ``uint16_t``
     - 标识 header 的 version。每次修改
       header struct 时须递增。这允许 parser
       拒绝较旧 header versions（从而不会错误解析
       header。
   * - Number of bytes
     - ``uint16_t``
     - Header 后包含 target data byte stream
       的 byte 数量。
   * - Byte stream
     - ``uint8_t[]``
     - 包含调试 threads 所需 data。

Memory Block
------------

Memory block 包含
memory region 的 start 和 end addresses 以及
其中的 data。

.. list-table:: Memory Block
   :widths: 2 1 7
   :header-rows: 1

   * - Field
     - Data Type
     - Description
   * - ID
     - ``char``
     - ``M`` 表示此为 memory block。
   * - Header version
     - ``uint16_t``
     - 标识 header 的 version。每次修改
       header struct 时须递增。这允许 parser
       拒绝较旧 header versions（从而不会错误解析
       header。
   * - Start address
     - ``uintptr_t``
     - Memory region 的 start address。
   * - End address
     - ``uintptr_t``
     - Memory region 的 end address。
   * - Memory byte stream
     - ``uint8_t[]``
     - 包含 start 和 end addresses 间的 memory content。

Adding New Target
*****************

Architecture-specific block 为 target specific（且新
targets 需新
dumping routine 和 parser。添加新 target 须做以下：

#. 在
   :zephyr_file:`include/zephyr/debug/coredump.h` 的
   ``enum coredump_tgt_code`` 中添加新 target code。
#. 简单返回
   新引入 target code 地实现 :c:func:`arch_coredump_tgt_code_get`。
#. 实现 :c:func:`arch_coredump_info_dump` 构建
   target architecture block（并调用 :c:func:`coredump_buffer_output`
   将 block 输出到 core dump backend。
#. 在 ``scripts/coredump/gdbstubs/`` 下的 core dump GDB stub scripts
   中添加 parser

   #. 扩展 ``gdbstubs.gdbstub.GdbStub`` class。
   #. ``__init__`` 期间（将对应
      exception reason 的 GDB signal 存储在 ``self.gdb_signal``。
   #. 从
      ``self.logfile.get_arch_data()`` 解析 architecture-specific block。须与
      step 3（在 :c:func:`arch_coredump_info_dump` 内）实现的格式
      匹配。
   #. 实现 abstract method ``handle_register_group_read_packet``
      （其按 GDB 期望返回 register group。参见
      GDB 的 code 和 documentation 了解其对
      新 target 的期望。
   #. 可选实现 ``handle_register_single_read_packet``
      用于 ``g`` packet 未覆盖的 registers。

#. 扩展
   :zephyr_file:`scripts/coredump/gdbstubs/__init__.py` 的 ``get_gdbstub()`` 以返回
   新实现的 GDB stub。

UDP logging backend sample
**************************

测试 UDP coredump path 的 Sample README pages 链接到此章节（使 Sphinx
将其包含在 documentation tree 中：

.. toctree::
   :maxdepth: 1
   :hidden:

   ../../samples/subsys/debug/coredump_udp_demos/demo_shell/README

API documentation
*****************

.. doxygengroup:: coredump_apis

.. doxygengroup:: arch-coredump
