.. _logging_api:

日志
#######

.. contents::
    :local:
    :depth: 2

日志 API 提供了一个通用接口，用于处理开发人员发出的消息。消息先经过前端（frontend），然后由处于激活状态的后端（
backend）处理。前端负责日志消息的即时过滤和排队，因此必须足够快。后端可以稍后运行并花费更多时间。它们格式化日志消息并将其发送到目标，例如 UART、RTT 或 BLE。必要时可以使用自定义前端和自定义后端。

日志功能摘要：

- 延迟日志通过将耗时操作转移到已知上下文中执行，而不是在调用时立即处理并发送日志消息，从而减少了记录一条消息所需的时间。
- 支持多个后端（最多 9 个后端）。
- 支持自定义前端，可与标准后端协同工作。
- 模块级别的编译期过滤。
- 每个后端独立的运行时过滤。
- 模块实例级别的附加运行时过滤。
- 使用用户提供的函数进行时间戳。时间戳可以是 32 位或 64 位。
- 用于转储（dump）数据的专用 API。
- 用于处理临时字符串（transient strings）的专用 API。
- 支持恐慌（panic）模式——在恐慌模式下，日志切换为阻塞式、同步处理。
- 支持 printk——printk 消息可以被重定向到日志系统。
- 设计上适用于多域/多处理器系统。
- 支持记录浮点数和 ``long long`` 值。
- 内置对用作参数的临时字符串的拷贝。
- 支持多域日志。
- 速率受限（rate-limited）日志宏，防止消息频繁生成时日志刷屏。

日志 API 在编译期和运行时都高度可配置。使用 Kconfig 选项（参见 :ref:`logging_kconfig`）
，可以逐步将日志从编译中移除，在不需要日志时减小镜像大小和执行时间。编译期间，可以按模块和严重级别过滤日志。

日志也可以在编译时保留但通过专用 API 在运行时过滤。运行时过滤对每个后端和每个日志消息来源相互独立。日志消息的来源可以是某个模块，也可以是某个模块的特定实例。

系统中有四种严重级别：error（错误）、warning（警告）、info（信息）和 debug（调试）。对于每种严重级别，
日志 API（:zephyr_file:`include/zephyr/logging/log.h`）都有一套专用宏。还有用于记录数据的宏。

对于每种严重级别，可使用以下宏集合：

- ``LOG_X`` 用于标准 printf 风格消息，例如 :c:macro:`LOG_ERR`。
- ``LOG_HEXDUMP_X`` 用于转储数据，例如 :c:macro:`LOG_HEXDUMP_WRN`。
- ``LOG_INST_X`` 用于与特定实例关联的标准 printf 风格消息，例如 :c:macro:`LOG_INST_INF`。
- ``LOG_INST_HEXDUMP_X`` 用于与特定实例关联的数据转储，例如 :c:macro:`LOG_INST_HEXDUMP_DBG`

警告级别还额外提供以下宏：

- :c:macro:`LOG_WRN_ONCE` 用于只关心首次出现的警告。

所有严重级别都提供速率受限日志宏，以防止日志刷屏：

- ``LOG_X_RATELIMIT`` 用于使用默认速率的速率受限标准 printf 风格消息，例如 :c:macro:`LOG_ERR_RATELIMIT`。
- ``LOG_X_RATELIMIT_RATE`` 用于使用自定义速率的速率受限标准 printf 风格消息，例如 :c:macro:`LOG_ERR_RATELIMIT_RATE`。
- ``LOG_HEXDUMP_X_RATELIMIT`` 用于使用默认速率的速率受限数据转储，例如 :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT`。
- ``LOG_HEXDUMP_X_RATELIMIT_RATE`` 用于使用自定义速率的速率受限数据转储，例如 :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT_RATE`。

便捷宏使用由 ``CONFIG_LOG_RATELIMIT_INTERVAL_MS`` 指定的默认速率，而显式速率宏接受一个速率参数（毫秒），指定日志消息之间的最小间隔。

有两类配置：按模块的配置和全局配置。当全局启用日志时，默认对所有模块启用。不过，模块可以本地禁用日志。每个模块可以指定自己的日志级别。
模块必须在使用 API 之前定义 :c:macro:`LOG_LEVEL` 宏。除非设置了全局覆盖，否则模块日志级别将被遵循。全局覆盖只能提高日志级别。它不能用于降低此前设置得更高的模块日志级别。还可以通过提供系统中存在的最高严重级别来全局限制日志，其中"最高"指最低严重级别（例如，如果系统中最高级别设置为 info，则表示存在 error、warning 和 info 级别，但 debug 消息被排除）。

每个使用日志的模块必须指定其唯一名称，并向日志系统注册自身。如果模块由多个文件组成，则只在其中一个文件中执行注册，但每个文件都必须指定模块名称。

日志器的默认前端设计为线程安全，并最小化记录消息所需的时间。耗时的操作（如字符串格式化或访问传输层）在调用日志 API 时默认不会执行。
调用日志 API 时，会创建一个消息并添加到列表中。使用一个专用的、可配置的日志消息池缓冲区。有 2 种类型的消息：标准消息和十六进制转储（hexdump）消息。每条消息包含一个来源 ID（模块或实例 ID 和域 ID，可用于多处理器系统）、时间戳和严重级别。标准消息包含指向字符串和参数的指针。十六进制转储消息包含已拷贝的数据和字符串。

.. _logging_kconfig:

全局 Kconfig 选项
**********************

这些选项可以在以下文件中找到：:zephyr_file:`subsys/logging/Kconfig`。

:kconfig:option:`CONFIG_LOG`：全局开关，开启/关闭日志。

运行模式：

:kconfig:option:`CONFIG_LOG_MODE_DEFERRED`：延迟模式。

