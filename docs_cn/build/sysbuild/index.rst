.. _sysbuild:

Sysbuild（系统构建）
#######################

Sysbuild 是一个更高层的构建系统，可以用来组合多个其他构建系统。
它是一个更高层的层，将一个或多个 Zephyr 构建系统和可选的额外构建系统
组合成一个层次化构建系统。

例如，你可以用 sysbuild 构建一个 Zephyr 应用和 MCUboot 引导加载器，
把它们都烧录到你的设备上，并调试结果。

Sysbuild 通过配置和构建至少一个 Zephyr 应用和可选的任意多个额外项目工作。
额外项目可以是 Zephyr 应用或你想运行的其他类型的构建。

与 Zephyr 的 :ref:`构建系统 <build_overview>` 类似，sysbuild 用 CMake 编写并使用
:ref:`Kconfig <kconfig>`。

定义
***********

以下是本文档使用的一些关键概念：

单镜像构建
    当 sysbuild 用来创建和管理仅一个 Zephyr 应用的构建系统时。

多镜像构建
    当 sysbuild 用来管理多个构建系统时。
    "image"（镜像）一词的使用是因为你的主要目标通常是从每个构建系统
    生成固件应用镜像的二进制文件。

域
    每个由 sysbuild 管理的 Zephyr CMake 构建系统。

多域
    当多于一个 Zephyr CMake 构建系统（域）由 sysbuild 管理时。

架构概览
**********************

这张图是 sysbuild 的输入、输出和用户接口的概览：

.. figure:: sysbuild.svg
   :align: center
   :alt: Sysbuild 架构概览
   :figclass: align-center
   :width: 80%

以下是这张图中指示的一些关键 sysbuild 功能：

- 你可以用 :ref:`west build <west-building>` 或直接通过 ``cmake`` 运行 sysbuild。

- 你可以用 sysbuild 从每个构建系统生成应用镜像，上面显示为 ELF、BIN 和 HEX 文件。

- 你可以用各种配置变量配置 sysbuild 或它管理的任何构建系统。
  这些变量是命名空间的，这样 sysbuild 可以将它们定向到正确的构建系统。
  在某些情况下，如 ``BOARD`` 变量，这些在多个构建系统之间共享。

- Sysbuild 本身也用 Kconfig 配置。例如，你可以指示 sysbuild 构建 MCUboot 引导加载器，
  以及构建和链接你的主 Zephyr 应用作为 MCUboot 可启动镜像，
  用 sysbuild 的 Kconfig 文件。

- Sysbuild 与 west 的 :ref:`west-build-flash-debug` 命令集成。
  它通过管理 :ref:`west-runner`，特别是每个 Zephyr 构建系统将包含的
  :file:`runners.yaml` 文件做到这。
  这些被打包成一个全局视图，描述如何烧录和调试每个构建系统，
  在由 sysbuild 生成和管理的 :file:`domains.yaml` 文件中。

- 构建名称用目标名称和下划线作前缀，例如 sysbuild 目标用 ``sysbuild_`` 作前缀，
  如果 MCUboot 作为 sysbuild 的部分启用，它将用 ``mcuboot_`` 作前缀。
  这也允许运行如 menuconfig 的东西带前缀，例如（如果用 ninja）
  ``ninja sysbuild_menuconfig`` 配置 sysbuild 或（如果用 make）
  ``make mcuboot_menuconfig``。

用 sysbuild 构建
**********************

如上面所述，你可以通过 ``west build`` 或 ``cmake`` 运行 sysbuild。

