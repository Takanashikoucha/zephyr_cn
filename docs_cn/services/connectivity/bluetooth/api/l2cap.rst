.. _bt_l2cap:

逻辑链路控制和适配协议（L2CAP）
####################################################

L2CAP 层提供面向连接的通道，可通过配置项 :kconfig:option:`CONFIG_BT_L2CAP_DYNAMIC_CHANNEL` 启用。这些通道透明地支持分片和重组，同时支持基于信用量的流量控制，因此适用于数据流。

通道实例由 :c:struct:`bt_l2cap_chan` 结构体表示，其中包含 :c:struct:`bt_l2cap_chan_ops` 结构体中的回调，用于通知通道已连接、已断开或加密状态已变化。此外，它还包含 ``recv`` 回调，每当收到传入数据时都会调用该回调。通过这种方式接收的数据可以通过返回 0 标记为已处理，或者在处理为异步时使用 :c:func:`bt_l2cap_chan_recv_complete` API。

.. note::
   ``recv`` 回调直接从 RX Thread 调用，因此不建议长时间阻塞。

发送数据可使用 :c:func:`bt_l2cap_chan_send` API。注意该 API 可能在没有可用信用量时阻塞，并会在更多信用量可用后立即恢复。

服务器可使用 :c:func:`bt_l2cap_server_register` API 注册，并传入 :c:struct:`bt_l2cap_server` 结构体，用于说明应监听哪个 ``psm``、所需的安全级别 ``sec_level``，以及用于授权传入连接请求并分配通道实例的回调 ``accept``。所分配的对象必须是 :c:struct:`bt_l2cap_le_chan` 类型，并通过 ``accept`` 回调返回的通道引用指向该对象的 ``chan`` 成员，如下面的示例所示。

.. literalinclude:: ../../../../../samples/bluetooth/l2cap_coc_acceptor/src/main.c
   :language: c
   :start-after: doc l2cap server start
   :end-before: doc l2cap server end
   :dedent:

一个完整的可运行示例，用于演示 L2CAP 动态通道，可在 acceptor（服务器）示例中找到：:zephyr:code-sample:`bluetooth_l2cap_coc_acceptor`

固定通道
--------------

用户还可以使用 :c:macro:`BT_L2CAP_FIXED_CHANNEL_DEFINE` 宏定义固定通道。固定通道在连接建立时初始化，不支持分片。注意，即使 ``accept`` 回调以 :c:struct:`bt_l2cap_chan` 形式传递通道引用，所分配的对象仍必须是 :c:struct:`bt_l2cap_le_chan` 类型，并且该引用必须指向其 ``chan`` 成员。下面展示了如何定义固定通道的示例。

.. code-block:: c

   static struct bt_l2cap_le_chan fixed_chan[CONFIG_BT_MAX_CONN];

   /* Callbacks are assumed to be defined prior. */
   static struct bt_l2cap_chan_ops ops = {
       .recv = recv_cb,
       .sent = sent_cb,
       .connected = connected_cb,
       .disconnected = disconnected_cb,
   };

   static int l2cap_fixed_accept(struct bt_conn *conn, struct bt_l2cap_chan **chan)
   {
       uint8_t conn_index = bt_conn_index(conn);

       fixed_chan[conn_index] = (struct bt_l2cap_le_chan){
           .chan.ops = &ops,
       };

       *chan = &fixed_chan[conn_index].chan;

       return 0;
   }

   BT_L2CAP_FIXED_CHANNEL_DEFINE(fixed_channel) = {
       .cid = 0x0010,
       .accept = l2cap_fixed_accept,
   };

客户端通道
---------------

客户端通道可使用 :c:func:`bt_l2cap_chan_connect` API 发起，并可使用 :c:func:`bt_l2cap_chan_disconnect` API 断开。注意，后者也可以断开由服务器创建的通道实例。

完整示例可参考 initiator（客户端）示例：:zephyr:code-sample:`bluetooth_l2cap_coc_initiator`

API Reference
*************

.. doxygengroup:: bt_l2cap