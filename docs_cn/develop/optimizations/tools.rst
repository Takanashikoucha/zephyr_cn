.. _optimization_tools:

优化工具
##################

可用的优化工具允许你使用不同的构建系统目标来分析 :ref:`footprint_tools` 和 :ref:`data_structure_tools`。也可以生成 :ref:`HTML 仪表盘 <dashboard>`，用于以更具动态性的方式查看构建产物和指标。

.. _footprint_tools:

占用空间与内存使用
**************************

构建系统提供 3 个目标，用于查看和分析生成镜像中 RAM、ROM 和栈的使用情况。这些工具在最终镜像上运行，给出关于 RAM 和 ROM 中使用的符号和代码大小的信息。此外，借助编译器提供的功能，我们还可以生成最坏情况栈使用分析。

本节提到的一些工具基于符号的物理组织来组织其输出。由于某些符号可能位于项目树结构之外，或者可能缺少按名称显示它们所需的元数据，因此使用以下顶层容器来分组此类符号：

* Hidden（隐藏）- RAM 和 ROM 报告将所有没有匹配映射文件的处理符号列在 Hidden 类别中。

  这意味着列出的符号的文件未被添加到元数据文件中，是空的，或未被定义。工具无法获取给定符号的函数名称，也无法识别它来自哪里。

* No paths（无路径）- RAM 和 ROM 报告将所有带相对路径的处理符号列在 No paths 类别中。

  这意味着列出的符号无法被放置在报告树结构中某个特定文件下的绝对路径处。工具能够获取函数名称，但无法识别它来自哪里。

  .. note::

     同一函数可能存在多个实例，No paths 类别将在一个条目中列出这些实例的总和。


构建目标：ram_report
========================

以表格形式列出所有编译对象及其 RAM 使用情况，包括每个符号的字节数及其所占百分比。数据基于对象在树中的文件系统位置以及包含该符号的文件进行分组。

在你的开发板上使用 ``ram_report`` 目标，如以下示例所示。如果你正在使用 :ref:`sysbuild`，请参见 :ref:`sysbuild_dedicated_image_build_targets`。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: ram_report

这些命令将生成类似以下输出的内容::

    Path                                                           Size    %      Address
    ========================================================================================
    Root                                                           4637 100.00%  -
    ├── (hidden)                                                      4   0.09%  -
    ├── (no paths)                                                 2748  59.26%  -
    │   ├── _cpus_active                                              4   0.09%  0x20000314
    │   ├── _kernel                                                  32   0.69%  0x20000318
    │   ├── _sw_isr_table                                           384   8.28%  0x00006474
    │   ├── cli.1                                                    16   0.35%  0x20000254
    │   ├── on.2                                                      4   0.09%  0x20000264
    │   ├── poll_out_lock.0                                           4   0.09%  0x200002d4
    │   ├── z_idle_threads                                          128   2.76%  0x20000120
    │   ├── z_interrupt_stacks                                     2048  44.17%  0x20000360
    │   └── z_main_thread                                           128   2.76%  0x200001a0
    ├── WORKSPACE                                                   184   3.97%  -
    │   └── modules                                                 184   3.97%  -
    │       └── hal                                                 184   3.97%  -
    │           └── nordic                                          184   3.97%  -
    │               └── nrfx                                        184   3.97%  -
    │                   └── drivers                                 184   3.97%  -
    │                       └── src                                 184   3.97%  -
    │                           ├── nrfx_clock.c                      8   0.17%  -
    │                           │   └── m_clock_cb                    8   0.17%  0x200002e4
    │                           ├── nrfx_gpiote.c                   132   2.85%  -
    │                           │   └── m_cb                        132   2.85%  0x20000060
    │                           ├── nrfx_ppi.c                        4   0.09%  -
    │                           │   └── m_channels_allocated          4   0.09%  0x200000e4
    │                           └── nrfx_twim.c                      40   0.86%  -
    │                               └── m_cb                         40   0.86%  0x200002ec
    └── ZEPHYR_BASE                                                1701  36.68%  -
        ├── arch                                                      5   0.11%  -
        │   └── arm                                                   5   0.11%  -
        │       └── core                                              5   0.11%  -
        │           ├── mpu                                           1   0.02%  -
        │           │   └── arm_mpu.c                                 1   0.02%  -
        │           │       └── static_regions_num                    1   0.02%  0x20000348
        │           └── tls.c                                         4   0.09%  -
        │               └── z_arm_tls_ptr                             4   0.09%  0x20000240
        ├── drivers                                                 258   5.56%  -
        │   ├── ...                                                 ...    ...%
    ========================================================================================
                                                                    4637


构建目标：rom_report
========================

以表格形式列出所有编译对象及其 ROM 使用情况，包括每个符号的字节数及其所占百分比。数据基于对象在树中的文件系统位置以及包含该符号的文件进行分组。