.. tabs::

   .. group-tab:: ``west build``

      这里是一个示例。细节见 ``west build 文档`` 中的 :ref:`west-multi-domain-builds`。

      .. zephyr-app-commands::
         :tool: west
         :zephyr-app: samples/hello_world
         :board: reel_board
         :goals: build
         :west-args: --sysbuild
         :compact:

      .. tip::

         要从现在起配置 ``west build`` 默认使用 ``--sysbuild``，运行：

         .. code-block:: shell

            west config build.sysbuild True

         由于 sysbuild 支持单镜像和多镜像构建，这让你可以一直使用 sysbuild，
         不用担心你在运行什么类型的构建。

         要关闭这，在生成你的构建系统之前运行：

         .. code-block:: shell

            west config build.sysbuild False

         要只为一个 ``west build`` 命令关闭这，运行：

         .. code-block:: shell

            west build --no-sysbuild ...

   .. group-tab:: ``cmake``

      这里是一个使用 CMake 和 Ninja 的示例。

      .. zephyr-app-commands::
         :tool: cmake
         :app: share/sysbuild
         :board: reel_board
         :goals: build
         :gen-args: -DAPP_DIR=samples/hello_world
         :compact:

      要直接用 CMake 使用 sysbuild，你必须指定 sysbuild 项目作为源文件夹，
      并给出 ``-DAPP_DIR=<path-to-sample>`` 作为额外的 CMake 参数
      或将 APP_DIR 设置为环境变量。
      ``APP_DIR`` 是 sysbuild 管理的主 Zephyr 应用的路径。

      .. tip::

         环境变量 :cmake:envvar:`CMAKE_BUILD_PARALLEL_LEVEL <envvar:CMAKE_BUILD_PARALLEL_LEVEL>` 和
         :cmake:envvar:`VERBOSE <envvar:VERBOSE>` 可以用于在使用 sysbuild 配合 CMake 和 ninja
         时控制构建过程。

         要为所有 sysbuild 镜像设置 ninja 的作业数，设置
         :cmake:envvar:`CMAKE_BUILD_PARALLEL_LEVEL <envvar:CMAKE_BUILD_PARALLEL_LEVEL>` 环境变量
         并用 ``cmake --build`` 调用构建，例如：

         .. code-block:: shell

            CMAKE_BUILD_PARALLEL_LEVEL=<n> cmake --build .

         要为所有镜像使用详细输出，使用：

         .. code-block:: shell

            VERBOSE=1 cmake --build .


配置命名空间
*************************

在不用 sysbuild 构建单个 Zephyr 应用时，所有作为 ``-D<var>=<value>`` 或
``-DCONFIG_<var>=<value>`` 在命令行给出的 CMake 缓存设置和 Kconfig 构建选项
由 Zephyr 构建系统处理。

但是，当 sysbuild 组合多个 Zephyr 构建系统时，可能有专属于 sysbuild 的
Kconfig 设置（不被任何应用使用）。为处理这，sysbuild 为配置变量有命名空间。
你可以使用这些命名空间将设置定向到 sysbuild 本身或 sysbuild 管理的
特定 Zephyr 应用，使用这些部分中的信息。

下面的示例显示如何构建启用 MCUboot 的 :zephyr:code-sample:`hello_world`，
对两个镜像应用调试优化：

.. tabs::

   .. group-tab:: ``west build``

      .. zephyr-app-commands::
         :tool: west
         :zephyr-app: samples/hello_world
         :board: reel_board
         :goals: build
         :west-args: --sysbuild
         :gen-args: -DSB_CONFIG_BOOTLOADER_MCUBOOT=y -DCONFIG_DEBUG_OPTIMIZATIONS=y -Dmcuboot_CONFIG_DEBUG_OPTIMIZATIONS=y
         :compact:

   .. group-tab:: ``cmake``

      .. zephyr-app-commands::
         :tool: cmake
         :app: share/sysbuild
         :board: reel_board
         :goals: build
         :gen-args: -DAPP_DIR=samples/hello_world -DSB_CONFIG_BOOTLOADER_MCUBOOT=y -DCONFIG_DEBUG_OPTIMIZATIONS=y -Dmcuboot_CONFIG_DEBUG_OPTIMIZATIONS=y
         :compact:

更多信息见以下子节。

.. _sysbuild_cmake_namespace:

CMake 变量命名空间
=========================

CMake 变量设置可以用 ``-D<var>=<value>`` 在命令行传递给 CMake。
你也可以通过 CMake 设置 Kconfig 选项为 ``-DCONFIG_<var>=<value>`` 或
``-D<namespace>_CONFIG_<var>=<value>``。

由于 sysbuild 是构建系统的入口点，且 sysbuild 用 CMake 编写，
所有 CMake 变量首先由 sysbuild 处理。

Sysbuild 为每个域创建命名空间。命名空间前缀是域的应用名称。
更多信息见 :ref:`sysbuild_zephyr_application`。

要在命名空间 ``<namespace>`` 中设置变量 ``<var>``，使用这个语法::

  -D<namespace>_<var>=<value>

例如，要在 ``my_sample`` 应用的构建系统中将 CMake 变量 ``FOO``
设置为值 ``BAR``，运行以下命令：

