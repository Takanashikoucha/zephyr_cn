.. _can_api:

CAN
Controller
##############

.. contents::
   :local:
   :depth:
   2

Overview
********

Controller
Area
Network
是
一
个
两
线
serial
bus
由
Bosch
CAN
Specification、
Bosch
CAN
with
Flexible
Data-Rate
specification
和
ISO
11898-1:2003
标准
指定。
CAN
主要
以
其
在
automotive
domain
中
的
应用
著称。
然而，
它
也
用
于
home
和
industrial
automation
以及
其他
products。

.. warning::

   CAN
   controllers
   只
   能
   在
   bus
   处于
   idle
   （recessive）
   state
   至少
   11
   recessive
   bits
   时
   初始化。
   因此
   你
   必须
   确保
   CAN
   RX
   是
   high，
   至少
   短暂
   时间。
   这
   对
   loopback
   mode
   也
   是
   必需
   的。

ISO
11898-1:2003
中
定义
的
bit-timing
看起来
像
以下
这样：

.. image::
   timing.svg
   :width:
   40%
   :align:
   center
   :alt:
   CAN
   Timing

一
个
单一
bit
被
分成
四
个
segments。

* Sync_Seg:
  nodes
  在
  Sync_Seg
  的
  edge
  同步。
  它
  始终
  是
  一
  个
  time
  quantum
  长度。

* Prop_Seg:
  bus
  的
  信号
  propagation
  delay
  和
  transceiver
  和
  node
  的
  其他
  delays。

* Phase_Seg1
  和
  Phase_Seg2
  :
  定义
  采样
  点。
  Bit
  在
  Phase_Seg1
  的
  末尾
  被
  采样。
