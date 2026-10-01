.. _bt_hci_pkt:

HCI Packet Helpers
##################

用于在 :c:struct:`net_buf_simple` buffers 和 packet bytes 中 framing HCI command packets 和解析 command responses 的 helpers（独立于 Bluetooth Host 和 HCI driver interface（连同用于通过其自身 transport 与 controller 交换 HCI commands 的 HCI drivers 的 lockstep helper（例如用于 vendor-specific controller initialization。

两个 helpers 均为启用 :kconfig:option:`CONFIG_BT` 的每个 build 的一部分。Lockstep helper 的 header 位于 HCI driver API 下（:file:`include/zephyr/drivers/bluetooth/`。

这些不是通用 application APIs：预期用户为 HCI drivers 和 Bluetooth stack internals。需要与运行中的 Host 一起发送 HCI commands 的 applications 改用更高层的 :c:func:`bt_hci_cmd_alloc`、:c:func:`bt_hci_cmd_send` 和 :c:func:`bt_hci_cmd_send_sync` APIs（其与 Host 的 command flow control 协作。

API Reference
*************

.. doxygengroup:: bt_hci_pkt

.. doxygengroup:: bt_hci_lockstep

.. doxygengroup:: bt_hci_h4
