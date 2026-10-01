.. _gdbstub:

GDB stub
########

.. contents::
   :local:
   :depth: 2

Overview
********

Gdbstub feature 提供 GDB Remote
Serial Protocol (RSP) 的实现（允许用 GDB 远程调试 Zephyr。

Protocol 支持不同 connection types：serial、UDP/IP 和
TCP/IP。Zephyr 当前仅支持 serial device communication。

GDB program 作为 client（而 Zephyr gdbstub 作为
server。启用此 feature 时（Zephyr 在
:c:func:`gdb_init` 启动 gdbstub service 后停止执行（并等待 GDB
connection。建立 connection 后可
与 Zephyr 同步交互。注意当前不
可能异步向 target 发送 commands。

Features
********

支持以下 features：

* 添加和移除 breakpoints
* Continue 和 step target
* Print backtrace
* 读取或写入 general registers
* 读取或写入 memory

Enabling GDB Stub
*****************

GDB stub 可用 :kconfig:option:`CONFIG_GDBSTUB` option 启用。

Using Serial Backend
====================

GDB stub 的 serial backend 可用
:kconfig:option:`CONFIG_GDBSTUB_SERIAL_BACKEND` option 启用。

由于 serial backend 用 UART devices 发送和接收 GDB commands（

* 若 board 有空闲 UART devices（将 chosen node 的 ``zephyr,gdbstub-uart``
  property 设为空闲 UART device（使 :c:func:`printk`
  和 log messages 不打印到用于 GDB 的同一 UART device。

* 对仅有一个 UART device 的 boards（若
  也用同一 UART device 输出（须禁用 :c:func:`printk` 和 logging。
  GDB 相关 messages 可能与 log messages 交错（可能
  产生非预期后果。通常可通过禁用
  :kconfig:option:`CONFIG_PRINTK` 和 :kconfig:option:`CONFIG_LOG` 完成。

Debugging
*********

Using Serial Backend
====================

#. 构建启用 GDB stub 和 serial backend。

#. 将构建的 image 刷入 board 并重置 board。

   * 执行现应暂停在 :c:func:`gdb_init`。

#. 在 development machine 上执行 GDB 并连接到 GDB stub。

   .. code-block:: bash

      target remote <serial device>

   例如（

.. code-block:: bash

      target remote /dev/ttyUSB1

#. 可用 GDB commands 开始调试。

Example
*******

有 test application :zephyr_file:`tests/subsys/debug/gdbstub`（其
test cases ``debug.gdbstub.breakpoints`` 演示 Zephyr GDB stub 如何使用。
Test 还有连接 QEMU 的 GDB stub 实现（在自定义
port ``tcp:1235``）的 case（作为验证 test script 本身的
reference。

从 :envvar:`ZEPHYR_BASE` directory 用以下 command 运行
test：

   .. code-block:: console

      west twister -p qemu_x86 -T tests/subsys/debug/gdbstub

Test 应成功运行（现在让我们逐步做类似的事
以从 GDB user 视角演示 Zephyr GDB stub 如何工作。

以下 snippets 中（用并期望你自己的适当 directories 替代
``<SDK install directory>``、``<build_directory>``、``<ZEPHYR_BASE>``。


#. 打开两个 terminal windows。

#. 第一个 terminal 中（构建并运行 test application：

   .. zephyr-app-commands::
      :zephyr-app: tests/subsys/debug/gdbstub
      :host-os: unix
      :board: qemu_x86
      :gen-args: '-DCONFIG_QEMU_EXTRA_FLAGS="-serial tcp:localhost:5678,server"'
      :goals: build run

   注意我们设置 :kconfig:option:`CONFIG_QEMU_EXTRA_FLAGS` 将 QEMU serial
   console port 导向 ``localhost`` TCP port ``5678``（以等待
   下一步 GDB ``remote`` command 的
   connection。

