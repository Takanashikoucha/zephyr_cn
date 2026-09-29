.. _eeprom_shell:

EEPROM
Shell
############

.. contents::
   :local:
   :depth:
   1

Overview
********

EEPROM
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
``eeprom``
命令。
它
允许
通过
交互式
interface
测试
和
探索
:ref:`EEPROM
<eeprom_api>`
driver
API
而
不
需要
写
专门
的
应用。
EEPROM
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
EEPROM
issues
的
交互式
debugging。

要
启用
EEPROM
shell，
必须
启用
以下
:ref:`Kconfig
<kconfig>`
选项：

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_EEPROM`
* :kconfig:option:`CONFIG_EEPROM_SHELL`

例如，
为
:zephyr:board:`native_sim`
构建
:zephyr:code-sample:`hello_world`
sample
启用
EEPROM
shell：

.. zephyr-app-commands::
   :zephyr-app:
   samples/hello_world
   :board:
   native_sim
   :gen-args:
   -DCONFIG_SHELL=y
   -DCONFIG_EEPROM=y
   -DCONFIG_EEPROM_SHELL=y
   :goals:
   build

参考
:ref:`shell
<shell_api>`
文档
获取
如何
连接
和
与
shell
交互
的
一般
说明。
EEPROM
shell
带
内置
help
（除非
:kconfig:option:`CONFIG_SHELL_HELP`
被
禁用）。
内置
help
messages
可以
通过
向
``eeprom``
命令
或
其
任何
subcommands
传递
``-h``
或
``--help``
打印。
所有
subcommands
也
支持
它们
的
arguments
的
tab-completion。

.. tip::
   所有
   EEPROM
   shell
   subcommands
   接受
   EEPROM
   peripheral
   的
   名称
   作为
   其
   第一
   argument，
   也
   支持
   tab-completion。
   所有
   可用
   devices
   的
   列表
   可以
   通过
   使用
