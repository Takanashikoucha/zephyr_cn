编写
片段
################

.. contents::
   :local:

基础
******

片段
使用
名为
:file:`snippet.yml` 的
YAML 文件
定义。

:file:`snippet.yml` 文件
包含
片段
的
名称，
连同
额外
的
构建
系统
设置，
像
这样：

.. code-block:: yaml

   name: snippet-name
   # ... 构建
   # 系统
   # 设置
   # 放
   # 这里
   # ...

构建
系统
设置
放在
文件
中
的
其他
键
中，
如
本页
后面
所述。

只要
设置
出现在
相同
的
键
下，
就
可以
组合
设置。
例如，
你
可以
像
这样
组合
片段
特定
的
设备树
覆盖
和
``.conf`` 文件：

.. code-block:: yaml

   name: foo
   append:
     EXTRA_DTC_OVERLAY_FILE: foo.overlay
     EXTRA_CONF_FILE: foo.conf

此外，
片段
也
可以
像
这样
应用
到
sysbuild
配置：

.. code-block:: yaml

   name: foo
   append:
     SB_EXTRA_CONF_FILE: sb.conf
     EXTRA_CONF_FILE: app.conf

命名空间
***********

在
片段
中
编写
设备树
覆盖
时，
选择
节点
标签、
节点
名称
等
的
名称
时
使用
``snippet_<name>`` 或
``snippet-<name>`` 作为
命名空间
前缀。
这
避免
命名空间
冲突。

例如，
如果
你的
片段
名为
``foo-bar``，
像
这样
编写
你的
设备树
覆盖：

.. code-block:: DTS

   chosen {
           zephyr,baz = &snippet_foo_bar_dev;
   };

   snippet_foo_bar_dev: device@12345678 {
           /* ... */
   };

片段
位于
哪里
**************************

构建
系统
在
这些
地方
查找
片段：

#. 在
   :makevar:`SNIPPET_ROOT` CMake 变量
   配置
   的
   目录
   中。
   这
   始终
   包含
   zephyr
   仓库
   （因此
   :zephyr_file:`snippets/` 始终
   是
   片段
   的
   来源）。

   额外
   的
   目录
   可以
   在
   CMake 时
   手动
   添加。

   该
   变量
   是
   空白
   或
   分号
   分隔
   的
   目录
   列表，
   可能
   包含
   片段
   定义。

   对于
   列表
   中
   的
   每个
   目录，
   构建
   系统
   查找
   名为
   :file:`snippets/` 的
   子
   目录
   下
   的
   :file:`snippet.yml` 文件
   （如果
   存在）。

   例如，
   如果
   :makevar:`SNIPPET_ROOT` 设置
   为
   ``/foo;/bar``，
   构建
   系统
   将
   查找
   以下
   子
   目录
   下
   的
   :file:`snippet.yml` 文件：

   - :file:`/foo/snippets/`
   - :file:`/bar/snippets/`

   :file:`snippet.yml` 文件
   可以
   嵌套
   在
   这些
   位置
   下
   的
   任何
   地方。

#. 在
   任何
   :ref:`模块 <modules>` 的
   :file:`module.yml` 文件
   提供
   ``snippet_root`` 设置
   的
   地方。

   例如，
   在
   名为
   ``baz`` 的
   zephyr
   模块
   中，
   你
   可以
   将
   这
   添加
   到
   你的
   :file:`module.yml` 文件：

   .. code-block:: yaml

      settings:
        snippet_root: .

   然后
   ``baz/snippets`` 中
   的
   任何
   :file:`snippet.yml` 文件
   将
   被
   构建
   系统
   自动
   发现，
   就像
   ``baz`` 的
   路径
   出现
   在
   :makevar:`SNIPPET_ROOT` 中
   一样。

处理
顺序
****************

片段
按
它们在
:makevar:`SNIPPET` 变量
中
列出
的
顺序
处理，
或
使用
west
时
``-S`` 参数
的
顺序。

在
``foo`` 之后
应用
``bar``：

.. code-block:: console

   cmake -Sapp -Bbuild -DSNIPPET="foo;bar" [...]
   cmake --build build

用
west
可以
用
以下
方式
达到
相同
效果：

.. code-block:: console

   west build -S foo -S bar [...] app

当
多个
片段
设置
相同
的
配置
时，
最后
处理
的
片段
设置
的
配置
值
最终
出现在
最终
配置
中。

例如，
如果
上面
示例
中
``foo`` 设置
``CONFIG_FOO=1`` 且
``bar`` 设置
``CONFIG_FOO=2``，
结果
最终
配置
将
是
``CONFIG_FOO=2``，
因为
``bar`` 在
``foo`` 之后
处理。

这个
原则
适用
于
Kconfig
片段
（``.conf`` 文件）
和
设备树
覆盖
（``.overlay`` 文件）
两者。

.. _snippets-devicetree-overlays:

