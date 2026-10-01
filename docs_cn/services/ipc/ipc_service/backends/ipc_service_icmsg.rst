.. _ipc_service_backend_icmsg:

ICMsg backend
#############

Inter
core
messaging
backend（ICMsg）是
更
heavy 的
RPMsg
static
vrings
backend 的
lighter
alternative。其
提供
minimal
feature
set
且
small
memory
footprint。ICMsg
backend
构建
在
:ref:`spsc_pbuf` 之上。

Overview
========

ICMsg
backend
用
shared
memory
和
MBOX
devices
交换
data。Shared
memory
用于
存储
data（MBOX
devices
用于
signal
data
已
写入。

Backend
支持
在
单个
instance
上
注册
单个
endpoint。若
application
需
超过
一个
communication
channel（须
定义
多个
instances（每
instance
有
其
自己
dedicated
endpoint。

Configuration
=============

Backend
通过
Kconfig
和
devicetree
配置。
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
  instance
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
* 定义
  用于
  发送
  告知
  另一
  domain（或
  CPU）data
  已
  写入
  的
  signal 的
  MBOX
  devices。
  确保
  另一
  domain（或
  CPU）能
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
            compatible = "zephyr,ipc-icmsg";
            dcache-alignment = <32>;
            tx-region = <&tx>;
            rx-region = <&rx>;
            mboxes = <&mbox 0>, <&mbox 1>;
            mbox-names = "tx", "rx";
            status = "okay";
         };
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
configuration（但
须
swap
MBOX
channels
和
memory
regions（``tx-region``
和
``rx-region``）。

Bonding
=======

Endpoint
注册
时（通过
IPC
instance
连接
的
每
domain（或
CPU）上
发生
以下：

1. Domain（或
   CPU）将
   magic
   number
   写入
   其
   shared
   memory 的
   ``tx-region``。
#. 然后
   向
   另一
   domain
   或
   CPU
   发送
   signal（告知
   data
   已
   写入。向
   另一
   domain
   或
   CPU
   发送
   signal
   用
   timeout
   重复。
#. 接收
   来自
   另一
   domain
   或
   CPU
   的
   signal
   时（从
   ``rx-region``
   读取
   magic
   number。若
   正确（bonding
   process
   完成（且
   backend
   通过
   调用
   :c:member:`ipc_service_cb.bound`
   callback
   告知
   application。

Samples
=======

 - :zephyr:code-sample:`ipc-icmsg`

Detailed Protocol Specification
===============================

ICMsg
用
两个
shared
memory
regions
和
两个
MBOX
channels。
Region
和
channel
pair
用于
单向
传输
messages。
另
一
pair
对称（且
传输
相反
方向
的
messages。因此（以下
specification
聚焦
于
一
pair。
另
一
pair
相同。

ICMsg
每
instance
仅
提供
一个
endpoint。

Shared Memory Region Organization
---------------------------------

若
启用
data
caching（提供
给
ICMsg 的
shared
memory
region
须
按
cache
requirement
对齐。
若
不
启用
cache（所需
alignment
为
4
bytes。

Shared
memory
region
完全
用于
单个
FIFO。
其
包含
read
和
write
indexes（后接
data
buffer。详细
structure
包含
在
以下
table
中：

.. list-table::
   :header-rows: 1

   * - Field name
     - Size (bytes)
     - Byte order
     - Description
   * - ``rd_idx``
     - 4
     - little‑endian
     - Index of the first incoming byte in the ``data`` field.
   * - ``padding``
     - depends on cache alignment
     - n/a
     - Padding added to align ``wr_idx`` to the cache alignment.
   * - ``wr_idx``
     - 4
     - little‑endian
     - Index of the byte after the last incoming byte in the ``data`` field.
   * - ``data``
     - everything to the end of the region
     - n/a
     - Circular buffer containing actual bytes to transfer.

此
为
带
circular
buffer 的
usual
FIFO：

* Indexes（``rd_idx``
  和
  ``wr_idx``）在
  到达
  ``data``
  buffer
  末尾
  时
  wrap
  around。
* 若
  ``rd_idx
  ==
  wr_idx``（FIFO
  为空。
* FIFO
  的
  capacity
  比
  ``data``
  buffer
  length
  少
  一
  byte。

Packets
-------

Packets
通过
上述
section
描述
的
FIFO
发送。
若
packet
发生在
FIFO
buffer
末尾（其
可
wrap
around。

以下
为
packet
structure：

.. list-table::
   :header-rows: 1

   * - Field name
     - Size (bytes)
     - Byte order
     - Description
   * - ``len``
     - 2
     - big‑endian
     - Length of the ``data`` field.
   * - ``reserved``
     - 2
     - n/a
     - Reserved for the future use.
       It must be 0 for the current protocol version.
   * - ``data``
     - ``len``
     - n/a
     - Packet data.
   * - ``padding``
     - 0‑3
     - n/a
     - Padding is added to align the total packet size to 4 bytes.

Packet
send
procedure
如下：

#. 检查
   packet
   是否
   装入
   buffer。
#. 从
   ``wr_idx``
   开始
   将
   packet
   写入
   ``data``
   FIFO
   buffer。
   需要
   时
   wrap。
#. 写入
   ``wr_idx``
   的
   新
   value。
#. 通过
   MBOX
   channel
   notify
   receiver。

Initialization
--------------

Initialization
sequence
如下：

#. 将
   ``wr_idx``
   和
   ``rd_idx``
   设为
   zero。
#. 向
   FIFO
   push
   单个
   含
   magic
   data 的
   packet：``45
   6d
   31
   6c
   31
   4b
   30
   72
   6e
   33
   6c
   69
   34``。
   尚
   不
   用
   MBOX。
#. 初始化
   MBOX。
#. 用
   某
   interval（如
   1
   ms）重复
   通过
   MBOX
   channel
   notify。
#. 等待
   含
   magic
   data 的
   传入
   packet。
   其
   将
   通过
   另
   一
   pair（shared
   memory
   region
   和
   MBOX）到达。
#. 停止
   重复
   MBOX
   notification。

此后（ICMsg
bound（且
ready
传输
packets。
