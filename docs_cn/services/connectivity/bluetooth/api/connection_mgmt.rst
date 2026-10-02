.. _bluetooth_connection_mgmt:

连接管理
#####################

Zephyr 蓝牙协议栈使用名为 :c:struct:`bt_conn` 的抽象来表示与其他设备的连接。该结构的内部不暴露给应用程序，但可以通过 :c:func:`bt_conn_get_info` API 获取有限信息（如远端地址）。连接对象采用引用计数，应用程序在较长时间存储连接指针时应使用 :c:func:`bt_conn_ref` API，因为这能确保对象保持有效（即使连接断开）。类似地，释放对连接的引用时应使用 :c:func:`bt_conn_unref` API。

一个常见错误是忘记释放由 :c:func:`bt_conn_le_create` 和 :c:func:`bt_conn_le_create_synced` 函数创建的连接对象的引用。为防止此问题，请使用 :kconfig:option:`CONFIG_BT_CONN_CHECK_NULL_BEFORE_CREATE` Kconfig 选项，该选项强制这些函数在传入的连接指针非 NULL 时返回错误。这有助于发现此类问题，避免由未释放连接对象导致的偶发性错误。

应用程序可以通过使用 :c:func:`bt_conn_cb_register` 或 :c:macro:`BT_CONN_CB_DEFINE` API 注册 :c:struct:`bt_conn_cb` 结构来跟踪连接。该结构允许应用程序为连接和断开连接事件以及其他与连接相关的事件（如安全级别变化或连接参数变化）定义回调。作为中心设备时，应用程序还可以通过 :c:func:`bt_conn_le_create` API 的返回值获取连接对象。

API 参考
*************

.. doxygengroup:: bt_conn
