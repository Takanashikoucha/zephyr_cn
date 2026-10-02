.. _gdbstub:

GDB stub
########

.. contents::
   :local:
   :depth: 2

概述
********

gdbstub 特性提供了 GDB 远程串行协议（Remote Serial Protocol，RSP）的实现，
允许使用 GDB 远程调试 Zephyr。

该协议支持不同的连接类型：串口（serial）、UDP/IP 和
TCP/IP。Zephyr 目前仅支持串口设备通信。

GDB 程序充当客户端（client），而 Zephyr gdbstub 充当
服务器（server）。启用该特性后，Zephyr 在
:c:func:`gdb_init` 启动 gdbstub 服务后会停止执行，并等待 GDB
连接。连接建立后，即可
与 Zephyr 进行同步交互。注意，目前尚不
支持向目标异步发送命令。

特性
********

支持以下特性：

* 添加和移除断点（breakpoint）
* 继续（continue）和单步（step）执行目标
* 打印回溯（backtrace）
* 读取或写入通用寄存器
* 读取或写入内存

启用 GDB Stub
*****************

可通过 :kconfig:option:`CONFIG_GDBSTUB` 选项启用 GDB stub。

使用串口后端
====================

GDB stub 的串口后端可通过
:kconfig:option:`CONFIG_GDBSTUB_SERIAL_BACKEND` 选项启用。

由于串口后端利用 UART 设备发送和接收 GDB 命令，

* 如果板上有空闲的 UART 设备，请将 chosen 节点的 ``zephyr,gdbstub-uart``
  属性设置为空闲的 UART 设备，以便 :c:func:`printk`
  和日志消息不会打印到用于 GDB 的同一 UART 设备。

* 对于只有一个 UART 设备的板，如果
  :c:func:`printk` 和日志也使用同一 UART 设备输出，则必须禁用它们。
  GDB 相关消息可能与日志消息交错，从而
  产生非预期后果。通常可以通过禁用
  :kconfig:option:`CONFIG_PRINTK` 和 :kconfig:option:`CONFIG_LOG` 来完成。

调试
*********

使用串口后端
====================

#. 构建时启用 GDB stub 和串口后端。

#. 将构建好的镜像刷入板中并复位板子。

   * 此时执行应暂停在 :c:func:`gdb_init`。

#. 在开发机上运行 GDB 并连接到 GDB stub。

   .. code-block:: bash

      target remote <serial device>

   例如，

   .. code-block:: bash

      target remote /dev/ttyUSB1

#. 使用 GDB 命令即可开始调试。

示例
*******

有一个测试应用 :zephyr_file:`tests/subsys/debug/gdbstub`，其中一个
测试用例 ``debug.gdbstub.breakpoints`` 演示了如何使用 Zephyr GDB stub。
该测试还有一个连接到 QEMU 的 GDB stub 实现（位于自定义
端口 ``tcp:1235``）的用例，作为验证测试脚本本身的
参照。

从 :envvar:`ZEPHYR_BASE` 目录使用以下命令运行
该测试：

   .. code-block:: console

      west twister -p qemu_x86 -T tests/subsys/debug/gdbstub

测试应成功运行，现在让我们逐步做类似的事情，
以从 GDB 用户视角演示 Zephyr GDB stub 如何工作。

以下代码片段中，请使用并期望以你自己相应的目录替代
``<SDK install directory>``、``<build_directory>``、``<ZEPHYR_BASE>``。


#. 打开两个终端窗口。

#. 在第一个终端中，构建并运行测试应用：

   .. zephyr-app-commands::
      :zephyr-app: tests/subsys/debug/gdbstub
      :host-os: unix
      :board: qemu_x86
      :gen-args: '-DCONFIG_QEMU_EXTRA_FLAGS="-serial tcp:localhost:5678,server"'
      :goals: build run

   注意我们设置了 :kconfig:option:`CONFIG_QEMU_EXTRA_FLAGS`，将 QEMU 串口
   控制台端口导向 ``localhost`` 的 TCP 端口 ``5678``，以等待
   下一步 GDB ``remote`` 命令发起的
   连接。

