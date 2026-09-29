.. _bluetooth_mesh_blob_cli:

BLOB
Transfer
Client
####################

Binary
Large
Object
（BLOB）
Transfer
Client
是
BLOB
transfer
的
sender。
它
支持
在
Push
BLOB
Transfer
Mode
和
Pull
BLOB
Transfer
Mode
两
种
模式
下
向
任何
数量
的
Target
nodes
发送
任何
size
的
BLOBs。

Usage
*****

Initialization
=============

BLOB
Transfer
Client
在
带
一
组
event
handler
callbacks
的
element
上
被
instantiated：

.. code-block:: C

   static
   const
   struct
   bt_mesh_blob_cli_cb
   blob_cb
   =
   {
         /*
         Callbacks
         */
   };

   static
   struct
   bt_mesh_blob_cli
   blob_cli
   =
   {
         .cb
         =
         &blob_cb,
   };

   static
   const
   struct
   bt_mesh_model
   models[]
   =
   {
         BT_MESH_MODEL_BLOB_CLI(&blob_cli),
   };

Transfer
context
================

Transfer
capabilities
retrieval
procedure
和
BLOB
transfer
都
使用
:c:struct:`bt_mesh_blob_cli_inputs`
的
instance
确定
如何
执行
transfer。
BLOB
Transfer
Client
Inputs
structure
在
被
用
于
procedure
之前
必须
至少
用
targets
列表、
application
key
和
time
to
live
（TTL）
value
初始化：

.. code-block:: c
