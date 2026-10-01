.. _cache_config:

缓存控制配置
###########################

这是 Zephyr 缓存接口和与缓存控制器相关的 Kconfig 选项的高级指南。参见 :ref:`cache_api` 获取 API 参考材料。

Zephyr 有不同的 Kconfig 选项来控制缓存控制器如何实现和被控制。

* :kconfig:option:`CONFIG_CPU_HAS_DCACHE` / :kconfig:option:`CONFIG_CPU_HAS_ICACHE`：
  这些隐藏选项应该在 SoC / 平台级别选择，
  当 CPU 实际支持数据缓存或指令缓存时。
  缓存控制器可以在核心中，也可以是提供了驱动程序的外部缓存控制器。

  这些选项的目标是记录一个可用的硬件特性，
  无论我们是否计划在 Zephyr 中支持和使用该缓存控制，都应设置。

* :kconfig:option:`CONFIG_DCACHE` / :kconfig:option:`CONFIG_ICACHE`：
  当 Zephyr 中存在可用的数据缓存或指令缓存支持时必须选择这些选项。
  注意，如果这些选项被禁用，根据硬件默认设置，缓存可能仍然处于启用状态。

  所有与缓存控制相关的代码路径必须根据这些符号条件启用。
  当符号被设置时，缓存被认为已启用并使用中。

  这些符号不说明暴露给用户的实际 API 接口。
  例如，使用数据缓存的平台可以启用 :kconfig:option:`CONFIG_DCACHE` 符号，
  并在某些平台特定代码中使用某些 HAL 导出函数来启用和管理数据缓存。

* :kconfig:option:`CONFIG_CACHE_MANAGEMENT`：
  当缓存操作通过标准 API（参见 :ref:`cache_api`）暴露给用户时必须选择此选项。

  当此选项被启用时，我们假设所有缓存函数
  都实现在架构代码或外部缓存控制器驱动程序中。

* :kconfig:option:`CONFIG_MEM_ATTR`：
  此选项允许用户（使用 :ref:`memory region attributes<mem_mgmt_api>`）
  指定内存中将在内核初始化后禁用缓存的固定区域。

* :kconfig:option:`CONFIG_NOCACHE_MEMORY`：
  此选项允许用户使用 ``__nocache`` 将个别全局变量指定为非缓存。
  这将指示链接器将任何被标记的变量放入内存中的特殊 ``nocache`` 区域，
  而 MPU 驱动程序会将该区域配置为非缓存。

* :kconfig:option:`CONFIG_ARCH_CACHE`/:kconfig:option:`CONFIG_EXTERNAL_CACHE`：
  用于 :kconfig:option:`CACHE_TYPE` 的互斥选项，
  用于定义缓存操作是在架构级别实现，
  还是使用带有所提供驱动程序的外部缓存控制器。

  * :kconfig:option:`CONFIG_ARCH_CACHE`：缓存 API 由架构代码实现。

  * :kconfig:option:`CONFIG_EXTERNAL_CACHE`：缓存 API 由支持外部缓存控制器的驱动程序实现。
    在这种情况下，驱动程序必须像往常一样位于 :file:`drivers/cache/` 目录中。

.. _cache_api:

缓存 API
*********

.. doxygengroup:: cache_interface
