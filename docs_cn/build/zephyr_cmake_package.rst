.. _cmake_pkg:

Zephyr CMake 包
####################

Zephyr `CMake 包`_
是
创建
基于
Zephyr 的
应用
的
便捷
方式。

.. note::
   :ref:`zephyr-app-types` 章节
   介绍
   本
   页
   使用
   的
   应用
   类型。

Zephyr CMake
包
确保
CMake
可以
自动
选择
用于
构建
应用
的
Zephyr 安装，
无论
它
是
:ref:`Zephyr 仓库
应用 <zephyr-repo-app>`、
:ref:`Zephyr 工作区
应用 <zephyr-workspace-app>`，
还是
:ref:`Zephyr 独立
应用 <zephyr-freestanding-app>`。

开发
基于
Zephyr 的
应用
时，
开发者
只需
在
应用
:file:`CMakeLists.txt` 文件
开头
写
``find_package(Zephyr)``。

要
使用
Zephyr CMake
包，
首先
必须
将其
导出
到
`CMake 用户
包
注册表`_。
这
意味着
在
CMake 用户
包
注册表
中
创建
对
当前
Zephyr 安装
的
引用。


.. tabs::

   .. group-tab:: Ubuntu

      在
      Linux 上，
      CMake 用户
      包
      注册表
      位于：

      ``~/.cmake/packages/Zephyr``

   .. group-tab:: macOS

      在
      macOS 上，
      CMake 用户
      包
      注册表
      位于：

      ``~/.cmake/packages/Zephyr``

   .. group-tab:: Windows

      在
      Windows 上，
      CMake 用户
      包
      注册表
      位于：

      ``HKEY_CURRENT_USER\Software\Kitware\CMake\Packages\Zephyr``


Zephyr CMake
包
允许
CMake
自动
查找
Zephyr base。
必须
导出
一个
或多个
Zephyr 安装。
导出
多个
Zephyr 安装
在
开发
或
测试
Zephyr 独立
应用、
带
厂商
fork 的
Zephyr 工作区
应用
等
时
可能
有用。


Zephyr CMake
包
导出
（west）
**********************************

使用
:ref:`west <get_the_code>` 安装
Zephyr
时，
推荐
使用
``west zephyr-export`` 导出
Zephyr。

.. _zephyr_cmake_package_export:

Zephyr CMake
包
导出
（无
west）
******************************************

Zephyr CMake
包
用
以下
命令
导出
到
CMake 用户
包
注册表：

.. code-block:: bash

   cmake -P <PATH-TO-ZEPHYR>/share/zephyr-package/cmake/zephyr_export.cmake

这
将
将
当前
Zephyr
导出
到
CMake 用户
包
注册表。

.. _zephyr_cmake_package_zephyr_base:

Zephyr Base 环境
设置
*******************************

Zephyr CMake
包
搜索
功能
允许
使用
环境
变量
显式
指定
Zephyr base。

要
做到
这，
使用
以下
``find_package()`` 语法：

.. code-block:: cmake

   find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

这
个
语法
指示
CMake
首先
使用
Zephyr base 环境
设置
:envvar:`ZEPHYR_BASE` 搜索
Zephyr，
然后
使用
正常
的
搜索
路径。

.. _zephyr_cmake_search_order:

Zephyr CMake
包
搜索
顺序
*********************************

当
Zephyr base 环境
设置
不
用于
搜索
时，
将
使用
匹配
以下
标准
的
Zephyr 安装：

* Zephyr 仓库
  应用
  将
  使用
  其
  位于
  的
  Zephyr。
  例如：

  .. code-block:: none

        <projects>/zephyr-workspace/zephyr
        └── samples
            └── hello_world

  在
  这个
  示例
  中，
  ``hello_world`` 将
  使用
  ``<projects>/zephyr-workspace/zephyr``。


* Zephyr 工作区
  应用
  将
  使用
  共享
  相同
  工作区
  的
  Zephyr。
  例如：

  .. code-block:: none

     <projects>/zephyr-workspace
     ├── zephyr
     ├── ...
     └── my_application

  在
  这个
  示例
  中，
  ``my_application`` 将
  使用
  ``<projects>/zephyr-workspace/zephyr``。

  要
  验证
  应用
  属于
  工作区，
  CMake
  将
  查找
  包含
  应用
  源
  目录
  的
  目录
  中
  的
  ``.west`` 目录。

* Zephyr 独立
  应用
  将
  使用
  从
  CMake 用户
  包
  注册表
  获取
  的
  Zephyr 安装
  列表
  中
  满足
  ``find_package(Zephyr ...)`` 调用
  时
  用户
  指定
  的
  要求
  的
  那个。

  如果
  没有
  指定
  版本，
  将
  使用
  注册表
  中
  的
  第一个
  安装。

  如果
  指定
  了
  版本，
  将
  使用
  匹配
  该
  版本
  的
  第一个
  安装。
  如果
  多个
  安装
  匹配，
  将
  使用
  列表
  中
  第一个
  匹配的
  那个。

  如果
  没有
  安装
  匹配，
  CMake
  将
  报告
  错误。

.. _zephyr_cmake_package_files:

Zephyr CMake
包
文件
*******************************

Zephyr CMake
包
由
以下
文件
组成：

:file:`ZephyrConfig.cmake`
   CMake
   为
   包
   调用
   的
   文件，
   满足
   用户
   调用
   ``find_package(Zephyr ...)`` 时
   指定
   的
   要求。
   这个
   文件
   负责
   源
   样板
   代码。

:file:`ZephyrConfigVersion.cmake`
   CMake
   为
   包
   版本
   调用
   的
   文件。
   它
   检查
   请求
   的
   版本
   与
   Zephyr 版本
   兼容。

:file:`zephyr_package_search.cmake`
   用于
   检测
   Zephyr 仓库
   和
   工作区
   候选
   的
   通用
   文件。
   用于
   ``ZephyrConfigVersion.cmake`` 和
   ``ZephyrConfig.cmake`` 的
   通用
   代码。

:file:`zephyr_export.cmake`
   见
   :ref:`zephyr_cmake_package_export`。

.. _CMake 包: https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html
.. _CMake 用户
   包
   注册表: https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html#user-package-registry
.. _CMake 包
   版本: https://cmake.org/cmake/help/latest/command/find_package.html#version-selection
.. _CMake 包
   搜索
   过程: https://cmake.org/cmake/help/latest/command/find_package.html#search-procedure
