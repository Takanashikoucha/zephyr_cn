.. _installation_linux:

安装
Linux
主机
依赖
###############################

以下
Linux
发行版
有
可用
文档：

* Ubuntu
* Fedora
* Clear
  Linux
* Arch
  Linux

对于
不
基于
滚动
发布
的
发行版，
某些
要求
和
依赖
可能
不
被
你的
包
管理器
满足。
在
这种
情况
下
请
遵循
提供
的
额外
说明
来
从
包
管理器
之外
的
来源
查找
软件。

.. note:: 如果
   你
   在
   企业
   防火墙
   后面
   工作，
   你
   很可能
   需要
   配置
   代理
   来
   访问
   互联网，
   如果
   你
   还
   没
   做
   的
   话。
   尽管
   某些
   工具
   使用
   环境变量
   ``http_proxy``
   和
   ``https_proxy``
   获取
   其
   代理
   设置，
   某些
   使用
   其
   自己
   的
   配置
   文件，
   最
   突出
   的
   是
   ``apt``
   和
   ``git``。

更新
你的
操作
系统
****************************

确保
你的
主机
系统
是
最新
的。

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: console

         sudo apt-get update
         sudo apt-get upgrade

   .. group-tab:: Fedora

      .. code-block:: console

         sudo dnf upgrade

   .. group-tab:: Clear
      Linux

      .. code-block:: console

         sudo swupd update

   .. group-tab:: Arch
      Linux

      .. code-block:: console

         sudo pacman -Syu

.. _linux_requirements:

安装
要求
和
依赖
*************************************

.. NOTE
   FOR
   DOCS
   AUTHORS:
   DO
   NOT
   PUT
   DOCUMENTATION
   BUILD
   DEPENDENCIES
   HERE.

   这
   一
   节
   是
   构建
   Zephyr
   二进制
   文件
   的
   依赖，
   *不
   是*
   本
   文档。
   如果
   你
   需要
   添加
   只
   用于
   构建
   文档
   的
   依赖，
   添加
   到
   doc/README.rst。
   （这个
   更改
   是
   在
   引入
   文档
   的
   LaTeX->PDF
   支持
   后
   做
   的，
   因为
   texlive
   的
   占用
   空间
   巨大
   且
   不
   构建
   PDF
   文档
   的
   用户
   不
   需要。）

注意
Ninja
和
Make
都
用
这些
说明
安装；
你
只
需要
一个。

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: console

         sudo apt-get install --no-install-recommends git cmake ninja-build gperf \
           ccache dfu-util device-tree-compiler wget \
           python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \
           make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

   .. group-tab:: Fedora

      .. code-block:: console

         sudo dnf group install development-tools c-development
         sudo dnf install cmake ninja-build gperf dfu-util dtc wget which \
           python3-pip python3-tkinter xz file python3-devel SDL2-devel \
           libusb1-devel

   .. group-tab:: Clear
      Linux

      .. code-block:: console

         sudo swupd bundle-add c-basic dev-utils dfu-util dtc \
           os-core-dev python-basic python3-basic python3-tcl

      Clear
      Linux
      的
      重点
      是
      *本地*
      性能
      和
      安全
      而
      不
      是
      交叉
      编译。
      因此
      它
      独特
      地
      默认
      向
      所有
      用户
      的
      :ref:`环境 <env_vars>`
      导出
      一
      组
      编译器
      和
      链接器
      标志。
      Zephyr
      的
      CMake
      构建
      系统
      会
      因为
      这些
      警告
      或
      失败。
      要
      清除
      这些
      中
      的
      C/C++
      标志
      并
      修复
      Zephyr
      构建，
      以
      root
      身份
      运行
      以下
      命令
      然后
      登出
      再
      登入：

      .. code-block:: console

         echo 'unset CFLAGS CXXFLAGS' >> /etc/profile.d/unset_cflags.sh

      注意
      这个
      命令
      为
      *系统
      上
      所有
      用户*
      取消
      设置
      C/C++
      标志。
      每个
      Linux
      发行版
      都
      有
      独特
      的、
      相对
      复杂
      且
      可能
      演变
      的
      bash
      初始化
      文件
      序列
      相互
      source，
      Clear
      Linux
      不
      是
      例外。
      如果
      你
      需要
      更
      灵活
      的
      方案，
      从
      查看
      ``/usr/share/defaults/etc/profile``
      中
      的
      逻辑
      开始。

   .. group-tab:: Arch
      Linux

      .. code-block:: console

         sudo pacman -S git cmake ninja gperf ccache dfu-util dtc wget \
             python-pip python-setuptools python-wheel tk xz file make which

CMake
=====

需要
:ref:`较
新
的
CMake
版本 <install-required-tools>`。
用
``cmake --version``
检查
你
有
什么
版本。
如果
你
有
旧
版本，
有
几种
方式
获取
更
新
的
版本：

* 在
  Ubuntu
  上，
  你
  可以
  遵循
  添加
  `kitware
  第三方
  apt
  仓库
  <https://apt.kitware.com/>`_
  的
  说明
  用
  apt
  获取
  cmake
  的
  更新
  版本。

