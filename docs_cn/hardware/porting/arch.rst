.. _architecture_porting_guide:

Architecture
Porting
Guide
##########################

Architecture
port
被
需要
以
使
Zephyr
能
在
当前
不
被
支持
的
:abbr:`ISA
(instruction
set
architecture)`
或
:abbr:`ABI
(Application
Binary
Interface)`
上
运行。

下面
是
Zephyr
支持
的
ISAs
和
ABIs
的
示例：

* x86_32
  ISA
  带
  System
  V
  ABI
* ARMv7
  M
  ISA
  带
  Thumb2
  instruction
  set
  和
  ARM
  Embedded
  ABI
  （aeabi）
* ARCv2
  ISA

关于
Kconfig
configuration
的
信息
参考
:ref:`setting_configuration_values`。
Architectures
使用
与
boards
类似
的
Kconfig
configuration
scheme。

一
个
architecture
port
可以
被
分成
多
个
parts；
大多数
是
required
的
一些
是
optional
的：

* **Early
  boot
  sequence**：
  每个
  architecture
  在
  CPU
  从
  reset
  出来
  时
  必须
  执行
  不同
  的
  steps
  （required）。

* **Interrupt
  和
  exception
  handling**：
  每个
  architecture
  用
  特定
  的
  manner
  处理
  asynchronous
  和
  unrequested
  events
  （required）。

* **Thread
  context
  switching**：
  Zephyr
  的
  context
  switch
  依赖
  于
  ABI
  每个
  ISA
  有
  不同
  的
  registers
  set
  需要
  save
  （required）。

* **Thread
  creation
  和
  termination**：
  Thread
  的
  initial
  stack
  frame
  是
  ABI
  和
  architecture
  特定
  的
  thread
  abortion
  可能
  也
  是
  （required）。

* **Device
  drivers**：
  大多数
  情况
  下
  system
  clock
  timer
  和
  interrupt
  controller
  与
  architecture
  绑定
  （一些
  required
  一些
  optional）。

* **Utility
  libraries**：
  一些
  common
  kernel
  APIs
  依赖
  architecture
  特定
  的
  implementation
  用于
  performance
  reasons
  （required）。
