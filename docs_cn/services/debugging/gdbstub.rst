.. _gdbstub:

GDB
stub
########

.. contents::
   :local:
   :depth:
   2

Overview
********

Gdbstub
feature
provide
GDB
Remote
Serial
Protocol
（RSP）
的
一
个
implementation
它
允许
你
用
GDB
remotely
debug
Zephyr。

Protocol
support
不同
的
connection
types：
serial、
UDP/IP
和
TCP/IP。
Zephyr
当前
只
support
serial
device
communication。

GDB
program
作为
client
同时
Zephyr
gdbstub
作为
server。
当
这
个
feature
被
enabled
时
Zephyr
在
:c:func:`gdb_init`
start
gdbstub
service
后
stop
它
的
execution
并
wait
一
个
GDB
connection。
一
旦
connection
被
established
可以
synchronously
与
Zephyr
interact。
注意
当前
不
可以
asynchronously
send
commands
到
target。

Features
********

以下
features
被
supported：

*
Add
和
remove
breakpoints
*
Continue
和
step
target
*
Print
backtrace
*
Read
或
write
general
registers
*
Read
或
write
memory

Enabling
GDB
Stub
*****************


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
      .. code-block:: text

         (gdb) target remote localhost:5678

      Response from GDB:

      .. code-block:: text

         Remote debugging using localhost:5678
         arch_gdb_init () at <ZEPHYR_BASE>/arch/x86/core/ia32/gdbstub.c:252
         252     }

      GDB also shows where the code execution is stopped. In this case,
      it is at :zephyr_file:`arch/x86/core/ia32/gdbstub.c`, line 252.

   #. Use command ``bt`` or ``backtrace`` to show the backtrace of stack frames.

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

   #. Use command ``list`` to show the source code and surroundings where
      code execution is stopped.

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

   #. Use command ``s`` or ``step`` to step through program until it reaches
      a different source line. Now that it finished executing :c:func:`arch_gdb_init`
      and is continuing in :c:func:`gdb_init`.

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

   #. Use command ``br`` or ``break`` to setup a breakpoint. For this example
      set up a breakpoint at :c:func:`main`, and let code execution continue
      without any intervention using command ``c`` (or ``continue``).

      .. code-block:: text

         (gdb) break main
         Breakpoint 1 at 0x10064d: file <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c, line 27.

      .. code-block:: text

         (gdb) continue
         Continuing.

      Once code execution reaches :c:func:`main`, execution will be stopped
      and GDB prompt returns.

      .. code-block:: text

         Breakpoint 1, main () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:27
         27              printk("%s():enter\n", __func__);

      Now GDB is waiting at the beginning of :c:func:`main`:

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

   #. To examine the value of ``ret``, the command ``p`` or ``print``
      can be used.

      .. code-block:: text

         (gdb) p ret
         $1 = 1273788

      Since ``ret`` has not been initialized, it contains some random value.

   #. If step (``s`` or ``step``) is used here, it will continue execution
      skipping the interior of :c:func:`test`.
      To examine code execution inside :c:func:`test`,
      a breakpoint can be set for :c:func:`test`, or simply using
      ``si`` (or ``stepi``) to execute one machine instruction, where it has
      the side effect of going into the function. The GDB command ``finish``
      can be used to continue execution without intervention until the function
      returns.

      .. code-block:: text

         (gdb) finish
         Run till exit from #0  test () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:17
         0x00100667 in main () at <ZEPHYR_BASE>/tests/subsys/debug/gdbstub/src/main.c:28
         28              ret = test();
         Value returned is $2 = 30

   #. Examine ``ret`` again which should have the return value from
      :c:func:`test`. Sometimes, the assignment is not done until another
      ``step`` is issued, as in this case. This is due to the assignment
      code is done after returning from function. The assignment code is
      generated by the toolchain as machine instructions which are not
      visible when viewing the corresponding C source file.

      .. code-block:: text

         (gdb) p ret
         $3 = 1273788
         (gdb) step
         29              printk("ret=%d\n", ret);
         (gdb) p ret
         $4 = 30

   #. If ``continue`` is issued here, code execution will continue indefinitely
      as there are no breakpoints to further stop execution. Breaking execution
      in GDB via :kbd:`Ctrl-C` does not currently work as the Zephyr gdbstub does
      not support this functionality yet. Switch to the first console with QEMU
      running the Zephyr image and stop it manually with :kbd:`Ctrl+a x`.
      When the same test is executed by Twister, it automatically takes care of
      stopping the QEMU instance.