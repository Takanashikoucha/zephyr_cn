.. _flash-debug-host-tools:

烧录
和
调试
主机
工具
########################

本
指南
描述
你
可以
在
主机
工作站
上
运行
来
烧录
和
调试
Zephyr
应用
的
软件
工具。

Zephyr
的
west
工具
在
其
``flash``、
``debug``、
``debugserver``
和
``attach``
命令
中
内置
支持
所有
这些
工具，
前提
是
你的
开发板
硬件
支持
它们
且
你的
Zephyr
开发板
目录
的
:file:`board.cmake`
文件
正确
声明
了
该
支持。
更多
信息
见
:ref:`west-build-flash-debug`。

.. _runner_blackmagicprobe:

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
硬件，
将
GDB
调试
服务器
功能
整合
到
固件
中。
不
需要
GDB
服务器
程序，
因此
不
有
host-tool
等价
的
程序。

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
:ref:`black-magic-probe`。

.. _atmel_sam_ba_bootloader:
.. _runner_bossac:

SAM
Boot
Assistant
（SAM-BA）
***************************

Atmel
SAM
Boot
Assistant
（Atmel
SAM-BA）
允许
从
USB
或
UART
主机
进行
系统
内
编程
（ISP）
而
不
需要
任何
外部
编程
接口。
Zephyr
允许
用户
用
:ref:`west
<west-flashing>`
开发
和
编程
支持
SAM-BA
的
开发板。
Zephyr
支持
带/不
带
ROM
bootloader
的
设备
和
Arduino
和
Adafruit
两者
的
扩展。
完整
支持
在
Zephyr
SDK
0.12.0
中
引入。

烧录
开发板
的
典型
命令
是：

.. code-block:: console

   west
   flash
   [
   -r
   bossac
   ]
   [
   -p
   /dev/ttyX
   ]
   [
   --erase
   ]

.. note::

   默认
   情况
   下，
   用
   bossac
   烧录
   只
   擦除
   包含
   烧录
   应用
   的
   flash
   页，
   其他
   页
   保持
   不
   变。
   如果
   你
   想
   烧录
   时
   擦除
   目标
   的
   整个
   flash，
   烧录
   时
   传递
   ``--erase``
   参数。

设备
的
flash
配置：

.. tabs::

   .. tab::
      带
      ROM
      bootloader

      这些
      设备
      不
      需要
      任何
      特殊
      配置。
      构建
      你的
      应用
      后，
      只
      运行
      ``west
      flash``
      烧录
      开发板。

   .. tab::
      不
      带
      ROM
      bootloader

      对于
      这些
      设备，
      用户
      应该：

      1. 定义
         容纳
         bootloader
         和
         应用
         镜像
         所需
         的
         flash
         分区；
         细节
         见
         :ref:`flash_map_api`。
      2. 有
         开发板
         :file:`.defconfig`
         文件
         将
         :kconfig:option:`CONFIG_USE_DT_CODE_PARTITION`
         Kconfig
         选项
         设置
         为
         ``y``
         以
         指示
         构建
         系统
         用
         这些
         分区
         做
         代码
         重定位。
         这个
         选项
         也
         可以
         在
         ``prj.conf``
         或
         任何
         其他
         Kconfig
         片段
         中
         设置。
      3. 构建
         并
         烧录
         设备
         上
         的
         SAM-BA
         bootloader。

   .. tab::
      带
      兼容
      SAM-BA
      bootloader

      对于
      这些
      设备，
      用户
      应该：

      1. 定义
         容纳
         bootloader
         和
         应用
         镜像
         所需
         的
         flash
         分区；
         细节
         见
         :ref:`flash_map_api`。
      2. 有
         开发板
         :file:`.defconfig`
         文件
         将
         :kconfig:option:`CONFIG_BOOTLOADER_BOSSA`
         Kconfig
         选项
         设置
         为
         ``y``。
         这
         将
         自动
         选择
         :kconfig:option:`CONFIG_USE_DT_CODE_PARTITION`
         Kconfig
         选项
         它
         指示
         构建
         系统
         用
         这些
         分区
         做
         代码
         重定位。
         开发板
         :file:`.defconfig`
         文件
         应该
         将
         :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_ARDUINO`、
         :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_ADAFRUIT_UF2`
         或
         :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_LEGACY`
         Kconfig
         选项
         设置
         为
         ``y``
         来
         选择
         正确
         的
         兼容
         SAM-BA
         bootloader
         模式。
         这些
         选项
         也
         可以
         在
         ``prj.conf``
         或
         任何
         其他
         Kconfig
         片段
         中
         设置。
      3. 构建
         并
         烧录
         设备
         上
         的
         SAM-BA
         bootloader。

.. note::

   :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_LEGACY`
   Kconfig
   选项
   应该
   作为
   最后
   手段
   使用。
   先
   尝试
   用
   不
   带
   ROM
   bootloader
   的
   设备
   配置。


