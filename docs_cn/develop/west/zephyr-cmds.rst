.. _west-zephyr-ext-cmds:

额外的 Zephyr 扩展命令
####################################

本页记录杂项 :ref:`west-zephyr-extensions`。

.. _west-boards:

列出板卡：``west boards``
*******************************

``boards`` 命令可用于列出 Zephyr 支持的板卡，
而无需诉诸额外的信息来源。

可以通过键入以下命令运行::

  west boards

该命令以默认格式列出所有受支持的板卡。
如果你希望自己指定显示格式，
可以使用 ``--format``（或 ``-f``）标志::

  west boards -f "{arch}:{name}"

关于格式选项的更多帮助可以通过运行以下命令获取::

  west boards -h

.. _west-completion:

Shell 补全脚本：``west completion``
*********************************************

``completion`` 扩展命令输出 shell 补全脚本，
然后可以直接用于为受支持的 shell 启用补全。

它目前支持以下 shell：

- bash
- zsh
- fish
- powershell（仅板卡限定符）

更多说明可在命令的帮助中获取::

  west help completion

.. _west-zephyr-export:

安装 CMake 包：``west zephyr-export``
*************************************************

该命令将当前 Zephyr 安装注册为
CMake 用户包注册表中的一个 CMake 配置包。

在 Windows 中，CMake 用户包注册表位于
``HKEY_CURRENT_USER\Software\Kitware\CMake\Packages``。

在 Linux 和 MacOS 中，CMake 用户包注册表位于
:file:`~/.cmake/packages`。

你可以在设置 Zephyr 工作区时运行此命令。
如果你这样做，工作区之外的应用 CMakeLists.txt 文件
将能够使用以下内容找到 Zephyr 仓库：

.. code-block:: cmake

   find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

详情参见 :zephyr_file:`share/zephyr-package/cmake`。

.. _west-spdx:

软件物料清单：``west spdx``
*****************************************

该命令为 Zephyr 构建生成一份软件物料清单（SBOM），
作为一组 `SPDX`_ 文档。
它记录了进入构建的源文件、它们产生的构建产物，
以及它们之间的关系。
在源文件中找到的 ``SPDX-License-Identifier`` 注释
会被扫描并填入文档中，连同文件哈希值和（尽力而为的）版权声明。

.. _west-spdx-versions:

选择 SPDX 版本
------------------------

``west spdx`` 可以输出两个主要 SPDX 规范系列中的任一个。
SPDX 2.3 是默认值；使用 ``--spdx-version`` 选项选择其他版本。

SPDX 2.3 是 2.2 的超集，并添加了诸如
``PrimaryPackagePurpose`` 之类的字段。
为兼容尚不理解 SPDX 3 的工具，选择 SPDX 2.x；
为获取 :ref:`west-spdx-build-profile` 中描述的
更丰富的机器可读构建来源信息，选择 SPDX 3.0 或更高版本。

.. note::

   SPDX 3.1 支持是实验性的：SPDX 3.1 规范仍在开发中。

生成 SPDX 文档
-------------------------

#. 在你的项目中启用 :kconfig:option:`CONFIG_BUILD_OUTPUT_META`，
   以便构建记录 ``west spdx`` 所需的信息。

#. 构建你的应用：

   .. code-block:: bash

      west build -d BUILD_DIR [...]

#. 使用此构建目录生成 SPDX 文档：

   .. code-block:: bash

      west spdx -d BUILD_DIR

   这默认生成 SPDX 2.3 标签值文档。
   若要改为生成 SPDX 2.2 或 3.0 文档，传入 ``--spdx-version``：

   .. code-block:: bash

      west spdx -d BUILD_DIR --spdx-version 3.0

.. note::

   使用 :ref:`sysbuild` 构建时，
   确保你针对的是你想要生成 SBOM 的实际应用。
   例如，如果应用名为 ``hello_world``：

   .. code-block:: bash

     west build --sysbuild -d BUILD_DIR
     west spdx -d BUILD_DIR/hello_world

输出文档
----------------