在你的开发板上使用 ``rom_report`` 目标，如以下示例所示。如果你正在使用 :ref:`sysbuild`，请参见 :ref:`sysbuild_dedicated_image_build_targets`。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: rom_report

这些命令将生成类似以下输出的内容::

    Path                                                           Size    %      Address
    ========================================================================================
    Root                                                          27828 100.00%  -
    ├── ...                                                         ...    ...%
    └── ZEPHYR_BASE                                               13558  48.72%  -
        ├── arch                                                   1766   6.35%  -
        │   └── arm                                                1766   6.35%  -
        │       └── core                                           1766   6.35%  -
        │           ├── cortex_m                                   1020   3.67%  -
        │           │   ├── fault.c                                 620   2.23%  -
        │           │   │   ├── bus_fault.constprop.0               108   0.39%  0x00000749
        │           │   │   ├── mem_manage_fault.constprop.0        120   0.43%  0x000007b5
        │           │   │   ├── usage_fault.constprop.0              84   0.30%  0x000006f5
        │           │   │   ├── z_arm_fault                         292   1.05%  0x0000082d
        │           │   │   └── z_arm_fault_init                     16   0.06%  0x00000951
        │           │   ├── ...                                     ...    ...%
        ├── boards                                                   32   0.11%  -
        │   └── arm                                                  32   0.11%  -
        │       └── reel_board                                       32   0.11%  -
        │           └── board.c                                      32   0.11%  -
        │               ├── __init_board_reel_board_init              8   0.03%  0x000063e4
        │               └── board_reel_board_init                    24   0.09%  0x00000ed5
        ├── build                                                   194   0.70%  -
        │   └── zephyr                                              194   0.70%  -
        │       ├── isr_tables.c                                    192   0.69%  -
        │       │   └── _irq_vector_table                           192   0.69%  0x00000040
        │       └── misc                                              2   0.01%  -
        │           └── generated                                     2   0.01%  -
        │               └── configs.c                                 2   0.01%  -
        │                   └── _ConfigAbsSyms                        2   0.01%  0x00005945
        ├── drivers                                                6282  22.57%  -
        │   ├── ...                                                 ...    ...%
    ========================================================================================
                                                                   21652

.. _footprint_tools_plot:

构建目标：ram_plot/rom_plot
================================

与 ``ram_report`` 和 ``rom_report`` 构建目标类似，这些目标以旭日图（sunburst chart）作为可视化表示来生成内存使用报告。用户可以点击各个扇区来浏览目录结构，将鼠标悬停在扇区上以获取更多详细信息。

运行这些目标会首先生成命令行报告，然后打开一个浏览器窗口。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: ram_plot

.. image:: ram_plot.png
   :align: center
   :alt: RAM usage sunburst chart

ROM 使用的情况类似。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: rom_plot

.. image:: rom_plot.png
   :align: center
   :alt: ROM usage sunburst chart


构建目标：puncover
=====================

此目标使用一个名为 puncover 的第三方工具，可以在 https://github.com/HBehrens/puncover 找到。构建此目标时，它会启动一个本地 web 服务器，允许你打开 web 客户端来浏览文件并查看它们的 ROM、RAM 和栈使用情况。

在使用此目标之前，请先安装 puncover Python 模块::

    pip3 install --user puncover

.. warning::

   这是一个第三方工具，在任何给定时间可能可用也可能不可用。请检查 GitHub issues，并向项目维护者报告新问题。

安装 Python 模块后，在你的开发板上使用 ``puncover`` 目标，如以下示例所示。如果你正在使用 :ref:`sysbuild`，请参见 :ref:`sysbuild_dedicated_image_build_targets`。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: puncover

``puncover`` 目标默认在 ``localhost:5000`` 上启动本地 web 服务器。HTTP 服务器运行的主机 IP 和端口可以通过设置环境变量 ``PUNCOVER_HOST`` 和 ``PUNCOVER_PORT`` 来更改。可以通过在 ``EXTRA_PUNCOVER_ARGS`` 中定义来为 puncover 提供进一步参数。

要在交互式 web 应用中查看最坏情况栈使用分析，请在启用 :kconfig:option:`CONFIG_STACK_USAGE` 的情况下构建。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: puncover
    :gen-args: -DCONFIG_STACK_USAGE=y -DCONFIG_CALLGRAPH_INFO=y