典型
flash
布局
和
配置
--------------------------------------

对于
位于
flash
上
的
bootloader，
设备树
分区
布局
是
强制
的。
对于
有
ROM
bootloader
的
设备，
当
应用
使用
存储
或
其他
非
应用
分区
时
是
强制
的。
在
这个
特殊
情况
下，
应该
省略
boot
分区
且
code_partition
应该
从
偏移
0
开始。
必须
总是
定义
大小
避免
重叠
的
分区。

不
带
ROM
bootloader
的
设备
的
典型
flash
布局
是：

.. code-block:: devicetree

   /
   {
       chosen
       {
           zephyr,code-partition
           =
           &code_partition;
       };
   };

   &flash0
   {
       partitions
       {
           compatible
           =
           "fixed-partitions";
           #address-cells
           =
           <1>;
           #size-cells
           =
           <1>;

           boot_partition:
           partition@0
           {
               label
               =
               "sam-ba";
               reg
               =
               <0x00000000
               0x2000>;
               read-only;
           };

           code_partition:
           partition@2000
           {
               label
               =
               "code";
               reg
               =
               <0x2000
               0x3a000>;
               read-only;
           };

           /*
           *
           最后
           16
           KiB
           为
           应用
           保留。
           *
           存储
           分区
           如果
           启用
           将
           被
           FCB/LittleFS/NVS
           使用。
           */
           storage_partition:
           partition@3c000
           {
               label
               =
               "storage";
               reg
               =
               <0x0003c000
               0x00004000>;
           };
       };
   };

带
ROM
bootloader
和
存储
分区
的
设备
的
典型
flash
布局
是：

.. code-block:: devicetree

   /
   {
       chosen
       {
           zephyr,code-partition
           =
           &code_partition;
       };
   };

   &flash0
   {
       partitions
       {
           compatible
           =
           "fixed-partitions";
           #address-cells
           =
           <1>;
           #size-cells
           =
           <1>;

           code_partition:
           partition@0
           {
               label
               =
               "code";
               reg
               =
               <0x0
               0xF0000>;
               read-only;
           };

           /*
           *
           最后
           64
           KiB
           为
           应用
           保留。
           *
           存储
           分区
           如果
           启用
           将
           被
           FCB/LittleFS/NVS
           使用。
           */
           storage_partition:
           partition@F0000
           {
               label
               =
               "storage";
               reg
               =
               <0x000F0000
               0x00100000>;
           };
       };
   };


启用
SAM-BA
runner
----------------------

要
指示
Zephyr
west
工具
使用
SAM-BA
bootloader，
:file:`board.cmake`
文件
必须
有
``include(${ZEPHYR_BASE}/boards/common/bossac.board.cmake)``
条目。
注意
Zephyr
工具
接受
更多
条目
来
定义
多个
runner。
默认
情况
下，
第一个
将
在
使用
``west
flash``
命令
时
被
选择。
剩余
的
选项
通过
传递
runner
选项
可用，
例如
``west
flash
-r
bossac``。


更多
实现
细节
可以
在
:ref:`boards`
文档
中
找到。
作为
快速
参考，
见
这
三个
开发板
文档
页面：

  - :zephyr:board:`sam4e_xpro`
    （ROM
    bootloader）
  - :zephyr:board:`adafruit_feather_m0_basic_proto`
    （Adafruit
    UF2
    bootloader）
  - :zephyr:board:`arduino_nano_33_iot`
    （Arduino
    bootloader）
  - :zephyr:board:`arduino_nano_33_ble`
    （Arduino
    legacy
    bootloader）

在
Windows
Native
启用
BOSSAC
[实验性]
------------------------------------------------

Zephyr
SDK
的
bossac
当前
只
支持
Linux
和
macOS。
Windows
支持
可以
通过
使用
`BOSSA
官方
发布`_
的
bossac
版本
实现。
用
默认
选项
安装
后，
:file:`bossac.exe`
必须
被
添加
到
Windows
PATH。
可以
通过
传递
``--bossac``
选项
使用
特定
的
bossac
可
执行
文件，
如下：

.. code-block:: console

   west
   flash
   -r
   bossac
   --bossac="C:\Program
   Files
   (x86)\BOSSA\bossac.exe"
   --bossac-port="COMx"