.. tabs::

   .. group-tab:: ``west build``

      .. code-block:: shell

         west build --sysbuild ... -- -Dmy_sample_FOO=BAR

   .. group-tab:: ``cmake``

      .. code-block:: shell

         cmake -Dmy_sample_FOO=BAR ...

.. _sysbuild_kconfig_namespacing:

Kconfig 命名空间
===================

要将 sysbuild Kconfig 选项 ``<var>`` 设置为值 ``<value>``，使用这个语法::

  -DSB_CONFIG_<var>=<value>

在上面的示例中，``SB_CONFIG`` 是 sysbuild Kconfig 选项的命名空间前缀。

要改为设置 Zephyr 应用的 Kconfig 选项，使用这个语法::

  -D<namespace>_CONFIG_<var>=<value>

在上面的示例中，``<namespace>`` 是上面 :ref:`sysbuild_cmake_namespace` 中
讨论的应用名称。

例如，要在 ``my_sample`` 应用的构建系统中将 Kconfig 选项 ``FOO``
设置为值 ``BAR``，运行以下命令：

.. tabs::

   .. group-tab:: ``west build``

      .. code-block:: shell

         west build --sysbuild ... -- -Dmy_sample_CONFIG_FOO=BAR

   .. group-tab:: ``cmake``

      .. code-block:: shell

        cmake -Dmy_sample_CONFIG_FOO=BAR ...

.. tip::
   当不用 ``<namespace>`` 时，Kconfig 设置传递给主 Zephyr 应用 ``my_sample``。

   这意味着传递 ``-DCONFIG_<var>=<value>`` 和
   ``-Dmy_sample_CONFIG_<var>=<value>`` 是等价的。

   这允许你在 CMake 时用相同语法设置 Kconfig 值，
   用或不用 sysbuild 构建相同应用。
   例如，以下命令将以相同方式工作：

   .. code-block:: shell

      west build -b <board> my_sample -- -DCONFIG_FOO=BAR

   .. code-block:: shell

      west build -b <board> --sysbuild my_sample -- -DCONFIG_FOO=BAR

用 ``west flash`` 烧录 sysbuild
**************************************

你可以用 :ref:`west flash <west-flashing>` 烧录用 sysbuild 构建的应用。

在由多个镜像组成的构建上调用 ``west flash`` 时，每个镜像按顺序烧录。
``--runner jlink`` 等额外参数传递给每次调用。

更多细节见 :ref:`west-multi-domain-flashing`。

用 ``west debug`` 调试 sysbuild
***************************************

你可以用 ``west debug`` 调试主应用，无论你是否使用 sysbuild。
只需遵循现有的 :ref:`west debug <west-debugging>` 指南来调试主示例。

要调试不同的域（Zephyr 应用），如 ``mcuboot``，使用
``--domain`` 参数，如下::

  west debug --domain mcuboot

更多细节见 :ref:`west-multi-domain-debugging`。

用 MCUboot 构建示例
******************************

Sysbuild 原生支持 MCUboot。

要用 MCUboot 构建 ``hello_world`` 这样的示例，
启用 MCUboot 并按如下方式构建和烧录示例：

.. tabs::

   .. group-tab:: ``west build``

      .. zephyr-app-commands::
         :tool: west
         :zephyr-app: samples/hello_world
         :board: reel_board
         :goals: build
         :west-args: --sysbuild
         :gen-args: -DSB_CONFIG_BOOTLOADER_MCUBOOT=y
         :compact:

   .. group-tab:: ``cmake``

      .. zephyr-app-commands::
         :tool: cmake
         :app: share/sysbuild
         :board: reel_board
         :goals: build
         :gen-args: -DAPP_DIR=samples/hello_world -DSB_CONFIG_BOOTLOADER_MCUBOOT=y
         :compact:

这为 ``reel_board`` 构建 ``hello_world`` 和 ``mcuboot``，
然后将 ``mcuboot`` 和 ``hello_world`` 应用镜像都烧录到开发板。

关于 Zephyr 使用 MCUboot 的更详细信息可以在 MCUboot 网站上的
`MCUboot with Zephyr`_ 文档页找到。

.. note::

   已弃用的 MCUBoot Kconfig 选项 ``CONFIG_ZEPHYR_TRY_MASS_ERASE``
   烧录时将执行整片擦除。如果此选项启用，那么只烧录 MCUBoot，
   例如使用 ``west flash --domain mcuboot``，可能擦除整个 flash，
   包括主应用镜像。

Sysbuild Kconfig 文件
*********************

