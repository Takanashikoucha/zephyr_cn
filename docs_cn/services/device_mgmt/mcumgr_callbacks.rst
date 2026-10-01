.. _mcumgr_callbacks:

MCUmgr Callbacks
################

Overview
********

MCUmgr 有可定制 callback/notification system（允许 application
（和 module）code 接收感兴趣的 MCUmgr events 的 callbacks（并
对其作出反应（或向提供控制该 action 是否应被允许的 calling function
返回 status code。一个示例为
fs_mgmt group（其中 file access 可被 gate（
callback 允许 application 检查 request path（并允许或
拒绝对该 file 的 access（或可将提供的 path 重写为
不同 path 以支持透明 file redirection。

Implementation
**************

Enabling
========

基础 callback/notification system 可用
:kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` 启用（其将
registration 和 notification system 编译进
code。默认不提供任何
callbacks（因为 build 支持的 callbacks 还须
通过启用所需 callbacks 的 Kconfigs 选择（细节
参见 :ref:`mcumgr_cb_events`。然后可声明
:c:type:`mgmt_cb` type 定义的 callback function（并通过
在 :c:struct:`mgmt_callback` structure 中为期望
event 调用 :c:func:`mgmt_callback_register` 注册。Handlers 按
注册顺序调用。

启用 system 后（可按如下方式在
application code 中设置并定义基本 handler：

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

此 code 注册 :c:enumerator:`MGMT_EVT_OP_CMD_DONE`
event 的 handler（其在 MCUmgr command 处理并
生成 output 后调用（注意须启用
:kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS` 才能接收
此 callback。

可设置多个 callbacks 用单个 function 作为
common callback（且每个 event 可用许多不同 functions（通过
每个 group 注册一次（或可用
``MGMT_EVT_OP_*_ALL`` events 之一启用整个 group 的所有
notifications（或 handler 可用
:c:enumerator:`MGMT_EVT_OP_ALL` 为每个
notification 设置。设置
handlers 时（仅能组合同一 group 中的 events（例如
5 个 img_mgmt callbacks 可用单个 registration 调用设置（但
还要
setup os_mgmt callback 的 callback 须作为单独
registration 完成。Group IDs 为数值递增（event IDs 为 bitmask values（
故有此限制。

例如（以下 registration 被允许（其用单个 callback function 在
单个 registration 中注册 3
个 SMP events：

.. code-block:: c

    my_callback.callback = my_function;
    my_callback.event_id = (MGMT_EVT_OP_CMD_RECV |
                            MGMT_EVT_OP_CMD_STATUS |
                            MGMT_EVT_OP_CMD_DONE);
    mgmt_callback_register(&my_callback);

以下 code 不被允许（且将导致 undefined operation（因为
其将 IMG management group 与 OS management group 混合（其中
group **非** bitmask value（仅 event 是：

.. code-block:: c

    my_callback.callback = my_function;
    my_callback.event_id = (MGMT_EVT_OP_IMG_MGMT_DFU_STARTED |
                            MGMT_EVT_OP_OS_MGMT_RESET);
    mgmt_callback_register(&my_callback);

.. _mcumgr_cb_events:

Events
======