.. note::

   WSL
   当前
   不
   受
   支持。


.. _linkserver-debug-host-tools:
.. _runner_linkserver:

LinkServer
Debug
Host
Tools
****************************

Linkserver
是
一个
用于
启动
和
管理
NXP
调试
探针
的
GDB
服务器
的
工具，
还
提供
命令行
目标
flash
编程
能力。
Linkserver
可以
与
`NXP
MCUXpresso
for
Visual
Studio
Code`_
实现
一起
使用，
与
基于
GNU
工具
的
自定义
调试
配置
一起
使用，
或
作为
持续
集成
和
测试
的
无
头
解决方案
的
部分。
LinkServer
可以
与
NXP
的
MCU-Link、
LPC-Link2、
基于
LPC11U35
和
基于
OpenSDA
的
独立
或
板载
调试
探针
一起
使用。

NXP
推荐
用
NXP
的
`MCUXpresso
Installer`_
安装
LinkServer。
这个
方法
也
将
安装
支持
以下
调试
探针
的
工具，
包括
NXP
的
MCU-Link
和
LPCScrypt
工具。

LinkServer
与
以下
调试
探针
兼容：

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`mcu-link-cmsis-onboard-debug-probe`
- :ref:`opensda-daplink-onboard-debug-probe`

要
用
West
命令
使用
LinkServer，
安装
文件夹
应该
被
添加
到
:envvar:`PATH`
:ref:`环境变量
<env_vars>`。
要
添加
的
默认
安装
路径
是：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

         /usr/local/LinkServer

   .. group-tab:: macOS

      .. code-block:: console

         /Applications/LinkServer_<version>

   .. group-tab:: Windows

      .. code-block:: console

         c:\nxp\LinkServer_<version>

受
支持
的
west
命令：

1. flash
#. debug
#. debugserver
#. attach

注意：


1. 探针
   可以
   用
   LinkServer
   列出：

.. code-block:: console

   LinkServer
   probes

2. 当
   多个
   调试
   探针
   连接
   到
   主机
   时，
   用
   LinkServer
   west
   runner
   的
   ``--probe``
   选项
   传递
   探针
   索引。

.. code-block:: console

   west
   flash
   --runner=linkserver
   --probe=3

3. 设备
   特定
   设置
   可以
   用
   LinkServer
   的
   west
   runner
   的
   '--override'
   选项
   覆盖。
   可以
   多次
   使用。
   格式
   由
   LinkServer
   规定，
   例如：

.. code-block:: console

   west
   flash
   --runner=linkserver
   --override
   /device/memory/5/flash-driver=MIMXRT500_SFDP_MXIC_OSPI_S.cfx

4. LinkServer
   不
   在
   reset
   handler
   安装
   隐式
   断点。
   如果
   你
   想
   从
   应用
   开始
   单步，
   你
   需要
   手动
   在
   ``main``
   或
   reset
   handler
   添加
   断点。

5. 那个
   断点，
   和
   任何
   其他
   GDB
   命令，
   可以
   用
   ``--gdb-init``
   自动
   安装，
   这
   个
   runner
   将
   它
   附加
   到
   ``west
   debug``
   和
   ``west
   attach``
   的
   GDB
   客户端，
   例如：

   .. code-block:: console

      west
      debug
      --runner=linkserver
      --gdb-init
      'b
      main'

   见
   :ref:`gdb-init-runner-option`。

.. _jlink-debug-host-tools:
.. _runner_jlink:

J-Link
Debug
Host
Tools
***********************

Segger
为
Linux、
macOS
和
Windows
操作
系统
提供
一
套
调试
主机
工具：

- J-Link
  GDB
  Server:
  GDB
  远程
  调试
- J-Link
  Commander:
  命令行
  控制
  和
  flash
  编程
- RTT
  Viewer:
  RTT
  终端
  输入
  和
  输出
- SystemView:
  实时
  事件
  可视化
  和
  记录

这些
调试
主机
工具
与
以下
调试
探针
兼容：

