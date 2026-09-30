.. _llext_debug:

Debugging
extensions
####################

Debugging
extensions
是
一
个
complex
的
task。
因为
extension
code
by
definition
不
与
Zephyr
application
一起
built
final
的
Zephyr
ELF
file
不
contain
extension
code
的
symbols。
Furthermore
extension
在
runtime
被
:c:func:`llext_load`
dynamically
relocated
所以
即使
symbols
available
debugger
也
impossible
know
extension
code
中
symbols
的
final
locations。

在
这
个
case
properly
set
up
debugger
session
require
几
个
manual
的
steps。
以下
sections
将
provide
some
tips
关于
如何
用
Zephyr
SDK
和
``west``
provided
的
debug
features
做
这
个
但
instructions
可以
be
adapted
到
任何
GDB
based
的
debugging
environment。

Extension
debugging
process
===========================

1.
Ensure
project
被
set
up
用于
display
verbose
的
LLEXT
debug
output
（:kconfig:option:`CONFIG_LOG`
和
:kconfig:option:`CONFIG_LLEXT_LOG_LEVEL_DBG`
被
set）。

2.
Build
Zephyr
application
和
extensions。

    对
    current
    build
    中
    included
    的
    每个
    target
    ``name``
    两
    个
    files
    将
    被
    generated
    到
    build
    root
    的
    ``llext``
    subdirectory
    中：

    ``name_ext_debug.elf``

            一
            个
            intermediate
            的
            ELF
            file
            带
            full
            的
            debugging
            information。

    ``name.llext``

            Final
            的
            extension
            binary
            被
            stripped
            到
            load
            到
            Zephyr
            application
            所需
            的
            essential
            data。

    根据
    target
    architecture
    和
    build
    configuration
    可能
    有
    其他
    files。


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) info sym 0x200001d0
   test_detached_ext + 464 in section datas of zephyr/build/zephyr/zephyr.elf
   detached_entry in section .detach of zephyr/build/llext/detached_fn_ext_debug.elf
   (gdb) info sym 0x200000ac
   test_detached_ext + 172 in section datas of zephyr/build/zephyr/zephyr.elf
   test_entry + 8 in section .text of zephyr/build/llext/detached_fn_ext_debug.elf

It is also impossible to inspect the variables in the extension or step through
code properly:

.. code-block::
   :caption: Terminal 2 (GDB client)

   (gdb) print bss_cnt
   No symbol "bss_cnt" in current context.
   (gdb) print data_cnt
   No symbol "data_cnt" in current context.
   (gdb) next
   Single stepping until exit from function test_detached_ext,
   which has no line number information.

   Breakpoint 2, 0x200001ea in test_detached_ext ()
   (gdb)

Discarding symbols
------------------

Discarding the Zephyr symbols and only focusing on the extension restores full
debugging functionality at the cost of losing the global context (note the
backtrace stops outside the extension):

.. code-block::
   :caption: Terminal 2 (GDB client)

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


Editing the ELF file
--------------------

In this alternative approach, the patches to the Zephyr ELF file must be
performed after building the Zephyr binary and starting the emulator on
Terminal 1, but before starting the GDB client on Terminal 2.

The above debugging session already identified ``test_detached_ext``, the char
array that holds the ELF file, as an offending symbol, so that will be removed
in a first pass. Performing the same steps multiple times, ``__data_start`` and
``__data_region_start`` can also be found to overlap the memory area of
interest.

The following commands will remove all of these from the Zephyr ELF file, then
start a debugging session on the modified file:

.. code-block::
   :caption: Terminal 2 (GDB client)

   zephyr$ export LLEXT_SDK_INSTALL_DIR=/opt/zephyr-sdk-0.17.0
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-objcopy -N test_detached_ext -N __data_start -N __data_region_start build/zephyr/zephyr.elf build/zephyr/zephyr-edit.elf
   zephyr$ ${LLEXT_SDK_INSTALL_DIR}/arm-zephyr-eabi/bin/arm-zephyr-eabi-gdb build/zephyr/zephyr-edit.elf
   GNU gdb (Zephyr SDK 0.17.0) 12.1
   [...]
   Reading symbols from build/zephyr/zephyr-edit.elf...
   (gdb)

The same steps used in the previous run can be performed again to attach to the
GDB server and load both the extension and its debug symbols. This time, however,
the result is rather different:

 * the ``break`` command includes line number information;

 * the output from ``backtrace`` contains functions from both the extension and
   the Zephyr application;

 * the local variables can be properly inspected.

.. code-block::
   :caption: Terminal 2 (GDB client)

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