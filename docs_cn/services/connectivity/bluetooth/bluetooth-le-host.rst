.. _bluetooth_le_host:

LE Host
#######

蓝牙 Host 实现了所有高层协议和配置文件，最重要的是，它为应用提供高层 API。下图展示了 host 的主要协议与配置文件层次。

.. figure:: img/ble_host_layers.png
   :align: center
   :alt: Bluetooth Host protocol & profile layers

   蓝牙 Host 协议与配置文件层次。

Host 协议栈最底层是一个所谓的 HCI 驱动，负责屏蔽 HCI 传输的细节。它提供了一个基础 API，用于在控制器与 host 之间双向传递数据。

也许在 HCI 处理之上最重要的模块是通用访问配置文件（GAP）。GAP 通过定义四种不同的蓝牙使用角色来简化蓝牙 LE 访问：

* 面向连接的角色

  * Peripheral（外围设备，例如智能传感器，通常具有有限的用户界面）

  * Central（中心设备，通常是手机或 PC）

* 非连接的角色

  * Broadcaster（广播器，发送蓝牙 LE 广播，例如智能 beacon）

  * Observer（观察者，扫描蓝牙 LE 广播）

每个角色都带有自己的构建时配置选项：
:kconfig:option:`CONFIG_BT_PERIPHERAL`、:kconfig:option:`CONFIG_BT_CENTRAL`、
:kconfig:option:`CONFIG_BT_BROADCASTER` 与 :kconfig:option:`CONFIG_BT_OBSERVER`。在
面向连接的角色中，central 隐式启用 observer 角色，
peripheral 隐式启用 broadcaster 角色。通常创建应用的第一步
是决定需要哪些角色，然后从那里开始。蓝牙 Mesh 是一个略特殊的案例，至少需要
observer 和 broadcaster 角色，可能还需要
Peripheral 角色。这将在后续章节中更详细地描述。

Peripheral 角色
================

大多数基于 Zephyr 的蓝牙 LE 设备很可能都是 peripheral 角色
设备。这意味着它们执行可连接广播并暴露一个或多个 GATT 服务。使用
:c:func:`bt_gatt_service_register` API 注册服务后，应用通常会
使用 :c:func:`bt_le_adv_start` API 开始可连接广播。

树中有多个 peripheral 示例应用可用，
例如 :zephyr_file:`samples/bluetooth/peripheral_hr`。

Central 角色
============

对于基于 Zephyr 的设备，central 角色可能不如 peripheral
角色常见，但它仍然是一个合理的选择，并且在
Zephyr 中同样得到良好支持。central 角色设备不是接受来自其他设备的连接，而是扫描可用的 peripheral 设备并选择其中一个
进行连接。连接后，central 通常充当 GATT
客户端，首先发现可用的服务，然后
访问一个或多个受支持的服务。

为了最初发现要连接的设备，应用很可能
使用 :c:func:`bt_le_scan_start` API，等待找到合适的设备
（使用扫描回调），使用
:c:func:`bt_le_scan_stop` 停止扫描，然后使用
:c:func:`bt_conn_le_create` 连接到该设备。

树中有一些 central 角色的示例应用可用，
例如 :zephyr_file:`samples/bluetooth/central_hr`。

Observer 角色
=============

observer 角色设备会使用 :c:func:`bt_le_scan_start` API
扫描设备，但不会连接到任何设备。相反，它会
简单地利用所发现设备的广播数据，可选地与接收信号强度（RSSI）结合使用。

Broadcaster 角色
================

broadcaster 角色设备会使用 :c:func:`bt_le_adv_start` API
广播特定的广播数据，但广播类型将
是不可连接的，即其他设备无法连接到它。

连接
==========

连接处理和相关 API 可在
:ref:`连接管理 <bluetooth_connection_mgmt>` 一节中找到。

.. _bluetooth_callback_contexts:

回调执行上下文
===========================

Host 通过注册的回调将事件传递给应用，
例如 :c:struct:`bt_conn_cb`、:c:struct:`bt_le_scan_cb` 或
:c:struct:`bt_l2cap_chan_ops` 中的回调。除非文档另有说明，这些回调
从线程上下文调用，绝不从中断服务程序（ISR）调用。大多数在协议栈内部上下文中运行，但有些目前从触发它们的 API 调用内部同步调用，
因此运行在调用线程中：
例如 :c:func:`bt_unpair` 调用 ``bond_deleted``，
:c:func:`bt_gatt_unsubscribe` 可以用 ``NULL`` 数据调用 ``notify``，
然后返回。两种行为都不属于 API 的一部分：当前同步传递的回调
可能在未来的版本中延迟到协议栈内部上下文，
或者反过来，具体的线程在之前的版本之间已经变化过，
未来也可能再次变化。应用只应依赖上述保证，
而不是依赖从任何特定内容调用，或在其返回之前被调用。