- :ref:`lpclink2-jlink-onboard-debug-probe`
- :ref:`opensda-jlink-onboard-debug-probe`
- :ref:`mcu-link-jlink-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

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
Commander，
并
安装
关联
的
USB
设备
驱动。
RTT
Viewer
和
SystemView
可以
分开
下载，
但
不
是
必须
的。

注意
J-Link
GDB
server
还
不
支持
Zephyr
RTOS-awareness。

.. _gdb-init-runner-option:

传递
额外
GDB
命令
--------------------------

``jlink``
runner
接受
``--gdb-init``，
它
向
``west
debug``
和
``west
attach``
启动
的
GDB
客户端
附加
一个
命令。
选项
可以
多次
给出
且
命令
按
给定
顺序
运行，
最后
的
在
runner
发送
给
GDB
的
所有
东西
之后
且
在
目标
恢复
前。
由于
它们
只
是
附加
的，
它们
不
能
更改
runner
自己
的
connect、
load
和
reset
序列。
``west
flash``、
``west
reset``、
``west
rtt``
和
``west
debugserver``
不受
影响。

例如，
要
为
一个
调试
会话
的
持续
时间
启用
J-Link
semihosting：

.. code-block:: console

   west
   debug
   -r
   jlink
   --gdb-init
   'monitor
   semihosting
   enable'
   \
   --gdb-init
   'monitor
   semihosting
   basedir
   .'

相同
的
命令
可以
通过
添加
到
开发板
的
:file:`board.cmake`
成为
开发板
的
默认：

.. code-block:: cmake

   board_runner_args(jlink
   "--gdb-init=monitor
   semihosting
   enable")

注意
``--gdb-init``
只
到达
GDB
客户端。
J-Link
GDB
server
本身
的
选项
用
``--tool-opt``
传递，
烧录
时
运行
的
J-Link
Commander
命令
用
``--pre-script-cmd``
传递。

``linkserver``、
``openocd``
和
``intel_cyclonev``
runner
接受
相同
的
选项。
它
适用
于
哪些
命令，
以及
命令
在
哪里
插入，
取决于
每个
runner。

.. _openocd-debug-host-tools:
.. _runner_openocd:

OpenOCD
Debug
Host
Tools
************************

OpenOCD
是
一个
社区
开源
项目，
为
广泛
的
SoC
提供
GDB
远程
调试
和
flash
编程
支持。
Zephyr
SDK
包括
一个
添加
Zephyr
RTOS-awareness
的
fork；
否则
见
`Getting
OpenOCD`_
获取
从
官方
仓库
下载
OpenOCD
的
选项。

这些
调试
主机
工具
与
以下
调试
探针
兼容：

- :ref:`opensda-daplink-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查
你的
SoC
是否
列
在
`OpenOCD
Supported
Devices`_
中。

.. note:: 在
   Linux
   上，
   openocd
   通过
   `Zephyr
   SDK
   <https://github.com/zephyrproject-rtos/sdk-ng/releases>`_
   可用。
   Windows
   用户
   应该
   用
   以下
   步骤
   安装
   openocd：

   - 从
     这里
     下载
     Windows
     的
     openocd:
     `OpenOCD
     Windows`_
   - 复制
     bin
     和
     share
     目录
     到
     ``C:\Program
     Files\OpenOCD\``
   - 将
     ``C:\Program
     Files\OpenOCD\bin``
     添加
     到
     'PATH'
     环境变量

.. _pyocd-debug-host-tools:
.. _runner_pyocd:

pyOCD
Debug
Host
Tools
**********************

pyOCD
是
来自
Arm
的
开源
项目，
为
Arm
Cortex-M
SoC
提供
GDB
远程
调试
和
flash
编程
支持。
它
在
PyPi
上
分发
并
在你
完成
入门
指南
中
的
:ref:`gs_python_deps`
步骤
时
安装。
pyOCD
包括
对
Zephyr
RTOS-awareness
的
支持。