:kconfig:option:`CONFIG_LOG_MODE_IMMEDIATE`：即时（同步）模式。

:kconfig:option:`CONFIG_LOG_MODE_MINIMAL`：最小占用模式。

过滤选项：

:kconfig:option:`CONFIG_LOG_RUNTIME_FILTERING`：启用运行时重新配置过滤。

:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`：默认级别，设置未指定自身日志级别的模块所使用的日志级别。

:kconfig:option:`CONFIG_LOG_OVERRIDE_LEVEL`：当模块日志级别未设置或设置得低于覆盖值时，覆盖该级别。

:kconfig:option:`CONFIG_LOG_MAX_LEVEL`：被编译进来的最高（最低严重级别）级别。

处理选项：

:kconfig:option:`CONFIG_LOG_MODE_OVERFLOW`：当无法为新消息分配空间时，丢弃最旧的消息。

:kconfig:option:`CONFIG_LOG_BLOCK_IN_THREAD`：如果启用且新日志消息无法分配，线程上下文将阻塞，
最长阻塞 :kconfig:option:`CONFIG_LOG_BLOCK_IN_THREAD_TIMEOUT_MS` 毫秒，或直到日志消息被分配成功。

:kconfig:option:`CONFIG_LOG_PRINTK`：将 printk 调用重定向到日志系统。

:kconfig:option:`CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD`：当缓冲的日志消息数量达到阈值时，
唤醒专用线程（参见 :c:func:`log_thread_set`）。如果启用了 :kconfig:option:`CONFIG_LOG_PROCESS_THREAD`，则内部线程使用此阈值。

:kconfig:option:`CONFIG_LOG_PROCESS_THREAD`：启用后，创建一个日志线程，负责处理日志。

:kconfig:option:`CONFIG_LOG_PROCESS_THREAD_STARTUP_DELAY_MS`：日志线程启动前的延迟时间（毫秒）。

:kconfig:option:`CONFIG_LOG_BUFFER_SIZE`：分配给循环数据包缓冲区的字节数。

:kconfig:option:`CONFIG_LOG_FRONTEND`：将日志直接送往自定义前端。

:kconfig:option:`CONFIG_LOG_FRONTEND_ONLY`：消息送往前端时不使用任何后端。

:kconfig:option:`CONFIG_LOG_FRONTEND_OPT_API`：针对最常见简单消息优化的可选 API。

:kconfig:option:`CONFIG_LOG_CUSTOM_HEADER`：向 log.h 注入应用程序提供的头文件。

:kconfig:option:`CONFIG_LOG_TIMESTAMP_64BIT`：64 位时间戳。

:kconfig:option:`CONFIG_LOG_SIMPLE_MSG_OPTIMIZE`：为大小和性能优化简单日志消息。该选项仅对 32 位架构可用。

格式化选项：

:kconfig:option:`CONFIG_LOG_FUNC_NAME_PREFIX_ERR`：在标准 ERROR 日志消息前添加函数名。十六进制转储消息不添加。

:kconfig:option:`CONFIG_LOG_FUNC_NAME_PREFIX_WRN`：在标准 WARNING 日志消息前添加函数名。十六进制转储消息不添加。

:kconfig:option:`CONFIG_LOG_FUNC_NAME_PREFIX_INF`：在标准 INFO 日志消息前添加函数名。十六进制转储消息不添加。

:kconfig:option:`CONFIG_LOG_FUNC_NAME_PREFIX_DBG`：在标准 DEBUG 日志消息前添加函数名。十六进制转储消息不添加。

:kconfig:option:`CONFIG_LOG_BACKEND_SHOW_TIMESTAMP`：启用后端随日志打印时间戳。

:kconfig:option:`CONFIG_LOG_BACKEND_SHOW_LEVEL`：启用后端随日志打印级别。

:kconfig:option:`CONFIG_LOG_BACKEND_SHOW_COLOR`：启用错误（红色）和警告（黄色）的着色。

:kconfig:option:`CONFIG_LOG_BACKEND_FORMAT_TIMESTAMP`：启用后，时间戳格式化为 *hh:mm:ss:mmm,uuu*。否则以原始格式打印。

后端选项：

:kconfig:option:`CONFIG_LOG_BACKEND_UART`：启用内置 UART 后端。

:kconfig:option:`CONFIG_LOG_BACKEND_NET`：启用内置网络后端，将 syslog 消息发送到网络服务器。


.. _log_usage:

使用
*****

在模块中使用日志
===================

要在模块中使用日志，必须为模块指定唯一名称，并使用 :c:macro:`LOG_MODULE_REGISTER` 注册该模块。
可选地，可以将模块的编译期日志级别作为第二个参数指定。如果未提供自定义日志级别，则使用默认日志级别（:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`）。

.. code-block:: c

   #include <zephyr/logging/log.h>
   LOG_MODULE_REGISTER(foo, CONFIG_FOO_LOG_LEVEL);