当回调在协议栈内部上下文中运行时，该上下文
与协议栈自身的处理共享：在回调中花费的时间会延迟
其他蓝牙活动，阻塞则带有额外风险，因为
只有蓝牙处理本身才能满足的等待会变成死锁，
因为该处理在回调返回之前无法继续。
经典例子是从由运行回调的同一上下文补充的池中
以 ``K_FOREVER`` 分配缓冲区。由于
应用无法依赖给定回调使用哪个上下文，以下做法
适用于每个回调。

从回调中调用蓝牙 API 很常见且受支持，即使
其中大多数可能会阻塞；阻塞风险通过管理而非
规避来处理：

* 保持回调简短，将长时间运行或无限阻塞的工作
  延迟到应用拥有的线程或工作队列。
* 优先使用 ``K_NO_WAIT`` 或有界超时的分配，
  而非 ``K_FOREVER``，并处理失败。
* 将缓冲区池（例如 :kconfig:option:`CONFIG_BT_L2CAP_TX_BUF_COUNT`
  或 :kconfig:option:`CONFIG_BT_ATT_TX_COUNT`）的尺寸设置为
  从回调中进行的分配无需等待。

安全
========

要在两个蓝牙设备之间建立安全关系，
使用一个称为配对的过程。该过程可以通过
GATT 服务的安全属性隐式触发，
或使用 :c:func:`bt_conn_set_security` API 在连接对象上显式触发。

要达到更高的安全级别并保护
免受中间人（MITM）攻击，建议在配对期间使用某个
带外信道。如果设备具有足够的
用户界面，该“信道”就是用户本身。设备的
能力使用 :c:func:`bt_conn_auth_cb_register`
API 注册。传递给该 API 的 :c:struct:`bt_conn_auth_cb` 结构体
有一组可选回调，可在配对期间使用——如果
设备缺少某个功能，对应的回调可设置为 NULL。
例如，如果设备没有输入方式但有
显示屏，``passkey_entry`` 和 ``passkey_confirm`` 回调将
设置为 NULL，但 ``passkey_display`` 将设置为
能够向用户显示口令的回调。

根据本地和远程的安全需求与能力，
有四种可以达到的安全级别：

    :c:enumerator:`BT_SECURITY_L1`
        无加密且无认证。

    :c:enumerator:`BT_SECURITY_L2`
        有加密但无认证（无 MITM 保护）。

    :c:enumerator:`BT_SECURITY_L3`
        使用 Bluetooth 4.0 和 4.1 的遗留配对方法进行
        加密和认证。

    :c:enumerator:`BT_SECURITY_L4`
        使用自 Bluetooth 4.2 起可用的 LE Secure Connections
        特性进行加密和认证。

.. note::
   Mesh 通过一个称为
   配准的过程拥有自己的安全解决方案。它遵循
   与配对类似的流程，但使用
   单独的 mesh 专属 API 完成。

L2CAP
=====

L2CAP 代表逻辑链路控制与适配协议。它是
所有蓝牙连接通信的公共层，但
应用仅在使用所谓的面向连接信道（CoC）模式与其直接接触时才会接触到它。有关
此的更多信息可在 :ref:`L2CAP API 一节 <bt_l2cap>` 中找到。

术语
-----------

定义来自 Core Specification 5.4 版，卷 3，部分 A
1.4。

.. list-table::
   :header-rows: 1

   * - 术语
     - 描述

   * - 上层
     - L2CAP 之上的层，以 SDU 形式交换数据。它可能是
       应用或更高层协议。

   * - 下层
     - L2CAP 之下的层，以 PDU（或片段）形式交换数据。它
       通常是 HCI。

   * - 服务数据单元（SDU）
     - L2CAP 与上层交换的数据包。

       该术语仅在增强重传模式、流模式、重传模式和流量控制模式下相关，在基本 L2CAP 模式下不相关。

   * - 协议数据单元（PDU）
     - 包含 L2CAP 数据的数据包。PDU 总是以基本 L2CAP
       头部开始。

       LE 的 PDU 类型：:ref:`B 帧 <bluetooth_l2cap_b_frame>` 和
       :ref:`K 帧 <bluetooth_l2cap_k_frame>`。

       BR/EDR 的 PDU 类型：I 帧、S 帧、C 帧和 G 帧。

   * - 最大传输单元（MTU）
     - 上层能够接受的 SDU 最大尺寸。

   * - 最大载荷尺寸（MPS）
     - L2CAP 层能够接受的最大载荷尺寸。

       在基本 L2CAP 模式下，MTU 尺寸等于 MPS。在无分段信用制
       信道中，MTU 为 MPS 减 2。

   * - 基本 L2CAP 头部
     - 位于每个 PDU 的开头。它包含两个字段，PDU
       长度和信道标识符（CID）。

