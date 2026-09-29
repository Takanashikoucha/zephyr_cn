.. _llext:

Linkable
Loadable
Extensions
（LLEXT）
####################################

LLEXT
subsystem
provide
一
个
toolbox
用于
在
runtime
用
linkable
loadable
的
code
extend
application
的
functionality。

Extensions
是
precompiled
的
executables
在
ELF
format
中
它们
可以
被
verified、
loaded、
和
与
main
Zephyr
binary
linked。
Extensions
可以
被
manipulated
和
introspected
到
certain
程度
并
在
不再
需要
时
被
unloaded。

.. toctree::
   :maxdepth:
   1

   config
   build
   load
   debug
   api

.. note::

   LLEXT
   subsystem
   require
   architecture
   specific
   的
   support。
   它
   当前
   只
   在
   RISC
   V、
   ARM、
   ARM64、
   ARC、
   x86、
   和
   Xtensa
   cores
   上
   available。
