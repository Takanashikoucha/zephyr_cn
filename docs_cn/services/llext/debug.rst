.. _llext_debug:

调试扩展
####################

调试扩展是一项复杂的任务。由于扩展代码按定义并非与 Zephyr 应用一起构建，最终的 Zephyr ELF 文件不包含扩展代码的符号。此外，扩展在运行时被 :c:func:`llext_load` 动态重定位，因此即使符号可用，调试器也无法知道扩展代码中符号的最终位置。

在这种情况下正确设置调试会话需要几个手动步骤。以下章节将介绍如何借助 Zephyr SDK 和 ``west`` 提供的调试功能来完成这一过程，但这些说明也可以适配到任何基于 GDB 的调试环境。

扩展调试流程
===========================

1. 确保项目已配置为显示详细的 LLEXT 调试输出（设置了 :kconfig:option:`CONFIG_LOG` 和 :kconfig:option:`CONFIG_LLEXT_LOG_LEVEL_DBG`）。

2. 构建 Zephyr 应用和扩展。

   对于当前构建中包含的每个目标 ``name``，会在构建根目录的 ``llext`` 子目录中生成两个文件：

   ``name_ext_debug.elf``

         一个包含完整调试信息的中间 ELF 文件。

   ``name.llext``

         最终的扩展二进制文件，已剥离至加载到 Zephyr 应用所需的基本数据。

   根据目标架构和构建配置，可能还存在其他文件。

3. 启动主 Zephyr 应用的调试会话。文档的 :ref:`调试 <west-debugging>` 章节对此有描述；在支持的板级上，只需运行 ``west debug``（可能附带一些额外参数）即可。

4. 在代码中 :c:func:`llext_load` 函数之后设置一个断点并让其运行。这将把扩展加载到内存中并完成重定位。输出日志中会包含一行 ``gdb add-symbol-file flags:``，其后跟着若干以 ``-s`` 开头的行。

5. 在 GDB 控制台中输入以下命令，加载该扩展的符号：

   .. code-block::

      add-symbol-file <path-to-debug.elf> <load-addresses>

   其中 ``<path-to-debug.elf>`` 是步骤 2 中识别出的带调试信息的 ELF 文件的完整路径，``<load-addresses>`` 是从上一步日志中收集到的所有 ``-s`` 行组成的空格分隔列表。

6. 此时扩展符号已可供调试器使用。你可以像往常一样设置断点、查看变量、单步执行代码。

如果应用加载了多个扩展，步骤 4-6 可以对每个扩展重复执行。

符号查找问题
==================

.. warning::

   几乎可以肯定，加载的符号会被主应用中的其他符号遮蔽；例如，它们可能位于 ELF 缓冲区或 LLEXT 堆的内存区域之内。

   在这种情况下，GDB 会选择第一个已知的符号，因此会将地址关联到某个 ``elf_buffer+0x123``，而不是预期的 ``ext_fn``。这进一步使其高级操作（如源码单步执行或查看局部变量）陷入混乱，因为在该上下文中它们毫无意义。

以下段落讨论该问题的两种可行解决方案。

丢弃所有 Zephyr 符号
--------------------------

最简单的做法是在步骤 5 之前，不带参数调用 ``add-symbol-file``，从 GDB 中丢弃所有 Zephyr 应用符号。但这样调试会话将只聚焦于 LLEXT，因为关于 Zephyr 应用的所有信息都会丢失。例如，调试器可能无法正确跟踪扩展代码之外的堆栈回溯。

可以在同一会话中多次使用相同的技术，在主符号表和扩展符号表之间按需切换，但很快就会变得繁琐。

编辑 ELF 文件
-----------------

这种替代方案更复杂，但能带来更无缝的调试体验。思路是编辑主 Zephyr ELF 文件，移除与要调试的扩展重叠的符号的信息，这样当扩展符号被加载时，GDB 就不会有任何歧义。可以通过使用 ``objcopy`` 的 ``-N <symbol>`` 选项来完成。

