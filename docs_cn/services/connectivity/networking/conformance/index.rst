.. _ttcn3_testing:

使用 TTCN-3 进行协议一致性测试
########################################

.. contents::
    :local:
    :depth: 2

Zephyr 的网络协议从两个方向覆盖。:zephyr_file:`tests/net` 下的测试
从内部用 C 验证实现，编译到同一个映像中。用 TTCN-3 编写的一致性
测试套件从外部入手：它们通过真实网络接口讲协议，并将
Zephyr 发送的内容与标准要求对照检查。

两者捕获不同的东西。针对实现编写的测试
倾向于编码实现所做的。针对标准编写的测试套件
不知道实现所做的，这正是要点。

TTCN-3 是 ETSI 标准化的用于编写测试的语言。此处的测试套件
用开源 TTCN-3 编译器 `Eclipse Titan`_ 编译，
与其他用于网络测试的主机侧工具一起保存在 ``net-tools`` 仓库的 :file:`ttcn3` 下。

.. toctree::
   :maxdepth: 1

   usage.rst
   architecture.rst

如何组合
********************

一致性测试的 Zephyr 侧只是被测系统：一个
普通应用程序，配置为启用被测试的协议。关于
测试的任何内容都没有编译到其中，没有控制通道，测试套件
完全通过网络驱动它。

这些应用程序以及对其运行测试套件的测试框架
位于 :zephyr_file:`tests/net/conformance` 下。Twister 构建并启动
应用程序，小型 pytest 测试框架用 Titan 构建测试套件，运行它，
并将 Titan 的判决转化为测试结果。

当 Titan、第三方 TTCN-3 模块或
网络接口缺失时，每个测试跳过自身，因此在
未为其设置的运行中测试套件是无害的。运行所需参见 :ref:`ttcn3_running`，
各部分如何组合参见 :ref:`ttcn3_architecture`。

.. _ttcn3_suites:

测试套件
**********

测试套件使用哪个接口，以及是否必须作为 root 运行，取决于
它做什么：在 IP 层以下工作的测试套件从
其自己链路上的数据包套接字读取帧。

.. list-table::
   :header-rows: 1

   * - 测试套件
     - 被测系统
     - 接口
     - 运行身份
   * - :zephyr_file:`mdns <tests/net/conformance/mdns/README.rst>`
     - :zephyr_file:`tests/net/conformance/mdns`
     - ``zeth``
     - 任何用户
   * - :zephyr_file:`dnssd <tests/net/conformance/dnssd/README.rst>`
     - :zephyr_file:`tests/net/conformance/dnssd`
     - ``zeth``
     - 任何用户
   * - :zephyr_file:`dns <tests/net/conformance/dns/README.rst>`
     - :zephyr_file:`tests/net/conformance/dns`
     - ``zeth``
     - 任何用户
   * - :zephyr_file:`sntp <tests/net/conformance/sntp/README.rst>`
     - :zephyr_file:`tests/net/conformance/sntp`
     - ``zeth``
     - 任何用户
   * - :zephyr_file:`mqtt <tests/net/conformance/mqtt/README.rst>`
     - :zephyr_file:`tests/net/conformance/mqtt`
     - ``zeth``
     - 任何用户
   * - :zephyr_file:`coap <tests/net/conformance/coap/README.rst>`
     - :zephyr_file:`tests/net/conformance/coap`
     - ``zeth``
     - 任何用户
   * - :zephyr_file:`dhcpv4 <tests/net/conformance/dhcpv4/README.rst>`
     - :zephyr_file:`tests/net/conformance/dhcpv4`
     - ``zeth``
     - root
   * - :zephyr_file:`dhcpv4_server <tests/net/conformance/dhcpv4_server/README.rst>`
     - :zephyr_file:`tests/net/conformance/dhcpv4_server`
     - ``zeth``
     - root
   * - :zephyr_file:`arp <tests/net/conformance/arp/README.rst>`
     - :zephyr_file:`tests/net/conformance/arp`
     - ``zethL2``
     - root
   * - :zephyr_file:`ndp <tests/net/conformance/ndp/README.rst>`
     - :zephyr_file:`tests/net/conformance/ndp`
     - ``zethL2``
     - root
   * - :zephyr_file:`tcp <tests/net/conformance/tcp/README.rst>`
     - :zephyr_file:`tests/net/conformance/tcp`
     - ``zethL2``
     - root

