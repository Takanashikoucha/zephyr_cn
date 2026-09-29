.. _external_module_zenoh_pico:

zenoh-pico
##########

简介
****

`zenoh-pico`_ 是 `Eclipse Zenoh`_ 面向受限设备的实现，提供原生
C API。它为嵌入式系统和微控制器提供零开销 Pub/sub、Store/Query
和 Compute 能力。

zenoh-pico 统一了流动中的数据、静态数据和计算，同时保持远超主流
协议栈的时间和空间效率。它与主 Rust Zenoh 实现完全兼容，提供
大多数功能量的轻量级实现。

zenoh-pico 采用 Eclipse Public License 2.0 和 Apache License 2.0。

在 Zephyr 中使用
****************

zenoh-pico 仓库是一个 Zephyr :ref:`module <modules>`，为 Zephyr
应用提供分布式通信能力。它支持基于 IPv4、IPv6 和 6LoWPAN 网络的
UDP（单播和组播）、TCP 传输层，数据链路层支持 WiFi、以太网、
Thread 和 Serial。

要将 zenoh-pico 作为 Zephyr 模块引入，可以将其作为 West 项目
添加到 ``west.yaml`` 文件，或通过添加子 manifest（例如
``zephyr/submanifests/zenoh-pico.yaml``）文件引入，内容如下，
然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: zenoh-pico
         url: https://github.com/eclipse-zenoh/zenoh-pico.git
         revision: main
         path: modules/lib/zenoh-pico # adjust the path as needed

更详细的步骤和 API 文档请参阅 `zenoh-pico 文档`_ 以及提供的
`Zephyr 示例`_。

参考资料
********

.. target-notes::

.. _zenoh-pico:
   https://github.com/eclipse-zenoh/zenoh-pico

.. _Eclipse Zenoh:
   https://zenoh.io

.. _zenoh-pico 文档:
   https://zenoh-pico.readthedocs.io/en/latest/

.. _Zephyr 示例:
   https://github.com/eclipse-zenoh/zenoh-pico/tree/main/examples/zephyr
