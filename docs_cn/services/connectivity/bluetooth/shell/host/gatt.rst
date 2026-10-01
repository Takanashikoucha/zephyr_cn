Bluetooth: GATT Shell
#####################

以下示例假设您已有两个已连接的 devices。

要在 client 端执行 service discovery（使用 :code:`gatt discover` 命令。这应打印 GATT server 上所有可用的 services。

在 server 端（可用 :code:`gatt register` 命令注册预定义的 test services。完成后（运行 discovery 命令时应在 client 端看到新添加的 services。

现在可在 client 端订阅这些新 services。以下是如何订阅 test service 的示例：

.. code-block:: console

        uart:~$ gatt subscribe 26 25
        Subscribed

Server 现在可用 :code:`gatt notify` 命令通知 client。

GATT command 提供的另一个选项是发起 MTU exchange。为此（使用 :code:`gatt exchange-mtu` 命令。要更新 shell 最大 MTU（需更新 shell configuration file 中的 Kconfig symbols。更多细节参见 :zephyr:code-sample:`bluetooth_mtu_update`。
