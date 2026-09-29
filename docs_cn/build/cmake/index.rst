.. _cmake-details:

构建系统（CMake）
*******************


CMake 用于将你的应用与 Zephyr 内核一起构建。CMake 构建分为两个阶段。第一个阶段称为
**配置**。在配置期间，CMakeLists.txt 构建脚本被执行。配置完成后，CMake 拥有 Zephyr
构建的内部模型，并可以生成适用于宿主平台的原生构建脚本。

CMake 支持为多种构建系统生成脚本，但 Zephyr 只测试并支持 Ninja 和 Make。配置完成后，
通过执行生成的构建脚本即可开始**构建**阶段。在大多数代码更改之后，这些构建脚本可以在
不涉及 CMake 的情况下重新编译应用。但在某些更改之后，必须在构建之前重新执行配置步骤。
构建脚本可以检测其中一些情况并自动重新配置，但也有一些情况必须手动处理。

Zephyr 使用 CMake 的“target”（构建目标）概念来组织构建。target 可以是可执行文件、
库或生成的文件。对于应用开发者而言，库 target 是最需要理解的。所有进入 Zephyr 构建
的源代码，包括应用代码在内，都是通过包含在库 target 中实现的。

库 target 的源代码通过如下 CMakeLists.txt 构建脚本添加：

.. code-block:: cmake

   target_sources(app PRIVATE src/main.c)

在上面的 :file:`CMakeLists.txt` 中，一个名为 ``app`` 的现有库 target 被配置为包含源
文件 :file:`src/main.c`。``PRIVATE`` 关键字表示我们在修改该库的内部构建方式。使用
``PUBLIC`` 关键字则会修改与 app 链接的其他库的构建方式。在这种情况下，使用 ``PUBLIC``
会导致与 ``app`` 链接的库也包含源文件 :file:`src/main.c`，这显然不是我们想要的行为。
不过在修改 target 库的 include 路径时，``PUBLIC`` 关键字可能派上用场。

在引入 CMake 构建系统代码或添加新的 CMake 文件时，请遵循 :ref:`此处 <cmake-style>`
概述的风格指南。

:ref:`cmake-reference` 章节提供了 Zephyr 使用且可供应用开发者使用的所有 CMake 命令、
变量和模块的参考。

构建与配置阶段
==============================

Zephyr 构建过程可分为两个主要阶段：配置阶段（由 CMake 驱动）和构建阶段（由 Make 或
Ninja 驱动）。

.. _build_configuration_phase:

配置阶段
-------------------

配置阶段在用户调用 *CMake* 生成构建系统时开始，此时需指定源应用目录和板级目标。

.. figure:: build-config-phase.svg
    :align: center
    :alt: Zephyr 的构建配置阶段
    :figclass: align-center
    :width: 80%

CMake 从处理应用目录中的 :file:`CMakeLists.txt` 文件开始，该文件引用 Zephyr 顶层目录
中的 :file:`CMakeLists.txt` 文件，后者进而（直接和间接地）引用整个构建树中的
:file:`CMakeLists.txt` 文件。其主要输出是一组用于驱动构建过程的 Makefile 或 Ninja
文件，但 CMake 脚本也会做一些自身的处理，下文将对此进行说明。

注意，下文以 :file:`build/` 开头的路径指的是你运行 CMake 时创建的构建目录。

