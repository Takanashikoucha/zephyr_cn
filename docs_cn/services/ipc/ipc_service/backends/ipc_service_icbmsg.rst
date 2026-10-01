.. _ipc_service_backend_icbmsg:

ICMsg with dynamically allocated buffers backend
################################################

通过
此
backend
传输
的
Data
在
shared
memory 上
动态
分配
的
buffers
中
travel。
Allocation
thread
safe（且
可
从
任何
context
发生。
Backend
支持：

* Multiple
  endpoints。
* No-copy
  sending。
* Holding
  RX
  buffers。
* 从
  interrupt
  context
  sending。
* 两
  级
  endpoint
  priorities。
* Statistics
  和
  带
  utilization
  report 的
  optional
  shell
  command
* 最多
  32
  blocks。
* Data
  cache
  support。
* Low
  memory
  footprint（约
  2
  kB
  的
  code。

Overview
========

每
direction
保留
一个
shared
memory
region（且
每
region
分为
两部分。
一
部分
形成
fixed
size
buffers 的
pool（且
allocator
从
pool
中
相邻
buffers
构建
variable
size
buffer。
另
一
部分
用于
由
两个
message
queues（每
direction
一个）组成
的
control
path。
有
sender
写入
且
receiver
读取
的
producer
queue（以及
receiver
写入
且
sender
读取
的
consumer
queue。
Producer
queue
有
下一
message 的
location（pool
内）信息。
Consumer
queue
有
consumed
message 的
location（pool
内）信息。

Data
sending
process
如下：

* Sender
  从
  pool
  分配
  一个
  或
  多个
  blocks。
  若
  不够
  sequential
  blocks（thread
  context
  用
  parameter
  提供
  的
  timeout
  等待（其
  也
  包含
  K_FOREVER
  和
  K_NO_WAIT。
* 分配
  的
  blocks
  填入
  data。
  第一
  block
  开头
  有
  32
  bit
  message
  header（含
  length、
  endpoint
  ID
  和
  own
  block
  index。
  对
  zero-copy
  case（由
  caller
  做（否则
  自动
  copy。
  此
  期间
  其他
  threads
  不
  被
  任何
  方式
  blocked（只要
  有
  足够
  free
  blocks
  供
  它们。
  它们
  可
  分配、
  发送
  data
  并
  接收
  data。
