.. _application:

应用开发
#######################

.. note::

   在本文档中，我们假设你的 **应用目录** :file:`<app>` 类似于 :file:`<home>/zephyrproject/app`，其 **构建目录** 为 :file:`<app>/build`。

   这些术语将在下文定义。在 Linux/macOS 上，<home> 等价于 ``~``；在 Windows 上，它等价于 ``%userprofile%``。

   将应用保留在工作区（:file:`<home>/zephyrproject`）内，可以更方便地使用 ``west build`` 等命令。（当然，只要 :ref:`ZEPHYR_BASE <important-build-vars>` 设置正确，你也可以将应用放在任何位置。）

概览
********

Zephyr 的构建系统基于 `CMake`_。

构建系统以应用为中心，要求基于 Zephyr 的应用发起对 Zephyr 源代码的构建。应用构建控制应用和 Zephyr 本身的配置与构建过程，将它们编译为单个二进制文件。

主 zephyr 仓库包含 Zephyr 的源代码、配置文件和构建系统。你很可能还安装了各种 :ref:`模块`，它们提供第三方源代码集成。

**应用目录** 中的文件将 Zephyr 和任何模块与应用关联起来。该目录包含所有应用特定的文件，例如应用特定的配置文件和源代码。

以下是一个简单 Zephyr 应用中的文件：

.. code-block:: none

   <app>
   ├── CMakeLists.txt
   ├── app.overlay
   ├── prj.conf
   ├── VERSION
   └── src
       └── main.c

这些文件的内容如下：

* **CMakeLists.txt**：该文件告知构建系统在哪里找到其他应用文件，并将应用目录与 Zephyr 的 CMake 构建系统关联起来。这种关联提供了 Zephyr 构建系统支持的功能，例如开发板特定的配置文件、在真实或仿真硬件上运行和调试编译后二进制文件的能力等。

* **app.overlay**：这是一个设备树覆盖文件，指定应应用于你所构建的任何开发板基础设备树的应用特定更改。设备树覆盖的用途通常是配置应用所使用的硬件的某些方面。

  构建系统默认查找 :file:`app.overlay`，但你还可以添加更多设备树覆盖文件，其他默认文件也会被搜索。

  有关设备树的更多信息，请参阅 :ref:`devicetree`。

* **prj.conf**：这是一个 Kconfig 片段，指定一个或多个 Kconfig 选项的应用特定值。这些应用设置与其他设置合并以生成最终配置。Kconfig 片段的用途通常是配置应用所使用的软件功能。

  构建系统默认查找 :file:`prj.conf`，但你还可以添加更多 Kconfig 片段文件，其他默认文件也会被搜索。

  有关更多信息，请参阅下文 :ref:`application-kconfig` 部分。

* **VERSION**：一个包含若干版本信息字段的文本文件。这些字段让你能够管理应用的生命周期，并在签名应用镜像时自动提供应用版本。

  有关该文件及其用法的更多信息，请参阅 :ref:`app-version-details`。

* **main.c**：一个源代码文件。应用通常包含用 C、C++ 或汇编语言编写的源文件。Zephyr 的惯例是将它们放在 :file:`<app>` 下名为 :file:`src` 的子目录中。

一旦应用被定义，你将使用 CMake 生成一个 **构建目录**，其中包含构建应用和 Zephyr 所需的文件，然后将它们链接为最终的二进制文件，以便在你的开发板上运行。最简单的方式是使用 :ref:`west build <west-building>`，但你也可以直接使用 CMake。应用构建产物始终生成在单独的构建目录中：Zephyr 不支持"树内"构建。

以下章节介绍如何创建、构建和运行 Zephyr 应用，之后提供更详细的参考资料。

.. _zephyr-app-types:

应用类型
*****************

我们根据 :file:`<app>` 的位置，将 Zephyr 应用区分为三种基本类型：

.. table::

   +------------------------------+--------------------------------+
   | 应用类型                     | :file:`<app>` 位置             |
   +------------------------------+--------------------------------+
   | :ref:`仓库内应用             | zephyr 仓库内                  |
   | <zephyr-repo-app>`           |                                |
   +------------------------------+--------------------------------+
   | :ref:`工作区应用              | Zephyr 所在的 west 工作区内    |
   | <zephyr-workspace-app>`      |                                |
   +------------------------------+--------------------------------+
   | :ref:`独立应用               | 其他位置                       |
   | <zephyr-freestanding-app>`   |                                |
   +------------------------------+--------------------------------+

我们将在下文详细讨论这些类型。要了解构建系统如何支持每种类型，请参阅 :ref:`cmake_pkg`。

.. _zephyr-repo-app:

Zephyr 仓库内应用
=============================

位于 Zephyr :ref:`west 工作区 <west-workspaces>` 中 ``zephyr`` 源代码仓库内的应用称为 Zephyr 仓库内应用。在以下示例中，:zephyr:code-sample:`hello_world 示例 <hello_world>` 就是一个 Zephyr 仓库内应用：

.. code-block:: none

   zephyrproject/
   ├─── .west/
   │    └─── config
   └─── zephyr/
        ├── arch/
        ├── boards/
        ├── cmake/
        ├── samples/
        │    ├── hello_world/
        │    └── ...
        ├── tests/
        └── ...

.. _zephyr-workspace-app:

Zephyr 工作区应用
============================

位于 :ref:`工作区 <west-workspaces>` 内但不在 zephyr 仓库本身内的应用称为 Zephyr 工作区应用。在以下示例中，``app`` 就是一个 Zephyr 工作区应用：

.. code-block:: none

   zephyrproject/
   ├─── .west/
   │    └─── config
   ├─── zephyr/
   ├─── bootloader/
   ├─── modules/
   ├─── tools/
   ├─── <vendor/private-repositories>/
   └─── applications/
        └── app/

