.. _uuid_api:

UUID
####

Overview
********

Universally
Unique
Identifiers
（UUID）
也
known
作为
Globally
Unique
IDentifiers
（GUIDs）
是
128
bit
的
identifiers
它们
intended
guarantee
across
space
和
time
的
uniqueness。
它们
由
:rfc:`9562`
defined。

UUID
subsystem
provide
utility
functions
用于
UUIDs
的
generation、
parsing、
和
manipulation。
它
support
generate
version
4
（random）
和
version
5
（name
based）
的
UUIDs。

Usage
=====

要
use
UUID
API
include
header
file：

.. code-block::
   c

   #include
   <zephyr/sys/uuid.h>

Generating
a
UUIDv4
-------------------

UUIDv4
基于
random
numbers
（hence
require
一
个
entropy
generator）
且
可以
用
:c:func:`uuid_generate_v4`
function
被
generated。
:kconfig:option:`CONFIG_UUID_V4`
也
必须
被
enabled。

.. code-block::
   c

   struct
   uuid
   my_uuid;
   char
   uuid_str[UUID_STR_LEN];

   int
   ret
   =
   uuid_generate_v4(&my_uuid);

   if
   (ret
   !=
   0)
   {
       printk("Failed
   to
   generate
   UUID
   v4
   (err
   %d)\n",
   ret);
       return
   ret;
