.. _net_l2_interface:

L2 层管理
###########

.. contents::
    :local:
    :depth: 2

概述
********

L2 协议栈的设计目标是把整个网络链路层部分及相关设备驱动对上层网络栈隐藏起来。
这是通过 :c:struct:`net_if` 实现的，该结构体声明在
:zephyr_file:`include/zephyr/net/net_if.h` 中。

上层除了 net_if 对象之外，对 L2 层在
:zephyr_file:`include/zephyr/net/net_l2.h` 中提供的 :c:struct:`net_l2`
通用 API 之外的实现细节并不知情。

只有 L2 层能够与绑定到 net_if 对象的设备驱动通信。L2 层规定了设备驱动
提供的 API，这些 API 针对特定设备并针对协同工作做了优化。

目前，已有的 L2 层包括 :ref:`Ethernet <ethernet_interface>`、
:ref:`IEEE 802.15.4 Soft-MAC <ieee802154_interface>`、:ref:`CANBUS <can_api>`、
:ref:`OpenThread <thread_protocol_interface>`、Wi-Fi，以及一个可作为
编写新 L2 层模板的 dummy 层示例。

L2 层 API
************

要创建一个 L2 层，或为某个特定 L2 层编写驱动，
就需要理解 L3 层如何与其交互，
以及 L2 层应当如何工作。
另请参阅 :ref:`网络栈架构 <network_stack_architecture>` 了解
更多细节。通用 L2 API 包含以下函数：

- ``recv()``：所有设备驱动在收到数据包并将其放入
  :c:struct:`net_pkt` 后，都会通过 :c:func:`net_recv_data`
  将该缓冲区推送到网络栈。此时，网络栈不知道该缓冲区该如何处理，
  而是将其传递给 L2 栈的 ``recv()`` 函数进行处理。
  L2 栈会对数据包做它需要做的事，例如解析链路层
  头部，或处理仅属于链路层的数据包。``recv()``
  函数在遇到错误数据包时返回 ``NET_DROP``，
  如果数据包已被 L2 完全消费则返回 ``NET_OK``，
  如果接下来应由网络栈处理则返回 ``NET_CONTINUE``。

- ``send()``：与接收函数类似，网络栈会调用此
  函数来实际发送一个网络数据包。所有相关的链路层内容
  都会由该函数生成并添加。
  ``send()`` 函数返回已发送的字节数，
  如果发送网络数据包失败则返回负错误码。

- ``enable()``：此函数用于启用/禁用某个网络
  接口上的流量。函数出错时返回 ``<0``，无错误时返回 ``>=0``。

- ``get_flags()``：此函数返回 L2 驱动的能力，
  例如 L2 是否支持多播或混杂模式。

网络设备驱动
**********************

网络设备驱动完全以 Zephyr 设备驱动模型
为基础。请参阅 :ref:`device_model_api`。

不过，有两点不同：

- driver_api 指针必须指向一个有效的 :c:struct:`net_if_api`
  指针。

- 网络设备驱动必须使用 :c:macro:`NET_DEVICE_INIT_INSTANCE()`
  或 :c:macro:`ETH_NET_DEVICE_INIT()`（针对以太网设备）。这些
  宏会调用 :c:macro:`DEVICE_DEFINE()` 宏，同时
  还会实例化一个与所创建的设备驱动实例相关联的
  唯一的 :c:struct:`net_if`。

实现网络设备驱动取决于其所属的 L2 栈：
:ref:`Ethernet <ethernet_interface>`、
:ref:`IEEE 802.15.4 <ieee802154_interface>` 等。
在下一节中，我们将描述设备驱动在
接收或发送网络数据包时应有的行为。其余部分依赖硬件，
此处不再详述。

以太网设备驱动
======================

在接收时，由设备驱动负责向网络数据包中填入
所需数量的数据缓冲区。网络数据包本身是一个
:c:struct:`net_pkt`，应通过
:c:func:`net_pkt_rx_alloc_with_buffer` 分配。然后所有数据缓冲区都会
由 :c:func:`net_pkt_write` 自动分配并填充。

在所有网络数据接收完毕后，设备驱动需要
调用 :c:func:`net_recv_data`。如果该调用失败，则由
设备驱动负责通过 :c:func:`net_pkt_unref` 解除对缓冲区的引用。

在发送时，会调用设备驱动的发送函数，由
设备驱动负责一次性发送整个网络数据包（包含所有缓冲区）。

每个以太网设备驱动最终都需要像这样调用
``ETH_NET_DEVICE_INIT()``：

.. code-block:: c

   ETH_NET_DEVICE_INIT(..., CONFIG_ETH_INIT_PRIORITY,
                       &the_valid_net_if_api_instance, 1500);

