.. _mcumgr_callbacks:

MCUmgr
Callbacks
################

Overview
********

MCUmgr
有
一
个
customisable
的
callback/notification
system
它
allow
application
（和
module）
code
receive
callbacks
用于
它们
interested
的
MCUmgr
events
并
react
到
它们
或
return
一
个
status
code
到
calling
的
function
它
provide
control
over
action
是否
应该
被
allowed。
这
的
一
个
example
是
fs_mgmt
group
那里
file
access
可以
被
gated
callback
allow
application
inspect
request
的
path
并
allow
或
deny
access
到
该
file
或
它
可以
rewrite
provided
的
path
到
不同
的
path
用于
transparent
的
file
redirection
support。

Implementation
**************

Enabling
========

Base
的
callback/notification
system
可
用
:kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS`
enabled
它
将
registration
和
notification
system
compile
到
code
中。
这
default
下
不
provide
任何
callbacks
因为
build
supported
的
callbacks
必须
也
通过
enable
required
callbacks
的
Kconfig
s
被
selected
（参考
:ref:`mcumgr_cb_events`
获取
further
details）。
带
:c:type:`mgmt_cb`
type
definition
的
callback
function
然后
可以
被
declared
并
通过
call
:c:func:`mgmt_callback_register`
在
:c:struct:`mgmt_callback`
structure
中
为
desired
的
event
registered。
Handlers
按
它们
被
registered
的
order
被
called。

当
system
被
enabled
一
个
basic
的
handler
可以
在
application
code
中
被
set
up
和
defined
如
下：

.. code-block::
   c

   #include
   <zephyr/kernel.h>


.. note::

   以下为原文（待翻译）

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

If no response is required for the callback, the function call be called and
casted to void.

.. _mcumgr_cb_migration:

Migration
*********

If there is existing code using the previous callback system(s) in Zephyr 3.2
or earlier, then it will need to be migrated to the new system. To migrate
code, the following callback registration functions will need to be migrated
to register for callbacks using :c:func:`mgmt_callback_register` (note that
:kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` will need to be set to
enable the new notification system in addition to any migrations):

 * mgmt_evt
    Using :c:enumerator:`MGMT_EVT_OP_CMD_RECV`,
    :c:enumerator:`MGMT_EVT_OP_CMD_STATUS`, or
    :c:enumerator:`MGMT_EVT_OP_CMD_DONE` as drop-in replacements for events of
    the same name, where the provided data is :c:struct:`mgmt_evt_op_cmd_arg`.
    :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS` needs to be set.
 * fs_mgmt_register_evt_cb
    Using :c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS` where the provided
    data is :c:struct:`fs_mgmt_file_access`. Instead of returning true to allow
    the action or false to deny, a MCUmgr result code needs to be returned,
    :c:enumerator:`MGMT_ERR_EOK` will allow the action, any other return code
    will disallow it and return that code to the client
    (:c:enumerator:`MGMT_ERR_EACCESSDENIED` can be used for an access denied
    error). :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK` needs to be
    set.
 * img_mgmt_register_callbacks
    Using :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STARTED` if
    ``dfu_started_cb`` was used,
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STOPPED` if ``dfu_stopped_cb`` was
    used, :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_PENDING` if
    ``dfu_pending_cb`` was used or
    :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED` if ``dfu_confirmed_cb``
    was used. These callbacks do not have any return status.
    :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS` needs to be set.
 * img_mgmt_set_upload_cb
    Using :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CHUNK` where the provided
    data is :c:struct:`img_mgmt_upload_check`. Instead of returning true to
    allow the action or false to deny, a MCUmgr result code needs to be
    returned, :c:enumerator:`MGMT_ERR_EOK` will allow the action, any other
    return code will disallow it and return that code to the client
    (:c:enumerator:`MGMT_ERR_EACCESSDENIED` can be used for an access denied
    error). :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_UPLOAD_CHECK_HOOK` needs to
    be set.
 * os_mgmt_register_reset_evt_cb
    Using :c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET`.  Instead of returning
    true to allow the action or false to deny, a MCUmgr result code needs to be
    returned, :c:enumerator:`MGMT_ERR_EOK` will allow the action, any other
    return code will disallow it and return that code to the client
    (:c:enumerator:`MGMT_ERR_EACCESSDENIED` can be used for an access denied
    error). :kconfig:option:`CONFIG_MCUMGR_GRP_OS_RESET_HOOK` needs to be set.

API Reference
*************

.. doxygengroup:: mcumgr_callback_api