#. 在第二个终端中，启动 GDB：

   .. code-block:: bash

      <SDK install directory>/x86_64-zephyr-elf/bin/x86_64-zephyr-elf-gdb

   #. 告知 GDB 在哪里查找构建好的 ELF 文件：

      .. code-block:: text

         (gdb) symbol-file <build directory>/zephyr/zephyr.elf

      GDB 响应：

      .. code-block:: text

         Reading symbols from <build directory>/zephyr/zephyr.elf...

   #. 告知 GDB 连接 Zephyr gdbstub 的串口后端，该后端之前通过 QEMU 的 ``-serial`` 重定向
      作为服务器经由 TCP 端口暴露出来。

      .. code-block:: text

         (gdb) target remote localhost:5678

      GDB 响应：

      .. code-block:: text

         Remote debugging using localhost:5678
         arch_gdb_init () at <ZEPHYR_BASE>/arch/x86/core/ia32/gdbstub.c:252
         252     }

      GDB 还显示代码执行停止的位置。在本例中，
      位于 :zephyr_file:`arch/x86/core/ia32/gdbstub.c` 第 252 行。

   #. 使用命令 ``bt`` 或 ``backtrace`` 显示栈帧的回溯。

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

   #. 使用命令 ``list`` 显示
      代码执行停止处的源代码及其上下文。

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

   #. 使用命令 ``s`` 或 ``step`` 单步执行程序，直到到达
      另一行源代码。此时它已完成 :c:func:`arch_gdb_init`
      的执行，并在 :c:func:`gdb_init` 中继续。

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

   #. 使用命令 ``br`` 或 ``break`` 设置断点。本例
      在 :c:func:`main` 处设置断点，并使用命令 ``c``（或 ``continue``）让代码执行
      继续，无需任何干预。

      .. code-block:: text

         (gdb) break main
         Breakpoint 1 at 0x10064d: file <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c, line 27.

      .. code-block:: text

         (gdb) continue
         Continuing.

      代码执行到达 :c:func:`main` 时，执行将停止，
      并返回 GDB 提示符。

      .. code-block:: text

         Breakpoint 1, main () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:27
         27              printk("%s():enter\n", __func__);

      现在 GDB 正等待在 :c:func:`main` 的开头：

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

   #. 要检查 ``ret`` 的值，可以使用命令 ``p`` 或 ``print``。

      .. code-block:: text

         (gdb) p ret
         $1 = 1273788

      由于 ``ret`` 尚未初始化，其中包含某个随机值。

   #. 如果在此处使用单步（``s`` 或 ``step``），执行将继续，
      跳过 :c:func:`test` 的内部。
      要检查 :c:func:`test` 内部的代码执行，
      可以为 :c:func:`test` 设置断点，或者简单地使用
      ``si``（或 ``stepi``）执行一条机器指令，其
      副作用是进入函数。GDB 命令 ``finish``
      可用于让执行继续而不加干预，直到函数
      返回。

      .. code-block:: text

         (gdb) finish
         Run till exit from #0  test () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:17
         0x00100667 in main () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:28
         28              ret = test();
         Value returned is $2 = 30

   #. 再次检查 ``ret``，此时它应该具有
      :c:func:`test` 的返回值。有时，赋值直到再发出一次
      ``step`` 才完成，正如本例所示。这是因为
      赋值
      代码在函数返回后才执行。赋值代码
      由工具链生成，作为查看对应 C 源文件时
      不可见的机器指令。

      .. code-block:: text

         (gdb) p ret
         $3 = 1273788
         (gdb) step
         29              printk("ret=%d\n", ret);
         (gdb) p ret
         $4 = 30

   #. 如果在此处发出 ``continue``，代码执行将无限继续，
      因为不再有任何断点来停止执行。在 GDB 中通过 :kbd:`Ctrl-C`
      中断执行目前不起作用，因为 Zephyr gdbstub 尚不
      支持该功能。切换到运行 Zephyr 镜像的 QEMU 的
      第一个控制台，并用 :kbd:`Ctrl+a x` 手动停止它。
      当 Twister 运行相同的测试时，它会自动
      负责停止 QEMU 实例。
