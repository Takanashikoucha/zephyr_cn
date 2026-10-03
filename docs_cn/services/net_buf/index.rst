.. _net_buf_interface:

网络缓冲区
###############

.. contents::
    :local:
    :depth: 2


概述
********

网络缓冲区是网络协议栈（以及蓝牙协议栈）传递数据的核心概念。其 API 定义在 :zephyr_file:`include/zephyr/net_buf.h` 中。

创建缓冲区
****************

网络缓冲区通过先定义一个缓冲区池来创建：

.. code-block:: c

   NET_BUF_POOL_DEFINE(pool_name, buf_count, buf_size, user_data_size, NULL);

缓冲区池是一个静态变量，如果需要将其导出到其他模块，则需要一个单独的指针。

一旦缓冲区池定义完成，就可以通过以下方式从中分配缓冲区：

.. code-block:: c

   buf = net_buf_alloc(&pool_name, timeout);

缓冲区池及其缓冲区没有显式的初始化函数，而是在调用 :c:func:`net_buf_alloc` 时隐式完成初始化。

如果需要在缓冲区中为稍后要添加的协议头预留空间，可以使用以下方式为缓冲区预留这部分头部空间：

.. code-block:: c

   net_buf_reserve(buf, headroom);

除了实际的协议数据和通用解析上下文外，网络缓冲区还可以包含协议特定的上下文，即用户数据。缓冲区的数据最大容量和用户数据最大容量在声明缓冲区池时于编译期定义。

缓冲区原生支持通过 k_fifo 内核对象进行传递。使用 :c:func:`k_fifo_put` 和 :c:func:`k_fifo_get` 将一个缓冲区从某个线程传递到另一个线程。

针对单链表中的缓冲区，存在一些特殊函数，其中必须使用 :c:func:`net_buf_slist_put` 和 :c:func:`net_buf_slist_get` 函数，而不能使用 :c:func:`sys_slist_append` 和 :c:func:`sys_slist_get`。

常用操作
*****************

网络缓冲区 API 提供了一些有用的辅助函数，用于编码和解码缓冲区中的数据。要完全理解这些辅助函数，最好先了解与它们配合使用的基本操作名称：

Add
  将数据添加到缓冲区末尾。修改数据长度值，同时保持实际数据指针不变。要求缓冲区中有足够的尾部空间。一些用于添加数据的 API 示例：

  .. code-block:: c

     void *net_buf_add(struct net_buf *buf, size_t len);
     void *net_buf_add_mem(struct net_buf *buf, const void *mem, size_t len);
     uint8_t *net_buf_add_u8(struct net_buf *buf, uint8_t value);
     void net_buf_add_le16(struct net_buf *buf, uint16_t value);
     void net_buf_add_le32(struct net_buf *buf, uint32_t value);

Remove
  从缓冲区末尾移除数据。修改数据长度值，同时保持实际数据指针不变。一些用于移除数据的 API 示例：

  .. code-block:: c

     void *net_buf_remove_mem(struct net_buf *buf, size_t len);
     uint8_t net_buf_remove_u8(struct net_buf *buf);
     uint16_t net_buf_remove_le16(struct net_buf *buf);
     uint32_t net_buf_remove_le32(struct net_buf *buf);

Push
  在缓冲区开头添加数据。同时修改数据长度值和数据指针。要求缓冲区中有足够的头部空间。一些用于在开头添加数据的 API 示例：

  .. code-block:: c

     void *net_buf_push(struct net_buf *buf, size_t len);
     void *net_buf_push_mem(struct net_buf *buf, const void *mem, size_t len);
     void net_buf_push_u8(struct net_buf *buf, uint8_t value);
     void net_buf_push_le16(struct net_buf *buf, uint16_t value);

Pull
  从缓冲区开头移除数据。同时修改数据长度值和数据指针。一些用于从开头移除数据的 API 示例：

  .. code-block:: c

     void *net_buf_pull(struct net_buf *buf, size_t len);
     void net_buf_pull_mem(struct net_buf *buf, size_t len);
     uint8_t net_buf_pull_u8(struct net_buf *buf);
     uint16_t net_buf_pull_le16(struct net_buf *buf);
     uint32_t net_buf_pull_le32(struct net_buf *buf);

Add 和 Push 操作用于将数据编码到缓冲区中，而 Remove 和 Pull 操作用于从缓冲区解码数据。

引用计数
******************