.. _zephyr-freestanding-app:

Zephyr 独立应用
==============================

位于 Zephyr :ref:`工作区 <west-workspaces>` 之外的 Zephyr 应用称为 Zephyr 独立应用。在以下示例中，``app`` 就是一个 Zephyr 独立应用：

.. code-block:: none

   <home>/
   ├─── zephyrproject/
   │     ├─── .west/
   │     │    └─── config
   │     ├── zephyr/
   │     ├── bootloader/
   │     ├── modules/
   │     └── ...
   │
   └─── app/
        ├── CMakeLists.txt
        ├── prj.conf
        └── src/
            └── main.c

.. _zephyr-creating-app:

创建应用
***********************

在 Zephyr 中，你可以使用参考工作区应用，也可以手动创建你的应用。

.. _zephyr-creating-app-from-example:

使用参考工作区应用
=======================================

`example-application`_ Git 仓库包含一个参考 :ref:`工作区应用 <zephyr-workspace-app>`。建议在下文所述的创建自己应用的过程中将其作为参考。

example-application 仓库演示了如何使用若干常用功能，例如：

- 自定义 :ref:`开发板移植 <board_porting_guide>`
- 自定义 :ref:`设备树绑定 <dt-bindings>`
- 自定义 :ref:`设备驱动 <device_model_api>`
- 持续集成（CI）设置，包括使用 :ref:`twister <twister_script>`
- 自定义 west :ref:`扩展命令 <west-extensions>`

基本用法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在现有 Zephyr 工作区内开始使用 example-application 仓库最简单的方式是按以下步骤操作：

.. code-block:: console

   cd <home>/zephyrproject
   git clone https://github.com/zephyrproject-rtos/example-application my-app

上面的目录名 :file:`my-app` 是任意的：可按需更改。现在你可以进入该目录并根据需要调整其内容。由于你使用的是现有的 Zephyr 工作区，你可以使用 ``west build`` 或其他 west 命令来构建、烧录和调试。

高级用法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

你也可以将 example-application 仓库作为构建自定义 Zephyr 软件发行版的起点。这让你可以执行以下操作：

- 移除不需要的 Zephyr 模块
- 添加额外的自定义仓库
- 用你自己的版本覆盖 Zephyr 提供的仓库
- 与他人分享成果并进一步协作

example-application 仓库包含一个 :file:`west.yml` 文件，因此它本身也是一个 west :ref:`清单仓库 <west-workspace>`。按以下步骤操作，即可使用它创建一个全新的自定义工作区：

.. code-block:: console

   cd <home>
   mkdir my-workspace
   cd my-workspace
   git clone https://github.com/zephyrproject-rtos/example-application my-manifest-repo
   west init -l my-manifest-repo

这将创建一个采用 :ref:`T2 拓扑 <west-t2>` 的新工作区，其中 :file:`my-manifest-repo` 为清单仓库。:file:`my-workspace` 和 :file:`my-manifest-repo` 的名称是任意的：可按需更改。

接下来，自定义清单仓库。克隆时该仓库的初始内容将与 example-application 的内容一致。然后你可以按喜好编辑 :file:`my-manifest-repo/west.yml`，按需要更改其中的仓库集合。有关如何按需从工作区添加或移除不同仓库的示例，请参阅 :ref:`west-manifest-import`。对其他文件进行任何你需要的更改。

当你满意后，可以运行：

.. code-block::

   west update

你的工作区即可就绪。

如果你将生成的 :file:`my-manifest-repo` 仓库推送到其他地方，就可以与他人分享你的工作。例如，假设你将仓库推送到 ``https://git.example.com/my-manifest-repo``。其他人可以通过运行以下命令设置对应的工作区：

.. code-block::

   west init -m https://git.example.com/my-manifest-repo my-workspace
   cd my-workspace
   west update

从现在开始，你可以通过推送更改到你使用的仓库、按需更新 :file:`my-manifest-repo/west.yml` 来添加和移除仓库或更改其内容，从而协作开发共享软件。

.. _zephyr-creating-app-by-hand:

手动创建应用
===============================

你可以按以下步骤从零创建一个基本的应用目录。不过，使用 `example-application`_ 仓库或 Zephyr 的 :zephyr:code-sample-category:`示例` 作为起点可能更容易。

#. 创建应用目录。

   例如，在 Unix shell 或 Windows ``cmd.exe`` 提示符中：

   .. code-block:: console

      mkdir app

   .. warning::

      在路径的任何位置包含空格的目录中构建 Zephyr 或创建应用是不支持的。因此 Windows 路径 :file:`C:\\Users\\YourName\\app` 可以工作，但 :file:`C:\\Users\\Your Name\\app` 不行。

#. 创建源代码文件。

   建议将所有应用源代码放在名为 :file:`src` 的子目录中。这使得更容易区分项目文件和源代码。

   继续上一步的示例，输入：

   .. code-block:: console

      cd app
      mkdir src

#. 将应用源代码放入 :file:`src` 子目录中。在本例中，假设你创建了一个名为 :file:`src/main.c` 的文件。

