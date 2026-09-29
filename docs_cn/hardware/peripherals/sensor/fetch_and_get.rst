.. _sensor-fetch-and-get:

Fetch
and
Get
#############

Stable
和
长期
存在
的
用于
read
sensor
data
和
处理
triggers
的
APIs
是：

* :c:func:`sensor_sample_fetch`
* :c:func:`sensor_sample_fetch_chan`
* :c:func:`sensor_channel_get`
* :c:func:`sensor_trigger_set`

这些
functions
协同
工作。
Fetch
APIs
block
calling
context
它
必须
是
一
个
thread
直到
请求
的
:c:enum:`sensor_channel`
（或
所有
channels）
被
获得
并
存储
到
driver
instance
的
private
data
中。

最近
fetch
的
channel
data
然后
可以
通过
对
每个
channel
type
调用
:c:func:`sensor_channel_get`
作为
:c:struct:`sensor_value`
获取。

.. warning::
   应该
   注意
   从
   多
   个
   contexts
   调用
   fetch
   和
   get
   而
   没有
   locking
   mechanism
   是
   undefined
   的
   大多数
   sensor
   drivers
   不
   尝试
   在
   这些
   calls
   期间
   或
   之间
   内部
   提供
   对
   device
   的
   exclusive
   access。

Polling
*******

使用
fetch
和
get
sensor
可以
从
software
threads
以
polling
方式
read。


.. literalinclude::
   ../../../../samples/sensor/magn_polling/src/main.c
   :language:
   c

Triggers
********

Stable
API
中
的
Triggers
需要
用
device
