配置
#############

LLEXT 子系统提供以下 Kconfig 选项。

.. _llext_kconfig_heap:

哈佛架构
--------------------

:kconfig:option:`CONFIG_HARVARD`

        该架构使用相互独立的指令存储器和数据存储器。

:kconfig:option:`CONFIG_HARVARD`
 不是 LLEXT 子系统定义的 Kconfig 选项。相反，
它必须由板级或 SoC 定义并选中，以表明 LLEXT 应构建为支持哈佛架构。板级或
 SoC 还必须实现 :c:func:`arch_is_instr_mem`。

堆大小
----------

LLEXT 子系统需要为扩展相关数据分配一块堆。当分配静态堆时，以下选项控制这一分配。

:kconfig:option:`CONFIG_LLEXT_HEAP_SIZE`

        LLEXT 堆的大小，单位为千字节。

对于使用哈佛架构的板级，LLEXT 堆被拆分为两个：一个位于指令存储器中，另一个位于数据存储器中。以下选项控制这些分配。

:kconfig:option:`CONFIG_LLEXT_INSTR_HEAP_SIZE`

        指令存储器中 LLEXT 堆的大小，单位为千字节。

:kconfig:option:`CONFIG_LLEXT_DATA_HEAP_SIZE`

        数据存储器中 LLEXT 堆的大小，单位为千字节。

或者，应用程序可以使用以下选项配置一个动态堆。

:kconfig:option:`CONFIG_LLEXT_HEAP_DYNAMIC`

        某些应用需要将扩展加载到在启动时不存在、因而无法静态分配的存储器中。由应用程序负责
         LLEXT 堆的分配，不要静态分配 LLEXT 堆。

        应用程序必须调用 :c:func:`llext_heap_init` 以指定用作
         LLEXT 堆的缓冲区，否则 LLEXT 模块将无法加载。
        当应用程序不再需要 LLEXT 功能时，应调用 :c:func:`llext_heap_uninit`，
        将缓冲区的控制权交还给应用程序。

.. note::

   启用 :ref:`用户模式 <usermode_api>` 时，
   堆大小必须足够大，以便扩展段能够按架构要求的对齐方式分配。

.. note::

   在哈佛架构上，应用程序必须调用 :c:func:`llext_heap_init_harvard`。

LLEXT 堆的底层数据结构默认是 :c:struct:`k_heap`，但可以通过为 :
kconfig:option:`CONFIG_LLEXT_HEAP_MANAGEMENT`
 选中 :kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK`，将其改为
  :c:type:`sys_mem_blocks_t`（用于非元数据，即扩展区域）。

:kconfig:option:`CONFIG_LLEXT_HEAP_MANAGEMENT`

        选择用于在 LLEXT 堆存储器中存放扩展区域的内存管理 API。此选择不影响 LLEXT
         元数据，元数据始终使用 :c:struct:`k_heap` 管理。

:kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK`

        使用 :c:type:`sys_mem_blocks_t` API 管理扩展区域的 LLEXT
         堆存储器。每个区域至少分配一个块。块大小的选择必须谨慎，以确保扩展区域获得正确的对齐。

