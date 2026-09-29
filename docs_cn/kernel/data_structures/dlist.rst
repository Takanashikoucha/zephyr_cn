.. _dlist_api:

双向链表
==================

双向链表在许多方面与单链表类似，Zephyr 提供了一个双向链表实现。
它对现有的所有 slist 操作提供相同的算法行为，但同时也支持
常数时间的删除和插入（在所有位置：头部或尾部之前或之后，
或任意内部节点处）。为此，链表为每个节点存储两个指针，
因此运行时代码和内存空间需求略高。

用户可以在任何可访问的内存中实例化 :c:type:`sys_dlist_t` 结构体。
它必须在使用前用 :c:func:`sys_dlist_init` 或 :c:macro:`SYS_DLIST_STATIC_INIT` 初始化。
:c:type:`sys_dnode_t` 结构体需要由用户为添加到链表的任何节点提供
（通常嵌入在被跟踪的结构体中，如上所述）。
它必须在使用前在清零的/bss 内存中初始化，或用
:c:func:`sys_dnode_init` 初始化。

基本操作可以用 :c:func:`sys_dlist_peek_head`、
:c:func:`sys_dlist_peek_tail`、:c:func:`sys_dlist_peek_next` 和
:c:func:`sys_dlist_peek_prev` 获取链表头/尾以及节点的 next/prev 指针。
这些函数在适当情况下都可以返回 NULL（即对于空链表，
或位于链表端点的节点）。

dlist 可以用常数时间修改：用 :c:func:`sys_dlist_remove` 删除一个节点，
用 :c:func:`sys_dlist_prepend` 和 :c:func:`sys_dlist_append` 将节点
添加到链表头或尾，或用 :c:func:`sys_dlist_insert`
将节点插入到某个现有节点之前。

与 slist 一样，dlist 中的每个节点都可以使用
:c:macro:`SYS_DLIST_FOR_EACH_NODE` 以自然的代码块风格处理。
该宏还有 "FROM_NODE" 形式，允许从已知起点开始迭代；
一个 "SAFE" 变体，允许在代码块内删除正在检查的节点；
一个 "CONTAINER" 风格，提供指向包含结构体的指针而非原始节点；
以及一个 "CONTAINER_SAFE" 变体，同时具备两种特性。

dlist 提供的便捷工具包括
:c:func:`sys_dlist_insert_at`，它线性搜索链表以找到正确的插入点
（由用户以 C 回调函数指针形式提供），以及
:c:func:`sys_dnode_is_linked`，它会明确返回一个节点当前是否已链接到 dlist
（通过一个相对于正常链表处理零开销的实现）。

双向链表内部实现
----------------------------

内部实现上，dlist 非常精简：:c:type:`sys_dlist_t`
结构体包含 "head" 和 "tail" 指针字段，:c:type:`sys_dnode_t`
包含 "prev" 和 "next" 指针，不存储其他数据。但实际上
两个结构体内部是完全相同的，链表结构体作为节点被插入到链表本身中。
这使得操作具有非常干净的对称性：

* 空链表在链表结构体中指向自身的回指指针，
  可以轻易检测到。

* 可以通过将节点的 prev/next 指针与链表结构体地址比较
  来检测链表头尾。

* 插入或删除永远不需要检查在头部或尾部插入的特殊情况。
  链表中永远没有需要避开的 NULL 指针。所有链表修改原语
  执行完全相同的操作，无需测试或分支。

实际上，一个包含 N 个节点的 dlist 可以看作一个 "N+1" 节点的"环"，
其中一个节点代表链表跟踪结构体。

.. figure:: dlist.png
    :align: center
    :alt: dlist 示例
    :figclass: align-center

    一个包含三个元素的 dlist。注意链表结构体
    作为第四个"元素"出现在链表中。

.. figure:: dlist-single.png
    :align: center
    :alt: 单元素 dlist 示例
    :figclass: align-center

    一个仅包含一个元素的 dlist。

.. figure:: dlist-empty.png
    :align: center
    :alt: dlist 示例
    :figclass: align-center

    一个空的 dlist。


双向链表 API 参考
--------------------------------

.. doxygengroup:: doubly-linked-list_apis
