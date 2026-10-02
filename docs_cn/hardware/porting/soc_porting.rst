.. _soc_porting_guide:

SoC 移植指南
###################

本页描述如何在 Zephyr 中为新的 :term:`SoC` 添加支持，无论是在上游 Zephyr 项目中还是在本地你自己的仓库中。

SoC 定义
***************

假设你已经熟悉 Zephyr 中的板级（board）概念。硬件支持层级以及 Zephyr 文档中所用术语的高层概述，参见 :ref:`hw_support_hierarchy`。

对于 SoC 移植，最重要的术语是：

- SoC：板级 CPU 所属的精确片上系统。
- SoC 系列（series）：一组紧密相关的 SoC。
- SoC 家族（family）：具有相似特征的更广泛的 SoC 组。
- CPU 簇（cluster）：一个或多个 CPU 核心组成的簇。
- CPU 核心（core）：给定架构的某个 CPU 实例。
- 架构（Architecture）：指令集架构。

架构
============

参见 :ref:`architecture_porting_guide`。


创建你的 SoC 目录
*************************

每个 SoC 必须有唯一名称。请使用 SoC 厂商给出的官方名称，并检查该名称尚未被使用。在某些情况下，其他人可能已经贡献了名称完全相同的 SoC。如果 SoC 名称已被占用，那么你应当改进现有的 SoC，而不是新建一个。脚本 ``list_hardware`` 可用于检索 Zephyr 中所有已知 SoC 的列表，例如在 Zephyr 根目录下执行 ``./scripts/list_hardware.py --soc-root=. --socs`` 即可获取已在使用中的名称列表。

首先创建目录 ``zephyr/soc/<VENDOR>/soc1``，其中 ``<VENDOR>`` 是你的厂商子目录。

.. note::
   如果要将你的 SoC 贡献到 Zephyr，``<VENDOR>`` 子目录是必需的；但如果你的 SoC 放在本地仓库中，则 ``<your-repo>/soc`` 之下任何文件夹结构都是允许的。
   ``<VENDOR>`` 子目录必须匹配 :zephyr_file:`dts/bindings/vendor-prefixes.txt` 列表中定义的厂商。如果该 SoC 厂商在列表中没有前缀，则必须创建一个。

.. note::

   SoC 目录名称不需要与 SoC 名称一致。多个 SoC 甚至可以定义在同一个目录中。在 Zephyr 中，SoC 通常按共同的 SoC 家族或 SoC 系列组织在子文件夹中。

你的 SoC 目录应如下所示：

.. code-block:: none

   soc/<VENDOR>/<soc-name>
   ├── soc.yml
   ├── soc.h
   ├── CMakeLists.txt
   ├── Kconfig
   ├── Kconfig.soc
   └── Kconfig.defconfig

请将 ``<soc-name>`` 替换为你的 SoC 名称。


必需文件如下：

#. :file:`soc.yml`：描述 SoC 高层元数据的 YAML 文件，例如：

   - SoC 名称：该 SoC 的名称
   - CPU 簇：如果该 SoC 包含一个或多个 CPU 簇
   - SoC 系列：该 SoC 所属的 SoC 系列
   - SoC 家族：该系列所属的 SoC 家族

#. :file:`soc.h`：可用于描述或提供 SoC 配置宏的头部文件。:file:`soc.h` 通常被 Zephyr 中的驱动程序、子系统、板级及其他源代码包含。

#. :file:`Kconfig.soc`：基础 SoC 配置，定义形如 ``config SOC_<soc-name>`` 的 Kconfig SoC 符号，并向 Kconfig ``SOC`` 设置提供 SoC 名称。如果 ``soc.yml`` 描述了 SoC 家族和系列，则它们也必须在此文件中定义。SoC 树之外的 Kconfig 设置不得被选择。要选择通用的 Zephyr Kconfig 设置，必须使用 :file:`Kconfig` 文件。