#. 在 ``app`` 目录中创建一个名为 :file:`CMakeLists.txt` 的文件，内容如下：

   .. code-block:: cmake

      cmake_minimum_required(VERSION 3.28.0)

      find_package(Zephyr)
      project(my_zephyr_app)

      target_sources(app PRIVATE src/main.c)

   说明：

   - ``cmake_minimum_required()`` 调用是 CMake 所必需的。它还会被下一行的 Zephyr 包调用。如果 CMake 版本低于 :file:`CMakeLists.txt` 中的版本或 Zephyr 包中的版本号，CMake 将报错。

   - ``find_package(Zephyr)`` 引入 Zephyr 构建系统，后者创建一个名为 ``app`` 的 CMake 目标（参见 :ref:`cmake_pkg`）。向该目标添加源代码即是将它们包含到构建中。Zephyr 包将把 ``Zephyr-Kernel`` 定义为 CMake 项目，并启用对 ``C``、``CXX``、``ASM`` 语言的支持。

   - ``project(my_zephyr_app)`` 定义你的应用的 CMake 项目。这必须在 ``find_package(Zephyr)`` 之后调用，以避免与 Zephyr 的 ``project(Zephyr-Kernel)`` 产生干扰。

   - ``target_sources(app PRIVATE src/main.c)`` 用于将你的源文件添加到 ``app`` 目标。这必须在定义了该目标的 ``find_package(Zephyr)`` 之后调用。你可以用 ``target_sources()`` 添加任意数量的文件。

#. 为你的应用创建至少一个 Kconfig 片段（通常命名为 :file:`prj.conf`），并在其中设置你的应用所需的 Kconfig 选项值。参见 :ref:`application-kconfig`。如果不需要设置任何 Kconfig 选项，创建一个空文件即可。

#. 配置你的应用所需的任何设备树覆盖文件，通常放在名为 :file:`app.overlay` 的文件中。参见 :ref:`set-devicetree-overlays`。

#. 设置你可能需要的其他文件，例如 :ref:`twister <twister_script>` 配置文件、持续集成文件、文档等。

.. _important-build-vars:

重要的构建系统变量
********************************

你可以使用许多变量来控制 Zephyr 构建系统。本节介绍每个 Zephyr 开发者都应了解的最重要的变量。

.. note::

   变量 :makevar:`BOARD`、:makevar:`CONF_FILE` 和 :makevar:`DTC_OVERLAY_FILE` 可以通过 3 种方式（按优先级排序）提供给构建系统：

   * 通过 ``-D`` 命令行开关作为 ``west build`` 或 ``cmake`` 调用的参数。如果你有多个覆盖文件，应使用引号，例如 ``"file1.overlay;file2.overlay"``
   * 作为 :ref:`环境变量 <env_vars>`。
   * 作为 :file:`CMakeLists.txt` 中的 ``set(<VARIABLE> <VALUE>)`` 语句。

* :makevar:`ZEPHYR_BASE`：构建系统使用的 Zephyr 基础变量。``find_package(Zephyr)`` 会自动将其设置为缓存的 CMake 变量。但 ``ZEPHYR_BASE`` 也可以作为环境变量设置，以强制 CMake 使用特定的 Zephyr 安装。

* :makevar:`BOARD`：选择应用构建将用于默认配置的开发板。有关内置开发板，请参阅 :ref:`boards`；有关添加开发板支持的信息，请参阅 :ref:`board_porting_guide`。

* :makevar:`CONF_FILE`：指定一个或多个 Kconfig 配置片段文件的名称。多个文件名可以用空格或分号分隔。每个文件包含覆盖默认配置值的 Kconfig 配置值。

  有关更多信息，请参阅 :ref:`initial-conf`。

* :makevar:`EXTRA_CONF_FILE`：额外的 Kconfig 配置片段文件。多个文件名可以用空格或分号分隔。这在希望保持 :makevar:`CONF_FILE` 为默认值但"混合"一些额外配置选项时很有用。

* :makevar:`DTC_OVERLAY_FILE`：要使用的一个或多个设备树覆盖文件。多个文件可以用分号分隔。有关示例，请参阅 :ref:`set-devicetree-overlays`；有关设备树与 Zephyr 的信息，请参阅 :ref:`devicetree-intro`。

* :makevar:`EXTRA_DTC_OVERLAY_FILE`：要使用的额外设备树覆盖文件。多个文件可以用分号分隔。这在希望保持 :makevar:`DTC_OVERLAY_FILE` 为默认值但"混合"一些额外覆盖文件时很有用。

* :makevar:`SHIELD`：参见 :ref:`shields`

* :makevar:`ZEPHYR_MODULES`：包含额外目录的绝对路径的 `CMake 列表`_，这些目录包含应在使用应用构建中使用的源代码、Kconfig 等。有关详情，请参阅 :ref:`modules`。如果你设置了该变量，它必须是所有要使用的模块的完整列表，因为构建系统不会自动从 west 获取任何模块。

* :makevar:`EXTRA_ZEPHYR_MODULES`：与 :makevar:`ZEPHYR_MODULES` 类似，不同之处在于这些模块将被添加到通过 west 找到的模块列表中，而不是替换该列表。

* :makevar:`FILE_SUFFIX`：可选的文件名后缀，将添加到 Kconfig 片段和设备树覆盖文件（如果这些文件存在，否则将回退到不带前缀的名称）。有关详情，请参阅 :ref:`application-file-suffixes`。

* :makevar:`KCONFIG_WARNING_AS_ERROR`：将每个 Kconfig 警告视为错误，包括那些默认仅打印的警告。有关详情，请参阅 :ref:`kconfig_warning_as_error`。

.. note::

   你可以使用 :ref:`cmake_build_config_package` 来共享这些变量的通用设置。

.. _zephyr-app-cmakelists:

应用 CMakeLists.txt
**************************

每个应用必须有一个 :file:`CMakeLists.txt` 文件。该文件是构建系统的入口点或顶层。最终的 :file:`zephyr.elf` 镜像同时包含应用和内核库。

本节介绍你可以在 :file:`CMakeLists.txt` 中执行的一些操作。请确保按顺序执行以下步骤。

