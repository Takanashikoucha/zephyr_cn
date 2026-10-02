.. _input:

输入
#####

输入子系统提供将输入设备的输入事件分发给应用的 API。

输入事件
************

该子系统围绕 :c:struct:`input_event` 结构构建。一个输入
事件表示单个事件实体的变化，例如单个按钮的状态
或单个轴上的移动。

:c:struct:`input_event` 结构描述具体的事件，
并包含一个同步位，用于指示设备已达到稳定
状态，例如当多轴设备多个轴对应的事件
均已报告时。

输入设备
*************

输入设备可以直接使用 :c:func:`input_report`
或任何相关函数报告输入事件；例如按钮或其他开/关输入实体
会使用 :c:func:`input_report_key`。

复杂设备可能使用多个事件的组合，
并在输出稳定后设置 ``sync``
位。

``input_report*`` 函数接收一个 :c:struct:`device` 指针，
用于指示哪个设备报告了该事件，订阅者
可以用它来仅接收来自特定设备的事件。如果事件没有
关联的实际设备，可以将其设置为 ``NULL``，在这种情况下，只有
没有设备过滤器的订阅者会收到该事件。

应用 API
***************

应用可以使用
:c:macro:`INPUT_CALLBACK_DEFINE` 宏注册回调。如果指定了
设备节点，回调仅对来自特定设备的事件调用，否则
回调将接收系统中的所有事件。这是唯一支持的
过滤类型，任何更复杂的过滤逻辑都必须在
回调本身中实现。

子系统可以同步运行或使用事件队列，
具体取决于 :kconfig:option:`CONFIG_INPUT_MODE` 选项。如果使用输入线程，
所有事件都会加入队列，并在一个通用的 ``input`` 线程中执行。
如果不使用线程，回调直接在输入
驱动程序上下文中调用。

同步模式可用于简单应用以保持最小
占用，也可用于具有现有事件模型的复杂应用，其中
回调只是将事件传递回更复杂的应用
特定事件系统的包装器。

HID 代码映射
****************

输入设备的常见用例是将其用于生成 HID 报告。为此，
可以使用 :c:func:`input_to_hid_code` 和
:c:func:`input_to_hid_modifier` 函数将输入代码映射为 HID
代码和修饰键。

通用驱动程序
***********************

- :dtcompatible:`adc-keys`：用于连接到电阻梯的按钮。
- :dtcompatible:`analog-axis`：用于连接到
  ADC 输入的绝对位置设备（摇杆、滑块...）。
- :dtcompatible:`gpio-kbd-matrix`：用于 GPIO 连接的键盘矩阵。
- :dtcompatible:`gpio-keys`：用于直接连接到 GPIO 的
  开关，实现按键去抖。
- :dtcompatible:`gpio-qdec`：用于 GPIO 连接的正交编码器。
- :dtcompatible:`input-keymap`：将键盘
  矩阵的行/列/触摸事件映射为键事件。
- :dtcompatible:`zephyr,input-longpress`：监听键事件，发出
  短按和长按事件。
- :dtcompatible:`zephyr,input-double-tap`：监听键事件，发出
  输入双击事件，以及（可选地）单击事件
- :dtcompatible:`zephyr,lvgl-button-input`
  :dtcompatible:`zephyr,lvgl-encoder-input`
  :dtcompatible:`zephyr,lvgl-keypad-input`
  :dtcompatible:`zephyr,lvgl-pointer-input`：监听输入事件
  并将其转换为各种类型的 LVGL 输入设备。

详细驱动程序文档
*****************************

.. toctree::
   :maxdepth: 1

   gpio-kbd.rst


API 参考
*************

.. doxygengroup:: input_interface

输入事件定义
***********************

.. doxygengroup:: input_events

模拟轴 API 参考
*************************

.. doxygengroup:: input_analog_axis

触摸屏 API 参考
*************************

.. doxygengroup:: touch_events