.. note::

   :kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK` 不支持
    :kconfig:option:`CONFIG_LLEXT_HEAP_DYNAMIC`。

堆将被拆分为两个，各子堆的大小由以下选项控制。

:kconfig:option:`CONFIG_LLEXT_EXT_HEAP_SIZE`

        可供 LLEXT 扩展段使用的堆大小，单位为千字节。必须是 :kconfig:optio
        n:`CONFIG_LLEXT_HEAP_MEMBLK_BLOCK_SIZE` 的整数倍。
        若选中 :kconfig:option:`CONFIG_HARVARD`，则由 :kc
        onfig:option:`CONFIG_LLEXT_INSTR_HEAP_SIZE`
         和 :kconfig:option:`CONFIG_LLEXT_DATA_HEAP_SIZE` 取代本选项。

:kconfig:option:`CONFIG_LLEXT_METADATA_HEAP_SIZE`

        可供 LLEXT 元数据使用的堆大小，单位为千字节。

另一个选项控制块大小。

:kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK_BLOCK_SIZE`

        LLEXT :c:type:`sys_mem_blocks_t` 堆的块大小，单位为字节。若启用
         MMU 或 MPU，块大小必须等于 ``LLEXT_PAGE_SIZE`` 或为其整数倍。
        块大小还必须等于任意扩展区域所需最大对齐值或其整数倍。若选中 :kconfig:option:`C
        ONFIG_MPU_REQUIRES_POWER_OF_TWO_ALIGNMENT` 且区域较大，
        可能需要一个过大的块大小才能满足对齐要求。

堆放置
--------------