#. 如果你只想为一个开发板构建，在新的一行中添加你应用的开发板配置名称。例如：

   .. code-block:: cmake

      set(BOARD qemu_x86)

   有关可用开发板的更多信息，请参阅 :ref:`boards`。

   Zephyr 构建系统按以下顺序检查来确定 :makevar:`BOARD` 的值（当找到 BOARD 值时，CMake 停止继续向下查找）：

   - 由 CMake 缓存确定的任何先前使用的值具有最高优先级。这确保你不会尝试用与构建配置步骤中设置的 :makevar:`BOARD` 值不同的值来运行构建。

   - 在 CMake 命令行上（直接或通过 ``west build`` 间接）使用 ``-DBOARD=YOUR_BOARD`` 给出的任何值接下来会被检查并使用。

   - 如果设置了 :ref:`环境变量 <env_vars>` ``BOARD``，其值将被使用。

   - 最后，如果你按本步骤所述在应用 :file:`CMakeLists.txt` 中设置了 ``BOARD``，该值将被使用。

#. 如果你的应用使用了除常规 :file:`prj.conf` 之外的配置文件，添加适当的行来设置 :makevar:`CONF_FILE` 变量指向这些文件。如果给出多个文件名，用单个空格或分号分隔。当希望避免在单一位置设置 :makevar:`CONF_FILE` 时，可以使用 CMake 列表以模块化方式构建配置片段文件。例如：

   .. code-block:: cmake

     set(CONF_FILE "fragment_file1.conf")
     list(APPEND CONF_FILE "fragment_file2.conf")

   有关更多信息，请参阅 :ref:`initial-conf`。

#. 如果你的应用使用了设备树覆盖文件，你可能需要设置 :ref:`DTC_OVERLAY_FILE <important-build-vars>`。参见 :ref:`set-devicetree-overlays`。

#. 如果你的应用有自己的内核配置选项，在与应用 :file:`CMakeLists.txt` 相同的目录中创建一个 :file:`Kconfig` 文件。

   有关详细的 Kconfig 文档，请参阅 :ref:`手册中的 Kconfig 部分 <kconfig>`。

   一个（不太可能的）高级使用场景是你的应用有自己的独特配置 **选项**，这些选项根据构建配置不同而设置不同。

   如果你只是想为现有 Zephyr 配置选项设置应用特定的 **值**，请参阅上文 :makevar:`CONF_FILE` 的说明。

   按以下结构组织你的 :file:`Kconfig` 文件：

   .. literalinclude:: application-kconfig.include
      :language: kconfig

   .. note::

      ``source`` 语句中的环境变量会直接展开，因此你不需要定义 ``option env="ZEPHYR_BASE"`` Kconfig "中转"符号。如果你使用了这样的符号，它必须与环境变量同名。

      有关更多信息，请参阅 :ref:`kconfig_extensions`。

   当 :file:`Kconfig` 文件放在应用目录中时会被自动检测，但如果 CMake 变量 :makevar:`KCONFIG_ROOT` 以绝对路径设置，它也可以在别处被找到。

#. 在新的一行中指定应用需要 Zephyr，**在从上述步骤添加的任何行之后**：

   .. code-block:: cmake

      find_package(Zephyr)
      project(my_zephyr_app)

   .. note:: ``find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})`` 可以在需要支持通过显式设置 ``ZEPHYR_BASE`` 环境变量来强制使用特定 Zephyr 安装时使用。Zephyr 中的所有示例都支持 ``ZEPHYR_BASE`` 环境变量。

#. 现在将任何应用源文件添加到 'app' 目标库中，每个文件占一行，如下所示：

   .. code-block:: cmake

      target_sources(app PRIVATE src/main.c)

下面是一个简单的 :file:`CMakeList.txt` 示例：

.. code-block:: cmake

   set(BOARD qemu_x86)

   find_package(Zephyr)
   project(my_zephyr_app)

   target_sources(app PRIVATE src/main.c)

CMake 属性 ``HEX_FILES_TO_MERGE`` 利用 Kconfig 和 CMake 提供的应用配置，让你可以将外部构建的 hex 文件与构建 Zephyr 应用时生成的 hex 文件合并。例如：

.. code-block:: cmake

  set_property(GLOBAL APPEND PROPERTY HEX_FILES_TO_MERGE
      ${app_bootloader_hex}
      ${PROJECT_BINARY_DIR}/${KERNEL_HEX_NAME}
      ${app_provision_hex})

.. _zephyr-app-cmakecache:

CMakeCache.txt
**********************

CMake 使用 CMakeCache.txt 文件作为持久的键值字符串存储，用于在多次运行之间缓存值，包括编译和构建选项以及库依赖项的路径。该缓存文件在 CMake 在空构建文件夹中运行时创建。

有关 CMakeCache.txt 文件的更多详情，请参阅官方 `CMake 缓存`_ 文档。

.. _CMake Cache: https://cmake.org/cmake/help/book/mastering-cmake/chapter/CMake%20Cache.html


应用配置
*************************

.. _application-configuration-directory:

应用配置目录
===================================

Zephyr 将使用来自应用配置目录的配置文件，但由上文描述的参数（例如 ``CONF_FILE``、``EXTRA_CONF_FILE``、``DTC_OVERLAY_FILE`` 和 ``EXTRA_DTC_OVERLAY_FILE``）提供的绝对路径文件除外。

应用配置目录由 ``APPLICATION_CONFIG_DIR`` 变量定义。

``APPLICATION_CONFIG_DIR`` 将由以下来源之一设置，按优先级从高到低排列：

