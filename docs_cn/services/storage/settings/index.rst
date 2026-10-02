.. _settings_api:

设置（Settings）
########

设置（Settings）子系统为模块提供了一种存储每设备持久化配置和运行时状态的方式。在统一 API 之后提供了多种存储实现，使用 FCB、NVS、ZMS 或文件系统。这些不同的实现为应用程序开发者提供了灵活性，可以选择合适的存储介质，甚至随着需求变化之后更换。该子系统被各种 Zephyr 组件使用，也可以被用户应用程序同时使用。

设置项以键值对字符串的形式存储。按照约定，键可以由定义该键的包和子树来组织，例如键 ``id/serial`` 将定义包 ``id`` 的 ``serial`` 配置元素。

提供了便捷例程，用于在键值与字符串类型之间相互转换。

关于设置子系统的示例，请参见 :zephyr:code-sample:`settings` 示例。

.. note::

   从 Zephyr 4.1 版本起，非文件系统存储的推荐后端是 :ref:`NVS <nvs_api>` 和 :ref:`ZMS <zms_api>`。

处理器（Handlers）
********

针对子树的设置处理器实现了一组处理器函数。对于动态处理器，通过调用 :c:func:`settings_register()` 进行注册；对于静态处理器，通过调用 :c:macro:`SETTINGS_STATIC_HANDLER_DEFINE()` 进行定义。

**h_get**
    当使用 :c:func:`settings_runtime_get()` 从运行时后端按名称请求某个设置元素的值时，会调用该函数。

**h_set**
    当使用 :c:func:`settings_load()` 从持久化存储加载值时，或使用运行时后端的 :c:func:`settings_runtime_set()` 时，会调用该函数。

**h_commit**
    在设置全部加载完成后会调用该函数。有时你不想让某个设置值立即生效，例如存在多个相互依赖的设置时。

**h_export**
    该函数被调用以写入所有当前设置。当 :c:func:`settings_save()` 尝试保存设置或传输到任何用户实现的后端时，会发生这种情况。

设置处理器还有一个提交优先级 ``cprio``，可用于对 ``h_commit`` 调用进行优先级排序。这在例如某个子系统初始化一个其他 ``h_commit`` 调用所依赖的服务时是有优势的。

设置处理器的 ``h_commit`` 例程默认以 ``cprio = 0`` 初始化；以不同的优先级初始化设置处理器，对于动态处理器通过调用 :c:func:`settings_register_with_cprio()` 完成，对于静态处理器通过调用 :c:macro:`SETTINGS_STATIC_HANDLER_DEFINE_WITH_CPRIO()` 完成。指定的 ``cprio`` 值是一个整数，数值越小表示优先级越高。

后端（Backends）
********

后端用于向设置处理器加载和保存数据，并实现一组处理器函数。对于可以加载数据的后端，通过调用 :c:func:`settings_src_register()` 进行注册；对于可以保存数据的后端，通过调用 :c:func:`settings_dst_register()` 进行注册。当前实现允许多个源后端，但只允许单个目标后端。

**csi_load**
    当使用 :c:func:`settings_load()` 从持久化存储加载值时，会调用该函数。

**csi_load_one**
    当使用 :c:func:`settings_load_one()` 仅从持久化存储加载一个条目时，会调用该函数。

**csi_get_val_len**
    当使用 :c:func:`settings_get_val_len()` 从持久化存储获取值的长度时，会调用该函数。

**csi_save**
    当使用 :c:func:`settings_save_one()` 将单个设置保存到持久化存储时，会调用该函数。

**csi_save_start**
    当使用 :c:func:`settings_save()` 或 :c:func:`settings_save_subtree()` 开始保存所有当前设置时，会调用该函数。

**csi_save_end**
    在使用 :c:func:`settings_save()` 或 :c:func:`settings_save_subtree()` 保存完所有当前设置之后，会调用该函数。

Zephyr 存储后端
***********************

Zephyr 提供以下存储后端：

* Flash 循环缓冲区（:kconfig:option:`CONFIG_SETTINGS_FCB`）。
* 文件系统中的文件（:kconfig:option:`CONFIG_SETTINGS_FILE`）。
* 非易失性存储（:kconfig:option:`CONFIG_SETTINGS_NVS`）。
* Zephyr 内存存储（:kconfig:option:`CONFIG_SETTINGS_ZMS`）。

你可以为设置声明多个源；调用 :c:func:`settings_load()` 时，所有这些源中的设置都会被恢复。

写入设置的目标只能有一个；调用 :c:func:`settings_save()` 或 :c:func:`settings_save_one()` 时，数据就存储在这里。

FCB 读目标使用 :c:func:`settings_fcb_src()` 注册，写目标使用 :c:func:`settings_fcb_dst()` 注册。作为副作用，:c:func:`settings_fcb_src()` 会初始化 FCB 区域，因此必须在调用 :c:func:`settings_fcb_dst()` 之前调用。文件读目标使用 :c:func:`settings_file_src()` 注册，写目标使用 :c:func:`settings_file_dst()` 注册。

