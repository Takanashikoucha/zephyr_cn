.. _memory_management_shared_multi_heap:

共享多堆
#################

共享多堆内存池管理器使用多堆分配器
来管理一组具有不同能力/属性
（可缓存、不可缓存等）的
保留内存区域。

所有不同的区域都可以在运行时
添加到共享多堆
池中，
提供
一个
不透明
的
"属性"
值
（
整数
或
枚举
值
），
驱动
或
应用
可以
用
它
请求
具有
某些
能力
的
内存。

该
框架
通常
按
如下
方式
使用
：

1. 启动
   时
   某些
   平台
   代码
   使用
   :c:func:`shared_multi_heap_pool_init()`
   初始化
   共享
   多堆
   框架，
   并用
   :c:func:`shared_multi_heap_add()`
   将
   内存
   区域
   添加
   到
   池中，
   可能
   从
   DT
   收集
   区域
   所需
   的
   信息。

2. 每个
   内存
   区域
   编码
   在
   :c:struct:`shared_multi_heap_region`
   结构体
   中。
   该
   结构体
   还
   携带
   一个
   不透明
   的、
   用户
   定义
   的
   整数
   值，
   用于
   定义
   区域
   能力
   （
   例如
   ：
   可缓存性、
   CPU
   亲和性
   等
   ）

.. code-block:: c

   // Init the shared multi-heap pool
   shared_multi_heap_pool_init()

   // Fill the struct with the data for cacheable memory
   struct shared_multi_heap_region cacheable_r0 = {
        .addr = addr_r0,
        .size = size_r0,
        .attr = SMH_REG_ATTR_CACHEABLE,
   };

   // Add the region to the pool
   shared_multi_heap_add(&cacheable_r0, NULL);

   // Add another cacheable region
   struct shared_multi_heap_region cacheable_r1 = {
        .addr = addr_r1,
        .size = size_r1,
        .attr = SMH_REG_ATTR_CACHEABLE,
   };

   shared_multi_heap_add(&cacheable_r1, NULL);

   // Add a non-cacheable region
   struct shared_multi_heap_region non_cacheable_r2 = {
        .addr = addr_r2,
        .size = size_r2,
        .attr = SMH_REG_ATTR_NON_CACHEABLE,
   };

   shared_multi_heap_add(&non_cacheable_r2, NULL);

3. 当
   驱动
   或
   应用
   需要
   具有
   某种
   能力
   的
   一些
   动态
   内存
   时，
   可以
   使用
   :c:func:`shared_multi_heap_alloc()`
   （
   或
   对齐
   版本
   ）
   通过
   使用
   不透明
   参数
   选择
   所需
   内存
   的
   正确
   属性
   集合
   来
   请求
   内存。
   框架
   会
   负责
   基于
   不透明
   参数
   和
   堆
   的
   运行时
   状态
   （
   可用
   内存、
   堆
   状态
   等
   ）
   选择
   正确
   的
   堆
   （
   从而
   是
   内存
   区域
   ）
   来
   划分
   内存。

.. code-block:: c

   // Allocate 4K from cacheable memory
   shared_multi_heap_alloc(SMH_REG_ATTR_CACHEABLE, 0x1000);

   // Allocate 4K from non-cacheable memory
   shared_multi_heap_alloc(SMH_REG_ATTR_NON_CACHEABLE, 0x1000);

添加新属性
*********************

该
API
不
强制
任何
属性，
但
至少
它
定义了
两个
最
常见
的
：
:c:enumerator:`SMH_REG_ATTR_CACHEABLE`
和
:c:enumerator:`SMH_REG_ATTR_NON_CACHEABLE`
。

.. doxygengroup:: shared_multi_heap
