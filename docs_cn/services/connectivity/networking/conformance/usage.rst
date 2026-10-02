.. _ttcn3_running:

运行一致性测试套件
##############################

.. contents::
    :local:
    :depth: 2

运行如下进行。Twister 构建并启动被测系统，
测试框架用 Titan 构建 TTCN-3 测试套件，测试套件通过
tap 接口与运行中的应用通信，Titan 的判决成为
测试结果。

运行需要什么
****************

* **Titan 安装**，``TTCN3_DIR`` 指向它。参见
  :ref:`ttcn3_installing_titan`。
* **第三方 TTCN-3 模块**，用
  :file:`ttcn3/fetch-modules.sh` 获取一次。它们在固定的提交上克隆，
  不是 ``net-tools`` 仓库的一部分。
* **net-tools 的 checkout**，west 工作区已有：它
  在 :file:`west.yml` 的 ``tools`` 组下，该组未被过滤。
* **make**，因为这是 Titan 构建测试套件的方式。
* **``zeth`` 接口**，或在 IP 层以下工作的测试套件用
  ``zethL2``。参见 :ref:`ttcn3_interfaces`。
* **root**，对无法避免特权端口或数据包套接字的测试套件。
* **expect**，对通过 Titan 主控制器运行的测试套件。

:ref:`ttcn3_suites` 列出哪些测试套件需要哪些，
:zephyr_file:`scripts/net/run-conformance-tests.sh` ``--list`` 打印相同内容。

测试框架在设置 ``NET_TOOLS_BASE`` 时在其中查找 net-tools，否则
在 ``ZEPHYR_BASE`` 相对的 :file:`../tools/net-tools/ttcn3`，然后
再高一个目录。所有这些在构建任何东西之前检查，
缺失的部分以原因跳过测试而不是使其失败。

在环境中设置 ``NET_CONFORMANCE_REQUIRED`` 可将上述每一项
转为失败。这适用于以测试套件为目的的运行（例如夜间作业），
其中未运行的测试不应像已运行的测试那样通过。

.. _ttcn3_installing_titan:

安装 Titan
****************

大多数发行版打包了 Titan，持续集成安装的就是它：

.. code-block:: console

   sudo apt install --no-install-recommends eclipse-titan expect
   export TTCN3_DIR=/usr

打包版本落后于测试套件构建所对的协议模块，因此
如果测试套件编译失败，改为从源码构建当前 Titan。

从源码构建 Titan
==========================

:file:`net-tools/docker/Dockerfile.ttcn3` 将 Titan 构建到 :file:`/opt/titan`，
并作为手动执行（作为容器或作为遵循的
配方）的参考。它是本地选项，不是持续集成使用的。

手动构建的 Titan 必须正确把握两件事。Titan 通过其
源码树中的 :file:`Makefile.personal`（而不是 ``configure`` 脚本）配置，
那里的 ``TTCN3_DIR`` 是安装前缀。并且 ``make install`` 必须
串行：运行时的一部分包含另一部分生成的头文件，
并行 make 会丢失该竞争。

用脚本运行测试套件
**********************************

:zephyr_file:`scripts/net/run-conformance-tests.sh` 用一条命令完成
以下两节描述的内容，是运行测试套件最简单的方式：它
查找 net-tools，缺失时获取模块，创建所选
测试套件需要的接口，所选测试套件需要 root 时在 ``sudo`` 下重跑自身，
运行一次 Twister，然后拆下接口。

.. code-block:: console

   export TTCN3_DIR=/usr
   ./scripts/net/run-conformance-tests.sh

命名测试套件仅运行它们，这是在调试一个时保持非
特权的快速方式：

.. code-block:: console

   ./scripts/net/run-conformance-tests.sh mdns dns

``--list`` 显示测试套件及各自所需，``--keep`` 为下次运行
保持接口，``--start`` 和 ``--stop`` 仅做该一半。``--help`` 列出其余，
以及检测到的目录。

由于特权运行以 root 创建文件，脚本在退出前
将 Twister 输出目录和测试套件构建目录交还给调用用户。

.. _ttcn3_interfaces:

设置网络接口
*********************************

测试套件使用两个 tap 接口，因为在 IP 层以下工作的
测试套件不能与为自己回答的主机共享链路。

``zeth``，共享接口
==============================

由通过套接字工作的测试套件使用，测试器只是
链路上的另一个主机：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   sudo ./net-setup.sh --config zeth.conf start

主机持有 ``192.0.2.2/24`` 和 ``2001:db8::2``；Zephyr 在
``192.0.2.1`` 和 ``2001:db8::1`` 回答。用 ``stop`` 替代
``start`` 拆下。

``zethL2``，无地址接口
=====================================

由在 IP 层以下工作的测试套件使用：

.. code-block:: console

   sudo ./net-setup.sh --config zeth-l2.conf --iface zethL2 start

此接口故意不赋予 IP 地址。Linux 除非被告知
否则为任何接口上持有的任何地址回答地址解析
和邻居发现，来自主机的回答与来自 Zephyr 的回答
无法区分。测试器讲原始帧，因此
它不需要自己的地址。

配置设置三个 sysctls 以阻止主机加入：
``arp_ignore=8`` 使其不为任何本地地址回答地址解析，
``arp_announce=2`` 使其从不以此接口不持有的地址回答，
``disable_ipv6=1`` 使没有邻居通告或路由器请求。

名称 ``zethL2`` 不可自由选择；参见 :ref:`ttcn3_test_network`。

用 Twister 运行测试套件
*******************************

获取第三方模块一次。脚本可安全重跑：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   ./ttcn3/fetch-modules.sh

然后运行测试：

