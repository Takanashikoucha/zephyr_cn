.. _develop_debug:

调试
#########

.. _application_debugging:

应用
调试
*********************

这
一
节
是
一个
快速
实践
参考，
用于
开始
用
QEMU
调试
你的
应用。
这
一
节
的
大多数
内容
已经
在
`QEMU`_
和
`GNU_Debugger`_
参考
手册
中
覆盖。

.. _QEMU:
   https://wiki.qemu.org/Main_Page

.. _GNU_Debugger:
   https://www.gnu.org/software/gdb

在
这个
快速
参考
中，
你
将
找到
快捷
方式、
特定
环境变量
和
参数，
它们
可以
帮助
你
快速
设置
你的
调试
环境。

调试
在
QEMU
中
运行
的
应用
的
最
简单
方式
是
使用
GNU
Debugger
并
在
你的
开发
系统
中
通过
QEMU
设置
一个
本地
GDB
服务器。

你
将
需要
一个
:abbr:`ELF
（可
执行
和
可
链接
格式）`
二进制
镜像
用于
调试
目的。
构建
系统
在
构建
目录
中
生成
镜像。
默认
情况
下，
内核
二进制
文件
名
是
:file:`zephyr.elf`。
名称
可以
用
:kconfig:option:`CONFIG_KERNEL_BIN_NAME`
更改。

GDB
服务器
==========

我们
将
使用
标准
1234
TCP
端口
打开
一个
:abbr:`GDB
（GNU
Debugger）`
服务器
实例。
这个
端口
号
可以
更改
为
最
适合
开发
环境
的
端口。
有
多种
方式
做
这。
每个
方式
启动
一个
QEMU
实例，
处理器
在
启动
时
停止
并
有
一个
GDB
服务器
实例
监听
连接。

直接
运行
QEMU
~~~~~~~~~~~~~~~~~~~~~

你
可以
运行
QEMU
在
它
开始
执行
任何
代码
前
监听
"gdb
连接"
来
调试
它。

.. code-block:: bash

   qemu
   -s
   -S
   <image>

将
设置
Qemu
监听
端口
1234
并
等待
GDB
连接
到
它。

上面
使用
的
选项
有
以下
含义：

* ``-S``
  不
  在
  启动
  时
  启动
  CPU；
  相反，
  你
  必须
  在
  monitor
  中
  键入
  'c'。
* ``-s``
  :literal:`-gdb
  tcp::1234`
  的
  简写：
  在
  TCP
  端口
  1234
  上
  打开
  一个
  GDB
  服务器。


用
:command:`ninja`
运行
QEMU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在
应用
的
构建
目录
内
运行
以下：

.. code-block:: console

   ninja
   debugserver

QEMU
将
将
控制台
输出
写
到
通过
CMake
指定
的
:makevar:`${QEMU_PIPE}`
路径，
通常
是
构建
目录
内
的
:file:`qemu-fifo`。
你
可以
在
运行
期间
用
:command:`tail
-f
qemu-fifo`
监控
这个
文件。

用
:command:`west`
运行
QEMU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

从
你的
项目
根
运行
以下：

.. code-block:: console

   west
   build
   -t
   debugserver_qemu

QEMU
将
将
控制台
输出
写
到
你
调用
:command:`west`
的
终端。

配置
:command:`gdbserver`
监听
设备
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kconfig
选项
:kconfig:option:`CONFIG_QEMU_GDBSERVER_LISTEN_DEV`
控制
监听
设备，
它
可以
是
TCP
端口
号
或
字符
设备
的
路径。
GDB
发布
9.0
及
之后
也
支持
Unix
域
套接字。

如果
选项
未
设置，
那么
QEMU
调用
将
缺少
``-s``
或
``-gdb``
参数。
你
然后
可以
使用
:envvar:`QEMU_EXTRA_FLAGS`
shell
环境变量
传入
你
自己
的
监听
设备
配置。

GDB
客户端
==========

通过
运行
:command:`gdb`
并
给出
这些
命令
连接
到
服务器：

.. code-block:: bash

   $
   path/to/gdb
   path/to/zephyr.elf
   (gdb)
   target
   remote
   localhost:1234
   (gdb)
   dir
   ZEPHYR_BASE

.. note::

   用
   你
   系统
   正确
   的
   :ref:`ZEPHYR_BASE
   <important-build-vars>`
   替换。

你
可以
使用
本地
GDB
配置
:file:`.gdbinit`
在
每次
运行
时
初始化
你的
GDB
实例。
你的
主
目录
是
典型
位置。
