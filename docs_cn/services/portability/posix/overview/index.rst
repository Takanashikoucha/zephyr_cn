.. _posix_overview:

概述
########

可移植操作系统接口（Portable Operating System Interface，POSIX）是一族由 `IEEE Computer Society`_ 制定的标准，用于维护操作系统之间的兼容性。Zephyr 实现了 `IEEE 1003.1-2017`_（也称为 POSIX-1.2017）所规定的标准 POSIX API 的一个子集。

..  figure:: posix.svg
    :align: center
    :alt: Zephyr 中的 POSIX 支持

    Zephyr 中的 POSIX 支持

.. note::
   本页面不介绍 Zephyr 的 :ref:`POSIX 架构<Posix arch>`，该架构用于在宿主操作系统下将 Zephyr 作为本地应用运行，用于原型设计、测试和诊断目的。

借助 Zephyr 中可用的 POSIX 支持，现有的符合 POSIX 标准的应用可以移植到 Zephyr 内核上运行，从而利用 Zephyr 的特性和功能。此外，设计为符合 POSIX 标准的库可以不经过任何修改就移植到基于 Zephyr 内核的应用中。

POSIX API 是物联网和嵌入式应用中日益流行的 OSAL（操作系统抽象层），Zephyr、AWS:FreeRTOS、TI-RTOS 和 NuttX 中都可以看到这一点。

Zephyr 中 POSIX 支持的好处包括：

- 为不熟悉嵌入式开发的程序员（尤其是来自 Linux 的程序员）提供熟悉的 API
- 实现基于 POSIX API 的现有库的复用（可移植性）
- 提供适合小型（MCU）嵌入式系统的高效 API 子集

.. _posix_subprofiles:

POSIX 子配置档（Subprofiles）
=================

虽然 Zephyr 支持运行多个 :ref:`线程 <threads_v2>`（可能采用 :ref:`SMP <smp_arch>` 配置），也支持 :ref:`虚拟内存和 MMU <memory_management_api>`，但 Zephyr 的代码和数据通常共享一个被划分为多个独立 :ref:`内存域 <memory_domain>` 的公共地址空间。Zephyr 内核可执行代码和应用可执行代码通常被编译到同一个二进制产物中。从这个角度看，Zephyr 应用可以被视为运行在单进程的上下文中。

虽然多用途操作系统（OS）提供完整的 POSIX 兼容性，但像 Zephyr 这样的实时操作系统（RTOS）通常服务于固定用途，硬件资源有限，用户交互也有限。在这样的系统中，完整的 POSIX 兼容性可能既不实际也没有必要。

因此，POSIX 将以下 :ref:`应用环境配置档（AEP）<posix_aep>` 定义为 `IEEE 1003.13-2003`_（也称为 POSIX.13-2003）的一部分。每个 AEP 都在必需的 :ref:`POSIX 系统接口 <posix_system_interfaces>` 之上增量地添加更多特性。

..  figure:: aep.svg
    :align: center
    :scale: 150%
    :alt: POSIX 应用环境配置档（AEP）

    POSIX 应用环境配置档（AEP）

* 最小实时系统配置档（Minimal Realtime System Profile，:ref:`PSE51 <posix_aep_pse51>`）
* 实时控制器系统配置档（Realtime Controller System Profile，:ref:`PSE52 <posix_aep_pse52>`）
* 专用实时系统配置档（Dedicated Realtime System Profile，:ref:`PSE53 <posix_aep_pse53>`）
* 多用途实时系统（Multi-Purpose Realtime System，PSE54）

POSIX.13-2003 AEP 于 2003 年通过"功能单元（Units of Functionality）"正式确立，但该规范现已停止维护（仅供参考）。尽管如此，其意图仍通过 :ref:`选项<posix_options>` 和 :ref:`选项组<posix_option_groups>` 作为 POSIX-1.2017 的一部分得以保留。

更多信息请参考 `IEEE 1003.1-2017, Section E, Subprofiling Considerations`_。

.. _posix_apps:

Zephyr 中的 POSIX 应用
===========================

Zephyr 中的 POSIX 应用与 :ref:`其他应用一样构建<application>`，因此需要常规的 :file:`prj.conf`、:file:`CMakeLists.txt` 和源代码。例如，下面的应用使用了 ``nanosleep()`` 和 ``perror()`` POSIX 函数。

.. code-block:: cfg
   :caption: Zephyr 中简单 POSIX 应用的 `prj.conf`

   CONFIG_POSIX_API=y

.. code-block:: c
   :caption: 使用 Zephyr POSIX API 的简单应用

   #include <stddef.h>
   #include <stdio.h>
   #include <time.h>

   void megasleep(size_t megaseconds)
   {
       struct timespec ts = {
           .tv_sec = megaseconds * 1000000,
           .tv_nsec = 0,
       };

       printf("See you in a while!\n");
       if (nanosleep(&ts, NULL) == -1) {
           perror("nanosleep");
       }
   }

   int main()
   {
       megasleep(42);
       return 0;
   }

有关 POSIX 应用的更多示例，请参考 :zephyr:code-sample-category:`POSIX 示例应用<posix>`。

.. _posix_config:

配置
=============

与 Zephyr 中的大多数特性一样，POSIX 特性 :ref:`高度可配置<zephyr_intro_configurability>`，但默认禁用。用户必须通过 :ref:`Kconfig<kconfig>` 选择显式启用 POSIX 选项。

子配置档
+++++++++++

启用以下 Kconfig 选项之一，即可快速配置一个预定义的 :ref:`POSIX 子配置档 <posix_subprofiles>`。

* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_BASE` (:ref:`Base <posix_system_interfaces_required>`)
* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE51` (:ref:`PSE51 <posix_aep_pse51>`)
* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE52` (:ref:`PSE52 <posix_aep_pse52>`)
* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE53` (:ref:`PSE53 <posix_aep_pse53>`)

根据需要，还可以通过 Kconfig 启用附加的 POSIX :ref:`选项和选项组 <posix_option_groups>`（例如 ``CONFIG_POSIX_C_LIB_EXT=y``）。进一步微调可通过 :ref:`附加的 POSIX 相关 Kconfig 选项 <posix_kconfig_options>` 实现。

今后，子配置档、选项和选项组应被视为在 Zephyr 中配置 POSIX 的首选方式。

遗留
++++++

历史上，Zephyr 使用 :kconfig:option:`CONFIG_POSIX_API` 来配置一组 POSIX 特性，该选项被过度使用且规模不断膨胀。

* :kconfig:option:`CONFIG_POSIX_API`

该选项现已冻结，可视为等价于以下选项的组合：

* :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_PSE51`
* :kconfig:option:`CONFIG_POSIX_FD_MGMT`
* :kconfig:option:`CONFIG_POSIX_MESSAGE_PASSING`
* :kconfig:option:`CONFIG_POSIX_NETWORKING`

但是，:kconfig:option:`CONFIG_POSIX_API` 应视为遗留选项，不应在新的 Zephyr 应用中使用。

.. _IEEE: https://www.ieee.org/
.. _IEEE Computer Society: https://www.computer.org/
.. _IEEE 1003.1-2017: https://standards.ieee.org/ieee/1003.1/7101/
.. _IEEE 1003.13-2003: https://standards.ieee.org/ieee/1003.13/3322/
.. _IEEE 1003.1-2017, Section E, Subprofiling Considerations:
   https://pubs.opengroup.org/onlinepubs/9699919799/xrat/V4_subprofiles.html
