.. _doxygen_style:

Doxygen 风格指南
########################

Zephyr 项目使用 `Doxygen`_ 从源代码注释生成 API 文档。本指南定义了
Zephyr 公共 API 文档化的一致约定。

所有 `Doxygen commands`_ 均可使用，即使它们没有明确出现在本文档中。

.. _Doxygen: https://www.doxygen.nl/
.. _Doxygen commands: https://www.doxygen.nl/manual/commands.html

要在本地构建并预览 Zephyr 的 Doxygen 文档，参见 :ref:`zephyr_doc`。

通用规则
*************

所有 :term:`公共头文件及其公共 API 符号 <public API>`（函数、结构体、
枚举、联合体、typedef、宏和全局变量）：

- 必须完整文档化（参见 :ref:`doxygen_internals` 了解例外）
- 必须至少属于一个 Doxygen 组（参见 :ref:`doxygen_groups`）

文档化公共 API 时必须使用以下语法：

- 使用 ``/**`` 开始块注释，使用 ``*/`` 结束块注释。
- 使用 ``/**<`` 写与符号同一行的尾随注释。
- Doxygen 命令使用 ``@``（而不是 ``\``）（例如用 ``@param`` 而不是 ``\param``）。
- ``@brief`` 命令是可选的。如果未使用，第一句（以句号结尾）将被
  视为简要描述。

仅用于内部使用的构造必须从公共文档中隐藏，如
:ref:`doxygen_internals` 中所述。

要文档化的内容
================

对于任何接受、返回或存储值的 API 元素（函数参数、返回值、
struct/union 成员、enum 值、typedef 和宏），其文档在适用时必须描述
以下内容：

语义
  该元素代表什么，调用者/用户应如何解释它。不要重述标识符或 C 类型。

  示例：

  - 避免：``@param timeout Timeout value in ms.``
  - 推荐：``@param timeout Maximum time to wait before returning, in milliseconds.``

有效值
  接受哪些值，以及它们如何被解释。指定以下一个或多个：

  - 范围：最小/最大值（例如，类型是 ``uint8_t`` 但只有 0–100 有效）。
  - 离散集：当只允许子集时，列出允许的值。
  - 枚举：值是否必须是给定枚举的有效成员（以及是允许所有枚举器
    还是只允许一个子集）。
  - 标志/位掩码：哪些位有效，以及是否允许组合。
  - 可空性：指针值是否允许 ``NULL``，以及它意味着什么。

单位
  当值表示一个数量时，指定单位和参考（例如，毫秒还是 tick、赫兹、
  字节）。适用时使用 SI 单位符号，并在数字与单位符号之间写一个空格
  （例如，``10 ms``）。

表示
  任何非显而易见的编码或缩放（例如，定点缩放、Q 格式、分离的整数和
  小数字段、字节序要求）。

所有权和生命周期
  对于指针/缓冲区，说明由谁分配/释放，以及内存必须保持有效多长时间。
  在相关时注明所需的大小/对齐。

写作风格
============

简要描述应使用祈使语气（动词短语）而不是第三人称叙述。
这使 API 摘要保持一致且易于快速浏览。

- 避免："Transmits data through a pipe.", "This function gets the device state."
- 推荐："Transmit data through a pipe.", "Get the device state.", "Initialize the subsystem."

参数和成员描述可以是句子片段，但应保持描述性并避免重复
参数/成员名称。


.. _doxygen_groups:

组
******

组将相关符号组织成层次结构，帮助用户浏览 API。

- 使用 ``@defgroup`` 定义每个组一次。

  - 所提供的标题应为该组的简短描述性名称。由于组本质上将各种
    接口/API 归并在一起，标题中*不要*使用 "API" 或 "Interface"
    （或这些词的任何变体），否则会显得冗余。
  - 组的简要描述不应复述其标题。

- 组名使用 `snake_case <https://en.wikipedia.org/wiki/Snake_case>`_。
- 使用 ``@ingroup`` 指定组所属的父组。

示例：

.. code-block:: c
   :emphasize-lines: 2,3

   /**
    * @defgroup mqtt_socket MQTT Client library
    * @ingroup networking
    * @since 1.14
    * @version 0.8.0
    * @{
    */

    /* documented contents of the MQTT header file */

    /** @} */

.. note::

   一个组可以属于多个父组，因此可以有多条 ``@ingroup`` 命令。
   例如，设备驱动仿真器通常同时出现在 "Emulator Interfaces" 和
   "Device drivers" 组中。参见 :c:group:`i2c_emul_interface` 的示例。