LLEXT 堆具有自定义段。非哈佛堆段（``.llext_heap``，或若选中 
:kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK`
 则为 ``.llext_metadata_heap`` 和 ``.llext_ext_heap``）
 与 ``.noinit``
  段一起放置在文件 :file:`include/zephyr/linker/common-noinit.ld` 中。如果你的链接脚本均未包含此文件，则需要手动放置非哈佛
   LLEXT 堆段。一种做法是在你的 ``.noinit`` 段之后，在链接脚本中包含 :file:`snippets-noinit.ld`。

.. code-block:: none

   /* Located in generated directory.
    This file is populated by the
    * zephyr_linker_sources() CMake function.
    */
   #include <snippets-noinit.ld>

在你的板级、SoC 或架构 :file:`CMakeFiles.txt` 中将该文件添加为链接器源文件。

.. code-block:: cmake

   zephyr_linker_sources(NOINIT snippets-noinit.ld)

然后在与你的 :file:`CMakeFiles.txt` 相同目录中创建一个名为
 :file:`noinit.ld` 的文件。

.. code-block:: none

   #if defined(CONFIG_LLEXT) && !define
   d(CONFIG_LLEXT_CUSTOM_HEAP_PLACEMENT)
   *(.llext_heap)
   *(.llext_ext_heap)
   *(.llext_metadata_heap)
   #endif /* CONFIG_LLEXT && !CONFI
   G_LLEXT_CUSTOM_HEAP_PLACEMENT */

对于 ARC，哈佛指令和数据堆段（``.llext_instr_heap``
 与 ``.llext_data_heap``）
在架构层面被放置在指令存储器和数据存储器中。如果你使用的是一块采用哈佛架构的非 ARC 板级，则需要手动放置
 ``.llext_instr_heap`` 和 ``.llext_data_heap``。

.. warning::

   如果指令存储器中的 ``.llext_instr_heap`` 在加载并链接扩展时不可写，LLEXT 将无法加载扩展。

也可以通过提供自定义链接脚本指定放置位置。

:kconfig:option:`CONFIG_CUSTOM_LINKER_SCRIPT`

        要用于替代板级所定义链接脚本的链接脚本路径。

        链接脚本必须基于 Zephyr 提供的版本，因为内核可能预期某种特定的布局/特定区域。

        当应用需要向链接脚本添加段、又不想修改 Zephyr 提供的脚本时，这很有用。

使用自定义链接脚本时，你可能需要覆盖默认放置位置。例如，你可能希望在链接脚本中包含 :f
ile:`include/zephyr/linker/common-noinit.ld`，
但将堆段放置到其他位置。要做到这一点，请选中以下选项。

:kconfig:option:`CONFIG_LLEXT_CUSTOM_HEAP_PLACEMENT`

        移除链接脚本中 LLEXT 堆段的默认放置位置，由用户自行放置堆。

字粒度访问指令存储器堆
--------------------------------------------

字粒度访问指令存储器是一种按字节寻址、但只能通过字大小且对齐的加载和存储指令访问的指令存储器。
LLEXT 子系统目前仅支持在 Xtensa 架构上将指令堆放置在字粒度访问指令存储器中。
对非 Xtensa 架构的支持将在未来按需添加。

要将 LLEXT 的指令堆放置在字粒度访问指令存储器中，你的 Xtensa SoC 或板级除
 :kconfig:option:`CONFIG_HARVARD` 外还必须选中以下选项。

:kconfig:option:`CONFIG_ARCH_HAS
_WORD_GRANULAR_ACCESS_INSTR_MEM`

        此选项启用对按字节寻址且字粒度访问的指令存储器的访问支持。

如果堆使用默认底层数据结构 :c:struct:`k_heap`，请启用以下选项。

:kconfig:option:`CONFIG_SYS_HEAP_BIG_ONLY`

        选中此项可将代码优化为仅适用于大堆。它可以适配任意堆大小，但在小堆下内存使用效率不会那么高。

如果未选中此选项，在指令堆初始化期间将对指令存储器执行非对齐和窄访问。

接下来，按照上文堆放置的说明，将 LLEXT 指令堆放置到该指令存储器中。确保你的
 SoC 或板级除 :c:func:`arch_is_instr_mem`
 外还实现了 :c:func:`arch_memcpy_to_instr`
  和 :c:func:`arch_memcpy_from_instr`。
 字粒度访问库中的 :c:func:`memcpy_to_word_granular` 和 
 :c:func:`memcpy_from_word_granular` 函数可能会有所帮助。

你可以将 ELF 缓冲区放在 RAM 中。加载时，LLEXT 子系统会强制将文本区域放到指令堆上（
即使 ELF 缓冲区可写）使其可执行，并在加载和链接期间访问文本区域时遵守字粒度访问约束。

.. warning::

   当指令堆位于字粒度访问指令存储器中时，只能使用缓冲区加载器（:c:
   struct:`llext_buf_loader`）来加载 ELF。

注意扩展本身负责确保其后对指令存储器的任何访问也遵守这些约束。

如果你仍然遇到加载/存储异常，可以使用以下选项为 Xtensa 启用无符号加载/存储异常处理程序。

:kconfig:option:`CONFIG_XTENSA_EMUL
ATE_UNSUPPORTED_UNSIGNED_LOAD_STORE`

        当无符号加载/存储指令触发不受支持的加载/存储异常时，异常处理程序将自行
        使用受支持的字大小且对齐的加载/存储指令执行该操作。目前不支持 VLIW。

如选项描述所述，要使用此选项还必须禁用 VLIW，因为启用 VLIW 会使编译器生成有符号加载/存储指令。

:kconfig:option:`CONFIG_COMPILER_CODEGEN_VLIW_DISABLED`

        明确指示编译器绝不生成 VLIW 指令。

.. _llext_kconfig_type:

ELF 对象类型
-------------------

LLEXT 子系统支持加载不同类型的扩展；类型可以通过选择以下 Kconfig 选项来设置：

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_OBJECT`

        将 LLEXT 子系统的二进制对象类型构建并期望为可重定位文件。使用单次编译器调用生成对象文件。

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_RELOCATABLE`

        将 LLEXT 子系统的二进制对象类型构建并期望为可重定位（部分链接）
        文件。这些对象文件由链接器将多个对象文件合并为一个而生成。

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_SHAREDLIB`

        将 LLEXT 子系统的二进制对象类型构建并期望为共享库。使用标准链接流程从多个对象文件生成共享库。

        .. note::

           目前 ARM 架构不支持此项。

.. _llext_kconfig_storage:

最小化分配
--------------------

LLEXT 子系统的加载机制默认使用 seek/read 抽象，并将所有数据复制到已分配的内存中；
这样做是为了让扩展可以从任意存储介质加载。
但有时数据已经位于 RAM 中的缓冲区里，无需复制。以下选项允许 LLEXT 子系统在这种情况下优化内存占用。