你可以用配置文件为单个应用设置 sysbuild 的 Kconfig 选项。
默认情况下，sysbuild 在应用顶层目录中查找名为 ``sysbuild.conf`` 的配置文件。

在下面的示例中，有一个 :file:`sysbuild.conf` 文件，
只要使用 sysbuild 就启用用 MCUboot 构建和烧录：

.. code-block:: none

   <home>/application
   ├── CMakeLists.txt
   ├── prj.conf
   └── sysbuild.conf


.. code-block:: cfg

   SB_CONFIG_BOOTLOADER_MCUBOOT=y

你可以用 ``-DSB_CONF_FILE=<sysbuild-conf-file>`` CMake 构建设置
设置要使用的配置文件。

例如，你可以创建 ``sysbuild-mcuboot.conf``，
然后在用 sysbuild 构建时指定此文件，如下：

.. tabs::

   .. group-tab:: ``west build``

      .. zephyr-app-commands::
         :tool: west
         :zephyr-app: samples/hello_world
         :board: reel_board
         :goals: build
         :west-args: --sysbuild
         :gen-args: -DSB_CONF_FILE=sysbuild-mcuboot.conf
         :compact:

   .. group-tab:: ``cmake``

      .. zephyr-app-commands::
         :tool: cmake
         :app: share/sysbuild
         :board: reel_board
         :goals: build
         :gen-args: -DAPP_DIR=samples/hello_world -DSB_CONF_FILE=sysbuild-mcuboot.conf
         :compact:

Sysbuild 目标
****************

Sysbuild 为每个镜像（包括 sysbuild 本身）创建以下模式的构建目标：

 * menuconfig
 * hardenconfig
 * guiconfig

对于主应用（与不使用 sysbuild 时相同），这些可以正常运行而无任何前缀。
对于其他镜像（包括 sysbuild），这些用镜像名称和下划线作前缀运行，
例如 ``sysbuild_`` 或 ``mcuboot_``，使用 ninja 或 make -
关于如何运行 sysbuild 中没有映射构建目标的镜像构建目标的细节，
见 :ref:`sysbuild_dedicated_image_build_targets` 部分。

.. _sysbuild_dedicated_image_build_targets:

专用镜像构建目标
*****************************

并非所有镜像构建目标在使用 sysbuild 时都被赋予等价的前缀构建目标，
例如 ``ram_report``、``rom_report``、``footprint``、``puncover`` 和
``pahole`` 等构建目标未被公开。
当使用 :ref:`Trusted Firmware <tfm_build_system>` 时，
``tfm_`` 和 ``bl2_`` 前缀的构建目标也未被公开，
例如 ``tfm_rom_report`` 和 ``bl2_ram_report``。
要运行这些构建目标，可以将镜像的构建目录连同要执行的构建目标名称
一起提供给 west/ninja/make，它将运行。

.. tabs::

   .. group-tab:: ``west``

      假设项目已使用 ``west`` 配置和构建，使用启用 mcuboot 的 sysbuild
      在默认 ``build`` 文件夹位置，``mcuboot`` 的 ``rom_report`` 构建目标
      可以用以下命令运行：

      .. code-block:: shell

         west build -d build/mcuboot -t rom_report

      对于使用 TF-M 目标的 TF-M 项目，应用构建目录像这样使用：

      .. code-block:: shell

         west build -d build/<app_name> -t tfm_rom_report

   .. group-tab:: ``ninja``

      假设项目已使用 ``cmake`` 配置并用 ``ninja`` 构建，
      使用启用 mcuboot 的 sysbuild，``mcuboot`` 的 ``rom_report`` 构建目标
      可以用以下命令运行：

      .. code-block:: shell

         ninja -C mcuboot rom_report

      对于使用 TF-M 目标的 TF-M 项目，应用构建目录像这样使用：

      .. code-block:: shell

         ninja -C <app_name> -t tfm_rom_report

   .. group-tab:: ``make``

      假设项目已使用 ``cmake`` 配置并用 ``make`` 构建，
      使用启用 mcuboot 的 sysbuild，``mcuboot`` 的 ``rom_report`` 构建目标
      可以用以下命令运行：

      .. code-block:: shell

         make -C mcuboot rom_report

      对于使用 TF-M 目标的 TF-M 项目，应用构建目录像这样使用：

      .. code-block:: shell

         make -C <app_name> -t tfm_rom_report

.. _sysbuild_zephyr_application:

向 sysbuild 添加 Zephyr 应用
**************************************