文档写入 :file:`BUILD_DIR/spdx/`（用 ``-s`` 覆盖）。
无论 SPDX 版本如何，都会生成同一组物料清单（BOM）文档；
只有文件扩展名不同：
SPDX 2.x 标签值格式用 ``.spdx``，
SPDX 3.0 JSON-LD 格式用 ``.jsonld``：

- ``app``：用于构建的应用源文件的 BOM
- ``zephyr``：用于构建的特定 Zephyr 源代码文件的 BOM
- ``build``：构建输出文件的 BOM
- ``modules-deps``：模块依赖项的 BOM。
  更多细节请查看 :ref:`modules
  <modules-vulnerability-monitoring>`。

对于 SPDX 3.0，每个文档都声明了对 Core、Software 和 Simple Licensing
配置文件（profiles）的合规性，
:file:`build.jsonld` 还额外声明了
:ref:`Build profile
<west-spdx-build-profile>`，
它捕获了产物是如何产生的。

物料清单中的每个文件都会被扫描，
以便记录其哈希值（SHA256、SHA1 和 MD5），
以及如果文件中出现 ``SPDX-License-Identifier`` 注释时
检测到的任何许可证。

版权声明使用 REUSE 组的第三方 :command:`reuse` 工具提取。
找到时，这些声明作为 ``FileCopyrightText`` 字段（SPDX 2.x）
或版权属性（SPDX 3.0）添加到 SPDX 文档中。

.. note::
   版权提取使用可能无法捕获完整声明文本的启发式方法，
   因此 ``FileCopyrightText`` 内容是尽力而为的。
   这与 SPDX 规范的建议一致。

关系
-------------

创建 SPDX 关系以指示 CMake 构建目标之间的依赖关系、
相互链接的构建目标，
以及编译以生成已构建库文件的源文件。

两个规范系列以不同方式表达构建来源：

- 在 **SPDX 2.x** 中，每个生成的产物都携带文件级的
  ``GENERATED_FROM`` 关系，
  指向其编译来源的源文件（以及使用 ``--analyze-includes`` 时的头文件）。

- 在 **SPDX 3.0** 中，该来源改由
  :ref:`Build profile <west-spdx-build-profile>` 承载，
  使用限定于 ``build`` 生命周期的
  ``hasInput``/``hasOutput``/``usesTool`` 关系。

.. _west-spdx-build-profile:

构建配置文件（SPDX 3.0）
------------------------

生成 SPDX 3.0 文档时，``west spdx`` 填充
`SPDX 3.0 Build profile`_，
以便 SBOM 不仅记录*构建了什么*，
还记录*如何构建*。
信息自动从 CMake file-API 收集，
存放在 :file:`build.jsonld` 中。

该配置文件添加一个描述整体构建的 ``build_Build`` 元素：
其构建类型、CMake 生成器和构建配置，
以及选定的环境变量（如 ``BOARD`` 和 ``ARCH``）。
工具链（CMake、编译器、汇编器、链接器和打包器）
作为 ``Tool`` 元素记录，每个元素带有其路径和版本。
构建范围的关系然后将构建与其输入（源包和编译文件）、
输出（最终镜像）以及所使用的工具关联起来。

每个中间目标（如静态库）也会获得自己的子构建，
捕获产生其产物的确切源文件、工具和编译标志，
因此任何输出都可以追溯到其构建方式。

命令行选项
--------------------

``west spdx`` 接受以下额外选项：

- ``-i``、``--init``：在构建目录配置之前
  在其中创建 CMake file-based API 查询。
  已弃用，并将在 Zephyr 5.0 中移除：
  带有 :kconfig:option:`CONFIG_BUILD_OUTPUT_META` 的构建
  现在自身就请求该查询。

- ``-n PREFIX``：将包含在生成的 SPDX 文档中的
  文档命名空间（Document Namespaces）的前缀。
  详情参见 `SPDX specification clause 6`_。
  如果省略 ``-n``，将根据第 2.5 节中描述的默认格式
  使用随机 UUID 生成默认命名空间。

- ``-s SPDX_DIR``：指定一个替代目录，
  SPDX 文档应写入该目录，
  而不是 :file:`BUILD_DIR/spdx/`。