如果模块由多个文件组成，则 ``LOG_MODULE_REGISTER()`` 应出现在其中一个文件中。其他每个文件应使用
 :c:macro:`LOG_MODULE_DECLARE` 来声明其属于该模块。可选地，可以将模块的编译期日志级别作为第二个参数指定。如果未提供自定义日志级别，则使用默认日志级别（:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`）。

.. code-block:: c

   #include <zephyr/logging/log.h>
   /* 在组成模块的所有文件中（除一个外） */
   LOG_MODULE_DECLARE(foo, CONFIG_FOO_LOG_LEVEL);

要在头文件中实现的函数里使用日志 API，必须在函数体中、调用日志 API 之前使用 :c:macro:`LOG_MODULE_DECLARE` 宏。
可选地，可以将模块的编译期日志级别作为第二个参数指定。如果未提供自定义日志级别，则使用默认日志级别（:kconfig:option:`CONFIG_LOG_DEFAULT_LEVEL`）。

.. code-block:: c

   #include <zephyr/logging/log.h>

   static inline void foo(void)
   {
   	LOG_MODULE_DECLARE(foo, CONFIG_FOO_LOG_LEVEL);

   	LOG_INF("foo");
   }

专用的 Kconfig 模板（:zephyr_file:`subsys/logging/Kconfig.template.log_config`）可用于创建本地日志级别配置。

下面的示例展示了该模板的使用。结果将生成 ``CONFIG_FOO_LOG_LEVEL``：

.. code-block:: none

   module = FOO
   module-str = foo
   source "subsys/logging/Kconfig.template.log_config"

在模块实例中使用日志
============================

如果存在多实例模块，且实例在系统中被广泛使用，启用日志会导致刷屏。日志 API 提供了工具，可用于在实例级别而非模块级别过滤日志。例如，可以只为某个特定实例启用日志。

要使用实例级别过滤，必须执行以下步骤：

- 在实例结构体中声明一个指向特定日志结构体的指针。使用 :c:macro:`LOG_INSTANCE_PTR_DECLARE` 完成。

.. code-block:: c

   #include <zephyr/logging/log_instance.h>

   struct foo_object {
   	LOG_INSTANCE_PTR_DECLARE(log);
   	uint32_t id;
   }

- 模块必须为其实例化提供一个宏。在该宏中，注册日志实例，并在对象结构体中初始化日志实例指针。

.. code-block:: c

   #define FOO_OBJECT_DEFINE(_name)                             \
   	LOG_INSTANCE_REGISTER(foo, _name, CONFIG_FOO_LOG_LEVEL) \
   	struct foo_object _name = {                             \
   		LOG_INSTANCE_PTR_INIT(log, foo, _name)          \
   	}

注意，当日志被禁用时，日志实例和指向该实例的指针不会被创建。

要在源文件中使用实例日志 API，必须使用 :c:macro:`LOG_LEVEL_SET` 设置编译期日志级别。

.. code-block:: c

   LOG_LEVEL_SET(CONFIG_FOO_LOG_LEVEL);

   void foo_init(foo_object *f)
   {
   	LOG_INST_INF(f->log, "Initialized.");
   }

要在头文件中使用实例日志 API，必须使用 :c:macro:`LOG_LEVEL_SET` 设置编译期日志级别。

.. code-block:: c

   static inline void foo_init(foo_object *f)
   {
   	LOG_LEVEL_SET(CONFIG_FOO_LOG_LEVEL);

   	LOG_INST_INF(f->log, "Initialized.");
   }

控制日志
=======================

默认情况下，延迟模式下的日志处理由一个自动启动的专用任务在内部处理。不过，如果禁用了多线程，该任务可能不可用。也可以通过取消设置
 :kconfig:option:`CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD` 将其禁用。在这种情况下，可以使用 :zephyr_file:`include/zephyr/logging/log_ctrl.h` 中定义的 API 来控制日志。日志必须先初始化才能使用。可选地，用户可以提供一个返回时间戳值的函数。如果未提供，则使用 :c:macro:`k_cycle_get` 或 :c:macro:`k_cycle_get_32` 进行时间戳。:c:func:`log_process` 函数用于处理一条日志消息（如果有待处理的），如果还有待处理消息则返回 true。不过，建议使用宏封装（:c:macro:`LOG_INIT` 和 :c:macro:`LOG_PROCESS`），它们能处理日志被禁用的情况。

下面的代码片段展示了如何在简单无限循环中处理日志。

.. code-block:: c

   #include <zephyr/logging/log_ctrl.h>

   int main(void)
   {
   	LOG_INIT();
   	/* 如果启用了多线程，向日志系统提供线程 ID。 */
   	log_thread_set(k_current_get());

   	while (1) {
   		if (LOG_PROCESS() == false) {
   			/* 休眠 */
   		}
   	}
   }

如果日志从某个线程（用户线程或内部线程）处理，则可以启用一个功能：当缓冲的日志消息数量达到一定数量时唤醒处理线程（参见 :kconfig:option:`CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD`）。

.. _logging_ratelimited:

速率受限日志
********************

速率受限日志宏提供了一种方式，在消息频繁生成时防止日志刷屏。这些宏确保日志消息的输出频率不超过指定间隔，类似于 Linux 的 ``printk_ratelimited`` 功能。

速率受限日志系统提供两类宏：

**便捷宏（使用默认速率）：**
- :c:macro:`LOG_ERR_RATELIMIT` —— 速率受限错误消息
- :c:macro:`LOG_WRN_RATELIMIT` —— 速率受限警告消息
- :c:macro:`LOG_INF_RATELIMIT` —— 速率受限信息消息
- :c:macro:`LOG_DBG_RATELIMIT` —— 速率受限调试消息
- :c:macro:`LOG_HEXDUMP_ERR_RATELIMIT` —— 速率受限错误十六进制转储
- :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT` —— 速率受限警告十六进制转储
- :c:macro:`LOG_HEXDUMP_INF_RATELIMIT` —— 速率受限信息十六进制转储
- :c:macro:`LOG_HEXDUMP_DBG_RATELIMIT` —— 速率受限调试十六进制转储

