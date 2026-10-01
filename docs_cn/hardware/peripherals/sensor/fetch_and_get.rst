.. _sensor-fetch-and-get:

获取与读取
#############

用于读取传感器数据和处理触发的稳定且长期存在的 API 是：

* :c:func:`sensor_sample_fetch`
* :c:func:`sensor_sample_fetch_chan`
* :c:func:`sensor_channel_get`
* :c:func:`sensor_trigger_set`

这些函数协同工作。fetch API 会阻塞调用上下文，该上下文必须是线程，直到所请求的
:c:enum:`sensor_channel`（或所有通道）已被获取并存储到驱动实例的私有数据中。

最近一次获取的通道数据随后可以通过为每种通道类型调用 :c:func:`sensor_channel_get`
作为 :c:struct:`sensor_value` 获取。

.. warning::
   应注意，在没有锁机制的情况下从多个上下文调用 fetch 和 get 是未定义行为，大多数
   传感器驱动不会尝试在内部为设备提供这些调用期间或调用之间的独占访问。

轮询
*******

使用 fetch 和 get，软件线程可以以轮询方式读取传感器。


.. literalinclude:: ../../../../samples/sensor/magn_polling/src/main.c
   :language: c

触发器
********

稳定 API 中的触发器需要使用设备特定的 Kconfig 来启用。设备特定的 Kconfig 通常允许
选择触发器运行的上下文。应用随后需要使用与 :c:type:`sensor_trigger_handler_t` 匹配的
函数签名，通过 :c:func:`sensor_trigger_set` 为要监听的具体触发器（事件）注册回调。

.. note::
   触发器不能从用户模式线程设置，且回调不在用户模式上下文中运行。

每个驱动通常提供两个选项来决定在哪里运行触发器处理函数。要么触发器处理函数使用系统
工作队列线程（:ref:`workqueues_v2`）运行，要么使用专用线程。BMI160 驱动就是一个
很好的示例，它提供了选择触发器模式的 Kconfig 选项。参见
:kconfig:option:`CONFIG_BMI160_TRIGGER_NONE`、
:kconfig:option:`CONFIG_BMI160_TRIGGER_GLOBAL_THREAD`（工作队列）、
:kconfig:option:`CONFIG_BMI160_TRIGGER_OWN_THREAD`（专用线程）。

使用驱动专用线程相比系统工作队列，有若干显著的特点。

* 驱动专用线程拥有专用栈（RAM），仅用于该单个触发器处理函数。
* 驱动专用线程*确实*会获得自己的优先级（通常），使你可以将触发器处理相对于其他线程进行优先级排序。
* 当驱动需要时间处理触发器时，驱动专用线程不会出现队首阻塞。

.. note::
   在所有情况下，从实际中断到你的回调函数运行，很可能存在可变的延迟。在工作队列
   （GLOBAL_THREAD）情况下，工作队列本身可能就是可变延迟的来源！

.. literalinclude:: tap_count.c
   :language: c
