.. _jwt_api:

JSON
Web
Token
（JWT）
####################

Overview
********

JSON
Web
Tokens
（JWT）
是
一
种
open
的
industry
standard
（:rfc:`7519`）
的
method
用于
在
两
个
parties
之间
securely
represent
claims。
虽然
JWT
fairly
flexible
这
个
API
limited
于
create
用于
authenticate
到
Google
Core
IoT
infrastructure
所需
的
simple
的
tokens。

在
high
level
JWT
只
是
一
个
signed
的
JSON
blob
client
可以
present
它
作为
token
而
不
是
每次
send
例如
它
的
username/password。

Usage
=====

要
use
JWT
API
include
该
header
file：

.. code-block::
   c

   #include
   <zephyr/data/jwt.h>

Generating
a
JWT
----------------

JWT
subsystem
provide
一
个
lightweight
的
builder
based
的
API
用于
construct
JSON
Web
Tokens
（JWT）。
它
allow
create
tokens
其
payload
（claims）
contain：
expiration
time、
issued
at
time、
和
audience。
Token
然后
用
provided
的
private
key
signed。

.. code-block::
   c

   #include
   <zephyr/data/jwt.h>

   struct
   jwt_builder
   builder;
   char
   buffer[1024];
   int
   ret;

   /*
   Initialize
   the
   builder
   */
