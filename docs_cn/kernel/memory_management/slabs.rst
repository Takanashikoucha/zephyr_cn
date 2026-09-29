.. _memory_slabs_v2:

内存池
############

:dfn:`内存池（memory slab）`是一个内核对象，
允许从指定的内存区域
动态分配内存块。
内存池中
所有
内存块
都有
单个
固定
大小，
允许
它们
被
高效
地
分配
和
释放，
并
避免
内存
碎片化
问题。

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
内存池
（
仅
受
可用
RAM
限制
）。
每个
内存池
由
其
内存
地址
引用。

内存池
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
  在
  32 位
  平台
  上
  它
  必须
  至少
  4N
  字节
  长，
  在
  64 位
  平台
  上
  必须
  至少
  8N
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
  为
  内存池
  的
  块
  提供
  内存。
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

内存池
的
缓冲区
必须
对齐
到
N 字节
边界，
其中
N
是
2 的
幂。
N
在
32 位
平台
上
必须
至少
为
4，
在
64 位
平台
上
至少
为
8
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

内存池
在
使用
前
必须
初始化。
这
将
其
所有
块
标记
为
未
使用。

需要
使用
内存块
的
线程
只需
从
内存池
分配
它
即可。
当
线程
用完
一个
内存块
，
它
必须
将该
块
释放
回
内存池，
以便
该
块
可以
被
重新
使用。

如果
所有
块
当前
都在
使用
中，
线程
可以
选择
等待
一个
变得
可用。
任意
数量
的
线程
可以
同时
等待
一个
空的
内存池
；
当
一个
内存块
变得
可用
时，
它
被
交给
等待
时间
最
长
的
最高
优先级
线程。

如有
需要，
可以
定义
多个
内存池。
这
允许
一个
具有
较小
块
的
内存池
和
其他
具有
较大
块
的
内存池。
或者，
可以
使用
内存池
对象
。

内部
操作
==================

内存池
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

内存池
使用
链表
跟踪
未
分配
的
块。
32 位
平台
使用
每个
未使用
块
的
前
4 个
字节
提供
所需
的
链接，
而
64 位
平台
使用
每个
未使用
块
的
前
8 个
字节。

实现
**************

定义
内存池
====================

内存池
使用
:c:type:`k_mem_slab`
类型
的
变量
定义。
然后
必须
通过
调用
:c:func:`k_mem_slab_init`
初始化。

以下
代码
定义
并
初始化
一个
内存池，
它
有
6 个
400
字节
长
的
块，
每个
都
对齐
到
8 字节
边界。

.. code-block:: c

    struct k_mem_slab my_slab;
    char __aligned(8) my_slab_buffer[6 * 400];

    k_mem_slab_init(&my_slab, my_slab_buffer, 400, 6);

或者，
内存池
可以
通过
调用
:c:macro:`K_MEM_SLAB_DEFINE`
在
编译时
定义
并
初始化。

以下
代码
与
上面
代码段
效果
相同。
注意
该
宏
同时
定义
内存池
及其
缓冲区。

.. code-block:: c

    K_MEM_SLAB_DEFINE(my_slab, 400, 6, 8);

类似地，
可以
在
私有
作用域
中
定义
内存池
：

.. code-block:: c

    K_MEM_SLAB_DEFINE_STATIC(my_slab, 400, 6, 8);

分配
内存块
=========================

内存块
通过
调用
:c:func:`k_mem_slab_alloc`
分配。

以下
代码
基于
上面
示例，
最多
等待
100
毫秒
让
一个
内存块
变得
可用，
然后
用
零
填充
它。
如果
未
获得
合适
的
块
，
打印
警告。

.. code-block:: c

    char *block_ptr;

    if (k_mem_slab_alloc(&my_slab, (void **)&block_ptr, K_MSEC(100)) == 0) {
        memset(block_ptr, 0, 400);
	...
    } else {
        printf("Memory allocation time-out");
    }

释放
内存块
=========================

内存块
通过
调用
:c:func:`k_mem_slab_free`
释放。

以下
代码
基于
上面
示例，
分配
一个
内存块，
然后
在
不再
需要
时
释放
它。

.. code-block:: c

    char *block_ptr;

    k_mem_slab_alloc(&my_slab, (void **)&block_ptr, K_FOREVER);
    ... /* use memory block pointed at by block_ptr */
    k_mem_slab_free(&my_slab, (void *)block_ptr);

查询
内存池
使用情况
===================

内存池
的
当前
利用率
可以
在
运行时
查询。
:c:func:`k_mem_slab_num_used_get`
返回
当前
已
分配
的
块
数，
:c:func:`k_mem_slab_num_free_get`
返回
仍
可用
的
块
数。
当
:kconfig:option:`CONFIG_MEM_SLAB_TRACE_MAX_UTILIZATION`
启用
时，
:c:func:`k_mem_slab_max_used_get`
报告
同时
已
分配
的
峰值
块
数，
:c:func:`k_mem_slab_runtime_stats_get`
将这些
数字
一起
返回
在
:c:struct:`sys_memory_stats`
结构体
中。

建议
用途
**************

使用
内存池
以
固定
大小
块
分配
和
释放
内存。

在
一个
线程
向
另一个
线程
发送
大量
数据
时
使用
内存池
块，
避免
不必要
地
拷贝
数据。

配置
选项
*********************

相关
配置
选项
：

* :kconfig:option:`CONFIG_MEM_SLAB_TRACE_MAX_UTILIZATION`

API
参考
*************

.. doxygengroup:: mem_slab_apis