如果你想要一份关于发现的最坏情况栈使用的 JSON 文件报告，而不启动 web 应用，你可以添加选项 ``--generate-report --non-interactive --report-type json`` 用于非交互使用。并通过将每个你感兴趣的函数以 ``--report-max-static-stack-usage FUNCTION_NAME:::MAXIMAL_STACK_SIZE`` 的形式作为参数添加，来将其纳入报告中。例如，要导出 ``log_process_thread_func``、``shell_thread``、``bg_thread_main`` 和 ``work_queue_main``，看起来将如下所示：

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: puncover
    :gen-args: -DCONFIG_STACK_USAGE=y -DCONFIG_CALLGRAPH_INFO=y -DEXTRA_PUNCOVER_ARGS="--generate-report;--non-interactive;--report-type;json;--report-max-static-stack-usage;log_process_thread_func:::832;--report-max-static-stack-usage;shell_thread:::4160;--report-max-static-stack-usage;bg_thread_main:::2112;--report-max-static-stack-usage;work_queue_main:::1088;--report-filename;$PWD/report"

为了更好的可维护性和概览性，所有参数也可以放在一个 yaml 配置中：

.. code-block:: yaml

      elf_file: ~/zephyrproject/zephyr/samples/net/mqtt_publisher/build/zephyr/zephyr.elf
      gcc-tools-base: ~/zephyr-sdk-1.0.1/gnu/arm-zephyr-eabi/bin/arm-zephyr-eabi-
      src_root: ~/zephyrproject/zephyr
      build_dir: ~/zephyrproject/zephyr/samples/net/mqtt_publisher/build
      generate-report: true
      non-interactive: true
      report-type: json
      report-max-static-stack-usage:
         - log_process_thread_func:::832
         - shell_thread:::4160
         - bg_thread_main:::2112
         - work_queue_main:::1088
         - mgmt_event_work_handler:::896

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: puncover
    :gen-args: -DCONFIG_STACK_USAGE=y -DCONFIG_CALLGRAPH_INFO=y -DEXTRA_PUNCOVER_ARGS="-c puncover_config.yaml"


.. _data_structure_tools:

数据结构
****************


构建目标：pahole
=====================

Poke-a-hole（pahole）是一个对象文件分析工具，用于查找数据结构的大小，以及由于编译器将数据元素对齐到 CPU 的字大小而产生的空洞。

在使用此目标之前必须安装 Poke-a-hole（pahole）。它可以获取自 https://git.kernel.org/pub/scm/devel/pahole/pahole.git，并且同时存在于 fedora 和 ubuntu 的 dwarves 包中::

    sudo apt-get install dwarves

或者，你可以从 fedora 获取::

    sudo dnf install dwarves

安装包后，在你的开发板上使用 ``pahole`` 目标，如以下示例所示。如果你正在使用 :ref:`sysbuild`，请参见 :ref:`sysbuild_dedicated_image_build_targets`。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: pahole

Pahole 将在控制台中生成类似以下输出的内容::

    /* Used at: [...]/build/zephyr/kobject_hash.c */
    /* <375> [...]/zephyr/include/zephyr/sys/dlist.h:37 */
    union {
            struct _dnode *            head;               /*     0     4 */
            struct _dnode *            next;               /*     0     4 */
    };
    /* Used at: [...]/build/zephyr/kobject_hash.c */
    /* <397> [...]/zephyr/include/zephyr/sys/dlist.h:36 */
    struct _dnode {
            union {
                    struct _dnode *    head;                 /*     0     4 */
                    struct _dnode *    next;                 /*     0     4 */
            };                                               /*     0     4 */
            union {
                    struct _dnode *    tail;                 /*     4     4 */
                    struct _dnode *    prev;                 /*     4     4 */
            };                                               /*     4     4 */

            /* size: 8, cachelines: 1, members: 2 */
            /* last cacheline: 8 bytes */
    };
    /* Used at: [...]/build/zephyr/kobject_hash.c */
    /* <3b7> [...]/zephyr/include/zephyr/sys/dlist.h:41 */
    union {
            struct _dnode *            tail;               /*     0     4 */
            struct _dnode *            prev;               /*     0     4 */
    };
    ...
    ...

.. _dashboard:

仪表盘
*********

可以生成一个 HTML 仪表盘，将各种工具输出和产物整合到一个简单视图中。除构建结果的基本摘要外，还包括以下详细信息：

* 完整的内存报告（ram、rom），以可钻取（drill-down）表格形式呈现，以及 :ref:`图表 <footprint_tools_plot>`（对应 ``footprint``、``ram_plot`` 和 ``rom_plot`` 构建目标）。
* Kconfig 符号的值和来源（对应 ``traceconfig`` 构建目标）。
* 带函数名的初始化级别（init-levels），以及关于 sys-init 相对于设备树（devicetree）存在任何优先级问题的报告（对应 ``initlevels`` 构建目标）。
* 可导航的设备树视图，包含属性值以及来自任何绑定（bindings）的详细信息。

在你的开发板上使用 ``dashboard`` 目标，如以下示例所示。如果你正在使用 :ref:`sysbuild`，请参见 :ref:`sysbuild_dedicated_image_build_targets`。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: dashboard

这将生成以下输出文件并在默认浏览器中打开它::

    build/dashboard/index.html

.. image:: dashboard.webp
   :align: center
   :alt: Dashboard