1. 如果用户通过 ``-DAPPLICATION_CONFIG_DIR=<path>`` 或在 ``find_package(Zephyr)`` 之前的 CMake 文件中指定了 ``APPLICATION_CONFIG_DIR``，则该文件夹被用作应用的配置目录。

2. 应用的源目录。

.. _application-kconfig:

Kconfig 配置
=====================

应用配置选项通常在应用目录中的 :file:`prj.conf` 中设置。例如，可以通过以下赋值启用 C++ 支持：

.. code-block:: cfg

   CONFIG_CPP=y

查看 :zephyr:code-sample-category:`现有示例 <samples>` 是一个很好的起步方式。

有关设置 Kconfig 配置值的详细文档，请参阅 :ref:`setting_configuration_values`。同一页面上的 :ref:`initial-conf` 部分解释了如何派生初始配置。有关配置选项的完整列表，请参阅 :ref:`kconfig-search`。有关与 Kconfig 选项相关的安全信息，请参阅 :ref:`hardening`。

:ref:`手册中的 Kconfig 部分 <kconfig>` 的其他页面也值得浏览，尤其是如果你计划添加新的配置选项。

实验性功能
~~~~~~~~~~~~~~~~~~~~~~~

Zephyr 是一个持续开发中的项目，因此有一些功能仍处于开发周期的早期阶段。此类功能将在其 Kconfig 标题中标记为 ``[EXPERIMENTAL]``。

:kconfig:option:`CONFIG_WARN_EXPERIMENTAL` 设置可用于在启用任何实验性功能时，在 CMake 配置阶段启用警告。

.. code-block:: cfg

   CONFIG_WARN_EXPERIMENTAL=y

例如，如果选项 ``CONFIG_FOO`` 是实验性的，那么启用它和 :kconfig:option:`CONFIG_WARN_EXPERIMENTAL` 将在你构建应用时在 CMake 配置阶段打印以下警告：

.. code-block:: none

   warning: Experimental symbol FOO is enabled.

设备树覆盖
===================

参见 :ref:`set-devicetree-overlays`。

.. _application-file-suffixes:

文件后缀
=============

Zephyr 应用可能希望拥有一个代码库，同时为不同的构建/产品变体提供多个配置，这需要不同的 Kconfig 选项和设备树配置。为了更好地配置这一点，Zephyr 在配置应用时提供了 :makevar:`FILE_SUFFIX` 选项，它可以自动附加到文件名。这应用于 Kconfig 片段和开发板覆盖文件，但带有回退机制：如果此类文件不存在，将使用不带这些后缀的文件。

给定以下示例项目布局：

.. code-block:: none

   <app>
   ├── CMakeLists.txt
   ├── prj.conf
   ├── prj_mouse.conf
   ├── boards
   │   ├── native_sim.overlay
   │   └── qemu_cortex_m3_mouse.overlay
   └── src
       └── main.c

* 如果正常构建且未为 ``native_sim`` 定义 ``FILE_SUFFIX``，则使用 ``prj.conf`` 和 ``boards/native_sim.overlay``。

* 如果正常构建且未为 ``qemu_cortex_m3`` 定义 ``FILE_SUFFIX``，则使用 ``prj.conf``，不使用任何应用设备树覆盖文件。

* 如果为 ``native_sim`` 将 ``FILE_SUFFIX`` 设置为 ``mouse`` 进行构建，则使用 ``prj_mouse.conf`` 和 ``boards/native_sim.overlay``（由于不存在 ``native_sim_mouse.overlay`` 文件，因此回退到 ``native_sim.overlay``）。

* 如果为 ``qemu_cortex_m3`` 将 ``FILE_SUFFIX`` 设置为 ``mouse`` 进行构建，则使用 ``prj_mouse.conf`` 和 ``boards/qemu_cortex_m3_mouse.overlay``。

应用特定代码
*************************

应用特定的源文件通常添加到应用的 :file:`src` 目录中。如果应用添加了大量文件，开发者可以将它们分组到 :file:`src` 下的子目录中，深度按需而定。

应用特定的源代码不应使用内核保留供自身使用的符号名前缀。有关更多信息，请参阅 `命名约定 <https://github.com/zephyrproject-rtos/zephyr/wiki/Naming-Conventions>`_。

第三方库代码
========================

可以在应用的 :file:`src` 目录之外构建库代码，但重要的是应用和库代码目标必须针对相同的二进制应用接口（ABI）。在大多数架构上，有控制目标 ABI 的编译器标志，因此库和应用必须共享某些编译器标志非常重要。粘合代码访问 Zephyr 内核头文件也可能很有用。

为了更容易集成第三方组件，Zephyr 构建系统定义了 CMake 函数，使应用构建脚本能够访问 zephyr 编译器选项。这些函数在 :zephyr_file:`cmake/modules/extensions.cmake` 中记录并定义，遵循命名约定 ``zephyr_get_<type>_<format>``。

以下变量通常需要导出到第三方构建系统。

* ``CMAKE_C_COMPILER``、``CMAKE_AR``。

* ``ARCH`` 和 ``BOARD``，连同标识 Zephyr 内核版本的若干变量。

:zephyr_file:`samples/application_development/external_lib` 是一个示例项目，演示了其中一些功能。


.. _build_an_application:

构建应用
***********************

Zephyr 构建系统将应用的所有组件编译并链接为单个应用镜像，可在仿真硬件或真实硬件上运行。

与任何其他基于 CMake 的系统一样，构建过程分 :ref:`两个阶段 <cmake-details>` 进行。首先，使用 ``cmake`` 命令行工具并指定生成器来生成构建文件（也称为构建系统）。该生成器决定构建系统在第二阶段将使用的原生构建工具。第二阶段运行原生构建工具来实际构建源文件并生成镜像。要了解这些概念的更多信息，请参阅官方 CMake 文档中的 `CMake 介绍`_。

