.. _gpio-kbd:

GPIO 键盘矩阵
####################

:dtcompatible:`gpio-kbd-matrix` 驱动程序支持大量键盘
矩阵硬件配置，并有众多选项可改变其行为。
以下概述了一些常见配置以及驱动程序如何支持它们。

所有这些配置的传统方式是：驱动程序在
行 GPIO（输入）上读取，在列 GPIO（输出）上选择。

基本用例：无隔离二极管、支持中断的 GPIO
***********************************************************

这是在消费级键盘中常见的配置，采用薄膜
开关和柔性电路板，无隔离二极管，需要
鬼键检测（默认启用）。

.. figure:: no-diodes.svg
      :align: center
      :width: 50%

      3x3 矩阵，无二极管

系统必须支持 GPIO 中断，并且可以同时
在所有行 GPIO 上启用中断。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        row-gpios = <&gpio0 0 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>,
                    <&gpio0 1 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>,
                    <&gpio0 2 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>;
        col-gpios = <&gpio0 3 GPIO_ACTIVE_LOW>,
                    <&gpio0 4 GPIO_ACTIVE_LOW>,
                    <&gpio0 5 GPIO_ACTIVE_LOW>;
   };

在此配置中，矩阵扫描库在所有
键释放后进入空闲模式，键盘矩阵线程仅在按下
某个键时才唤醒。

当前未选中的列的 GPIO 被配置为高阻
态。这意味着行状态可能需要一些时间才能稳定，
以避免从一列误读到下一列的键状态。稳定
时间可通过修改 ``settle-time-us`` 属性来调整。

隔离二极管
****************

如果矩阵的每个键都有隔离二极管，则可以：

 - 禁用鬼键检测，从而能够检测任意键组合
 - 将驱动程序配置为驱动未选中列的 GPIO 至非活动状态，
   而不是高阻态，这可以减少稳定时间
   （甚至可能降至 0），并使用效率更高的整端口 GPIO 读取 API
   （如果 GPIO 引脚是连续的，会自动发生）

二极管从行指向列的矩阵必须在行上使用上拉，
列使用低电平有效。

.. figure:: diodes-rc.svg
      :align: center
      :width: 50%

      带行到列隔离二极管的 3x3 矩阵。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        row-gpios = <&gpio0 0 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>,
                    <&gpio0 1 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>,
                    <&gpio0 2 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>;
        col-gpios = <&gpio0 3 GPIO_ACTIVE_LOW>,
                    <&gpio0 4 GPIO_ACTIVE_LOW>,
                    <&gpio0 5 GPIO_ACTIVE_LOW>;
        col-drive-inactive;
        settle-time-us = <0>;
        no-ghostkey-check;
   };

二极管从列指向行的矩阵必须在行上使用下拉，
列使用高电平有效。

.. figure:: diodes-cr.svg
      :align: center
      :width: 50%

      带列到行隔离二极管的 3x3 矩阵。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        row-gpios = <&gpio0 0 (GPIO_PULL_DOWN | GPIO_ACTIVE_HIGH)>,
                    <&gpio0 1 (GPIO_PULL_DOWN | GPIO_ACTIVE_HIGH)>,
                    <&gpio0 2 (GPIO_PULL_DOWN | GPIO_ACTIVE_HIGH)>;
        col-gpios = <&gpio0 3 GPIO_ACTIVE_HIGH>,
                    <&gpio0 4 GPIO_ACTIVE_HIGH>,
                    <&gpio0 5 GPIO_ACTIVE_HIGH>;
        col-drive-inactive;
        settle-time-us = <0>;
        no-ghostkey-check;
   };

不支持中断的 GPIO
******************************

一些 GPIO 控制器对 GPIO 中断有限制，可能不支持
同时在所有行 GPIO 上启用中断。

在这种情况下，可以将驱动程序配置为完全不使用中断，
而是通过选择所有列并持续轮询行 GPIO 来空闲，
如果引脚是连续的，这是一个单独的 GPIO API 操作。

通过将 ``idle-mode`` 属性设置为
``poll`` 可以启用此配置：

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        ...
        idle-mode = "poll";
   };

GPIO 多路复用器
****************

在更极端的情况下，例如列使用多路复用器且
无法同时选择所有列时，可以将驱动程序配置为
持续扫描。

这可以通过将 ``idle-mode`` 设置为 ``scan``，将 ``poll-timeout-ms``
设置为 ``0`` 来实现。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        ...
        poll-timeout-ms = <0>;
        idle-mode = "scan";
   };

