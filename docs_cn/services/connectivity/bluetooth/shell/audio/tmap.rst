Bluetooth: Telephone and Media Audio Profile Shell
##################################################

此文档描述如何运行 Telephone and Media Audio Profile 功能。与大多数其他 low-layer profiles 不同（TMAP 是一个存在于所有设备上且有 service（TMAS）的 profile。因此 initiator 和 acceptor（或 central 和 peripheral）都应 discover 远端 device 的 TMAS 以查看其支持的 TMAP roles。

Using the TMAP Shell
********************

当 Bluetooth stack 已初始化（:code:`bt init`）时（TMAS 可通过调用 :code:`tmap init` 注册。

.. code-block:: console


   tmap --help
   tmap - Bluetooth TMAP shell commands
   Subcommands:
     init          :Initialize and register the TMAS
     discover      :Discover TMAS on remote device