不过，识别肇事符号是一个反复试错的迭代过程，因为可能存在很多不同的层次；例如，ELF 缓冲区本身可能包含在数据段的某个符号中。幸运的是，对于给定项目，这份列表不太可能变化，因此这些知识可以多次复用。

调试会话示例
=========================

本示例演示如何在一块基于 ARM Cortex-M3 的仿真 ``mps2/an385`` 板级上，调试 ``tests/subsys/llext`` 项目中的 ``detached_fn`` 扩展（具体为 ``writable`` 用例）。

.. note::

   以下日志使用 Zephyr 4.1 版本和 Zephyr SDK 0.17.0 版本获取。不过，即使使用相同版本，确切地址在不同运行之间仍可能不同。请根据你自己会话的结果调整以下命令。

以下命令将构建项目并以调试模式启动仿真器：

.. code-block::
   :caption: 终端 1（构建、QEMU 仿真器、GDB 服务器）

   zephyr$ west build -p -b mps2/an385 tests/subsys/llext/ -T llext.writable -t debugserver_qemu
   -- west build: generating a build system
   [...]
   -- west build: running target debugserver_qemu
   [...]
   [186/187] To exit from QEMU enter: 'CTRL+a, x'[QEMU] CPU: cortex-m3

在另一个终端中，将 ``ZEPHYR_SDK_INSTALL_DIR`` 设置为你的安装中 Zephyr SDK 的目录，然后启动目标 GDB 客户端：

.. code-block::
   :caption: 终端 2（GDB 客户端）

   zephyr$ export LLEXT_SDK_INSTALL_DIR=/opt/zephyr-sdk-0.17.0
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-gdb build/zephyr/zephyr.elf
   GNU gdb (Zephyr SDK 0.17.0) 12.1
   [...]
   Reading symbols from build/zephyr/zephyr.elf...
   (gdb)

连接，在 ``llext_load`` 函数上设置断点并运行至其结束：

.. code-block::
   :caption: 终端 2（GDB 客户端）

   (gdb) target extended-remote :1234
   Remote debugging using :1234
   z_arm_reset () at zephyr/arch/arm/core/cortex_m/reset.S:124
   124         movs.n r0, #_EXC_IRQ_DEFAULT_PRIO
   (gdb) break llext_load
   Breakpoint 1 at 0x236c: file zephyr/subsys/llext/llext.c, line 168.
   (gdb) continue
   Continuing.

   Breakpoint 1, llext_load (ldr=ldr@entry=0x2000bef0 <ztest_thread_stack+3488>,
                             name=name@entry=0x9d98 "test_detached",
                             ext=ext@entry=0x2000abb8 <detached_llext>,
                             ldr_parm=ldr_parm@entry=0x2000bee8 <ztest_thread_stack+3480>)
                 at zephyr/subsys/llext/llext.c:168
   168             *ext = llext_by_name(name);
   (gdb) finish
   Run till exit from #0  llext_load ([...])
       at zephyr/subsys/llext/llext.c:168
   llext_test_detached () at zephyr/tests/subsys/llext/src/test_llext.c:481
   481             zassert_ok(res, "load should succeed");

第一个终端将打印大量与扩展加载相关的调试信息。找到包含地址的那一节：

.. code-block::
   :caption: 终端 1（构建、QEMU 仿真器、GDB 服务器）

   [...]
   D: Allocate and copy regions...
   [...]
   D: gdb add-symbol-file flags:
   D: -s .text 0x20000034
   D: -s .data 0x200000b4
   D: -s .bss 0x2000c2e0
   D: -s .rodata 0x200000b8
   D: -s .detach 0x200001d0
   D: Counting exported symbols...
   [...]

使用这些地址将符号加载到 GDB：

