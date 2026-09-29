.. _rtc_api:

Real-Time
Clock
（RTC）
#####################

Overview
********

.. list-table::
   **Glossary**
   :widths:
   30
   80
   :header-rows:
   1

   * - Word
     - Definition
   * - Real-time
     clock
     - 用
     broken-down
     time
     跟踪
     time
     的
     low
     power
     device
   * - Real-time
     counter
     - 可以
     用
     来
     跟踪
     time
     的
     low
     power
     counter
   * - RTC
     - real-time
     clock
     的
     acronym

RTC
是
一
个
用
broken-down
time
跟踪
time
的
low
power
device。
它
不
应该
与
有时
共享
同一
name、
acronym、
或
两者
的
low-power
counters
混淆。

RTCs
通常
被
优化
为
低
energy
consumption
并
通常
在
system
处于
low
power
state
时
保持
运行。

RTCs
通常
包含
一
个
或
多
个
alarms
它们
可以
被
配置
为
在
给定
的
time
触发。
这些
alarms
通常
被
用
来
从
low
power
state
唤醒
system。

Devicetree
bindings
*******************

RTC
bindings
必须
包括
``rtc-device.yaml``
binding
它
包括
``base.yaml``
binding
和
required
的
``alarms-count``
property。

.. code-block:: yaml
