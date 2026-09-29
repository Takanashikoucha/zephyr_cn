.. _net_buf_interface:

Network
Buffers
###############

.. contents::
    :local:
    :depth:
    2


Overview
********

Network
buffers
是
networking
stack
（以及
Bluetooth
stack）
如何
pass
data
around
的
core
concept。
它们
的
API
在
:zephyr_file:`include/zephyr/net_buf.h`
中
defined。

Creating
buffers
****************

Network
buffers
被
created
通过
first
define
一
个
pool
of
them：

.. code-block::
   c

   NET_BUF_POOL_DEFINE(pool_name,
   buf_count,
   buf_size,
   user_data_size,
   NULL);

Pool
是
一
个
static
variable
所以
如果
它
需要
被
exported
到
另
一
个
module
需要
一
个
separate
的
pointer。

一
旦
pool
被
defined
buffers
可以
用
以下
方式
从
它
被
allocated：

.. code-block::
   c

   buf
   =
   net_buf_alloc(&pool_name,
   timeout);

没有
explicit
的
initialization
function
用于
pool
或
它
的
buffers
相反
这
被
implicitly
done
当
:c:func:`net_buf_alloc`
被
called
时。

如果
有
需要
在
buffer
中
reserve
space
用于
protocol
headers
