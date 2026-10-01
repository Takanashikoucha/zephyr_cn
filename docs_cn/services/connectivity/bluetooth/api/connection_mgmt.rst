.. _bluetooth_connection_mgmt:

Connection Management
#####################

Zephyr Bluetooth stack 使用称为 :c:struct:`bt_conn` 的 abstraction 表示与其他设备的 connections。此 struct 的内部不暴露给 application（但可用 :c:func:`bt_conn_get_info` API 获取有限信息（如 remote address。Connection objects 为 reference counted（且 application 预期在较长时期存储 connection pointer 时使用 :c:func:`bt_conn_ref` API（因为这确保 object 保持有效（即使 connection 断开。类似地（释放对 connection 的 reference 时使用 :c:func:`bt_conn_unref` API。

一个常见错误是忘记释放由 functions :c:func:`bt_conn_le_create` 和 :c:func:`bt_conn_le_create_synced` 创建的 connection object 的 reference。为防止此（使用 :kconfig:option:`CONFIG_BT_CONN_CHECK_NULL_BEFORE_CREATE` Kconfig option（其强制这些 functions 在传递给它们的 connection pointer 非 NULL 时返回 error。这有助于发现此类问题并避免由不释放 connection object 引起的 sporadic bugs。

Application 可通过使用 :c:func:`bt_conn_cb_register` 或 :c:macro:`BT_CONN_CB_DEFINE` APIs 注册 :c:struct:`bt_conn_cb` struct 来跟踪 connections。此 struct 让 application 定义 connection & disconnection events 以及其他与 connection 相关 events（如 security level 或 connection parameters 变化）的 callbacks。作为 central 时（application 还通过 :c:func:`bt_conn_le_create` API 的返回值获取 connection object。

API Reference
*************

.. doxygengroup:: bt_conn
