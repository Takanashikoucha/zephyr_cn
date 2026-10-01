.. _ttcn3_testing:

Protocol conformance testing with TTCN-3
########################################

.. contents::
    :local:
    :depth: 2

Zephyr 的 network protocols 从两个方向覆盖。:zephyr_file:`tests/net` 下的 tests 从内部（用 C（构建到相同 image 中）验证实现。用 TTCN-3 编写的 conformance suites 从外部入手：其通过真实 network interface 讲 protocol（并将 Zephyr 发送的与 standard 要求的对照检查。

两者捕获不同的东西。针对实现编写的 test 倾向编码实现所做的。针对 standard 编写的 suite 不知实现所做的（这正是要点。

TTCN-3 为 ETSI 标准化的用于编写 tests 的 language。此处的 suites 用 open source TTCN-3 compiler `Eclipse Titan`_ 编译（并与其他用于 network testing 的 host side tools 一起保存在 ``net-tools`` repository 的 :file:`ttcn3` 下。

.. toctree::
   :maxdepth: 1

   usage.rst
   architecture.rst

How it fits together
********************

Conformance test 的 Zephyr 侧仅为被测系统：普通 application（配置为启用被测试的 protocol。关于 test 的什么都不编译到其中（无 control channel（且 suite 完全通过网络驱动其。

这些 applications（以及对其运行 suite 的 harness）位于 :zephyr_file:`tests/net/conformance` 下。Twister 构建并启动 application（且小型 pytest harness 用 Titan 构建 suite（运行其（并将 Titan 的 verdict 转为 test result。

每个 test 在 Titan、第三方 TTCN-3 modules 或 network interface 缺失时跳过自身（故未为其设置的 run 中 suites 无害。run 所需参见 :ref:`ttcn3_running`（各部分如何组合参见 :ref:`ttcn3_architecture`。

.. _ttcn3_suites:

The suites
**********

Suite 使用哪个 interface（以及是否须以 root 运行）取决于其做什么：在 IP layer 以下工作的 suite 从自己 link 上的 packet socket 读取 frames。

.. list-table::
   :header-rows: 1

   * - Suite
     - System under test
     - Interface
     - Runs as
   * - :zephyr_file:`mdns <tests/net/conformance/mdns/README.rst>`
     - :zephyr_file:`tests/net/conformance/mdns`
     - ``zeth``
     - any user
   * - :zephyr_file:`dnssd <tests/net/conformance/dnssd/README.rst>`
     - :zephyr_file:`tests/net/conformance/dnssd`
     - ``zeth``
     - any user
   * - :zephyr_file:`dns <tests/net/conformance/dns/README.rst>`
     - :zephyr_file:`tests/net/conformance/dns`
     - ``zeth``
     - any user
   * - :zephyr_file:`sntp <tests/net/conformance/sntp/README.rst>`
     - :zephyr_file:`tests/net/conformance/sntp`
     - ``zeth``
     - any user
   * - :zephyr_file:`mqtt <tests/net/conformance/mqtt/README.rst>`
     - :zephyr_file:`tests/net/conformance/mqtt`
     - ``zeth``
     - any user
   * - :zephyr_file:`coap <tests/net/conformance/coap/README.rst>`
     - :zephyr_file:`tests/net/conformance/coap`
     - ``zeth``
     - any user
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

添加 suite 在 :ref:`ttcn3_adding_a_suite` 中描述。

.. _ttcn3_known_gaps:

Known gaps
**********

Suite 断言与 standard 不符的行为时（其在断言处说明（使 divergence 被记录而非无声冻结。以下是另一类 gap：尚无 suite 覆盖的领域。

DNS-SD legacy unicast queries
=============================

mDNS responder 的 hostname 侧按 :rfc:`6762` section 6.7 要求回答 legacy unicast query。Service discovery 侧不：其构建自己的 messages（为属于一个 instance 的 records 设置 cache flush bit（使用本用于 multicast answer 的 lifetimes（且既不 echo identifier 也不 echo question。修复意味着重新计算全部从固定 header size 计算的 name compression offsets。

``dnssd`` suite 在 ``f_check_legacy_shape`` 中记录而非断言 standard（使 test 不会一直失败直到有人处理。那里的每个 check 说明须随之改变什么。

MQTT 5.0, packet identifiers and re-sending
===========================================

``mqtt`` suite 覆盖 MQTT 3.1.1。Zephyr 也实现 MQTT 5.0（:kconfig:option:`CONFIG_MQTT_VERSION_5_0`）（且 Titan project 未为其发布 protocol module（故覆盖意味着在编写任何 test 前编写 message types。

Packet identifiers 和 re-sending 也未覆盖。Zephyr 的 client 将两者留给 application：:c:func:`mqtt_publish` 发送其收到的 identifier 和 duplicate flag（故任一 test 将测试被测系统自己的 counter 而非 client。

Overlapping DNS queries
=======================

Resolver 在向无未决事项的 server 发送前更新其 source port（默认每次一个 query 意味着每个 query。在一个 server 上重叠的 queries 仍共享 port（故 ``dns`` suite 中的 check 在此情况不会捕获 regression。参见 :rfc:`5452` section 9.2。

Continuous integration
**********************

这些 suites 不是普通 Twister run 的一部分：其需 Titan 安装（面向 device 的 network interface（以及 suites 的 checkout（普通 build 均无。其也慢（且不能同时运行彼此。

其改为夜间运行（来自 :zephyr_file:`.github/workflows/net_conformance.yml`（其也可从 Actions tab 手动启动。Job 安装打包的 Titan（设置 ``TTCN3_DIR=/usr``（在持有 ``NET_ADMIN`` 的容器中启动两个 interfaces（并以 root 运行整个 directory 使无 suite 被跳过。Twister report 和 harness logs 作为 artifacts 保留。

Other TTCN-3 suites
*******************

Eclipse Titan project 为大量 protocols 发布 protocol modules 和 test ports（作为 `gitlab.eclipse.org/eclipse/titan`_ 下的单独 repositories。此处的 suites 针对其构建（而非定义自己的 message formats。

那里也存在某些完整 suites。``titan.misc`` 包含可对 :zephyr:code-sample:`coap-server` sample 运行的 CoAP conformance suite；该 suite 参见 :ref:`coap_sock_interface`。

Intel 为 TCP rewrite 编写的较旧 TCP TTCN-3 suite 影响了 ``tcp`` suite 覆盖的内容（但其代码均未使用。其通过 JSON control channel 驱动 Zephyr（并断言 stack 的内部 state names（且该 channel 所需的 option 已移除；参见 4.5 migration guide。

.. _Eclipse Titan: https://projects.eclipse.org/projects/tools.titan
.. _gitlab.eclipse.org/eclipse/titan: https://gitlab.eclipse.org/eclipse/titan
