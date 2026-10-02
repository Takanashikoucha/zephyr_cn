.. _ttcn3_architecture:

一致性测试如何组织
##########################################

.. contents::
    :local:
    :depth: 2

有四个组成部分，分布在两个仓库中，它们只
在线路上相遇：一个 Zephyr 应用程序、一个 Twister 和 pytest 测试框架、一个
Eclipse Titan 的 shell 包装器，以及 TTCN-3 测试套件本身。

组成部分
**********

.. graphviz::
   :caption: 什么构建什么，以及两半在哪里相遇
   :alt: 显示 Twister 和 pytest 测试框架驱动 Zephyr
       应用程序和 Titan 构建的 TTCN-3 测试套件，它们只在
       tap 接口处相遇的图表。

   digraph ttcn3_pieces {
       rankdir=TB;
       node [shape=box, style=filled, fillcolor="#e8e8e8", fontname="sans-serif"];
       edge [arrowsize=0.8];

       twister [label="Twister", fillcolor="#cce5ff"];
       harness [label="pytest harness\n(ttcn3_runner.py)", fillcolor="#cce5ff"];

       subgraph cluster_zephyr {
           label="zephyr";
           style=dashed;
           fontname="sans-serif";
           sut [label="System under test\n(native_sim)"];
       }

       subgraph cluster_nettools {
           label="net-tools";
           style=dashed;
           fontname="sans-serif";
           build [label="build.sh\n+ Eclipse Titan"];
           suite [label="TTCN-3 suite\nexecutable"];
       }

       tap [label="zeth / zethL2\ntap interface", shape=ellipse, fillcolor="#ffe0b2"];

       twister -> harness [label="harness: pytest"];
       harness -> sut [label="start, read ready line"];
       harness -> build [label="build"];
       build -> suite;
       harness -> suite [label="run, read verdict"];
       sut -> tap [dir=both, label="the protocol"];
       suite -> tap [dir=both];
   }

Twister
    构建被测系统，启动它，并对它运行 pytest 测试框架。
    它提供测试标识符、平台限制和整个流程的 900 秒预算。

pytest 测试框架
    :zephyr_file:`tests/net/conformance/ttcn3_runner.py`，由所有
    测试共享。它决定测试套件是否可以运行，获取接口
    锁，构建测试套件，运行它并读取判决。

被测系统
    一个启用了协议的普通 Zephyr 应用程序。关于
    测试的任何内容都没有编译到其中。

build.sh 和 Eclipse Titan
    主机侧构建。Titan 将 TTCN-3 编译为 C++ 并生成 makefile；
    :file:`build.sh` 安排源代码以便它可以构建。

TTCN-3 测试套件可执行文件
    测试本身，从外部驱动协议。

Tap 接口
    两半共享的唯一事物。没有控制通道，没有共享
    内存，Zephyr 映像中也没有测试钩子。

Zephyr 侧
***************

被测系统
=====================

每个应用程序都刻意保持普通：启用协议，做
任何保持流量流动的事情（测试套件需要观察），并打印一个独特的
就绪行。该行是应用程序和
测试框架之间唯一的契约 —— 这是测试框架在测试套件开始
发送之前知道协议栈已启动的方式。

测试套件目录包含：

.. code-block:: none

   tests/net/conformance/<suite>/
       CMakeLists.txt
       prj.conf
       README.rst
       tests.yaml
       src/main.c
       pytest/pytest.ini
       pytest/conftest.py
       pytest/test_<suite>_conformance.py

Twister 集成
===================

每个 :file:`tests.yaml` 共享相同的代码块：

.. code-block:: yaml

   common:
     harness: pytest
     slow: true
     timeout: 900
     platform_allow:
       - native_sim
     integration_platforms:
       - native_sim

``harness: pytest`` 将运行交给测试框架，而不是读取控制台
输出以获取 ztest 摘要。``slow: true`` 将测试套件排除在普通
Twister 运行之外，因为完整通过需要几十分钟。900 秒超时
必须覆盖构建测试套件和运行测试套件。``native_sim`` 是
唯一平台，因为 tap 驱动程序将测试系统放在
真实链路上。

