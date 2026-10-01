.. _llext:

可链接可加载扩展（LLEXT）
####################################

LLEXT 子系统提供了一套工具箱，用于在运行时通过可链接可加载代码扩展应用的功能。

扩展是以 ELF 格式预编译的可执行文件，可以经过校验、加载，并与主 Zephyr 二进制文件链接。扩展可以在一定程度上被操作和检查，不再需要时也可以卸载。

.. toctree::
   :maxdepth: 1

   config
   build
   load
   debug
   api

.. note::

   LLEXT 子系统需要架构特定的支持。目前仅在 RISC-V、ARM、ARM64、ARC、x86 和 Xtensa 内核上可用。
