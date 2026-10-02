.. _symtab:

符号表（Symbol Table，Symtab）
#####################

Symtab 模块启用时，将在 Zephyr 链接（linking）
阶段生成完整的符号表（symbol table），用于跟踪函数的名称和地址信息；对于
函数数量众多的复杂应用，预计将消耗相当可观的 ROM 空间。

目前，该模块用于在受支持的架构（architecture）中，在栈回溯（stack trace）期间查找
函数名称。


用法
*****

应用程序可以通过包含 :file:`symtab.h` 头
文件并调用 :c:func:`symtab_get 来访问符号表数据结构。目前，我们仅提供 :c:func:`symtab_find_symbol_name`
函数来查找地址对应的符号名称和偏移量。更高级的功能可
通过直接访问数据结构的成员来实现。

配置
*************

使用以下选项配置该模块。

* :kconfig:option:`CONFIG_SYMTAB`：启用符号表的生成。

API 文档
*****************

.. doxygengroup:: symtab_apis
