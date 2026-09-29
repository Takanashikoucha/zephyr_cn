.. _posix_conformance:

POSIX
Conformance
#################

根据
`IEEE
1003.1
2017`_
这
个
section
detail
Zephyr
的
POSIX
conformance。

.. _IEEE
   1003.1
   2017:
   https://standards.ieee.org/ieee/1003.1/7101/

.. _posix_system_interfaces:

POSIX
System
Interfaces
======================

..
   以下
   在
   Zephyr
   中
   有
   大于
   1
   的
   values
   与
   POSIX
   specification
   conformant。

..
   csv-table::
   POSIX
   System
   Interfaces
   :header:
   Symbol,
   Support,
   Remarks
   :widths:
   50,
   10,
   50

   _POSIX_CHOWN_RESTRICTED,
   0,
   _POSIX_NO_TRUNC,
   0,
   _POSIX_VDISABLE,
   ``'\0'``,

..
   TODO:
   POSIX_ASYNCHRONOUS_IO
   和
   下面
   的
   其他
   interfaces
   是
   mandatory
   的。
   这
   means
   严格
   conforming
   的
   application
   不
   需要
   被
   modified
   才能
   compile
   到
   Zephyr。
   然而
   我们
   可能
   add
   implementations
   它们
   simply
   fail
   with
   ENOSYS
   只要
   functional
   modification
   被
   clearly
   documented。
   该
   implementation
   对
   PSE51
   或
   PSE52
   不
   是
   required
   且
   超出
   那
   个
   POSIX
   async
   I/O
   functions
   在
   practice
   中
   rarely
   被
   used。

.. _posix_system_interfaces_required:

..
   csv-table::
   POSIX
   System
   Interfaces
   :header:
   Symbol,
   Support,
   Remarks
   :widths:
   50,
   10,
   50

   _POSIX_VERSION,
   200809L,
   :ref:`_POSIX_ASYNCHRONOUS_IO<posix_option_asynchronous_io>`,
   200809L,
   :kconfig:option:`CONFIG_POSIX_ASYNCHRONOUS_IO`:ref:`†<posix_undefined_behaviour>`
   :ref:`_POSIX_BARRIERS<posix_option_group_barriers>`,
   200809L,
   :kconfig:option:`CONFIG_POSIX_BARRIERS`
   :ref:`_POSIX_CLOCK_SELECTION<posix_option_group_clock_selection>`,
   200809L,
   :kconfig:option:`CONFIG_POSIX_CLOCK_SELECTION`
