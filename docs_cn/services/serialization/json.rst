.. _json_api:

JSON
####

Zephyr
provide
一
个
JSON
library
它
可
被
used
用于
encode
和
decode
JSON
data。

Usage
*****

Defining
the
Data
Structure
===========================

First
define
与
JSON
object
对应
的
C
structure
和
将
structure
fields
map
到
JSON
tokens
的
descriptor。

.. code-block::
   c

   #include
   <zephyr/data/json.h>

   struct
   foo
   {
       int
   bar;
       const
   char
   *baz;
   };

   static
   const
   struct
   json_obj_descr
   foo_descr[]
   =
   {
       JSON_OBJ_DESCR_PRIM(struct
   foo,
   bar,
   JSON_TOK_NUMBER),
       JSON_OBJ_DESCR_PRIM(struct
   foo,
   baz,
   JSON_TOK_STRING),
   };

Encoding
========

要
将
C
structure
encode
到
JSON
string
中
use
:c:func:`json_obj_encode_buf`。

.. code-block::
   c

   void
   encode_example(void)
   {
       struct
   foo
   data
   =
   {
   .bar
   =
   42,
   .baz
   =
   "hello"
   };