.. code-block::
   :caption: 终端 2（GDB 客户端）

   (gdb) add-symbol-file build/llext/detached_fn_ext_debug.elf -s .text 0x20000034 -s .data 0x200000b4 -s .bss 0x2000c2e0 -s .rodata 0x200000b8 -s .detach 0x200001d0
   add symbol table from file "build/llext/detached_fn_ext_debug.elf" at
           .text_addr = 0x20000034
           .data_addr = 0x200000b4
           .bss_addr = 0x2000c2e0
           .rodata_addr = 0x200000b8
           .detach_addr = 0x200001d0
   (y or n) y
   Reading symbols from build/llext/detached_fn_ext_debug.elf...
   (gdb) break detached_entry
   Breakpoint 2 at 0x200001d0 (2 locations)
   (gdb) continue
   Continuing.

   Breakpoint 2, 0x200001d0 in test_detached_ext ()
   (gdb) backtrace
   #0  0x200001d0 in test_detached_ext ()
   #1  0x200000ac in test_detached_ext ()
   #2  0x00000706 in llext_test_detached () at zephyr/tests/subsys/llext/src/test_llext.c:496
   #3  0x00001a36 in run_test_functions (suite=0x92bc <z_ztest_test_node_llext>, data=0x0 <cbvprintf_package>, test=0x92d8 <z_ztest_unit_test.llext.test_detached>) at zephyr/subsys/testsuite/ztest/src/ztest.c:328
   #4  test_cb (a=0x92bc <z_ztest_test_node_llext>, b=0x92d8 <z_ztest_unit_test.llext.test_detached>, c=0x0 <cbvprintf_package>) at zephyr/subsys/testsuite/ztest/src/ztest.c:662
   #5  0x00000e96 in z_thread_entry (entry=0x1a05 <test_cb>, p1=0x92bc <z_ztest_test_node_llext>, p2=0x92d8 <z_ztest_unit_test.llext.test_detached>, p3=0x0 <cbvprintf_package>) at zephyr/lib/os/thread_entry.c:48
   #6  0x00000000 in ?? ()

与断点位置关联的符号以及最后几个堆栈帧错误地引用了 Zephyr 应用中的 ELF 缓冲区，而不是扩展符号。注意 GDB 其实两者都知道：

.. code-block::
   :caption: 终端 2（GDB 客户端）

   (gdb) info sym 0x200001d0
   test_detached_ext + 464 in section datas of zephyr/build/zephyr/zephyr.elf
   detached_entry in section .detach of zephyr/build/llext/detached_fn_ext_debug.elf
   (gdb) info sym 0x200000ac
   test_detached_ext + 172 in section datas of zephyr/build/zephyr/zephyr.elf
   test_entry + 8 in section .text of zephyr/build/llext/detached_fn_ext_debug.elf

同样，也无法正确查看扩展中的变量或单步执行代码：

.. code-block::
   :caption: 终端 2（GDB 客户端）

   (gdb) print bss_cnt
   No symbol "bss_cnt" in current context.
   (gdb) print data_cnt
   No symbol "data_cnt" in current context.
   (gdb) next
   Single stepping until exit from function test_detached_ext,
   which has no line number information.

   Breakpoint 2, 0x200001ea in test_detached_ext ()
   (gdb)

丢弃符号
------------------

丢弃 Zephyr 符号、只聚焦于扩展，可以恢复完整的调试功能，代价是丢失全局上下文（注意堆栈回溯在扩展之外就停止了）：

