.. _settings_api:

Settings
########

Settings
subsystem
给
modules
一
种
way
用于
store
persistent
的
per
device
的
configuration
和
runtime
state。
一
系列
storage
implementations
被
provided
在
common
的
API
后面
用
FCB、
NVS、
ZMS
或
file
system。
这些
不同
的
implementations
给
application
developer
flexibility
select
appropriate
的
storage
medium
甚至
随着
needs
change
later
change
它。
这
个
subsystem
被
各种
Zephyr
components
used
且
可以
被
user
applications
simultaneously
used。

Settings
items
被
stored
作为
key
value
pair
的
strings。
By
convention
keys
可以
按
define
key
的
package
和
subtree
被
organized
例如
key
``id/serial``
将
define
package
``id``
的
``serial``
configuration
element。

Convenience
的
routines
被
provided
用于
将
key
value
convert
到
string
type
和
从
string
type。

关于
settings
subsystem
的
example
参考
:zephyr:code-sample:`settings`
sample。

.. note::

   从
   Zephyr
   release
   4.1
   起
   对
   non
   filesystem
   storage
   的
   recommended
   backends
   是
   :ref:`NVS
   <nvs_api>`
   和
   :ref:`ZMS
   <zms_api>`。

Handlers
********

对
subtree
的
Settings
handlers
implement
一
set
的
handler
functions。
这些
用
对
:c:func:`settings_register()`
的
call
被
registered
用于
dynamic
的
handlers
或
用
对
:c:macro:`SETTINGS_STATIC_HANDLER_DEFINE()`
的
call
被
defined
用于
static
的
handlers。

**h_get**
    这
    在
    用
    :c:func:`settings_runtime_get()`
    从
    runtime
    backend
    按
    name
    ask
    settings
    element
    value
    时
    被
    called。


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
                 * rc contains value length.
                 */
                return 0;
            }
            /* read-out error */
            return rc;
        }

        return -ENOENT;
    }

    static int foo_settings_export(int (*storage_func)(const char *name,
                                                       const void *value,
                                                       size_t val_len))
    {
        return storage_func("foo/bar", &foo_val, sizeof(foo_val));
    }

    struct settings_handler my_conf = {
        .name = "foo",
        .h_set = foo_settings_set,
        .h_export = foo_settings_export
    };

Example: Persist Runtime State
******************************

This is a simple example showing how to persist runtime state. In this example,
only ``h_set`` is defined, which is used when restoring value from
persistent storage.

In this example, the ``main`` function increments ``foo_val``, and then
persists the latest number. When the system restarts, the application calls
:c:func:`settings_load()` while initializing, and ``foo_val`` will continue counting
up from where it was before restart.

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/sys/reboot.h>
    #include <zephyr/settings/settings.h>
    #include <zephyr/sys/printk.h>
    #include <inttypes.h>

    #define DEFAULT_FOO_VAL_VALUE 0

    static uint8_t foo_val = DEFAULT_FOO_VAL_VALUE;

    static int foo_settings_set(const char *name, size_t len,
                                settings_read_cb read_cb, void *cb_arg)
    {
        const char *next;
        int rc;

        if (settings_name_steq(name, "bar", &next) && !next) {
            if (len != sizeof(foo_val)) {
                return -EINVAL;
            }

            rc = read_cb(cb_arg, &foo_val, sizeof(foo_val));
            if (rc >= 0) {
                return 0;
            }

            return rc;
        }


        return -ENOENT;
    }

    struct settings_handler my_conf = {
        .name = "foo",
        .h_set = foo_settings_set
    };

    int main(void)
    {
        settings_subsys_init();
        settings_register(&my_conf);
        settings_load();

        foo_val++;
        settings_save_one("foo/bar", &foo_val, sizeof(foo_val));

        printk("foo: %d\n", foo_val);

        k_msleep(1000);
        sys_reboot(SYS_REBOOT_COLD);
    }

Example: Custom Backend Implementation
**************************************

This is a simple example showing how to register a simple custom backend
handler (:kconfig:option:`CONFIG_SETTINGS_CUSTOM`).

.. code-block:: c

    static int settings_custom_load(struct settings_store *cs,
                                    const struct settings_load_arg *arg)
    {
        //...
    }

    static int settings_custom_save(struct settings_store *cs, const char *name,
                                    const char *value, size_t val_len)
    {
        //...
    }

    /* custom backend interface */
    static struct settings_store_itf settings_custom_itf = {
        .csi_load = settings_custom_load,
        .csi_save = settings_custom_save,
    };

    /* custom backend node */
    static struct settings_store settings_custom_store = {
        .cs_itf = &settings_custom_itf
    };

    int settings_backend_init(void)
    {
        /* register custom backend */
        settings_dst_register(&settings_custom_store);
        settings_src_register(&settings_custom_store);
        return 0;
    }

API Reference
*************

The Settings subsystem APIs are provided by :zephyr_file:`include/zephyr/settings/settings.h`.

API for general settings usage
==============================
.. doxygengroup:: settings

API for key-name processing
===========================
.. doxygengroup:: settings_name_proc

API for runtime settings manipulation
=====================================
.. doxygengroup:: settings_rt

API of backend interface
========================
..  doxygengroup:: settings_backend