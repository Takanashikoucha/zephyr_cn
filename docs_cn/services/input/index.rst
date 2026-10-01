.. _input:

Input
#####

Input
subsystem
提供
将
input
events
从
input
devices
分发
到
application 的
API。

Input Events
************

Subsystem
围绕
:c:struct:`input_event`
structure
构建。Input
event
代表
individual
event
entity 的
变更（如
单个
button 的
state（或
单个
axis 的
movement。

:c:struct:`input_event`
structure
描述
specific
event（并
包含
指示
device
到达
stable
state 的
synchronization
bit（如
multi-axis
device
的
多个
axes 对应
的
events
已
报告
时。

Input Devices
*************

Input
device
可
用
:c:func:`input_report`
或
任何
相关
function
直接
报告
input
events；如
buttons
或
其他
on-off
input
entities
用
:c:func:`input_report_key`。

Complex
devices
可
用
多个
events 的
combination（并在
output
stable
后
设置
``sync``
bit。

``input_report*``
functions
接受
:c:struct:`device`
pointer（其
用于
指示
哪个
device
报告
了
event（且
可
被
subscribers
用于
仅
接收
来自
特定
device 的
events。若
event
无
关联
的
actual
device（可
设为
``NULL``（此
情况下
仅
无
device
filter 的
subscribers
接收
event。

Application API
***************

Application
可
用
:c:macro:`INPUT_CALLBACK_DEFINE`
macro
注册
callback。若
指定
device
node（callback
仅
对
来自
特定
device 的
events
调用（否则
callback
接收
system
中
所有
events。此
为
支持的
唯一
filtering
类型（任何
更
complex 的
filtering
logic
须
在
callback
本身
实现。

Subsystem
可
同步
运行
或
用
event
queue（取决于
:kconfig:option:`CONFIG_INPUT_MODE`
option。若
用
input
thread（所有
events
加入
queue（并在
common
``input``
thread
中
执行。若
不用
thread（callbacks
直接在
input
driver
context
中
调用。

Synchronous
mode
可
用于
simple
application
以
保持
minimal
footprint（或
用于
有
既有
event
model 的
complex
application（其中
callback
仅为
将
event
pipe
回
更
complex
application
specific
event
system 的
wrapper。

HID code mapping
****************

Input
devices 的
common
use
case
为
用
它们
生成
HID
reports。为此（
:c:func:`input_to_hid_code` 和
:c:func:`input_to_hid_modifier`
functions
可
用于
将
input
codes
map
到
HID
codes
和
modifiers。

General Purpose Drivers
***********************

- :dtcompatible:`adc-keys`: 用于
  连接
  到
  resistor
  ladder 的
  buttons。
- :dtcompatible:`analog-axis`: 用于
  连接
  到
  ADC
  input 的
  absolute
  position
  devices（thumbsticks、
  sliders...）。
- :dtcompatible:`gpio-kbd-matrix`: 用于
  GPIO-connected
  keyboard
  matrices。
- :dtcompatible:`gpio-keys`: 用于
  直接
  连接
  到
  GPIO 的
  switches（
  实现
  button
  debouncing。
- :dtcompatible:`gpio-qdec`: 用于
  GPIO-connected
  quadrature
  encoders。
- :dtcompatible:`input-keymap`: 将
  keyboard
  matrix 的
  row/col/touch
  events
  map
  到
  key
  events。
- :dtcompatible:`zephyr,input-longpress`: 监听
  key
  events（发出
  short
  和
  long
  press 的
  events。
- :dtcompatible:`zephyr,input-double-tap`: 监听
  key
  events（发出
  input
  double
  taps 的
  events（可选
  single
  taps
- :dtcompatible:`zephyr,lvgl-button-input`
  :dtcompatible:`zephyr,lvgl-encoder-input`
  :dtcompatible:`zephyr,lvgl-keypad-input`
  :dtcompatible:`zephyr,lvgl-pointer-input`: 监听
  input
  events（并将
  它们
  转换
  为
  各种
  类型
  的
  LVGL
  input
  devices。

Detailed Driver Documentation
*****************************

.. toctree::
   :maxdepth: 1

   gpio-kbd.rst


API Reference
*************

.. doxygengroup:: input_interface

Input Event Definitions
***********************

.. doxygengroup:: input_events

Analog Axis API Reference
*************************

.. doxygengroup:: input_analog_axis

Touchscreen API Reference
*************************

.. doxygengroup:: touch_events
