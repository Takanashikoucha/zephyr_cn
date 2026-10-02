.. _coredump:

Core Dump
#########

core dump 模块支持转储 CPU 寄存器和内存内容，用于离线调试。当遇到致命错误时会调用该模块，并根据启用的后端打印或存储数据。

配置
*************

使用以下选项配置该模块。

* ``DEBUG_COREDUMP``：启用该模块。

启用 core dump 输出后端的选项：

* ``DEBUG_COREDUMP_BACKEND_LOGGING``：使用日志模块（log module）作为 core dump 输出。
* ``DEBUG_COREDUMP_BACKEND_LOGGING_UDP``：与 logging 后端相同，但支持可选的
  原始 UDP 传输；对端为 ``DEBUG_COREDUMP_LOGGING_UDP_HOST``，一个由 ``net_ipaddr_parse()`` 解析的字符串
  （IPv4 或 IPv6，可选 ``:port``，省略时默认
  UDP 端口 ``17777``）。使用
  :zephyr_file:`scripts/coredump/coredump_udp_receiver.py` 构建
  :zephyr_file:`scripts/coredump/coredump_gdbserver.py` 的二进制文件。
* ``DEBUG_COREDUMP_BACKEND_FLASH_PARTITION``：使用 flash 分区作为 core
  dump 输出。
* ``DEBUG_COREDUMP_BACKEND_NULL``：其他
  后端无法启用时的备用 core dump 后端。所有输出均发送到 null。

关于内存转储的选项：

* ``DEBUG_COREDUMP_MEMORY_DUMP_MIN``：仅转储异常
  线程的栈、其线程结构体以及其他用于在
  调试器中遍历栈的最小必要数据。仅在
  希望转储绝对最小数据
  量时使用。

* ``DEBUG_COREDUMP_MEMORY_DUMP_THREADS``：转储所有
  线程的线程结构体和栈，以及调试线程所需的所有数据。

* ``DEBUG_COREDUMP_MEMORY_DUMP_LINKER_RAM``：转储
  _image_ram_start[] 与 _image_ram_end[] 之间的内存区域。这至少包括 data、noinit、
  和 BSS 段。这是默认选项。

额外的内存可以通过一个或多个 :ref:`coredump 设备 <coredump_device_api>`
  包含在转储中（即使选择了
  "DEBUG_COREDUMP_MEMORY_DUMP_MIN"
  配置项）。

用法
*****

启用 core dump 模块后，发生致命错误时，CPU 寄存器
和内存内容会根据启用的
后端进行打印或存储。该 core dump 数据可以输入
自制的 GDB server，作为 GDB（及其他 GDB 兼容调试器）的远程目标。CPU 寄存器、
内存内容和栈都可以在调试器中检查。

这通常涉及以下步骤：

1. 根据启用的后端从设备获取 core dump 日志。
   例如，如果使用日志模块后端，则从
   日志模块后端获取日志输出。

2. 将 core dump 日志转换为 GDB server 可解析的
   二进制格式。例如，
   :zephyr_file:`scripts/coredump/coredump_serial_log_parser.py` 可用于
   将串口控制台日志转换为二进制文件。
   如果启用了 UDP coredump 后端
   （``DEBUG_COREDUMP_BACKEND_LOGGING_UDP``），在
   采集
   主机上运行 :zephyr_file:`scripts/coredump/coredump_udp_receiver.py` 将 UDP 数据报重组为 **相同的** 原始二进制格式。

3. 使用 core dump
   二进制日志文件和 Zephyr ELF 文件作为参数，通过脚本
   :zephyr_file:`scripts/coredump/coredump_gdbserver.py` 启动
   自定义 GDB server。GDB server
   也可以从 GDB 内部启动，见下文。

4. 启动与目标架构对应的调试器。

.. note::
   使用
   ``ZEPHYR_TOOLCHAIN_VARIANT=zephyr`` 的 Intel ADSP CAVS 15-25 平台的开发者
   应使用 SDK 的
   ``xtensa-intel_apl_adsp`` 工具链中的调试器。