- ``--spdx-version {2.2,2.3,3.0,3.1}``：
  指定使用哪个 SPDX 规范版本。
  默认为 ``2.3``。
  版本之间的差异参见 :ref:`west-spdx-versions`。

- ``--analyze-includes``：除了记录编译的源代码文件
  （如 ``.c``、``.S``）在物料清单中，
  还尝试确定每个 ``.c`` 文件包含的特定头文件。

  这需要更长时间，
  因为它使用与构建时相同参数，
  对每个 ``.c`` 文件执行 C 编译器的试运行。

- ``--include-sdk``：与 ``--analyze-includes`` 一起，
  还创建第四份 SPDX 文档
  :file:`sdk.spdx`（或 :file:`sdk.jsonld`），
  列出从 SDK 包含的头文件。

.. warning::

   目前不支持为 ``native_sim`` 平台生成 SBOM 文档。

.. _SPDX: https://spdx.dev/

.. _SPDX 3.0 Build profile:
   https://spdx.github.io/spdx-spec/v3.0.1/model/Build/Build/

.. _SPDX specification clause 6:
   https://spdx.github.io/spdx-spec/v2.2.2/document-creation-information/

.. _west-blobs:

处理二进制 blob：``west blobs``
*****************************************

``blobs`` 命令允许用户通过其 :ref:`module.yml <module-yml>` 文件
与一个或多个 :ref:`modules <modules>` 中声明的
:ref:`binary blobs
<bin-blobs>` 进行交互。

``blobs`` 命令有三个子命令，
用于列出、获取或清理（即删除）二进制 blob 本身。

你可以通过指定输出格式来列出二进制 blob::

  west blobs list -f '{module}: {type} {path}'

要获取 ``-f/--format`` 中可用的完整变量集，
运行 ``west blobs -h``。

获取 blob 的方式类似::

  west blobs fetch

注意，如 :ref:`modules 章节 <modules-bin-blobs>` 中所述，
获取的 blob 存储在相对于相应模块仓库根目录的
:file:`zephyr/blobs/` 文件夹中。

删除它们的方式也类似::

  west blobs clean

此外，该工具允许你通过键入模块名作为命令行参数
来指定要列出、获取或清理 blob 的模块。

可以向 ``west blobs fetch`` 传入参数 ``--allow-regex``
来通过传入正则表达式限制获取的特定 blob::

  # For example, only download esp32 blobs, skip the other variants
  west blobs fetch hal_espressif --allow-regex 'lib/esp32/.*'

可以通过 ``--auto-cache`` 命令行参数
或 ``blobs.auto-cache`` 配置选项提供自动缓存目录。
启用后，每当 blob 缺失并被下载时，
自动缓存目录会自动填充。

可以在 ``--cache-dirs`` 命令行参数
或 ``blobs.cache-dirs`` 配置选项中提供
一个或多个额外的缓存目录（用 ``;`` 分隔）。

``west blobs fetch`` 在所有已配置的缓存目录
（包括自动缓存）中搜索匹配的 blob 文件名。
缓存文件可以存储在其原始文件名下，
或带有 SHA-256 后缀（``<filename>.<sha>``）。
如果找到，blob 从缓存复制到 blob 路径；
否则从其 URL 下载到 blob 路径。

.. _west-twister:

Twister 封装器：``west twister``
*********************************

该命令是 :ref:`twister <twister_script>` 的封装器。

然后可以通过 west 如下调用 Twister::

  west twister -help
  west twister -T tests/ztest/base

.. _west-bindesc:

处理二进制描述符：``west bindesc``
*************************************************

``bindesc`` 命令允许用户读取可执行文件的
:ref:`binary descriptors<binary_descriptors>`。
它目前支持 ``.bin``、``.hex``、``.elf`` 和 ``.uf2`` 文件作为输入。

你可以在镜像中搜索特定描述符，例如::

   west bindesc search KERNEL_VERSION_STRING build/zephyr/zephyr.bin

你可以按类型和 ID 搜索自定义描述符，例如::

   west bindesc custom_search STR 0x200 build/zephyr/zephyr.bin

你可以使用以下命令转储镜像中的所有描述符::

   west bindesc dump build/zephyr/zephyr.bin

你可以使用以下命令将镜像的描述符数据区域提取到文件::

   west bindesc extract

