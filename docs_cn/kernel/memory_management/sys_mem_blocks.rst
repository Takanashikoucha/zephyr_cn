.. _sys_mem_blocks:

内存块分配器
#######################

内存块分配器
允许
从
指定
内存
区域
动态
分配
内存块，
其中
：

* 所有
  内存块
  有
  单个
  固定
  大小。

* 可以
  同时
  分配
  或
  释放
  多个
  块。

* 一起
  分配
  的
  一组
  块
  可能
  不
  连续。
  这
  对
  分散-聚集
  （
  scatter-gather
  ）
  DMA
  传输
  等
  操作
  很有
  用。

* 已
  分配
  块
  的
  记账
  在
  关联
  缓冲区
  之外
  进行
  （
  与
  内存池
  不同
  ）。
  这
  允许
  缓冲区
  驻留
  在
  可以
  断电
  以
  节省
  能量
  的
  内存
  区域。

.. contents::
    :local:
    :depth: 2

概念
********

可以
定义
任意
数量
的
内存块
分配器
（
仅
受
可用
RAM
限制
）。
每个
分配器
由
其
内存
地址
引用。

内存块
分配器
具有
以下
关键
特性
：

* 每个
  块
  的
  **块
  大小**
  ，
  以
  字节
  为
  单位。
  它
  必须
  至少
  4N
  字节
  长，
  其中
  N
  大于
  0
  。

* 可供
  分配
  的
  **块
  数量**
  。
  它
  必须
  大于
  零。

* 一个
  **缓冲区**
  ，
  提供
  内存块
  分配器
  将
  从
  中
  分配
  块
  的
  后备
  存储。
  它
  必须
  至少
  "块
  大小"
  乘以
  "块
  数量"
  字节
  长。

* 一个
  **块
  位图**
  ，
  用于
  跟踪
  哪个
  块
  已
  被
  分配。

缓冲区
必须
对齐
到
N 字节
边界，
其中
N
是
大于
2 的
2 的
幂
（
即
4、
8、
16、
...
）
。
要
确保
缓冲区
中
所有
内存块
同样
对齐
到
该
边界，
块
大小
也
必须
是
N
的
倍数。

由于
内部
记账
结构
的
使用
和
创建，
每个
内存块
分配器
必须
在
编译时
声明
和
定义。

内部
操作
==================

与
每个
分配器
关联
的
缓冲区
是
固定
大小
块
的
数组，
块
之间
没有
浪费
的
空间。

内存块
分配器
使用
位图
跟踪
未
分配
的
块。

内存块
分配器
***********************

内部地，
内存块
分配器
使用
位图
跟踪
哪些
块
已
被
分配。
每个
分配器
利用
``sys_bitarray``
接口，
从
后备
缓冲区
一次
一个
地
获取
内存块，
直到
达到
请求
的
块
数。
关于
分配器
的
所有
元数据
存储
在
后备
缓冲区
之外。
这
允许
后备
缓冲区
的
内存
区域
断电
以
节省
能量，
因为
分配器
代码
从不
触碰
缓冲区
的
内容。

多
内存块
分配器
组
***********************************

多
内存块
分配器
组
工具
函数
用于
方便
地
管理
一组
分配器。
可以
编写
自定义
函数
来选择
该
组
管理
的
哪个
分配器
应
被
用于
块
分配。

分配器
组
应
在
运行时
通过
:c:func:`sys_multi_mem_blocks_init`
初始化。
然后
每个
分配器
可以
通过
:c:func:`sys_multi_mem_blocks_add_allocator`
添加。

要
从
组
分配
内存块，
调用
:c:func:`sys_multi_mem_blocks_alloc`
并
传入
一个
不透明
的
"配置"
参数。
该
参数
直接
传递
给
分配器
选择
函数，
以便
选择
合适
的
分配器。
选择
分配器
后，
内存块
通过
:c:func:`sys_mem_blocks_alloc`
分配。

已
分配
的
内存块
可以
通过
:c:func:`sys_multi_mem_blocks_free`
释放。
调用者
不
需要
传递
配置
参数。
分配器
代码
将
传入
的
内存
地址
匹配
以
找到
正确
的
分配器，
然后
内存块
通过
:c:func:`sys_mem_blocks_free`
释放。

使用
*****

定义
内存块
分配器
==================================

内存块
分配器
使用
:c:type:`sys_mem_blocks_t`
类型
的
变量
定义。
它
需要
通过
调用
:c:macro:`SYS_MEM_BLOCKS_DEFINE`
在
编译时
定义
并
初始化。

以下
代码
定义
并
初始化
一个
内存块
分配器，
它
有
4 个
64
字节
长
的
块，
每个
都
对齐
到
4 字节
边界
：

.. code-block:: c

   SYS_MEM_BLOCKS_DEFINE(allocator, 64, 4, 4);

类似地，
可以
在
私有
作用域
中
定义
内存块
分配器
：

.. code-block:: c

   SYS_MEM_BLOCKS_DEFINE_STATIC(static_allocator, 64, 4, 4);

也可以
向
分配器
提供
预定义
的
缓冲区，
缓冲区
可以
单独
放置。
注意
缓冲区
**必须**
在
定义
时
指定
其
对齐。

.. code-block:: c

   uint8_t __aligned(4) backing_buffer[64 * 4];
   SYS_MEM_BLOCKS_DEFINE_WITH_EXT_BUF(allocator, 64, 4, backing_buffer);

分配
内存块
========================

内存块
可以
通过
调用
:c:func:`sys_mem_blocks_alloc`
分配。

.. code-block:: c

   int ret;
   uintptr_t blocks[2];

   ret = sys_mem_blocks_alloc(allocator, 2, blocks);

如果
``ret == 0``
，
数组
``blocks``
将
包含
一个
内存
地址
数组，
指向
已
分配
的
块。

释放
内存块
========================

内存块
通过
调用
:c:func:`sys_mem_blocks_free`
释放。

以下
代码
基于
上面
示例
分配
2 个
内存块，
然后
在
不再
需要
时
释放
它们。

.. code-block:: c

   int ret;
   uintptr_t blocks[2];

   ret = sys_mem_blocks_alloc(allocator, 2, blocks);
   ... /* perform some operations on the allocated memory blocks */
   ret = sys_mem_blocks_free(allocator, 2, blocks);

使用
多
内存块
分配器
组
=========================================

以下
代码
演示
如何
初始化
一个
分配器
组
：

.. code-block:: c

   sys_mem_blocks_t *choice_fn(struct sys_multi_mem_blocks *group, void *cfg)
   {
       ... /* choose which allocator in the group to use based on cfg */
   }

   SYS_MEM_BLOCKS_DEFINE(allocator0, 64, 4, 4);
   SYS_MEM_BLOCKS_DEFINE(allocator1, 64, 4, 4);

   static sys_multi_mem_blocks_t alloc_group;

   sys_multi_mem_blocks_init(&alloc_group, choice_fn);
   sys_multi_mem_blocks_add_allocator(&alloc_group, &allocator0);
   sys_multi_mem_blocks_add_allocator(&alloc_group, &allocator1);

要
从
组
分配
和
释放
内存块
：

.. code-block:: c

   int ret;
   uintptr_t blocks[1];
   size_t blk_size;

   ret = sys_multi_mem_blocks_alloc(&alloc_group, UINT_TO_POINTER(0),
                                   1, blocks, &blk_size);

   ret = sys_multi_mem_blocks_free(&alloc_group, 1, blocks);

API
参考
*************

.. doxygengroup:: mem_blocks_apis
