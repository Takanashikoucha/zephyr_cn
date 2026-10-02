.. _sensing:

传感子系统
########################

.. contents::
    :local:
    :depth: 2

概述
********

传感子系统是操作系统用户空间服务层中的高级传感器框架。它是一个专注于传感器融合、客户端仲裁、采样、定时、调度以及基于传感器的电源管理的框架。

传感子系统的关键概念包括物理传感器和虚拟传感器对象，以及基于传感器对象关系的调度框架。物理传感器不依赖于任何其他传感器对象作为输入，并且直接与现有的 Zephyr 传感器设备驱动程序交互。虚拟传感器依赖其他传感器对象（物理或虚拟）作为报告输入。

传感子系统依赖 Zephyr 传感器设备 API（现有版本或未来更新版本），以利用 Zephyr 庞大的传感器设备驱动程序库（100 多个）。

使用传感子系统是可选的。只需要访问简单传感器设备的应用可以直接使用 Zephyr :ref:`sensor` API。

由于传感子系统与设备驱动程序层或内核空间分离，并且可以使用虚拟传感器概念在用户空间中支持各种定制和传感器算法。现有的传感器设备驱动程序可以专注于底层设备端工作，尽可能保持简单，只需提供设备硬件抽象和操作等。这对系统稳定性非常好。

传感子系统与任何传感器暴露/传输协议解耦，目标是支持具有不同传感器暴露/传输协议的各种上层框架和应用，例如 `CHRE <https://github.com/zephyrproject-rtos/chre>`_、HID 传感器应用、根据产品不同需求采用 MQTT 传感器应用，甚至利用其多客户端支持设计同时支持具有不同上层传感器协议的多个应用。

传感子系统有助于构建统一的 Zephyr 传感架构，以支持跨宿主操作系统以及 IoT 传感器解决方案。

下图说明了传感子系统如何与上层框架集成。

.. image:: images/sensing_solution.png
   :align: center
   :alt: 统一的 Zephyr 传感架构。

可配置性
***************

* 可复用、可配置的独立子系统。
* 基于 Zephyr 现有低级 Sensor API（复用 100 多个现有传感器设备驱动程序）。
* 为应用提供 Zephyr 高级传感子系统 API。
* 独立的可选 CHRE Sensor PAL 实现模块以支持 CHRE。
* 与任何宿主链路协议解耦，处理不同协议（MQTT、HID 或私有协议，均可配置）是 Zephyr 应用的角色。

主要特性
*************

范围
  专注于传感器融合、多客户端、仲裁、数据采样、定时管理和调度的框架。

传感器抽象
  * **物理传感器**：与 Zephyr 传感器设备驱动程序交互，专注于数据收集。
  * **虚拟传感器**：依赖其他传感器（**物理**或**虚拟**），专注于数据融合。

数据驱动模型
  * **轮询模式**：周期性采样率。
  * **中断模式**：数据就绪、阈值中断等。

调度
  所有传感器对象采样和处理的单线程主循环。

用于批处理的缓冲区模式
  ..

通过设备树配置
  ..

下面的图显示了 API 的位置和范围：

.. image:: images/sensing_api_org.png
   :align: center
   :alt: 传感子系统 API 组织。

``Sensing Subsystem API`` 面向应用。
``Sensing Sensor API`` 用于开发 ``sensors``。

主要流程
***********

* 传感器配置流程

.. image:: images/sensor_config_flow.png
   :align: center
   :alt: 传感器配置流程（应用将报告间隔设置为铰链角度传感器的示例）。

* 传感器数据流程

.. image:: images/sensor_data_flow.png
   :align: center
   :alt: 传感器数据流程（应用通过数据事件回调接收铰链角度数据的示例）。

传感器类型和实例
*************************

``Sensing Subsystem`` 支持同一传感器类型的多个实例，应用有两种方法识别并打开唯一的传感器实例：

* 枚举所有传感器实例

  :c:func:`sensing_get_sensors` 返回当前板级配置支持的所有传感器实例信息，以 :c:struct:`sensing_sensor_info` 指针数组形式返回。

  然后应用可以使用 :c:func:`sensing_open_sensor` 打开特定传感器实例，以便后续访问、配置和接收传感器数据等。

  该方法适用于支持某些需要动态枚举底层平台传感器实例的上层框架，如 ``CHRE``、``HID``。

* 直接通过设备树节点打开传感器实例

  应用可以使用 :c:func:`sensing_open_sensor_by_dt` 通过传感器设备树节点标识符直接打开传感器实例。

  例如：