#. :file:`CMakeLists.txt`：由 Zephyr 构建系统加载的 CMake 文件。此 CMake 文件可以定义当构建目标指向该 SoC 时使用的附加包含路径和/或源文件。此外还必须定义要使用的基础链接脚本。

可选文件如下：

- :file:`Kconfig`、:file:`Kconfig.defconfig`：以 :ref:`kconfig` 格式编写的软件配置。这些文件用于选择可用的架构和外设。

编写你的 SoC YAML
*********************

SoC YAML 文件在高层描述 SoC 家族、SoC 系列和 SoC。

详细配置（如硬件描述和配置）在设备树（devicetree）和 Kconfig 中完成。

仅包含一个 SoC 的简单 SoC YAML 文件骨架如下：

.. code-block:: yaml

   socs:
     - name: <soc1>

可以在同一个 SoC 文件夹中放置多个 SoC。
例如，如果它们属于共同的家族或系列，建议将这些 SoC 放在共同的目录树中。
同一文件夹中的多个 SoC 和 SoC 系列可以在 :file:`soc.yml` 文件中描述为：

.. code-block:: yaml

   family:
     - name: <family-name>
       series:
         - name: <series-1-name>
           socs:
             - name: <soc1>
               cpuclusters:
                 - name: <coreA>
                 - name: <coreB>
                   ...
             - name: <soc2>
         - name: <series-2-name>
           ...


编写你的 SoC 设备树
*************************

SoC 设备树包含文件位于 :file:`<zephyr-repo>/dts` 文件夹下对应的 :file:`<ARCH>/<VENDOR>` 中。

SoC 的 :file:`dts/<ARCH>/<VENDOR>/<soc>.dtsi` 以设备树源（DTS）格式描述你的 SoC 硬件，且必须被使用该 SoC 的所有板级包含。

如果存在高层的 :file:`<arch>.dtsi` 文件，那么一个好的起点是在你的 :file:`<soc>.dtsi` 中包含该文件。

一般来说，:file:`<soc>.dtsi` 应如下所示：

