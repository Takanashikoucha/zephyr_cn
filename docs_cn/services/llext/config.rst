Configuration
#############

LLEXT 子系统提供以下 Kconfig 选项。

.. _llext_kconfig_heap:

Harvard
architecture
--------------------

:kconfig:option:`CONFIG_HARVARD`

        该架构使用相互独立的指令存储器和数据存储器。

:kconfig:option:`CONFIG_HARVARD` 不是 LLEXT 子系统定义的 Kconfig 选项。相反，它必须由板级或 SoC 定义并选中，以表明 LLEXT 应构建为支持哈佛架构。板级或 SoC 还必须实现 :c:func:`arch_is_instr_mem`。

Heap
size
----------

LLEXT 子系统需要为扩展相关数据分配一块堆。当分配静态堆时，以下选项控制这一分配。

:kconfig:option:`CONFIG_LLEXT_HEAP_SIZE`

        LLEXT 堆的大小，单位为千字节。

对于使用哈佛架构的板级，LLEXT 堆被拆分为两个：一个位于指令存储器中，另一个位于数据存储器中。以下选项控制这些分配。

:kconfig:option:`CONFIG_LLEXT_INSTR_HEAP_SIZE`

        指令存储器中 LLEXT 堆的大小，单位为千字节。

:kconfig:option:`CONFIG_LLEXT_DATA_HEAP_SIZE`

        数据存储器中 LLEXT 堆的大小，单位为千字节。

或者，应用可以使用以下选项配置动态堆。

:kconfig:option:`CONFIG_LLEXT_HEAP_DYNAMIC`

        某些应用需要将扩展加载到启动时不存在、无法静态分配的内存中。让应用负责 LLEXT 堆的分配。不要静态分配 LLEXT 堆。

        应用必须调用 :c:func:`llext_heap_init` 来指定用作 LLEXT 堆的缓冲区，否则 LLEXT 模块将无法加载。当应用不再需要 LLEXT 功能时，应调用 :c:func:`llext_heap_uninit`，它将缓冲区控制权释放回应用。

.. note::

   启用 :ref:`user mode <usermode_api>` 时，堆大小必须足够大，以允许扩展 section 按照架构所需的对齐方式进行分配。

.. note::

   在哈佛架构上，应用必须调用 :c:func:`llext_heap_init_harvard`。

LLEXT 堆的底层数据结构默认是 :c:struct:`k_heap`，但对于无元数据（即扩展 region），可以通过为 :kconfig:option:`CONFIG_LLEXT_HEAP_MANAGEMENT` 选择 :kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK` 将其更改为 :c:type:`sys_mem_blocks_t`。

:kconfig:option:`CONFIG_LLEXT_HEAP_MANAGEMENT`

        选择用于在 LLEXT 堆内存中存储扩展 region 的内存管理 API。此选择不影响 LLEXT 元数据，元数据始终由 :c:struct:`k_heap` 管理。

:kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK`

        使用 :c:type:`sys_mem_blocks_t` API 管理扩展 region 的 LLEXT 堆内存。每个 region 至少分配一个块。块大小必须仔细选择，以确保扩展 region 的正确对齐。

.. note::

   :kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK` 不支持 :kconfig:option:`CONFIG_LLEXT_HEAP_DYNAMIC`。

堆将被拆分为两个，每个子堆的大小由以下选项控制。

:kconfig:option:`CONFIG_LLEXT_EXT_HEAP_SIZE`

        可供 LLEXT 扩展 section 使用的堆大小，单位为千字节。必须是 :kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK_BLOCK_SIZE` 的倍数。如果选中了 :kconfig:option:`CONFIG_HARVARD`，则被 :kconfig:option:`CONFIG_LLEXT_INSTR_HEAP_SIZE` 和 :kconfig:option:`CONFIG_LLEXT_DATA_HEAP_SIZE` 取代。

:kconfig:option:`CONFIG_LLEXT_METADATA_HEAP_SIZE`

        可供 LLEXT 元数据使用的堆大小，单位为千字节。

另一个选项控制块大小。

:kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK_BLOCK_SIZE`

        LLEXT :c:type:`sys_mem_blocks_t` 堆的块大小，单位为字节。如果启用了 MMU 或 MPU，必须等于 ``LLEXT_PAGE_SIZE`` 或为其倍数。块大小还必须等于任何扩展 region 所需最大对齐值或为其倍数。如果选中了 :kconfig:option:`CONFIG_MPU_REQUIRES_POWER_OF_TWO_ALIGNMENT` 且 region 较大，可能需要不合理的块大小才能满足对齐要求。

Heap
placement
----------------

LLEXT 堆具有自定义 section。非哈佛堆 section（``.llext_heap``，或如果选中 :kconfig:option:`CONFIG_LLEXT_HEAP_MEMBLK` 则为 ``.llext_metadata_heap`` 和 ``.llext_ext_heap``）与 ``.noinit`` section 一起放置在文件 :file:`include/zephyr/linker/common-noinit.ld` 中。如果你的链接脚本都没有包含此文件，则需要手动放置非哈佛 LLEXT 堆 section。一种方法是在 ``.noinit`` section 之后将 :file:`snippets-noinit.ld` 包含到你的链接脚本中。

.. code-block:: none

   /* Located in generated directory. This file is populated by the
    * zephyr_linker_sources() CMake function.
    */
   #include <snippets-noinit.ld>

在你的板级、SoC 或架构 :file:`CMakeFiles.txt` 中将该文件添加为链接器源。

.. code-block:: cmake

   zephyr_linker_sources(NOINIT snippets-noinit.ld)

然后在与 :file:`CMakeFiles.txt` 相同的目录下创建一个名为 :file:`noinit.ld` 的文件。

.. code-block:: none

   #if defined(CONFIG_LLEXT) && !defined(CONFIG_LLEXT_CUSTOM_HEAP_PLACEMENT)
   *(.llext_heap)
   *(.llext_ext_heap)
   *(.llext_metadata_heap)
   #endif /* CONFIG_LLEXT && !CONFIG_LLEXT_CUSTOM_HEAP_PLACEMENT */

对于 ARC，哈佛指令和数据堆 section（``.llext_instr_heap`` 和 ``.llext_data_heap``）在架构层面放置在指令存储器和数据存储器中。如果你使用的是采用哈佛架构的非 ARC 板级，则需要手动放置 ``.llext_instr_heap`` 和 ``.llext_data_heap``。

.. warning::

   如果加载和链接扩展时，放置 ``.llext_instr_heap`` 的指令存储器不可写，LLEXT 将无法加载扩展。

也可以通过提供自定义链接脚本来指定放置位置。

:kconfig:option:`CONFIG_CUSTOM_LINKER_SCRIPT`

        要使用的链接脚本路径，用于替代板级定义的链接脚本。

        链接脚本必须基于 Zephyr 提供的版本，因为内核可以预期特定的布局/特定 region。

        当应用需要在链接脚本中添加 section 而不必修改 Zephyr 提供的脚本时，这很有用。

使用自定义链接脚本时，你可能需要覆盖默认放置位置。例如，你可能希望将 :file:`include/zephyr/linker/common-noinit.ld` 包含到你的链接脚本中，但将堆 section 放置在其他位置。为此，选择以下选项。

:kconfig:option:`CONFIG_LLEXT_CUSTOM_HEAP_PLACEMENT`

        移除链接脚本中 LLEXT 堆 section 的默认放置位置，允许用户自行放置堆。

Word
granular
access
instruction
memory
heap
--------------------------------------------

Word granular access 指令存储器是一种按字节寻址的指令存储器，但只能使用字大小且对齐的加载和存储操作进行访问。LLEXT 子系统目前仅支持在 Xtensa 架构上将指令堆放置在 word granular access 指令存储器中。对非 Xtensa 架构的支持将在未来根据需求添加。

要将 LLEXT 与位于 word granular access 指令存储器中的指令堆一起使用，你的 Xtensa SoC 或板级除了 :kconfig:option:`CONFIG_HARVARD` 外还必须选择以下选项。

:kconfig:option:`CONFIG_ARCH_HAS_WORD_GRANULAR_ACCESS_INSTR_MEM`

        此选项启用对按字节寻址且 word granular access 指令存储器的访问支持。

如果使用堆的默认底层数据结构 :c:struct:`k_heap`，请启用以下选项。

:kconfig:option:`CONFIG_SYS_HEAP_BIG_ONLY`

        选择此项以针对仅大堆优化代码。这可以容纳任何堆大小，但对于小堆内存使用效率不会那么高。

如果未选择此选项，在指令堆初始化期间将对指令存储器执行非对齐和窄访问。

接下来，按照上述堆放置说明将 LLEXT 指令堆放置到该指令存储器中。确保你的 SoC 或板级除了 :c:func:`arch_is_instr_mem` 外还实现了 :c:func:`arch_memcpy_to_instr` 和 :c:func:`arch_memcpy_from_instr`。Word granular access 库函数 :c:func:`memcpy_to_word_granular` 和 :c:func:`memcpy_from_word_granular` 可能有所帮助。

你可以将 ELF 缓冲区放置在 RAM 中。加载时，LLEXT 子系统会强制将 text region 放到指令堆上（即使 ELF 缓冲区可写），使其可执行，并在加载和链接期间访问 text region 时遵守 word granular access 约束。

.. warning::

   当指令堆位于 word granular access 指令存储器中时，你只能使用缓冲区加载器（:c:struct:`llext_buf_loader`）加载 ELF。

请注意，扩展本身负责确保后续对指令存储器的访问也遵守这些约束。

如果你仍然遇到 load / store 异常，可以使用以下选项为 Xtensa 启用无符号 load / store 异常处理程序。

:kconfig:option:`CONFIG_XTENSA_EMULATE_UNSUPPORTED_UNSIGNED_LOAD_STORE`

        当无符号 load / store 指令触发不支持的 load / store 异常时，异常处理程序将使用受支持的、字大小且对齐的 load / store 自行执行该操作。目前不支持 VLIW。

如选项描述中所述，要使用此选项，你还必须禁用 VLIW，因为启用 VLIW 会导致编译器生成有符号 load / store 指令。

:kconfig:option:`CONFIG_COMPILER_CODEGEN_VLIW_DISABLED`

        明确指示编译器绝不生成 VLIW 指令。

.. _llext_kconfig_type:

ELF
object
type
---------------

LLEXT 子系统支持加载不同类型的扩展；类型可以通过选择以下 Kconfig 选项来设置：

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_OBJECT`

        构建并期望可重定位文件作为 LLEXT 子系统的二进制对象类型。使用单次编译器调用生成对象文件。

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_RELOCATABLE`

        构建并期望可重定位（部分链接）文件作为 LLEXT 子系统的二进制对象类型。这些对象文件由链接器将多个对象文件组合成一个文件生成。

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_SHAREDLIB`

        构建并期望共享库作为 LLEXT 子系统的二进制对象类型。使用标准链接过程从多个对象文件生成共享库。

        .. note::

           目前这在 ARM 架构上不受支持。

