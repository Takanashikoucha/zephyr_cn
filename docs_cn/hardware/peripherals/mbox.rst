.. _mbox_api:

Multi-Channel
Inter-Processor
Mailbox
（MBOX）
############################################

Overview
********

MBOX
device
是
一
个
可以
在
system
中
CPUs
和
clusters
之间
传递
signals
（以及
根据
peripheral
的
data）
的
peripheral。
每个
MBOX
instance
提供
一
个
或
多
个
channels
每个
targeting
一
个
其他
CPU
cluster
（多
个
channels
可以
target
同一
cluster）。


API
Reference
*************

.. doxygengroup::
   mbox_interface
