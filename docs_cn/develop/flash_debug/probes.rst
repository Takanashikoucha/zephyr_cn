.. _debug-probes:

调试
探针
############

*调试
探针*
是
特殊
硬件，
允许
你
控制
运行
在
另一
块
开发板
上
的
Zephyr
应用
的
执行。
调试
探针
通常
允许
读取
和
写入
寄存器
和
内存，
并
支持
用
GDB
等
工具
在
你的
主机
工作站
上
对
Zephyr
应用
做
断点
调试。
它们
可能
也
支持
其他
调试
软件
和
更
高级
的
功能
如
:ref:`追踪
程序
执行
<tracing>`。
关于
Zephyr
支持
的
相关
主机
软件
的
细节，
见
:ref:`flash-debug-host-tools`。

调试
探针
通常
通过
USB
连接
到
你的
主机
工作站；
它们
有时
也
可以
通过
IP
网络
或
其他
方式
访问。
它们
通常
用
JTAG
或
SWD
协议
连接
到
运行
Zephyr
的
设备。
调试
探针
是
独立
的
硬件
设备
或
集成
在
运行
Zephyr
的
相同
开发板
上
的
电路。

Zephyr
中
许多
受
支持
开发板
包括
一个
第二
微控制器，
充当
板载
调试
探针、
USB
到
串口
适配器，
有时
还
是
拖放
flash
编程器。
这
消除
了
购买
外部
调试
探针
的
需要
并
提供
多种
调试
主机
工具
选项。

几个
硬件
厂商
有
他们
自己
品牌
的
板载
调试
探针
实现：
NXP
开发板
可能
用
`OpenSDA
<#opensda-onboard-debug-probe>`_、
`LPC-Link2
<#lpc-link2-onboard-debug-probe>`_
或
`MCU-Link
<#mcu-link-onboard-debug-probe>`_
探针，
取决于
调试
探针
固件
运行
的
微控制器。
ST
开发板
有
`ST-LINK
探针
<#stlink-v21-onboard-debug-probe>`_。
每个
板载
调试
探针
微控制器
可以
支持
一个
或多个
类型
的
固件
与
其
各自
的
调试
主机
工具
通信。
例如，
一个
OpenSDA
微控制器
可以
被
编程
DAPLink
固件
与
pyOCD
或
OpenOCD
调试
主机
工具
通信，
或
编程
J-Link
固件
与
J-Link
调试
主机
工具
通信。


+------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
||
*调试
探针
和
主机
工具*
             |                                                            主机
                                                            工具
                                                            |
+|
*兼容性
表*                   +--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                                          |  **J-Link
  调试**  |    **OpenOCD**     |      **pyOCD**      |   **NXP
  S32DS**    | **NXP
  LinkServer** | **ST-LINK
  GDB
  Server** |
+----------------+-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **J-Link
  外部**     |           ✓        |          ✓         |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **LPC-Link2
  CMSIS-DAP** |                    |                    |                     |                    |         ✓          |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **LPC-Link2
  J-Link**    |           ✓        |                    |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **MCU-Link
  CMSIS-DAP**  |                    |                    |                     |                    |         ✓          |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **MCU-Link
  J-Link**    |           ✓        |                    |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **OpenSDA
  DAPLink**   |                    |          ✓         |          ✓         |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **OpenSDA
  J-Link**    |           ✓        |                    |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **ST-LINK
  V2.1**      |           ✓        |          ✓         |                     |                    |         ✓          |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **NXP
  S32
  调试
  探针**    |                    |                    |                     |         ✓          |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **Black
  Magic
  Probe**   |           ✓        |          ✓         |          ✓         |                    |                    |                        |
+----------------+-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+


.. _jlink-external-debug-probe:

J-Link
外部
调试
探针
***********************

Segger
J-Link
是
一个
外部
调试
探针，
通过
USB
连接
到
主机
并
通过
JTAG
或
SWD
连接
到
目标
开发板。
它
支持
J-Link
调试
主机
工具
和
OpenOCD。

检查
你的
SoC
是否
列
在
`J-Link
Supported
Devices`_
中。

下载
并
安装
`J-Link
Software
and
Documentation
Pack`_
获取
J-Link
GDB
Server
和
Commander。

.. _lpc-link2-cmsis-onboard-debug-probe:

LPC-Link2
CMSIS-DAP
板载
调试
探针
************************************

LPC-Link2
是
NXP
的
板载
调试
探针，
运行
CMSIS-DAP
固件。
它
支持
OpenOCD、
pyOCD
和
NXP
LinkServer。

.. _lpc-link2-jlink-onboard-debug-probe:

LPC-Link2
J-Link
板载
调试
探针
******************************

LPC-Link2
也
可以
运行
J-Link
固件
与
J-Link
调试
主机
工具
通信。

.. _mcu-link-cmsis-onboard-debug-probe:

MCU-Link
CMSIS-DAP
板载
调试
探针
*************************************

MCU-Link
是
NXP
的
较
新
板载
调试
探针，
运行
CMSIS-DAP
固件。
它
支持
OpenOCD、
pyOCD
和
NXP
LinkServer。

.. _mcu-link-jlink-onboard-debug-probe:

MCU-Link
J-Link
板载
调试
探针
******************************

MCU-Link
也
可以
运行
J-Link
固件
与
J-Link
调试
主机
工具
通信。

.. _opensda-daplink-onboard-debug-probe:

OpenSDA
DAPLink
板载
调试
探针
*****************************

OpenSDA
是
NXP
的
开源
板载
调试
探针，
运行
DAPLink
固件。
它
支持
OpenOCD
和
pyOCD。

.. _opensda-jlink-onboard-debug-probe:

OpenSDA
J-Link
板载
调试
探针
**************************

OpenSDA
也
可以
运行
J-Link
固件
与
J-Link
调试
主机
工具
通信。

.. _stlink-v21-onboard-debug-probe:

ST-LINK
V2.1
板载
调试
探针
**************************

ST-LINK
V2.1
是
STMicroelectronics
的
板载
调试
探针。
它
支持
J-Link
调试
主机
工具、
OpenOCD
和
ST-LINK
GDB
Server。

.. _nxp-s32-debug-probe:

NXP
S32
调试
探针
****************

NXP
S32
调试
探针
设计
用于
与
`NXP
S32
Design
Studio
for
S32
Platform`_
配合
工作。
它
支持
NXP
S32DS
调试
主机
工具。

.. _black-magic-probe:

Black
Magic
Probe
*****************

Black
Magic
Probe
（BMP）
是
一个
开源
调试
探针，
将
GDB
调试
服务器
功能
整合
到
固件
中。
它
支持
J-Link
调试
主机
工具、
OpenOCD
和
pyOCD。

关于
Black
Magic
Probe
的
更多
细节，
包括
使用
说明
和
受
支持
目标，
见
`Black
Magic
Debug`_
和
`Black
Magic
Debug
supported
hardware`_。

.. _`J-Link
   Software
   and
   Documentation
   Pack`:
   https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack

.. _J-Link
   Supported
   Devices:
   https://www.segger.com/downloads/supported-devices.php

.. _NXP
   S32
   Design
   Studio
   for
   S32
   Platform:
   https://www.nxp.com/design/software/development-software/s32-design-studio-ide/s32-design-studio-for-s32-platform:S32DS-S32PLATFORM

.. _Black
   Magic
   Debug:
   https://black-magic.org/index.html

.. _Black
   Magic
   Debug
   supported
   hardware:
   https://black-magic.org/index.html#other-hardware-supported-by-black-magic-debug
