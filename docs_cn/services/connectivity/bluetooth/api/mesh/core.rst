.. _bluetooth_mesh_core:

核心
####

核心模块提供管理蓝牙 Mesh 通用状态的功能。

.. _bluetooth_mesh_lpn:

低功耗节点
**************

低功耗节点（LPN）角色允许电池供电设备作为叶节点参与 Mesh 网络。LPN 通过 Friend 节点与 Mesh 网络交互，该节点负责中继所有发往 LPN 的消息。LPN 通过保持无线电关闭来节省电量，只在需要发送消息或轮询 Friend 节点获取入站消息时才唤醒。

无线电控制和轮询由 Mesh 协议栈自动管理，但 LPN API 允许应用随时通过 :c:func:`bt_mesh_lpn_poll` 触发轮询。LPN 运行参数（包括轮询间隔、轮询事件时序和 Friend 要求）通过 :kconfig:option:`CONFIG_BT_MESH_LOW_POWER` 选项及相关配置选项控制。

在结合日志功能使用 LPN 特性时，强烈建议仅使用 :kconfig:option:`CONFIG_LOG_MODE_DEFERRED` 选项。延迟模式以外的日志模式可能在处理日志消息时引入非预期延迟，进而影响接收延迟和接收窗口的调度。同样的限制也适用于 :kconfig:option:`CONFIG_BT_MESH_FRIEND` 选项。

重放保护列表
**********************

重放保护列表（RPL）用于保存从 Mesh 网络内各元素最近接收到的序列号，以执行针对重放攻击的保护。

为了让节点在重启后仍受重放攻击保护，需要在断电前将整个 RPL 保存到持久存储中。根据 Mesh 网络中的流量大小，保存最近看到的序列号可能导致闪存磨损提前或延后发生。为缓解该问题，可以使用 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT`。该选项会推迟将 RPL 条目保存到持久存储。

不过，该选项并不能完全解决问题，因为节点可能在保存 RPL 的定时器触发前断电。为确保消息不能被重放，节点可以随时（或在断电前足够早的时间）调用 :c:func:`bt_mesh_rpl_pending_store` 来启动保存待处理的 RPL 条目。在此情况下，由节点决定保存哪些 RPL 条目。

将 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 设置为 -1 可以完全关闭该定时器，这有助于显著减少闪存磨损。这会将保存 RPL 的责任转移给用户应用，并要求从调用该 API 到所有 RPL 条目写入闪存期间，都有足够的电源备份可用。

在 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 与调用 :c:func:`bt_mesh_rpl_pending_store` 之间找到合适的平衡，可以降低安全风险和闪存磨损。

.. warning:

   未启用 :kconfig:option:`CONFIG_BT_SETTINGS`，或将 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT` 设置为 -1 后未在重启之间保存 RPL，都会使设备容易遭受重放攻击，并且无法执行规范要求的重放保护。

.. _bluetooth_mesh_persistent_storage:

持久存储
******************

Mesh 协议栈使用 :ref:`Settings 子系统 <settings_api>` 来持久保存设备配置。当协议栈配置发生变化且该变化需要持久保存时，协议栈会调度一个工作项。调度工作项与提交到工作队列之间的延迟由 :kconfig:option:`CONFIG_BT_MESH_STORE_TIMEOUT` 选项定义。一旦数据保存被调度，在工作项被处理之前就不能重新调度。某些例外情况见下文描述。

当 IV 索引、序列号或 CDB 配置需要保存时，工作项会不带延迟地提交到工作队列。如果工作项之前已被调度，则会被不带延迟地重新调度。

重放保护列表使用同一个工作项来保存 RPL 条目。如果请求保存 RPL 条目，且没有其他待保存的配置，则延迟被设置为 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT`。如果有其他协议栈配置需要保存，且 :kconfig:option:`CONFIG_BT_MESH_STORE_TIMEOUT` 选项定义的延迟小于 :kconfig:option:`CONFIG_BT_MESH_RPL_STORE_TIMEOUT`，并且工作项是由重放保护列表调度的，则工作项会被重新调度。

当工作项运行时，协议栈会保存所有待保存的配置，包括 RPL 条目。

工作项执行上下文
===========================

:kconfig:option:`CONFIG_BT_MESH_SETTINGS_WORKQ` 选项配置工作项的执行上下文。该选项默认启用，结果是协议栈使用专用协作线程来处理工作项。这允许协议栈在保存协议栈配置的同时，继续处理其他入站和出站消息，以及提交到系统工作队列的其他工作项。

当该选项禁用时，工作项被提交到系统工作队列。这意味着系统工作队列会被阻塞，持续时间为保存协议栈配置所需的时间。不建议禁用该选项，因为这会使设备在可察觉的时间内无响应。

.. _bluetooth_mesh_adv_identity:

广播身份
**********************

所有 Mesh 协议栈承载者都使用 :c:macro:`BT_ID_DEFAULT` 本地身份广播数据。该值在 Mesh 协议栈实现中预设。当蓝牙低功耗（LE）和蓝牙 Mesh 在同一设备上共存时，应用应在开始通信之前为蓝牙低功耗用途分配并配置另一个本地身份。

API 参考
**************

.. doxygengroup:: bt_mesh