每个网络缓冲区都采用引用计数。缓冲区最初通过调用 :c:func:`net_buf_alloc()` 从空闲缓冲区池中获取，得到一个引用计数为 1 的缓冲区。引用计数可以通过 :c:func:`net_buf_ref()` 递增，或通过 :c:func:`net_buf_unref()` 递减。当计数降为零时，缓冲区会自动放回空闲缓冲区池。

所有权
*********

对缓冲区的每个引用都有且仅有一个所有者。所有者要么通过
:c:func:`net_buf_unref` 释放其引用，要么把引用转移给新的所有者，
例如 FIFO、链表，或某个接收缓冲区所有权的函数。
转移之后，原所有者不得再使用该缓冲区，除非它自己还持有另一个引用。

片段链通过其头部拥有所有权。链中每个缓冲区都拥有对下一个片段的引用，
并在其自身被释放时释放该引用；因此，释放对头部的最后一个引用，
会释放整条链，直到第一个仍在其他地方被引用的片段为止。
:c:func:`net_buf_frag_insert` 会接收所给片段的所有权；
当头部不是 ``NULL`` 时，:c:func:`net_buf_frag_add` 也会接收所有权。
当头部为 ``NULL`` 时，:c:func:`net_buf_frag_add` 会带有一个新引用返回该片段，
调用者仍保留其自身引用。

被传入缓冲区的函数或回调会对该引用执行以下操作之一，
其文档应说明是哪一种：

借用
  函数可以使用该缓冲区直到返回，但不得保留或转移它。
  若要保留借用的缓冲区，必须先通过 :c:func:`net_buf_ref` 获取自己的引用。

接收所有权
  无论成功还是出错，引用都会在所有返回路径上转移给函数。

仅在成功时接收所有权
  只有函数成功时引用才会转移。出错时，调用者仍拥有该缓冲区。

有两个辅助函数作用于持有引用的指针本身，
使得原所有者留下的是 ``NULL``，而不是指向一个它不再拥有的缓冲区的指针。
:c:func:`net_buf_take` 从指针中移出引用，:c:func:`net_buf_drop` 释放引用。
:c:func:`net_buf_drop` 适用于生命周期长于释放动作的指针，
例如结构体成员，或可能已经为 ``NULL`` 的指针。
一个持有引用并在作用域结束时离开的局部指针，
只需要 :c:func:`net_buf_unref`。

将缓冲区放入 FIFO 或链表，就是把引用转移给队列。
接收方可能在 :c:func:`k_fifo_put` 返回之前就已处理并释放该缓冲区，
例如当更高优先级的线程正在等待该 FIFO 时。
应在同一表达式中用 :c:func:`net_buf_take` 转移引用：

.. code-block:: c

   k_fifo_put(&tx_queue, net_buf_take(&buf));

即使 ``buf`` 在调用后立即离开作用域也应这样做：
普通指针参数看起来与仅被借用的参数相同，
而 :c:func:`net_buf_take` 能在调用点表明引用发生了转移。

只有当调用总是接收所有权时（例如 :c:func:`k_fifo_put`、
:c:func:`net_buf_slist_put` 和 :c:func:`net_buf_frag_insert`），
才能把 ``net_buf_take(&buf)`` 作为参数传入。
对于仅在成功时接收所有权的函数，如果传入普通指针，
无论结果如何，调用者的指针都不会改变，
只有返回值能表明缓冲区是否仍归调用者所有。

因此，新设计的、接收所有权的函数应接收调用者缓冲区指针的指针，
并在接收所有权时用 :c:func:`net_buf_take` 移出引用。
这样，调用者的指针恰好在全权转移时变为 ``NULL``，
无论调用结果如何，之后调用 :c:func:`net_buf_drop` 都是正确的：

.. code-block:: c

   int foo_send(struct foo *foo, struct net_buf **buf)
   {
       if (!foo->ready) {
           return -EAGAIN;
       }

       k_fifo_put(&foo->tx_queue, net_buf_take(buf));

       return 0;
   }

   err = foo_send(foo, &buf);
   if (err != 0) {
       LOG_WRN("Not sent (err %d)", err);
   }

   /* 仅在 foo_send() 未接收缓冲区时释放 */
   net_buf_drop(&buf);

把现有函数改成这种形式会破坏其调用者，
因此最好在函数本身被重构时一并完成。

API 参考
*************

.. doxygengroup:: net_buf