虽然 Zephyr 的默认构建工具是 :std:ref:`west <west>`（Zephyr 的元工具，在幕后调用 ``cmake`` 和底层构建工具（``ninja`` 或 ``make``）），但你也可以选择在需要时直接调用 ``cmake``。在 Linux 和 macOS 上，你可以在 ``make`` 和 ``ninja`` 生成器（即构建工具）之间选择，而在 Windows 上你必须使用 ``ninja``，因为 ``make`` 在该平台上不受支持。为简单起见，本指南将全程使用 ``ninja``，如果你选择使用 ``west build`` 来构建应用，要知道它默认在底层使用 ``ninja``。

作为示例，让我们为 ``reel_board`` 构建 Hello World 示例：

.. zephyr-app-commands::
   :tool: all
   :zephyr-app: samples/hello_world
   :board: reel_board
   :goals: build

在 Linux 和 macOS 上，你还可以使用 ``make`` 代替 ``ninja`` 进行构建：

使用 west：

- 仅一次使用 ``make``，在 west build 命令行中添加 ``-- -G"Unix Makefiles"``；参见 :ref:`west build <west-building-generator>` 文档中的示例。
- 从现在开始默认使用 ``make``，运行 ``west config build.generator "Unix Makefiles"``。

直接使用 CMake：

.. zephyr-app-commands::
   :tool: cmake
   :zephyr-app: samples/hello_world
   :generator: make
   :host-os: unix
   :board: reel_board
   :goals: build


基础
======

#. 导航到应用目录 :file:`<app>`。
#. 输入以下命令，为命令行参数中指定的开发板构建应用的 :file:`zephyr.elf` 镜像：

   .. zephyr-app-commands::
      :tool: all
      :cd-into:
      :board: <board>
      :goals: build

   如果需要，你可以使用 :code:`CONF_FILE` 参数通过替代的 :file:`.conf` 文件中指定的配置设置来构建应用。这些设置将覆盖应用 :file:`.config` 文件或其默认 :file:`.conf` 文件中的设置。例如：

   .. zephyr-app-commands::
      :tool: all
      :cd-into:
      :board: <board>
      :gen-args: -DCONF_FILE=prj.alternate.conf
      :goals: build
      :compact:

   如前一节所述，你也可以选择通过导出 :makevar:`BOARD` 和 :makevar:`CONF_FILE` 环境变量或在 :file:`CMakeLists.txt` 中使用 ``set()`` 语句设置它们的值来永久设置开发板和配置设置。此外，``west`` 允许你 :ref:`设置默认开发板 <west-building-config>`。

.. _build-directory-contents:

构建目录内容
========================

使用 Ninja 生成器时，构建目录看起来像这样：

.. code-block:: none

   <app>/build
   ├── build.ninja
   ├── CMakeCache.txt
   ├── CMakeFiles
   ├── cmake_install.cmake
   ├── rules.ninja
   └── zephyr

构建目录中最值得注意的文件是：

* :file:`build.ninja`，可调用以构建应用。

* :file:`zephyr` 目录，它是生成的构建系统的工作目录，大多数生成的文件在此创建和存储。

运行 ``ninja`` 后，以下构建输出文件将写入构建目录的 :file:`zephyr` 子目录中。（这 **不是 Zephyr 基础目录**，后者包含 Zephyr 源代码等，在上文中已描述。）

* :file:`.config`，包含用于构建应用的配置设置。

  .. note::

     每当配置更新时，:file:`.config` 的先前版本会保存到 :file:`.config.old`。这是为了方便，因为比较新旧版本可能很有用。

* 各种目标文件（:file:`.o` 文件和 :file:`.a` 文件），包含编译后的内核和应用代码。

* :file:`zephyr.elf`，包含最终合并的应用和内核二进制文件。还支持其他二进制输出格式，例如 :file:`.hex` 和 :file:`.bin`。

.. _application_rebuild:

重新构建应用
=========================

应用开发通常在持续测试更改时最快。随着应用变得更加复杂，频繁重新构建应用可以使调试不那么痛苦。通常在应用源文件、CMakeLists.txt 文件或配置设置发生重大更改后重新构建并测试是个好主意。

.. important::

    Zephyr 构建系统仅重新构建可能受更改影响的应用镜像部分。因此，重新构建应用通常比首次构建快得多。

有时构建系统未能正确重新构建应用，因为它未能重新编译一个或多个必需文件。你可以按以下操作强制构建系统从头重新构建整个应用：

#. 在主机计算机上打开终端控制台，导航到构建目录 :file:`<app>/build`。

#. 根据你想使用 ``west`` 还是直接使用 ``cmake``，输入以下命令之一，删除应用生成的文件，但包含应用当前配置信息的 :file:`.config` 文件除外。

   .. code-block:: console

      west build -t clean

   或者

   .. code-block:: console

      ninja clean

   或者，输入以下命令之一，删除 *所有* 生成的文件，包括包含应用当前配置信息的 :file:`.config` 文件（针对那些开发板类型）。

   .. code-block:: console

      west build -t pristine

   或者

   .. code-block:: console

      ninja pristine

   如果你使用 west，可以利用其能力在需要时自动 :ref:`使构建文件夹恢复原始状态 <west-building-config>`。

#. 按上文 :ref:`build_an_application` 中指定的步骤正常重新构建应用。

.. _application_board_version:

为开发板修订版构建
=============================

Zephyr 构建系统支持为具有微小差异的单个开发板的多个硬件修订版进行指定。使用修订版使开发板支持文件能够对开发板配置进行微调，而无需为每个修订版复制 :ref:`create-your-board-directory` 中描述的所有文件。

