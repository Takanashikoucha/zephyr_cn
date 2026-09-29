.. _stm32cube_ide:

STM32CubeIDE
############

STM32CubeIDE_
是
STMicroelectronics
的
基于
Eclipse
的
集成
开发
环境
设计
用于
STM32
系列
的
MCUs
和
MPUs。

本
指南
描述
用
IDE
设置、
构建
和
调试
Zephyr
应用
的
过程。

项目
必须
已经
用
Zephyr
和
west
创建。

这些
说明
已
验证
与
IDE
version
1.16.0
在
Linux
上
工作。

项目
设置
*************

#. 开始
   前，
   确保
   你
   有
   一
   个
   工作
   的
   Zephyr
   开发
   环境，
   按
   :ref:`getting_started`
   中
   的
   说明。

#. 从
   你
   的
   Zephyr
   环境
   运行
   STM32CubeIDE。
   示例：

   .. code-block::

      $
      /opt/st/stm32cubeide_1.16.0/stm32cubeide

#. 通过
   去
   :menuselection:`File
   -->
   New
   -->
   STM32
   CMake
   Project`
   打开
   你
   已
   存在
   的
   项目：

   .. figure::
      img/stm32cube_new_cmake.webp
      :align:
      center
      :alt:
      Create
      new
      CMake
      project

#. 选择
   :guilabel:`Project
   with
   existing
   CMake
   sources`，
   然后
   点击
   :guilabel:`Next`。

#. 选择
   :menuselection:`Next`
   并
   浏览
   到
   你
   的
   源
   位置。
   打开
   的
   文件夹
   应该
   有
   ``CMakeLists.txt``
   和
   ``prj.conf``
   文件。

#. 选择
   :menuselection:`Next`
   并
   选择
   适当
   的
   MCU。
