.. _bt_l2cap_br:

用于 BR/EDR 的 Bluetooth 逻辑链路控制和适配协议（L2CAP）
#########################################################################

L2CAP BR/EDR 提供对 Bluetooth Classic L2CAP（逻辑链路控制和适配协议）特性的支持，包括 ECHO 请求/响应和无连接数据通道。

ECHO 请求/响应
*********************

L2CAP ECHO 特性允许通过发送 ECHO 请求并接收 ECHO 响应来测试连接。
应用程序可以注册回调以监视 ECHO 数据包并发送 ECHO 数据。
该特性通过配置选项启用：:kconfig:option:`CONFIG_BT_CLASSIC`。

注册 ECHO 回调
==========================

要监视 ECHO 请求/响应数据包，请注册 :c:struct:`bt_l2cap_br_echo_cb` 回调
结构体：

.. code-block:: c

    static void echo_req_cb(struct bt_conn *conn, uint8_t identifier, struct net_buf *buf)
    {
        /* Handle ECHO request */
    }

    static void echo_rsp_cb(struct bt_conn *conn, struct net_buf *buf)
    {
        /* Handle ECHO response */
    }

    static struct bt_l2cap_br_echo_cb echo_cb = {
        .req = echo_req_cb,
        .rsp = echo_rsp_cb,
    };

    bt_l2cap_br_echo_cb_register(&echo_cb);

发送 ECHO 请求
====================

要发送 ECHO 请求，请分配一个为 L2CAP 头部保留 :c:macro:`BT_L2CAP_BR_ECHO_REQ_RESERVE`
字节的缓冲区：

.. code-block:: c

    struct net_buf *buf;

    buf = net_buf_alloc(&pool, K_FOREVER);
    net_buf_reserve(buf, BT_L2CAP_BR_ECHO_REQ_RESERVE);
    net_buf_add_mem(buf, data, data_len);

    bt_l2cap_br_echo_req(conn, buf);

发送 ECHO 响应
====================

要发送 ECHO 响应（通常用于响应接收到的 ECHO 请求），请分配一个为 L2CAP 头部保留
:c:macro:`BT_L2CAP_BR_ECHO_RSP_RESERVE` 字节的缓冲区：

.. code-block:: c

    struct net_buf *buf;

    buf = net_buf_alloc(&pool, K_FOREVER);
    net_buf_reserve(buf, BT_L2CAP_BR_ECHO_RSP_RESERVE);
    net_buf_add_mem(buf, data, data_len);

    bt_l2cap_br_echo_rsp(conn, buf);

identifier 参数必须与接收到的 ECHO 请求中的 identifier 相匹配，以便正确
将响应与请求关联起来。

无连接数据通道
***************************

无连接数据通道允许向特定 PSM
（协议/服务复用器）发送和接收数据，而无需建立面向连接的 L2CAP 通道。
该特性通过配置选项启用：:kconfig:option:`CONFIG_BT_L2CAP_CONNLESS`。

注册无连接回调
====================================

要接收无连接数据，请注册 :c:struct:`bt_l2cap_br_connless_cb` 回调结构体：

.. code-block:: c

    static void connless_recv_cb(struct bt_conn *conn, uint16_t psm, struct net_buf *buf)
    {
        /* Handle received connectionless data */
    }

    static struct bt_l2cap_br_connless_cb connless_cb = {
        .psm = MY_PSM,  /* Or 0 to receive all */
        .sec_level = BT_SECURITY_L1,
        .recv = connless_recv_cb,
    };

    bt_l2cap_br_connless_register(&connless_cb);

发送无连接数据
===========================

要发送无连接数据，请分配一个保留了 :c:macro:`BT_L2CAP_CONNLESS_RESERVE`
字节的缓冲区：

.. code-block:: c

    struct net_buf *buf;

    buf = net_buf_alloc(&pool, K_FOREVER);
    net_buf_reserve(buf, BT_L2CAP_CONNLESS_RESERVE);
    net_buf_add_mem(buf, data, data_len);

    bt_l2cap_br_connless_send(conn, psm, buf);

API 参考
*************

.. doxygengroup:: bt_l2cap_br