.. code-block:: console

   export TTCN3_DIR=/usr
   cd $ZEPHYR_BASE
   ./scripts/twister -p native_sim --enable-slow -T tests/net/conformance

``--enable-slow`` 是必需的：测试套件标记自己为慢，因为
完整运行需要几十分钟。``native_sim`` 是它们允许的唯一平台。

单个测试套件由其测试标识符选择，为
``net.conformance.<suite>``：

.. code-block:: console

   ./scripts/twister -p native_sim --enable-slow -T tests/net/conformance \
       -s net.conformance.mdns

它们也带 ``net`` 和 ``conformance`` 标签，因此 ``--tag conformance``
选取所有。

作为 root 运行
==============

某些测试套件必须作为 root 运行。DHCP 定义在端口 67 和 68
上没有其他方式移动，因此测试器无法避免绑定
特权端口；并且从链路读取帧需要数据包套接字。这些
测试在权限不足时跳过自身。

用 ``sudo -E`` 使 ``TTCN3_DIR`` 和其余环境存活。
运行要么完全特权要么完全非特权 —— 为何两者不可混合参见 :ref:`ttcn3_runner`。

为什么运行是串行的
===================

所有被测系统在同一接口上回答相同地址，因此
一次只能运行一个一致性测试。它们对接口
取排他锁并相互等待，这意味着无论 Twister 给多少任务，
整个目录的运行都是串行的。

.. _ttcn3_running_by_hand:

手动运行测试套件
***********************

Twister 方便但绕路慢。编写或调试测试套件时，
手动运行两半。

启动被测系统并让其运行：

.. code-block:: console

   cd $ZEPHYR_BASE
   west build -p -b native_sim -d ../build/mdns tests/net/conformance/mdns
   ../build/mdns/zephyr/zephyr.exe

构建并运行测试套件对其：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools/ttcn3
   ./build.sh mdns
   cd suites/mdns/build
   ./mdns ../mdns.cfg

对于测试用例创建并行测试组件的测试套件，改为通过
主控制器启动：

.. code-block:: console

   ttcn3_start ./coap ../coap.cfg

单个测试用例通过命名运行：

.. code-block:: console

   ./mdns ../mdns.cfg MDNS_Suite.tc_a_query

地址、接口和超时都来自测试套件配置文件
的 ``[MODULE_PARAMETERS]`` 部分，因此运行
可以通过编辑一个文件（而不是测试套件）移到不同的链路上。

测试框架做而你必须自己做的：将 Titan 的库
目录放到 ``LD_LIBRARY_PATH`` 上。

.. _ttcn3_verdicts:

读取结果
******************

Titan 运行以每个判决的计数和运行的判决结束：

.. code-block:: console

   Verdict statistics: 0 none (0.00 %), 7 pass (100.00 %), 0 inconc (0.00 %), 0 fail (0.00 %), 0 error (0.00 %).
   Test execution summary: 7 test cases were executed. Overall verdict: pass

``inconc`` 意味着测试用例无法得出结论，通常因为
它依赖的某事未发生。它不是通过。``error`` 意味着
测试套件本身失败，而不是被测系统。

证据在两处。Titan 将每个测试套件的日志写入
构建目录，命名来自配置文件中的 ``LogFile`` 设置。Twister
在其输出目录下写 :file:`twister_harness.log`，以 ``INFO``
携带整个测试套件输出。

测试套件何时被跳过
***********************

测试套件所需的一切在构建任何东西之前检查，
缺失的部分跳过测试而不是使其失败。原因，按检查
顺序：

.. list-table::
   :header-rows: 1

   * - 原因
     - 该做什么
   * - ``TTCN3_DIR is unset``
     - 安装 Titan 并 export ``TTCN3_DIR``；参见 :ref:`ttcn3_installing_titan`
   * - ``make is not installed``
     - 安装 make；Titan 用生成的 makefile 构建测试套件
   * - ``no TTCN-3 suites under ...``
     - 未找到 net-tools；设置 ``NET_TOOLS_BASE``
   * - ``... has no <suite> suite``
     - net-tools checkout 早于测试套件；更新它
   * - ``third party modules are missing``
     - 运行 :file:`ttcn3/fetch-modules.sh`
   * - ``the <iface> interface does not exist``
     - 用 :file:`net-setup.sh` 创建；参见 :ref:`ttcn3_interfaces`
   * - ``ttcn3_start is not in TTCN3_DIR/bin``
     - 安装 ``expect`` 和带主控制器的 Titan
   * - ``has to be run as root``
     - 在 ``sudo -E`` 下重跑，或用脚本

故障排除
***************

测试套件无法编译
==========================

几乎总是落后于测试套件构建所对协议模块的打包 Titan。
从源码构建 Titan。

测试套件看不到任何内容并超时
====================================

检查应用程序和测试套件是否在同一接口：在 IP 以下工作的
测试套件需要 ``zethL2``，并且应用程序必须用命名
相同接口的 ``host-interface`` 属性构建，测试在
:file:`boards/native_sim.overlay` 中设置。如果主机
在链路上回答而不是 Zephyr，``zethL2`` sysctls 未生效；
用 ``sysctl net.ipv4.conf.zethL2.arp_ignore`` 确认。

运行挂起或被切断
=========================

四个超时嵌套在运行周围，哪个触发说明问题所在：
应用程序就绪行 30 秒，测试套件构建 1800 秒，
测试套件运行 600 秒，Twister 测试整体 900 秒。
超时的测试套件连同其整个进程组被杀死，因此
没有主控制器遗留。

遗留状态
=============

用 :file:`net-setup.sh` 和 ``stop`` 拆下接口。
测试取的锁是临时目录中名为 :file:`zephyr-net-conformance-<euid>.lock` 的文件；
进程退出时释放，因此过期的无害。
