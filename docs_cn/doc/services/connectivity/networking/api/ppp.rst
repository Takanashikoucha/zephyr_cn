.. _ppp:

Point-to-Point Protocol (PPP) 支持
#####################################

.. contents::
    :local:
    :depth: 2

概述
********

`点对点协议
<https://en.wikipedia.org/wiki/Point-to-Point_Protocol>`_（PPP，Point-to-Point Protocol）是一种数据链路层（第 2 层）通信协议，用于在两个节点之间建立直接连接。由于 IP 数据包无法自行通过调制解调器线路传输，必须借助某种数据链路协议，因此 PPP 被用于多种类型的串行链路。

在 Zephyr 中，每条独立的 PPP 链路都被建模为一个网络接口。这与 Linux 实现 PPP 的方式类似。

PPP 支持必须在编译时通过设置 :kconfig:option:`CONFIG_NET_L2_PPP` 选项来启用。
PPP 实现仅支持以下协议：

* LCP（链路控制协议，
  :rfc:`1661`）
* HDLC（高级数据链路控制，
  :rfc:`1662`）
* IPCP（IP 控制协议，
  :rfc:`1332`）
* IPV6CP（IPv6 控制协议，
  :rfc:`5072`）

关于使用蜂窝调制解调器配合 PPP，请参见 :zephyr:code-sample:`cellular-modem` 示例
以获取更多信息。

测试
*******

有关如何在 Linux 上运行 pppd 来测试 Zephyr PPP 的更多细节，请参见 `net-tools README`_ 文件。

.. _net-tools README:
   https://github.com/zephyrproject-rtos/net-tools/blob/master/README.md#ppp-connectivity
