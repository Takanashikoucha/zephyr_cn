.. _ttcn3_running:

Running the conformance suites
##############################

.. contents::
    :local:
    :depth: 2

Run 如下进行。Twister 构建并启动被测系统（harness 用 Titan 构建 TTCN-3 suite（suite 通过 tap interface 与运行中的 application 通信（且 Titan 的 verdict 成为 test result。

What a run needs
****************

* **Titan 安装**（``TTCN3_DIR`` 指向其。参见 :ref:`ttcn3_installing_titan`。
* **第三方 TTCN-3 modules**（用 :file:`ttcn3/fetch-modules.sh` 获取一次。其在 pinned commits 克隆（且不是 ``net-tools`` repository 的一部分。
* **net-tools 的 checkout**（west workspace 已有：其在 :file:`west.yml` 的 ``tools`` group 下（该 group 未被过滤。
* **make**（因为这是 Titan 构建 suite 的方式。
* **``zeth`` interface**（或在 IP layer 以下工作的 suite 的 ``zethL2``。参见 :ref:`ttcn3_interfaces`。
* **root**（对无法避免 privileged port 或 packet socket 的 suite。
* **expect**（对通过 Titan 的 main controller 运行的 suite。

:ref:`ttcn3_suites` 列出哪些 suites 需要哪些（:zephyr_file:`scripts/net/run-conformance-tests.sh` ``--list`` 打印相同内容。

Harness 在设置 ``NET_TOOLS_BASE`` 时在其中查找 net-tools（否则在 ``ZEPHYR_BASE`` 相对的 :file:`../tools/net-tools/ttcn3`（然后高一个 directory。所有这些在构建任何东西前检查（且缺失部分以 reason 跳过 test 而非使其失败。

.. _ttcn3_installing_titan:

Installing Titan
****************

大多数 distributions 打包 Titan（且 continuous integration 安装的就是其：

.. code-block:: console

   sudo apt install --no-install-recommends eclipse-titan expect
   export TTCN3_DIR=/usr

打包版本落后于 suites 构建所对的 protocol modules（故若 suite 编译失败（改为从 source 构建当前 Titan。

Building Titan from source
==========================

:file:`net-tools/docker/Dockerfile.ttcn3` 将 Titan 构建到 :file:`/opt/titan`（并作为手动执行（作为 container 或作为遵循的 recipe）的 reference。其为本地 option（而非 continuous integration 使用的。

手动构建的 Titan 须正确把握两件事。Titan 通过其 source tree 中的 :file:`Makefile.personal`（而非 ``configure`` script）配置（且那里的 ``TTCN3_DIR`` 为 install prefix。且 ``make install`` 须串行：runtime 的部分包含另一部分生成的 headers（且并行 make 丢失该 race。

Running the suites with the script
**********************************

:zephyr_file:`scripts/net/run-conformance-tests.sh` 用一条 command 完成以下两节描述的内容（且是运行 suites 最简单的方式：其查找 net-tools（缺失时获取 modules（创建所选 suites 需要的 interfaces（所选 suite 需 root 时在 ``sudo`` 下重跑自身（运行一次 Twister（然后拆下 interfaces。

.. code-block:: console

   export TTCN3_DIR=/usr
   ./scripts/net/run-conformance-tests.sh

命名 suites 仅运行其（在调试一个时保持非 privileged 的快速方式：

.. code-block:: console

   ./scripts/net/run-conformance-tests.sh mdns dns

``--list`` 显示 suites 及各自所需（``--keep`` 为下次 run 保持 interfaces（``--start`` 和 ``--stop`` 仅做该一半。``--help`` 列出其余（以及检测到的 directories。

由于 privileged run 以 root 创建 files（script 在退出前将 Twister output directory 和 suite build directories 交还给调用 user。

.. _ttcn3_interfaces:

Setting up the network interfaces
*********************************

Suites 用两个 tap interfaces（因为在 IP layer 以下工作的 suite 不能与为自己回答的 host 共享 link。

``zeth``, the shared interface
==============================

由通过 sockets 工作的 suites 使用（tester 为 link 上另一个 host：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   sudo ./net-setup.sh --config zeth.conf start

Host 持有 ``192.0.2.2/24`` 和 ``2001:db8::2``；Zephyr 在 ``192.0.2.1`` 和 ``2001:db8::1`` 回答。用 ``stop`` 替代 ``start`` 拆下。

``zethL2``, the address-less interface
======================================

由在 IP layer 以下工作的 suites 使用：

.. code-block:: console

   sudo ./net-setup.sh --config zeth-l2.conf --iface zethL2 start

此 interface 故意不赋予 IP address。Linux 除非被告知否则为任何 interface 上持有的任何 address 回答 address resolution 和 neighbour discovery（且来自 host 的回答与来自 Zephyr 的回答无法区分。Tester 讲 raw frames（故其无需自己的 address。

Configuration 设置三个 sysctls 以阻止 host 加入：``arp_ignore=8`` 使其不为任何 local address 回答 address resolution（``arp_announce=2`` 使其从不以此 interface 不持有的 address 回答（``disable_ipv6=1`` 使无 neighbour advertisements 或 router solicitations。

名称 ``zethL2`` 不可自由选择；参见 :ref:`ttcn3_test_network`。

Running the suites with Twister
*******************************

获取第三方 modules 一次。Script 可安全重跑：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   ./ttcn3/fetch-modules.sh

然后运行 tests：

.. code-block:: console

   export TTCN3_DIR=/usr
   cd $ZEPHYR_BASE
   ./scripts/twister -p native_sim --enable-slow -T tests/net/conformance