5. 启用 ``DEBUG_COREDUMP_BACKEND_FLASH_PARTITION`` 时，core dump
   数据存储在 flash 分区中。flash 分区必须
   在设备树中定义：

   .. code-block:: devicetree

      &flash0 {
         partitions {
            coredump_partition: partition@255000 {
               label = "coredump-partition";
               reg = <0x255000 DT_SIZE_K(4)>;
            };
         };
      };

示例
-------

本示例使用绑定串口控制台的日志模块后端。
这是在 :zephyr:board:`qemu_x86` 上完成的，其中发生了一个空指针解引用。

以下是串口控制台的 core dump 日志，存储
在 :file:`coredump.log` 中：

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
   E: #CD:0100000000000000000000000180000000000000000000000000000000000000
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


1. 运行 core dump 串口日志转换工具：

   .. code-block:: console

      ./scripts/coredump/coredump_serial_log_parser.py coredump.log coredump.bin

2. 启动自定义 GDB server：

   .. code-block:: console

      ./scripts/coredump/coredump_gdbserver.py build/zephyr/zephyr.elf coredump.bin

3. 启动 GDB：

   .. code-block:: console

      <path to SDK>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb build/zephyr/zephyr.elf

4. 在 GDB 内部，通过端口 1234 连接 GDB server：

   .. code-block:: console

      (gdb) target remote localhost:1234

5. 检查 CPU 寄存器：

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

6. 检查回溯（backtrace）：

   .. code-block:: console

      (gdb) bt


   GDB 输出：

   ::

      #0  0x00100459 in func_3 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:14
      #1  0x00100477 in func_2 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:21
      #2  0x00100492 in func_1 (addr=0x0) at zephyr/rtos/zephyr/samples/hello_world/src/main.c:28
      #3  0x001004c8 in main () at zephyr/rtos/zephyr/samples/hello_world/src/main.c:42

从 GDB 内部启动 GDB server
---------------------------------------

可以使用 ``target remote |`` 从 GDB 内部启动
自定义 GDB server，而不是在单独的 shell 中启动。

1. 启动 GDB：

   .. code-block:: console

      <path to SDK>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb build/zephyr/zephyr.elf

2. 在 GDB 内部，使用 ``--pipe`` 选项启动 GDB server：

   .. code-block:: console

      (gdb) target remote | ./scripts/coredump/coredump_gdbserver.py --pipe build/zephyr/zephyr.elf coredump.bin


文件格式
***********

core dump 二进制文件由一个文件头、一个
架构相关块（architecture-specific block）、零个或一个线程元数据块（threads metadata block）
和多个内存块组成。以下
文件头中的所有数字均为小端序（little endian）。

文件头
-----------

文件头由以下字段组成：

.. list-table:: Core dump 二进制文件头
   :widths: 2 1 7
   :header-rows: 1

   * - 字段
     - 数据类型
     - 描述
   * - ID
     - ``char[2]``
     - ``Z``、``E``，作为文件的标识符。
   * - 头版本
     - ``uint16_t``
     - 标识文件头的版本。每次修改
       头结构体时须递增。这允许解析器
       拒绝较旧的头版本，从而不会错误地解析
       文件头。
   * - 目标代码
     - ``uint16_t``
     - 指示目标（如架构或 SoC），使解析器
       可以实例化正确的寄存器块解析器。
   * - 指针大小
     - 'uint8_t'
     - ``uintptr_t`` 的大小（以 2 的幂表示，例如 32 位为 5、
       64 位为 6）。解析内存块地址时需要兼容 32 位和 64 位
       目标。
   * - 标志
     - ``uint8_t``
     -
   * - 致命错误原因
     - ``unsigned int``
     - 致命错误的原因，与
       :zephyr_file:`include/zephyr/fatal.h` 中定义的
       ``enum k_fatal_error_reason`` 相同

架构相关块
---------------------------

架构相关块包含特定
于目标架构（如 CPU 寄存器）的数据字节流