添加测试套件在 :ref:`ttcn3_adding_a_suite` 中描述。

.. _ttcn3_known_gaps:

已知差距
**********

当测试套件断言与标准不符的行为时，它在断言
处说明，因此偏差被记录而不是静默固化。
以下是另一类差距：尚无测试套件覆盖的领域。

DNS-SD 传统单播查询
=============================

mDNS 响应器的主机名侧按 :rfc:`6762` 第 6.7 节要求回答传统单播查询。服务发现侧不回答：它构建
自己的消息，为属于一个
实例的记录设置缓存刷新位，使用本用于多播应答的生存时间，
并且既不回显标识符也不回显问题。修复意味着重新计算
全部从固定头部大小计算的名压缩偏移量。

``dnssd`` 测试套件在 ``f_check_legacy_shape`` 中记录而不是断言标准，
使测试不会一直失败直到有人处理。那里的每个检查
说明必须随之改变什么。

MQTT 5.0、数据包标识符和重发
===========================================

``mqtt`` 测试套件覆盖 MQTT 3.1.1。Zephyr 也实现 MQTT 5.0
（:kconfig:option:`CONFIG_MQTT_VERSION_5_0`），Titan 项目未为其
发布协议模块，因此覆盖意味着在编写任何测试前
编写消息类型。

数据包标识符和重发也未覆盖。Zephyr 的客户端
将两者留给应用程序：:c:func:`mqtt_publish` 发送其收到的标识符
和重复标志，因此任一测试将测试被测系统
自己的计数器而不是客户端。

重叠的 DNS 查询
=======================

解析器在向没有未决事项的服务器发送前更新其源端口，
默认每次一个查询意味着每个查询。
在一个服务器上重叠的查询仍共享端口，因此
``dns`` 测试套件中的检查在此情况不会捕获回归。参见 :rfc:`5452`
第 9.2 节。

持续集成
**********************

这些测试套件不是普通 Twister 运行的一部分：它们需要 Titan
安装、面向设备的网络接口，以及
测试套件的 checkout，普通构建都没有。它们也很慢，
并且不能同时运行彼此。

它们改为夜间运行，来自
:zephyr_file:`.github/workflows/net_conformance.yml`，也可以从 Actions 标签页手动启动。任务安装打包的 Titan 并
设置 ``TTCN3_DIR=/usr``，在持有
``NET_ADMIN`` 的容器中启动两个接口，并作为 root 运行整个目录，
使没有测试套件被跳过。Twister 报告和测试框架日志
作为 artifacts 保留。

其他 TTCN-3 测试套件
*******************

Eclipse Titan 项目为大量协议发布协议模块和测试端口，
作为 `gitlab.eclipse.org/eclipse/titan`_ 下的单独仓库。此处的测试套件
针对其构建，而不是定义自己的消息格式。

那里也存在某些完整测试套件。``titan.misc`` 包含一个
可以对 :zephyr:code-sample:`coap-server` 示例运行的 CoAP 一致性
测试套件；该测试套件参见 :ref:`coap_sock_interface`。

Intel 为 TCP 重写编写的较旧 TCP TTCN-3 测试套件
影响了 ``tcp`` 测试套件覆盖的内容，但其代码均未使用。
它通过 JSON 控制通道驱动 Zephyr，并断言协议栈
的内部状态名称，且该通道所需的选项已移除；
参见 4.5 迁移指南。

.. _Eclipse Titan: https://projects.eclipse.org/projects/tools.titan
.. _gitlab.eclipse.org/eclipse/titan: https://gitlab.eclipse.org/eclipse/titan
