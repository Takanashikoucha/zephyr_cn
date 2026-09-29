.. _devicetree-scope-purpose:

范围与目的
*****************

*设备树*（devicetree）主要是描述硬件的
层次化数据结构。
`设备树规范`_ 定义了它的
源码和
二进制表示。

.. _设备树规范: https://www.devicetree.org/

Zephyr 使用设备树来描述：

- 其 :ref:`开发板` 上可用的硬件
- 该硬件的初始配置

因此，设备树既是 Zephyr 的硬件描述语言，
也是配置语言。
设备树与 Zephyr 另一种主要配置语言 Kconfig 之间
的一些比较见 :ref:`dt_vs_kconfig`。

有两种类型的设备树输入文件：*设备树源*
和*设备树绑定*。
源包含
设备树本身。
绑定描述
其内容，
包括数据类型。
:ref:`构建系统
<build_overview>` 使用设备树源和绑定
生成一个
生成的 C
头文件。
生成头文件的内容
由 ``devicetree.h``
API 抽象，
你可以用它
从设备树获取信息。

以下是该流程的简化视图：

.. figure:: zephyr_dt_build_flow.png
   :figclass: align-center

   设备树构建流程

所有 Zephyr 和应用源代码文件
都可以包含并使用
``devicetree.h``。
这包括 :ref:`设备驱动 <device_model_api>`、
:ref:`应用 <application>`、:ref:`测试 <testing>`、内核等。

API 本身基于
C 宏。
宏名都以 ``DT_`` 开头。
一般来说，
如果你在 Zephyr 源文件中
看到以 ``DT_`` 开头的宏，
它很可能
是 ``devicetree.h`` 宏。
生成的 C 头文件也包含
以 ``DT_`` 开头的宏；
你可能在编译器
错误信息中
看到它们。
你总是
能区分
生成的
宏和
非生成的
宏：
生成的
宏
含有一些小写字母，
而 ``devicetree.h`` 宏
名
全是大写字母。
