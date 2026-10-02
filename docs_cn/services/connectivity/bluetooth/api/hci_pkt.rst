.. _bt_hci_pkt:

HCI 数据包辅助函数
##################

用于在 :c:struct:`net_buf_simple` 缓冲区和数据包字节中组帧 HCI 命令数据包以及解析命令响应的辅助函数，独立于蓝牙主机和 HCI 驱动程序接口，同时提供用于通过自身传输层与控制器交换 HCI 命令的 HCI 驱动程序的同步辅助函数，例如用于特定于厂商的控制器初始化。

两个辅助函数都是启用 :kconfig:option:`CONFIG_BT` 的每个构建的一部分。同步辅助函数的头文件位于 HCI 驱动程序 API 下，路径为 :file:`include/zephyr/drivers/bluetooth/`。

这些不是通用应用程序 API：预期用户是 HCI 驱动程序和蓝牙协议栈内部。需要与运行中的主机一起发送 HCI 命令的应用程序应改用更高层的 :c:func:`bt_hci_cmd_alloc`、:c:func:`bt_hci_cmd_send` 和 :c:func:`bt_hci_cmd_send_sync` API，这些 API 与主机的命令流控协作。

API 参考
*************

.. doxygengroup:: bt_hci_pkt

.. doxygengroup:: bt_hci_lockstep

.. doxygengroup:: bt_hci_h4
