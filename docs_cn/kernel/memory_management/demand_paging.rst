.. _memory_management_api_demand_paging:

按需分页
###########

按需分页（Demand paging）提供了一种机制，数据仅在当前执行上下文
需要时才会调入物理内存。物理内存
在概念上被划分为页大小的页框（page frame）
区域，用于存放数据。

Zephyr 内核映像本身始终驻留在物理内存中，
永远不会成为被驱逐（eviction）的候选对象。按需分页仅适用于：

* 运行时通过 :c:func:`k_mem_map()` 创建的匿名内存映射，以及
* 当 :kconfig:option:`CONFIG_LINKER_USE_ONDEMAND_SECTION` 启用时，
  通过 ``__ondemand_func`` / ``__ondemand_rodata`` 属性
  放入显式按需链接器段中的内存。

这是所有主流操作系统使用的同一模型：
异常或中断的分发路径
永远不会位于可分页的页上，
因此从结构上就不可能在故障处理期间
发生故障。被添加到
``__ondemand_*`` 段的代码或数据
是贡献者显式选择让
该区域可分页，
并承担确保它不会从页故障
处理器自身执行路径到达的责任。

.. note::

   早期版本的 Zephyr 还支持一种基于
   ``__pinned_*`` 链接器属性的选择性固定（pinning）方案，
   它只让内核映像中标记的子集保持驻留，
   其余部分按需分页。该
   模型被发现既不安全和/或侵入性极强：
   CPU 异常分发
   可能指向位于可驱逐页上的线程特权栈，
   如果该页已被驱逐，
   在 x86 上会升级为双重故障（double fault），
   在 ARM64 上会升级为嵌套中止（nested abort）；
   而且，"故障处理器可达表面（调度器、
   驱动、libc、
   锁原语）上的每个字节都必须
   穷尽标记"这一契约
   一次建立起来就不切实际，
   之后也无法维护。
   ``__pinned_*`` 属性族、
   对应的 Kconfig 选项
   （``LINKER_USE_PINNED_SECTION`` /
   ``LINKER_GENERIC_SECTIONS_PRESENT_AT_BOOT``）
   以及
   ``K_*_PINNED_STACK_*`` 栈宏
   已在 Zephyr 4.4 中移除。
   完整分析见 :github:`108773`。

* 当处理器尝试访问数据且数据页存在
  于某个页框中时，
  执行继续进行，
  不会受到任何中断。

* 当处理器尝试访问的数据页
  不存在于任何页框中时，
  会发生页故障（page fault）。
  然后分页代码
  如果有空闲页框，
  就从后备存储（backing store）将
  对应的数据页调入物理内存。
  如果没有更多空闲页框，
  就调用驱逐算法
  选择一个要换出的数据页，
  从而为新数据调入
  释放一个页框。
  如果该数据页
  在首次调入后被修改过，
  数据
  将被写回
  后备存储。
  如果没有修改
  或在写回后备存储之后，
  该数据页
  即被视为已换出，
  对应的页框
  现在空闲。
  然后分页代码
  调用后备存储，
  将对应于
  所请求数据位置的数据页调入。
  后备存储将该数据
  页拷贝到
  空闲页框中。
  现在数据页
  已在物理内存中，
  执行
  可以继续。

存在可以手动调用换入和换出的函数，
使用 :c:func:`k_mem_page_in()` 和 :c:func:`k_mem_page_out()`。
:c:func:`k_mem_page_in()`
可用于预调入数据页
以预期它们在近未来会
被需要。
这用于
减少页故障数量，
因为这些数据页
已在物理内存中，
从而最小化延迟。
:c:func:`k_mem_page_out()`
可用于换出那些
在相当长一段时间内
不会被访问的数据页。
这释放了页框，
使下一次
换入可以
更快执行，
因为分页代码
不需要调用
驱逐算法。

数据区域也可以用
:c:func:`k_mem_pin()`
**固定（pin）**在物理内存中。
这会
在必要时将该区域调入，
并标记其页
框，
使驱逐算法
永远不会选择它们，
从而保证
该区域保持驻留，
对它的访问
永远不会故障。
这是 :c:func:`k_mem_page_in()`
的更强形式，
适用于
必须始终可用的
延迟敏感或
安全关键数据。
固定的区域之后
用 :c:func:`k_mem_unpin()`
释放，
它
将页框
重新标记为
可驱逐；
解除固定
本身
不会驱逐该区域，
因此
如果希望立即驱逐，
之后
可以跟一个
:c:func:`k_mem_page_out()`。

术语
***********

数据页（Data Page）
  数据页
  是页大小的数据区域。
  它
  可能存在于页框中，
  或被换出到某个
  后备存储。
  其位置
  始终可以
  通过虚拟地址
  在 CPU 的页表（或等效物）中
  查找。
  数据类型
  始终
  是 ``void *``
  或在某些情况下做指针运算时
  是 ``uint8_t *``
  。

