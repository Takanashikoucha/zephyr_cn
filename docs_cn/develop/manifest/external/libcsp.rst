.. _external_module_libcsp:

libcsp（Cubesat Space Protocol）
###############################

简介
****

libcsp 是 CubeSat Space Protocol（CSP）的一个实现。它是一个用 C
编写的小型协议栈。CSP 旨在简化小型网络（如 CubeSat）中分布式嵌入式
系统之间的通信。其设计遵循 TCP/IP 模型，包含传输协议、路由协议和
多个 MAC 层接口。libcsp 的核心包含路由器、面向连接的 socket API，
以及消息池和连接池。

一些 CubeSat 使用 Zephyr，它们使用 libcsp 与 CubeSat 内的其他组件
通信。

libcsp 采用 MIT 许可。

在 Zephyr 中使用
****************

要在 Zephyr 中使用 libcsp，首先需要将以下片段添加到 ``west.yaml``：

.. code-block:: yaml

   manifest:
     projects:
       - name: libcsp
         url: https://github.com/libcsp/libcsp
         revision: develop
         path: modules/lib/libcsp

并在 ``prj.conf`` 中添加：

.. code-block:: cfg

     CONFIG_LIBCSP=y

将 libcsp 添加到项目后，运行 ``west update``。

更详细的步骤和 API 文档请参阅 `libcsp 文档`_。

参考资料
********

.. target-notes::

.. _libcsp:
   https://github.com/libcsp/libcsp

.. _libcsp 文档:
   https://libcsp.github.io/libcsp/