PDU 类型
---------

.. _bluetooth_l2cap_b_frame:

B 帧：基本信息帧
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在基本 L2CAP 模式下使用的 PDU。它包含从上层
接收的载荷，或作为其载荷交付给上层的载荷。

.. image:: img/l2cap_b_frame.drawio.svg
   :align: center
   :width: 45%
   :alt: B 帧 PDU 的表示。PDU 分为两个矩形，
         第一个是 L2CAP 头部，其尺寸为 4 个八位组，
         由 PDU 长度和信道 ID 组成。第二个矩形表示
         信息载荷，其尺寸小于或等于 MPS。

.. _bluetooth_l2cap_k_frame:

K 帧：信用制帧
^^^^^^^^^^^^^^^^^^^^^^^

在 LE 信用制流量控制模式和增强信用制流量
控制模式下使用的 PDU。它包含一个 SDU 片段和
附加协议信息。

.. image:: img/l2cap_k_frame_1.drawio.svg
   :width: 45%
   :alt: 起始 K 帧 PDU 的表示。PDU 分为三个
         矩形，第一个是 L2CAP 头部，其尺寸为 4 个八位组
         ，由 PDU 长度和信道 ID 组成。第二个矩形
         表示 L2CAP SDU 长度，其尺寸为 2 个八位组。第三个
         矩形表示信息载荷，其尺寸小于或
         等于 MPS 减 2 个八位组。信息载荷包含 L2CAP
         SDU。

.. image:: img/l2cap_k_frame.drawio.svg
   :align: right
   :width: 45%
   :alt: 起始 K 帧之后的 K 帧 PDUs 的表示。PDU 分为
         两个矩形，第一个是 L2CAP 头部，其尺寸为 4 个
         八位组，由 PDU 长度和信道 ID 组成。第二个
         矩形表示信息载荷，其尺寸小于或
         等于 MPS。信息载荷包含 L2CAP SDU。

相关 Kconfig
----------------

.. list-table::
   :header-rows: 1

   * - Kconfig 符号
     - 描述

   * - :kconfig:option:`CONFIG_BT_BUF_ACL_RX_SIZE`
     - 代表 MPS

   * - :kconfig:option:`CONFIG_BT_L2CAP_TX_MTU`
     - 代表 L2CAP MTU

   * - :kconfig:option:`CONFIG_BT_L2CAP_DYNAMIC_CHANNEL`
     - 启用 LE 信用制流量控制，从而使协议栈可能使用
       :ref:`K 帧 <bluetooth_l2cap_k_frame>` PDU

GATT
====

通用属性配置文件是在 LE 连接上进行通信的最常见方式。有关该层更详细的描述
以及 API 参考可在
:ref:`GATT API 参考一节 <bt_gatt>` 中找到。

ATT 超时
-----------

如果对端设备未在 ATT 超时内响应 ATT 请求（如读或写），
host 将自动发起断开连接。这通过
将罕见故障条件减少为常见断开来简化错误处理，
使开发者无需为 ATT 超时设置特殊情况即可管理意外断开。

.. image:: img/att_timeout.svg
   :align: center
   :alt: ATT timeout

Mesh
====

在所需 GAP 角色方面，Mesh 略特殊。
默认情况下，mesh 需要同时启用 observer 和 broadcaster 角色。
如果希望使用可选的 GATT Proxy 特性，则
还应启用 peripheral 角色。

mesh 的 API 参考可在
:ref:`Mesh API 参考一节 <bluetooth_mesh>` 中找到。

LE Audio
========
LE audio 是一组利用 GATT 和
等时信道在蓝牙低功耗上提供音频的配置和服务。
架构和 API 参考可在
:ref:`蓝牙音频架构 <bluetooth_le_audio_arch>` 中找到。


.. _bluetooth-persistent-storage:

持久存储
==================

蓝牙 host 协议栈使用 settings 子系统实现
到 flash 的持久存储。这需要存在 flash
驱动和 flash 上指定的“storage”分区。所需的一组
典型配置选项大致如下：

  .. code-block:: cfg

    CONFIG_BT_SETTINGS=y
    CONFIG_FLASH=y
    CONFIG_FLASH_PAGE_LAYOUT=y
    CONFIG_FLASH_MAP=y
    CONFIG_NVS=y
    CONFIG_SETTINGS=y

启用后，由应用负责在初始化蓝牙
（使用
:c:func:`bt_enable` API）之后调用
settings_load()。
