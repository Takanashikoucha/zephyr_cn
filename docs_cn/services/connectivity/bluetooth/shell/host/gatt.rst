Bluetooth: GATT 外壳
#####################

以下示例假设两台设备已经建立连接。

要在客户端执行服务发现，请使用 :code:`gatt discover` 命令。该命令应打印出 GATT 服务器上可用的所有服务。

在服务端，你可以使用 :code:`gatt register` 命令注册预定义的服务。完成后，在客户端运行发现命令时，应该能看到新添加的服务。

现在你可以在客户端订阅这些新服务。以下是如何订阅测试服务的示例：

.. code-block:: console

        uart:~$ gatt subscribe 26 25
        Subscribed

现在服务端可以使用 :code:`gatt notify` 命令向客户端发送通知。

通过 GATT 命令可用的另一个选项是发起 MTU 交换。要执行此操作，请使用 :code:`gatt exchange-mtu` 命令。要更新外壳的最大 MTU，你需要在配置文件中更新 Kconfig 符号。更多细节，请参见
:zephyr:code-sample:`bluetooth_mtu_update`。
