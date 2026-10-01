.. _sensor:

传感器
#######

传感器驱动 API 提供了统一读取、配置和设置事件处理的功能，适用于以有意义的单位进行真实世界测量的设备。

传感器的范围从必须用固定缩放进行轮询的简单温度测量设备，到从大量传感器接收读数并自身产生新的推断传感器数据（如步数、存在检测、方向等）的复杂设备。

支持如此广泛范围的设备是一项艰巨的任务，传感器 API 试图为它们提供统一的接口。


.. _sensor-using:

使用传感器
*************

从应用中使用传感器时，有一些 API 和术语有助于理解。Zephyr 中的传感器由 :ref:`sensor-channel`、:ref:`sensor-attribute` 和 :ref:`sensor-trigger` 组成。属性和触发器可以是设备特定的，也可以是通道特定的。

.. note::
   目前使用传感器 API 从传感器获取样本有两种方式：稳定且长期存在的 API :ref:`sensor-fetch-and-get`，或较新但正在快速趋于稳定的 API :ref:`sensor-read-and-decode`。预计在不远的将来 :ref:`sensor-fetch-and-get` 将被弃用，转而使用 :ref:`sensor-read-and-decode`。触发器在 :ref:`sensor-fetch-and-get` 和 :ref:`sensor-read-and-decode` 中的处理方式完全不同，差异在各相应章节中均有说明。

.. toctree::
   :maxdepth: 1

   attributes.rst
   channels.rst
   triggers.rst
   power_management.rst
   device_tree.rst
   fetch_and_get.rst
   read_and_decode.rst


.. _sensor-implementing:

实现传感器驱动
***************************

.. note::
   实现传感器 API 的驱动侧需要理解传感器 API 是如何被使用的。请先阅读 :ref:`sensor-using`！

实现属性
=======================

* 应当（SHOULD）以阻塞方式实现属性设置。
* 应当（SHOULD）在设备支持时提供获取和设置通道缩放的能力。
* 应当（SHOULD）在设备支持时提供获取和设置通道采样率的能力。

实现 Fetch 与 Get
==========================

* 应当（SHOULD）将 :c:type:`sensor_sample_fetch_t` 实现为阻塞调用，将指定通道（或所有传感器通道）存储为驱动实例数据。
* 应当（SHOULD）将 :c:type:`sensor_channel_get_t` 实现为无副作用，不操作驱动状态而返回已存储的传感器读数。
* 应当（SHOULD）将 :c:type:`sensor_trigger_set_t` 实现为存储 :c:struct:`sensor_trigger` 的地址而不是复制其内容。这样 :c:macro:`CONTAINER_OF` 即可用于触发器回调的上下文。

实现 Read 与 Decode
============================

* 必须（MUST）将 :c:type:`sensor_submit_t` 实现为非阻塞调用。
* 应当（SHOULD）如果可能，使用 :ref:`rtio` 实现 :c:type:`sensor_submit_t` 进行非阻塞总线传输。
* 可以（MAY）如果总线不支持 :ref:`rtio`，使用工作队列实现 :c:type:`sensor_submit_t`。
* 应当（SHOULD）实现 :c:type:`sensor_submit_t` 时检查 :c:struct:`rtio_sqe` 是否为 :c:enum:`RTIO_SQE_RX` 类型（读取请求）。
* 应当（SHOULD）实现 :c:type:`sensor_submit_t` 时检查所有请求的通道是否受支持，否则返回错误。
* 应当（SHOULD）实现 :c:type:`sensor_submit_t` 时检查提供的缓冲区是否足以容纳请求的通道。
* 应当（SHOULD）将 :c:type:`sensor_submit_t` 实现为直接读取到提供的缓冲区，避免任何形式的复制，少数例外。
* 必须（MUST）使用纯无状态函数实现 :c:struct:`sensor_decoder_api`。将原始传感器读数转换为定点 SI 单位值所需的所有状态必须位于提供的缓冲区中。
* 必须（MUST）实现 :c:type:`sensor_get_decoder_t`，返回该设备类型的 :c:struct:`sensor_decoder_api`。

.. _sensor-api-reference:

API 参考
***************

.. doxygengroup:: sensor_interface
.. doxygengroup:: sensor_emulator_backend