:kconfig:option:`CONFIG_LLEXT_STORAGE_WRITABLE`

        允许通过直接引用 ELF 缓冲区中的段数据来加载扩展。要使其生效，需要使用支持 ``peek``
         功能的 ELF 加载器，例如 :c:struct:`llext_buf_loader`。

        .. warning::

           应用程序必须确保用于加载扩展的缓冲区在扩展卸载之前始终保持分配状态。

        .. note::

           这会在链接阶段直接修改缓冲区的内容。扩展卸载后，缓冲区必须重新加载，
           才能再次在调用 :c:func:`llext_load` 时使用。

.. _llext_symbol_groups:

符号组
-------------

所有 LLEXT 符号都属于某个组，每个组是否包含在导出的符号表中由对应的
 Kconfig 符号控制。将符号作为某个组的一部分导出，
使用 :c:macro:`EXPORT_GROUP_SYMBOL` 和 :c
:macro:`EXPORT_GROUP_SYMBOL_NAMED` 宏完成。
例如，以下代码将符号 ``memcpy`` 作为 ``LIBC`` 组的一部分导出：

.. code:: c

   EXPORT_GROUP_SYMBOL(LIBC, memcpy);

组名可以任意，但必须全部为大写字母。对于 C 代码中使用的每个组，
**必须**存在一个形式如下的对应 Kconfig 符号：

.. code::

   config LLEXT_EXPORT_SYMBOL_GROUP_{GROUP_NAME}
      bool "Export all symbols from the {GROUP_NAME} group"

符号的默认组（使用 :c:macro:`EXPORT_SYMBOL` 或 
:c:macro:`EXPORT_SYMBOL_NAMED` 声明的符号）
是 ``UNASSIGNED`` 组。按照上述规则，该组的包含由 :kconfig:option:
`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_UNASSIGNED` 控制。

Zephyr 目前定义的组为：

.. csv-table:: Zephyr LLEXT 符号组
  :header: 组名, Kconfig 符号, 描述

  ``UNASSIGNED``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_UNASSIGNED`, 未显式指定组的符号
  ``SYSCALL``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_SYSCALL`, Zephyr 内核系统调用
  ``LIBC``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_LIBC`, C 标准库函数（:c:func:`memcpy` 等）
  ``DEVICE``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_DEVICE`, 设备树设备

.. _llext_kconfig_slid:

使用 SLID 进行符号查找
-----------------------------

加载扩展时，LLEXT 子系统必须找到扩展所引用的、位于主应用中的所有符号的地址。
为此，主二进制文件包含一个 LLEXT 专用符号表，
主应用导出给扩展的每个符号对应一条符号名到地址的映射条目。扩展加载时，
LLEXT 链接器即可在该表中进行搜索。由于字符串比较的特性，
这一过程相当缓慢，且随着导出符号数量的增加，该表占用的空间可能变得可观。

:kconfig:option:`CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID`

        对 Zephyr 二进制文件以及正在构建的所有扩展执行额外的处理步骤，
        将符号表中的每个字符串转换为一个指针大小的哈希，称为符号链接标识符（
        Symbol Link Identifier，SLID），并存储在二进制文件中。

        这使得符号查找过程得以加速，因为可以使用基于整数的比较而非基于字符串的比较。基于 SLID
         的链接还有一个好处：不再需要在二进制文件中存储符号名，从而使符号表大小显著减小。

        .. note::

           此选项目前与 :ref:`LLEXT EDK <llext_build_edk>` 不兼容。

        .. note::

           不支持在主二进制文件和扩展中使用不同的选项值。例如，如果主应用以 ``CONF
           IG_LLEXT_EXPORT_BUILTINS_BY_SLID=y`` 构建，
           则禁止加载以 ``CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID=n`` 编译的扩展。

EDK 配置
-----------------

影响 LLEXT EDK 生成与行为的选项在 :ref:`llext_kconfig_edk` 中有描述。