.. code-block:: devicetree

   #include <arch>/<arch>.dtsi

   / {
           chosen {
                   /* 你的 SoC 的通用 chosen 设置 */
           };

           cpus {
                   #address-cells = <m>;
                   #size-cells = <n>;

                   cpu@0 {
                   device_type = "cpu";
                   compatible = "<compatibles>";
                   /* ... 你的 CPU 定义 ... */
           };

           soc {
                   /* 你的 SoC 定义和外设 */
                   /* 例如 ram、时钟、总线、外设。 */
           };
   };

.. hint::
   可以将多个 :file:`<VENDOR>/<soc>.dtsi` 文件组织在子目录中，以获得更清晰的文件系统结构。例如按 SoC 系列组织，如下所示：:file:`<VENDOR>/<SERIES>/<soc>.dtsi`。


多个 CPU 簇
=====================

设备树反映硬件。一个 CPU 簇可用的内存空间和外设可能与另一个 CPU 簇大不相同，因此每个 CPU 簇通常拥有自己的 :file:`.dtsi` 文件。

CPU 簇的 :file:`.dtsi` 文件应遵循 :file:`<soc>_<cluster>.dtsi` 命名方案。:file:`<soc>_<cluster>.dtsi` 文件看起来类似于不含 CPU 簇的 SoC :file:`.dtsi`。

编写 Kconfig 文件
*******************

Zephyr 使用 Kconfig 语言配置软件功能。在能为你的 SoC 编译 Zephyr 应用之前，它必须提供一些 Kconfig 设置。

设置 Kconfig 配置值的方法在 :ref:`setting_configuration_values` 中有详细说明。

SoC 目录中有一个必需的 Kconfig 文件，以及两个可选文件：

.. code-block:: none

   soc/<vendor>/<your soc>
   ├── Kconfig.soc
   ├── Kconfig
   └── Kconfig.defconfig

:file:`Kconfig.soc`
   可被 Zephyr Kconfig 和 sysbuild Kconfig 树共同引用的共享 Kconfig 文件。

   此文件在 Kconfig 树中选择 SoC 家族和系列，以及潜在的其他 SoC 相关 Kconfig 设置，某些情况下还包括 SOC_PART_NUMBER。此文件不得选择可复用 Kconfig SoC 树之外的任何内容。

   :file:`Kconfig.soc` 可能如下所示：

   .. code-block:: kconfig

      config SOC_FAMILY_<SOC_FAMILY_NAME>
              bool

      config SOC_SERIES_<SOC_SERIES_NAME>
              bool
              select SOC_FAMILY_<SOC_FAMILY_NAME>

      config SOC_<SOC_NAME>
              bool
              select SOC_SERIES_<SOC_SERIES_NAME>

      config SOC_FAMILY
              default "<soc_family_name>" if SOC_FAMILY_<SOC_FAMILY_NAME>

      config SOC_SERIES
              default "<soc_series_name>" if SOC_SERIES_<SOC_SERIES_NAME>

      config SOC
              default "<soc_name>" if SOC_<SOC_NAME>

   注意 ``SOC_NAME`` 是 SoC 名称的纯大写版本，``SOC_SERIES_NAME`` 是 SoC 系列名称的纯大写版本，``SOC_FAMILY_NAME`` 是 SoC 家族名称的纯大写版本。如果这些字段不出现在 :file:`soc.yml` 文件中，那么它们也不应出现在 :file:`Kconfig.soc` 文件中。

   Kconfig 设置 ``SOC``、``SOC_SERIES`` 和 ``SOC_FAMILY`` 全局定义为字符串，因此 :file:`Kconfig.soc` 文件应只定义默认字符串值而不定义类型。注意字符串值必须与 :file:`soc.yml` 文件中使用的值一致。

.. note::
   构建系统支持 ``soc_name``、``soc_series_name`` 和 ``soc_family_mame`` 的任何大小写变体，但在向 Zephyr 本身提交板级以供收录时，这些必须是 Kconfig 名称的纯小写版本

:file:`Kconfig`
   由 :zephyr_file:`soc/Kconfig` 包含。

   此文件可以添加特定于当前 SoC 的 Kconfig 设置。

   :file:`Kconfig` 通常用形如 ``HAS_<support>`` 的设置来指示对给定硬件的支持。

   .. code-block:: kconfig

      config SOC_<SOC_NAME>
              select ARM
              select CPU_HAS_FPU

   如果设置名称与 Zephyr 中现有的 Kconfig 设置相同，且仅修改该设置的默认值，那么应改用 :file:`Kconfig.defconfig`。

:file:`Kconfig.defconfig`
   Kconfig 选项的 SoC 特定默认值。

   并非所有 SoC 都有 :file:`Kconfig.defconfig` 文件。

   整个文件应位于一对 ``if SOC_<SOC_NAME>`` / ``endif`` 或 ``if SOC_SERIES_<SERIES_NAME>`` / ``endif`` 之内，如下所示：

   .. code-block:: kconfig

      if SOC_<SOC_NAME>

      config NUM_IRQS
              default 32

      endif # SOC_<SOC_NAME>

多个 CPU 簇
=====================

CPU 簇必须在 :file:`Kconfig.soc` 文件中提供额外的 Kconfig 设置。这通常以 ``SOC_<SOC_NAME>_<CLUSTER>`` 的形式出现，因此对于给定的 ``soc1`` 及其两个簇 ``clusterA`` 和 ``clusterB``，应如下所示：

当 SoC 定义了 CPU 簇时的 SoC

  .. code-block:: kconfig

     config SOC_SOC1_CLUSTERA
             bool
             select SOC_SOC1

     config SOC_SOC1_CLUSTERB
             bool
             select SOC_SOC1
