.. _ppp:

Point-to-Point Protocol (PPP) Support
#####################################

.. contents::
    :local:
    :depth: 2

Overview
********

`Point-to-Point Protocol
<https://en.wikipedia.org/wiki/Point-to-Point_Protocol>`_（PPP）是用于在两个 nodes 之间建立直接连接的 data link layer（layer 2）communications protocol。由于 IP packets 无法仅通过 modem line 传输（无某些 data link protocol）（PPP 用于许多类型的 serial links。

在 Zephyr 中（每个独立 PPP link 建模为 network interface。这与 Linux 实现 PPP 的方式类似。

PPP 支持须通过设置 :kconfig:option:`CONFIG_NET_L2_PPP` option 在 compile time 启用。PPP 实现仅支持以下 protocols：

* LCP（Link Control Protocol（
  :rfc:`1661`）
* HDLC（High-level data link control（
  :rfc:`1662`）
* IPCP（IP Control Protocol（
  :rfc:`1332`）
* IPV6CP（IPv6 Control Protocol（
  :rfc:`5072`）

关于用 cellular modem 使用 PPP（参见 :zephyr:code-sample:`cellular-modem` sample 以获取额外信息。

Testing
*******

如何测试 Zephyr PPP 对 Linux 中运行的 pppd 的更多细节参见 `net-tools README`_ file。

.. _net-tools README:
   https://github.com/zephyrproject-rtos/net-tools/blob/master/README.md#ppp-connectivity
