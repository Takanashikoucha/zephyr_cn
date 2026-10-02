Bluetooth：电话和媒体音频配置文件 Shell
##################################################

本文档描述如何运行电话和媒体音频配置文件功能。
与大多数其他底层配置文件不同，TMAP 是一个在所有设备上都存在并拥有服务（TMAS）的配置文件。
因此发起方和接受方（或中央设备和外围设备）都应该对远程设备的 TMAS 进行发现，
以查看它们支持哪些 TMAP 角色。

使用 TMAP Shell
********************

当蓝牙协议栈已初始化（:code:`bt init`）后，
可以通过调用 :code:`tmap init` 来注册 TMAS。

.. code-block:: console


   tmap --help
   tmap - Bluetooth TMAP shell commands
   Subcommands:
     init          :Initialize and register the TMAS
     discover      :Discover TMAS on remote device
