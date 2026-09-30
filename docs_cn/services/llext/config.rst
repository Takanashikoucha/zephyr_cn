Configuration
#############

以下
Kconfig
options
对
LLEXT
subsystem
available。

.. _llext_kconfig_heap:

Harvard
architecture
--------------------

:kconfig:option:`CONFIG_HARVARD`

        Architecture
        use
        separate
        的
        instruction
        和
        data
        memory。

:kconfig:option:`CONFIG_HARVARD`
不
是
LLEXT
subsystem
defined
的
Kconfig。
相反
它
必须
由
board
或
SoC
defined
并
selected
用于
signal
LLEXT
应该
被
build
带
Harvard
architecture
support。
Board
或
SoC
必须
也
implement
:c:func:`arch_is_instr_mem`。

Heap
size
----------

LLEXT
subsystem
需要
一
个
heap
被
allocated
用于
extension
related
的
data。
以下
option
control
这
个
allocation
当
allocating
一
个
static
heap
时。

:kconfig:option:`CONFIG_LLEXT_HEAP_SIZE`

        LLEXT
        heap
        的
        size
        以
        kilobytes
        计。

对
use
Harvard
architecture
的
boards
LLEXT
heap
被
split
到
两
个：
一
个
在
instruction
memory
中
另
一
个
在
data
memory
中。
以下
options
control
这些
allocations。

:kconfig:option:`CONFIG_LLEXT_INSTR_HEAP_SIZE`

        LLEXT
        heap
        在
        instruction
        memory
        中
        的
        size
        以
        kilobytes
        计。

:kconfig:option:`CONFIG_LLEXT_DATA_HEAP_SIZE`

        LLEXT
        heap
        在
        data
        memory
        中
        的
        size
        以
        kilobytes
        计。


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
--------------------------------------------

Word granular access instruction memory is a type of
instruction memory that is byte addressable, but can only be accessed
with word-sized and aligned loads and stores. The LLEXT subsystem
currently supports the placement of the instruction heap in
word granular access instruction memory on the Xtensa architecture
only. Support for non-Xtensa architectures will be added in the
future on request.

To use LLEXT with the instruction heap in word granular access
instruction memory, your Xtensa SoC or board must select the
following option in addition to :kconfig:option:`CONFIG_HARVARD`.

:kconfig:option:`CONFIG_ARCH_HAS_WORD_GRANULAR_ACCESS_INSTR_MEM`

        This option enables support for access to byte addressable and
        word granular access instruction memory.

If using the default backing data structure for the heap,
:c:struct:`k_heap`, enable the following option.

:kconfig:option:`CONFIG_SYS_HEAP_BIG_ONLY`

        Select this to optimize the code for big heaps only. This can
        accommodate any heap size but memory usage won't be as
        efficient with small sized heaps.

Unaligned and narrow accesses to instruction memory will be performed
during the instruction heap initialization if this option is not selected.

Next, place the LLEXT instruction heap in that instruction memory
following the instructions for heap placement above. Make sure your SoC or
board implements :c:func:`arch_memcpy_to_instr` and
:c:func:`arch_memcpy_from_instr` in addition to :c:func:`arch_is_instr_mem`.
The word granular access library :c:func:`memcpy_to_word_granular` and
:c:func:`memcpy_from_word_granular` functions may be helpful.

You may place your ELF buffer in RAM. At load time, the LLEXT subsystem will
force the text region onto the instruction heap (even when the ELF buffer
is writable) so that it is executable, and respect word granular access
constraints when accessing the text region during loading and linking.

.. warning::

   You may only use the buffer loader (:c:struct:`llext_buf_loader`) to
   load the ELF when the instruction heap is in word granular access
   instruction memory.

Note that the extension itself is responsible for ensuring any subsequent
accesses to instruction memory also respect these constraints.

If you still encounter load / store exceptions, you can enable the
unsigned load / store exception handler for Xtensa with the following option.

:kconfig:option:`CONFIG_XTENSA_EMULATE_UNSUPPORTED_UNSIGNED_LOAD_STORE`

        When an unsigned load / store instruction triggers an unsupported
        load / store exception, the exception handler will perform the
        operation itself with supported word sized and aligned loads /
        stores. Does not currently support VLIW.

As mentioned in the option description, to use this option you must also disable
VLIW, as enabling VLIW causes the compiler to generate signed load / store
instructions.

:kconfig:option:`CONFIG_COMPILER_CODEGEN_VLIW_DISABLED`

        Explicitly instructs the compiler to NEVER generate VLIW instructions.

.. _llext_kconfig_type:

ELF object type
---------------

