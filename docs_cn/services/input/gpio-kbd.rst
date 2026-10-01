.. _gpio-kbd:

GPIO Keyboard Matrix
####################

:dtcompatible:`gpio-kbd-matrix` driver 支持
大量
keyboard
matrix
hardware
configurations（并有
numerous
options
改变
其
behavior。此为
某些
common
setups
及
driver
如何
支持
它们的
overview。

所有
这些
的
conventional
configuration
为
driver
在
row
GPIOs（inputs）上
读取（并在
columns
GPIOs（output）上
select。

Base use case, no isolation diodes, interrupt capable GPIOs
***********************************************************

此为
membrane
switches
和
flexible
circuit
boards 的
consumer
keyboards 上
找到的
common
configuration（无
isolation
diodes（需
ghosting
detection（默认
启用）。

.. figure:: no-diodes.svg
      :align: center
      :width: 50%

      A 3x3 matrix, no diodes

System
须
支持
GPIO
interrupts（且
interrupt
可
同时
在
所有
row
GPIOs
上
启用。

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

此
configuration
中（matrix
scanning
library
在
所有
keys
释放
后
进入
idle
mode（且
keyboard
matrix
thread
仅在
key
按下
时
唤醒。

当前
未
select 的
columns 的
GPIOs
配置
为
high
impedance
mode。这
意味着
row
state
可能
需
一些
time
settle（以
避免
从
一
column
到
下一
column
误读
key
state。Settle
time
可
通过
更改
``settle-time-us``
property
调整。

Isolation diodes
****************

若
matrix
每
key
有
isolation
diodes（则
可：

 - 禁用
   ghosting
   detection（允许
   检测
   任何
   key
   combination
 - 配置
   driver
   将
   未
   select 的
   columns
   GPIO
   drive
   为
   inactive
   state
   而非
   high
   impedance（这
   允许
   减少
   settle
   time
   （潜在
   至
   0）（并
   用
   更
   efficient 的
   port
   wide
   GPIO
   read
   APIs
   （若
   GPIO
   pins
   连续
   则
   自动
   发生）

diodes
从
rows
到
columns 的
Matrixes
须
rows
上
用
pull-ups（且
columns
active
low。

.. figure:: diodes-rc.svg
      :align: center
      :width: 50%

      A 3x3 matrix with row to column isolation diodes.

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

diodes
从
columns
到
rows 的
Matrixes
须
rows
上
用
pull-downs（且
columns
active
high。

.. figure:: diodes-cr.svg
      :align: center
      :width: 50%

      A 3x3 matrix with column to row isolation diodes.

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

GPIO with no interrupt support
******************************

某些
GPIO
controllers
对
GPIO
interrupts
有
limitations（且
可能
不支持
同时
在
所有
row
GPIOs
上
启用
interrupts。

此
情况下（driver
可
配置
为
完全
不用
interrupt（而
通过
select
所有
columns 并
持续
poll
row
GPIOs 来
idle（pins
连续
时
此为
单个
GPIO
API
operation。

此
configuration
可
通过
将
``idle-mode``
property
设为
``poll`` 启用：

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        ...
        idle-mode = "poll";
   };

GPIO multiplexer
****************

更
extreme
cases（如
columns
用
multiplexer（且
不可能
同时
select
所有
时（driver
可
配置
为
持续
scan。

可
通过
将
``idle-mode``
设为
``scan``（``poll-timeout-ms``
设为
``0`` 完成。

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        ...
        poll-timeout-ms = <0>;
        idle-mode = "scan";
   };

Row and column GPIO selection
*****************************

若
row
GPIOs
连续
且
在
同一
gpio
controller
上（driver
自动
切换
API
为
从
整个
GPIO
port
读取（而非
individual
pins。若
GPIOs
非
memory
mapped（如
I2C
或
SPI
port
expander 上）这
特别
有用（因为
这
显著
减少
对应
bus 上
的
transactions 数量。

Column
GPIOs
同样
如此（但
仅
当
matrix
配置
为
``col-drive-inactive`` 时（故
仅
可
用于
有
isolation
diodes 的
matrixes。

16-bit row support
******************

Driver
默认
用
8-bit
datatype
存储
row
state（这
将
matrix
row
size
限制
为
8。可
通过
启用
:kconfig:option:`CONFIG_INPUT_KBD_MATRIX_16_BIT_ROW`
option
增加
至
16。

Actual key mask configuration
*****************************

若
key
matrix
不
完整（可用
``actual-key-mask``
property
指定
实际
populated
的
keys
的
map。这
允许
过滤
matrix
state（在
ghosting
detection
前
移除
不
存在的
keys（潜在
允许
否则
被
其
阻止
的
key
combinations。

例如
缺
一
key 的
3x3
matrix：

.. figure:: no-sw4.svg
      :align: center
      :width: 50%

      A 3x3 matrix missing a key.

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        ...
        actual-key-mask = <0x07 0x05 0x07>;
   };

这
允许（例如（同时
检测
``Sw1``、``SW2`` 和
``SW4``
按下
而
不
触发
anti
ghosting。

Actual
key
mask
可
通过
启用
:kconfig:option:`CONFIG_INPUT_KBD_ACTUAL_KEY_MASK_DYNAMIC`（并
用
:c:func:`input_kbd_matrix_actual_key_mask_set`
API
在
runtime
更改。

Keymap configuration
********************

Keyboard
matrix
devices
报告
x/y/touch
events
的
series。可
用
:dtcompatible:`input-keymap`
driver
将
它们
map
到
normal
key
events。

例如（以下
setup
``keymap``
device（其
取
x/y/touch
events
作为
input（并
生成
对应
key
events
作为
output：

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

Keyboard matrix shell commands
******************************

Shell
command
``kbd_matrix_state_dump``
可
用于
测试
用
keyboard
matrix
library
实现
的
任何
keyboard
matrix
driver 的
functionality。启用
后（每次
matrix
变更
时
log
其
state（禁用
后
打印
任何
检测
到
的
key 的
or-mask（可
用于
设置
``actual-key-mask``
property。

Command
可
用
:kconfig:option:`CONFIG_INPUT_SHELL_KBD_MATRIX_STATE` 启用。

Example
usage：

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

Keyboard matrix library
***********************

GPIO
keyboard
matrix
driver
基于
generic
keyboard
matrix
library（其
实现
scanning
delays、
debouncing、
idle
mode 等
core
functionalities。可
复用
以
实现
其他
keyboard
matrix
drivers（潜在
application
specific。

.. doxygengroup:: input_kbd_matrix
