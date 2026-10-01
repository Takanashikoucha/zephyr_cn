:orphan:

.. _glossary:

术语表
#################

.. glossary::
   :sorted:

   API
      （应用程序编程接口，Application Program Interface）
      用于构建应用软件的一组定义好的例程和协议。

   application
      应用：用户提供的文件集合，Zephyr 构建系统使用它来为指定的板级配置构建应用镜像。
      它可包含应用专属代码、内核配置设置，以及至少一个 CMakeLists.txt 文件。
      应用的内核配置设置指导构建系统创建一个自定义内核，
      高效利用板级资源。如果应用不需要任何板级专属能力，
      有时可以为多于一种板级配置（包括不同 CPU 架构的板）
      构建同一个应用。

   application image
      应用镜像：由其所构建的目标板加载并执行的二进制文件。
      每个应用镜像同时包含应用代码和支持它所需的
      Zephyr 内核代码，二者被编译为单个完全链接的二进制文件。
      应用镜像加载到板级后，镜像接管系统、初始化系统，
      并作为系统唯一的应用运行。应用代码和内核代码
      都在单个共享地址空间内作为特权代码执行。

   architecture
      体系结构：指令集架构（ISA）以及一个编程模型。

   board
      板级：具有明确定义的设备与能力集合、可加载并执行应用镜像的
      目标系统。它可以是真实的硬件系统，也可以是运行在
      QEMU 下的模拟系统。一块板可包含一个或多个 :term:`SoCs <SoC>`。
      Zephyr 内核支持 :ref:`多种板级 <boards>`。

   board configuration
      板级配置：一组内核配置选项，指定板级上存在的设备如何被内核使用。
      Zephyr 构建系统为它支持的每块板定义一个或多个板级配置。
      构建系统指定的内核配置设置可被应用覆盖（如需要）。

   board name
      板名：:term:`board` 的人类可读名称。唯一且具描述性地标识某个
      特定系统，但不包含实际为其构建 Zephyr 镜像可能需要的
      附加信息。更多细节参见 :ref:`board_terminology`。

   board qualifiers
      板级限定符：紧跟在 :term:`board name`（以及可选的 :term:`board revision`）之后、
      由正斜线（``/``）分隔的一组附加标记，共同构成
      :term:`board target`。当前接受的限定符为
      :term:`SoC`、:term:`CPU cluster` 和 :term:`variant`。
      更多细节参见 :ref:`board_terminology`。

   board revision
      板级修订版本：可选的版本字符串，标识硬件系统的某个特定修订版本。
      当硬件系统引入微小变更时，这有助于避免板级文件重复。
      更多信息参见 :ref:`porting_board_revisions` 与
      :ref:`application_board_version`。

   board target
      板级目标：可提供给任何 Zephyr 构建工具、用于为特定硬件系统
      编译链接镜像的完整字符串。该字符串唯一标识
      :term:`board name`、:term:`board revision` 与
      :term:`board qualifiers` 的组合。
      更多细节参见 :ref:`board_terminology`。

   CPU cluster
      CPU 簇：一组一个或多个 :term:`CPU cores <CPU core>`，全部在相同地址空间内
      以对称（SMP）配置执行同一镜像。只有相同
      :term:`architecture` 的 :term:`CPU cores <CPU core>` 才能位于同一个簇中。
      多个 CPU 簇（每个含一个或多个核心）可在同一
      :term:`SoC` 中共存。

   CPU core
      CPU 核心：单个处理单元，拥有自己的程序计数器，顺序执行程序指令。
      CPU 核心属于 :term:`CPU cluster`，一个簇可包含一个或多个核心。

   device runtime power management
      设备运行时电源管理（PM）：指设备独立于系统电源状态
      节约能量的能力。设备会记录自身的使用情况，
      并自动被挂起或恢复。该功能通过
      :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME`
      Kconfig 选项启用。

   idle thread
      空闲线程：当没有其他可运行线程时运行的系统线程。

   IDT
      （中断描述符表，Interrupt Descriptor Table）
      x86 架构用于实现中断向量表的数据结构。IDT 用于
      确定对中断和异常的正确响应。

   internal API
      内部 API：在 Zephyr 源码树任何位置定义的内部函数、结构或宏。
      内部 API 用于"扩展" Zephyr，只应在特定
      :term:`software components <software
      component>` 之间使用，通常在内树中，
      某些情况下在树外（例如添加树外架构或驱动）。
      应用不得在其自身作用域之外调用内部 API。
      API 被调用或实现的上下文是明确定义的。
      例如，以 ``arch_`` 为前缀的函数供 Zephyr 内核
      调用架构专属代码使用。内部 API 大体保持稳定，
      但保证程度低于 :term:`public APIs <public API>`。

   ISR
      （中断服务例程，Interrupt Service Routine）
      又称中断处理程序，ISR 是一个回调函数，其执行由
      硬件中断（或软件中断指令）触发，用于处理需要中断
      处理器上当前执行代码的高优先级条件。

   kernel
      内核：实现 Zephyr 内核的 Zephyr 提供的文件集合，
      包括其核心服务、设备驱动、网络协议栈等。

   power domain
      电源域：一组设备的集合，其供电在单次操作中
      被集体施加和移除。电源域由 :c:struct:`device` 表示。

   power gating
      电源门控：通过关闭集成电路中未使用区域来降低功耗。

   private API
      私有 API：在 Zephyr 源码树任何位置定义的、只供其定义的
      :term:`software component` 内部使用的函数、结构或宏。
      私有 API 随时可能变化，对应软件组件之外的代码不得使用。

   public API
      公开 API：在 ``include/zephyr`` 文件夹内定义的、未被显式标记为私有的
      任何函数、结构或宏。公开 API 供任何内树或树外
      :term:`software
      components <software component>` 使用。
      公开 API 若不遵循 :ref:`API lifecycle
      <api_lifecycle>` 一节所述规定，则不可被修改，
      这意味着它们提供随时间保持稳定的保证。

   SoC
      片上系统（System on a chip）：
      即包含至少一个 :term:`CPU cluster`（进而含至少一个 :term:`CPU core`）
      以及外设和内存的集成电路。

   SoC family
      SoC 家族：一个或多个 :term:`SoCs <SoC>` 或 :term:`SoC series`，
      它们共享足够多的共同点，被视为相关并归于同一个家族名称之下。

   SoC series
      SoC 系列：若干个特性与功能相似的 :term:`SoCs <SoC>`，
      厂商通常将它们一起命名和营销。

   software component
      软件组件：Zephyr 源代码中自包含、模块化且可替换的部分。
      驱动、子系统或应用都是 Zephyr 中软件组件的示例。

   subsystem
      子系统：操作系统中逻辑上独立的部分，
      负责特定功能或提供特定服务。

   system power state
      系统电源状态：描述整个系统的功耗。
      系统电源状态由 :c:enum:`pm_state` 表示。

   variant
      变体：在 :term:`board qualifiers` 的上下文中，变体指定
      :term:`SoC` 与 :term:`CPU cluster` 组合的构建的
      特定类型或配置。variant 概念的常见用途包括
      为支持可信执行环境（TEE）的平台同时引入安全
      与非安全构建，或选择构建中使用的 RAM 类型。

   west
      west：为 Zephyr 项目开发的多仓库元工具。参见 :ref:`west`。

   west installation
      west 安装：west 0.7 之前使用的 :term:`west workspace` 的过时术语。

   west manifest
      west 清单：一个 YAML 文件，通常命名为 :file:`west.yml`，
      描述组成 :term:`west workspace` 的项目（即 Git 仓库）
      以及附加元数据。总体信息参见 :ref:`west-basics`，
      细节参见 :ref:`west-manifests`。

   west manifest repository
      west 清单仓库：:term:`west workspace` 中包含 :term:`west manifest` 的
      Git 仓库。其位置由 :ref:`manifest.path
      配置选项 <west-config-index>` 给出。参见 :ref:`west-basics`。

   west project
      west 项目：:term:`west manifest` 中的各个条目，描述一个将在处理
      对应 :term:`west manifest repository` 时被 west
      克隆和管理的 Git 仓库。注意 west 项目不同于
      :term:`zephyr module`，尽管许多项目同时也是模块。
      更多信息参见 :ref:`west-manifests-projects`。

   west workspace
      west 工作区：系统中带有 :file:`.west` 子目录且其中包含
      :term:`west manifest repository` 的文件夹。
      通过 ``west init`` 命令创建 west 工作区，
      即可把 Zephyr 源码及其 :term:`west projects <west project>`
      的源码克隆到系统上。参见 :ref:`west-basics`。

   XIP
      （原地执行，eXecute In Place）
      直接从长期存储执行程序的方法，而非将其复制到 RAM，
      从而把可写内存留给动态数据而非静态程序代码。

   zephyr module
      Zephyr 模块：包含 :file:`zephyr/module.yml` 文件的 Git 仓库，
      供 Zephyr 构建系统将模块的源代码和配置文件
      集成到常规 Zephyr 构建中。Zephyr 模块可以是
      west 项目，但不必须。更多细节参见 :ref:`modules`。

.. _System on a chip: https://en.wikipedia.org/wiki/System_on_a_chip