这些
调试
主机
工具
与
以下
调试
探针
兼容：

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`mcu-link-cmsis-onboard-debug-probe`
- :ref:`opensda-daplink-onboard-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查
你的
SoC
是否
列
在
`pyOCD
Supported
Devices`_
中。

.. _lauterbach-trace32-debug-host-tools:
.. _runner_trace32:

Lauterbach
TRACE32
Debug
Host
Tools
***********************************

`Lauterbach
TRACE32`_
是
一
条
微
处理器
开发
工具、
调试器
和
实时
追踪器
产品
线，
支持
JTAG、
SWD、
NEXUS
或
多
核心
架构
上
的
ETM，
包括
Arm
Cortex-A/-R/-M、
RISC-V、
Xtensa
等。
Zephyr
允许
用户
用
:ref:`west
<west-flashing>`
开发
和
编程
支持
Lauterbach
TRACE32
的
开发板。

runner
由
TRACE32
软件
的
一个
包装器
组成，
允许
Zephyr
开发板
为
受
支持
的
不同
命令
执行
自定义
启动
脚本
（Practice
Script），
包括
从
CMake
传递
额外
参数
的
能力。
由
使用
这个
runner
的
开发板
决定
定义
每个
命令
执行
的
操作。

安装
Lauterbach
TRACE32
软件
-----------------------------------

从
`Lauterbach
TRACE32
download
website`_
下载
Lauterbach
TRACE32
软件
（需要
注册）
并
遵循
`Lauterbach
TRACE32
Installation
Guide`_
中
描述
的
安装
步骤。

烧录
和
调试
----------------------

将
:ref:`环境变量
<env_vars>`
:envvar:`T32_DIR`
设置
为
TRACE32
系统
目录。
然后
执行
``west
flash``
或
``west
debug``
命令
来
烧录
或
调试
Zephyr
应用，
如
:ref:`west-build-flash-debug`
中
详细
描述
的。
``debug``
命令
启动
TRACE32
GUI
允许
调试
Zephyr
应用，
而
``flash``
命令
隐藏
GUI
并
在
后台
执行
所有
操作。

默认
情况
下，
``t32``
runner
将
用
位于
TRACE32
系统
目录
中
名为
``config.t32``
的
默认
配置
文件
启动
TRACE32。
要
使用
不同
的
配置
文件，
向
runner
提供
参数
``--config
CONFIG``，
例如：

.. code-block:: console

   west
   flash
   --config
   myconfig.t32

更多
选项，
运行
``west
flash
--context
-r
t32``
打印
用法。

Zephyr
RTOS
Awareness
---------------------

要
启用
Zephyr
RTOS
awareness
遵循
`Lauterbach
TRACE32
Zephyr
OS
Awareness
Manual`_
中
描述
的
步骤。

.. _nxp-s32-debug-host-tools:
.. _runner_nxp_s32dbg:

NXP
S32
Debug
Probe
Host
Tools
******************************

:ref:`nxp-s32-debug-probe`
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

下载
（需要
注册）
NXP
S32
Design
Studio
for
S32
Platform
并
遵循
`S32
Design
Studio
for
S32
Platform
Installation
User
Guide`_
获取
需要
的
调试
主机
工具
和
关联
的
USB
设备
驱动。

注意
NXP
S32
GDB
server
的
Zephyr
RTOS-awareness
支持
取决于
目标
设备。
咨询
产品
发布
说明
获取
更多
信息。

受
支持
的
west
命令：

1. debug
#. debugserver
#. attach

基本
使用
-----------

开始
前，
将
NXP
S32
Design
Studio
安装
目录
添加
到
系统
:ref:`PATH
环境变量
<env_vars>`。
或者，
它
可以
在
每次
调用
时
通过
``--s32ds-path``
传递
给
runner
如下
所示：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

         west
         debug
         --s32ds-path=/opt/NXP/S32DS.3.6

   .. group-tab:: Windows

      .. code-block:: console

         west
         debug
         --s32ds-path=C:\NXP\S32DS.3.6

如果
多个
S32
调试
探针
通过
USB
连接
到
主机，
runner
将
要求
用户
在
继续
前
通过
命令行
提示
选择
一个。
探针
的
连接
字符串
也
可以
在
调用
runner
时
通过
``--dev-id=<connection-string>``
指定。
咨询
NXP
S32
调试
探针
用户
手册
获取
如何
构造
连接
字符串
的
细节。
例如，
如果
使用
序列
ID
``00:04:9f:00:ca:fe``
的
探针：

.. code-block:: console

   west
   debug
   --dev-id='s32dbg:00:04:9f:00:ca:fe'

可以
通过
``--tool-opt``
向
调试
主机
工具
传递
额外
选项。
执行
``debug``
或
``attach``
命令
时，
工具
选项
只
传递
给
GDB
客户端。
执行
``debugserver``
时，
工具
选项
传递
给
GDB
服务器。
例如，
要
将
Zephyr
应用
加载
到
SRAM
并
之后
分离
调试
会话：

.. code-block:: console

   west
   debug
   --tool-opt='--batch'

要求
--------------

- **S32
  Design
  Studio
  版本**：
  3.6.0
  或
  更
  新。
- **S32DebugProbe
  OS
  （固件）**：
  1.1.0
  或
  更
  新。

S32
Debug
Probe
OS
升级
程序
------------------------------------

参考
`S32
Debug
Probe
User
Guide`_
中
的
"Reprogramming
S32
Debug
Probe
Firmware
Images"
章节
升级
S32DebugProbe
的
OS。

.. _runner_probe_rs:

probe-rs
Debug
Host
Tools
*************************

probe-rs
是
一个
用
Rust
编写
的
开源
嵌入式
工具
包。
它
为
各种
调试
探针
提供
开箱
即用
的
支持，
包括
CMSIS-DAP、
ST-Link、
SEGGER
J-Link、
FTDI
和
ESP32
设备
上
的
内置
USB-JTAG
接口。

更多
设置
细节
检查
`probe-rs
Installation`_。

检查
你的
SoC
是否
列
在
`probe-rs
Supported
Devices`_
中。

.. _runner_rfp:

Renesas
Flash
Programmer
（RFP）
Host
Tools
*****************************************

Renesas
提供
`Renesas
Flash
Programmer`_
作为
Renesas
开发板
的
官方
编程
工具，
使用
Renesas
标准
boot
固件。
它
以
GUI
和
CLI
形式
可用。

对于
配置
了
``rfp``
west
runner
的
开发板，
RFP
CLI
可以
轻松
使用
来
烧录
Zephyr。

受
支持
的
west
命令：

1. flash

下载
后，
如果
``rfp-cli``
没有
放
在
你
系统
PATH
的
某
处，
你
可以
在
烧录
时
向
``rfp-cli``
传递
位置：

.. code-block:: console

   west
   flash
   --rfp-cli
   ~/Downloads/RFP_CLI_Linux_V31800_x64/linux-x64/rfp-cli

.. _stm32cubeclt-host-tools:
.. _runner_stlink_gdbserver:

STM32CubeCLT
Flash
&
Debug
Host
Tools
*************************************

STMicroelectronics
提供
`STM32CubeCLT`_
作为
兼容
Linux®、
macOS®
和
Windows®
的
官方
一体
工具
集，
允许
在
第三方
开发
环境
中
使用
STMicroelectronics
专有
工具。

它
特别
提供
一个
GDB
调试
服务器
（*ST-LINK
GDB
Server*），
可以
用
板载
或
外部
ST-LINK
调试
探针
调试
STM32
开发板
上
的
应用。

它
与
以下
调试
探针
兼容：

- :ref:`stlink-v21-onboard-debug-probe`
- 独立
  `ST-LINK-V2`_、
  `ST-LINK-V3`_
  和
  `STLINK-V3PWR`_
  探针

安装
STM32CubeCLT
--------------------

获取
ST-LINK
GDB
Server
的
最
简单
方式
是
从
STMicroelectronics
网站
安装
`STM32CubeCLT`_。
需要
一个
有效
的
邮件
地址
来
接收
下载
链接。

基本
使用
-----------

ST-Link
GDB
Server
可以
通过
``west
attach``、
``west
debug``
或
``west
debugserver``
命令
使用
来
调试
Zephyr
应用。

.. code-block:: console

   west
   debug
   --runner
   stlink_gdbserver

.. note::

   `STM32CubeCLT`_
   安装
   中
   包含
   的
   `STM32CubeProgrammer`_
   版本
   也
   可以
   用
   来
   烧录
   应用。
   要
   做
   这，
   应该
   用
   专用
   的
   :ref:`STM32CubeProgrammer
   runner
   <runner_stm32cubeprogrammer>`
   替代
   ``stlink_gdbserver``，
   如
   以下
   示例
   中
   做
   的：

   .. code-block:: console

      west
      flash
      --runner
      stm32cubeprogrammer

.. _stm32cubeprog-flash-host-tools:
.. _runner_stm32cubeprogrammer:

STM32CubeProgrammer
Flash
Host
Tools
************************************

STMicroelectronics
提供
`STM32CubeProgrammer`_
（STM32CubeProg）
作为
STM32
开发板
在
Linux®、
macOS®
和
Windows®
操作
系统
上
的
官方
编程
工具。

它
提供
一个
易
用
和
高效
的
环境
用于
通过
调试
接口
（JTAG
和
SWD）
和
bootloader
接口
（UART
和
USB
DFU、
I2C、
SPI
和
CAN）
读取、
写入
和
验证
设备
内存。

它
提供
广泛
的
功能
用于
编程
STM32
内部
内存
（如
flash、
RAM
和
OTP）
以及
外部
内存。

它
还
允许
选项
编程
和
上传、
编程
内容
验证、
以及
通过
脚本
的
编程
自动化。

它
以
GUI
（图形
用户
接口）
和
CLI
（命令行
接口）
版本
提供。

它
与
以下
调试
探针
兼容：

- :ref:`stlink-v21-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- 独立
  `ST-LINK-V2`_、
  `ST-LINK-V3`_
  和
  `STLINK-V3PWR`_
  探针

