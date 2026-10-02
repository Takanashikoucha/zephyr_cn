.. _code_data_relocation:

代码和数据重定位
########################

概述
********

此功能可将 .text、.rodata、.data 和 .bss 段从指定文件重定位到指定的内存区域。
内存区域和文件以字符串形式提供给 :ref:`gen_relocate_app.py` 脚本。
该脚本始终从 cmake 内部调用。

该脚本提供了一种稳健的方法来重新排列内存内容，而无需实际修改代码。
简单来说，该脚本会对一批文件一起完成 ``__attribute__((section("name")))`` 的工作。

可以使用正则表达式过滤器来选择仅重定位所需的段。

细节
*******

内存区域和文件通过一个文件提供给 :ref:`gen_relocate_app.py` 脚本，
其中每一行指定要放置到给定区域的一组文件。

此类文件的一个示例为：

  .. code-block:: none

     SRAM2:/home/xyz/zephyr/samples/hello_world/src/main.c,
     SRAM1:/home/xyz/zephyr/samples/hello_world/src/main2.c,

该脚本以如下参数调用：
``python3 gen_relocate_app.py -i input_file -o generated_linker -c generated_code``

Kconfig :kconfig:option:`CONFIG_CODE_DATA_RELOCATION` 选项在
``prj.conf`` 中启用后，会调用该脚本并执行所需的重定位。

该脚本还会触发生成 ``linker_relocate.ld`` 和 ``code_relocation.c`` 文件。
``linker_relocate.ld`` 文件创建相应的段，并将所有选定文件中所需的函数或变量链接起来。

.. note::

    text 段在主链接脚本中被拆分为 2 部分。第一部分包含有关向量表
    和其他调试相关信息的信息。第二部分包含完整的 text 段。
    这是为了强制将所需的函数和数据变量放到正确位置所必需的，
    原因在于链接器的行为。链接器只会链接一次，因此必须拆分该 text 段
    以为生成的链接脚本腾出空间。

``code_relocation.c`` 文件包含初始化数据段所需的代码，
以及 text 段的副本（如果是 XIP）。
此外还包含 bss 清零所需的代码，
以及从 ROM 到所需内存类型的数据拷贝操作代码。

**启用此功能的步骤为：**

* 在 ``prj.conf`` 文件中启用 :kconfig:option:`CONFIG_CODE_DATA_RELOCATION`

* 在项目中的 ``CMakeLists.txt`` 文件里，列出所有需要重定位的文件。

  ``zephyr_code_relocate(FILES src/main.c LOCATION SRAM2)``

  其中第一个参数是文件（单个或多个），第二个参数
  是必须放置到的内存。

  .. note::

     函数 ``zephyr_code_relocate()`` 可以按需调用任意多次。

附加配置
=========================

本节介绍可以在 ``CMakeLists.txt`` 中设置的附加配置选项。

* 如果内存为 ``SRAM1``、``SRAM2``、``CCD`` 或 ``AON``，则将完整对象
  放入段中。例如：

  .. code-block:: cmake

     zephyr_code_relocate(FILES src/file1.c LOCATION SRAM2)
     zephyr_code_relocate(FILES src/file2.c LOCATION SRAM1)

* 如果内存类型后附加了 ``_DATA``、``_TEXT``、``_RODATA``、
  ``_BSS`` 或 ``_NOINIT``，则只有所选的内存会被放入所需的
  内存区域。例如：

  .. code-block:: cmake

     zephyr_code_relocate(FILES src/file1.c LOCATION SRAM2_DATA)
     zephyr_code_relocate(FILES src/file2.c LOCATION SRAM2_TEXT)

* 也可以将多个区域拼接在一起，例如：
  ``SRAM2_DATA_BSS_NOINIT``。这将把所有数据——值初始化、
  零初始化和未初始化的——都放入 ``SRAM2`` 中。

* 可以向 ``FILES`` 参数传递多个文件，或者使用 CMake 生成器
  表达式来重定位以逗号分隔的文件列表。

  .. code-block:: cmake

     file(GLOB sources "file*.c")
     zephyr_code_relocate(FILES ${sources} LOCATION SRAM2)
     zephyr_code_relocate(FILES $<TARGET_PROPERTY:my_tgt,SOURCES> LOCATION SRAM2)

段过滤
================

默认情况下，指定文件的所有段都会被重定位。如果使用
``FILTER``，则提供一个正则表达式来选择仅重定位的段。

该正则表达式作用于段名，可用于在文件使用
``-ffunction-sections`` 和 ``-fdata-sections`` 构建时（这是
默认情况）选择文件中的符号。

  .. code-block:: cmake

     zephyr_code_relocate(FILES src/file1.c FILTER ".*\\.func1|.*\\.func2" LOCATION SRAM2_TEXT)

上述示例只会重定位 ``src/file1.c`` 文件中的 ``func1()`` 和 ``func2()``。

NOKEEP 标志
===============

默认情况下，生成 ``linker_relocate.ld`` 时，所有被重定位的函数和变量
都会被标记为 ``KEEP()``。因此，如果某个输入文件恰好
包含未使用的符号，即使链接器以 ``--gc-sections`` 调用，
它们也不会被丢弃。如果想覆盖此行为，
可以在 ``zephyr_code_relocate()`` 调用中传入 ``NOKEEP``。

  .. code-block:: cmake

     zephyr_code_relocate(FILES src/file1.c LOCATION SRAM2_TEXT NOKEEP)

上述示例有助于确保在 ``file1.c`` 的 .text 段中发现的任何未使用代码
都不会滞留在 SRAM2 中。

NOCOPY 标志
===============

当向 ``zephyr_code_relocate()`` 函数传入 ``NOCOPY`` 选项时，
不会在 ``code_relocation.c`` 中生成重定位代码。当希望
将某个特定文件（或一组文件）的内容移到 XIP 区域时可以使用该标志。

此示例将 ``xip_external_flash.c`` 文件的 .text 段放入
``EXTFLASH`` 内存区域，从该区域直接执行（XIP）。
.data 会像往常一样被重定位到 SRAM。

  .. code-block:: cmake

     zephyr_code_relocate(FILES src/xip_external_flash.c LOCATION EXTFLASH_TEXT NOCOPY)
     zephyr_code_relocate(FILES src/xip_external_flash.c LOCATION SRAM_DATA)

重定位库
==================

可以使用 ``zephyr_code_relocation()`` 的 LIBRARY 参数和库名来重定位库。
例如，以下片段将串口驱动重定位到 SRAM2：

  .. code-block:: cmake

    zephyr_code_relocate(LIBRARY drivers__serial LOCATION SRAM2)

提示
====

在重定位内核/架构文件时要小心，其中一些包含在代码重定位发生之前
执行的早期初始化代码。

可能还需要附加的 MPU/MMU 配置，以确保目标内存区域
被配置为允许代码执行。

示例/测试
=============

展示此功能的测试位于 ``$ZEPHYR_BASE/tests/application_development/code_relocation``

该测试展示了如何使用代码重定位功能。

该测试使用基于 ``include/zephyr/arch/arm/cortex_m/scripts/linker.ld``
派生的自定义链接文件，将 3 个文件的 .text、.data、.bss 放入 SRAM 的各个部分。

展示 NOCOPY 标志的示例在这里：:zephyr:code-sample:`code_relocation_nocopy`。