* 带
  message
  开头
  的
  block
  index
  写入
  producer
  queue。
  Endpoint
  的
  priority
  信息
  追加
  到
  block
  index。
  :kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_MAX_ACTIVE_COUNT`
  定义
  queue
  中
  slots
  数量。
  Mailbox
  notification
  发送
  给
  receiver。
* Receiver
  读取
  producer
  queue。
  更高
  prioriy
  messages
  先
  处理。
  可
  按
  期望
  持有
  data。
  同样（其他
  threads
  不
  被
  blocked（只要
  有
  足够
  free
  blocks
  供
  它们。
* 不再
  需要
  data
  时（receiver
  将
  block
  index
  写入
  consumer
  queue。
* Sender
  通过
  读取
  consumer
  queue
  并
  释放
  buffers
  执行
  garbage
  collection。
  发送
  任何
  message
  后
  或
  无
  available
  buffers
  时
  执行
  garbage
  collection。

Configuration
=============

Backend
用
Kconfig
和
devicetree
配置。

有
以下
Kconfig
options：

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_NUM_EP` -
  注册
  endpoints
  的
  最大
  数量。

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_MAX_ACTIVE_COUNT` -
  queues
  中
  slots
  数量。

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_DEINIT` -
  支持
  deregistration
  和
  closing。

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_SHELL` -
  支持
  shell
  command。

配置
backend
时（做
以下：

* 若
  至少
  一个
  core
  在
  shared
  memory
  上
  用
  data
  cache（设置
  ``dcache-alignment``
  value。
  其
  须
  为
  通信
  双方
  的
  invalidation
  或
  write-back
  size
  的
  最大
  value。
  若
  通信
  双方
  均
  不
  在
  shared
  memory
  上
  用
  data
  cache（可
  跳过。
* 定义
  两个
  memory
  regions（并
  分配
  给
  实例
  的
  ``tx-region``
  和
  ``rx-region``。
  确保
  用于
  data
  exchange
  的
  memory
  regions
  唯一（不
  与
  任何
  其他
  region
  重叠）且
  两个
  domains（或
  CPUs）可
  访问。
* 用
  ``tx-blocks``
  和
  ``rx-blocks``
  为
  每
  region
  定义
  allocable
  blocks
  数量。
* 定义
  MBOX
  devices
  以
  发送
  告知
  另一
  domain（或
  CPU）已
  写入
  data 的
  signal。
  确保
  另一
  domain（或
  CPU）可
  接收
  signal。

.. caution::

    确保
    设置
    正确
    的
    ``dcache-alignment``
    value。
    最初（错误
    value
    可能
    不
    显示
    任何
    signs（这
    可能
    给
    一切
    工作
    的
    错误
    印象。
    Unstable
    behavior
    迟早
    会
    出现。

若
用
``dcache-alignment``（则
blocks
数量
的
configuration
应
仔细
选择
以
避免
memory
的
inefficient
usage。
这是因为
blocks
对齐
到
cache
alignment（且
若
blocks
数量
非
cache
alignment 的
multiple（最后
block
将
不
被
高效
使用。
这是因为
blocks
和
control
data
对齐
到
cache
alignment。
例如（若
``dcache-alignment``
为
32（且
一
direction
用
1024
bytes
的
shared
memory。
Control
data
占
64
bytes（且
剩
960
bytes
供
buffers。
用
16
blocks
将
导致
每
block
32
bytes（因
cache
alignment。
用
15
blocks
将
导致
每
block
64
bytes（因
cache
alignment）（memory
utilization
好
得多。


参见
以下
一
instance
的
configuration
示例：

.. code-block:: devicetree

   reserved-memory {
      tx: memory@20070000 {
         reg = <0x20070000 0x0800>;
      };

      rx: memory@20078000 {
         reg = <0x20078000 0x0800>;
      };
   };

   ipc {
      ipc0: ipc0 {
         compatible = "zephyr,ipc-icbmsg";
         dcache-alignment = <32>;
         tx-region = <&tx>;
         rx-region = <&rx>;
         tx-blocks = <16>;
         rx-blocks = <16>;
         mboxes = <&mbox 0>, <&mbox 1>;
         mbox-names = "tx", "rx";
         status = "okay";
      };
   };


须
为
通信
另一
侧（domain
或
CPU）提供
类似
configuration。
Swap
MBOX
channels、
memory
regions（``tx-region``
和
``rx-region``）及
block
count（``tx-blocks``
和
``rx-blocks``）。

Limitations
===========

* 期望
  通信
  双方
  相同
  endianness。
* 不
  支持
  检测
  unexpected
  remote
  reset。

Samples
=======

* :zephyr:code-sample:`ipc_multi_endpoint`

Detailed Protocol Specification
===============================

ICBMsg
protocol
用
shared
memory 上
动态
分配
的
blocks
传输
messages。

Shared Memory Organization
--------------------------

ICBMsg
用
两个
shared
memory
regions：``rx-region``
用于
message
receiving（``tx-region``
用于
message
transmission。
Regions
不
需
相邻、
按
任何
specific
order
放置
或
相同
size。
这些
regions
在
每
core
上
互换。

每
shared
memory
region
分为
以下
两部分：

* **Control
  area** - 保留
  给
  producer
  和
  consumer
  queues 的
  area。
* **Blocks
  area** - 包含
  携带
  messages
  content 的
  allocatable
  blocks 的
  area。
  此
  area
  分为
  对齐
  到
  cache
  boundaries 的
  even-sized
  blocks。

每
area
的
location
按
cache
boundary
requirements
计算（以
允许
optimal
region
usage。
用
以下
algorithm
计算：

Inputs：

* ``region_begin``、``region_end`` -
  Region
  的
  boundaries。
* ``local_blocks`` -
  此
  region
  中
  blocks
  数量。
* ``remote_blocks`` -
  相反
  region
  中
  blocks
  数量。
* ``alignment`` -
  Memory
  cache
  alignment。

Algorithm：

#. 将
   region
   boundaries
   对齐
   到
   cache：

   * ``region_begin_aligned = ROUND_UP(region_begin, alignment)``
   * ``region_end_aligned = ROUND_DOWN(region_end, alignment)``
   * ``region_size_aligned = region_end_aligned - region_begin_aligned``

#. 计算
   control
   area
   所需
   最小
   size：

   * 每
     queue
     有
     :kconfig:option:`IPC_SERVICE_BACKEND_ICBMSG_MAX_ACTIVE_COUNT`
     bytes
     和
     8
     byte
     queue
     header。
   * 通常
     control
     data
     每
     direction
     占
     少于
     64
     bytes。

#. 计算
   block
   area
   的
   available
   size。注意
   因
   block
   alignment
   实际
   size
   可能
   更小：

   ``blocks_area_available_size = region_size_aligned - control_area``

#. 计算
   单个
   block
   size：

   ``block_size = ROUND_DOWN(blocks_area_available_size / local_blocks, alignment)``

#. 计算
   实际
   block
   area
   size：

   ``blocks_area_size = block_size * local_blocks``

#. 计算
   block
   area
   start
   address：

   ``blocks_area_begin = region_end_aligned - blocks_area_size``

Result：

* ``region_begin_aligned`` -
  ICMsg
  area
  的
  start。
* ``blocks_area_begin`` -
  ICMsg
  area
  的
  End
  和
  block
  area
  的
  start。
* ``block_size`` -
  单个
  block
  size。
* ``region_end_aligned`` -
  blocks
  area
  的
  End。

.. image:: icbmsg_memory.svg
   :align: center

|

Message Transfer
----------------

ICBMsg
用
以下
两种
message
types：

* **Control
  message** - 如
  binding
  或
  unbinding 的
  messages。
* **Data
  message** - 携带
  实际
  user
  data 的
  message。

它们
服务
不同
purposes（但
lifetime
和
flow
相同。
以下
steps
描述
它：

#. Sender
   想
   发送
   含
   ``K``
   bytes 的
   message。
#. Sender
   从其
   ``tx-region``
   blocks
   area
   保留
   可
   容纳
   至少
   ``K
   +
   4``
   bytes 的
   blocks。
   额外
   ``+
   4``
   bytes
   保留
   给
   header。
   Blocks
   须
   continuous（一个
   接
   一个）。
   Sender
   负责
   block
   allocation
   management。
   若
   blocks
   不
   available（thread
   context
   可能
   block（且
   interrupt
   context
   返回
   error。
#. Sender
   填入
   header。
#. Sender
   用
   其
   data
   填入
   blocks
   的
   剩余
   部分。
   Unused
   space
   忽略。
#. Sender
   将
   message
   写入
   producer
   queue（并
   发送
   mailbox
   signal。
#. Receiver
   在
   mailbox
   interrupt
   context
   中
   执行
   mailbox
   callback（并
   读取
   producer
   queue。
#. Receiver
   读取
   block
   index（并
   在其
   ``rx-region``
   内
   定位
   message。
#. Receiver
   读取
   endpoint
   和
   message
   length（并
   处理
   message。
#. Receiver
   通过
   将
   其
   block
   index
   写入
   consumer
   queue
   消费
   message。
   不
   发送
   mailbox
   signal。
#. Sender
   每次
   sending
   后
   或
   sending
   失败
   时
   检查
   consume
   queue。
   Messages
   从
   consumer
   queue
   读取（并
   释放
   到
   pool。

.. image:: icbmsg_message.svg
   :align: center

|

Binding Instances
-----------------

Backend
instance
open
时
发送
bound
message（其
含
64
bit
magic
number。
Mailbox
callback
启用（且
instance
等待
bound
message。
接收
bound
message
后（instance
bind
到
remote
instance（且
endpoints
可
注册。

Binding Endpoint
----------------

Endpoint
binding
message
含
endpoint
name 的
SHA
和
endpoint
ID（其
为
endpoint
data 的
local
array
中
的
index。

有
两种
可能
scenarios：

* Remote
  instance
  在
  endpoint
  注册
  前
  发送
  了
  其
  binding
  message。
* Endpoint
  在
  接收
  remote
  instance
  的
  binding
  message
  前
  注册。

接收
binding
message
时（SHA
与
endpoint
data
array
中
存储
的
SHA
比较。
若
找到
match（意味
endpoint
已
被
local
instance
注册。
Endpoint
ID
存储
在
endpoint
data
中（且
bound
callback
调用。
若
未
找到
match（则
找到
empty
slot（且
endpoint
ID
和
SHA
存储
在
available
slot。

Endpoint
注册
时（name
的
SHA
计算（并
与
endpoint
data
array
中
存储
的
SHA
比较。
若
找到
match（意味
该
endpoint 的
remote
binding
message
已
接收。
此
情况下（binding
message
发送
给
remote
instance（且
bound
callback
调用。
若
未
找到
match（则
找到
empty
slot（且
endpoint
ID
和
SHA
存储
在
available
slot。
Binding
message
发送
给
remote
instance（但
endpoints
尚
未
bound。

稍后（remote
endpoint
ID
用于
data
message
以
识别
endpoint。

Unbinding Endpoint
------------------

Endpoint
unregister
时
发送
unbinding
control
message。
Endpoint
从
endpoint
data
array
移除。
接收
unbinding
message
时（endpoint
slot
标记
为
empty（且
unbinding
callback
调用。
