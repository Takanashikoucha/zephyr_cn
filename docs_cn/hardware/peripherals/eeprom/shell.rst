.. _eeprom_shell:

EEPROM Shell
############

.. contents::
    :local:
    :depth: 1

概述
********

EEPROM Shell 为 :ref:`shell <shell_api>` 模块提供带有子命令集的 ``eeprom`` 命令。它允许通过交互式接口测试和探索 :ref:`EEPROM <eeprom_api>` 驱动 API，而无需编写专用应用。EEPROM Shell 也可以在现有应用中启用，以辅助交互式调试 EEPROM 问题。

要启用 EEPROM shell，必须启用以下 :ref:`Kconfig <kconfig>` 选项：

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_EEPROM`
* :kconfig:option:`CONFIG_EEPROM_SHELL`

例如，为 :zephyr:board:`native_sim` 构建 :zephyr:code-sample:`hello_world` 示例并启用 EEPROM Shell：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: native_sim
   :gen-args: -DCONFIG_SHELL=y -DCONFIG_EEPROM=y -DCONFIG_EEPROM_SHELL=y
   :goals: build

参见 :ref:`shell <shell_api>` 文档获取如何连接并与 Shell 交互的一般说明。EEPROM Shell 带有内置帮助（除非禁用了 :kconfig:option:`CONFIG_SHELL_HELP`）。向 ``eeprom`` 命令或其任何子命令传递 ``-h`` 或 ``--help`` 即可打印内置帮助消息。所有子命令还支持其参数的 Tab 补全。

.. tip::
   所有 EEPROM Shell 子命令都接受 EEPROM 外设名称作为第一个参数，该参数也支持 Tab 补全。当启用 :kconfig:option:`CONFIG_DEVICE_SHELL` 时，可使用 ``device list`` Shell 命令获取所有可用设备的列表。下面的示例均使用设备名 ``eeprom@0``。

EEPROM 大小
***********

EEPROM 的大小可以用 ``eeprom size`` 子命令检查，如下所示：

.. code-block:: console

   uart:~$ eeprom size eeprom@0
   32768 bytes

写入数据
************

数据可使用 ``eeprom write`` 子命令写入 EEPROM。该子命令至少接受三个参数：EEPROM 设备名、起始写入偏移量以及至少一个数据字节。在以下示例中，十六进制字节序列 ``0x0d 0x0e 0x0a 0x0d 0x0b 0x0e 0x0e 0x0f`` 被写入偏移量 ``0x0``：

.. code-block:: console

   uart:~$ eeprom write eeprom@0 0x0 0x0d 0x0e 0x0a 0x0d 0x0b 0x0e 0x0e 0x0f
   Writing 8 bytes to EEPROM...
   Verifying...
   Verify OK

还可以使用 ``eeprom fill`` 子命令用相同模式填充 EEPROM 的一部分。在以下示例中，模式 ``0xaa`` 被写入从偏移量 ``0x8`` 开始的 16 个字节：

.. code-block:: console

   uart:~$ eeprom fill eeprom@0 0x8 16 0xaa
   Writing 16 bytes of 0xaa to EEPROM...
   Verifying...
   Verify OK

读取数据
************

数据可使用 ``eeprom read`` 子命令从 EEPROM 读取。该子命令接受三个参数：EEPROM 设备名、起始读取偏移量以及要读取的字节数：

.. code-block:: console

   uart:~$ eeprom read eeprom@0 0x0 8
   Reading 8 bytes from EEPROM, offset 0...
   00000000: 0d 0e 0a 0d 0b 0e 0e 0f                          |........         |