测试本身是三行：请求锁，等待就绪行，运行
测试套件。

.. code-block:: python

   def test_mdns_conformance(network_lock, dut, suite_binary):
       dut.readlines_until(regex='mDNS responder ready', timeout=30.0)
       run_suite(suite_binary, SUITE)

``network_lock`` 参数故意放在第一位；见下文。
:file:`conftest.py` 在每个测试目录中相同，只做一件事：
将共享运行器放到 ``sys.path`` 上并重新导出锁 fixture。

.. _ttcn3_runner:

测试框架
***********

.. mermaid::
   :caption: 一个一致性测试，从锁到判决
   :alt: 序列图显示测试框架在
       启动测试系统之前获取接口锁，然后构建和运行测试套件，
       在释放锁之前解析其判决。

   sequenceDiagram
       participant T as Twister
       participant H as Harness<br/>(ttcn3_runner.py)
       participant Z as System under test
       participant B as build.sh + Titan
       participant S as TTCN-3 suite

       T->>H: start test (900 s budget)
       H->>H: flock(LOCK_EX) on the interface
       Note over H,Z: the lock is taken before the DUT fixture,<br/>so nothing starts while another test runs
       H->>Z: start
       Z-->>H: ready line (30 s)
       H->>B: build the suite (1800 s)
       B-->>H: executable
       H->>S: run against the running application (600 s)
       S-->>H: verdict statistics, overall verdict
       H->>H: release the lock
       H-->>T: pass or fail

以下所有内容都在
:zephyr_file:`tests/net/conformance/ttcn3_runner.py` 中。

持有接口
=====================

Twister 在单独的 pytest 进程中运行每个测试，因此将一个测试
从另一个测试中排除必须在进程之间工作。测试框架在会话范围的 fixture 中
对锁文件获取排他
``flock``。

顺序与锁同样重要。fixture 在
``dut`` fixture 之前请求，因此当另一个
一致性测试持有接口时，测试系统甚至不会启动 —— 两个应用程序同时响应
``192.0.2.1`` 会混淆两个测试套件。

锁文件名携带有效用户 ID。特权测试套件以
root 身份运行，root 无法打开另一个用户留在粘性
临时目录中的锁文件。由于运行要么完全特权要么完全非特权，每个
用户的锁仍然排除了所有可能冲突的内容 —— 这也是
特权运行和非特权运行不能同时启动的原因。

测试套件特征
=============

关于测试套件的三个事实从 :file:`suites/<name>/build.conf` 读取：

``MODE=parallel``
    测试用例创建并行测试组件，因此测试套件通过
    Titan 的主控制器运行，而不是作为单个可执行文件，并且必须安装 ``expect``。

``PRIVILEGED=yes``
    测试套件绑定特权端口或打开数据包套接字，因此运行
    必须是 root。

``L2=yes``
    测试套件在 IP 层以下工作，因此它需要 ``zethL2`` 而不是
    ``zeth``。

同一文件由 :file:`build.sh` 作为 shell 片段 source，这就是
为什么它写成 shell 赋值；测试框架只匹配其中的子字符串。

构建和运行测试套件
==============================

构建是 :file:`build.sh <suite>`，预算 1800 秒，生成
:file:`suites/<suite>/build/<suite>`。

运行必须应对 Titan 以两种不同方式安装。
发行版包将其库放在 :file:`{TTCN3_DIR}/lib/titan`，
源码构建放在 :file:`{TTCN3_DIR}/lib`；测试框架选择存在的那个
并将其加到 ``LD_LIBRARY_PATH`` 前面，并将 :file:`{TTCN3_DIR}/bin` 加到
``PATH`` 前面。并行测试套件用 ``ttcn3_start`` 启动，其他测试套件
直接启动。

测试套件在新会话中启动，因此超时的测试套件可以
连同其启动的所有内容一起被杀死 —— 遗留运行的主控制器
会为下一个测试持有接口。

将判决转化为结果
===============================

