.. _input:

输入
#####

输入子系统提供了一个 API，用于将输入事件从输入设备分发到应用。

输入事件
************

子系统围绕 :c:struct:`input_event` 结构构建。输入事件表示单个事件实体的变化，
例如单个按钮的状态，或单个轴的运动。

:c:struct:`input_event` 结构描述具体事件，并包含一个同步位，
指示设备到达稳定状态，例如当多轴设备的多个轴对应的事件已报告时。

输入设备
*************

输入设备可使用 :c:func:`input_report` 或任何相关函数直接报告输入事件；
例如按钮或其他开关输入实体会使用 :c:func:`input_report_key`。

复杂设备可能使用多个事件的组合，并在输出稳定后设置 ``sync`` 位。

``input_report*`` 函数接受 :c:struct:`device` 指针，用于指示哪个设备报告了事件，
订阅者可据此仅接收来自特定设备的事件。如果没有与事件关联的实际设备，
可将其设置为 ``NULL``，在这种情况下仅无设备过滤的订阅者会接收该事件。

应用 API
***************

应用可使用 :c:macro:`INPUT_CALLBACK_DEFINE` 宏注册回调。如果指定了设备节点，
回调仅对来自特定设备的事件调用；否则回调将接收系统中所有事件。
这是唯一支持的过滤类型，更复杂的过滤逻辑必须在回调本身中实现。

子系统可同步运行或使用事件队列，取决于 :kconfig:option:`CONFIG_INPUT_MODE` 选项。
如果使用输入线程，所有事件被添加到队列并在公共 ``input`` 线程中执行。
如果不使用线程，回调直接在输入驱动上下文中调用。

同步模式可用于简单应用以保持最小占用，或用于具有现有事件模型的复杂应用，
其中回调仅是将事件管道回更复杂的应用特定事件系统的包装器。

HID 代码映射
****************

输入设备的常见用例是用于生成 HID 报告。为此，
:c:func:`input_to_hid_code` 和 :c:func:`input_to_hid_modifier` 函数
可用于将输入代码映射到 HID 代码和修饰符。

通用驱动
***********************

- :dtcompatible:`adc-keys`：用于连接到电阻梯的按钮。
- :dtcompatible:`analog-axis`：用于连接到 ADC 输入的绝对位置设备（摇杆、滑块...）。
- :dtcompatible:`gpio-kbd-matrix`：用于 GPIO 连接的键盘矩阵。
- :dtcompatible:`gpio-keys`：用于直接连接到 GPIO 的开关，实现按钮去抖动。
- :dtcompatible:`gpio-qdec`：用于 GPIO 连接的正交编码器。
- :dtcompatible:`input-keymap`：将键盘矩阵的行/列/touch 事件映射到按键事件。
- :dtcompatible:`zephyr,input-longpress`：监听按键事件，为短按和长按发出事件。
- :dtcompatible:`zephyr,input-double-tap`：监听按键事件，为输入双击和（可选）单击发出事件。
- :dtcompatible:`zephyr,lvgl-button-input`
  :dtcompatible:`zephyr,lvgl-encoder-input`
  :dtcompatible:`zephyr,lvgl-keypad-input`
  :dtcompatible:`zephyr,lvgl-pointer-input`：监听输入事件并将其转换为
  各种类型的 LVGL 输入设备。

详细驱动文档
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
