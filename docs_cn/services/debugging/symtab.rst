.. _symtab:

Symbol Table (Symtab)
#####################

Symtab module 启用时（将在 Zephyr linking
阶段生成完整 symbol table（跟踪 functions 的 name 和 address 信息（对
functions 很多的 advanced application（预期将消耗大量 ROM。

当前（其用于在支持的 architectures 中 stack trace 期间查找
function names。


Usage
*****

Application 可包含 :file:`symtab.h` header
file 并调用 :c:func:`symtab_get 访问 symbol table 数据结构。目前（仅提供 :c:func:`symtab_find_symbol_name`
function 查找 address 的 symbol name 和 offset。更高级 functionalities 可
通过直接访问 data structure 的 members 实现。

Configuration
*************

用以下 options 配置此 module。

* :kconfig:option:`CONFIG_SYMTAB`: 启用 symbol table 的生成。

API documentation
*****************

.. doxygengroup:: symtab_apis