Events 可通过启用相应 Kconfig option 选择：

 - :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS`
    MCUmgr command status (:c:enumerator:`MGMT_EVT_OP_CMD_RECV`、
    :c:enumerator:`MGMT_EVT_OP_CMD_STATUS`、
    :c:enumerator:`MGMT_EVT_OP_CMD_DONE`)
 - :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK`
    fs_mgmt file access (:c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS`)
 - :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_UPLOAD_CHECK_HOOK`
    img_mgmt upload check (:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CHUNK`)
 - :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS`
    img_mgmt upload status (:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STOPPED`、
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STARTED`、
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_PENDING`、
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED`)
 - :kconfig:option:`CONFIG_MCUMGR_GRP_OS_RESET_HOOK`
    os_mgmt reset check (:c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET`)
 - :kconfig:option:`CONFIG_MCUMGR_GRP_SETTINGS_ACCESS_HOOK`
    settings_mgmt access (:c:enumerator:`MGMT_EVT_OP_SETTINGS_MGMT_ACCESS`)

Actions
=======

某些 callbacks 期望返回 status 以允许或 disallow operation（
示例为允许或拒绝 file access 的 fs_mgmt access hook。这些
handlers 中（handler 返回的第一个非 OK error code 将返回给
MCUmgr client。

选择性拒绝 file access 的示例：

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

此 code 注册
:c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS` event 的 handler（其在
收到 fs_mgmt file read/write command 后调用（以检查对
file 的 access 是否应被允许（注意须启用
:kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK` 才能接收
此 callback。
可返回两种类型的 errors：``rc`` parameter 可设为
:c:enum:`mcumgr_err_t` error code（且返回
:c:enumerator:`MGMT_CB_ERROR_RC`（或可将 ``group`` 值设为
group（``rc``
值设为 group error code（并返回 :c:enumerator:`MGMT_CB_ERROR_ERR` 设置
group error code（MCUmgr
protocol version 2 引入。

MCUmgr Command Callback Usage/Adding New Event Types
====================================================

要为 MCUmgr command 添加 callback（可
用 event ID 调用 :c:func:`mgmt_callback_notify`（可选
data struct 传递给 callback（可被 handlers 修改。若无需传回
data（
可用 ``NULL`` 替代（且 data size 设为 0。

MCUmgr command handler 示例：

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

若 callback 无需 response（函数调用可被
cast 为 void。

.. _mcumgr_cb_migration:

Migration
*********

若有使用 Zephyr 3.2
及更早版本中前 callback system(s) 的既有 code（则须迁移到
新 system。迁移
code 时（以下 callback registration functions 须迁移为
用 :c:func:`mgmt_callback_register` 注册 callbacks（注意
:kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` 须
设置
以启用新 notification system（除任何迁移外）：

 * mgmt_evt
    用 :c:enumerator:`MGMT_EVT_OP_CMD_RECV`、
    :c:enumerator:`MGMT_EVT_OP_CMD_STATUS` 或
    :c:enumerator:`MGMT_EVT_OP_CMD_DONE` 作为同名 events 的
    drop-in replacements（其中提供的 data 为 :c:struct:`mgmt_evt_op_cmd_arg`。
    须设置 :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS`。
 * fs_mgmt_register_evt_cb
    用 :c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS`（其中提供的
    data 为 :c:struct:`fs_mgmt_file_access`。不返回 true 允许
    action 或 false 拒绝（而须返回 MCUmgr result code（
    :c:enumerator:`MGMT_ERR_EOK` 允许
    action（其他任何 return code
    将其 disallow 并向 client 返回该 code
    (:c:enumerator:`MGMT_ERR_EACCESSDENIED` 可用于 access denied
    error。须设置 :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK`。
 * img_mgmt_register_callbacks
    若用 ``dfu_started_cb`` 则用
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STARTED`（
    若用 ``dfu_stopped_cb`` 则用
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STOPPED`（
    若用 ``dfu_pending_cb`` 则用
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_PENDING`（
    若用 ``dfu_confirmed_cb`` 则用
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED`。这些
    callbacks 无任何 return status。
    须设置 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS`。
 * img_mgmt_set_upload_cb
    用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CHUNK`（其中提供的
    data 为 :c:struct:`img_mgmt_upload_check`。不返回 true 允许
    action 或 false 拒绝（而须返回 MCUmgr result code（
    :c:enumerator:`MGMT_ERR_EOK` 允许
    action（其他任何 return code
    将其 disallow 并向 client 返回该 code
    (:c:enumerator:`MGMT_ERR_EACCESSDENIED` 可用于 access denied
    error。须设置 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_UPLOAD_CHECK_HOOK`。
 * os_mgmt_register_reset_evt_cb
    用 :c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET`。不返回 true 允许
    action 或 false 拒绝（而须返回 MCUmgr result code（
    :c:enumerator:`MGMT_ERR_EOK` 允许
    action（其他任何 return code
    将其 disallow 并向 client 返回该 code
    (:c:enumerator:`MGMT_ERR_EACCESSDENIED` 可用于 access denied
    error。须设置 :kconfig:option:`CONFIG_MCUMGR_GRP_OS_RESET_HOOK`。

API Reference
*************

.. doxygengroup:: mcumgr_callback_api
