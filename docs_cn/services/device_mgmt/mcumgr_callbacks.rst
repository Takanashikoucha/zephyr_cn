.. _mcumgr_callbacks:

MCUmgr Callbacks
################

概述
********

MCUmgr 有一个可定制的回调/通知系统，允许应用程序
（和模块）代码接收它们感兴趣的 MCUmgr 事件的回调，
并对这些事件作出反应，或者向调用函数返回状态码，
以控制该操作是否应被允许。一个例子是
fs_mgmt 组，其中文件访问可以被门控，
回调允许应用程序检查请求路径，并允许或
拒绝对该文件的访问，或者可以将提供的路径重写为
不同的路径，以支持透明的文件重定向。

实现
**************

启用
========

基础回调/通知系统可以使用
:kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` 启用，它会将
注册和通知系统编译进代码。默认不会提供任何
回调，因为构建所支持的回调还须
通过启用所需回调的 Kconfig 来选择（详见
:ref:`mcumgr_cb_events`）。然后可以声明
一个 :c:type:`mgmt_cb` 类型定义的回调函数，并通过
在 :c:struct:`mgmt_callback` 结构体中为期望的
事件调用 :c:func:`mgmt_callback_register` 来注册。处理器按
注册顺序被调用。

启用该系统后，可以在
应用程序代码中按如下方式设置并定义一个基本处理器：

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/mgmt/mcumgr/mgmt/mgmt.h>
    #include <zephyr/mgmt/mcumgr/mgmt/callbacks.h>

    struct mgmt_callback my_callback;

    enum mgmt_cb_return my_function(uint32_t event, enum mgmt_cb_return prev_status,
                                    int32_t *rc, uint16_t *group, bool *abort_more,
                                    void *data, size_t data_size)
    {
        if (event == MGMT_EVT_OP_CMD_DONE) {
            /* This is the event we registered for */
        }

        /* Return OK status code to continue with acceptance to underlying handler */
        return MGMT_CB_OK;
    }

    int main()
    {
        my_callback.callback = my_function;
        my_callback.event_id = MGMT_EVT_OP_CMD_DONE;
        mgmt_callback_register(&my_callback);
    }

此代码为 :c:enumerator:`MGMT_EVT_OP_CMD_DONE`
事件注册了一个处理器，它会在 MCUmgr 命令被处理并
生成输出后被调用，注意这要求启用
:kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS` 才能接收
此回调。

可以设置多个回调来使用单个函数作为
公共回调，并且每个事件可以使用许多不同的函数，通过
为每个组注册一次，或者可以使用
``MGMT_EVT_OP_*_ALL`` 事件之一来启用整个组的所有
通知，或者处理器可以使用
:c:enumerator:`MGMT_EVT_OP_ALL` 为每个
通知设置。设置
处理器时，只能组合同一个组中的事件，例如
可以用单个注册调用设置 5 个 img_mgmt 回调，但
如果要
再设置一个 os_mgmt 回调，必须作为单独的
注册来完成。组 ID 是数值递增的，事件 ID 是位掩码值，
因此有此限制。

例如，以下注册是被允许的，它用单个回调函数在
单个注册中注册了 3
个 SMP 事件：

.. code-block:: c

    my_callback.callback = my_function;
    my_callback.event_id = (MGMT_EVT_OP_CMD_RECV |
                            MGMT_EVT_OP_CMD_STATUS |
                            MGMT_EVT_OP_CMD_DONE);
    mgmt_callback_register(&my_callback);

以下代码不被允许，并且会导致未定义行为，因为
它混合了 IMG 管理组和 OS 管理组，其中
组 **不是** 位掩码值，只有事件才是：

.. code-block:: c

    my_callback.callback = my_function;
    my_callback.event_id = (MGMT_EVT_OP_IMG_MGMT_DFU_STARTED |
                            MGMT_EVT_OP_OS_MGMT_RESET);
    mgmt_callback_register(&my_callback);

.. _mcumgr_cb_events:

事件
======