Devicetree
    :file:`*.dts`（*devicetree 源文件*）和 :file:`*.dtsi`（*devicetree 源包含文件*）
    从目标的架构、SoC、板级和应用目录中收集而来。

    :file:`*.dtsi` 文件通过 C 预处理器（常缩写为 *cpp*，注意不要与 C++ 混淆）被
    :file:`*.dts` 文件包含。C 预处理器还用于合并所有 devicetree
    :file:`*.overlay` 文件，并展开 :file:`*.dts`、:file:`*.dtsi` 和
    :file:`*.overlay` 文件中的宏。预处理器输出被放在
    :file:`build/zephyr/zephyr.dts.pre` 中。

    经过预处理的 devicetree 源文件由
    :zephyr_file:`gen_defines.py <scripts/dts/gen_defines.py>` 解析，以生成带有
    预处理器宏的 :file:`build/zephyr/include/generated/zephyr/devicetree_generated.h`
    头文件。

    源代码应通过包含 :zephyr_file:`devicetree.h <include/zephyr/devicetree.h>`
    头文件来访问由 devicetree 生成的预处理器宏，该头文件包含了
    :file:`devicetree_generated.h`。

    :file:`gen_defines.py` 还会将最终的 devicetree 写入构建目录中的
    :file:`build/zephyr/zephyr.dts`。该文件的内容对调试可能有用。

    如果安装了 devicetree 编译器 ``dtc``，它会针对
    :file:`build/zephyr/zephyr.dts` 运行，以捕获该工具产生的额外警告和错误。
    ``dtc`` 的输出在其他方面不会被使用，如果未安装 ``dtc``，则跳过此步骤。

    以上只是简要概述。有关 devicetree 的更多信息，请参见
    :ref:`dt-guide`。

Kconfig
    :file:`Kconfig` 文件定义了目标架构、SoC、板级和应用可用的配置选项，以及选项
    之间的依赖关系。

    Kconfig 配置存储在*配置文件*中。初始配置由合并板级和应用的配置片段（例如
    :file:`prj.conf`）生成。

    Kconfig 的输出是一个带有预处理器赋值的 :file:`autoconf.h` 头文件，以及一个
    既作为已保存配置又作为配置输出（供 CMake 使用）的 :file:`.config` 文件。
    :file:`autoconf.h` 中的定义在编译时会自动暴露，因此无需包含该头文件。

    devicetree 中的信息可通过
    :zephyr_file:`kconfigfunctions.py
    <scripts/kconfig/kconfigfunctions.py>` 中定义的函数供 Kconfig 使用。

    有关更多信息，请参见 :ref:`手册中的 Kconfig 章节 <kconfig>`。

构建阶段
-----------

构建阶段在用户调用 ``make`` 或 ``ninja`` 时开始。其最终输出是一个完整的 Zephyr 应用，
其格式适合加载/烧写到目标板（:file:`zephyr.elf`、:file:`zephyr.hex` 等）。从概念上
讲，构建阶段可以细分为四个阶段：预构建、第一遍二进制、最终二进制和后处理。

预构建
+++++++++

预构建发生在任何源文件被编译之前，因为在此阶段会生成源文件所使用的头文件。

构建时常量生成
    某些常量必须从 C 结构体布局在构建时派生，而不是硬编码。CMake 函数
    ``zephyr_constants_library()`` 自动完成这一过程：它将一个包含
    ``GEN_ABSOLUTE_SYM()`` 声明的 C 源文件编译为 OBJECT 库，然后运行
    ``gen_offset_header.py`` 提取以 ``_OFFSET`` 或 ``_SIZEOF`` 结尾的符号，
    并将其作为 ``#define`` 行输出到 ``include/generated/zephyr/`` 下生成的
    头文件中。

    该机制在两处使用：

    - **offsets.h**：供汇编代码使用的架构相关偏移量，当这些结构的定义无法
      直接访问时，汇编代码需要访问高层数据结构。源文件为
      ``arch/<arch>/core/offsets/offsets.c``。

    - **heap_constants.h**：堆尺寸常量（``Z_HEAP_MIN_SIZE``、
      ``Z_HEAP_MIN_SIZE_FOR``），根据实际的堆结构体布局计算得出，取代了
      此前在 ``kernel.h`` 中硬编码的值。源文件为
      ``lib/heap/heap_constants.c``。

    要添加新的构建时常量，请创建一个包含 ``<gen_offset.h>`` 并使用
    ``GEN_ABSOLUTE_SYM()`` 声明每个常量的 C 源文件，然后在你的
    ``CMakeLists.txt`` 中调用 ``zephyr_constants_library()``。如果新库的源文件
    包含了由另一个常量库生成的头文件，请使用 ``DEPENDS`` 参数声明该顺序
    （例如 ``DEPENDS heap_constants``）。生成的 OBJECT 库也可以链接到最终
    二进制中（就像 offsets.h 在链接脚本中通过
    ``$<TARGET_OBJECTS:offsets>`` 所做的那样）。