The LLEXT subsystem supports loading different types of extensions; the type
can be set by choosing among the following Kconfig options:

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_OBJECT`

        Build and expect relocatable files as binary object type for the LLEXT
        subsystem. A single compiler invocation is used to generate the object
        file.

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_RELOCATABLE`

        Build and expect relocatable (partially linked) files as the binary
        object type for the LLEXT subsystem. These object files are generated
        by the linker by combining multiple object files into a single one.

:kconfig:option:`CONFIG_LLEXT_TYPE_ELF_SHAREDLIB`

        Build and expect shared libraries as binary object type for the LLEXT
        subsystem. The standard linking process is used to generate the shared
        library from multiple object files.

        .. note::

           This is not currently supported on ARM architectures.

.. _llext_kconfig_storage:

Minimize allocations
--------------------

The LLEXT subsystem loading mechanism, by default, uses a seek/read abstraction
and copies all data into allocated memory; this is done to allow the extension
to be loaded from any storage medium. Sometimes, however, data is already in a
buffer in RAM and copying it is not necessary. The following option allows the
LLEXT subsystem to optimize memory footprint in this case.

:kconfig:option:`CONFIG_LLEXT_STORAGE_WRITABLE`

        Allow the extension to be loaded by directly referencing section data
        into the ELF buffer. To be effective, this requires the use of an ELF
        loader that supports the ``peek`` functionality, such as the
        :c:struct:`llext_buf_loader`.

        .. warning::

           The application must ensure that the buffer used to load the
           extension remains allocated until the extension is unloaded.

        .. note::

           This will directly modify the contents of the buffer during the link
           phase. Once the extension is unloaded, the buffer must be reloaded
           before it can be used again in a call to :c:func:`llext_load`.

.. _llext_symbol_groups:

Symbol Groups
-------------

All LLEXT symbols belong to a group, with the inclusion of each group in the
exported symbol table controlled by a corresponding Kconfig symbol. Exporting
a symbol as part of a group is done with the :c:macro:`EXPORT_GROUP_SYMBOL`
and :c:macro:`EXPORT_GROUP_SYMBOL_NAMED` macros. For example the following
exports the symbol ``memcpy`` as part of the ``LIBC`` group:

.. code:: c

   EXPORT_GROUP_SYMBOL(LIBC, memcpy);

Group names are arbitrary, but they must be all uppercase. For each group
used in C code, there **MUST** be a corresponding Kconfig symbol of the form:

.. code::

   config LLEXT_EXPORT_SYMBOL_GROUP_{GROUP_NAME}
      bool "Export all symbols from the {GROUP_NAME} group"

The default group for symbols (those declared with :c:macro:`EXPORT_SYMBOL`
or :c:macro:`EXPORT_SYMBOL_NAMED`) is the ``UNASSIGNED`` group. As per the
above rules, the inclusion of this group is controlled by
:kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_UNASSIGNED`.

The groups currently defined by Zephyr are:

.. csv-table:: Zephyr LLEXT symbol groups
  :header: Group Name, Kconfig Symbol, Description

  ``UNASSIGNED``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_UNASSIGNED`, Symbols without an explicit group
  ``SYSCALL``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_SYSCALL`, Zephyr kernel system calls
  ``LIBC``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_LIBC`, C standard library functions (:c:func:`memcpy` etc)
  ``DEVICE``, :kconfig:option:`CONFIG_LLEXT_EXPORT_SYMBOL_GROUP_DEVICE`, Devicetree devices

.. _llext_kconfig_slid:

Using SLID for symbol lookups
-----------------------------

When an extension is loaded, the LLEXT subsystem must find the address of all
the symbols residing in the main application that the extension references.
To this end, the main binary contains a LLEXT-dedicated symbol table, filled
with one symbol-name-to-address mapping entry for each symbol exported by the
main application to extensions. This table can then be searched into by the
LLEXT linker at extension load time. This process is pretty slow due to the
nature of string comparisons, and the size consumed by the table can become
significant as the number of exported symbols increases.

:kconfig:option:`CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID`

        Perform an extra processing step on the Zephyr binary and on all
        extensions being built, converting every string in the symbol tables to
        a pointer-sized hash called Symbol Link Identifier (SLID), which is
        stored in the binary.

        This speeds up the symbol lookup process by allowing usage of
        integer-based comparisons rather than string-based ones. Another
        benefit of SLID-based linking is that storing symbol names in the
        binary is no longer necessary, which provides a significant decrease in
        symbol table size.

        .. note::

           This option is not currently compatible with the :ref:`LLEXT EDK
           <llext_build_edk>`.

        .. note::

           Using a different value for this option in the main binary and in
           extensions is not supported. For example, if the main application
           is built with ``CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID=y``, it is
           forbidden to load an extension that was compiled with
           ``CONFIG_LLEXT_EXPORT_BUILTINS_BY_SLID=n``.

EDK configuration
-----------------

Options influencing the generation and behavior of the LLEXT EDK are described
in :ref:`llext_kconfig_edk`.