安装
STM32CubeProgrammer
---------------------------

获取
`STM32CubeProgrammer`_
的
最
简单
方式
是
从
STMicroelectronics
网站
下载。
需要
一个
有效
的
邮件
地址
来
接收
下载
链接。

或者，
它
可以
作为
`STM32CubeCLT`_
一体
多
OS
命令行
工具
集
的
部分
安装，
该
工具
集
还
包括
GDB
调试器
客户端
和
服务器。

如果
你
系统
上
有
STM32CubeIDE
安装，
那么
STM32CubeProg
已经
存在。

基本
使用
-----------

`STM32CubeProgrammer`_
设置
为
Zephyr
支持
的
所有
活跃
STM32
开发板
的
默认
west
runner。
它
可以
通过
``west
flash``
命令
使用
来
烧录
Zephyr
应用。

.. code-block:: console

   west
   flash
   --runner
   stm32cubeprogrammer

高级
使用
通过
GUI
或
CLI，
检查
`STM32CubeProgrammer
User
Manual`_。

.. _runner_xsdb:

XSDB
Flash
&
Debug
Host
Tools
*****************************

AMD
XSDB
工具
（Xilinx
Software
Command-line
Tool
for
Debug）
是
用于
编程
和
调试
许多
AMD
adaptive
SoC
和
FPGA
平台
的
命令行
工具。
它
**不**
包括
在
Zephyr
SDK
中：
安装
`AMD
Vitis`_
（或
你
平台
的
等价
AMD
工具链
分发）
并
确保
``xsdb``
可
执行
文件
在
你
系统
:ref:`PATH
<env_vars>`
上。