.. code-block:: c

   sensing_open_sensor_by_dt(DEVICE_DT_GET(DT_NODELABEL(base_accel)), cb_list, handle);
   sensing_open_sensor_by_dt(DEVICE_DT_GET(DT_CHOSEN(zephyr_sensing_base_accel)), cb_list, handle);

该方法对于只想访问特定传感器的简单应用既有用又易于使用。

``Sensor type`` 遵循
`HID 标准传感器类型定义 <https://usb.org/sites/default/files/hutrr39b_0.pdf>`_。

参见 :zephyr_file:`include/zephyr/sensing/sensing_sensor_types.h`

传感器实例句柄
***********************

客户端使用 :c:type:`sensing_sensor_handle_t` 类型句柄处理已打开的传感器实例，并且对该传感器实例的所有后续操作都需要使用此句柄，例如设置配置、读取传感器采样数据等。

对于一个传感器实例，可能有两类客户端：``Application clients`` 和 ``Sensor clients``。

``Application clients`` 可以使用 :c:func:`sensing_open_sensor` 打开传感器实例并获取其句柄。

对于 ``Sensor clients``，没有用于打开 reporter 的 open API，因为客户端与 reporter 之间的关系在传感器注册阶段通过设备树建立。

``Sensing Subsystem`` 会自动为客户端传感器打开并创建到其 reporter 传感器的 ``handlers``。
``Sensor clients`` 可以通过 :c:func:`sensing_sensor_get_reporters` 获取其 reporter 的句柄。

.. image:: images/sensor_top.png
   :align: center
   :alt: 传感器报告拓扑。

.. note::
   传感子系统内部的传感器之间，它们之间的报告关系全部由传感子系统根据设备树定义自动生成，客户端传感器与 reporter 传感器之间的句柄会自动创建。应用需要调用 :c:func:`sensing_open_sensor` 显式打开传感器实例。

传感器采样值
*******************

* 数据结构

  每个传感器采样值定义为通用 ``header`` + ``readings[]`` 数据结构，例如 :c:struct:`sensing_sensor_value_3d_q31`、:c:struct:`sensing_sensor_value_q31` 和 :c:struct:`sensing_sensor_value_uint32`。

  ``header`` 定义为 :c:func:`sensing_sensor_value_header`。

* 时间戳

  传感子系统的时间戳单位为``微秒``。

  ``header`` 定义一个 **base_timestamp**，
  **readings[]** 数组中的每个元素定义 **timestamp_delta**。

  **timestamp_delta** 相对于前一个 **readings**（或 **base_timestamp**）。

  例如：

  * ``readings[0]`` 的时间戳是 ``header.base_timestamp`` + ``readings[0].timestamp_delta``。

  * ``readings[1]`` 的时间戳是 ``readings[0] 的时间戳`` + ``readings[1].timestamp_delta``。

  由于时间戳单位为微秒，
  最大 **timestamp_delta**（``uint32_t``）为 ``4295`` 秒。

  如果传感器有批处理数据，两个连续读数的差值超过 ``4295`` 秒，
  传感子系统运行时会将它们拆分到多个 readings 结构实例中，
  并发送多个事件。

  该概念参考自 `CHRE Sensor API <https://github.com/zephyrproject-rtos/
  chre/blob/zephyr/chre_api/include/chre_api/chre/sensor_types.h>`_。

* 数据格式

  ``Sensing Subsystem`` 使用按传感器类型定义的数据格式结构，
  并支持 :zephyr_file:`include/zephyr/dsp/types.h` 中定义的 ``Q Format``
  以支持 ``zdsp`` 库。

  例如 :c:struct:`sensing_sensor_value_3d_q31` 可用于 3D IMU 传感器，如
  :c:macro:`SENSING_SENSOR_TYPE_MOTION_ACCELEROMETER_3D`、
  :c:macro:`SENSING_SENSOR_TYPE_MOTION_UNCALIB_ACCELEROMETER_3D`
  和 :c:macro:`SENSING_SENSOR_TYPE_MOTION_GYROMETER_3D`。

  :c:struct:`sensing_sensor_value_uint32` 可用于
  :c:macro:`SENSING_SENSOR_TYPE_LIGHT_AMBIENTLIGHT` 传感器，

  而 :c:struct:`sensing_sensor_value_q31` 可用于
  :c:macro:`SENSING_SENSOR_TYPE_MOTION_HINGE_ANGLE` 传感器。

  参见 :zephyr_file:`include/zephyr/sensing/sensing_datatypes.h`

设备树配置
*************************

传感子系统使用设备树配置所有传感器实例及其属性、
报告关系。

参见示例 :zephyr_file:`samples/subsys/sensing/simple/boards/native_sim.overlay`

API 参考
*************

.. doxygengroup:: sensing_api