页框（Page Frame）
  页框
  是 RAM 中页大小的
  物理内存区域。
  它是
  数据页
  可以放置的
  容器。
  它
  始终
  通过
  物理地址
  引用。
  Zephyr
  有一个
  约定，
  用 ``uintptr_t``
  表示
  物理
  地址。
  对于
  每个
  页框，
  都会实例化
  一个
  ``struct k_mem_page_frame``
  来
  存储
  元数据。
  每个
  页框
  的标志
  ：

  * ``K_MEM_PAGE_FRAME_FREE``
    表示
    页框
    未使用
    且
    在
    空闲页框
    列表
    中。
    当
    该
    标志
    置位
    时，
    其他
    任何
    标志
    都
    无
    意义，
    且
    不
    得
    被
    修改。

  * ``K_MEM_PAGE_FRAME_PINNED``
    表示
    页框
    被
    固定
    在
    内存
    中，
    应
    永远
    不
    被
    换出。

  * ``K_MEM_PAGE_FRAME_RESERVED``
    表示
    被
    硬件
    保留
    的
    物理页，
    不
    得
    被
    使用。

  * ``K_MEM_PAGE_FRAME_MAPPED``
    在
    物理页
    被
    映射
    到
    虚拟
    内存
    地址
    时
    置位。

  * ``K_MEM_PAGE_FRAME_BUSY``
    表示
    页框
    当前
    参与
    换入/换出
    操作。

  * ``K_MEM_PAGE_FRAME_BACKED``
    表示
    页框
    在
    后备存储
    中
    有
    干净
    副本。

K_MEM_SCRATCH_PAGE
  提供给
  后备存储
  的
  特殊
  页的
  虚拟
  地址，
  用于
  ：
  * 将
    数据页
    从
    ``k_MEM_SCRATCH_PAGE``
    拷贝
    到
    指定
    位置
    ；或
  * 将
    数据页
    从
    提供的
    位置
    拷贝
    到
    ``K_MEM_SCRATCH_PAGE``
    。
  这
  被
  用作
  换入/换出
  操作的
  中间
  页。
  该
  临时页
  需要
  被
  映射
  为
  可
  读/写，
  供
  后备存储
  代码
  访问。
  然而
  数据页
  本身
  在
  虚拟
  地址
  空间
  中
  可能
  只
  被
  映射
  为
  只读。
  如果
  该
  页
  原样
  提供
  给
  后备存储，
  数据页
  必须
  被
  重新
  映射
  为
  可
  读/写，
  这
  有
  安全
  影响，
  因为
  数据页
  对
  应用
  的
  其他
  部分
  不再
  只读。

分页统计
*****************

当
:kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS`
启用时，
可以
通过
各种
函数
调用
获取
分页
统计
：

* 总体统计
  通过
  :c:func:`k_mem_paging_stats_get()`

* 每线程统计
  通过
  :c:func:`k_mem_paging_thread_stats_get()`
  （如果
  :kconfig:option:`CONFIG_DEMAND_PAGING_THREAD_STATS`
  启用）

* 执行
  时间
  直方图
  可以
  在
  :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM`
  启用
  且
  :kconfig:option:`CONFIG_DEMAND_PAGING_TIMING_HISTOGRAM_NUM_BINS`
  定义
  时
  获取。
  注意
  计时
  高度
  依赖
  于
  架构、
  SoC
  或
  开发板。
  强烈
  建议
  为
  特定
  应用
  定义
  ``k_mem_paging_eviction_histogram_bounds[]``
  和
  ``k_mem_paging_backing_store_histogram_bounds[]``
  。

  * 驱逐
    算法
    执行
    时间
    直方图
    通过
    :c:func:`k_mem_paging_histogram_eviction_get()`

  * 后备存储
    执行
    换入
    的
    执行
    时间
    直方图
    通过
    :c:func:`k_mem_paging_histogram_backing_store_page_in_get()`

  * 后备存储
    执行
    换出
    的
    执行
    时间
    直方图
    通过
    :c:func:`k_mem_paging_histogram_backing_store_page_out_get()`

驱逐算法
******************

驱逐算法
用于
确定
哪个
数据页
及其
对应的
页框
可以
被
换出，
以
为
下一次
换入
操作
释放
一个
页框。
有
四个
函数
被
内核
分页
代码
调用
：

* :c:func:`k_mem_paging_eviction_init()`
  被
  调用
  以
  初始化
  驱逐
  算法。
  这
  在
  ``POST_KERNEL``
  时
  被
  调用。

* :c:func:`k_mem_paging_eviction_add()`
  每次
  一个
  数据页
  变得
  有资格
  被
  未来
  驱逐
  时
  被
  调用。

* :c:func:`k_mem_paging_eviction_remove()`
  在
  一个
  数据页
  不再
  有资格
  被
  驱逐
  时
  被
  调用。
  这
  可能
  发生
  在
  给定
  数据页
  变得
  被
  固定、
  被
  解除
  映射
  或
  即将
  被
  驱逐
  时。