系统调用样板代码
    *gen_syscall.py* 和 *parse_syscalls.py* 脚本协同工作，将潜在的系统调用
    函数与其实现绑定在一起。

.. figure:: build-build-phase-1.svg
    :align: center
    :alt: Zephyr 的构建阶段 I
    :figclass: align-center
    :width: 80%

中间二进制
+++++++++++++++++++++

真正的编译从第一个中间二进制开始。源文件（C 和汇编）从各个子系统收集而来
（收集哪些子系统在配置阶段决定），并编译为归档（引用树中的头文件，以及配置
阶段和预构建阶段生成的头文件）。

.. figure:: build-build-phase-2.svg
    :align: center
    :alt: Zephyr 的构建阶段 II
    :figclass: align-center
    :width: 80%

中间二进制的确切数量在配置阶段决定。

如果启用了内存保护，则：

分区分组
    *gen_app_partitions.py* 脚本扫描所有生成的归档，并输出链接脚本，以确保
    应用分区针对目标的内存保护硬件正确分组和对齐。

然后使用 *cpp* 将目标架构/SoC、内核树、（如果启用了内存保护）可选的分区
输出，以及配置过程中选定的其他片段中的链接脚本片段合并为一个 *linker.cmd*
文件。随后按照 *linker.cmd* 中的规定，使用 *ld* 将编译好的归档链接起来。

尺寸未固定的二进制
    当启用 :ref:`usermode_api` 或使用了 :ref:`devicetree` 时，会生成尺寸未固定
    的中间二进制。它生成的二进制尺寸未固定，因此可用于会影响最终二进制尺寸的
    后处理步骤。

.. figure:: build-build-phase-3.svg
    :align: center
    :alt: Zephyr 的构建阶段 III
    :figclass: align-center
    :width: 80%

尺寸已固定的二进制
    当启用 :ref:`usermode_api` 或使用了生成的中断表时，会生成尺寸已固定的
    中间二进制，:kconfig:option:`CONFIG_GEN_ISR_TABLES`
    它生成的二进制尺寸已固定，因此中间二进制与最终二进制之间的尺寸
    不得发生变化。

.. figure:: build-build-phase-4.svg
    :align: center
    :alt: Zephyr 的构建阶段 IV
    :figclass: align-center
    :width: 80%

中间二进制的后处理
+++++++++++++++++++++++++++++++++++++

上一阶段生成的二进制是不完整的，其中包含空白和/或占位符段，必须通过本质上
类似于反射（reflection）的方式填充。

为完成构建过程，以下脚本会作用于中间二进制，以生成最终二进制所需的缺失部分。

当启用 :ref:`usermode_api` 时：

分区对齐
    *gen_app_partitions.py* 脚本扫描尺寸未固定的二进制，生成一个应用共享内存
    对齐的链接脚本片段，其中分区按降序排列。

.. figure:: build-postprocess-1.svg
    :align: center
    :alt: Zephyr 的中间二进制后处理 I
    :figclass: align-center
    :width: 80%

当使用了 :ref:`devicetree` 时：

设备依赖
    *gen_device_deps.py* 脚本扫描尺寸未固定的二进制，确定从 devicetree 数据
    中记录的设备间关系，并将编码的关系替换为针对应用中实际存在的设备优化
    后的值。

.. figure:: build-postprocess-2.svg
    :align: center
    :alt: Zephyr 的中间二进制后处理 II
    :figclass: align-center
    :width: 80%

当启用 :kconfig:option:`CONFIG_GEN_ISR_TABLES` 时：
    *gen_isr_tables.py* 脚本扫描尺寸已固定的二进制，创建一个包含硬件向量表
    和/或软件中断表的 isr_tables.c 源文件。

.. figure:: build-postprocess-3.svg
    :align: center
    :alt: Zephyr 的中间二进制后处理 III
    :figclass: align-center
    :width: 80%