你可以用 :cmake:command:`ExternalZephyrProject_Add` 函数将 Zephyr 应用
添加为 sysbuild 域。从你的应用 :file:`sysbuild.cmake` 文件调用这个 CMake 函数，
或从你知道将作为 sysbuild CMake 调用一部分运行的任何其他 CMake 文件调用。

变体镜像也可以用 :cmake:command:`ExternalZephyrVariantProject_Add` 函数添加，
这将复制 sysbuild 项目中已有的镜像，并允许配置上的细微差异。
这个功能的一个示例用例是更改镜像的选定 flash 节点，
但让其余配置与基础镜像相同。
当使用这时，sysbuild 本身和镜像都不会为其创建额外的 Kconfig 目标，
如 menuconfig、guiconfig、hardenconfig 或 traceconfig，
因为基础镜像可用于查看/调整这些。

针对相同开发板
========================

要将 ``my_sample`` 作为另一个 sysbuild 域包含，针对与主镜像相同的开发板，
使用这个示例：

.. code-block:: cmake

   ExternalZephyrProject_Add(
     APPLICATION my_sample
     SOURCE_DIR <path-to>/my_sample
   )

这可能有用，例如如果你的开发板要求你构建和烧录 SoC 特定的引导加载器
连同你的主应用。

针对不同开发板
=========================

在 sysbuild 和 Zephyr CMake 构建系统中，开发板可以指：

* 具有单核 SoC 的物理开发板。
* 具有多核 SoC 的物理开发板上的特定核心，如 :zephyr:board:`nrf5340dk`。
* 具有多个 SoC 的物理开发板上的特定 SoC，
  如 :ref:`nrf9160dk_nrf9160` 和 :ref:`nrf9160dk_nrf52840`。

如果你的主应用，例如，为 ``mps2/an521/cpu0`` 构建，
而你的辅助应用必须针对 ``mps2/an521/cpu1`` 开发板目标，
添加一个结构如下的 CMake 函数调用：

.. code-block:: cmake

   ExternalZephyrProject_Add(
     APPLICATION my_sample
     SOURCE_DIR <path-to>/my_sample
     BOARD mps2/an521/cpu1
   )

这可能有用，例如如果你的主应用需要另一个辅助 Zephyr 应用
与之一起构建和烧录，但辅助应用在你的 SoC 的另一个核心上运行。

用 Kconfig 条件性地针对
=====================================

你可以用 Kconfig 控制是否将额外应用包含为 sysbuild 域。

如果额外应用镜像专属于开发板或应用，你可以创建两个额外文件：
:file:`sysbuild.cmake` 和 :file:`Kconfig.sysbuild`。

对于应用，这看起来像这样：

.. code-block:: none

   <home>/application
   ├── CMakeLists.txt
   ├── prj.conf
   ├── Kconfig.sysbuild
   └── sysbuild.cmake

在上面的示例中，:file:`sysbuild.cmake` 的结构如下：

.. code-block:: cmake

   if(SB_CONFIG_SECOND_SAMPLE)
     ExternalZephyrProject_Add(
       APPLICATION second_sample
       SOURCE_DIR <path-to>/second_sample
     )
   endif()

:file:`Kconfig.sysbuild` 的结构如下：

.. code-block:: kconfig

   source "sysbuild/Kconfig"

   config SECOND_SAMPLE
           bool "Second sample"
           default y

这默认包含 ``second_sample``，同时仍允许你用 Kconfig 选项
``SECOND_SAMPLE`` 禁用它。

关于设置 sysbuild Kconfig 选项的更多信息，见 :ref:`sysbuild_kconfig_namespacing`。

构建而不烧录
=========================

你可以像这样将 ``my_sample`` 标记为仅构建应用：

.. code-block:: cmake

   ExternalZephyrProject_Add(
     APPLICATION my_sample
     SOURCE_DIR <path-to>/my_sample
     BUILD_ONLY TRUE
   )

结果是，``my_sample`` 将作为 sysbuild 构建调用的一部分构建，
但它将从 ``west flash`` 使用的默认镜像序列中排除。
相反，你可以将此域的输出用于其他目的 - 例如，
为 DFU 生成次要镜像，或合并多个镜像。

你还可以用 CMake 中的另一个布尔常量替换 ``TRUE``，
如 Kconfig 选项，这将使 ``my_sample`` 条件性地仅构建。

