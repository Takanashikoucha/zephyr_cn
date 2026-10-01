.. _external_module_cannectivity:

CANnectivity USB 转 CAN 适配器固件
##################################

简介
****

`CANnectivity`_ 是一个用于通用串行总线（USB）转控制器局域网（CAN）适配器的开源固件。

该固件实现了 Geschwister Schneider USB/CAN 设备协议（通常称为 “gs_usb”）。该协议受 Linux 内核 SocketCAN 的 `gs_usb 驱动`_、`python-can`_ 以及许多其他软件包支持。

该固件基于 Zephyr RTOS，可将你喜爱的微控制器开发板变成功能完备的 USB 转 CAN 适配器。

CANnectivity 采用 Apache-2.0 许可。

在 Zephyr 中使用
****************

CANnectivity 固件仓库是一个 Zephyr :ref:`module <modules>`，允许在 CANnectivity 固件应用之外复用其组件（即 “gs_usb” 协议实现）。

要将 CANnectivity 作为 Zephyr 模块引入，可以将其作为 West 项目添加到 ``west.yaml`` 文件，或通过添加子 manifest（例如 ``zephyr/submanifests/cannectivity.yaml``）文件引入，内容如下，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: cannectivity
         url: https://github.com/CANnectivity/cannectivity.git
         revision: main
         path: custom/cannectivity # adjust the path as needed

将 CANnectivity 添加为 Zephyr 模块后，即可在 CANnectivity 固件应用之外复用 “gs_usb” 实现，只需包含其头文件：

.. code-block:: c

   #include <cannectivity/usb/class/gs_usb.h>

API 详情请参见该头文件。

.. _CANnectivity:
   https://github.com/CANnectivity/cannectivity

.. _gs_usb 驱动:
   https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/can/usb/gs_usb.c

.. _python-can:
   https://python-can.readthedocs.io/en/stable/interfaces/gs_usb.html
