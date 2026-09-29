.. _sca:

静态
代码
分析
（SCA）
##########################

Zephyr
中
对
静态
代码
分析
工具
的
支持
通过
CMake
实现。

构建
设置
:makevar:`ZEPHYR_SCA_VARIANT`
可以
用
来
指定
要
使用
的
SCA
工具。
:envvar:`ZEPHYR_SCA_VARIANT`
也
被
支持
作为
:ref:`环境变量
<env_vars>`。

用
``-DZEPHYR_SCA_VARIANT=<tool>``，
例如
``-DZEPHYR_SCA_VARIANT=sparse``
启用
静态
分析
工具
``sparse``。

.. _sca_infrastructure:

SCA
工具
基础设施
***********************

对
一个
SCA
工具
的
支持
在
一个
:file:`sca.cmake`
文件
中
实现。
:file:`sca.cmake`
必须
放
在
:file:`{SCA_ROOT}/cmake/sca/{tool}/sca.cmake`
下。
Zephyr
本身
始终
被
添加
作为
:makevar:`SCA_ROOT`
但
构建
系统
提供
添加
额外
文件夹
到
:makevar:`SCA_ROOT`
设置
的
可能。

你
可以
通过
创建
以下
结构
提供
树
外
SCA
工具
的
支持：

.. code-block:: none

   <sca_root>/
                 #
                 自定义
                 SCA
                 root
   └──
   cmake/
       └──
       sca/
           └──
           <tool>/
           #
           SCA
           工具
           名称，
           这
           是
           给
           ZEPHYR_SCA_VARIANT
           的
           值
               └──
               sca.cmake
               #
               配置
               工具
               与
               Zephyr
               一起
               使用
               的
               CMake
               代码

要
在
``/path/to/my_tools/cmake/sca``
下
添加
``foo``
创建
以下
结构：

.. code-block:: none

   /path/to/my_tools
           └──
           cmake/
               └──
               sca/
                   └──
                   foo/
                       └──
                       sca.cmake

要
用
``foo``
作为
SCA
工具
你
必须
然后
指定
``-DZEPHYR_SCA_VARIANT=foo``。

记住
将
``/path/to/my_tools``
添加
到
:makevar:`SCA_ROOT`。

:makevar:`SCA_TOOL`
可以
作为
普通
CMake
设置
用
``-DSCA_ROOT=<sca_root>``
设置，
或
由
Zephyr
模块
在
其
:file:`module.yml`
文件
中
添加，
见
:ref:`Zephyr
Modules
-
Build
settings
<modules_build_settings>`

编译器
和
链接器
launcher
=============================

需要
观察
或
包装
编译
和
链接
命令
的
SCA
工具
通过
从
其
:file:`sca.cmake`
设置
``CMAKE_<LANG>_COMPILER_LAUNCHER``
和
``CMAKE_<LANG>_LINKER_LAUNCHER``
变量
做
到。
它们
必须
作为
普通
变量
设置，
不
是
作为
cache
条目。

用
这种
方式
设置
的
launcher
替换
任何
已经
配置
的
launcher，
``ccache``
包括
在内。
是
透明
包装器
的
工具，
意味
它
运行
给
它
的
命令
不
修改，
可以
替代
地
通过
追加
之前
的
launcher
保持
它：

.. code-block:: cmake

   set(CMAKE_C_COMPILER_LAUNCHER
   ${my_wrapper}
   ${CMAKE_C_COMPILER_LAUNCHER})

.. _sca_native_tools:

本地
SCA
工具
支持
***********************

以下
是
Zephyr
构建
系统
本地
支持
的
SCA
工具
列表。

.. toctree::
   :maxdepth: 1
   :glob:

   *