选择
``xsdb``
west
runner
的
开发板
通常
在
开发板
定义
旁边
附带
开发板
特定
的
``support/xsdb.cfg``。
见
你
开发板
的
文档
获取
需要
的
boot
制品
（PDI、
bitstream、
FSBL
等）。

受
支持
的
west
命令
包括
``flash``、
``debug``
和
``debugserver``。

对于
这个
runner，
``west
debug``
和
``west
debugserver``
都
启动
相同
的
本地
XSDB
交互
会话。
与
基于
GDB
的
runner
不同
（那里
``debugserver``
为
IDE
启动
一个
远程
stub），
xsdb
runner
总是
直接
启动
XSDB，
通过
开发板
``xsdb.cfg``
加载
应用，
并
让
你
在
XSDB
提示符
处。

.. code-block:: console

   west
   flash
   --runner
   xsdb

   west
   debug
   --runner
   xsdb

   west
   debugserver
   --runner
   xsdb

.. note::

   这
   与
   本
   章
   其他
   专有
   主机
   工具
   （例如
   :ref:`J-Link
   <jlink-debug-host-tools>`
   或
   :ref:`STM32CubeCLT
   <stm32cubeclt-host-tools>`）
   是
   相同
   类
   的
   依赖：
   Zephyr
   通过
   west
   runner
   与
   工具
   集成；
   获取
   和
   许可
   工具链
   是
   用户
   的
   责任。

.. _runner_uf2:

UF2
Uploader
************

uf2
runner
支持
用
UF2
（USB
Flashing
Format）
烧录
某些
开发板。
UF2
是
一个
用户
友好
的
文件
格式，
设计
用于
通过
USB
大容量
存储
设备
拖放
编程。

它
依赖
目标
设备
进入
一个
特殊
bootloader
模式
其中
它
对
主机
出现
为
USB
大容量
存储
设备。
进入
这个
模式
后，
应用
镜像
可以
通过
将
``.uf2``
文件
复制
到
挂载
的
卷
上传。

.. code-block:: console

   west
   flash
   --runner
   uf2

如果
UF2
卷
不
自动
检测，
你
可能
需要
用
``--device``
选项
手动
指定
挂载
点：

关于
UF2
格式
和
其
工具
的
更多
信息，
见
`USB
Flashing
Format
（UF2）`_。

.. _runner_rtkprog:

Realtek
Alternate
Flash
Programmer
（rtkprog）
********************************************

``rtkprog``
是
用
UART
烧录
Realtek
Bee
家族
SoC
所需
协议
的
开源
实现。

.. code-block:: console

   west
   flash
   --runner
   rtkprog

.. _rtkprog
   源
   代码:
   https://github.com/a-labs-io/rtkprog
.. _rtkprog
   Python
   包:
   https://pypi.org/p/rtkprog


.. _runner_mpcli:

Realtek
Bee
Flash
Programmer
（MPCli）
Host
Tools
***********************************************

Realtek
提供
`Realtek
Flash
Programmer
（MPCli）`_
作为
Bee
系列
的
官方
编程
工具，
支持
Linux、
macOS
和
Windows
操作
系统。
MPCli
通过
UART
接口
启用
系统
内
编程
（ISP），
消除
对
外部
编程
硬件
的
需要。
在
大多数
官方
Bee
系列
评估
开发板
上，
包括
内置
的
UART
到
USB
转换器
用于
开箱
即用
的
编程
和
日志。

