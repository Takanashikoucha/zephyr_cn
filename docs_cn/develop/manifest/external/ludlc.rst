.. _external_module_ludlc:

LuDLC
#####

简介
************

LuDLC（Lightweight Micro Devices Link Control，轻量级微设备链路控制），是一个传输无关的数据链路协议，面向资源受限系统。

LuDLC 在 UART、SPI 或 CAN 总线等简单传输之上提供可靠、按序的通信，无需完整的网络栈。它提供流量控制、重传、连接管理和通道复用，适合 TCP/IP 过重或不可用的场景。

LuDLC 采用 (Apache-2.0 OR GPL-2.0-or-later) 双重许可。

在 Zephyr 中使用
*****************

要将 LuDLC 作为 Zephyr 模块（ludlc）引入，可以将其作为 West 项目添加到 :file:`west.yaml` 文件，或通过添加一个子 manifest 文件（例如 ``zephyr/submanifests/ludlc.yaml``，内容如下）引入，然后运行 :command:`west update`：

.. code-block:: yaml

   manifest:
     projects:
       - name: ludlc
         url: https://github.com/avolkov-1221/ludlc.git
         revision: main
         path: modules/ludlc # adjust the path as needed

参考资料
*********

.. target-notes::

.. _ludlc: https://github.com/avolkov-1221/ludlc

.. _ludlc 文档:
   https://github.com/avolkov-1221/ludlc/tree/main/doc

.. _ludlc 示例:
   https://github.com/avolkov-1221/ludlc/tree/main/src/samples
