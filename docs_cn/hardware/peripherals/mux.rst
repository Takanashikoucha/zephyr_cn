.. _mux_api:

多路复用器（MUX）
#################

概述
********

MUX 子系统为硬件信号多路复用器提供统一 API。它让消费者驱动通过标准设备树 ``mux-controls`` 或 ``mux-states`` 句柄数组属性引用一个 MUX 控制器，从而将输入信号路由到输出，而无需依赖任何厂商特定的 HAL。

该子系统区分两种消费者侧模式：

* ``mux-controls`` —— 消费者引用一个控制器，并在运行时通过 :c:func:`mux_control_set` 提供*状态*（路由哪个输入，或写入哪个输出模式）。在路由于正常操作期间会变化时使用此模式。

* ``mux-states`` —— 消费者在设备树中引用一个控制器*以及*一个固定状态（说明符的尾部单元即为状态值）。运行时调用 :c:func:`mux_state_apply` 一行即可编程该固定状态。在路由于集成时已确定且初始化后不再变化时使用此模式。

设备树绑定
*******************

控制器侧
==============

每个 MUX 控制器绑定都包含 ``mux-controller.yaml``（位于 ``dts/bindings/mux/`` 中），并声明两个单元数量属性：

* ``#mux-control-cells`` —— ``mux-controls`` 说明符中的单元数量，纯粹用于在控制器内寻址期望的控制线。
* ``#mux-state-cells`` —— ``mux-states`` 说明符中的单元数量；等于 ``#mux-control-cells + 1``。尾部单元携带状态值，在编译时由框架提取到 ``mux_state::state``。

后端可以自由地按硬件命名寻址单元（``channel``、``output``、``index``、``device``/``input``、...），并按其硬件语义命名尾部状态单元（``state``、``input``、``connection``、``source``、...）。

消费者侧
=============

消费者包含 ``mux-consumer.yaml``，并可设置：

* ``mux-controls`` —— 句柄 + 寻址单元元组的列表。
* ``mux-control-names`` —— 可选名称，与 ``mux-controls`` 条目一一对应。
* ``mux-states`` —— 句柄 + 寻址单元 + 尾部状态单元元组的列表。
* ``mux-state-names`` —— 可选名称，与 ``mux-states`` 条目一一对应。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_MUX`

API 参考
*************

.. doxygengroup:: mux_interface