.. code-block::
   :caption: 终端 2（GDB 客户端）

   (gdb) symbol-file
   Discard symbol table from `zephyr/build/zephyr/zephyr.elf'? (y or n) y
   Error in re-setting breakpoint 1: No symbol table is loaded.  Use the "file" command.
   No symbol file now.
   (gdb) add-symbol-file build/llext/detached_fn_ext_debug.elf -s .text 0x20000034 -s .data 0x200000b4 -s .bss 0x2000c2e0 -s .rodata 0x200000b8 -s .detach 0x200001d0
   add symbol table from file "build/llext/detached_fn_ext_debug.elf" at
           .text_addr = 0x20000034
           .data_addr = 0x200000b4
           .bss_addr = 0x2000c2e0
           .rodata_addr = 0x200000b8
           .detach_addr = 0x200001d0
   (y or n) y
   Reading symbols from build/llext/detached_fn_ext_debug.elf...
   (gdb) backtrace
   #0  detached_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:18
   #1  0x200000ac in test_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:26
   #2  0x00000706 in ?? ()
   Backtrace stopped: previous frame identical to this frame (corrupt stack?)
   (gdb) next
   19              zassert_true(data_cnt < 0);
   (gdb) print bss_cnt
   $1 = 1
   (gdb) print data_cnt
   $2 = -2
   (gdb)

编辑 ELF 文件
--------------------

在这种替代方案中，对 Zephyr ELF 文件的修补必须在终端 1 上构建 Zephyr 二进制文件并启动仿真器之后、在终端 2 上启动 GDB 客户端之前进行。

上述调试会话已经识别出 ``test_detached_ext``（保存 ELF 文件的字符数组）是一个肇事符号，因此第一轮将移除它。重复执行相同步骤后，还可以发现 ``__data_start`` 和 ``__data_region_start`` 也与目标内存区域重叠。

以下命令将从 Zephyr ELF 文件中移除所有这些符号，然后在修改后的文件上启动调试会话：

.. code-block::
   :caption: 终端 2（GDB 客户端）

   zephyr$ export LLEXT_SDK_INSTALL_DIR=/opt/zephyr-sdk-0.17.0
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-objcopy -N test_detached_ext -N __data_start -N __data_region_start build/zephyr/zephyr.elf build/zephyr/zephyr-edit.elf
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-gdb build/zephyr/zephyr-edit.elf
   GNU gdb (Zephyr SDK 0.17.0) 12.1
   [...]
   Reading symbols from build/zephyr/zephyr-edit.elf...
   (gdb)

可以再次执行上次运行中使用的相同步骤，连接 GDB 服务器并加载扩展及其调试符号。这一次，结果却大不相同：

 * ``break`` 命令包含行号信息；

 * ``backtrace`` 的输出同时包含扩展和 Zephyr 应用的函数；

 * 局部变量可以被正确查看。

.. code-block::
   :caption: 终端 2（GDB 客户端）

   (gdb) add-symbol-file build/llext/detached_fn_ext_debug.elf [...]
   [...]
   Reading symbols from build/llext/detached_fn_ext_debug.elf...
   (gdb) break detached_entry
   Breakpoint 2 at 0x200001d6: file zephyr/tests/subsys/llext/src/detached_fn_ext.c, line 17.
   (gdb) continue
   Continuing.

   Breakpoint 2, detached_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:17
   17              printk("bss %u @ %p\n", bss_cnt++, &bss_cnt);
   (gdb) backtrace
   #0  detached_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:17
   #1  0x200000ac in test_entry () at zephyr/tests/subsys/llext/src/detached_fn_ext.c:26
   #2  0x00000706 in llext_test_detached () at zephyr/tests/subsys/llext/src/test_llext.c:496
   #3  0x00001a36 in run_test_functions (suite=0x92bc <z_ztest_test_node_llext>, data=0x0 <cbvprintf_package>, test=0x92d8 <z_ztest_unit_test.llext.test_detached>) at zephyr/subsys/testsuite/ztest/src/ztest.c:328
   #4  test_cb (a=0x92bc <z_ztest_test_node_llext>, b=0x92d8 <z_ztest_unit_test.llext.test_detached>, c=0x0 <cbvprintf_package>) at zephyr/subsys/testsuite/ztest/src/ztest.c:662
   #5  0x00000e96 in z_thread_entry (entry=0x1a05 <test_cb>, p1=0x92bc <z_ztest_test_node_llext>, p2=0x92d8 <z_ztest_unit_test.llext.test_detached>, p3=0x0 <cbvprintf_package>) at zephyr/lib/os/thread_entry.c:48
   #6  0x00000000 in ?? ()
   (gdb) print bss_cnt
   $1 = 0
   (gdb) print data_cnt
   $2 = -3
   (gdb)
