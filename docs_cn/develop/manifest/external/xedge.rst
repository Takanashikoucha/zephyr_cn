.. _external_module_xedge:

Xedge
#####

简介
****

`Xedge`_ 是一个安全的嵌入式 Web 和 IoT 边缘框架，面向资源受限设备和 RTOS 环境设计。它基于 Barracuda App Server 技术构建，提供基于 Lua 的高层应用环境，用于开发安全的、联网的设备。

Xedge 采用 GPLv2 许可，另有商业许可选项。

在 Zephyr 中使用
*****************

Xedge 框架是一个 Zephyr :ref:`模块 <modules>`，使开发者能够在嵌入式硬件上直接实现基于 Web 的管理界面、REST API 和安全的 IoT 服务。

要将 Xedge 作为 Zephyr 模块引入，添加子 manifest（例如 ``zephyr/submanifests/xedge.yaml``）文件，内容如下，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: xedge
         url: https://github.com/RealTimeLogic/Xedge4Zephyr.git
         revision: main
         path: modules/Xedge4Zephyr

详细的构建说明、支持的特性和示例请参见 `Xedge for Zephyr GitHub 仓库`_。

参考资料
**********

.. target-notes::

.. _Xedge:
.. _Xedge Introduction:
   https://realtimelogic.com/products/xedge/

.. _Xedge for Zephyr GitHub Repository:
   https://github.com/RealTimeLogic/Xedge4Zephyr

.. _Barracuda App Server:
   https://realtimelogic.com/products/barracuda-application-server/
