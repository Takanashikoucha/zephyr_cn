.. _net_l2_interface:

L2 Layer Management
###################

.. contents::
    :local:
    :depth: 2

Overview
********

L2 stack 设计为向 network stack 上层隐藏整个 networking link-layer 部分和相关 device drivers。这通过 :zephyr_file:`include/zephyr/net/net_if.h` 中声明的 :c:struct:`net_if` 实现。

Upper layers 除 net_if 对象和 :zephyr_file:`include/zephyr/net/net_l2.h` 中 L2 layer 提供的 :c:struct:`net_l2` 的 generic API 外（不了解实现细节。

仅 L2 layer 可与链接到 net_if 对象的 device driver 通信。L2 layer 规定 device driver 提供的 API（特定于该 device（并针对协同工作优化。

当前（有 :ref:`Ethernet <ethernet_interface>`、:ref:`IEEE 802.15.4 Soft-MAC <ieee802154_interface>`、:ref:`CANBUS <can_api>`、:ref:`OpenThread <thread_protocol_interface>`、Wi-Fi 的 L2 layers（以及可用作编写新 L2 layer 模板的 dummy layer 示例。

L2 layer API
************

要创建 L2 layer 或特定 L2 layer 的 driver（须理解 L3 layer 如何与其交互（以及 L2 layer 应如何行为。更多细节参见 :ref:`network stack architecture <network_stack_architecture>`。Generic L2 API 有以下 functions：

- ``recv()``：所有 device drivers 一旦收到其放入 :c:struct:`net_pkt` 的 packet（将通过 :c:func:`net_recv_data` 将此 buffer 推上 network stack。此时（network stack 不知如何处理。相反（其将 buffer 传递给 L2 stack 的 ``recv()`` function 处理。L2 stack 对 packet 做其需做的（例如解析 link layer header（或处理仅 link-layer 的 packets。``recv()`` function 在 error packet 时返回 ``NET_DROP``（packet 被 L2 完全消费时返回 ``NET_OK``（network stack 应随后处理时返回 ``NET_CONTINUE``。

- ``send()``：类似 receive function（network stack 调用此 function 以实际发送 network packet。所有相关 link-layer content 由此 function 生成并添加。``send()`` function 返回发送的 bytes 数（发送 network packet 失败时返回负 error code。

- ``enable()``：此 function 用于启用/禁用 network interface 上的 traffic。Function 错误时返回 ``<0``（无错误时返回 ``>=0``。

- ``get_flags()``：此 function 返回 L2 driver 的 capabilities（例如 L2 是否支持 multicast 或 promiscuous mode。

Network Device drivers
**********************

Network device drivers 完全以 Zephyr device driver model 为基础。参见 :ref:`device_model_api`。

然而（有两点不同：

- Driver_api pointer 须指向有效的 :c:struct:`net_if_api` pointer。

- Network device driver 须用 :c:macro:`NET_DEVICE_INIT_INSTANCE()` 或 Ethernet devices 的 :c:macro:`ETH_NET_DEVICE_INIT()`。这些 macros 调用 :c:macro:`DEVICE_DEFINE()` macro（并为创建的 device driver 实例实例化唯一的 :c:struct:`net_if`。

实现 network device driver 取决于其所属的 L2 stack：:ref:`Ethernet <ethernet_interface>`、:ref:`IEEE 802.15.4 <ieee802154_interface>` 等。下一节描述 device driver 在接收或发送 network packet 时应如何行为。其余为 hardware 相关（此处不详细。

Ethernet device driver
======================

接收时（由 device driver 决定用多少 data buffers 填充 network packet。Network packet 本身为 :c:struct:`net_pkt`（应通过 :c:func:`net_pkt_rx_alloc_with_buffer` 分配。然后所有 data buffers 由 :c:func:`net_pkt_write` 自动分配并填充。

收到所有 network data 后（device driver 需调用 :c:func:`net_recv_data`。若该调用失败（由 device driver 负责通过 :c:func:`net_pkt_unref` 取消 buffer 的引用。

发送时（device driver 的 send function 被调用（且由 device driver 决定一次性发送带所有 buffers 的 network packet。

每个 Ethernet device driver 最终须调用 ``ETH_NET_DEVICE_INIT()``（如下：

.. code-block:: c

   ETH_NET_DEVICE_INIT(..., CONFIG_ETH_INIT_PRIORITY,
                       &the_valid_net_if_api_instance, 1500);