非易失性存储读目标使用 :c:func:`settings_nvs_src()` 注册，写目标使用 :c:func:`settings_nvs_dst()` 注册。

Zephyr 内存存储（ZMS）读目标使用 :c:func:`settings_zms_src()` 注册，写目标使用 :c:func:`settings_zms_dst()` 注册。

ZMS 后端的特点是在将设置键存储到持久化存储之前，使用哈希函数对其哈希。这种实现意味着，如果存储了大量不同的键，键的哈希之间可能会发生一些冲突。这个数量取决于所选的哈希函数。

ZMS 后端可以处理最多 :math:`2^n` 次冲突，其中 n 由 (:kconfig:option:`CONFIG_SETTINGS_ZMS_MAX_COLLISIONS_BITS`) 定义。


存储位置
****************

FCB、非易失性存储（NVS）和 ZMS 后端默认查找标签为 "storage" 的固定分区。可以通过设置设备树中 chosen 节点的 ``zephyr,settings-partition`` 属性来选择不同的分区。

文件后端用于存储设置的文件路径通过选项 :kconfig:option:`CONFIG_SETTINGS_FILE_PATH` 选择。

从持久化存储加载数据
************************************

调用 :c:func:`settings_load()` 会使用 ``h_set`` 实现将设置数据从存储加载到易失性内存。所有数据加载完成后，会触发 ``h_commit`` 处理器，向应用程序发出信号表示设置已成功获取。

或者，调用 :c:func:`settings_load_one()` 将只加载一个设置条目并将其存储在提供的缓冲区中。

可选地，要仅获取与设置条目关联的值长度，可以调用 :c:func:`settings_get_val_len()`。例如，动态分配数据缓冲区的应用程序需要在使用 settings_load_one() 读取之前获取数据大小，就会用到它。

从技术上讲，FCB 和文件后端可能存储一些实体的历史。这意味着最新的数据实体存储在任何较旧的现有数据实体之后。从 Zephyr 2.1 开始，后端必须过滤掉所有旧实体，并只使用最新实体调用回调。

将数据存储到持久化存储
**********************************

调用 :c:func:`settings_save_one()` 会使用后端实现将设置数据存储到存储介质。调用 :c:func:`settings_save()` 会使用 ``h_export`` 实现，通过 :c:func:`settings_save_one()` 在一次操作中存储不同的数据。只有当某个键预期被 :c:func:`settings_save()` 调用存储时，它才需要被某个 ``h_export`` 覆盖。

对于 FCB 和文件后端，只有数据实际改变了当前键值 的存储请求才会被存储，因此无需检查值是否被应用程序改变。这样的存储机制意味着存储中可能包含一个键的多个值赋值，而只有最后一个是该键的当前值。

垃圾回收
==================
当存储变满（FCB）或占用过多空间（文件）时，
后端会移除非最近的键值对记录以及不必要的键删除记录。

安全域设置
************************
目前设置子系统不支持同一实例同时提供安全配置存储和非安全配置存储。
建议安全域使用自己的设置实例，如有需要，可通过专用接口向非安全域提供数据（视情况而定）。

示例：设备配置
*****************************

这是一个简单的示例，其中设置处理器只实现了 ``h_set``
和 ``h_export``。当值从存储恢复（或初始设置）时调用 ``h_set``，
``h_export`` 借助 ``storage_func()`` 用于将值写入存储。用户还可以实现其他
导出功能，例如写入 shell 控制台。

.. code-block:: c

    #define DEFAULT_FOO_VAL_VALUE 1

    static int8 foo_val = DEFAULT_FOO_VAL_VALUE;

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
                /* key-value pair was properly read.
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

示例：持久化运行时状态
******************************

这是一个简单的示例，展示如何持久化运行时状态。在该示例中，
只定义了 ``h_set``，它在从持久化存储恢复值时使用。

在该示例中，``main`` 函数对 ``foo_val`` 加一，
然后持久化最新的数值。当系统重启时，应用程序在初始化期间调用
:c:func:`settings_load()`，``foo_val`` 将从重启前的值继续往上计数。

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

示例：自定义后端实现
**************************************

这是一个简单的示例，展示如何注册一个简单的自定义后端
处理器（:kconfig:option:`CONFIG_SETTINGS_CUSTOM`）。

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

API 参考
*************

设置子系统的 API 由 :zephyr_file:`include/zephyr/settings/settings.h` 提供。

用于一般设置使用的 API
==============================
.. doxygengroup:: settings

用于键名处理的 API
===========================
.. doxygengroup:: settings_name_proc

用于运行时设置操作的 API
=====================================
.. doxygengroup:: settings_rt

后端接口的 API
========================
..  doxygengroup:: settings_backend
