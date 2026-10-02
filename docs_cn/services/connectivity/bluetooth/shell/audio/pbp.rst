Bluetooth：公共广播配置文件 Shell
#########################################

本文档描述如何运行公共广播配置文件功能。
PBP 没有关联的服务。其目的是启用更快、更高效地发现
正在以常用编解码器配置传输音频的广播源。

使用 PBP Shell
*******************

当蓝牙协议栈已初始化（:code:`bt init`）后，公共广播配置文件即可运行。
要设置公共广播公告功能，调用 :code:`pbp set_features`。

.. code-block:: console


   pbp --help
   pbp - Bluetooth PBP shell commands
   Subcommands:
     set_features    :Set the Public Broadcast Announcement features