下载
MPCli
的
归档
后，
解压
它
并
选择
与
你
操作
系统
兼容
的
版本。
然后，
将
包含
``mpcli``
可
执行
文件
的
目录
添加
到
你
系统
:ref:`PATH
环境变量
<env_vars>`。

开始
前，
确保
你
的
开发板
在
download
模式。
请
参考
开发板
文档
在：
`Realtek
Supported
Boards`_

.. code-block:: console

   west
   flash
   [--runner
   mpcli]
   --port
   /dev/ttyX


.. _iar-debug-host-tools:
.. _runner_iar:

IAR
EW
&
C-Spy
Host
Tools
*************************

IAR
提供
Embedded
Workbench
和
CSpyBat
用于
调试
和
烧录。
iar
runner
与
EWARM
10.10
或
更
新
的
一起
工作。

.. _AMD
   Vitis:
   https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vitis.html

.. _J-Link
   Software
   and
   Documentation
   Pack:
   https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack

.. _J-Link
   Supported
   Devices:
   https://www.segger.com/downloads/supported-devices.php

.. _Getting
   OpenOCD:
   https://openocd.org/pages/getting-openocd.html

.. _OpenOCD
   Supported
   Devices:
   https://github.com/zephyrproject-rtos/openocd/tree/latest/tcl/target

.. _pyOCD
   Supported
   Devices:
   https://github.com/pyocd/pyOCD/tree/main/pyocd/target/builtin

.. _OpenOCD
   Windows:
   https://gnutoolchains.com/arm-eabi/openocd/

.. _Lauterbach
   TRACE32:
   https://www.lauterbach.com/

.. _Lauterbach
   TRACE32
   download
   website:
   https://www.lauterbach.com/download_trace32.html

.. _Lauterbach
   TRACE32
   Installation
   Guide:
   https://www2.lauterbach.com/pdf/installation.pdf

.. _Lauterbach
   TRACE32
   Zephyr
   OS
   Awareness
   Manual:
   https://www2.lauterbach.com/pdf/rtos_zephyr.pdf

.. _BOSSA
   官方
   发布:
   https://github.com/shumatech/BOSSA/releases

.. _NXP
   MCUXpresso
   for
   Visual
   Studio
   Code:
   https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-for-visual-studio-code:MCUXPRESSO-VSC

.. _MCUXpresso
   Installer:
   https://mcuxpresso.nxp.com/mcux-vscode/latest/html/MCUXpresso-Installer.html

.. _NXP
   S32
   Design
   Studio
   for
   S32
   Platform:
   https://www.nxp.com/design/software/development-software/s32-design-studio-ide/s32-design-studio-for-s32-platform:S32DS-S32PLATFORM

.. _Renesas
   Flash
   Programmer:
   https://www.renesas.com/en/software-tool/renesas-flash-programmer-programming-gui

.. _S32
   Design
   Studio
   for
   S32
   Platform
   Installation
   User
   Guide:
   https://www.nxp.com/webapp/Download?colCode=S32DSIG

.. _S32
   Debug
   Probe
   User
   Guide:
   https://www.nxp.com/docs/en/user-guide/S32DBGUG.pdf

.. _probe-rs
   Installation:
   https://probe.rs/docs/getting-started/installation/

.. _probe-rs
   Supported
   Devices:
   https://probe.rs/targets/

.. _STM32CubeCLT:
   https://www.st.com/en/development-tools/stm32cubeclt.html

.. _STM32CubeProgrammer:
   https://www.st.com/en/development-tools/stm32cubeprog.html

.. _STM32CubeProgrammer
   User
   Manual:
   https://www.st.com/resource/en/user_manual/um2237-stm32cubeprogrammer-software-description-stmicroelectronics.pdf

.. _ST-LINK-V2:
   https://www.st.com/en/development-tools/st-link-v2.html

.. _ST-LINK-V3:
   https://www.st.com/en/development-tools/stlink-v3set.html

.. _STLINK-V3PWR:
   https://www.st.com/en/development-tools/stlink-v3pwr.html

.. _USB
   Flashing
   Format
   （UF2）:
   https://github.com/microsoft/uf2

.. _Realtek
   Flash
   Programmer
   （MPCli）:
   https://docs.realmcu.com/tools/mpcli_tool/en/latest/mpcli/text_en/README.html

.. _Realtek
   Supported
   Boards:
   https://docs.zephyrproject.org/latest/boards/realtek/index.html