**显式速率宏（使用自定义速率）：**
- :c:macro:`LOG_ERR_RATELIMIT_RATE` —— 使用自定义速率的速率受限错误消息
- :c:macro:`LOG_WRN_RATELIMIT_RATE` —— 使用自定义速率的速率受限警告消息
- :c:macro:`LOG_INF_RATELIMIT_RATE` —— 使用自定义速率的速率受限信息消息
- :c:macro:`LOG_DBG_RATELIMIT_RATE` —— 使用自定义速率的速率受限调试消息
- :c:macro:`LOG_HEXDUMP_ERR_RATELIMIT_RATE` —— 使用自定义速率的速率受限错误十六进制转储
- :c:macro:`LOG_HEXDUMP_WRN_RATELIMIT_RATE` —— 使用自定义速率的速率受限警告十六进制转储
- :c:macro:`LOG_HEXDUMP_INF_RATELIMIT_RATE` —— 使用自定义速率的速率受限信息十六进制转储
- :c:macro:`LOG_HEXDUMP_DBG_RATELIMIT_RATE` —— 使用自定义速率的速率受限调试十六进制转储

便捷宏使用由 :kconfig:option:`CONFIG_LOG_RATELIMIT_INTERVAL_MS` 指定的默认速率（
默认 5000ms）。显式速率宏接受一个速率参数（毫秒），指定日志消息之间的最小间隔。速率限制按宏调用点（call site）划分，即对速率受限宏的每次不同调用都有各自独立的速率限制。

使用示例：

.. code-block:: c

    #include <zephyr/logging/log.h>
    #include <zephyr/kernel.h>

    LOG_MODULE_REGISTER(my_module, CONFIG_LOG_DEFAULT_LEVEL);

    void process_data(void)
    {
        /* 使用默认速率（CONFIG_LOG_RATELIMIT_INTERVAL_MS）的便捷宏 */
        LOG_WRN_RATELIMIT("Data processing warning: %d", error_code);
        LOG_ERR_RATELIMIT("Critical error occurred: %s", error_msg);
        LOG_INF_RATELIMIT("Processing status: %d items", item_count);
        LOG_HEXDUMP_WRN_RATELIMIT(data_buffer, data_len, "Data buffer:");

        /* 使用自定义间隔的显式速率宏 */
        LOG_WRN_RATELIMIT_RATE(1000, "Fast rate warning: %d", error_code);
        LOG_ERR_RATELIMIT_RATE(30000, "Slow rate error: %s", error_msg);
        LOG_INF_RATELIMIT_RATE(2000, "Custom rate status: %d items", item_count);
        LOG_HEXDUMP_ERR_RATELIMIT_RATE(5000, data_buffer, data_len, "Error data:");
    }

速率受限日志特别适用于：

- 可能频繁发生但不需要刷屏的错误条件
- 紧循环或高频回调中的状态更新
- 可能压垮日志系统的调试信息
- 可能反复失败的网络或 I/O 操作

配置
=============

速率受限日志可通过以下 Kconfig 选项配置：

- :kconfig:option:`CONFIG_LOG_RATELIMIT` —— 启用/禁用速率受限日志的主开关
- :kconfig:option:`CONFIG_LOG_RATELIMIT_INTERVAL_MS` —— 便捷宏的默认间隔（5000ms）

当 :kconfig:option:`CONFIG_LOG_RATELIMIT` 被禁用时，速率受限宏的行为由 :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK` 选择项控制：

- :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK_LOG` —— 所有速率受限宏表现为普通日志宏
- :kconfig:option:`CONFIG_LOG_RATELIMIT_FALLBACK_DROP` —— 所有速率受限宏展开为空操作（默认）

这允许你控制在速率限制不可用时，速率受限日志宏是始终打印还是完全抑制。

速率限制使用静态变量和 :c:func:`k_uptime_get_32` 实现，用于跟踪每个调用点最后一次记录日志的时间。

.. _logging_panic:

日志恐慌（panic）
*****************

出现错误条件时，系统通常不能再依赖调度器或中断。在这种情况下，延迟日志消息处理不可行。日志控制 API 提供了一个进入恐慌模式的函数（:c:func:`log_panic`），应在该情况下调用。

调用 :c:func:`log_panic` 时，向所有激活的后端发送 *panic* 通知。所有后端收到通知后，所有缓冲的消息被刷新。从那一刻起，所有日志都以阻塞方式处理。

.. _logging_printk:

Printk
******

通常，日志和 :c:func:`printk` 使用同一个输出，并相互竞争。如果输出不支持抢占，这会导致问题，也可能导致输出损坏，
因为日志数据与 printk 数据交错。不过，可以通过启用 :kconfig:option:`CONFIG_LOG_PRINTK` 将 printk 消息重定向到日志子系统。在这种情况下，printk 条目被视为级别 0 的日志消息（不能被禁用）。启用后，日志系统管理输出，因此不会交错。不过，在延迟模式下，printk 行为会改变，因为输出被延迟，直到日志线程处理数据。:kconfig:option:`CONFIG_LOG_PRINTK` 默认启用。


.. _log_architecture:

架构
************

日志由 3 个主要部分组成：

- 前端（Frontend）
- 核心（Core）
- 后端（Backends）

日志消息由日志来源生成，来源可以是模块，也可以是模块的实例。

默认前端
================

当日志来源（例如 :c:macro:`LOG_INF`）调用日志 API 时，默认前端被启用，负责过滤消息（编译期和运行时）
、为消息分配缓冲区、创建消息并提交该消息。由于日志 API 可以在中断中调用，前端被优化为尽可能快地记录消息。

日志消息
-------------

日志消息包含消息描述符（来源、域和级别）、时间戳、格式化字符串详情（参见 :ref:`cbprintf_packaging`）
以及可选数据。日志消息存储在一个连续的内存块中。内存从循环数据包缓冲区（:ref:`mpsc_pbuf`）分配，这带来一些影响：

 * 每条消息都是一个自包含的、连续的内存块。因此，它适合拷贝消息（例如用于离线处理）。
 * 消息必须按顺序释放。后端处理是同步的。后端可以创建副本用于延迟处理。

日志消息具有以下格式：