要为特定修订版构建，使用 ``<board>@<revision>`` 或 ``<board>@<revision>/<qualifiers>`` 代替普通的 ``<board>`` 或 ``<board>/<qualifiers>``。例如：

.. zephyr-app-commands::
   :tool: all
   :cd-into:
   :board: nrf9160dk@0.14.0/nrf9160/ns
   :goals: build
   :compact:

查看你的开发板文档以了解它是否有多个修订版以及支持哪些修订版。

当目标为开发板修订版时，活动的修订版将在 CMake 配置阶段打印出来，如下所示：

.. code-block:: console

   -- Board: plank, Revision: 1.5.0

.. _application_run:

运行应用
******************

应用镜像可以在真实开发板或仿真硬件上运行。

.. _application_run_board:

在开发板上运行
==================

Zephyr 支持的大多数开发板都允许你使用 ``west flash`` 烧录编译后的二进制文件，将二进制文件复制到开发板并运行它。按以下说明在真实硬件上烧录并运行应用：

#. 如 :ref:`build_an_application` 所述构建你的应用。

#. 确保你的开发板已连接到主机计算机。通常你通过 USB 完成此操作。

#. 从构建目录 :file:`<app>/build` 运行以下控制台命令，将编译后的 Zephyr 镜像烧录到你的开发板并运行：

   .. code-block:: console

     west flash

Zephyr 构建系统与开发板支持文件集成，使用硬件特定工具将 Zephyr 二进制文件烧录到你的硬件，然后运行它。

每次运行 flash 命令时，你的应用都会被重新构建并再次烧录。

在开发板支持不完整的情况下，通过 Zephyr 构建系统烧录可能不受支持。如果你收到关于 flash 支持不可用的错误消息，请参阅 :ref:`你的开发板文档 <boards>` 以获取有关如何烧录开发板的额外信息。

.. note:: 在 Linux 上开发时，通常需要安装开发板特定的 udev 规则，以便以非 root 用户身份通过 USB 设备访问你的开发板。如果烧录失败，请参阅你的开发板文档查看这是否必要。

.. _application_run_qemu:

在仿真器中运行
=====================

Zephyr 内置了对 QEMU 的仿真器支持。它允许你在（或代替）将应用加载到实际目标硬件上运行之前虚拟地运行和测试应用。

有关在 Windows 上所需的额外步骤，请参阅 :ref:`beyond-GSG`。

按以下说明通过 QEMU 运行应用：

#. 如 :ref:`build_an_application` 所述，为你的应用构建一个 QEMU 开发板。

   例如，你可以将 ``BOARD`` 设置为：

   - ``qemu_x86`` 以仿真在基于 x86 的开发板上运行
   - ``qemu_cortex_m3`` 以仿真在基于 ARM Cortex M3 的开发板上运行

#. 从构建目录 :file:`<app>/build` 运行以下控制台命令之一，在 QEMU 中运行 Zephyr 二进制文件：

   .. code-block:: console

     west build -t run

   或者

   .. code-block:: console

     ninja run

#. 按 :kbd:`Ctrl A, X` 停止应用在 QEMU 中运行。

   应用停止运行，终端控制台提示符重新显示。

每次执行 run 命令时，你的应用都会被重新构建并再次运行。


.. note::

   如果安装了 :ref:`Zephyr SDK <toolchain_zephyr_sdk>`，``run`` 目标默认使用 SDK 的 QEMU 二进制文件。要使用其他版本的 QEMU，:ref:`设置环境变量 <env_vars>` ``QEMU_BIN_PATH`` 为你想要使用的 QEMU 二进制文件的路径。

.. note::

   你可以在目标名称后追加 ``_<emulator>`` 来选择特定的仿真器，例如 QEMU 的 ``west build -t run_qemu`` 或 ``ninja run_qemu``。

.. _custom_board_definition:

自定义开发板、设备树和 SoC 定义
********************************************

如果你正在开发的开发板或平台尚未被 Zephyr 支持，你可以向应用添加开发板、设备树和 SoC 定义，而无需将它们添加到 Zephyr 树中。

支持树外开发板和 SoC 开发所需的结构与 Zephyr 树中维护开发板及 SoC 的方式类似。通过使用这种结构，在你完成初始开发后，将你的平台相关工作上游到 Zephyr 树将更容易得多。

使用以下结构将自定义开发板添加到你的应用或专用仓库中：

.. code-block:: console

   boards/
   soc/
   CMakeLists.txt
   prj.conf
   README.rst
   src/

其中 ``boards`` 目录承载你正在构建的目标开发板：

.. code-block:: console

   .
   ├── boards
   │   └── vendor
   │       └── my_custom_board
   │           ├── doc
   │           │   └── img
   │           └── support
   └── src

``soc`` 目录承载任何 SoC 代码。你也可以拥有由 Zephyr 树中可用的 SoC 支持的开发板。

开发板
======

使用厂商名称作为文件夹名称（如果向 Zephyr 上游提交，必须与 :zephyr_file:`dts/bindings/vendor-prefixes.txt` 中的厂商前缀匹配，或者如果不是厂商开发板则为 ``others``），放在 ``boards`` 下的 ``my_custom_board`` 中。

文档（在 ``doc/`` 下）和支持文件（在 ``support/`` 下）是可选的，但在向 Zephyr 提交时将需要。

``my_custom_board`` 的内容应遵循任何 Zephyr 开发板的相同指南，并提供以下文件::

    board.yml
    my_custom_board_defconfig
    my_custom_board.dts
    my_custom_board.yaml
    board.cmake
    board.h
    CMakeLists.txt
    doc/
    Kconfig.my_custom_board
    Kconfig.defconfig
    support/


