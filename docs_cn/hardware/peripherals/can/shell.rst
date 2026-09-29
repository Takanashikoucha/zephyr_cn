.. _can_shell:

CAN
Shell
#########

.. contents::
   :local:
   :depth:
   1

Overview
********

CAN
shell
为
:ref:`shell
<shell_api>`
模块
提供
一
个
带
一
组
subcommands
的
``can``
命令。
它
允许
通过
交互式
interface
测试
和
探索
:ref:`can_api`
driver
API
而
不
需要
写
专门
的
应用。
CAN
shell
也
可以
在
现有
应用
中
启用
以
辅助
CAN
issues
的
交互式
debugging。

CAN
shell
提供
对
大多数
CAN
controller
功能
的
访问，
包括
inspection、
configuration、
CAN
frames
的
发送
和
接收、
以及
bus
recovery。

要
启用
CAN
shell，
必须
启用
以下
:ref:`Kconfig
<kconfig>`
选项：

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_CAN`
* :kconfig:option:`CONFIG_CAN_SHELL`

以下
:ref:`Kconfig
<kconfig>`
选项
启用
``can``
命令
的
额外
subcommands
和
功能：

* :kconfig:option:`CONFIG_CAN_FD_MODE`
  启用
  CAN
  FD
  特定
  subcommands
  （例如
  用于
  设置
  CAN
  FD
  data
  phase
  的
  timing）。
* :kconfig:option:`CONFIG_CAN_RX_TIMESTAMP`
  启用
  接收
  的
  CAN
  frames
  的
  timestamps
  打印。
* :kconfig:option:`CONFIG_CAN_STATS`
  启用
  ``can
  show``
  subcommand
  中
  CAN
  controller
  的
  各种
  statistics
  打印。
  这
  依赖
  于
  :kconfig:option:`CONFIG_STATS`
  也
  被
  启用。
* :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE`
  启用
  ``can
  recover``
  subcommand。

例如，
为
:zephyr:board:`frdm_k64f`
构建
:zephyr:code-sample:`hello_world`
sample
启用
CAN
shell
和
CAN
statistics：