+------------------+----------------------------------------------------+
| 消息头（Message Header）   | 2 位：MPSC 数据包缓冲区头                  |
|                  +----------------------------------------------------+
|                  | 1 位：Trace/Log 消息标志                      |
|                  +----------------------------------------------------+
|                  | 3 位：域 ID                                  |
|                  +----------------------------------------------------+
|                  | 3 位：级别                                      |
|                  +----------------------------------------------------+
|                  | 10 位：Cbprintf 包长度                   |
|                  +----------------------------------------------------+
|                  | 12 位：数据长度                               |
|                  +----------------------------------------------------+
|                  | 1 位：保留                                    |
|                  +----------------------------------------------------+
|                  | 指针：指向来源描述符的指针 [#l0]_   |
|                  +----------------------------------------------------+
|                  | 32 或 64 位：时间戳 [#l0]_                    |
|                  +----------------------------------------------------+
|                  | 指针：指向线程 ID 的指针（可选） [#l1]_    |
|                  +----------------------------------------------------+
|                  | 8 位：核心 ID（可选） [#l2]_                  |
|                  +----------------------------------------------------+
|                  | 可选填充 [#l3]_                            |
+------------------+----------------------------------------------------+
| Cbprintf         | 头（Header）                                             |
|                  +----------------------------------------------------+
| | 包（package）        | 参数（Arguments）                                          |
| | （可选）     +----------------------------------------------------+
|                  | 追加的字符串（Appended strings）                                   |
+------------------+----------------------------------------------------+
| 十六进制转储数据（Hexdump data，可选）                                               |
+------------------+----------------------------------------------------+
| 对齐填充（Alignment padding，可选）                                          |
+------------------+----------------------------------------------------+

.. rubric:: 脚注

.. [#l0] 根据大小不同，来源描述符和时间戳字段可能被交换，以减少填充量。
.. [#l1] 仅在启用 CONFIG_LOG_THREAD_ID_PREFIX 时存在。
.. [#l2] 仅在启用 CONFIG_LOG_CORE_ID_PREFIX 时存在。
.. [#l3] 可能用于 cbprintf 包的对齐。

日志消息分配
----------------------

前端可能无法为消息分配内存。当系统在某一时间段内生成的日志消息多于它能处理的数量时，就会发生这种情况。有两种策略来处理该情况：

- 无溢出（No overflow）——如果无法为消息分配空间，则丢弃新日志。
- 溢出（Overflow）——释放最旧的待处理消息，直到新消息可以被分配。由 :kconfig:option:`CONFIG_LOG_MODE_OVERFLOW` 启用。注意它会降低性能，因此建议调整缓冲区大小和启用的日志数量，以减少丢弃。

.. _logging_runtime_filtering:

运行时过滤
------------------

如果启用了运行时过滤，则为每个日志来源在 RAM 中声明一个过滤结构体。该过滤结构体使用 32 位，分为十个 3 位槽（slot）
。除 *slot 0* 外，每个槽存储系统中一个后端的当前过滤器。*Slot 0*（位 0-2）用于汇总给定日志来源的最大过滤设置。汇总槽决定给定条目是否创建日志消息，因为它指示是否至少有一个后端期望该日志条目。当消息被核心处理时，会检查后端槽，以确定消息是否被给定后端接受。与编译期过滤相比，二进制占用会增加，因为被丢弃的日志仍被编译进来。

在下面的示例中，后端 1 被设置为接收错误（*slot 1*），后端 2 接收直到 info 级别（*slot 2*）。Slot 3-9 未使用。
汇总过滤器（*slot 0*）被设置为 info 级别，意味着直到该级别，来自该特定来源的消息会被缓冲。

+------+------+------+------+-----+------+
|slot 0|slot 1|slot 2|slot 3| ... |slot 9|
+------+------+------+------+-----+------+
| INF  | ERR  | INF  | OFF  | ... | OFF  |
+------+------+------+------+-----+------+

.. _log_frontend:

自定义前端
================

使用 :kconfig:option:`CONFIG_LOG_FRONTEND` 启用自定义前端。日志被送往在 :zephyr_file:`include/zephyr/logging/log_frontend.h` 中声明的函数。如果启用了选项 :kconfig:option:`CONFIG_LOG_FRONTEND_ONLY`，则不创建日志消息，也不处理任何后端。否则，自定义前端可以与后端共存。

在某些情况下，日志需要在宏级别重定向。对于这些情况，可以使用 :kconfig:option:`CONFIG_LOG_CUSTOM_HEADER`
 注入一个应用程序提供的头文件 :file:`zephyr_custom_log.h`，放在 :zephyr_file:`include/zephyr/logging/log.h` 的末尾。

使用 ARM Coresight STM（System Trace Macrocell）的前端
---------------------------------------------------------

关于使用 ARM Coresight STM 进行日志的更多详情，参见 :ref:`logging_cs_stm`。

.. _logging_strings:

日志字符串
================

字符串参数由 :ref:`cbprintf_packaging` 处理。关于限制和建议，参见 :ref:`cbprintf_packaging_limitations`。

多域支持
====================

更复杂的系统可以由多个域组成，每个域都是一个独立的二进制。域的示例包括多核 SoC 中的一个核心，或 ARM TrustZone 核心上的一个二进制（Secure 或 Nonsecure）。

在多域系统上进行跟踪和调试更复杂，需要一个高效的日志系统。可以使用两种方法来构建该日志系统：

* 在每个域内独立记录日志。该选项并不总是可行，因为它要求每个域都有可用的后端（例如 UART）。该方法也可能难以使用且不可扩展，因为日志显示在独立的输出上。
* 使用多域日志系统，其中每个域的日志消息最终进入一个根域，在那里它们被处理，与单域情况完全相同。在该方法中，日志消息通过域之间的连接传递，该连接由一侧的后端创建并与另一侧链接。

  Log link（日志链接）是该多域方法中引入的接口。Log link 负责接收来自另一个域的任何日志消息，创建副本，并将该本地日志消息副本（
  包括远程数据）放入消息队列。该特定 log link 实现与互补的后端实现相匹配，以允许日志消息交换和日志器控制，如配置过滤、获取日志来源名称等。

多域系统中有三种类型的域：

* *末端域（end domain）* 拥有日志核心实现和跨域后端。它也可以并行拥有其他后端。
* *中继域（relay domain）* 拥有一个或多个到其他域的链接，但没有向用户输出日志的后端。它拥有一个跨域后端，指向另一个中继域或根域。
* *根域（root domain）* 拥有一个或多个链接，以及一个向用户输出日志的后端。

参见下图了解多域配置的示例：

.. figure:: images/multidomain.png

    多域示例

在该架构中，一个链接可以处理多个域。例如，考虑一个 SoC，有两个带 TrustZone 的 ARM Cortex-M33 核心：
核心 A 和 B（参见上面图示的示例）。系统中有四个域，因为每个核心都有 Secure 和 Nonsecure 两个域。如果 *core A nonsecure*（A_NS）是根域，它有两个链接：一个到 *core A secure*（A_NS-A_S），一个到 *core B nonsecure*（A_NS-B_NS）。*B_NS* 域有一个链接，到 *core B secure*（*B_NS-B_S*），以及一个到 *A_NS* 的后端。

由于在所有实例中都有标准日志子系统，因此始终可以拥有多个后端并同时向它们输出消息。上图中 *B_NS* 域上的虚线 UART 后端就是一个示例。

域 ID
---------

每条日志消息的来源可以通过头中的以下字段识别：``source_id`` 和 ``domain_id``。

分配给 ``domain_id`` 的值是相对的。每当一个域创建日志消息时，它将自身的 ``domain_id`` 设置为 ``0``。
当消息跨越域时，``domain_id`` 会变化，因为它加上链接偏移量。链接偏移量在初始化期间分配，此时日志核心遍历所有已注册的链接并分配偏移量。

第一个链接的偏移量设置为 1。后续偏移量等于前一个链接偏移量加上前一个链接中的域数量。

下面的示例展示了为每个域分配的 ``domain_ids``：

.. figure:: images/domain_ids.png

    域 ID 分配示例

考虑一条在 *B_S* 域上创建的日志消息：

1. 初始时，它的 ``domain_id`` 被设置为 ``0``。
#. 当 *B_NS-B_S* 链接收到该消息时，它通过加上 *B_NS-B_S* 偏移量将 ``domain_id`` 增加到 ``1``。
#. 消息被传递到 *A_NS*。
#. 当 *A_NS-B_NS* 链接收到该消息时，它将偏移量（``2``）加到 ``domain_id`` 上。最终消息的 ``domain_id`` 被设置为 ``3``，唯一标识了消息的来源。

跨域日志消息
------------------------

在大多数情况下，每个域的地址空间是唯一的，一个域不能直接访问另一个域中的数据。因此，后端可以在消息被传递到另一个域之前对其部分处理。
部分处理可以包括将字符串包转换为*完全自包含*版本（将只读字符串拷贝到包主体中）。

每个域在频率和偏移方面可以有不同的时间戳源。日志不执行任何时间戳转换。

运行时过滤
-----------------

在单域情况下，每个日志来源都有一个专用变量，用于系统中每个后端的运行时过滤。在多域情况下，日志消息的来源不知道根域中后端的数量。

因此，要在多个域中过滤日志，每个来源在通往根域的每个域中都需要一个运行时过滤设置。由于其他域中来源的数量在编译期间未知，远程来源的运行时过滤必须使用动态分配的内存（
每个来源一个字）。当根域中的后端更改来自远程域的模块的过滤时，本地过滤器被更新。更新后，汇总过滤器（所有本地后端中的最大值）被检查，如果发生变化，远程域会被告知该变化。通过这种方法，运行时过滤在多域和单域场景下行为完全相同。

消息顺序
----------------

日志不提供任何机制来同步多个域之间的时间戳：

* 如果域有不同的时间戳源，消息将按到达根域缓冲区的顺序处理。
* 如果域有相同的时间戳源，或者存在一个带外机制重新计算时间戳，则有 2 个选项：

  * 消息按到达根域缓冲区的顺序处理。消息无序，但主机可以按时间戳排序，因为时间戳指示消息生成的时间。
  * 链接拥有专用缓冲区。处理期间，检查每个缓冲区的头部，最先处理最旧的消息。

    通过这种方法，可以保持消息的顺序，代价是次优的内存利用率（因为缓冲区不共享）和增加的处理延迟（参见 :kconfig:option:`CONFIG_LOG_PROCESSING_LATENCY_US`）。

日志后端
================

日志后端使用 :c:macro:`LOG_BACKEND_DEFINE` 注册。该宏在专用内存段中创建一个实例。后端可以动态启用（
:c:func:`log_backend_enable`）和禁用。当启用了 :ref:`logging_runtime_filtering` 时，可以使用 :c:func:`log_filter_set` 动态更改给定后端的模块日志过滤。模块由来源 ID 和域 ID 标识。如果已知来源名称，可以通过遍历所有已注册的来源来获取来源 ID。

日志支持最多 9 个并发后端。一条日志消息在处理阶段被传递给每个后端。此外，当日志进入恐慌模式时，后端通过 :c:func:`log_backend_panic` 收到通知。
当发生这种情况时，后端应切换到同步的、无中断的操作，或者如果不支持，则关闭自身。偶尔，日志可能通过 :c:func:`log_backend_dropped` 告知后端被丢弃消息的数量。消息处理 API 是版本相关的。

:c:func:`log_backend_msg_process` 用于处理消息。它对标准消息和十六进制转储消息通用，因为标准消息将其格式化参数存放在与十六进制转储消息存放数据相同的位置。
它对延迟和即时日志也通用。

.. _log_output:

消息格式化
------------------

日志提供了一组函数，后端可用于格式化消息。辅助函数在 :zephyr_file:`include/zephyr/logging/log_output.h` 中可用。

使用 :c:func:`log_output_msg_process` 格式化的示例消息：

.. code-block:: console

   [00:00:00.000,274] <info> sample_instance.inst1: logging message


.. _logging_guide_dictionary:

基于字典的日志
========================

基于字典的日志以二进制格式输出日志消息，而非人类可读的文本。该二进制格式将格式化字符串的参数以其原生存储格式编码，可能比其文本等价形式更紧凑。
对于静态定义的字符串（包括格式字符串和任何字符串参数），编码的是对 ELF 文件的引用，而非整个字符串。构建时创建的字典包含这些引用与实际字符串之间的映射。这允许离线解析器从字典获取字符串来解析日志消息。该二进制格式在某些场景下允许更紧凑的日志消息表示。不过，这需要使用离线解析器，且不如基于文本的日志消息直观易用。

注意 ``long double`` 不被 Python 的 ``struct`` 模块支持。因此，包含 ``long double`` 的日志消息不会显示正确的值。


配置
-------------

以下是与基于字典的日志相关的 kconfig 选项：

- :kconfig:option:`CONFIG_LOG_DICTIONARY_SUPPORT` 启用基于字典的日志支持。需要它的后端应选择此项。

- UART 后端可用于基于字典的日志。以下是 UART 后端的附加配置：

  - :kconfig:option:`CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_HEX` 让 UART 后端对基于字典的日志输出十六进制字符。当日志数据需要通过终端和控制台手动捕获时，这很有用。

  - :kconfig:option:`CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_BIN` 让 UART 后端输出二进制数据。

- RTT 后端也可用于基于字典的日志：

  - :kconfig:option:`CONFIG_LOG_BACKEND_RTT` 启用 RTT 后端。

  - :kconfig:option:`CONFIG_LOG_BACKEND_RTT_OUTPUT_DICTIONARY` 为 RTT 后端启用基于字典的输出。与 :kconfig:option:`CONFIG_USE_SEGGER_RTT` 一起使用。

  - :kconfig:option:`CONFIG_LOG_BACKEND_RTT_OUTPUT_DICTIONARY_HEX` 让 RTT 后端对基于字典的日志输出十六进制字符。


使用
-----

当通过启用相关日志后端启用基于字典的日志时，将在构建目录中创建一个名为 :file:`log_dictionary.json` 的 JSON 数据库文件。
该数据库文件包含解析器正确解析日志数据所需的信息。注意该数据库文件仅与同一构建配合使用，不能用于任何其他构建。

离线解析
^^^^^^^^^^^^^^^

要解析之前捕获的日志文件：

.. code-block:: console

  ./scripts/logging/dictionary/log_parser.py <build dir>/log_dictionary.json <log data file>

解析器接受两个必需参数，第一个是 JSON 数据库文件的完整路径，第二个是包含日志数据的文件。如果日志数据文件包含十六进制字符，
则在末尾添加可选参数 ``--hex``（例如当 ``CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY_HEX=y`` 时）。这告诉解析器在解析前将十六进制字符转换为二进制。

实时解析
^^^^^^^^^^^^

要实时解码基于字典的日志输出，使用实时日志解析器。它连接到正在运行的设备，并在二进制日志数据到达时持续解码。注意实时解析器仅支持二进制字典输出（不支持十六进制编码）。实时解析器支持三种输入模式：

**串口（Serial，UART）：**

.. code-block:: console

  ./scripts/logging/dictionary/live_log_parser.py <build dir>/log_dictionary.json
   serial <port> <baudrate>

例如，以 115200 波特率从 ``/dev/ttyACM0`` 读取：

.. code-block:: console

  ./scripts/logging/dictionary/live_log_parser.py build/zephyr/log_dictionary.json
   serial /dev/ttyACM0 115200

**JLink RTT：**

.. code-block:: console

  ./scripts/logging/dictionary/live_log_parser.py <build dir>/log_dictionary.json
   jlink-rtt <device_name>

例如，从 nRF5340 读取 RTT 输出：

.. code-block:: console

  ./scripts/logging/dictionary/live_log_parser.py build/zephyr/log_dictionary.json
   jlink-rtt nrf5340_xxaa_app

JLink RTT 模式需要 ``pylink-square`` Python 包（``pip install pylink-square``）
。可选参数包括 ``--channel`` 选择 RTT 通道（默认：0）、``--speed`` 设置连接速度，以及 ``--block-address`` 以十六进制指定 RTT 控制块地址。

**文件 / 标准输入（File / stdin）：**

.. code-block:: console

  ./scripts/logging/dictionary/live_log_parser.py <build dir>/log_dictionary.json file <filepath>

当省略 ``<filepath>`` 时，解析器从标准输入读取，这允许将二进制数据直接管道输入。

更多使用日志解析器的示例，请参见 :zephyr:code-sample:`logging-dictionary` 示例。


建议与限制
*******************************

请考虑以下建议：

* 启用 :kconfig:option:`CONFIG_LOG_SPEED` 可以略微加快延迟日志，代价是略微增加内存占用。
* 建议当指针与 ``%s`` 格式说明符一起使用且指向常量字符串时，将其转换为 ``const char *``。
* 建议当指针与 ``%s`` 格式说明符一起使用且指向临时字符串时，将其转换为 ``char *``。
* 要求当字符指针与 ``%p`` 格式说明符一起使用时，将其转换为非字符指针（例如 ``void *``）。

.. code-block:: c

   LOG_WRN("%s", str);
   LOG_WRN("%p", (void *)str);

请考虑以下限制：

* 日志不支持带宽度的字符串格式说明符（例如 ``%.*s`` 或 ``%8s``）。这是因为格式字符串内容不用于构建日志消息，只有参数类型被使用。
* 如果使用延迟日志，且日志消息以线程名作为前缀（Kconfig 选项 ``CONFIG_LOG_THREAD_ID_PREFIX=y`` 和 ``CONFIG_THREAD_NAME=y``），则假定当日志消息被格式化时，对应的 :c:struct:`k_thread` 结构体仍然有效。当该结构体使用 :c:func:`k_malloc` 或 :c:func:`malloc` 动态分配时，这可能是一个问题。在这种情况下，如果线程记录了一些消息然后被停止，且其 ``struct k_thread`` 被释放，日志系统稍后处理该消息时仍会尝试访问该结构体。这会造成释放后使用（use-after-free）场景。为避免此问题，解决方案是在释放结构体前调用 :c:func:`log_flush`。

.. code-block:: c

   struct k_thread *thread = k_malloc(sizeof(*thread)); /* 动态分配的结构体 */
   k_thread_create(thread, ...);
   k_thread_name_set(thread, "foobar");

   /* 线程调用 LOG_*(...) */

   k_thread_join(thread, K_FOREVER);
   log_flush();  /* 在释放 struct k_thread 之前刷新日志缓冲区 */
   k_free(thread); /* 避免使用延迟日志时潜在的释放后使用场景 */

基准测试（Benchmark）
*****************

基准测试数据来自 :zephyr_file:`tests/subsys/logging/log_benchmark`，在 ``qemu_x86`` 上执行。这是一个粗略的对比，用于给出总体概况。

+--------------------------------------------+------------------+
| 特性（Feature）                                    |                  |
+============================================+==================+
| 内核日志（Kernel logging）                             | 7us [#f0]_/11us  |
|                                            |                  |
+--------------------------------------------+------------------+
| 用户日志（User logging）                               | 13us             |
|                                            |                  |
+--------------------------------------------+------------------+
| 带覆盖写的内核日志（kernel logging with overwrite）              | 10us [#f0]_/15us |
+--------------------------------------------+------------------+
| 记录临时字符串（Logging transient string）                   | 42us             |
+--------------------------------------------+------------------+
| 从用户空间记录临时字符串（Logging transient string from user）         | 50us             |
+--------------------------------------------+------------------+
| 内存利用率（Memory utilization）[#f1]_                  | 518              |
|                                            |                  |
+--------------------------------------------+------------------+
| 内存占用（测试）（Memory footprint (test)）[#f2]_             | 2k               |
+--------------------------------------------+------------------+
| 内存占用（应用程序）（Memory footprint (application)）[#f3]_      | 3.5k             |
+--------------------------------------------+------------------+
| 消息占用（Message footprint）[#f4]_                   | 47 [#f0]_/32     |
|                                            | 字节（bytes）            |
+--------------------------------------------+------------------+

.. rubric:: 基准测试详情

.. [#f0] 启用 :kconfig:option:`CONFIG_LOG_SPEED`。

.. [#f1] 在分配给日志的 2048 字节中可容纳的不同参数数量的日志消息数量。

.. [#f2] 日志子系统在 :zephyr_file:`tests/subsys/logging/log_benchmark` 中的内存占用，其中未使用过滤和格式化功能。

.. [#f3] 日志子系统在 :zephyr_file:`samples/subsys/logging/logger` 中的内存占用。

.. [#f4] 在 ``Cortex M3`` 上带 2 个参数的日志消息（不含字符串）的平均大小

栈使用
**********

启用日志时，它会影响使用日志 API 的上下文的栈使用。如果栈被优化，可能导致栈溢出。栈使用取决于模式和优化。它也在不同平台之间显著变化。
一般来说，当使用 :kconfig:option:`CONFIG_LOG_MODE_DEFERRED` 时，栈使用更小，因为日志仅限于创建和存储日志消息。如果使用 :kconfig:option:`CONFIG_LOG_MODE_IMMEDIATE`，则日志消息由后端处理，包括字符串格式化，直接在调用日志 API 的上下文中执行。在该模式下，栈使用取决于使用哪些后端。

一些平台对带两个 ``integer`` 参数日志消息的特性列表如下：

+---------------+----------+----------------------------+-----------+-----------------------------+
| 平台（Platform）      | 延迟（Deferred） | 延迟（无优化）（Deferred (no optimization)） | 即时（Immediate） | 即时（无优化）（Immediate (no optimization)） |
+===============+==========+============================+===========+=============================+
| ARM Cortex-M3 | 40       | 152                        | 412       | 783                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| x86           | 12       | 224                        | 388       | 796                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| riscv32       | 24       | 208                        | 456       | 844                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| xtensa        | 72       | 336                        | 504       | 944                         |
+---------------+----------+----------------------------+-----------+-----------------------------+
| x86_64        | 32       | 528                        | 1088      | 1440                        |
+---------------+----------+----------------------------+-----------+-----------------------------+

使用 ARM Coresight STM 进行日志
*******************************

关于在 NRF54H20 上使用 ARM Coresight STM 进行日志，参见 :ref:`logging_cs_stm`。

API 参考
*************

.. doxygengroup:: log_api

.. doxygengroup:: log_ctrl

.. doxygengroup:: log_msg

.. doxygengroup:: log_backend

.. doxygengroup:: log_output

.. toctree::
   :maxdepth: 1

   cs_stm.rst
