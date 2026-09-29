:orphan:

.. _nordic_segger:

Nordic
nRF5x
Segger
J-Link
##########################

概览
********

所有
Nordic
nRF5x
开发
套件、
预览
开发
套件
和
Dongle
都
配备
一个
调试
IC
（Atmel
ATSAM3U2C），
提供
以下
功能：

* Segger
  J-Link
  固件
  和
  桌面
  工具
* nRF5x
  IC
  的
  SWD
  调试
* 拖放
  镜像
  烧录
  的
  大容量
  存储
  设备
* 桥接
  到
  nRF5x
  UART
  外设
  的
  USB
  CDC
  ACM
  串口
* Segger
  RTT
  控制台
* Segger
  Ozone
  调试器

Segger
J-Link
软件
安装
***********************************

要
安装
J-Link
软件
和
文档
包，
遵循
以下
步骤：

#. 从
   `J-Link
   Software
   and
   documentation
   pack`_
   网站
   下载
   适当
   的
   包
#. 取决于
   你的
   平台，
   安装
   包
   或
   运行
   安装器
#. 当
   连接
   一个
   J-Link
   使能
   的
   开发板
   如
   nRF5x
   DK、
   PDK
   或
   dongle
   时，
   对应
   USB
   大容量
   存储
   设备
   的
   驱动器
   和
   一个
   串口
   应该
   出现

nRF5x
命令行
工具
安装
*************************************

nRF5x
命令行
工具
允许
你
从
命令行
控制
你的
nRF5x
设备，
包括
重置
它、
擦除
或
编程
flash
内存
等。

要
安装
它们，
访问
`nRF5x
Command-Line
Tools`_
并
选择
你的
操作
系统。

安装
后，
确保
``nrfjprog``
在
你
的
可
执行
路径
某
处
以
能够
从
任何
地方
调用
它。

.. _nordic_segger_flashing:

烧录
********

在
遵循
安装
Segger
J-Link
软件
和
nRF5x
命令行
工具
的
说明
后，
要
用
编译
的
Zephyr
镜像
编程
flash，
遵循
以下
步骤：

* 将
  micro-USB
  线
  连接
  到
  nRF5x
  开发板
  和
  你的
  电脑
* 擦除
  nRF5x
  IC
  中
  的
  flash
  内存：

.. code-block:: console

   nrfjprog
   --eraseall
   -f
   nrf5<x>

其中
``<x>``
是
1
用于
nRF51
基于
的
开发板
或
2
用于
nRF52
基于
的
开发板

* 从
  你
  选择
  的
  示例
  文件夹
  烧录
  Zephyr
  镜像：

.. code-block:: console

   nrfjprog
   --program
   outdir/<board>/zephyr.hex
   -f
   nrf5<x>

其中：
``<board>``
是
你
在
构建
时
BOARD
指令
中
使用
的
开发板
名称
（例如
nrf52dk/nrf52832）
且
``<x>``
是
1
用于
nRF51
基于
的
开发板
或
2
用于
nRF52
基于
的
开发板

* 重置
  并
  启动
  Zephyr：

.. code-block:: console

   nrfjprog
   --reset
   -f
   nrf5<x>

其中
``<x>``
是
1
用于
nRF51
基于
的
开发板
或
2
用于
nRF52
基于
的
开发板

USB
CDC
ACM
串口
设置
*****************************

**重要
注意**：
nRF5x
开发板
上
的
Segger
J-Link
固件
的
一个
问题
可能
导致
某些
机器
上
USB
CDC
ACM
串口
的
数据
丢失
和/或
损坏。
要
绕过
这
在
你的
开发板
上
禁用
大容量
存储
设备
如
:ref:`nordic_segger_msd`
中
描述
的。

Windows
=======

串口
将
出现
为
``COMxx``。
只
需要
检查
设备
管理器
中
的
"Ports
(COM
&
LPT)"
章节。

GNU/Linux
=========

串口
将
出现
为
``/dev/ttyACMx``。
默认
情况
下
端口
不
对
所有
用户
可
访问。
键入
下面
的
命令
将
你
的
用户
添加
到
dialout
组
以
给
它
串口
访问
权限。
注意
这
需要
重新
登录
才
生效。

.. code-block:: bash

   sudo
   usermod
   -a
   -G
   dialout
   `whoami`

较
新
版本
的
`ModemManager
send
AT
commands
to
TTY-like
devices`_；
这
包括
Nordic
开发
套件。
这
将
阻止
你
使用
串口
几
秒，
并
可能
使
你
的
应用
行为
不
正常
如果
它
从
UART
读取
数据。
运行
你的
应用
前，
你
可能
想
临时
禁用
ModemManager
通过
`blocklist
Segger
devices
by
editing
udev
rules`_。

.. _nordic_segger_msd:

禁用
大容量
存储
设备
*****************************

如果
你
遇到
USB
CDC
ACM
串口
的
数据
丢失
或
损坏
问题，
你
应该
禁用
开发板
上
的
大容量
存储
设备。
这
可以
通过
在
J-Link
固件
设置
中
禁用
Mass
Storage
做
到。

.. _nordic_segger_rtt:

RTT
控制台
************

Segger
RTT
（Real-Time
Tracing）
是
一个
低
开销
的
实时
日志
机制，
允许
你
从
目标
读取
日志
而
不
干扰
应用
执行。
它
可以
用
`Real-Time
Tracing
（RTT）`_
或
`pyrtt-viewer`_
查看。

.. _nordic_segger_ozone:

Ozone
调试器
************

Segger
Ozone
是
一个
功能
强大
的
图形
调试器，
支持
断点
调试、
单步
执行
和
变量
查看。
它
可以
从
`Segger
Ozone
Download`_
下载。

.. _nordic_segger_gdb:

GDB
调试
************

要
用
GDB
调试
nRF5x
开发板，
用
``nrfjprog``
启动
一个
GDB
服务器
并
连接
GDB
客户端。

.. code-block:: console

   nrfjprog
   --gdbserver
   -f
   nrf5<x>

然后
在
GDB
客户端
中：

.. code-block:: gdb

   target
   remote
   :1337

GDB
服务器
在
端口
1337
监听。
你
可以
加载
:file:`zephyr.elf`
文件
（你
可以
在
构建
文件夹
中
找到
的
那个）
来
调试
你的
应用。

参考
**********

.. target-notes::

.. _nRF5x
   Command-Line
   Tools:
   https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Command-Line-Tools

.. _Segger
   SAM3U
   Wiki:
   https://wiki.segger.com/J-Link-OB_SAM3U
.. _Real-Time
   Tracing
   （RTT）:
   https://www.segger.com/jlink-rtt.html
.. _pyrtt-viewer:
   https://github.com/thomasstenersen/pyrtt-viewer
.. _Segger
   Ozone:
   https://www.segger.com/ozone.html
.. _Segger
   Ozone
   Download:
   https://www.segger.com/downloads/jlink#Ozone

.. _ModemManager
   send
   AT
   commands
   to
   TTY-like
   devices:
   https://bugs.freedesktop.org/show_bug.cgi?id=85007
.. _blocklist
   Segger
   devices
   by
   editing
   udev
   rules:
   http://www.at91.com/linux4sam/bin/view/Linux4SAM/SoftwareTools#Device_or_resource_busy_dev_ttyA

.. _J-Link
   Software
   and
   documentation
   pack:
   https://www.segger.com/jlink-software.html