.. note::

   标记为仅构建的应用仍可以手动烧录，使用 ``west flash --domain my_sample``。
   因此，``BUILD_ONLY`` 选项只控制 ``west flash`` 的默认行为。

.. _sysbuild_application_configuration:

Zephyr 应用配置
================

当向 sysbuild 添加 Zephyr 应用，如 MCUboot，那么将使用
应用（MCUboot）本身的配置文件。

当将多个应用集成在一起时，通常需要对额外镜像的配置进行调整。

Sysbuild 给用户创建 Kconfig 片段或设备树覆盖的能力，
它们将与应用的默认配置一起使用。
Sysbuild 还允许用户更改 :ref:`application-configuration-directory`
以给用户对镜像配置的完全控制。

Zephyr 应用 Kconfig 片段和设备树覆盖
--------------------------------------------------

在主应用的文件夹中，在 sysbuild 文件夹下创建 Kconfig 片段或设备树覆盖，
其中文件名是 :file:`<image>.conf` 或 :file:`<image>.overlay`，
例如如果你的主应用包含 ``my_sample``，那么创建 :file:`sysbuild/my_sample.conf`
文件或设备树覆盖 :file:`sysbuild/my_sample.overlay`。

Kconfig 片段可以像：

.. code-block:: cfg

   # sysbuild/my_sample.conf
   CONFIG_FOO=n

Zephyr 应用配置目录
--------------------------------------------------

在主应用的文件夹中，在 :file:`sysbuild/<image>/` 下创建新文件夹。
然后该文件夹将在构建 ``<image>`` 时用作 ``APPLICATION_CONFIG_DIR``。
作为示例，如果你的主应用包含 ``my_sample``，那么创建
:file:`sysbuild/my_sample/` 文件夹并将任何配置文件放在那里，
像通常做的那样：

.. code-block:: none

   <home>/application
   ├── CMakeLists.txt
   ├── prj.conf
   └── sysbuild
       └── my_sample
           ├── prj.conf
           ├── app.overlay
           └── boards
               ├── <board_A>.conf
               ├── <board_A>.overlay
               ├── <board_B>.conf
               └── <board_B>.overlay

:file:`sysbuild/my_sample/` 文件夹下的所有配置文件现在将在
``my_sample`` 包含在构建中时使用，而 ``my_sample`` 的默认配置文件
将被忽略。

这给你在将这些与 ``application`` 集成时如何配置镜像的完全控制。

.. _sysbuild_file_suffixes:

Sysbuild 文件后缀支持
----------------------------

通过 :makevar:`FILE_SUFFIX` 的文件后缀支持在 sysbuild 中受支持
（关于此功能在应用中的细节见 :ref:`application-file-suffixes`）。
对于 sysbuild，全局提供的选项将传递到所有镜像。
此外，如果文件存在，镜像配置文件将应用并使用此值（而非构建类型）。

给定示例项目：

.. code-block:: none

   <home>/application
   ├── CMakeLists.txt
   ├── prj.conf
   ├── sysbuild.conf
   ├── sysbuild_test_key.conf
   └── sysbuild
       ├── mcuboot.conf
       ├── mcuboot_max_log.conf
       └── my_sample.conf

* 如果 ``FILE_SUFFIX`` 未定义且 ``mcuboot`` 和 ``my_sample`` 镜像都包含，
  ``mcuboot`` 将使用 ``mcuboot.conf`` Kconfig 片段文件，
  ``my_sample`` 将使用 ``my_sample.conf`` Kconfig 片段文件。
  Sysbuild 本身将使用 ``sysbuild.conf`` Kconfig 片段文件。

* 如果 ``FILE_SUFFIX`` 设置为 ``max_log`` 且 ``mcuboot`` 和 ``my_sample``
  镜像都包含，``mcuboot`` 将使用 ``mcuboot_max_log.conf`` Kconfig 片段文件，
  ``my_sample`` 将使用 ``my_sample.conf`` Kconfig 片段文件
  （因为它将回退到无后缀的文件）。
  Sysbuild 本身将使用 ``sysbuild.conf`` Kconfig 片段文件
  （因为它将回退到无后缀的文件）。

* 如果 ``FILE_SUFFIX`` 设置为 ``test_key`` 且 ``mcuboot`` 和 ``my_sample``
  镜像都包含，``mcuboot`` 将使用 ``mcuboot.conf`` Kconfig 片段文件，
  ``my_sample`` 将使用 ``my_sample.conf`` Kconfig 片段文件
  （因为它将回退到无后缀的文件）。
  Sysbuild 本身将使用 ``sysbuild_test_key.conf`` Kconfig 片段文件。
  这可以用于应用不同的 sysbuild 配置，
  例如在 MCUboot 和签名主应用时使用不同的签名密钥。

