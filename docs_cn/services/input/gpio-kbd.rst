.. _gpio-kbd:

GPIO 键盘矩阵
####################

:dtcompatible:`gpio-kbd-matrix` 驱动支持大量键盘矩阵硬件配置，并有众多选项可改变其行为。
本文概述了某些常见配置以及驱动如何支持它们。

所有这些的传统配置为驱动在行 GPIO（输入）上读取，并在列 GPIO（输出）上选择。

基础用例：无隔离二极管、支持中断的 GPIO
***********************************************************

这是消费级键盘上常见的配置，使用薄膜开关和柔性电路板，无隔离二极管，
需要鬼键检测（默认启用）。

.. figure:: no-diodes.svg
      :align: center
      :width: 50%

      3x3 矩阵，无二极管

系统须支持 GPIO 中断，且中断可在所有行 GPIO 上同时启用。

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

在此配置中，矩阵扫描库在所有按键释放后进入空闲模式，
键盘矩阵线程仅在按键被按下时唤醒。

当前未选中的列 GPIO 被配置为高阻模式。这意味着行状态可能需要一些时间
才能稳定，以避免从一个列到下一个列误读键状态。稳定时间可通过
修改 ``settle-time-us`` 属性来调整。

隔离二极管
****************

如果矩阵为每个按键都有隔离二极管，则可能：

 - 禁用鬼键检测，允许检测任意按键组合
 - 配置驱动将未选中的列 GPIO 驱动到非活动状态而非高阻，
   这允许减少稳定时间（可能降至 0），并使用更高效的端口宽 GPIO 读取 API
   （如果 GPIO 引脚是连续的则自动发生）

二极管从行到列的矩阵必须使用行上拉和列低有效。

.. figure:: diodes-rc.svg
      :align: center
      :width: 50%

      3x3 矩阵，行到列隔离二极管。

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

二极管从列到行的矩阵必须使用行下拉和列高有效。

.. figure:: diodes-cr.svg
      :align: center
      :width: 50%

      3x3 矩阵，列到行隔离二极管。

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

无中断支持的 GPIO
**************************

某些 GPIO 控制器对 GPIO 中断有限制，可能不支持同时在所有行 GPIO 上启用中断。

在这种情况下，驱动可配置为不使用任何中断，而是通过选择所有列并在行 GPIO 上
保持轮询来空闲，如果引脚是连续的则这是单个 GPIO API 操作。

此配置可通过将 ``idle-mode`` 属性设置为 ``poll`` 来启用：

.. code-block:: devicetree

   kbd-matrix {
       compatible = "gpio-kbd-matrix";
       ...
       idle-mode = "poll";
   };

GPIO 多路复用器
****************

在更极端的案例中，例如列使用多路复用器且不可能同时选择所有列时，
驱动可配置为连续扫描。

这可通过将 ``idle-mode`` 设置为 ``scan`` 并将 ``poll-timeout-ms`` 设置为 ``0`` 来实现。

.. code-block:: devicetree

   kbd-matrix {
       compatible = "gpio-kbd-matrix";
       ...
       poll-timeout-ms = <0>;
       idle-mode = "scan";
   };

行和列 GPIO 选择
*****************************

如果行 GPIO 是连续的且在同一 GPIO 控制器上，驱动自动切换到从整个 GPIO 端口
而非单个引脚读取的 API。这对 GPIO 不是内存映射的情况特别有用，
例如在 I2C 或 SPI 端口扩展器上，因为这显著减少了相应总线上的事务数量。

列 GPIO 也是如此，但仅当矩阵配置为 ``col-drive-inactive`` 时，
因此仅可用于有隔离二极管的矩阵。

16 位行支持
******************

驱动默认使用 8 位数据类型存储行状态，这将矩阵行大小限制为 8。
可通过启用 :kconfig:option:`CONFIG_INPUT_KBD_MATRIX_16_BIT_ROW` 选项将其增加到 16。

实际按键掩码配置
*****************************

如果按键矩阵不完整，可使用 ``actual-key-mask`` 属性指定实际存在的按键映射。
这允许在鬼键检测前过滤矩阵状态以移除不存在的按键，
从而可能允许否则会被其阻止的按键组合。

例如对于缺少一个按键的 3x3 矩阵：

.. figure:: no-sw4.svg
      :align: center
      :width: 50%

      缺少一个按键的 3x3 矩阵。

.. code-block:: devicetree

   kbd-matrix {
       compatible = "gpio-kbd-matrix";
       ...
       actual-key-mask = <0x07 0x05 0x07>;
   };

例如，这将允许同时检测按下 ``Sw1``、``SW2`` 和 ``SW4`` 而不触发防鬼键。

实际按键掩码可通过启用 :kconfig:option:`CONFIG_INPUT_KBD_ACTUAL_KEY_MASK_DYNAMIC`
并使用 :c:func:`input_kbd_matrix_actual_key_mask_set` API 在运行时更改。

按键映射配置
********************

键盘矩阵设备报告一系列 x/y/touch 事件。这些可使用 :dtcompatible:`input-keymap` 驱动
映射为常规按键事件。

例如，以下设置了一个 ``keymap`` 设备，将 x/y/touch 事件作为输入
并生成相应的按键事件作为输出：

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
**************************

shell 命令 ``kbd_matrix_state_dump`` 可用于测试任何使用键盘矩阵库实现的
键盘矩阵驱动的功能。启用后，它记录矩阵每次变化时的状态；
禁用后，它打印任何已检测按键的或掩码，可用于设置 ``actual-key-mask`` 属性。

该命令可通过 :kconfig:option:`CONFIG_INPUT_SHELL_KBD_MATRIX_STATE` 启用。

使用示例：

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

GPIO 键盘矩阵驱动基于通用键盘矩阵库，该库实现了扫描延迟、去抖动、
空闲模式等核心功能。这可复用于实现其他键盘矩阵驱动，
可能是应用特定的。

.. doxygengroup:: input_kbd_matrix