.. important::

   没有父组的组会成为 :ref:`api_overview` 的顶级条目，而顶级条目
   类别是刻意保持精简的。新组务必用 ``@ingroup`` 指定父组。

   顶级条目在 :zephyr_file:`doc/_doxygen/toplevel_groups.txt` 中
   以白名单形式列出，并由 :zephyr_file:`scripts/ci/doxygen_toplevel_groups.py`
   强制执行。新增一个条目需要文档维护者批准。

.. _doxygen_api_versioning:

API 版本管理
=============

在组定义（``@defgroup``）上使用 ``@since`` 和 ``@version`` 来记录
API 的历史和成熟度：

- ``@since`` 指示引入该 API 的 Zephyr 版本（例如 ``@since 3.7``）
- ``@version`` 指示当前 API 版本，遵循语义化版本管理

版本号反映 :ref:`api_overview` 中定义的 API 成熟度。

示例：

.. code-block:: c
   :caption: 一个在 Zephyr 1.14 引入、当前版本为 0.8.0（不稳定）的 API 示例。
   :emphasize-lines: 4,5

   /**
    * @defgroup mqtt_socket MQTT Client library
    * @ingroup networking
    * @since 1.14
    * @version 0.8.0
    * @{
    */

    /* documented contents of the MQTT header file */

    /** @} */

文件
*****

每个公共头文件顶部都必须有一个 ``@file`` 块，出现在 SPDX 许可证
和版权声明之后。

``@file`` 块还必须属于一个 Doxygen 组，通常就是同一头文件中定义
的那个组。这样，按文件浏览的用户就能轻松导航到相应的组。

.. code-block:: c
   :emphasize-lines: 2,4

   /**
    * @file
    * @brief Public API for the GPIO driver.
    * @ingroup gpio_interface
    */

类型定义
****************

用简要描述文档化 ``struct``、``enum``、``union`` 和 ``typedef`` 定义。

每个成员（结构体字段、枚举值等）也要文档化。当只提供简要描述且
能写在一行内时，推荐使用 ``/**<`` 尾随注释风格。

.. code-block:: c
   :caption: 完整文档化的 enum、struct 和 typedef 示例。

   /** @brief Parity modes */
   enum uart_config_parity {
        UART_CFG_PARITY_NONE,   /**< No parity */
        UART_CFG_PARITY_ODD,    /**< Odd parity */
        UART_CFG_PARITY_EVEN,   /**< Even parity */
        UART_CFG_PARITY_MARK,   /**< Mark parity */
        UART_CFG_PARITY_SPACE,  /**< Space parity */
   };

   /**
    * GPIO pin configuration.
    *
    * Specifies direction, pull resistor, and interrupt settings.
    */
   struct gpio_config {
       uint32_t flags;    /**< Pin configuration flags. */
       gpio_pin_t pin;    /**< Pin number within the port. */
   };

   /**
    * @brief Identifies a set of pins associated with a port.
    *
    * The pin with index n is present in the set if and only if the bit
    * identified by (1U << n) is set.
    */
   typedef uint32_t gpio_port_pins_t;

函数
*********

参数
==========

- 按声明顺序用 ``@param`` 文档化参数
- 函数写入的指针使用 ``@param[out]``。
- 函数既读取又写入的指针使用 ``@param[in,out]``。
- 对于 const 指针和标量（隐含只读）可以省略方向说明符。

返回值
=============

- 一般描述（例如布尔值或计算值）使用 ``@return <description>``。
- 具体的、离散的返回值（通常是错误码）使用 ``@retval <value> <description>``，
  从成功情况开始（如适用）。``<value>`` 必须作为第一个词给出，
  后跟描述（例如 ``@retval -EINVAL Invalid arguments``，而不是
  ``@retval -EINVAL if invalid arguments``）。

  .. note::

     同一个离散值可能因多个原因被返回，因此允许在多条
     ``@retval`` 语句中使用同一个值。

示例：