``FILE_SUFFIX`` 也可以用镜像名称作前缀仅应用到单个镜像：

.. tabs::

   .. group-tab:: ``west build``

      .. zephyr-app-commands::
         :tool: west
         :app: file_suffix_example
         :board: reel_board
         :goals: build
         :west-args: --sysbuild
         :gen-args: -DSB_CONFIG_BOOTLOADER_MCUBOOT=y -Dmcuboot_FILE_SUFFIX="max_log"
         :compact:

   .. group-tab:: ``cmake``

      .. zephyr-app-commands::
         :tool: cmake
         :app: share/sysbuild
         :board: reel_board
         :goals: build
         :gen-args: -DAPP_DIR=<app_dir> -DSB_CONFIG_BOOTLOADER_MCUBOOT=y -Dmcuboot_FILE_SUFFIX="max_log"
         :compact:

.. _sysbuild_zephyr_application_dependencies:

在 Zephyr 应用之间添加依赖
=============================================

有时，在多镜像构建中，你可能希望某些 Zephyr 应用按特定顺序
配置或烧录。例如，如果你需要从一个应用的构建系统获取的信息
可用于另一个应用，那么首先要做的是在它们之间添加配置依赖。
单独地，你还可以添加烧录依赖来控制 ``west flash`` 使用的镜像序列；
如果 SoC、_runner_ 或其他东西要求特定烧录顺序，就可以使用这。

默认情况下，sysbuild 按添加顺序配置和烧录应用，
因为 :cmake:command:`ExternalZephyrProject_Add` 调用由 CMake 处理。
你可以用 :cmake:command:`sysbuild_add_dependencies` 函数
根据你的需求调整这个顺序。其用法类似于 CMake 中标准的
:cmake:command:`add_dependencies() <command:add_dependencies>` 函数。

这里是 ``my_sample`` 添加配置依赖的示例：

.. code-block:: cmake

   sysbuild_add_dependencies(IMAGE CONFIGURE my_sample sample_a sample_b)

这将确保 sysbuild 在为 ``my_sample`` 做同样事情之前
先为 ``sample_a`` 和 ``sample_b`` 运行 CMake（以某种顺序），
在单次调用中构建这些域时。

如果你想改为添加烧录依赖，那么像这样做：

.. code-block:: cmake

   sysbuild_add_dependencies(IMAGE FLASH my_sample sample_a sample_b)

结果是，``my_sample`` 将在 ``sample_a`` 和 ``sample_b`` 之后烧录
（以某种顺序），在单次调用中烧录这些域时。

.. note::

   不允许为仅构建应用添加烧录依赖。
   如果 ``my_sample`` 是用 ``BUILD_ONLY TRUE`` 创建的，
   那么上面对 ``sysbuild_add_dependencies()`` 的调用将产生错误。

.. _sysbuild_merged_hex_files:

合并的 hex 文件
****************

Sysbuild 支持创建合并的 hex 文件，它们将为 sysbuild 项目中
每个唯一开发板目标创建一个，可以用 :kconfig:option:`SB_CONFIG_MERGED_HEX_FILES` 启用。
输出文件名格式为 :file:`merged_<NORMALIZED_BOARD_TARGET>.hex`。
这非常适合创建用于部署的生产镜像，它要求所有镜像输出 hex 文件。
如果 sysbuild 项目为同一开发板目标构建多个镜像
但为**不同**设备（例如作为测试的一部分为 3 个不同开发板构建 3 个镜像），
那么此选项应保持禁用。
hex 文件将按照配置的烧录顺序合并，
之前地址中任何与后面合并的 hex 文件冲突的重叠数据
将被后面 hex 文件的数据覆盖 -
关于如何配置 sysbuild 镜像的烧录顺序见
:ref:`sysbuild_zephyr_application_dependencies`。

向 sysbuild 添加非 Zephyr 应用
******************************************

你可以用标准 CMake 模块 :cmake:module:`ExternalProject <module:ExternalProject>`
在多镜像构建中包含非 Zephyr 应用。
用法细节请参阅 CMake 文档。

当使用 :cmake:module:`ExternalProject <module:ExternalProject>` 时，
非 Zephyr 应用将作为 sysbuild 构建调用的一部分构建，
但 ``west flash`` 或 ``west debug`` 将不知道该应用。
相反，你必须手动烧录和调试该应用。