行和列 GPIO 选择
*****************************

如果行 GPIO 是连续的且位于同一 GPIO 控制器上，
驱动程序会自动切换 API，从整个 GPIO 端口读取，
而不是逐个引脚读取。如果 GPIO 不是内存
映射的，例如在 I2C 或 SPI 端口扩展器上，这特别有用，
因为它显著减少了相应总线上的事务数量。

列 GPIO 也是如此，但仅在矩阵配置为
``col-drive-inactive`` 时成立，因此仅适用于带隔离
二极管的矩阵。

16 位行支持
******************

驱动程序默认使用 8 位数据类型存储行状态，
这将矩阵行数限制为 8。通过启用
:kconfig:option:`CONFIG_INPUT_KBD_MATRIX_16_BIT_ROW` 选项可以
将其增加到 16。

实际键掩码配置
*****************************

如果键矩阵不完整，可以使用 ``actual-key-mask`` 属性
指定实际存在键的映射。这使得可以在
鬼键检测之前对矩阵状态进行过滤，移除不存在的键，
从而可能允许原本会被鬼键检测阻止的键组合。

例如，对于一个缺少某个键的 3x3 矩阵：

.. figure:: no-sw4.svg
      :align: center
      :width: 50%

      缺少一个键的 3x3 矩阵。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        ...
        actual-key-mask = <0x07 0x05 0x07>;
   };

例如，这将允许同时检测按下 ``Sw1``、``SW2`` 和  ``SW4``
而不触发防鬼键。

通过启用
:kconfig:option:`CONFIG_INPUT_KBD_ACTUAL_KEY_MASK_DYNAMIC` 并使用
:c:func:`input_kbd_matrix_actual_key_mask_set` API，可以在运行时
更改实际键掩码。

键位图配置
********************

键盘矩阵设备报告一系列 x/y/触摸事件。这些可以
使用 :dtcompatible:`input-keymap` 驱动程序映射为普通键事件。

例如，以下设置了一个 ``keymap`` 设备，它接收
x/y/触摸事件作为输入，并生成相应的键事件作为
输出：

.. code-block:: devicetree

  kbd {
      ...
      keymap {
          compatible = "input-keymap";
          keymap = <
              MATRIX_KEY(0, 0, INPUT_KEY_1)
              MATRIX_KEY(0, 1, INPUT_KEY_2)
              MATRIX_KEY(0, 2, INPUT_KEY_3)
              MATRIX_KEY(1, 0, INPUT_KEY_4)
              MATRIX_KEY(1, 1, INPUT_KEY_5)
              MATRIX_KEY(1, 2, INPUT_KEY_6)
              MATRIX_KEY(2, 0, INPUT_KEY_7)
              MATRIX_KEY(2, 1, INPUT_KEY_8)
              MATRIX_KEY(2, 2, INPUT_KEY_9)
          >;
          row-size = <3>;
          col-size = <3>;
      };
  };

.. doxygengroup:: input_keymap

键盘矩阵 shell 命令
******************************

shell 命令 ``kbd_matrix_state_dump`` 可用于测试
任何使用键盘矩阵库实现的键盘矩阵驱动程序
的功能。启用后，它会在矩阵每次
状态变化时记录状态；禁用后，它会打印出所有已
检测到的键的或掩码，可用于设置 ``actual-key-mask`` 属性。

该命令可通过
:kconfig:option:`CONFIG_INPUT_SHELL_KBD_MATRIX_STATE` 启用。

用法示例：

.. code-block:: console

   uart:~$ device list
   devices:
   - kbd-matrix (READY)
   uart:~$ input kbd_matrix_state_dump kbd-matrix
   Keyboard state logging enabled for kbd-matrix
   [00:01:41.678,466] <inf> input: kbd-matrix state [01 -- -- --] (1)
   [00:01:41.784,912] <inf> input: kbd-matrix state [-- -- -- --] (0)
   ...
   press more buttons
   ...
   uart:~$ input kbd_matrix_state_dump off
   Keyboard state logging disabled
   [00:01:47.967,651] <inf> input: kbd-matrix key-mask [07 05 07 --] (8)

键盘矩阵库
***********************

GPIO 键盘矩阵驱动程序基于一个通用的键盘矩阵库，
该库实现了扫描延迟、去抖、
空闲模式等核心功能。可以复用它来实现其他键盘矩阵驱动程序，
包括应用特定的驱动程序。

.. doxygengroup:: input_kbd_matrix
