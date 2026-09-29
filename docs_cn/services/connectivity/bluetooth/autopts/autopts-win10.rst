.. _autopts-win10:

AutoPTS
on
Windows
10
with
nRF52
board
#######################################

这
个
tutorial
展示
如何
setup
AutoPTS
client
和
server
都
运行
在
Windows
10
上。
我们
用
WSL1
带
Ubuntu
只
为
了
build
Zephyr
project
到
elf
file
因为
Zephyr
SDK
还
不
可用
于
Windows。
Tutorial
只
cover
nrf52840dk。

.. contents::
    :local:
    :depth:
    2

Update
Windows
and
drivers
===========================

在
以下
位置
Update
Windows：

Start
->
Settings
->
Update
&
Security
->
Windows
Update

Update
drivers
遵循
你
的
hardware
vendor
的
instructions。

Install
Python
3
================

Download
并
install
`Python
3
<https://www.python.org/downloads/>`_。
Setup
在
versions
>=3.8
上
tested。
让
installer
将
Python
installation
directory
添加
到
PATH
并
disable
path
length
limitation。

.. image::
   install_python1.png
   :height:
   300
   :width:
   450
   :align:
   center

.. image::
   install_python2.png
   :height:
   300
   :width:
   450
   :align:
   center
