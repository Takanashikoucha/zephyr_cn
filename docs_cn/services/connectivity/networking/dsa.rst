.. _dsa:

分布式交换架构（DSA）
#####################################

.. contents::
    :local:
    :depth: 2

分布式交换架构（DSA）并非新事物。多年来它一直是
Linux 中成熟的子系统。本文档只是跳过背景、
术语和任何知识相关描述，用户可以在
`Linux DSA 文档`_ 中找到所有这些。


DSA 交换机 TX/RX 流程
************************

DSA 交换机 TX/RX 流程如下。

.. image:: dsa_txrx_process.svg

主机接口
**************

主机接口网络设备使用常规且未修改的以太网驱动程序
作为 DSA 导管端口工作，通过处理器管理交换机。

交换机接口
****************

交换机接口也在 zephyr 中暴露为标准以太网接口。
连接到导管端口的作为 CPU 端口工作，其余用于
用户目的的作为用户端口工作。

交换机标记协议
************************

通常，交换机标记协议是厂商特定的。它们都包含某物：

- 标识以太网帧来自/应发往哪个端口
- 提供此帧为何被转发到管理接口的理由

并在数据包上添加标签以赋予其交换机帧头。但也有无标签情况。
取决于厂商。

网络栈流程
************************

为使 DSA 子系统通过导管端口处理以太网交换机特定的标记协议。

对于 RX 路径，在 ``subsys/net/ip/net_core.c`` 的 ``net_recv_data()`` 开头
放置 ``dsa_recv()`` 以首先处理去除标签和重定向接口。

对于 TX 路径，交换机接口注册为标准以太网设备，
``ethernet_api->send`` 为 ``dsa_xmit()``。``dsa_xmit()`` 处理
标记和重定向到导管端口的工作。

DSA 设备驱动支持
*************************

由于 DSA 核心驱动程序与包括 MDIO、PHY 和设备树在内的
子系统/驱动程序交互以支持通用 DSA 设置和工作流程，
设备驱动支持容易得多。

对于设备树，交换机描述应遵循 ``dts/bindings/dsa/dsa.yaml``。

对于设备驱动，所有须准备的为 :c:struct:`dsa_api`、
私有数据（若有的）以及 :c:struct:`dsa_port_config`。
宏函数可以利用。以下为 i.MX NETC 示例。

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

使用 DSA 设置的常见陷阱
********************************

此从 Linux DSA 文档复制。也适用于 zephyr。尽管 zephyr 中
导管端口和 CPU 端口暴露为以太网设备，它们无法被使用。

.. note::

  一旦导管网络设备配置为使用 DSA（dev->dsa_ptr 变为非-NULL），
  且其后交换机期望标记协议，此网络接口仅可专属用作
  导管接口。直接通过此接口发送数据包（例如：用此接口
  打开套接字）不会使其通过交换机标记协议的传输函数，
  因此另一端的以太网交换机，期望标签通常会丢弃此帧。

待办工作
*********

与 Linux 相比，zephyr DSA 中/基于其须支持的功能太多。
但基本上桥接层应被支持。然后 DSA 可为用户
提供两个选项使用交换机端口。

- 独立模式：所有用户端口作为常规以太网设备工作。无交换。
- 桥接模式：启用交换模式，将用户端口添加到虚拟桥接设备。
  IP 地址可分配给桥接。

.. _Linux DSA 文档:
   https://www.kernel.org/doc/html/latest/networking/dsa/dsa.html