两个正则表达式匹配 Titan 在运行结束时打印的行，
断言三件事：是否打印了判决，是否至少运行了一个
测试用例，以及总体判决是否为 ``pass``。没有产生
任何输出的测试套件，或因为所有用例都被过滤掉而没有运行任何内容的测试套件，
会失败而不是静默通过。判决的含义见 :ref:`ttcn3_verdicts`。

主机侧
*************

以下所有内容都在 ``net-tools`` 仓库中，位于 :file:`ttcn3` 下。

布局
======

.. code-block:: none

   ttcn3/
       common/            shared TTCN-3 modules and the ethernet test port
       modules/           third party modules, cloned, not in git
       modules.txt        which modules, at which commit
       fetch-modules.sh   clone or check out the pinned commits
       build.sh           build one suite
       suites/<name>/     the suite, its sources.txt and its .cfg

测试套件如何构建
===================

:file:`build.sh` 清除测试套件的构建目录并扁平重建，
将所需的每个源代码通过符号链接并排放在一个目录中。

扁平化不是整洁，而是变通方案。Titan 生成的 makefile
用 ``sed`` 构建依赖规则，使用目标词干作为模式，
一旦源代码通过包含斜杠的路径命名就会出错。因此每个源代码
必须能通过其裸名称访问。

链接顺序是测试套件自己的源代码，然后是 :file:`common`，然后是 :file:`common/sources.txt` 中命名的模块
源代码，然后是测试套件自己的
:file:`sources.txt` 中的源代码。然后 ``ttcn3_makefilegen`` 生成 makefile ——
单模式测试套件用 ``-s``，并行测试套件不用 —— 然后 ``make``
构建它。

共享 TTCN-3 层
=======================

``Zephyr_SUT`` 保存所有测试套件共享的模块参数。测试套件从不
将地址或超时写入自身；它们从这里获取，因此
运行可以通过编辑一个配置文件移到不同的链路上。

.. list-table::
   :header-rows: 1

   * - 参数
     - 默认值
     - 含义
   * - ``tsp_sut_ipv4``
     - ``192.0.2.1``
     - Zephyr 响应的位置
   * - ``tsp_sut_ipv6``
     - ``2001:db8::1``
     - Zephyr 响应的位置，IPv6
   * - ``tsp_tester_ipv4``
     - ``192.0.2.2``
     - 测试套件响应的位置
   * - ``tsp_tester_ipv6``
     - ``2001:db8::2``
     - 测试套件响应的位置，IPv6
   * - ``tsp_tester_interface``
     - ``zeth``
     - 链路本地多播所需
   * - ``tsp_sut_hostname``
     - ``zephyr``
     - 响应器拥有的名称
   * - ``tsp_response_timeout``
     - ``5.0``
     - 响应可以花费多长时间
   * - ``tsp_silence_timeout``
     - ``2.0``
     - 观察静默多长时间

``Zephyr_Transport`` 提供 ``Zephyr_Tester`` 组件，带有
``IPL4asp`` 端口和用于监听、打开、发送、带保护定时器接收
以及断言没有到达的辅助函数。基于套接字的测试套件扩展该组件
而不是自己打开套接字。

``ARP_Types`` 是手写的，位于 :file:`common` 而不是
``arp`` 测试套件中，因为任何在 IP 以下工作的测试套件都必须自己响应
地址解析，在没有任何其他东西响应的链路上。Titan 项目
不发布 ARP 模块。

以太网测试端口
=====================

Titan 发布原始链路层测试端口 ``LANL2asp``，这里不使用
它。它用 libpcap 捕获，用零读取超时打开句柄，
在 Linux 上意味着"等待直到捕获块填满"。在像
测试链路一样安静的链路上，帧永远达不到测试，没有参数
可以改变它。

:file:`common/Ethernet_PT.cc` 改为读取数据包套接字，它
在到达时提供每个帧。它接受三个测试端口参数：``interface``，
必需；``source_address``，默认为接口自己的；以及
``ethertype``，设置时只传递该类型。

第三方模块
==================