.. _MCUboot with Zephyr: https://docs.mcuboot.com/readme-zephyr

.. _sysbuild_var_override:

配置 sysbuild 内部状态
***********************************

由于 sysbuild 本身是一个 CMake 项目，它像 Zephyr 应用一样运行和设置自己，
但使用它自己的 CMake 代码。这意味着某些功能，
例如在应用 ``CMakeLists.txt`` 中指定变量（如 ``BOARD_ROOT``）将不起作用，
相反这些必须通过使用 :ref:`一个模块 <modules_build_settings>`
或通过使用自定义 sysbuild 项目文件作为 ``<application>/sysbuild/CMakeLists.txt`` 设置，
例如：

.. code-block:: cmake

   # 在这里放置 sysbuild 前的配置项

   # 为更改 sysbuild 本身使用的配置：
   # set(<var> <value>)
   # list(APPEND <list> <value>)

   # 为更改其他镜像的配置：
   # set(<image>_<var> <value> CACHE INTERNAL "<description>")

   # 查找 sysbuild 项目并用新配置包含它
   find_package(Sysbuild REQUIRED HINTS $ENV{ZEPHYR_BASE})

   project(sysbuild LANGUAGES)

添加 ``BOARD_ROOT`` 的示例：

.. code-block:: cmake

   list(APPEND BOARD_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/../<extra-board-root>)

   find_package(Sysbuild REQUIRED HINTS $ENV{ZEPHYR_BASE})

   project(sysbuild LANGUAGES)

这将把开发板根作为项目的一部分传递到所有镜像，
不需要在每个镜像的 ``CMakeLists.txt`` 文件中重复。

扩展 sysbuild
******************

sysbuild 可以被其他模块扩展以给它额外功能
或包含其他配置或镜像，一个示例可以是添加对
另一个引导加载器或外部签名方法的支持。

模块可以通过像普通 :ref:`模块 <module-yml>` 一样添加自定义
CMake 或 Kconfig 文件来扩展，这将导致这些文件被包含在
作为项目一部分的每个镜像中。
或者，有 :ref:`sysbuild 特定的模块扩展 <sysbuild_module_integration>` 文件，
它们可以用于包含整体 sysbuild 镜像本身的 CMake 和 Kconfig 文件，
这就是例如可以为特定开发板或 SoC 添加自定义镜像的地方。


.. toctree::
   :maxdepth: 1

   images.rst

Sysbuild 和 CMake 预设
**************************

:cmake:manual:`CMake 预设 <manual:cmake-presets(7)>` 可以与 Sysbuild 一起使用，
但并非所有预设宏都会按预期工作。

.. note::

   在 sysbuild 中使用 CMake 预设需要 CMake 版本 3.27 或更高。

如 :ref:`sysbuild` 中所述，sysbuild 是一个更高层的构建系统，
这意味着当 CMake 预设与 sysbuild 一起使用时，预设由 sysbuild 本身
消费和处理，结果传递给应用。

用预设运行 sysbuild。

.. tabs::

   .. group-tab:: ``west build``

      这里是一个应该使用预设 ``release`` 的示例。
      细节见 ``west build 文档`` 中的 :ref:`west-multi-domain-builds`。

      .. zephyr-app-commands::
         :tool: west
         :zephyr-app: samples/hello_world
         :board: reel_board
         :goals: build
         :west-args: --sysbuild -- --preset=release
         :compact:

   .. group-tab:: ``cmake``

      这里是一个使用 CMake 和 Ninja 的示例。

      .. code-block:: shell

         APP_DIR=samples/hello_world cmake -Bbuild -GNinja -DBOARD=reel_board --preset=release share/sysbuild
         ninja -Cbuild

      当用 sysbuild 使用 CMake 预设时，``APP_DIR`` 必须在环境中设置，
      以便 Sysbuild CMake 能够从主 Zephyr 应用的源目录包含 ``CMakePresets.json``。

.. note::

   由于 sysbuild 将顶层 cmake 项目更改为其自己的目录，
   cmake 预设从那里解析，应用的预设从该文件原样包含。
   因此相对路径和解析为相对于源目录的宏将不按预期工作，
   而是相对于 share/sysbuild，例如 ``${sourceDir}``。

   ``${fileDir}`` 宏可以用来创建相对于应用目录的可移植路径。