当启用 :ref:`usermode_api` 时：

内核对象哈希
    *gen_kobject_list.py* 扫描 *ELF DWARF* 调试数据，以查找所有内核对象的
    地址。该列表被传给 *gperf*，*gperf* 生成这些地址的完美哈希函数和哈希表，
    然后其输出由 *process_gperf.py* 针对我们特殊场景的已知特性进行优化。

.. figure:: build-postprocess-4.svg
    :align: center
    :alt: Zephyr 的中间二进制后处理 IV
    :figclass: align-center
    :width: 80%

当不需要中间二进制的后处理时，第一个中间二进制将直接用作最终二进制。

最终二进制
++++++++++++

上一阶段生成的二进制是不完整的，其中包含空白和/或占位符段，必须通过本质上
类似于反射（reflection）的方式填充。

上一阶段的链接过程会重复执行，这次将缺失的部分填充完毕。

.. figure:: build-build-phase-5.svg
    :align: center
    :alt: Zephyr 的构建最终阶段
    :figclass: align-center
    :width: 80%

后处理
+++++++++++++++

最后，如有必要，会将完整的内核从 *ELF* 格式转换为目标所需的加载器和/或烧写
工具所期望的格式。这一步使用 *objdump* 即可直接完成。

.. figure:: build-build-phase-6.svg
    :align: center
    :alt: Zephyr 的构建最终阶段后处理
    :figclass: align-center
    :width: 80%


.. _build_system_scripts:

支撑脚本与工具
============================

以下是对构建过程中使用的脚本的详细说明。

.. _gen_syscalls.py:

:zephyr_file:`scripts/build/gen_syscalls.py`
--------------------------------------------

.. include:: ../../../scripts/build/gen_syscalls.py
   :start-after: """
   :end-before: """

.. _gen_device_deps.py:

:zephyr_file:`scripts/build/gen_device_deps.py`
------------------------------------------------

.. include:: ../../../scripts/build/gen_device_deps.py
   :start-after: """
   :end-before: """

.. _gen_kobject_list.py:

:zephyr_file:`scripts/build/gen_kobject_list.py`
------------------------------------------------

.. include:: ../../../scripts/build/gen_kobject_list.py
   :start-after: """
   :end-before: """

.. _gen_offset_header.py:

:zephyr_file:`scripts/build/gen_offset_header.py`
-------------------------------------------------

.. include:: ../../../scripts/build/gen_offset_header.py
   :start-after: """
   :end-before: """

.. _parse_syscalls.py:

:zephyr_file:`scripts/build/parse_syscalls.py`
----------------------------------------------


.. include:: ../../../scripts/build/parse_syscalls.py
   :start-after: """
   :end-before: """

.. _gen_idt.py:

:zephyr_file:`arch/x86/gen_idt.py`
----------------------------------

.. include:: ../../../arch/x86/gen_idt.py
   :start-after: """
   :end-before: """

.. _gen_gdt.py:

:zephyr_file:`arch/x86/gen_gdt.py`
----------------------------------

.. include:: ../../../arch/x86/gen_gdt.py
   :start-after: """
   :end-before: """

.. _gen_relocate_app.py:

:zephyr_file:`scripts/build/gen_relocate_app.py`
------------------------------------------------

.. include:: ../../../scripts/build/gen_relocate_app.py
   :start-after: """
   :end-before: """

.. _process_gperf.py:

:zephyr_file:`scripts/build/process_gperf.py`
---------------------------------------------

.. include:: ../../../scripts/build/process_gperf.py
   :start-after: """
   :end-before: """

:zephyr_file:`scripts/build/gen_app_partitions.py`
--------------------------------------------------

.. include:: ../../../scripts/build/gen_app_partitions.py
   :start-after: """
   :end-before: """

.. _check_init_priorities.py:

:zephyr_file:`scripts/build/check_init_priorities.py`
-----------------------------------------------------

.. include:: ../../../scripts/build/check_init_priorities.py
   :start-after: """
   :end-before: """
