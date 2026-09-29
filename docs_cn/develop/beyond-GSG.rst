.. _beyond-gsg:

超越
入门
指南
################################

:ref:`getting_started` 给出
一条
直接
的
路径
来
设置
你的
Linux、macOS 或
Windows 环境
用于
Zephyr 开发。
在
本文档
中，
我们
深入
探讨
Zephyr 开发
设置
问题
和
替代
方案。

.. _python-pip:

Python 和
pip
**************

Python 3 和
其
包
管理器
pip\ [#pip]_ 被
Zephyr
广泛
使用
来
安装
和
运行
编译
和
运行
Zephyr
应用
所需
的
脚本，
设置
和
维护
Zephyr
开发
环境，
以及
构建
项目
文档。

根据
你的
操作
系统，
你
可能
需要
在
安装
新
包
时
向
``pip3`` 命令
提供
``--user`` 标志。
这
在
说明
中
贯穿
记录。
关于
pip\ [#pip]_ 的
更多
信息，
包括
`关于
-\-user
的信息`_，
见
Python
打包
用户
指南
中的
`安装
包`_。

- 在
  Linux 上，
  确保
  ``~/.local/bin`` 在
  :envvar:`PATH`
  :ref:`环境变量 <env_vars>` 的
  开头，
  否则
  用
  ``--user`` 安装
  的
  程序
  将
  找不到。
  用
  ``--user`` 安装
  避免
  pip
  和
  系统
  包
  管理器
  之间
  的
  冲突，
  并
  是
  基于
  Debian
  的
  发行版
  的
  默认
  值。

- 在
  macOS 上，
  `Homebrew
  禁用
  -\--user`_。

- 在
  Windows 上，
  如果
  你
  需要
  使用
  这个
  选项，
  见
  `安装
  包`_ 中
  关于
  ``--user`` 的
  信息。

在
所有
操作
系统
上，
pip
的
``-U`` 标志
在
包
已经
本地
安装
但
有
更
新
版本
可用
时
安装
或
更新
包。
如果
需要
包
的
最新
版本，
使用
这个
标志
是
好
的
实践。
（检查
:zephyr_file:`scripts/requirements.txt` 文件
查看
是否
期望
特定
的
Python
包
版本。）

高级
平台
设置
***********************

这里
是
一些
替代
说明，
用于
受
支持
开发
平台
的
更
高级
平台
设置
配置：

.. toctree::
   :maxdepth: 1

   Linux
   设置
   替代
   方案
   <getting_started/installation_linux.rst>
   macOS
   设置
   替代
   方案
   <getting_started/installation_mac.rst>
   Windows
   设置
   替代
   方案
   <getting_started/installation_win.rst>

.. _gs_toolchain:

安装
工具链
*******************

Zephyr
二进制
文件
由
*工具链*
编译
和
链接，
它
由
交叉
编译器
和
相关
工具
组成，
与
用于
开发
在
你的
主机
操作
系统
上
本地
运行
的
软件
的
编译器
和
工具
不同。

你
可以
安装
:ref:`Zephyr
SDK <toolchain_zephyr_sdk>` 获取
所有
受
支持
架构
的
工具链，
或
安装
SoC
厂商
或
特定
开发板
推荐
的
:ref:`替代
工具链 <toolchains>`
（检查
你的
特定
:ref:`开发板
级
文档 <boards>`）。

你
可以
通过
设置
:ref:`环境变量 <env_vars>`
（如
:envvar:`ZEPHYR_TOOLCHAIN_VARIANT <{TOOLCHAIN}_TOOLCHAIN_PATH>`）
设置
为
受
支持
的
值，
连同
工具链
变体
特定
的
额外
变量
来
配置
Zephyr
构建
系统
使用
特定
工具链。

.. _gs_toolchain_update:

更新
Zephyr
SDK
工具链
*********************************

更新
Zephyr
SDK
时，
检查
:envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
或
:envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量
是否
已经
设置。

* 如果
  变量
  未
  设置，
  默认
  将
  选择
  最新
  兼容
  版本
  的
  Zephyr
  SDK。
  不
  做
  任何
  更改
  继续
  下一步。

* 如果
  :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
  已
  设置，
  构建
  时
  将
  选择
  对应
  工具链。
  Zephyr
  SDK
  由
  值
  ``zephyr`` 标识。
  如果
  :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 环境变量
  不
  是
  ``zephyr``，
  那么
  取消
  设置
  它
  或
  将
  其
  值
  更改
  为
  ``zephyr`` 确保
  选择
  Zephyr
  SDK。

* 如果
  :envvar:`ZEPHYR_SDK_INSTALL_DIR` 环境变量
  已
  设置，
  它
  将
  覆盖
  Zephyr
  SDK
  的
  默认
  查找
  位置。
  如果
  你
  将
  Zephyr
  SDK
  安装
  到
  :ref:`推荐
  位置 <toolchain_zephyr_sdk_bundle_variables>`
  之一，
  你
  可以
  取消
  设置
  这个
  变量。
  否则，
  将
  它
  设置
  为
  你
  选择
  的
  安装
  位置。

关于
这些
环境变量
在
Zephyr 中
的
更多
信息，
见
:ref:`env_vars_important`。

克隆
Zephyr
仓库
*******************************

Zephyr
项目
源
代码
维护
在
`GitHub
zephyr
仓库
<https://github.com/zephyrproject-rtos/zephyr>`_。
Zephyr
使用
的
外部
模块
位于
父
`GitHub
Zephyr
项目
<https://github.com/zephyrproject-rtos/>`_。
由于
这些
依赖
关系，
使用
Zephyr
创建
的
:ref:`west
<west>` 工具
获取
和
管理
Zephyr
和
外部
模块
源
代码
很
方便。
更多
细节
见
:ref:`west-basics`。

安装
开发
工具
后，
使用
:ref:`west` 创建、
初始化
和
从
zephyr
和
外部
模块
仓库
下载
源
代码。
我们
将
使用
名称
``zephyrproject``，
但
你
可以
选择
任何
不
包含
空格
的
名称。

.. code-block:: console

   west init zephyrproject
   cd zephyrproject
   west update

``west update`` 命令
获取
并
保持
:ref:`模块`
与
本地
zephyr
仓库
中
的
代码
同步
在
:file:`zephyrproject` 文件夹
中。

.. warning::

   每次
   :file:`zephyr/west.yml`
   更改
   时
   你
   必须
   运行
   ``west update``，
   例如
   当
   你
   拉取
   :file:`zephyr`
   仓库、
   在
   其中
   切换
   分支、
   或
   在
   其中
   执行
   ``git bisect`` 时。

保持
Zephyr
更新
=====================

要
更新
Zephyr
项目
源
代码，
你
需要
通过
``git`` 获取
最新
更改。
之后，
如
前
一段
所述
运行
``west update``。
此外，
检查
更新
或
添加
的
Python
依赖。

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         # 将
         # zephyrproject
         # 替换
         # 为
         # 你
         # 给
         # west
         # init
         # 的
         # 路径
         cd zephyrproject/zephyr
         git pull
         west update
         west packages pip --install

   .. group-tab:: Windows

      .. tabs::

         .. code-tab:: bat

            :: 将
            :: zephyrproject
            :: 替换
            :: 为
            :: 你
            :: 给
            :: west
            :: init
            :: 的
            :: 路径
            cd zephyrproject\zephyr
            git pull
            west update
            cmd /c scripts\utils\west-packages-pip-install.cmd

         .. code-tab:: powershell

            # 将
            # zephyrproject
            # 替换
            # 为
            # 你
            # 给
            # west
            # init
            # 的
            # 路径
            cd zephyrproject\zephyr
            git pull
            west update
            python -m pip install @((west packages pip) -split ' ')

导出
Zephyr
CMake
包
***************************

如果
还
没有
作为
:ref:`getting_started` 的
一部分
完成，
:ref:`cmake_pkg`
可以
被
导出
到
CMake
的
用户
包
注册表。

.. _gs-board-aliases:

开发板
别名
*************

与
多个
开发板
工作
的
开发者
可能
觉得
显式
开发板
名称
麻烦
并
希望
为
通用
目标
使用
别名。
这
由
一个
CMake
文件
支持，
内容
像
这样：

.. code-block:: cmake

   # 变量
   # foo_BOARD_ALIAS=bar
   # 将
   # BOARD=foo
   # 替换
   # 为
   # BOARD=bar
   # 并
   # 在
   # CMake
   # 缓存
   # 中
   # 设置
   # BOARD_ALIAS=foo。
   set(pca10028_BOARD_ALIAS nrf51dk/nrf51822)
   set(pca10056_BOARD_ALIAS nrf52840dk/nrf52840)
   set(k64f_BOARD_ALIAS frdm_k64f)
   set(sltb004a_BOARD_ALIAS efr32mg_sltb004a)

并
在
:envvar:`ZEPHYR_BOARD_ALIASES` 中
指定
其
位置。
这
允许
在
``cmake -DBOARD=pca10028`` 和
``west -b pca10028`` 这样
的
上下文
中
使用
别名
``pca10028``。

构建
和
运行
应用
****************************

你
可以
在
真实
硬件
上
使用
受
支持
的
主机
系统
构建、
烧录
和
运行
Zephyr
应用。
根据
你的
操作
系统，
你
还
可以
用
QEMU
在
仿真
中
运行
它，
或
用
:zephyr:board:`native_sim <native_sim>` 作为
本地
应用
运行。
关于
构建
应用
的
更多
信息
可以
在
:ref:`build_an_application` 章节
找到。

构建
Blinky
=============

让我们
构建
:zephyr:code-sample:`blinky` 示例
应用。

Zephyr
应用
被
构建
为
在
特定
硬件
上
运行，
称为
"开发板"\ [#board_misnomer]_。
我们
这里
使用
Phytec
:zephyr:board:`reel_board<reel_board>`，
但
如果
你
有
不同
的
开发板，
你
可以
将
``reel_board`` 构建
目标
更改
为
其他
值。
见
:ref:`boards` 或
在
``zephyrproject`` 目录
内
任何
地方
运行
``west boards`` 获取
受
支持
开发板
的
列表。

#. 进入
   zephyr
   仓库：

   .. code-block:: console

      cd zephyrproject/zephyr

#. 为
   ``reel_board`` 构建
   blinky
   示例：

   .. zephyr-app-commands::
      :zephyr-app: samples/basic/blinky
      :board: reel_board
      :goals: build

主要
构建
产物
将
在
:file:`build/zephyr`；
:file:`build/zephyr/zephyr.elf` 是
ELF
格式
的
blinky
应用
二进制
文件。
根据
你的
开发板，
可能
存在
其他
二进制
格式、
反
汇编
和
map
文件。

:zephyr_file:`samples` 文件夹
中
的
其他
示例
应用
在
:zephyr:code-sample-category:`samples` 中
记录。

.. note:: 如果
   你
   想
   为
   其他
   开发板
   或
   应用
   重用
   现有
   构建
   目录，
   你
   需要
   向
   ``west build`` 添加
   参数
   ``-p=auto`` 清理
   之前
   构建
   的
   设置
   和
   产物。

通过
烧录
到
开发板
运行
应用
==========================================

Zephyr
支持
的
大多数
硬件
开发板
可以
通过
运行
``west flash`` 烧录。
这
可能
需要
开发板
特定
工具
安装
和
配置
才能
正常
工作。

更多
细节
见
:ref:`application_run` 和
:ref:`boards` 中
你的
特定
开发板
的
文档。

.. _setting-udev-rules:

设置
udev
规则
==================

烧录
开发板
需要
直接
访问
开发板
硬件
的
权限，
通常
由
烧录
工具
安装
管理。
在
Linux
系统
上，
如果
``west flash`` 命令
失败，
你
很可能
需要
定义
udev
规则
来
授予
需要
的
访问
权限。

Udev
是
Linux
内核
的
设备
管理器，
udev
守护
程序
处理
硬件
设备
添加
（或
移除）
到
系统
时
引发
的
所有
用户
空间
事件。
我们
可以
添加
一个
规则
文件
来
授予
非
root
用户
对
某些
USB
连接
设备
的
访问
权限。

OpenOCD（On-Chip
Debugger）
项目
方便
地
提供
了
一个
规则
文件，
为
大多数
Zephyr
支持
的
基于
arm
的
开发板
定义
了
开发板
特定
规则，
因此
我们
推荐
通过
从
其
sourceforge
仓库
下载
安装
这个
规则
文件，
或
如果
你
安装
了
Zephyr
SDK，
SDK
文件夹
中
有
这个
规则
文件
的
副本：

* 要么
  下载
  OpenOCD
  规则
  文件
  并
  复制
  到
  正确
  位置::

     wget -O 60-openocd.rules https://sf.net/p/openocd/code/ci/master/tree/contrib/60-openocd.rules?format=raw
     sudo cp 60-openocd.rules /etc/udev/rules.d

* 要么
  从
  Zephyr
  SDK
  文件夹
  复制
  规则
  文件::

     sudo cp ${ZEPHYR_SDK_INSTALL_DIR}/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d

然后，
两种
情况
都
要求
udev
守护
程序
重新
加载
这些
规则::

   sudo udevadm control --reload

拔下
再
插上
到
开发板
的
USB
连接，
你
应该
有
权限
访问
开发板
硬件
用于
烧录。
如果
需要，
检查
你的
开发板
特定
文档
（:ref:`boards`）
获取
更多
信息。

在
QEMU
中
运行
应用
===========================

当
目标
是
x86 或
ARM
Cortex-M3
架构
时，
你
可以
用
`QEMU <https://www.qemu.org/>`_
在
主机
系统
上
通过
仿真
运行
Zephyr
应用。
QEMU
包含
在
Zephyr
SDK
中。

如果
使用
手动
QEMU
安装，
确保
它
在
系统
``PATH`` 环境变量
中
可用。

``QEMU_BIN_PATH``
可以
作为
可选
覆盖
使用
来
指定
Twister
使用
的
QEMU
二进制
文件
位置。
提供
时，
Twister
验证
指定
的
路径
存在。
否则，
Twister
依赖
SDK
或
其他
QEMU
发现
机制。

例如，
你
可以
用
x86
仿真
开发板
配置
（``qemu_x86``）
构建
并
运行
:zephyr:code-sample:`hello_world` 示例：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: qemu_x86
   :goals: build run

要
退出
QEMU，
键入
:kbd:`Ctrl-a`，
然后
:kbd:`x`。

用
``qemu_cortex_m3`` 目标
仿真
的
Arm
Cortex-M3
示例。

.. _gs_native:

本地
运行
示例
应用
（Linux）
=========================================

你
可以
编译
某些
示例
作为
主机
程序
在
Linux
上
运行。
更多
信息
见
:zephyr:board:`native_sim`。
在
64 位
主机
操作
系统
上，
你
需要
安装
32 位
C
库，
或
目标
为
:ref:`native_sim/native/64<native_sim32_64>` 构建。

首先，
为
``native_sim`` 构建
Hello
World。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :host-os: unix
   :board: native_sim
   :goals: build

接下来，
运行
应用。

.. code-block:: console

   west build -t run
   # 或
   # 直接
   # 运行
   # zephyr.exe：
   ./build/zephyr/zephyr.exe

按
:kbd:`Ctrl-C` 退出。

你
可以
运行
``./build/zephyr/zephyr.exe --help`` 获取
可用
选项
列表。

这个
可
执行
文件
可以
用
标准
工具
（如
gdb 或
valgrind）
插桩。

.. rubric:: 脚注

.. [#pip]

   pip
   是
   Python
   的
   包
   安装
   器。
   其
   ``install`` 命令
   首先
   尝试
   重用
   已
   安装
   在
   你
   电脑
   上
   的
   包
   和
   包
   依赖。
   如果
   不
   可能，
   ``pip install``
   从
   互联网
   上
   的
   Python
   包
   索引
   （PyPI）
   下载
   它们。

   Zephyr
   的
   :file:`requirements.txt`
   请求
   的
   包
   版本
   可能
   与
   你
   系统
   上
   的
   其他
   要求
   冲突，
   在
   这种
   情况
   下
   你
   可能
   想
   为
   Zephyr
   开发
   设置
   一个
   virtualenv。

.. [#board_misnomer]

   这
   随
   时间
   变得
   有些
   名
   不
   副
   实。
   尽管
   目标
   可以
   （且
   经常
   是）
   运行
   在
   其
   自己
   专用
   硬件
   开发板
   上
   的
   微
   处理器，
   Zephyr
   也
   支持
   使用
   QEMU
   在
   仿真
   中
   运行
   为
   其他
   架构
   构建
   的
   目标，
   产生
   实现
   Zephyr
   驱动
   接口
   的
   本地
   主机
   系统
   二进制
   文件
   的
   目标，
   甚至
   在
   相同
   物理
   芯片
   上
   不同
   架构
   的
   CPU
   核心
   上
   运行
   不同
   的
   Zephyr
   基础
   二进制
   文件。
   每个
   这些
   硬件
   配置
   都
   称为
   "开发板"，
   尽管
   在
   上下文
   中
   这
   不
   总
   是
   完全
   合理。

.. _关于
   -\--user
   的
   信息:
   https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site
.. _Homebrew
   禁用
   -\--user:
   https://docs.brew.sh/Homebrew-and-Python#note-on-pip-install---user
.. _安装
   包:
   https://packaging.python.org/tutorials/installing-packages/