.. _llext_kconfig_storage:

Minimize
allocations
--------------------

LLEXT 子系统的加载机制默认使用 seek/read 抽象并将所有数据复制到已分配的内存中；这样做是为了允许扩展从任何存储介质加载。然而，有时数据已经在 RAM 中的缓冲区里，无需复制。以下选项允许 LLEXT 子系统在此情况下优化内存占用。

:kconfig:option:`CONFIG_LLEXT_STORAGE_WRITABLE`

        允许扩展通过直接引用 ELF 缓冲区中的 section 数据来加载。要生效，这需要支持 ``peek`` 功能的 ELF 加载器，例如 :c:struct:`llext_buf_loader`。

        .. warning::

           应用必须确保用于加载扩展的缓冲区在扩展卸载之前保持已分配状态。

        .. note::

           这将在链接阶段直接修改缓冲区的内容。一旦扩展卸载，在再次调用 :c:func:`llext_load` 使用之前必须重新加载缓冲区。

.. _llext_symbol_groups:

Symbol
Groups
-------------

所有 LLEXT 符号都属于一个 group，每个 group 在导出的符号表中的包含由对应的 Kconfig 符号控制。将符号作为 group 的一部分导出是通过 :c:macro:`EXPORT_GROUP_SYMBOL` 和 :c:macro:`EXPORT_GROUP_SYMBOL_NAMED` 宏完成的。例如，以下将符号 ``memcpy`` 作为 ``LIBC`` group 的一部分导出：

.. code:: c

   EXPORT_GROUP_SYMBOL(LIBC, memcpy);

Group 名称是任意的，但必须全部大写。对于 C 代码中使用的每个 group，**必须**有对应的 Kconfig 符号，格式如下：

.. code::

   config LLEXT_EXPORT_SYMBOL_GROUP_{GROUP_NAME}
      bool "Export all symbols from the {GROUP_NAME} group"

符号的默认 group（使用 :c:macro:`EXPORT_SYMBOL` 或 :c:macro:`EXPORT_SYMBOL_NAMED` 声明的符号）是 ``UNASSIGNED`` group。根据上述规则，该 group 的包含由 :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_UNASSIGNED` 控制。

Zephyr 当前定义的 group 如下：

.. csv-table:: Zephyr LLEXT symbol groups
  :header: Group Name, Kconfig Symbol, Description

  ``UNASSIGNED``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_UNASSIGNED`, Symbols without an explicit group
  ``SYSCALL``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_SYSCALL`, Zephyr kernel system calls
  ``LIBC``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_LIBC`, C standard library functions (:c:func:`memcpy` etc)
  ``DEVICE``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_DEVICE`, Devicetree devices

.. _llext_kconfig_slid:

Using
SLID
for
symbol
lookups
-----------------------------

当扩展被加载时，LLEXT 子系统必须找到扩展引用的、位于主应用中的所有符号的地址。为此，主二进制文件包含一个 LLEXT 专用符号表，其中为每个由主应用导出给扩展的符号填充一个符号名到地址的映射条目。然后 LLEXT 链接器可以在扩展加载时搜索该表。由于字符串比较的性质，这个过程相当慢，而且随着导出符号数量的增加，表占用的空间可能变得很大。

:kconfig:option:`CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID`

        对 Zephyr 二进制文件和所有正在构建的扩展执行额外的处理步骤，将符号表中的每个字符串转换为一个指针大小的哈希，称为 Symbol Link Identifier（SLID），存储在二进制文件中。

        这通过使用基于整数的比较而非基于字符串的比较来加速符号查找过程。基于 SLID 链接的另一个好处是不再需要在二进制文件中存储符号名，这使符号表大小显著减小。

        .. note::

           此选项目前与 :ref:`LLEXT EDK <llext_build_edk>` 不兼容。

        .. note::

           在主二进制文件和扩展中使用该选项的不同值不受支持。例如，如果主应用以 ``CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID=y`` 构建，则禁止加载以 ``CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID=n`` 编译的扩展。

EDK
configuration
-----------------

影响 LLEXT EDK 生成和行为的选项在 :ref:`llext_kconfig_edk` 中有描述。