``--enable-slow`` 必需：suites 标记自己为 slow（因为完整 run 需数十分钟。``native_sim`` 为其允许的唯一 platform。

单个 suite 由其 test identifier 选择（为 ``net.conformance.<suite>``：

.. code-block:: console

   ./scripts/twister -p native_sim --enable-slow -T tests/net/conformance \
       -s net.conformance.mdns

其也带 ``net`` 和 ``conformance`` tags（故 ``--tag conformance`` 选取所有。

Running as root
===============

某些 suites 须以 root 运行。DHCP 定义在 ports 67 和 68（且无其他方式移动（故 tester 无法避免绑定 privileged port；且从 link 读取 frames 需 packet socket。这些 tests 在权限不足时跳过自身。

用 ``sudo -E`` 使 ``TTCN3_DIR`` 和其余 environment 存活。Run 要么完全 privileged 要么完全不是——为何两者不可混合参见 :ref:`ttcn3_runner`。

Why a run is serial
===================

所有被测系统在同一 interface 上回答相同 address（故一次仅能运行一个 conformance test。其对 interface 取 exclusive lock（并相互等待（这意味着无论 Twister 给多少 jobs（整个 directory 的 run 为串行。

.. _ttcn3_running_by_hand:

Running a suite by hand
***********************

Twister 方便但绕路慢。编写或调试 suite 时（手动运行两半。

启动被测系统并让其运行：

.. code-block:: console

   cd $ZEPHYR_BASE
   west build -p -b native_sim -d ../build/mdns tests/net/conformance/mdns
   ../build/mdns/zephyr/zephyr.exe

构建并运行 suite 对其：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools/ttcn3
   ./build.sh mdns
   cd suites/mdns/build
   ./mdns ../mdns.cfg

对 test cases 创建 parallel test components 的 suite（改为通过 main controller 启动：

.. code-block:: console

   ttcn3_start ./coap ../coap.cfg

单个 test case 通过命名运行：

.. code-block:: console

   ./mdns ../mdns.cfg MDNS_Suite.tc_a_query

Addresses、interface 和 timeouts 均来自 suite configuration file 的 ``[MODULE_PARAMETERS]`` section（故 run 可通过编辑一个 file（而非 suite）移到不同 link。

Harness 做而您须自己做的：将 Titan 的 library directory 放到 ``LD_LIBRARY_PATH``。

.. _ttcn3_verdicts:

Reading the result
******************

Titan run 以每个 verdict 的计数和 run 的 verdict 结束：

.. code-block:: console

   Verdict statistics: 0 none (0.00 %), 7 pass (100.00 %), 0 inconc (0.00 %), 0 fail (0.00 %), 0 error (0.00 %).
   Test execution summary: 7 test cases were executed. Overall verdict: pass

``inconc`` 意味着 test case 无法得出结论（通常因为其依赖的某事未发生。其不是 pass。``error`` 意味着 suite 本身失败（而非被测系统。

证据在两处。Titan 将每个 suite 的 log 写入 build directory（命名来自 configuration file 的 ``LogFile`` 设置。Twister 在其 output directory 下写 :file:`twister_harness.log`（以 ``INFO`` 携带整个 suite output。

When a suite is skipped
***********************

Suite 所需的一切在构建任何东西前检查（且缺失部分跳过 test 而非使其失败。Reasons（按检查顺序）：

.. list-table::
   :header-rows: 1

   * - Reason
     - What to do
   * - ``TTCN3_DIR is unset``
     - 安装 Titan 并 export ``TTCN3_DIR``；参见 :ref:`ttcn3_installing_titan`
   * - ``make is not installed``
     - 安装 make；Titan 用生成的 makefile 构建 suite
   * - ``no TTCN-3 suites under ...``
     - 未找到 net-tools；设置 ``NET_TOOLS_BASE``
   * - ``... has no <suite> suite``
     - net-tools checkout 早于 suite；更新其
   * - ``third party modules are missing``
     - 运行 :file:`ttcn3/fetch-modules.sh`
   * - ``the <iface> interface does not exist``
     - 用 :file:`net-setup.sh` 创建；参见 :ref:`ttcn3_interfaces`
   * - ``ttcn3_start is not in TTCN3_DIR/bin``
     - 安装 ``expect`` 和带 main controller 的 Titan
   * - ``has to be run as root``
     - 在 ``sudo -E`` 下重跑（或用 script

Troubleshooting
***************

The suite does not compile
==========================

几乎总是落后于 suite 构建所对 protocol modules 的打包 Titan。从 source 构建 Titan。

The suite sees nothing and times out
====================================

检查 application 和 suite 是否在同一 interface：IP 以下工作的 suite 要 ``zethL2``（且 application 须用命名相同 interface 的 ``host-interface`` property 构建（test 在 :file:`boards/native_sim.overlay` 中设置。若 host 在 link 上回答而非 Zephyr（``zethL2`` sysctls 未生效；用 ``sysctl net.ipv4.conf.zethL2.arp_ignore`` 确认。

A run hangs or is cut off
=========================

四个 timeouts 嵌套在 run 周围（哪个触发说明问题所在：application ready line 30 秒（suite build 1800 秒（suite run 600 秒（Twister test 整体 900 秒。超时 suite 连同其整个 process group 被杀死（故无 main controller 遗留。

Leftover state
==============

用 :file:`net-setup.sh` 和 ``stop`` 拆下 interfaces。Tests 取的 lock 为 temporary directory 中名为 :file:`zephyr-net-conformance-<euid>.lock` 的 file；process 退出时释放（故过期的无害。
