.. _slist_api:

单链表
==================

Zephyr 提供了一个 :c:type:`sys_slist_t` 类型，用于存储简单的
单链表数据（即每个列表元素只存储
指向下一个元素的指针，而不存储前一个元素的指针）。
它支持对列表第一个（头）和最后一个（尾）元素的
常数时间访问、在列表头之前和尾之后插入，
以及对头的常数时间删除。删除后续节点
需要访问"前一个"指针，因此
只能通过搜索列表以线性时间完成。

:c:type:`sys_slist_t` 结构体可以由用户在任何
可访问内存中实例化。
它应在使用前用 :c:func:`sys_slist_init` 或
SYS_SLIST_STATIC_INIT 静态赋值初始化。
其内部字段是不透明的，不应被
用户代码访问。

可以用
:c:func:`sys_slist_peek_head` 和 :c:func:`sys_slist_peek_tail`
获取列表的端点节点，
如果列表为空则返回 NULL，
否则返回指向
:c:type:`sys_snode_t` 结构体的指针。

:c:type:`sys_snode_t` 结构体代表要插入的数据。
通常，它由用户分配/控制，
一般嵌入在要添加到列表的结构体中。
可以用 :c:macro:`SYS_SLIST_CONTAINER`
从列表节点获取容器结构体指针，
传入包含结构体的结构体名和节点字段名。
内部地，:c:type:`sys_snode_t` 结构体
只包含一个 next 指针，
可以用 :c:func:`sys_slist_peek_next` 访问。

可以用 :c:func:`sys_slist_prepend` 和
:c:func:`sys_slist_append` 在头或尾添加单个节点
来修改列表。也可以用
:c:func:`sys_slist_insert` 在内部点添加节点，
它在现有节点之后插入一个新节点。
类似地，:c:func:`sys_slist_remove`
在给定其前驱指针的情况下删除一个节点。
所有这些操作都是常数时间的。

针对列表更复杂的修改存在
便捷例程。:c:func:`sys_slist_merge_slist`
将整个列表追加到现有列表之后。
:c:func:`sys_slist_append_list`
以常数时间追加现有列表的有界子集。
:c:func:`sys_slist_find_and_remove`
搜索列表（线性时间）查找给定节点，
如果存在则删除它。

最后，slist 实现提供了一组"for each"宏，
允许以自然方式遍历列表，而无需
手动遍历 next 指针。:c:macro:`SYS_SLIST_FOR_EACH_NODE`
给定一个存储节点指针的局部变量，
将枚举列表中的每个节点。
:c:macro:`SYS_SLIST_FOR_EACH_NODE_SAFE`
行为类似，但实现更复杂，
需要一个额外的临时变量存储，
并允许用户在迭代期间删除
正在迭代的节点。每个宏还有
"container"变体（:c:macro:`SYS_SLIST_FOR_EACH_CONTAINER` 和
:c:macro:`SYS_SLIST_FOR_EACH_CONTAINER_SAFE`），
它分配一个与用户容器结构体类型匹配的
局部变量（而非节点结构体类型），
在内部执行所需的偏移。
:c:macro:`SYS_SLIST_ITERATE_FROM_NODE`
则允许只枚举某个节点及其所有后继，
而不检查列表的前半部分。

单链表内部实现
----------------------------

slist 代码被设计得极简且符合惯例。
内部地，:c:type:`sys_slist_t` 结构体
不过是一对 "head" 和 "tail" 指针字段。
而 :c:type:`sys_snode_t` 只存储
单个 "next" 指针。

.. figure:: slist.png
    :align: center
    :alt: slist 示例
    :figclass: align-center

    一个包含三个元素的 slist。

.. figure:: slist-empty.png
    :align: center
    :alt: 空 slist 示例
    :figclass: align-center

    一个空的 slist

然而，列表代码的具体实现
是通过内部的 "Z_GENLIST" 模板 API 完成的，
它允许从任意结构体中提取
这些字段，并发射任意命名的
一组函数。这使得可以使用相同的基础原语
实现更复杂的单链表变体。
genlist 实现者只需负责原语操作的
自定义实现：每个结构体的 "init" 步骤，
以及 head、tail 和 next 指针在
其相关结构体上的 "get" 和 "set" 原语。
这些内联函数作为参数传递给
genlist 宏展开。

目前 Zephyr 中只存在这样一个变体：sflist。


带标志的列表
------------

:c:type:`sys_sflist_t` 使用上述 genlist
模板 API 实现。除符号命名（"sflist" 而非
"slist"）和下面描述的附加 API 外，
它在所有方面都与 slist API 行为相同。

它增加了为每个列表节点关联恰好
两位用户定义的"标志"的能力。
可以用 :c:func:`sys_sfnode_flags_get` 和
:c:func:`sys_sfnode_flags_set`
访问和修改这些标志。
内部地，标志与 next 指针的
低位以联合体方式存储，与更简单的
slist 代码相比不产生任何 SRAM 存储开销。


单链表 API 参考
--------------------------------

.. doxygengroup:: single-linked-list_apis

带标志的列表 API 参考
--------------------------------

.. doxygengroup:: flagged-single-linked-list_apis