.. list-table:: 架构相关块
   :widths: 2 1 7
   :header-rows: 1

   * - 字段
     - 数据类型
     - 描述
   * - ID
     - ``char``
     - ``A``，表示这是架构相关块。
   * - 头版本
     - ``uint16_t``
     - 标识此块的版本。由目标
       架构相关块解析器解释。
   * - 字节数
     - ``uint16_t``
     - 文件头之后包含目标数据字节流
       的字节数。字节流的格式特定于
       目标，且仅由目标解析器解析。
   * - 寄存器字节流
     - ``uint8_t[]``
     - 包含目标架构特定数据。

线程元数据块
---------------------------

线程元数据块包含
调试线程所需数据的字节流。

.. list-table:: 线程元数据块
   :widths: 2 1 7
   :header-rows: 1

   * - 字段
     - 数据类型
     - 描述
   * - ID
     - ``char``
     - ``T``，表示这是线程元数据块。
   * - 头版本
     - ``uint16_t``
     - 标识文件头的版本。每次修改
       头结构体时须递增。这允许解析器
       拒绝较旧的头版本，从而不会错误地解析
       文件头。
   * - 字节数
     - ``uint16_t``
     - 文件头之后包含目标数据字节流
       的字节数。
   * - 字节流
     - ``uint8_t[]``
     - 包含调试线程所需的数据。

内存块
------------

内存块包含
内存区域的起始地址和结束地址，以及
其中的数据。

.. list-table:: 内存块
   :widths: 2 1 7
   :header-rows: 1

   * - 字段
     - 数据类型
     - 描述
   * - ID
     - ``char``
     - ``M``，表示这是内存块。
   * - 头版本
     - ``uint16_t``
     - 标识文件头的版本。每次修改
       头结构体时须递增。这允许解析器
       拒绝较旧的头版本，从而不会错误地解析
       文件头。
   * - 起始地址
     - ``uintptr_t``
     - 内存区域的起始地址。
   * - 结束地址
     - ``uintptr_t``
     - 内存区域的结束地址。
   * - 内存字节流
     - ``uint8_t[]``
     - 包含起始地址和结束地址之间的内存内容。

添加新目标
*****************

架构相关块是目标特定的，新的
目标需要新的
转储例程和解析器。添加新目标需要执行以下操作：

#. 在
   :zephyr_file:`include/zephyr/debug/coredump.h` 的
   ``enum coredump_tgt_code`` 中添加新的目标代码。
#. 实现 :c:func:`arch_coredump_tgt_code_get`，简单地
   返回新引入的目标代码。
#. 实现 :c:func:`arch_coredump_info_dump`，构建
   目标架构块，并调用 :c:func:`coredump_buffer_output`
   将块输出到 core dump 后端。
#. 在 ``scripts/coredump/gdbstubs/`` 下的 core dump GDB stub 脚本
   中添加解析器

   #. 扩展 ``gdbstubs.gdbstub.GdbStub`` 类。
   #. 在 ``__init__`` 期间，将对应
      异常原因的 GDB 信号存储在 ``self.gdb_signal`` 中。
   #. 从
      ``self.logfile.get_arch_data()`` 解析架构相关块。其格式需要与
      第 3 步（在 :c:func:`arch_coredump_info_dump` 中）实现的格式
      匹配。
   #. 实现抽象方法 ``handle_register_group_read_packet``，
      按 GDB 期望返回寄存器组。参见
      GDB 的代码和文档，了解其对
      新目标的期望。
   #. 可选地实现 ``handle_register_single_read_packet``，
      用于 ``g`` 数据包未覆盖的寄存器。

#. 扩展
   :zephyr_file:`scripts/coredump/gdbstubs/__init__.py` 中的 ``get_gdbstub()``，以返回
   新实现的 GDB stub。

UDP 日志后端示例
**************************

演练 UDP coredump 路径的示例 README 页面链接到本章，以便 Sphinx
将其包含在文档树中：

.. toctree::
   :maxdepth: 1
   :hidden:

   ../../samples/subsys/debug/coredump_udp_demos/demo_shell/README

API 文档
*****************

.. doxygengroup:: coredump_apis

.. doxygengroup:: arch-coredump
