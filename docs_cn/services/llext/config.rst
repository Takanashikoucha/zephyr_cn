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