.. code-block:: c
   :caption: 完整文档化的函数示例。

   /**
    * @brief Write data to the TX queue from a provided buffer
    *
    * @param dev Pointer to the device structure for the driver instance.
    * @param buf Pointer to a buffer containing the data to transmit.
    * @param size Number of bytes to write. This value has to be equal or smaller
    *        than the size of the channel's TX memory block configuration.
    *
    * @retval 0 on success.
    * @retval -EIO The interface is not in READY or RUNNING state.
    * @retval -EBUSY Returned without waiting.
    * @retval -EAGAIN Waiting period timed out.
    * @retval -ENOMEM No memory in TX slab queue.
    * @retval -EINVAL Size parameter larger than TX queue memory block.
    */
   int i2s_buf_write(const struct device *dev, void *buf, size_t size);

   /**
    * @brief Add an application callback.
    *
    * @param port Pointer to the device structure for the driver instance.
    * @param callback A valid application's callback structure pointer.
    *
    * @return 0 on success, negative errno value on failure.
    * @retval -ENOSYS Driver does not implement the operation.
    */
   int gpio_add_callback(const struct device *port, struct gpio_callback *callback);

   /**
    * @brief Helper function for converting struct sensor_value to float.
    *
    * @param val A pointer to a sensor_value struct.
    * @return The converted value.
    */
   static inline float sensor_value_to_float(const struct sensor_value *val)
   {
       return (float)val->val1 + (float)val->val2 / 1000000;
   }


宏
******

对于函数式宏，像文档化函数一样文档化其参数。

.. code-block:: c
   :caption: 完整文档化的函数式宏示例。

   /**
    * @brief Get a node's (only) register block size
    *
    * Equivalent to DT_REG_SIZE_BY_IDX(node_id, 0).
    *
    * @param node_id node identifier
    * @return node's only register block's size
    */
   #define DT_REG_SIZE(node_id) DT_REG_SIZE_BY_IDX(node_id, 0)

.. _doxygen_sphinx_xrefs:

引用主文档
**********************************

API 文档可以使用下面描述的命令引用主文档（基于 Sphinx）中的内容。
在生成的 API 文档页面中，这些引用会渲染为指向主文档对应页面的
超链接。

``@kconfig{<option>}``
  通过完整名称（包括 ``CONFIG_`` 前缀）引用一个 Kconfig 选项。
  这是 :rst:role:`kconfig:option` 角色的 Doxygen 对应物。

  示例：``@kconfig{CONFIG_GPIO}``

``@kconfig_regex{<regex>}``
  通过正则表达式引用所有匹配的 Kconfig 选项，渲染为带预填模式的
  Kconfig 搜索页面的链接。这是 :rst:role:`kconfig:option-regex` 角色的
  Doxygen 对应物。由于逗号在 Doxygen 命令中有特殊含义，必须用反斜杠
  转义。

  示例：``@kconfig_regex{CONFIG_SECURE_STORAGE_ITS_.*_CUSTOM}``

``@dtcompatible{<compatible>}``
  通过 compatible 字符串引用一个 Devicetree 绑定。这是
  :rst:role:`dtcompatible` 角色的 Doxygen 对应物。由于逗号在 Doxygen
  命令中有特殊含义，必须用反斜杠转义。

  示例：``@dtcompatible{zephyr\,input-longpress}``

``@rstref{<target>}`` 或 ``@rstref{<text> <target>}``
  通过引用标签（或文档名）引用任意文档页面或章节，类似于 Sphinx 的
  :rst:role:`ref` 角色。未提供自定义文本时，使用所引用页面或章节的
  标题作为链接文本。

  示例：``@rstref{zephyr_licensing}`` 或 ``@rstref{the licensing page <zephyr_licensing>}``

构建文档时会检查这些引用：引用不存在的 Kconfig 选项、绑定或标签
会导致文档构建警告。

.. note::

   单独构建 Doxygen 文档（即不包含其余文档）时，这些命令会展开为
   纯文本。更多细节参见 :ref:`zephyr_doc`。

.. _doxygen_rfc_refs:

引用 IETF RFC
*********************

``@rfc{<number>}`` 或 ``@rfc{<number>,<anchor>}``
  通过编号引用一个 IETF RFC，可选地指向其中的某个锚点。这是
  :rst:role:`rfc` 角色的 Doxygen 对应物，渲染为指向 IETF Datatracker
  上该 RFC 的超链接。

  锚点按原样传递，因此可以指向 Datatracker 为该 RFC 定义的任何
  内容，例如 ``section-3.1``、``appendix-B.1.2``、``figure-2`` 或
  ``table-1``。哪些锚点存在取决于该 RFC：图和表只有在从 XML 源
  渲染的 RFC 中才有锚点。

  逗号后面不要加空格：Doxygen 会把空格保留为参数的一部分，最终
  出现在 URL 片段中。渲染出的链接文本看起来仍然正常，因此锚点损坏
  只有在点击链接时才能被发现。

  示例：``@rfc{7519}``、``@rfc{8613,section-3.1}`` 或 ``@rfc{8613,appendix-B.1.2}``

