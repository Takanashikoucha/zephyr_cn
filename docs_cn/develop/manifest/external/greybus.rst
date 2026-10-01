.. _external_module_greybus:

Greybus
#######

简介
****

Greybus 是一个轻量级、基于消息的协议框架，为主机访问远程模块上实现的硬件功能提供标准化方式。它最初为模块化系统开发，为 GPIO、I²C、SPI、PWM 和固件更新等常见外设类定义了一组规范明确的操作协议。

Zephyr 的 Greybus 模块提供 Greybus 协议层的实现，将 Greybus 操作映射到 Zephyr 子系统。启用后，Zephyr 设备可使用 Greybus 协议向主机暴露其硬件能力。主机通过 Greybus manifest 数据发现可用功能，然后发出类特定的请求，由 Zephyr 模块处理并响应。

最初，Greybus 设计用于通过 `Unipro`_ 使用。不过协议本身大多与底层传输无关。目前，Greybus 模块支持 TCP socket 作为传输。不过 UART、I2C 等任何传输都应能正常工作。当前支持的传输后端请参见 `此目录 <Greybus 传输目录>`_ 的内容。欢迎为新传输后端创建 PR。

Greybus 采用 Apache-2.0 与 BSD-3-Clause 许可的组合。

在 Zephyr 中使用
****************

要将 Greybus for Zephyr 作为 Zephyr 模块引入，可以将其作为 West 项目添加到 west.yaml 文件，或通过添加子 manifest（例如 ``zephyr/submanifests/greybus.yaml``）文件引入，内容如下，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: Greybus-Zephyr
         path: modules/lib/greybus
         revision: main
         url: https://github.com/beagleboard/greybus-zephyr

有关 greybus 子系统使用的说明，请参阅 `Greybus 模块仓库`_ 和 `Greybus 示例`_。

目前所有开发和实际测试都使用 `BeaglePlay`_ 和 `BeagleConnect Freedom`_ 进行。

参考资料
********

#. `Greybus 规范`_

#. Christopher Friedt，LPC 2020

   - `幻灯片 <LPC 2020 幻灯片>`_
   - `视频 <LPC 2020 视频>`_

.. target-notes::

.. _Greybus 规范: https://github.com/projectara/greybus-spec
.. _LPC 2020 幻灯片: https://linuxplumbersconf.org/event/7/contributions/814/
.. _LPC 2020 视频: https://youtu.be/n4yiCF2wYeo?t=11683
.. _Greybus 模块仓库: https://github.com/beagleboard/greybus-zephyr
.. _Greybus 示例: https://github.com/beagleboard/greybus-zephyr/tree/main/samples/basic
.. _BeaglePlay: https://www.beagleboard.org/boards/beagleplay
.. _BeagleConnect Freedom: https://www.beagleboard.org/boards/beagleconnect-freedom
.. _UniPro: https://en.wikipedia.org/wiki/UniPro
.. _Greybus 传输目录: https://github.com/beagleboard/greybus-zephyr/tree/main/subsys/greybus/transport