一旦开发板结构就位，你可以通过向 CMake 构建系统指定 ``-DBOARD_ROOT`` 参数来指定自定义开发板信息的位置，从而针对该开发板构建你的应用：

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DBOARD_ROOT=<path to boards>
   :goals: build
   :compact:

这将使用你的自定义开发板配置，并将 Zephyr 二进制文件生成到你的应用目录中。

你也可以在应用 :file:`CMakeLists.txt` 文件中定义 ``BOARD_ROOT`` 变量。确保在通过 ``find_package(Zephyr ...)`` 引入 Zephyr 样板代码 **之前** 这样做。

.. note::

   如果在 CMakeLists.txt 中指定 ``BOARD_ROOT``，则必须提供绝对路径，例如 ``list(APPEND BOARD_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-board-root>)``。使用 ``-DBOARD_ROOT=<board-root>`` 时，绝对和相对路径都可以使用。相对路径相对于应用目录处理。

.. note::

   如果使用 sysbuild，则必须在模块中或 sysbuild 的 ``CMakeLists.txt`` 文件中定义 ``BOARD_ROOT``，详见 :ref:`sysbuild_var_override`。

SoC 定义
================

与开发板支持类似，结构类似于 Zephyr 树中维护 SoC 的方式，例如：

.. code-block:: none

        soc
        └── st
            └── stm32
                ├── common
                └── stm32l0x


文件 :zephyr_file:`soc/Kconfig` 将在 Kconfig 中创建顶层 ``SoC/CPU/Configuration Selection`` 菜单。

树外 SoC 定义可以使用 ``SOC_ROOT`` CMake 变量添加到该菜单中。该变量包含以分号分隔的目录列表，这些目录包含 SoC 支持文件。

遵循上述结构，可以添加以下文件以将更多 SoC 加载到菜单中。

.. code-block:: none

        soc
        └── st
            └── stm32
                └── stm32l0x
                    ├── Kconfig
                    ├── Kconfig.soc
                    └── Kconfig.defconfig

上述 Kconfig 文件可以描述 SoC 或加载额外的 SoC Kconfig 文件。

在此结构中加载 ``stm32l0`` 特定 Kconfig 文件的示例：

.. code-block:: none

        soc
        └── st
            └── stm32
                ├── Kconfig.soc
                └── stm32l0x
                    └── Kconfig.soc

可以通过 ``st/stm32/Kconfig.soc`` 中的以下内容完成：

.. code-block:: kconfig

   rsource "*/Kconfig.soc"

一旦 SoC 结构就位，你可以通过向 CMake 构建系统指定 ``-DSOC_ROOT`` 参数来指定自定义平台信息的位置，从而针对该平台构建你的应用：

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DSOC_ROOT=<path to soc> -DBOARD_ROOT=<path to boards>
   :goals: build
   :compact:

这将使用你的自定义平台配置，并将 Zephyr 二进制文件生成到你的应用目录中。

有关在模块的 :file:`zephyr/module.yml` 文件中设置 SOC_ROOT 的信息，请参阅 :ref:`modules_build_settings`。

或者你可以在应用 :file:`CMakeLists.txt` 文件中定义 ``SOC_ROOT`` 变量。确保在通过 ``find_package(Zephyr ...)`` 引入 Zephyr 样板代码 **之前** 这样做。

.. note::

   如果在 CMakeLists.txt 中指定 ``SOC_ROOT``，则必须提供绝对路径，例如 ``list(APPEND SOC_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-soc-root>``。使用 ``-DSOC_ROOT=<soc-root>`` 时，绝对和相对路径都可以使用。相对路径相对于应用目录处理。

.. _dts_root:

设备树定义
====================

设备树目录树位于 ``APPLICATION_SOURCE_DIR``、``BOARD_DIR`` 和 ``ZEPHYR_BASE`` 中，但可以通过创建以下目录树来添加额外的树（或 DTS_ROOT）::

    include/
    dts/common/
    dts/arm/
    dts/
    dts/bindings/

其中 'arm' 更改为适当的架构。每个目录都是可选的。绑定目录包含绑定，其他目录包含可从 DT 源包含的文件。

一旦目录结构就位，你可以通过 ``DTS_ROOT`` CMake 缓存变量指定其位置来使用它：

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DDTS_ROOT=<path to dts root>
   :goals: build
   :compact:

你也可以在应用 :file:`CMakeLists.txt` 文件中定义该变量。确保在通过 ``find_package(Zephyr ...)`` 引入 Zephyr 样板代码 **之前** 这样做。

.. note::

   如果在 CMakeLists.txt 中指定 ``DTS_ROOT``，则必须提供绝对路径，例如 ``list(APPEND DTS_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/<extra-dts-root>``。使用 ``-DDTS_ROOT=<dts-root>`` 时，绝对和相对路径都可以使用。相对路径相对于应用目录处理。

设备树源通过 C 预处理器传递，因此你可以包含可以位于 ``DTS_ROOT`` 目录中的文件。按约定，设备树包含文件有 ``.dtsi`` 扩展名。

你还可以使用预处理器来控制设备树文件的内容，通过 ``DTS_EXTRA_CPPFLAGS`` CMake 缓存变量指定指令：

.. zephyr-app-commands::
   :tool: all
   :board: <board name>
   :gen-args: -DDTS_EXTRA_CPPFLAGS=-DTEST_ENABLE_FEATURE
   :goals: build
   :compact:

.. _CMake: https://www.cmake.org
.. _CMake introduction: https://cmake.org/cmake/help/latest/manual/cmake.1.html#description
.. _CMake list: https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#lists
.. _example-application: https://github.com/zephyrproject-rtos/example-application
