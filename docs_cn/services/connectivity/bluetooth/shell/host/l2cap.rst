Bluetooth: L2CAP 外壳
######################

:code:`l2cap` 命令暴露了 L2CAP API 的一部分。以下示例展示了如何注册一个 LE PSM、从另一台设备连接到它并发送 3 个各 14 字节的数据包。

该示例假设两台设备已经建立连接。

在设备 A 上，注册 LE PSM：

.. code-block:: console

        uart:~$ l2cap register 29
        L2CAP psm 41 sec_level 1 registered

在设备 B 上，连接到已注册的 LE PSM 并发送数据：

.. code-block:: console

        uart:~$ l2cap connect 29
        Chan sec: 1
        L2CAP connection pending
        Channel 0x20000210 connected
        Channel 0x20000210 status 1
        uart:~$ l2cap send 3 14
        Rem 2
        Rem 1
        Rem 0
        Outgoing data channel 0x20000210 transmitted
        Outgoing data channel 0x20000210 transmitted
        Outgoing data channel 0x20000210 transmitted

在设备 A 上，你应该已经收到了数据：

.. code-block:: console

        Incoming conn 0x20002398
        Channel 0x20000210 status 1
        Channel 0x20000210 connected
        Channel 0x20000210 requires buffer
        Incoming data channel 0x20000210 len 14
        00000000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff       |........ ......  |
        Channel 0x20000210 requires buffer
        Incoming data channel 0x20000210 len 14
        00000000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff       |........ ......  |
        Channel 0x20000210 requires buffer
        Incoming data channel 0x20000210 len 14
        00000000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff       |........ ......  |