事件可以通过启用相应的 Kconfig 选项来选择：

 - :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS`
   MCUmgr 命令状态（:c:enumerator:`MGMT_EVT_OP_CMD_RECV`、
   :c:enumerator:`MGMT_EVT_OP_CMD_STATUS`、
   :c:enumerator:`MGMT_EVT_OP_CMD_DONE`）
 - :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK`
   fs_mgmt 文件访问（:c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS`）
 - :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_UPLOAD_CHECK_HOOK`
   img_mgmt 上传检查（:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CHUNK`）
 - :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS`
   img_mgmt 上传状态（:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STOPPED`、
   :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STARTED`、
   :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_PENDING`、
   :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED`）
 - :kconfig:option:`CONFIG_MCUMGR_GRP_OS_RESET_HOOK`
   os_mgmt 复位检查（:c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET`）
 - :kconfig:option:`CONFIG_MCUMGR_GRP_SETTINGS_ACCESS_HOOK`
   settings_mgmt 访问（:c:enumerator:`MGMT_EVT_OP_SETTINGS_MGMT_ACCESS`）

操作
=======

某些回调期望返回一个状态码来允许或禁止一个操作，
例如允许或拒绝文件访问的 fs_mgmt 访问钩子。对于这些
处理器，处理器返回的第一个非 OK 错误码将被返回给
MCUmgr 客户端。

选择性拒绝文件访问的示例：

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/mgmt/mcumgr/mgmt/mgmt.h>
    #include <zephyr/mgmt/mcumgr/mgmt/callbacks.h>
    #include <string.h>

    struct mgmt_callback my_callback;

    enum mgmt_cb_return my_function(uint32_t event, enum mgmt_cb_return prev_status,
                                    int32_t *rc, uint16_t *group, bool *abort_more,
                                    void *data, size_t data_size)
    {
        /* Only run this handler if a previous handler has not failed */
        if (event == MGMT_EVT_OP_FS_MGMT_FILE_ACCESS && prev_status == MGMT_CB_OK) {
            struct fs_mgmt_file_access *fs_data = (struct fs_mgmt_file_access *)data;

            /* Check if this is an upload and deny access if it is, otherwise check
             * the path and deny if is matches a name
             */
            if (fs_data->access == FS_MGMT_FILE_ACCESS_WRITE) {
                /* Return an access denied error code to the client and abort calling
                 * further handlers
                 */
                *abort_more = true;
                *rc = MGMT_ERR_EACCESSDENIED;

                return MGMT_CB_ERROR_RC;
            } else if (strcmp(fs_data->filename, "/lfs1/false_deny.txt") == 0) {
                /* Return a no entry error code to the client, call additional handlers
                 * (which will have failed set to true)
                 */
                *rc = MGMT_ERR_ENOENT;

                return MGMT_CB_ERROR_RC;
            }
        }

        /* Return OK status code to continue with acceptance to underlying handler */
        return MGMT_CB_OK;
    }

    int main()
    {
        my_callback.callback = my_function;
        my_callback.event_id = MGMT_EVT_OP_FS_MGMT_FILE_ACCESS;
        mgmt_callback_register(&my_callback);
    }

此代码为
:c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS` 事件注册了一个处理器，它会在
收到 fs_mgmt 文件读/写命令后被调用，以检查对
该文件的访问是否应被允许，注意这要求启用
:kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK` 才能接收
此回调。
可以返回两种类型的错误：``rc`` 参数可设为
一个 :c:enum:`mcumgr_err_t` 错误码并返回
:c:enumerator:`MGMT_CB_ERROR_RC`，或者可以设置组错误码（由 MCUmgr
协议版本 2 引入），方法是将 ``group`` 值设为
该组，将 ``rc`` 值设为组错误码，并返回 :c:enumerator:`MGMT_CB_ERROR_ERR`。

MCUmgr 命令回调的使用/添加新事件类型
====================================================

要为 MCUmgr 命令添加回调，可以
使用事件 ID 调用 :c:func:`mgmt_callback_notify`，可选地
传回一个数据结构给回调（可被处理器修改）。如果无需传回
数据，
可用 ``NULL`` 替代，并将数据大小设为 0。

一个 MCUmgr 命令处理器示例：

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zcbor_common.h>
    #include <zcbor_encode.h>
    #include <zephyr/mgmt/mcumgr/smp/smp.h>
    #include <zephyr/mgmt/mcumgr/mgmt/mgmt.h>
    #include <zephyr/mgmt/mcumgr/mgmt/callbacks.h>

    #define MGMT_EVT_GRP_USER_ONE MGMT_EVT_GRP_USER_CUSTOM_START

    enum user_one_group_events {
        /** Callback on first post, data is test_struct. */
        MGMT_EVT_OP_USER_ONE_FIRST  = MGMT_DEF_EVT_OP_ID(MGMT_EVT_GRP_USER_ONE, 0),

        /** Callback on second post, data is test_struct. */
        MGMT_EVT_OP_USER_ONE_SECOND = MGMT_DEF_EVT_OP_ID(MGMT_EVT_GRP_USER_ONE, 1),

        /** Used to enable all user_one events. */
        MGMT_EVT_OP_USER_ONE_ALL    = MGMT_DEF_EVT_OP_ALL(MGMT_EVT_GRP_USER_ONE),
    };

    struct test_struct {
        uint8_t some_value;
    };

    static int test_command(struct mgmt_ctxt *ctxt)
    {
        int rc;
        int err_rc;
        uint16_t err_group;
        zcbor_state_t *zse = ctxt->cnbe->zs;
        bool ok;
        struct test_struct test_data = {
            .some_value = 8,
        };

        rc = mgmt_callback_notify(MGMT_EVT_OP_USER_ONE_FIRST, &test_data,
                                  sizeof(test_data), &err_rc, &err_group);

        if (rc != MGMT_CB_OK) {
            /* A handler returned a failure code */
            if (rc == MGMT_CB_ERROR_RC) {
                /* The failure code is the RC value */
                return err_rc;
            }

            /* The failure is a group and ID error value */
            ok = smp_add_cmd_err(zse, err_group, (uint16_t)err_rc);
            goto end;
        }

        /* All handlers returned success codes */
        ok = zcbor_tstr_put_lit(zse, "output_value") &&
             zcbor_int32_put(zse, 1234);

    end:
        rc = (ok ? MGMT_ERR_EOK : MGMT_ERR_EMSGSIZE);

        return rc;
    }

如果回调无需响应，函数调用可以
被强制转换为 void。

.. _mcumgr_cb_migration:

迁移
*********

如果存在使用 Zephyr 3.2
及更早版本中旧回调系统的既有代码，则需要迁移到
新系统。迁移
代码时，以下回调注册函数需要迁移为
使用 :c:func:`mgmt_callback_register` 注册回调（注意
:kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` 须
被设置
以启用新的通知系统，除了任何迁移之外）：

 * mgmt_evt
   使用 :c:enumerator:`MGMT_EVT_OP_CMD_RECV`、
   :c:enumerator:`MGMT_EVT_OP_CMD_STATUS` 或
   :c:enumerator:`MGMT_EVT_OP_CMD_DONE` 作为同名事件的
   直接替换，其中提供的数据为 :c:struct:`mgmt_evt_op_cmd_arg`。
   须设置 :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS`。
 * fs_mgmt_register_evt_cb
   使用 :c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS`，其中提供的
   数据为 :c:struct:`fs_mgmt_file_access`。不再返回 true 允许
   操作或 false 拒绝，而须返回一个 MCUmgr 结果码，
   :c:enumerator:`MGMT_ERR_EOK` 允许
   操作，其他任何返回码
   将禁止该操作并向客户端返回该码
   （:c:enumerator:`MGMT_ERR_EACCESSDENIED` 可用于访问被拒绝
   错误）。须设置 :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK`。
 * img_mgmt_register_callbacks
   若使用了 ``dfu_started_cb``，则使用
   :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STARTED`；
   若使用了 ``dfu_stopped_cb``，则使用
   :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STOPPED`；
   若使用了 ``dfu_pending_cb``，则使用
   :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_PENDING`；
   若使用了 ``dfu_confirmed_cb``，则使用
   :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED`。这些
   回调没有任何返回状态。
   须设置 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS`。
 * img_mgmt_set_upload_cb
   使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CHUNK`，其中提供的
   数据为 :c:struct:`img_mgmt_upload_check`。不再返回 true 允许
   操作或 false 拒绝，而须返回一个 MCUmgr 结果码，
   :c:enumerator:`MGMT_ERR_EOK` 允许
   操作，其他任何返回码
   将禁止该操作并向客户端返回该码
   （:c:enumerator:`MGMT_ERR_EACCESSDENIED` 可用于访问被拒绝
   错误）。须设置 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_UPLOAD_CHECK_HOOK`。
 * os_mgmt_register_reset_evt_cb
   使用 :c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET`。不再返回 true 允许
   操作或 false 拒绝，而须返回一个 MCUmgr 结果码，
   :c:enumerator:`MGMT_ERR_EOK` 允许
   操作，其他任何返回码
   将禁止该操作并向客户端返回该码
   （:c:enumerator:`MGMT_ERR_EACCESSDENIED` 可用于访问被拒绝
   错误）。须设置 :kconfig:option:`CONFIG_MCUMGR_GRP_OS_RESET_HOOK`。

API 参考
*************

.. doxygengroup:: mcumgr_callback_api