你可以使用以下命令列出所有已知的标准描述符名称::

   west bindesc list

你可以使用以下命令打印描述符在镜像中的偏移量::

   west bindesc get_offset

用 GNU Global 对源代码进行索引：``west gtags``
****************************************************

.. important:: 你必须安装 `GNU Global`_ 提供的
               ``gtags`` 和 ``global`` 程序才能使用此命令。

``west gtags`` 命令让你为整个 west 工作区
创建一个 GNU Global tags 文件::

  west gtags

.. _GNU Global: https://www.gnu.org/software/global/

这将在工作区 :ref:`topdir <west-workspace>` 中
创建一个名为 ``GTAGS`` 的 tags 文件
（它还会在同一位置创建其他名为 ``GPATH`` 和 ``GRTAGS`` 的
Global 相关元数据文件）。

然后你可以在工作区内的任何地方运行 ``global`` 命令，
使用此 tags 文件搜索符号位置。

例如，从 ``zephyr/drivers`` 目录开始
搜索 ``arch_system_halt()`` 函数的定义::

  $ cd zephyr/drivers
  $ global -x arch_system_halt
  arch_system_halt   65 ../arch/arc/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt  455 ../arch/arm64/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt  137 ../arch/nios2/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt   18 ../arch/posix/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt   17 ../arch/x86/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt  126 ../arch/xtensa/core/fatal.c FUNC_NORETURN void arch_system_halt(unsigned int reason)
  arch_system_halt   21 ../kernel/fatal.c FUNC_NORETURN __weak void arch_system_halt(unsigned int reason)

这打印搜索的符号、其定义所在的行、
其定义所在文件的相对路径，以及该行本身，
涵盖符号定义的所有位置。

额外提示：

- 这也有助于搜索供应商 HAL 函数定义。

- 更多信息参见 ``global`` 命令的手册页，
  了解如何使用此工具。

- 你应该运行 ``global``，而**不是** ``west global``。
  由于 ``global`` 已经会从你当前的工作目录开始
  搜索 ``GTAGS`` 文件，因此不需要单独的
  ``west global`` 命令。这就是为什么你需要
  从工作区内部运行 ``global``。

.. _west-patch:

处理补丁：``west patch``
************************************

``patch`` 命令允许用户以受控的方式向 Zephyr 或 Zephyr 模块
应用补丁，使得使用 :ref:`T2 star topology <west-t2>` 的
外部应用更容易进行自动化和跟踪。
:ref:`patches.yml <patches-yml>` 文件存储
关于补丁文件的元数据，并填补官方 Zephyr 版本发布之间的空白，
使用户可以轻松查看任何上游化工作的状态，
并在升级到下一个 Zephyr 版本之前
确定要放弃哪些补丁。

有若干可用的子命令来管理工作区中 Zephyr 或其他模块的补丁：

* ``apply``：应用 ``patches.yml`` 中列出的补丁
* ``reverse``：反转之前已应用的 ``patches.yml`` 中列出的补丁
* ``clean``：移除所有已应用的补丁，并重置到 manifest 检出状态
* ``list``：列出 ``patches.yml`` 中的所有补丁
* ``gh-fetch``：从 GitHub pull request 获取补丁

.. code-block:: none

    west-workspace/
    └── application/
       ...
       ├── west.yml
       └── zephyr
           ├── module.yml
           ├── patches
           │   ├── bootloader
           │   │   └── mcuboot
           │   │       └── my-tweak-for-mcuboot.patch
           │   └── zephyr
           │       └── my-zephyr-change.patch
           └── patches.yml

在这个示例中，:ref:`west manifest <west-manifests>` 文件
``west.yml`` 将固定到特定的 Zephyr 修订版
（如 ``v4.1.0``），并针对该修订版的 Zephyr
以及应用中使用的其他模块的特定修订版应用补丁。
然而，该应用需要两个更改才能满足要求；
一个用于 Zephyr，另一个用于 MCUBoot。

.. _patches-yml:

