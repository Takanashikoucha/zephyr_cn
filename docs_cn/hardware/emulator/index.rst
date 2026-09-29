.. _emulators:

Zephyr
的
device
emulators/simulators
####################################

Overview
========

Zephyr
在
其
代码库
中
包含
一
组
device
emulators/simulators。
我们
用
这
指
与
embedded
SW
一起
构建
的
SW
组件
它们
向
系统
的
其余
部分
呈现
自己
为
给定
class
的
devices。

这些
device
emulators/simulators
可以
为
任何
有
足够
RAM
和
flash
的
target
构建，
即使
一些
可能
有
额外
功能
只
在
某些
targets
中
可用。

.. note::

   | Zephyr
     也
     包含
     并
     使用
     许多
     其他
     类型
     的
     simulators/emulators，
     包括
     CPU
     和
     platform
     simulators、
     radio
     simulators、
     以及
     多
     个
     允许
     在
     开发
     主机
     上
     运行
     embedded
     代码
     的
     build
     targets。
   | 一些
     Zephyr
     communication
     controllers/drivers
     也
     包含
     loopback
     modes
     或
     loopback
     devices。
   | 本
     页
     不
     覆盖
     这些
     中
     的
     任何
     一
     个。

.. note::
   特定
   于
   某些
   platform
   的
   drivers，
   如
   例如
   :ref:`native_sim
   specific
   drivers
   <native_sim_peripherals>`
   通过
   连接
   到
   host
   APIs
   emulate
   一
   个
   peripheral
   class
   的
   那些
   不
   被
   本
   页
   覆盖。


Available
Emulators
===================

**ADC
emulator**
  * 一
    个
    fake
    driver
    假装
    是
    实际
    ADC，
    可以
    用
    于
    测试
    ADC
    devices
    的
    更
    高层
    API
  * Main
    Kconfig
    option:
    :kconfig:option:`CONFIG_ADC_EMUL`
  * DT
    binding:
    :dtcompatible:`zephyr,adc-emul`

**DMA
emulator**