设备树
覆盖
（``.overlay``）
**********************************

这个
:file:`snippet.yml`
将
:file:`foo.overlay` 添加
到
构建：

.. code-block:: yaml

   name: foo
   append:
     EXTRA_DTC_OVERLAY_FILE: foo.overlay

:file:`foo.overlay` 的
路径
相对
于
包含
:file:`snippet.yml` 的
目录。
多个
``.overlay`` 文件
也
可以
作为
列表
提供：

.. code-block:: yaml

   name: foo
   append:
     EXTRA_DTC_OVERLAY_FILE:
       - foo.overlay
       - bar.overlay

.. _snippets-conf-files:

``.conf`` 文件
***********************

这个
:file:`snippet.yml`
将
:file:`foo.conf` 添加
到
构建：

.. code-block:: yaml

   name: foo
   append:
     EXTRA_CONF_FILE: foo.conf

:file:`foo.conf` 的
路径
相对
于
包含
:file:`snippet.yml` 的
目录。
多个
``.conf`` 文件
也
可以
作为
列表
提供。

Sysbuild
``.conf`` 文件
************************

这个
:file:`snippet.yml`
将
:file:`foo.conf` 添加
到
sysbuild
配置：

.. code-block:: yaml

   name: foo
   append:
     SB_EXTRA_CONF_FILE: foo.conf

:file:`foo.conf` 的
路径
相对
于
包含
:file:`snippet.yml` 的
目录。
多个
sysbuild
``.conf`` 文件
也
可以
作为
列表
提供。

``DTS_EXTRA_CPPFLAGS``
**********************

这个
:file:`snippet.yml`
将
``DTS_EXTRA_CPPFLAGS`` CMake
Cache
变量
添加
到
构建：

.. code-block:: yaml

   name: foo
   append:
     DTS_EXTRA_CPPFLAGS: -DMY_DTS_CONFIGURE

添加
这些
标志
使
控制
设备树
文件
的
内容
成为
可能。

开发板
特定
设置
***********************

你
可以
编写
只
应用
于
某些
开发板
的
设置。

这里
描述
的
设置
在
**除了**
应用
于
所有
开发板
的
片段
设置
**之外**
被
应用。
（这
类似
于
例如
一个
同时
有
:file:`prj.conf` 和
:file:`boards/foo.conf` 文件
的
应用
在
为
开发板
``foo`` 构建
时
将在
构建
中
使用
两个
``.conf`` 文件，
而非
只
使用
:file:`boards/foo.conf`）

按
名称
=======

.. code-block:: yaml

   name: ...
   boards:
     bar: # 开发板
     # "bar"
     # 的
     # 设置
     # 放
     # 这里
     append:
       EXTRA_DTC_OVERLAY_FILE: bar.overlay
     baz: # 开发板
     # "baz"
     # 的
     # 设置
     # 放
     # 这里
     append:
       EXTRA_DTC_OVERLAY_FILE: baz.overlay

上面
示例
在
为
开发板
``bar`` 构建
时
使用
:file:`bar.overlay`，
为
``baz`` 构建
时
使用
:file:`baz.overlay`。

按
正则
表达式
=====================

你
可以
将
开发板
名称
包围
在
斜杠
（``/``）
中
以
按
`CMake 语法`_ 中
的
正则
表达式
匹配
名称。
正则
表达式
必须
匹配
整个
开发板
名称。

.. _CMake 语法:
   https://cmake.org/cmake/help/latest/command/string.html#regex-specification

例如：

.. code-block:: yaml

   name: foo
   boards:
     /my_vendor_.*/:
       append:
         EXTRA_DTC_OVERLAY_FILE: my_vendor.overlay

上面
示例
在
为
开发板
``my_vendor_board1`` 或
``my_vendor_board2`` 构建
时
使用
设备树
覆盖
:file:`my_vendor.overlay`。
为
``another_vendor_board`` 或
``x_my_vendor_board`` 构建
时
它
不
会
使用
该
覆盖。

开发板
修订
版本
==================

开发板
修订
版本
的
特定
配置
也
被
支持，
将
在
通用
文件
之后
应用：

.. code-block:: yaml

   name: foo
   boards:
     bar:
       append:
         # 基础
         # 文件
         # 先
         # 应用
         EXTRA_DTC_OVERLAY_FILE: first.overlay
       revisions:
         "0.7.0":
           append:
             # 将
             # 在
             # 通用
             # 开发板
             # 文件
             # 之上
             # 应用
             EXTRA_DTC_OVERLAY_FILE: extra_0_7_0.overlay

上面
示例
将
对
``bar`` 开发板
的
所有
修订
版本
使用
:file:`first.overlay`，
并为
``bar`` 开发板
的
修订
版本
``0.7.0``（``bar@0.7.0``）
构建
时
也
包含
:file:`extra_0_7_0.overlay`。