.. code-block:: yaml

    patches:
      - path: zephyr/my-zephyr-change.patch
        sha256sum: c676cd376a4d19dc95ac4e44e179c253853d422b758688a583bb55c3c9137035
        module: zephyr
        author: Obi-Wan Kenobi
        email: obiwan@jedi.org
        date: 2025-05-04
        upstreamable: false
        comments: |
          An application-specific change we need for Zephyr.
      - path: bootloader/mcuboot/my-tweak-for-mcuboot.patch
        sha256sum: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        module: mcuboot
        author: Darth Sidious
        email: sidious@sith.org
        date: 2025-05-04
        merge-pr: https://github.com/zephyrproject-rtos/zephyr/pull/<pr-number>
        issue: https://github.com/zephyrproject-rtos/zephyr/issues/<issue-number>
        merge-status: true
        merge-commit: 1234567890abcdef1234567890abcdef12345678
        merge-date: 2025-05-06
        apply-command: git apply
        comments: |
          A change to mcuboot that has been merged already. We can remove this
          patch when we are ready to upgrade to the next Zephyr release.

补丁可以轻松地以自动化方式应用。例如：

.. code-block:: bash

    west init -m <manifest repo> <workspace>
    cd <workspace>
    west update
    west patch apply

当需要更新到更新版本的 Zephyr 时，
可以更新 ``west.yml`` 文件指向下一个 Zephyr 版本，
如 ``v4.2.0``。
不再需要的补丁（如上面示例中的
``my-tweak-for-mcuboot.patch``）
可以从 ``patches.yml`` 和外部应用仓库中移除，
然后运行以下命令。

.. code-block:: bash

    west patch clean
    west update
    west patch apply --roll-back # roll-back all patches if one does not apply cleanly

可选地，可以反转补丁而不是清理所有模块。
这保留了不冲突的、与模块无关的编辑，
但仅移除由补丁所做的更改。
这在开发补丁并在应用中测试它们时很有用，
但不想清理所有补丁并丢失对模块所做的任何手动编辑。

.. code-block:: bash

    west patch reverse

如果补丁需要重新制作，
记得用新的 SHA256 校验和更新 ``patches.yml`` 文件。

.. code-block:: bash

    sha256sum zephyr/patches/zephyr/my-zephyr-change.patch
    7d57ca78d5214f422172cc47fed9d0faa6d97a0796c02485bff0bf29455765e9

还可以使用 ``west patch gh-fetch``
从 GitHub pull request 获取补丁，
并自动创建或更新 ``patches.yml`` 文件。
当作者已经在现有的上游 pull request 中
捕获了若干更改时，这很有用。

.. code-block:: bash

    west patch gh-fetch --owner zephyrproject-rtos --repo zephyr --pull-request <pr-number> \
      --module zephyr --split-commits

上面的命令将创建以下目录和文件结构，
其中包括与给定 pull request 关联的
每个单独提交的补丁。

.. code-block:: none

    zephyr
    ├── patches
    │   ├── first-commit-from-pr.patch
    │   ├── second-commit-from-pr.patch
    │   └── third-commit-from-pr.patch
    └── patches.yml

处理 Zephyr SDK：``west sdk``
*****************************************

``west sdk`` 命令是一个 Zephyr 特定的 west 命令，
用于列出和安装 Zephyr SDK 及其工具链。

列出 SDK 和工具链
---------------------------

要列出已安装的 Zephyr SDK 以及可用的 SDK 版本
和工具链，运行：

.. code-block:: console

   west sdk list

该命令显示：

- 已安装的 SDK 版本
- 可用的 SDK 版本
- 每个 SDK 中包含的工具链

安装 Zephyr SDK
-------------------------

要安装 Zephyr SDK，运行：

.. code-block:: console

   west sdk install

该命令可能以交互模式运行，
提示选择 SDK 或工具链。
当通过 ``--toolchains`` 提供特定工具链时，
命令以非交互方式运行，这推荐用于自动化。

要仅安装特定工具链，使用 ``--toolchains`` 选项：

.. code-block:: console

   west sdk install --toolchains arm-zephyr-eabi riscv64-zephyr-elf

如果你不确定需要哪些工具链，
先运行 ``west sdk list`` 查看可用选项，
避免下载不必要的工具链，
这可以节省数 GB 的磁盘空间和下载时间。
