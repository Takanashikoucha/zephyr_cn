.. _design_guidelines:

API 设计指南
#####################

Zephyr 的开发和演进是一项群体努力，为简化和增强维护工作，
在开发新功能或接口时应遵循以下通用策略。

所有公共 API 必须使用 Doxygen 进行文档化。详见 :ref:`doxygen_style`。

使用回调
***************

许多 API 涉及将回调作为参数或作为配置结构的成员传递。
在指定回调的签名时，应遵循以下策略：

* 第一个参数应是指向与回调最密切相关的对象的指针。
  对于设备驱动，这通常是 ``const struct device *dev``。
  对于库函数，它可能是指向另一个在提供回调时被引用的对象的指针。

* 接下来的参数应是回调调用特有的附加信息，
  例如通道标识符、新的状态值，
  以及/或消息指针后跟消息长度。

* 最后一个参数应是 ``void *user_data`` 指针，
  携带允许共享回调函数定位处理该回调所需附加材料的上下文。

在将 ``user_data`` 作为最后一个参数这一惯例上，
存在一种可能的例外：当回调本身通过一个将被嵌入到另一个结构中的结构提供时。
此类情况的一个示例是 :c:struct:`gpio_callback`，
它通常定义在特定于同时定义回调函数的代码的数据结构中。
在这些情况下，回调可以通过 :c:macro:`CONTAINER_OF` 间接访问更多上下文。

示例
========

* :c:type:`k_timer_expiry_t` 在系统定时器报警触发时的要求
  由以下函数满足::

    void handle_timeout(struct k_timer *timer)
    { ... }

  这里的假设与 :c:struct:`gpio_callback` 相同，
  即定时器嵌入在可通过 :c:macro:`CONTAINER_OF` 到达的结构中，
  该结构可以为回调提供额外的上下文。

* :c:type:`counter_alarm_callback_t` 在计数器设备报警触发时的要求
  由以下函数满足::

    void handle_alarm(const struct device *dev,
                      uint8_t chan_id,
		      uint32_t ticks,
		      void *user_data)
    { ... }

  这提供了更完整、更有用的信息，
  包括哪个计数器通道超时以及超时发生时计数器的值，
  还有用户上下文——它可能是也可能不是用于注册回调的
  :c:struct:`counter_alarm_cfg`，具体取决于用户需求。

条件数据和 API
*************************

API 和库可能提供在 RAM 或代码大小方面代价高昂但可选的功能，
即某些应用可以在没有这些功能的情况下实现。
此类功能的示例包括
:kconfig:option:`捕获时间戳 <CONFIG_CAN_RX_TIMESTAMP>` 或
:kconfig:option:`提供替代接口 <CONFIG_SPI_ASYNC>`。
开发者必须与社区协商，确定是否应通过 Kconfig 选项来控制启用该功能。

当某功能被确定为可选时，应遵循以下实践。

* 任何仅在功能启用时访问的数据，
  应通过 ``#ifdef CONFIG_MYFEATURE``
  在结构或联合体声明中条件包含。
  这减少了不需要该功能的应用的内存使用。
* 仅在选项启用时可用的函数声明应无条件提供。
  在描述中添加注释，说明该函数仅在指定功能启用时可用，
  并按名称引用所需的 Kconfig 符号。
  当函数被使用但未启用时，该函数的定义应被排除出编译，
  因此对不受支持 API 的引用将导致链接时错误。
* 当特定于某功能的代码被隔离在一个没有其他内容的源文件中时，
  该文件应在 ``CMakeLists.txt`` 中条件包含::

    zephyr_sources_ifdef(CONFIG_MYFEATURE foo_funcs.c)
* 当特定于某功能的代码是某个有其他内容的源文件的一部分时，
  该功能特定代码应使用 ``#ifdef CONFIG_MYFEATURE`` 条件处理。

如何确保条件代码对 Doxygen 可见并被包含在公共 API 文档中，
详见 :ref:`doxygen_conditional_code`。

返回码
************

API 的实现，例如用于访问外设的 API，
可能只实现了最小运行所需函数的子集。
需要在"不受支持的 API"与"未实现或可选的 API"之间做出区分：

- 受支持但未实现的 API 应返回 ``-ENOSYS``。

- 硬件不支持的可选 API 应被实现，
  此情况下的返回码应为 ``-ENOTSUP``。

- 当 API 已实现，但调用中请求的选项组合无法被实现满足时，
  该调用应返回 ``-ENOTSUP``。
  （例如，在仅支持边沿触发中断的硬件上请求电平触发 GPIO 中断）