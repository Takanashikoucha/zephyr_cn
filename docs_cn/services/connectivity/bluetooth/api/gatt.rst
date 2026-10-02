.. _bt_gatt:


通用属性配置（GATT）
################################

GATT 层管理服务数据库，提供服务注册和属性声明的 API。

GATT 客户端向 GATT 服务器发起命令和请求，并可接收服务器发送的响应、指示和通知。它通过配置选项启用：
:kconfig:option:`CONFIG_BT_GATT_CLIENT`

GATT 服务器接受来自 GATT 客户端的传入命令和请求，并向客户端发送响应、指示和通知。

服务可以通过 :c:func:`bt_gatt_service_register` API 注册，该 API 接收 :c:struct:`bt_gatt_service` 结构，该结构提供服务包含的属性列表。辅助宏 :c:macro:`BT_GATT_SERVICE()` 可用于声明服务。

属性可以使用 :c:struct:`bt_gatt_attr` 结构或以下辅助宏之一声明：

    :c:macro:`BT_GATT_PRIMARY_SERVICE`
        声明主服务。

    :c:macro:`BT_GATT_SECONDARY_SERVICE`
        声明次级服务。

    :c:macro:`BT_GATT_INCLUDE_SERVICE`
        声明包含服务。

    :c:macro:`BT_GATT_CHARACTERISTIC`
        声明特征。

    :c:macro:`BT_GATT_DESCRIPTOR`
        声明描述符。

    :c:macro:`BT_GATT_ATTRIBUTE`
        声明属性。

    :c:macro:`BT_GATT_CCC`
        声明客户端特征配置。

    :c:macro:`BT_GATT_CEP`
        声明特征扩展属性。

    :c:macro:`BT_GATT_CUD`
        声明特征用户格式。

每个属性包含一个 ``uuid``（描述其类型）、一个 ``read`` 回调、一个 ``write`` 回调和一组权限。如果属性权限不允许相应操作，read 和 write 回调都可以设置为 NULL。

.. note::
   GATT 中不支持 32 位 UUID。当 UUID 包含在 ATT PDU 中时，所有 32 位 UUID 必须转换为 128 位 UUID。

.. note::
   属性的 ``read`` 和 ``write`` 回调直接从接收线程调用，因此不建议在其中长时间阻塞。

属性值变化可以使用 :c:func:`bt_gatt_notify` API 进行通知，也可以使用 :c:func:`bt_gatt_notify_cb`，后者允许传入一个回调，在需要知道数据确切何时通过空中传输时调用。指示由 :c:func:`bt_gatt_indicate` API 支持。

发现过程可以使用 :c:func:`bt_gatt_discover` API 发起，该 API 接收 :c:struct:`bt_gatt_discover_params` 结构，该结构描述发现类型。参数还充当过滤器：设置 ``uuid`` 字段时仅发现匹配的属性，将其设置为 NULL 则允许发现所有属性。

.. note::
   不支持缓存已发现的属性。

读操作由 :c:func:`bt_gatt_read` API 支持，接收 :c:struct:`bt_gatt_read_params` 结构作为参数。参数中可设置一个或多个属性，但设置多个句柄需要选项：
:kconfig:option:`CONFIG_BT_GATT_READ_MULTIPLE`

写操作由 :c:func:`bt_gatt_write` API 支持，接收 :c:struct:`bt_gatt_write_params` 结构作为参数。如果写操作不需要响应，可以使用 :c:func:`bt_gatt_write_without_response` 或 :c:func:`bt_gatt_write_without_response_cb` API，后者的工作方式类似于 :c:func:`bt_gatt_notify_cb`。

对通知和指示的订阅可以使用 :c:func:`bt_gatt_subscribe` API 发起，该 API 接收 :c:struct:`bt_gatt_subscribe_params` 作为参数。支持对同一属性的多个订阅，因此同一属性可能触发多个 ``notify`` 回调。订阅可以使用 :c:func:`bt_gatt_unsubscribe` API 移除。

.. note::
   移除订阅时，``notify`` 回调以数据设置为 NULL 的方式被调用。

API 参考
*************

.. doxygengroup:: bt_gatt

GATT 服务器
===========

.. doxygengroup:: bt_gatt_server

GATT 客户端
===========

.. doxygengroup:: bt_gatt_client
