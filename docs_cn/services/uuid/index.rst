.. _uuid_api:

UUID
####

Overview
********

通用唯一识别码（UUID），又称全局唯一标识符（GUID），是 128 位标识符，旨在保证在空间和时间上的唯一性。它们由 :rfc:`9562` 定义。

UUID 子系统提供用于生成、解析和操作 UUID 的实用函数。它支持生成版本 4（随机）和版本 5（基于名称）的 UUID。

Usage
=====

要使用 UUID API，请包含头文件：

.. code-block:: c

   #include <zephyr/sys/uuid.h>

Generating a UUIDv4
-------------------

UUIDv4 基于随机数（因此需要熵源生成器），可使用 :c:func:`uuid_generate_v4` 函数生成。同时必须启用 :kconfig:option:`CONFIG_UUID_V4`。

.. code-block:: c

   struct uuid my_uuid;
   char uuid_str[UUID_STR_LEN];

   int ret = uuid_generate_v4(&my_uuid);

   if (ret != 0) {
       printk("Failed to generate UUID v4 (err %d)\n", ret);
       return ret;
   }

   ret = uuid_to_string(&my_uuid, uuid_str);
   if (ret != 0) {
       printk("Failed to convert UUID to string (err %d)\n", ret);
       return ret;
   }

    printk("UUID: %s\n", uuid_str);

Generating a UUIDv5
-------------------

UUIDv5 由一个命名空间 UUID 和一个名称（二进制数据）生成，可使用 :c:func:`uuid_generate_v5` 函数生成。同时必须启用 :kconfig:option:`CONFIG_UUID_V5`。

UUIDv5 是确定性的：相同的命名空间和名称始终产生相同的 UUID。

.. code-block:: c

   struct uuid ns_uuid;
   struct uuid my_uuid;
   char uuid_str[UUID_STR_LEN];

   /* Well-known namespace ID for URLs (RFC 9562) */
   uuid_from_string("6ba7b811-9dad-11d1-80b4-00c04fd430c8", &ns_uuid);

   const char *name = "https://zephyrproject.org/";
   int ret = uuid_generate_v5(&ns_uuid, name, strlen(name), &my_uuid);

   if (ret != 0) {
       printk("Failed to generate UUID v5 (err %d)\n", ret);
       return ret;
   }

   ret = uuid_to_string(&my_uuid, uuid_str);
   if (ret != 0) {
       printk("Failed to convert UUID to string (err %d)\n", ret);
       return ret;
   }

   /* outputs: "UUID: abdb72b5-b342-5882-925b-4ce0e3cb4790" */
   printk("UUID: %s\n", uuid_str);

Configuration
*************

相关配置选项：

* :kconfig:option:`CONFIG_UUID`
* :kconfig:option:`CONFIG_UUID_V4`
* :kconfig:option:`CONFIG_UUID_V5`
* :kconfig:option:`CONFIG_UUID_BASE64`

API Reference
*************

.. doxygengroup:: uuid