* :c:func:`k_mem_paging_eviction_select()`
  被
  调用
  以
  选择
  一个
  要
  驱逐
  的
  数据页。
  函数
  参数
  ``dirty``
  被
  写入
  以
  向
  调用者
  发出
  信号，
  指示
  所选
  数据页
  自
  首次
  换入
  以来
  是否
  被
  修改。
  如果
  ``dirty``
  位
  被
  返回
  为
  置位，
  分页
  代码
  向
  后备存储
  发出
  信号，
  将
  数据页
  写回
  存储
  （从而
  更新
  其
  内容）。
  该
  函数
  返回
  指向
  所选
  数据页
  对应
  页框
  的
  指针。

还有
一个
额外的
函数，
被
架构
的
内存
管理
代码
调用，
在
数据页
触发
访问
故障
时
标记
它们
：
:c:func:`k_mem_paging_eviction_accessed()`
。
这
被
LRU
算法
用于
重新
入队
"已使用"
页。

当前
有
两种
可用的
驱逐
算法
：

* 一种
  NRU
  （Not-Recently-Used，
  非最近使用）
  驱逐
  算法
  已
  作为
  示例
  实现。
  这
  是
  一个
  非常
  简单
  的
  算法，
  根据
  数据页
  是否
  被
  访问
  和
  修改
  对
  其
  排序。
  选择
  基于
  该
  排序。

* 一种
  LRU
  （Least-Recently-Used，
  最近最少使用）
  驱逐
  算法
  也
  可用。
  它
  基于
  数据页
  的
  有序
  队列。
  与
  NRU
  代码
  相比，
  LRU
  代码
  更
  复杂，
  但
  也
  显著
  更
  高效。
  推荐
  用于
  生产
  环境。

要
实现
新的
驱逐
算法，
必须
实现
:c:func:`k_mem_paging_eviction_init()`
和
:c:func:`k_mem_paging_eviction_select()`
。
如果
为
某个
算法
启用了
:kconfig:option:`CONFIG_EVICTION_TRACKING`
，
还必须
实现
这些
额外的
函数
，
:c:func:`k_mem_paging_eviction_add()`
、
:c:func:`k_mem_paging_eviction_remove()`
、
:c:func:`k_mem_paging_eviction_accessed()`
。

后备存储
*************

后备存储
负责
在
数据页
与其
对应的
页框
和
存储
之间
换入/换出。
这些
是
必须
实现
的
函数
：

* :c:func:`k_mem_paging_backing_store_init()`
  在
  ``POST_KERNEL``
  时
  被
  调用
  以
  初始化
  后备存储。

* :c:func:`k_mem_paging_backing_store_location_get()`
  被
  调用
  以
  保留
  一个
  后备存储
  位置，
  以便
  数据页
  可以
  被
  换出。
  这个
  ``location``
  令牌
  被
  传递给
  :c:func:`k_mem_paging_backing_store_page_out()`
  以
  执行
  实际的
  换出
  操作。

* :c:func:`k_mem_paging_backing_store_location_free()`
  被
  调用
  以
  释放
  一个
  后备存储
  位置
  （
  ``location``
  令牌
  ），
  然后
  可以
  用于
  后续
  换出
  操作。

* :c:func:`k_mem_paging_backing_store_location_query()`
  被
  调用
  以
  获取
  对应于
  将被
  虚拟
  映射
  并
  按需
  换入
  的
  存储
  内容
  的
  ``location``
  令牌。
  与
  :kconfig:option:`CONFIG_DEMAND_MAPPING`
  搭配
  最
  有用。

* :c:func:`k_mem_paging_backing_store_page_in()`
  将
  数据页
  从
  与
  提供的
  ``location``
  令牌
  关联
  的
  后备存储
  位置
  拷贝
  到
  ``K_MEM_SCRATCH_PAGE``
  指向
  的
  页。

* :c:func:`k_mem_paging_backing_store_page_out()`
  将
  数据页
  从
  ``K_MEM_SCRATCH_PAGE``
  拷贝
  到
  与
  提供的
  ``location``
  令牌
  关联
  的
  后备存储
  位置。

* :c:func:`k_mem_paging_backing_store_page_finalize()`
  在
  :c:func:`k_mem_paging_backing_store_page_in()`
  之后
  被
  调用，
  以便
  更新
  页框
  结构体
  用于
  内部
  记账。
  这
  可以
  是
  无
  操作
  。

要
实现
新的
后备存储，
必须
实现
上面
提到
的
函数。
:c:func:`k_mem_paging_backing_store_page_finalize()`
如果
愿意，
可以
是
一个
空
函数。

API 参考
*************

.. doxygengroup:: mem-demand-paging

驱逐算法 API
=======================

.. doxygengroup:: mem-demand-paging-eviction

后备存储 API
==================

.. doxygengroup:: mem-demand-paging-backing-store