* 从
  CMake
  项目
  网站
  下载
  并
  安装
  打包
  的
  cmake。
  （注意
  这
  不
  会
  卸载
  cmake
  的
  之前
  版本。）

  .. code-block:: console

     cd ~
     wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-Linux-x86_64.sh
     chmod +x cmake-3.21.1-Linux-x86_64.sh
     sudo ./cmake-3.21.1-Linux-x86_64.sh --skip-license --prefix=/usr/local
     hash -r

  如果
  安装
  脚本
  将
  cmake
  放
  到
  你
  PATH
  上
  的
  新
  位置，
  ``hash -r``
  命令
  可能
  是
  必要
  的。

* 从
  CMake
  项目
  本身
  提供
  的
  预
  构建
  二进制
  文件
  下载
  并
  安装，
  在
  `CMake
  下载`_
  页面
  中。
  例如，
  要
  在
  :file:`~/bin/cmake`
  安装
  版本
  3.21.1：

  .. code-block:: console

     mkdir $HOME/bin/cmake && cd $HOME/bin/cmake
     wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-Linux-x86_64.sh
     yes | sh cmake-3.21.1-Linux-x86_64.sh | cat
     echo "export PATH=$PWD/cmake-3.21.1-Linux-x86_64/bin:\$PATH" >> $HOME/.zephyrrc

* 使用
  ``pip3``：

  .. code-block:: console

     pip3 install --user cmake

  注意
  这
  不
  会
  卸载
  cmake
  的
  之前
  版本
  并
  将
  新
  cmake
  安装
  到
  你的
  ~/.local/bin
  文件夹，
  因此
  你
  需要
  将
  ~/.local/bin
  添加
  到
  你的
  PATH。
  （细节
  见
  :ref:`python-pip`。）

* 检查
  你
  发行版
  的
  beta
  或
  不稳定
  发布
  包
  库
  获取
  更新。

* 在
  Ubuntu
  上
  你
  也
  可以
  使用
  snap
  获取
  可用
  的
  最新
  版本：

  .. code-block:: console

     sudo snap install cmake

更新
cmake
后，
用
``cmake --version``
验证
新
安装
的
cmake
被
找到。
你
可能
还
想
卸载
包
管理器
提供
的
CMake
以
避免
冲突。
（使用
``whereis cmake``
查找
其他
已
安装
版本。）

DTC
（Device
Tree
Compiler）
==========================

需要
:ref:`较
新
的
DTC
版本 <install-required-tools>`。
用
``dtc --version``
检查
你
有
什么
版本。
如果
你
有
旧
版本，
要么
从
源
构建
安装
更
新
的
版本，
要么
安装
:ref:`Zephyr
SDK <toolchain_zephyr_sdk>`
中
捆绑
的
那个。

Python
======

需要
:ref:`现代
Python
3
版本 <install-required-tools>`。
用
``python3 --version``
检查
你
有
什么
版本。

如果
你
有
旧
版本，
你
将
需要
安装
更
新
的
Python
3。
你
可以
从
源
构建，
或
使用
你
发行版
包
管理器
渠道
的
backport
（如果
可用）。
推荐
在
虚拟
环境
中
隔离
这个
Python
以
避免
干扰
你的
系统
Python。

.. _pyenv: https://github.com/pyenv/pyenv

安装
Zephyr
软件
开发
套件
（SDK）
*************************************************

Zephyr
软件
开发
套件
（SDK）
包含
Zephyr
每个
受
支持
架构
的
工具链。
它
还
包括
额外
的
主机
工具，
如
自定义
QEMU
和
OpenOCD。

强烈
推荐
使用
Zephyr
SDK，
在
某些
条件
下
甚至
可能
是
必须
的
（例如
在
QEMU
中
运行
某些
架构
的
测试）。

要
安装
SDK，
遵循
:ref:`Zephyr
SDK
安装
指南 <linux_zephyr_sdk>`
的
Linux
步骤。

.. _sdkless_builds:

在
Linux
上
不
使用
Zephyr
SDK
构建
****************************************

Zephyr
SDK
为
方便
和
易用
提供。
它
提供
所有
Zephyr
目标
架构
的
工具链，
构建
应用
或
运行
测试
时
不
需要
任何
额外
标志。
除
交叉
编译器
外，
Zephyr
SDK
还
提供
预
构建
的
主机
工具。
不过，
可以
用
:ref:`工具链`
章节
中
描述
的
其他
工具链
不
使用
SDK
的
工具链
构建。

如
上面
已
注意
的，
SDK
还
包括
预
构建
的
主机
工具。
要
使用
SDK
的
预
构建
主机
工具
配合
来自
其他
来源
的
工具链，
你
必须
将
:envvar:`ZEPHYR_SDK_INSTALL_DIR`
环境变量
设置
为
Zephyr
SDK
安装
目录。
要
不
使用
Zephyr
SDK
的
预
构建
主机
工具
构建，
:envvar:`ZEPHYR_SDK_INSTALL_DIR`
环境变量
必须
取消
设置。

要
确保
这个
变量
取消
设置，
运行：

.. code-block:: console

   unset ZEPHYR_SDK_INSTALL_DIR

.. _Zephyr
   SDK
   发布: https://github.com/zephyrproject-rtos/sdk-ng/tags
.. _CMake
   下载: https://cmake.org/download