IEEE 802.15.4 设备驱动
===========================

IEEE 802.15.4 L2 的设备驱动基本上与
以太网的工作方式相同。上面描述的内容，尤其是 ``recv()`` 部分，
同样适用。不过有两点特定差异：

- 它需要一个专用的设备驱动 API：:c:struct:`ieee802154_radio_api`，
  该结构重载了 :c:struct:`net_if_api`。这是因为 802.15.4 L2 需要从设备
  驱动获取的不仅仅是 ``send()`` 和 ``recv()`` 函数。该专用 API 声明在
  :zephyr_file:`include/zephyr/net/ieee802154_radio.h` 中。每一个
  IEEE 802.15.4 设备驱动都必须提供一个指向相应
  已填充的 API 结构体的有效指针。

- 发送数据包的方式与以太网略有不同。大多数 IEEE 802.15.4
  PHY 仅支持相对较小的帧，总共 127 字节：包括帧
  头、有效载荷和帧校验和。要通过无线电发送的缓冲区
  往往超出这一帧大小限制，例如包含 IPv6
  数据包的缓冲区通常必须拆分为若干分片，并且 IPv6 数据包头部
  和分片需要先使用 6LoWPAN 之类的协议进行压缩，
  然后才能传递给无线电驱动。此外，IEEE 802.15.4 标准定义了
  媒体访问（例如 CSMA/CA）、帧重传、加密以及其他预处理
  步骤（例如添加信息元素），这些
  单个无线电驱动无需关心。这就是为什么
  :c:struct:`ieee802154_radio_api` 要求一个 tx 函数指针，它不同于
  :c:struct:`net_if_api` 的 send 函数指针。Zephyr 的原生
  IEEE 802.15.4 L2 实现提供了一个通用的 :c:func:`ieee802154_send`
  函数，作为 :c:type:`net_if` 的 send 函数使用。:c:func:`ieee802154_send`
  的实现负责 IEEE 802.15.4 标准的数据包
  准备步骤：将数据包拆分为可能经过压缩、
  加密和其他预处理的分片缓冲区，通过 :c:struct:`ieee802154_radio_api`
  的 tx 函数一次发送一个缓冲区，并且只有当整个传输
  成功或失败时才解除对网络数据包的引用。

IEEE 802.15.4 无线电设备驱动与 L2 之间的交互是双向的：

- L2 -> L1：像 :c:func:`ieee802154_send` 以及若干 IEEE 802.15.4 网络
  管理调用这样的方法会调用驱动，例如通过
  无线电链路发送数据包或在运行时重新配置驱动。这些传入的调用
  都会由 :c:struct:`ieee802154_radio_api` 中的方法处理。

- L1 -> L2：有若干情况需要驱动
  发起对 L2/MAC 层的调用。在这些情况下，Zephyr 的 IEEE 802.15.4 L1 -> L2 适配 API
  采用"控制反转"（inversion-of-control）模式，以避免在
  相互独立的驱动实现中重复复杂的逻辑，并确保
  与实现无关的松耦合以及 MAC（L2）与 PHY（L1）之间干净的职责分离，
  无论何时需要反向信息传递或硬件与 L2 之间的紧密协作都是如此。例如在
  驱动初始化期间，驱动调用 :c:func:`ieee802154_init` 将接口的 MAC 地址
  以及其他与硬件相关的配置传递给 L2。类似地，驱动可以
  向 L2 指示性能或时序敏感的无线电事件（例如 :c:func:`ieee802154_handle_ack`），
  这些事件需要与硬件紧密集成。
  从 L1 到 L2 的调用不作为 :c:struct:`ieee802154_radio_api` 中的方法实现，
  而是作为独立的函数，并在
  :zephyr_file:`include/zephyr/net/ieee802154_radio.h` 中声明并作为此类函数进行文档说明。API 文档会
  明确说明哪些函数必须由所有 L2 栈作为
  L1 -> L2"控制反转"适配 API 的一部分实现。

注意：:zephyr_file:`include/zephyr/net/ieee802154_radio.h` 中
未明确文档为回调（callback）的独立函数，被视为
PHY（L1）层内部独立于任何特定 L2 栈实现的辅助函数，参见
:c:func:`ieee802154_is_ar_flag_set` 等。

和所有网络接口一样，IEEE 802.15.4 设备驱动实现最终都必须调用
``NET_DEVICE_INIT_INSTANCE()``：

.. code-block:: c

   NET_DEVICE_INIT_INSTANCE(...,
                           the_device_init_prio,
			   &the_valid_ieee802154_radio_api_instance,
			   IEEE802154_L2,
			   NET_L2_GET_CTX_TYPE(IEEE802154_L2), 125);

API 参考
*************

.. doxygengroup:: net_l2
