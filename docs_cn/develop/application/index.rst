.. _application:

应用
开发
#######################

.. note::

   在
   本文档
   中，
   我们
   假设：

   - 你的
     **应用
     目录**，
     :file:`<app>`，
     是
     类似
     :file:`<home>/zephyrproject/app`
     的
     东西
   - 其
     **构建
     目录**
     是
     :file:`<app>/build`

   这些
   术语
   在
   下面
   定义。
   在
   Linux/macOS
   上，
   <home>
   等价
   于
   ``~``。
   在
   Windows
   上，
   它
   是
   ``%userprofile%``。

   将
   你的
   应用
   保持
   在
   工作区
   （:file:`<home>/zephyrproject`）
   内
   使
   使用
   ``west
   build``
   和
   其他
   命令
   配合
   它
   更
   容易。
   （你
   可以
   把
   应用
   放
   在
   任何
   地方
   只要
   :ref:`ZEPHYR_BASE
   <important-build-vars>`
   被
   适当
   设置，
   尽管
   这样。）

概览
********

Zephyr
的
构建
系统
基于
`CMake`_。

构建
系统
是
应用
中心
的，
并
要求
基于
Zephyr
的
应用
发起
构建
Zephyr
源
代码。
应用
构建
控制
应用
和
Zephyr
本身
两者
的
配置
和
构建
过程，
将
它们
编译
成
单个
二进制
文件。

主
zephyr
仓库
包含
Zephyr
的
源
代码、
配置
文件
和
构建
系统。
你
也
很可能
安装
了
各种
:ref:`模块`
与
zephyr
仓库
一起，
它们
提供
第三方
源
代码
集成。

**应用
目录**
中
的
文件
将
Zephyr
和
任何
模块
与
应用
链接。
这个
目录
包含
所有
应用
特定
文件，
如
应用
特定
配置
文件
和
源
代码。

这里
是
简单
Zephyr
应用
中
的
文件：

.. code-block:: none

   <app>
   ├──
   CMakeLists.txt
   ├──
   app.overlay
   ├──
   prj.conf
   ├──
   VERSION
   └──
   src
       └──
       main.c

这些
内容
是：

* **CMakeLists.txt**：
  这个
  文件
  告诉
  构建
  系统
  哪里
  找到
  其他
  应用
  文件，
  并
  将
  应用
  目录
  与
  Zephyr
  的
  CMake
  构建
  系统
  链接。
  这个
  链接
  提供
  Zephyr
  构建
  系统
  支持
  的
  功能，
  如
  开发板
  特定
  配置
  文件、
  在
  真实
  或
  仿真
  硬件
  上
  运行
  和
  调试
  编译
  后
  二进制
  文件
  的
  能力
  等。

* **app.overlay**：
  这
  是
  一个
  设备树
  覆盖
  文件，
  指定
  应该
  应用
  到
  你
  构建
  目标
  的
  任何
  开发板
  基础
  设备树
  的
  应用
  特定
  更改。
  设备树
  覆盖
  的
  目的
  通常
  是
  配置
  应用
  使用
  的
  硬件
  的
  某些
  东西。

  构建
  系统
  默认
  查找
  :file:`app.overlay`，
  但
  你
  可以
  添加
  更多
  设备树
  覆盖，
  其他
  默认
  文件
  也
  被
  搜索。

  关于
  设备树
  的
  更多
  信息
  见
  :ref:`devicetree`。

* **prj.conf**：
  这
  是
  一个
  Kconfig
  片段，
  指定
  一个
  或多个
  Kconfig
  选项
  的
  应用
  特定
  值。
  这些
  应用
  设置
  与
  其他
  设置
  合并
  以
  产生
  最终
  配置。
  Kconfig
  片段
  的
  目的
  通常
  是
  配置
  应用
  使用
  的
  软件
  功能。

  构建
  系统
  默认
  查找
  :file:`prj.conf`，
  但
  你
  可以
  添加
  更多
  Kconfig
  片段，
  其他
  默认
  文件
  也
  被
  搜索。

  关于
  这个
  文件
  和
  如何
  使用
  它
  的
  更多
  信息
  见
  :ref:`app-version-details`。

