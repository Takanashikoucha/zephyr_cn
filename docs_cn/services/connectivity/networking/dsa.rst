.. _dsa:

Distributed Switch Architecture (DSA)
#####################################

.. contents::
    :local:
    :depth: 2

Distributed Switch Architecture (DSA) 并非新事物。其多年来一直是 Linux 中成熟的 subsystem。此文档跳过 background、terms 及任何 knowledge 相关描述（用户可在 `Linux DSA documentation`_ 中找到所有这些。

DSA switch TX/RX process
************************

DSA switch TX/RX process 如下。

.. image:: dsa_txrx_process.svg

Host interface
**************

Host interface network devices 使用常规且未修改的 ethernet driver 作为 DSA conduit port 工作（其通过 processor 管理 switch。

Switch interface
****************

Switch interfaces 也在 zephyr 中暴露为标准 ethernet interfaces。连接到 conduit port 的作为 CPU port 工作（其余用于 user purpose 的作为 user ports 工作。

Switch tagging protocols
************************

通常（switch tagging protocols 为 vendor specific。其均包含某物：

- 标识 Ethernet frame 来自/应发往哪个 port
- 提供此 frame 为何被转发到 management interface 的理由

并在 packets 上添加 tag 以赋予其 switch frame header。但也有 tag-less 情况。取决于 vendor。

Networking stack process
************************

为使 DSA subsystem 通过 conduit port 处理 Ethernet switch 特定的 tagging protocol。

对 RX path（在 ``subsys/net/ip/net_core.c`` 的 ``net_recv_data()`` 开头放置 ``dsa_recv()`` 以首先处理 untagging 和 re-directing interface。

对 TX path（switch interfaces 注册为标准 ethernet devices（``ethernet_api->send`` 为 ``dsa_xmit()``。``dsa_xmit()`` 处理 tagging 和 re-directing 到 conduit port 的工作。

DSA device driver support
*************************

由于 DSA core driver 与包括 MDIO、PHY 和 device tree 在内的 subsystems/drivers 交互以支持通用 DSA setup 和 working process（device driver support 容易得多。

对 device tree（switch 描述应遵循 ``dts/bindings/dsa/dsa.yaml``。

对 device driver（所有须准备的为 :c:struct:`dsa_api`（若有的 private data（以及 :c:struct:`dsa_port_config`。Macro functions 可利用。以下为 i.MX NETC 示例。

- :c:macro:`DSA_SWITCH_INST_INIT`
- :c:macro:`DSA_PORT_INST_INIT`

.. code-block:: c

   #define DSA_NETC_PORT_INST_INIT(port, n)                                                    \
           COND_CODE_1(DT_NUM_PINCTRL_STATES(port),                                            \
                           (PINCTRL_DT_DEFINE(port);), (EMPTY))                                \
           struct dsa_netc_port_config dsa_netc_##n##_##port##_config = {                      \
                   .pincfg = COND_CODE_1(DT_NUM_PINCTRL_STATES(port),                          \
                                   (PINCTRL_DT_DEV_CONFIG_GET(port)), NULL),                   \
                   .phy_mode = NETC_PHY_MODE(port),                                            \
           };                                                                                  \
           struct dsa_port_config dsa_##n##_##port##_config = {                                \
                   .mcfg = NET_ETH_MAC_DT_CONFIG_INIT(port),                                   \
                   .port_idx = DT_REG_ADDR(port),                                              \
                   .phy_dev = DEVICE_DT_GET_OR_NULL(DT_PHANDLE(port, phy_handle)),             \
                   .phy_mode = DT_PROP_OR(port, phy_connection_type, ""),                      \
                   .ethernet_connection = DEVICE_DT_GET_OR_NULL(DT_PHHANDLE(port, ethernet)),   \
                   .prv_config = &dsa_netc_##n##_##port##_config,                              \
           };                                                                                  \
           DSA_PORT_INST_INIT(port, n, &dsa_##n##_##port##_config)

   #define DSA_NETC_DEVICE(n)                                                                  \
           AT_NONCACHEABLE_SECTION_ALIGN(static netc_cmd_bd_t dsa_netc_##n##_cmd_bd[8],        \
                                         NETC_BD_ALIGN);                                       \
           static struct dsa_netc_data dsa_netc_data_##n = {                                   \
                   .cmd_bd = dsa_netc_##n##_cmd_bd,                                            \
           };                                                                                  \
           DSA_SWITCH_INST_INIT(n, &dsa_netc_api, &dsa_netc_data_##n, DSA_NETC_PORT_INST_INIT);

Common pitfalls using DSA setups
********************************

此从 Linux DSA documentation 复制。也适用于 zephyr。尽管 zephyr 中 conduit port 和 cpu port 暴露为 ethernet device（其无法被使用。

.. note::

  一旦 conduit network device 配置为使用 DSA（dev->dsa_ptr 变为非-NULL）（且其后 switch 期望 tagging protocol（此 network interface 仅可专属用作 conduit interface。直接通过此 interface 发送 packets（例如：用此 interface 打开 socket）不会使其通过 switch tagging protocol 的 transmit function（故另一端的 Ethernet switch（期望 tag 通常会丢弃此 frame。

TODO work
*********

与 Linux 相比（zephyr DSA 中/基于其须支持的 features 太多。但基本上 bridge layer 应被支持。然后 DSA 可为 users 提供两个 options 使用 switch ports。

- Standalone mode：所有 user ports 作为常规 ethernet devices 工作。无 switching。
- Bridge mode：启用 switch mode（将 user ports 添加到虚拟 bridge device。IP address 可分配给 bridge。

.. _Linux DSA documentation:
   https://www.kernel.org/doc/html/latest/networking/dsa/dsa.html