IEEE 802.15.4 device driver
===========================

IEEE 802.15.4 L2 的 device drivers 基本与 Ethernet 的工作方式相同。上述描述的（尤其对 ``recv()``）此处同样适用。然而有两点特定不同：

- 其需要专用 device driver API：:c:struct:`ieee802154_radio_api`（其重载 :c:struct:`net_if_api`。这是因为 802.15.4 L2 需要从 device driver 获得比 ``send()`` 和 ``recv()`` functions 更多的内容。此专用 API 在 :zephyr_file:`include/zephyr/net/ieee802154_radio.h` 中声明。每个 IEEE 802.15.4 device driver 须提供指向如此适当填充的 API structure 的有效 pointer。

- 发送 packet 与 Ethernet 略有不同。大多数 IEEE 802.15.4 PHYs 仅支持相对小的 frames（127 bytes 全包：frame header、payload 和 frame checksum。要通过 radio 发送的 buffers 通常不符合此 frame size 限制（例如包含 IPv6 packet 的 buffer 通常须拆分为多个 fragments（且 IP6 packet headers 和 fragments 在传递给 radio driver 前须用 6LoWPAN 等 protocol 压缩。此外（IEEE 802.15.4 standard 定义 medium access（如 CSMA/CA）、frame retransmission、encryption 和其他 pre-processing procedures（如添加 information elements）（单个 radio drivers 不应关心。这就是 :c:struct:`ieee802154_radio_api` 要求与 :c:struct:`net_if_api` send function pointer 不同的 tx function pointer 的原因。Zephyr 的 native IEEE 802.15.4 L2 实现提供通用的 :c:func:`ieee802154_send`（意在作为 :c:type:`net_if` send function 给出。:c:func:`ieee802154_send` 的实现处理 IEEE 802.15.4 standard packet 准备 procedures（将 packet 拆分为可能的 compressed、encrypted 和其他 pre-processed fragment buffers（一次通过 :c:struct:`ieee802154_radio_api` tx function 发送一个 buffer（且仅当整个传输成功或失败时取消 network packet 的引用。

IEEE 802.15.4 radio device drivers 与 L2 之间的交互为双向：

- L2 -> L1：:c:func:`ieee802154_send` 等方法以及若干 IEEE 802.15.4 net management calls 调用 driver（例如通过 radio link 发送 packet 或在 runtime 重新配置 driver。这些 incoming calls 均由 :c:struct:`ieee802154_radio_api` 中的 methods 处理。

- L1 -> L2：driver 需发起调用到 L2/MAC layer 的若干情况。Zephyr 的 IEEE 802.15.4 L1 -> L2 adaptation API 在此类情况下采用 "inversion-of-control" pattern（避免跨独立 driver 实现重复复杂 logic（并确保实现无关的 loose coupling（以及需要反向 information 传输或 hardware 与 L2 紧密协同时 MAC（L2）和 PHY（L1）之间干净的 separation of concerns。例如（driver 初始化期间（driver 调用 :c:func:`ieee802154_init` 以将 interface 的 MAC address 以及其他 hardware 相关 configuration 传递给 L2。类似地（drivers 可向 L2 指示需要与 hardware 紧密集成的 performance 或 timing critical radio events（如 :c:func:`ieee802154_handle_ack`。L1 到 L2 的调用不作为 :c:struct:`ieee802154_radio_api` 中的 methods 实现（而是作为 :zephyr_file:`include/zephyr/net/ieee802154_radio.h` 中如此声明并文档化的 standalone functions。API 文档将明确声明哪些 functions 须由所有 L2 stacks 作为 L1 -> L2 "inversion-of-control" adaptation API 的一部分实现。

注意：:zephyr_file:`include/zephyr/net/ieee802154_radio.h` 中未明确文档化为 callbacks 的 standalone functions 视为 PHY（L1）layer 中独立于任何特定 L2 stack 实现的 helper functions（例如 :c:func:`ieee802154_is_ar_flag_set`。

与所有 net interfaces 一样（IEEE 802.15.4 device driver 实现最终须调用 ``NET_DEVICE_INIT_INSTANCE()``：

.. code-block:: c

   NET_DEVICE_INIT_INSTANCE(...,
                            the_device_init_prio,
			    &the_valid_ieee802154_radio_api_instance,
			    IEEE802154_L2,
			    NET_L2_GET_CTX_TYPE(IEEE802154_L2), 125);

API Reference
*************

.. doxygengroup:: net_l2