* **VERSION**：
  一个
  包含
  几个
  版本
  信息
  字段
  的
  文本
  文件。
  这些
  字段
  让
  你
  管理
  应用
  的
  生命周期
  并
  在
  签名
  应用
  镜像
  时
  自动
  提供
  应用
  版本。

  关于
  这个
  文件
  和
  如何
  使用
  它
  的
  更多
  信息
  见
  :ref:`app-version-details`。

* **main.c**：
  一个
  源
  代码
  文件。
  应用
  通常
  包含
  用
  C、
  C++
  或
  汇编
  语言
  编写
  的
  源
  文件。
  Zephyr
  约定
  是
  将
  它们
  放
  在
  :file:`<app>`
  中
  名为
  :file:`src`
  的
  子
  目录
  中。

一旦
应用
被
定义，
构建
系统
就
可以
构建
它。
应用
构建
控制
应用
和
Zephyr
本身
两者
的
配置
和
构建
过程。

构建
应用
****************

构建
应用
的
首选
方式
是
使用
:ref:`west
build
<west-building>`
命令。
它
接受
开发板
名称
和
应用
目录
作为
参数：

.. code-block:: console

   west
   build
   -b
   <board>
   <app>

构建
系统
将
应用
配置
与
Zephyr
配置
合并
并
构建
所有
源
代码
成
单个
二进制
文件。

构建
过程
产生
几个
输出
文件
在
构建
目录
中：

.. code-block:: none

   <app>/build
   ├──
   zephyr
   │   ├──
   │   zephyr.elf
   │   ├──
   │   zephyr.bin
   │   ├──
   │   zephyr.hex
   │   └──
   │   zephyr.map
   └──
   ...

.. _application-kconfig:

Kconfig
配置
****************

应用
可以
有
一个
或多个
Kconfig
片段
文件
来
配置
Zephyr
的
软件
功能。
默认
的
Kconfig
片段
文件
是
:file:`prj.conf`。

Kconfig
片段
是
普通
文本
文件，
包含
一个
或多个
Kconfig
选项
赋值。
每个
赋值
是
一行，
格式
为：

.. code-block:: cfg

   CONFIG_<option
   name>=<value>

例如，
启用
日志
的
Kconfig
片段
可能
像
这样：

.. code-block:: cfg

   CONFIG_LOG=y
   CONFIG_LOG_DEFAULT_LEVEL=3

构建
系统
将
应用
Kconfig
片段
与
开发板
默认
配置
和
其他
设置
合并
以
产生
最终
Kconfig
配置。
最终
配置
保存
到
构建
目录
中
的
:file:`zephyr/.config`
文件。

可以
用
``west
build
--
-DCONF_FILE=<file>``
指定
额外
的
Kconfig
片段
文件。

.. _application-devicetree:

设备树
配置
****************

应用
可以
有
一个
或多个
设备树
覆盖
文件
来
配置
硬件。
默认
的
设备树
覆盖
文件
是
:file:`app.overlay`。

设备树
覆盖
是
普通
文本
文件，
包含
一个
或多个
设备树
节点
或
属性
赋值。
构建
系统
将
应用
设备树
覆盖
与
开发板
基础
设备树
合并
以
产生
最终
设备树。

可以
用
``west
build
--
-DEXTRA_DTC_OVERLAY_FILE=<file>``
指定
额外
的
设备树
覆盖
文件。

设备树
源
通过
C
预
处理器
传递，
因此
你
可以
包含
可以
位于
``DTS_ROOT``
目录
中
的
文件。
按
约定
设备树
包含
文件
有
``.dtsi``
扩展名。

你
也
可以
用
预
处理器
控制
设备树
文件
的
内容，
通过
``DTS_EXTRA_CPPFLAGS``
CMake
Cache
变量
指定
指令：

.. zephyr-app-commands::
   :tool:
   all
   :board:
   <board
   name>
   :gen-args:
   -DDTS_EXTRA_CPPFLAGS=-DTEST_ENABLE_FEATURE
   :goals:
   build
   :compact:

.. _CMake:
   https://www.cmake.org
.. _CMake
   介绍:
   https://cmake.org/cmake/help/latest/manual/cmake.1.html#description
.. _CMake
   列表:
   https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#lists
.. _示例
   应用:
   https://github.com/zephyrproject-rtos/example-application
