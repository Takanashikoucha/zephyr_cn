Bluetooth: Public Broadcast Profile Shell
#########################################

此文档描述如何运行 Public Broadcast Profile 功能。PBP 没有关联的 service。其目的是启用更快、更高效地发现正在以常用 codec 配置传输 audio 的 Broadcast Sources。

Using the PBP Shell
*******************

当 Bluetooth stack 已初始化（:code:`bt init`）时（Public Broadcast Profile 已就绪运行。要设置 Public Broadcast Announcement features（调用 :code:`pbp set_features`。

.. code-block:: console


   pbp --help
   pbp - Bluetooth PBP shell commands
   Subcommands:
     set_features    :Set the Public Broadcast Announcement features