.. _doxygen_internals:

隐藏内部细节
***********************

使用 ``@cond INTERNAL_HIDDEN`` / ``@endcond`` 从生成的文档中隐藏
内部细节。

这些内部符号仍然可以选地文档化，为内部使用者提供有用的参考。

.. code-block:: c
   :emphasize-lines: 7,11

   /** Timer structure.
    *
    * Opaque type for a timer object. All the fields in this structure are internal and should not
    * be accessed outside of kernel code.
    */
   struct k_timer {
       /** @cond INTERNAL_HIDDEN */

       /* ... internal members ... */

       /** @endcond */
   };

.. _doxygen_driver_backend:

驱动后端 API
******************

驱动子系统向应用暴露一个公共 API，同时向驱动实现者暴露一个
"后端" API。

后端 API 虽然不打算让应用直接使用，但它仍然是子系统与驱动实现者
之间的公共契约，因此必须妥善文档化。它通常包括驱动操作结构体、
定义每个操作签名的 typedef，以及某些情况下对驱动实现有用的
辅助类型或宏。

后端 API Doxygen 组
=========================

使用 ``@def_driverbackendgroup`` 创建一个子组，它是主 API 组的子组，
包含所有与后端 API 关联的符号。该命令接受两个参数：后端 API 的
人类可读名称（通常与父组相同）和父组标识符。

.. code-block:: c

   /**
    * @def_driverbackendgroup{Haptics,haptics_interface}
    * @{
    */

    /* callback typedefs, driver ops struct, helpers ... */

    /** @} */

驱动操作 typedef
==========================

为每个驱动操作定义一个 ``typedef``。详细描述可以引用对应的
公共 API 函数，因为其签名通常相似。

.. code-block:: c

   /**
    * @brief Set the haptic device to stop output.
    * See haptics_stop_output() for argument description.
    */
   typedef int (*haptics_stop_output_t)(const struct device *dev);

驱动操作结构体
===========================

用 ``@driver_ops{Name}`` 注释该结构体（其中 *Name* 与传给
``@def_driverbackendgroup`` 的名称一致）。对每个成员，使用
``@driver_ops_mandatory`` 或 ``@driver_ops_optional`` 指示驱动是否
必须实现它，并使用 ``@copybrief`` 从公共 API 函数继承简要描述：

.. code-block:: c

   /**
    * @driver_ops{Haptics}
    */
   __subsystem struct haptics_driver_api {
       /**
        * @driver_ops_mandatory @copybrief haptics_start_output
        */
       haptics_start_output_t start_output;
       /**
        * @driver_ops_mandatory @copybrief haptics_stop_output
        */
       haptics_stop_output_t stop_output;
       /**
        * @driver_ops_optional @copybrief haptics_register_error_callback
        */
       haptics_register_error_callback_t register_error_callback;
   };

.. _doxygen_conditional_code:

条件编译代码
****************

要确保条件编译的代码出现在文档中，使用以下任一方法：

1. 将控制该代码的 Kconfig 宏（``CONFIG_...``）添加到
   :zephyr_file:`doc/zephyr.doxyfile.in` 中的 ``PREDEFINED`` 列表。
   这会使该代码在文档生成时对 Doxygen 可见。

#. 或者，可以依赖 ``__DOXYGEN__`` 宏被设置来使条件代码对 Doxygen
   可见，因为该宏由 Doxygen 自动定义。

.. code-block:: c
   :emphasize-lines: 3,9

   struct coap_packet {
       uint8_t *data;  /**< User allocated buffer. */
   #if defined(CONFIG_COAP_KEEP_USER_DATA) || defined(__DOXYGEN__)
       /**
        * Application-specific user data.
        * @kconfig_dep{CONFIG_COAP_KEEP_USER_DATA}
        */
       void *user_data;
   #endif
   };

.. _doxygen_kconfig_dep:

Kconfig 依赖
===================

``@kconfig_dep`` 命令可用于文档化 API 符号对用户可用所需的
Kconfig 选项。该命令可以搭配一个、两个或三个 Kconfig 选项使用。

例如，在某个 API 符号的 Doxygen 文档中添加
``@kconfig_dep{CONFIG_PM,CONFIG_SMP}``，生成的文档就会包含一条
注释："Available only when the following Kconfig options are enabled:
``CONFIG_PM``, ``CONFIG_SMP``."。

你可以在 :c:struct:`coap_packet` 的文档中看到 ``@kconfig_dep``
用法的示例。