测试套件针对 Titan 项目发布的协议模块和测试端口构建，
而不是定义自己的消息格式。使用十一个仓库，每个在 :file:`modules.txt` 中固定到一个提交，
由 :file:`fetch-modules.sh` 按需克隆。它们不是 vendored，克隆被
git 忽略，因此今天通过的测试套件明天仍然可以构建。移动一个固定是一
行编辑和重新运行。

上游模块是 EPL-2.0，而这里编写的所有内容是 Apache-2.0。
两者都是 OSI 批准的，这是 Zephyr 对永远不会成为
Zephyr 映像一部分的工具的要求；见 :ref:`external-contributions`。

.. _ttcn3_test_network:

测试网络
****************

``zeth`` 是一个两侧都有地址的普通 tap，使用它的
测试套件只是链路上的另一个主机。``zethL2`` 完全没有地址，
主机配置为不在其上响应，因此唯一响应
地址解析的是 Zephyr。:ref:`ttcn3_interfaces` 涵盖创建它们。

.. warning::

   名称 ``zethL2`` 写入三个必须一致的地方，
   没有任何东西检查它们是否一致：

   * :zephyr_file:`tests/net/conformance/ttcn3_runner.py` 中的 ``L2_INTERFACE``，
     决定测试运行前哪个接口必须存在
   * 每个 ``zethL2`` 测试的 :file:`boards/native_sim.overlay` 中的 ``host-interface``，
     决定测试系统出现在哪里
   * 每个 ``zethL2`` 测试套件配置文件中的 ``system.pt.interface``，
     决定测试套件在哪里监听

   不匹配表现为测试套件看不到帧并超时，而不是
   错误。

.. _ttcn3_adding_a_suite:

添加测试套件
******************

测试套件有两半，每个仓库一个，在
两者之前有一个决定要做。

选择形状
==================

**套接字或原始帧。** 可以通过 UDP 或 TCP 表达其含义的测试套件
扩展 ``Zephyr_Tester``，使用 ``IPL4asp`` 端口，在 ``zeth`` 上运行，
不需要特权。必须自己看到或发送帧的测试套件使用
``Ethernet_Port``，在 ``zethL2`` 上运行，必须是 root，并且必须自己响应
地址解析，因为该链路上没有其他东西会响应。优先使用套接字；
原始路径花费第二个接口和密码提示。

**单模式或并行。** 单模式，除非测试用例创建并行测试
组件。并行花费 Titan 的主控制器和对
``expect`` 的依赖，并使测试套件更难手动运行。

主机侧
=============

创建 :file:`suites/<name>`，包含 TTCN-3 源代码、
:file:`sources.txt`（命名测试套件所需的模块源代码）和
:file:`<name>.cfg`（包含模块参数和要运行的测试用例列表）。
只运行第三方模块中测试用例的测试套件不需要
自己的源代码 —— ``coap`` 是实际示例。

从 ``Zephyr_SUT`` 获取地址和超时。将任何新的上游模块添加到
:file:`modules.txt`，带有固定的提交。如果测试套件
是并行的、特权的或在 IP 以下工作，添加 :file:`build.conf`。

Zephyr 侧
==================

在 :zephyr_file:`tests/net/conformance` 下创建具有
上述布局的应用程序。:file:`src/main.c` 启用协议，
生成测试套件需要观察的任何流量，并打印一个独特的就绪
行。:file:`tests.yaml` 复制公共代码块并将测试命名为
``net.conformance.<name>``。

三个 pytest 文件中，:file:`pytest.ini` 和 :file:`conftest.py`
逐字复制；:file:`test_<name>_conformance.py` 只在测试套件
名称和等待的就绪行上不同。

记录不匹配的内容
=============================

当测试套件断言与标准不匹配的行为时，在断言
处说明，因此偏差被记录而不是静默固化。
没有任何测试套件覆盖的内容属于
:ref:`ttcn3_known_gaps`，新测试套件是向
:ref:`ttcn3_suites` 添加一行的好时机。

试一试
=============

先手动运行两半，如 :ref:`ttcn3_running_by_hand` 所示，
只有测试套件通过后才通过 Twister。预期第一次构建会很慢，
记住缺少先决条件会跳过测试而不是失败
—— 似乎立即通过的测试套件可能从未运行过。