#. 第二个 terminal 中（启动 GDB：

   .. code-block:: bash

      <SDK install directory>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb

   #. 告知 GDB 在哪查找构建的 ELF file：

      .. code-block:: text

         (gdb) symbol-file <build directory>/zephyr/zephyr.elf

      GDB 响应：

      .. code-block:: text

         Reading symbols from <build directory>/zephyr/zephyr.elf...

   #. 告知 GDB 连接之前通过 QEMU 的 ``-serial`` 重定向
      作为 server 暴露的 Zephyr gdbstub serial backend（经
      TCP port。

      .. code-block:: text

         (gdb) target remote localhost:5678

      GDB 响应：

      .. code-block:: text

         Remote debugging using localhost:5678
         arch_gdb_init () at <ZEPHYR_BASE>/arch/x86/core/ia32/gdbstub.c:252
         252     }

      GDB 还显示 code 执行停止处。此情况下（
      在 :zephyr_file:`arch/x86/core/ia32/gdbstub.c` line 252。

   #. 用 command ``bt`` 或 ``backtrace`` 显示 stack frames 的 backtrace。

      .. code-block:: text

         (gdb) bt
         #0  arch_gdb_init () at <ZEPHYR_BASE>/arch/x86/core/ia32/gdbstub.c:252
         #1  0x00104140 in gdb_init () at <ZEPHYR_BASE>/zephyr/subsys/debug/gdbstub.c:852
         #2  0x00109c13 in z_sys_init_run_level (level=INIT_LEVEL_PRE_KERNEL_2) at <ZEPHYR_BASE>/kernel/init.c:360
         #3  0x00109e73 in z_cstart () at <ZEPHYR_BASE>/kernel/init.c:630
         #4  0x00104422 in z_prep_c (arg=0x1245bc <x86_cpu_boot_arg>) at <ZEPHYR_BASE>/arch/x86/core/prep_c.c:80
         #5  0x001000c9 in __csSet () at <ZEPHYR_BASE>/arch/x86/core/ia32/crt0.S:290
         #6  0x001245bc in uart_dev ()
         #7  0x00134988 in z_interrupt_stacks ()
         #8  0x00000000 in ?? ()

   #. 用 command ``list`` 显示
      code 执行停止处的 source code 和 surroundings。

      .. code-block:: text

         (gdb) list
         247             __asm__ volatile ("int3");
         248
         249     #ifdef CONFIG_GDBSTUB_TRACE
         250             printk("gdbstub:%s GDB is connected\n", __func__);
         251     #endif
         252     }
         253
         254     /* Hook current IDT. */
         255     _EXCEPTION_CONNECT_NOCODE(z_gdb_debug_isr, IV_DEBUG, 3);
         256     _EXCEPTION_CONNECT_NOCODE(z_gdb_break_isr, IV_BREAKPOINT, 3);

   #. 用 command ``s`` 或 ``step`` 逐步执行 program 直到到达
      不同 source line。现在其完成执行 :c:func:`arch_gdb_init`
      并在 :c:func:`gdb_init` 中继续。

      .. code-block:: text

         (gdb) s
         gdb_init () at <ZEPHYR_BASE>/subsys/debug/gdbstub.c:857
         857     return 0;

      .. code-block:: text

         (gdb) list
         852             arch_gdb_init();
         853
         854     #ifdef CONFIG_GDBSTUB_TRACE
         855             printk("gdbstub:%s exit\n", __func__);
         856     #endif
         857             return 0;
         858     }
         859
         860     #ifdef CONFIG_XTENSA
         861     /*

   #. 用 command ``br`` 或 ``break`` 设置 breakpoint。此示例
      在 :c:func:`main` 设置 breakpoint（并用 command ``c`` (或 ``continue``) 让 code 执行
      继续而无需干预。

      .. code-block:: text

         (gdb) break main
         Breakpoint 1 at 0x10064d: file <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c, line 27.

      .. code-block:: text

         (gdb) continue
         Continuing.

      code 执行到达 :c:func:`main` 时（执行将停止
      且 GDB prompt 返回。

      .. code-block:: text

         Breakpoint 1, main () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:27
         27              printk("%s():enter\n", __func__);

      现在 GDB 等待在 :c:func:`main` 开头：

      .. code-block:: text

         (gdb) list
         22
         23      int main(void)
         24      {
         25              int ret;
         26
         27              printk("%s():enter\n", __func__);
         28              ret = test();
         29              printk("ret=%d\n", ret);
         30              return 0;
         31      }

   #. 要检查 ``ret`` 的值（可用 command ``p`` 或 ``print``
      。

      .. code-block:: text

         (gdb) p ret
         $1 = 1273788

      由于 ``ret`` 未初始化（其包含某随机值。

   #. 若此处用 step（``s`` 或 ``step``）（将
      继续执行（跳过 :c:func:`test` 内部。
      要检查 :c:func:`test` 内的 code 执行（
      可为 :c:func:`test` 设置 breakpoint（或简单用
      ``si`` (或 ``stepi``) 执行一条 machine instruction（其
      副作用为进入 function。GDB command ``finish``
      可用于继续执行而无需干预（直到 function
      返回。

      .. code-block:: text

         (gdb) finish
         Run till exit from #0  test () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:17
         0x00100667 in main () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:28
         28              ret = test();
         Value returned is $2 = 30

   #. 再次检查 ``ret``（其应有
      :c:func:`test` 的返回值。有时（赋值直到另一
      ``step`` 发出才完成（如此案例。这是因为
      assignment
      code 在 function 返回后执行。Assignment code
      由 toolchain 生成（为查看对应 C source file 时
      不可见的 machine instructions。

      .. code-block:: text

         (gdb) p ret
         $3 = 1273788
         (gdb) step
         29              printk("ret=%d\n", ret);
         (gdb) p ret
         $4 = 30

   #. 若此处发出 ``continue``（code 执行将无限继续
      因为没有进一步停止执行的 breakpoints。用 :kbd:`Ctrl-C` 在 GDB 中
      中断执行当前不工作（因为 Zephyr gdbstub 尚不
      支持此 functionality。切换到运行 Zephyr image 的 QEMU 的
      第一个 console（并用 :kbd:`Ctrl+a x` 手动停止。
      当 Twister 执行相同 test 时（其自动
      负责停止 QEMU instance。
