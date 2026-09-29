.. _memory_management_api_virtual_memory:

虚拟内存
##############

Zephyr 中的虚拟内存（VM）为开发者提供了
精细调整
内存
访问
的
能力。
要
利用
虚拟内存，
平台
必须
支持
内存
管理
单元
（
MMU
）
，
并
在
构建
中
启用
它。
由于
Zephyr
的
目标
主要
是
嵌入式
系统，
Zephyr
中的
虚拟内存
支持
与
传统
操作系统
中
的
略有
不同
：

内核
映像
映射
  默认
  情况下，
  如果
  未
  启用
  按需
  分页，
  对
  内核
  映像
  （
  包括
  代码
  和
  数据
  ）
  在
  物理
  与
  虚拟
  内存
  地址
  空间
  之间
  做
  1:1
  映射。
  偏离
  这
  一
  做法
  需要
  仔细
  操作
  链接
  脚本。

二级
存储
  基本
  虚拟内存
  支持
  不
  利用
  二级
  存储
  来
  扩展
  可用
  内存。
  最大
  可用
  内存
  与
  物理
  内存
  相同。

  * :ref:`memory_management_api_demand_paging`
    启用
    将
    二级
    存储
    用作
    虚拟内存
    的
    后备
    存储，
    从而
    允许
    比
    可用
    物理内存
    更
    大
    的
    可用
    内存。
    注意
    按需
    分页
    需要
    显式
    启用。

  * 虽然
    虚拟
    内存
    空间
    可以
    大于
    物理
    内存
    空间，
    但
    不
    启用
    按需
    分页
    时，
    所有
    虚拟
    映射
    的
    内存
    必须
    由
    物理
    内存
    支撑。


Kconfig
********

必需
========

这些
是
内核
支持
虚拟内存
需要
启用
或
定义
的
Kconfig
。

* :kconfig:option:`CONFIG_MMU`
  ：
  必须
  启用
  才能
  支持
  内核
  虚拟内存。

* :kconfig:option:`CONFIG_MMU_PAGE_SIZE`
  ：
  内存
  页
  大小。
  默认
  为
  4KB
  。

* :kconfig:option:`CONFIG_KERNEL_VM_BASE`
  ：
  虚拟
  地址
  空间
  的
  基
  地址。

* :kconfig:option:`CONFIG_KERNEL_VM_SIZE`
  ：
  虚拟
  地址
  空间
  的
  大小。
  默认
  为
  8MB
  。

* :kconfig:option:`CONFIG_KERNEL_VM_OFFSET`
  ：
  内核
  映像
  从
  :kconfig:option:`CONFIG_KERNEL_VM_BASE`
  开始
  的
  该
  偏移
  处
  开始。

可选
========

* :kconfig:option:`CONFIG_KERNEL_DIRECT_MAP`
  ：
  允许
  虚拟
  地址
  与
  物理
  地址
  之间
  1:1
  映射，
  而
  不是
  内核
  在
  虚拟
  地址
  空间
  内
  选择
  地址。
  这
  对
  映射
  设备
  MMIO
  区域
  以
  获得
  更
  精确
  的
  访问
  控制
  很有
  用。


内存
映射
概览
*******************

这是
虚拟内存
地址
空间
内存
映射
的
概览。
注意
代码
中
使用
的
``Z_*``
宏
可能
根据
架构
和
Kconfig
有
不同
的
含义，
下面
会
解释。

.. code-block:: none
   :emphasize-lines: 1, 3, 9, 22, 24

   +--------------+ <- K_MEM_VIRT_RAM_START
   | Undefined VM | <- architecture specific reserved area
   +--------------+ <- K_MEM_KERNEL_VIRT_START
   | Mapping for  |
   | main kernel  |
   | image        |
   |              |
   |              |
   +--------------+ <- K_MEM_VM_FREE_START
   |              |
   | Unused,      |
   | Available VM |
   |              |
   |..............| <- grows downward as more mappings are made
   | Mapping      |
   +--------------+
   | Mapping      |
   +--------------+
   | ...          |
   +--------------+
   | Mapping      |
   +--------------+ <- memory mappings start here
   | Reserved     | <- special purpose virtual page(s) of size K_MEM_VM_RESERVED
   +--------------+ <- K_MEM_VIRT_RAM_END

* ``K_MEM_VIRT_RAM_START``
  是
  虚拟
  内存
  地址
  空间
  的
  开头。
  这
  需要
  页
  对齐。
  当前
  它
  与
  :kconfig:option:`CONFIG_KERNEL_VM_BASE`
  相同。

* ``K_MEM_VIRT_RAM_SIZE``
  是
  虚拟
  内存
  地址
  空间
  的
  大小。
  这
  需要
  页
  对齐。
  当前
  它
  与
  :kconfig:option:`CONFIG_KERNEL_VM_SIZE`
  相同。

* ``K_MEM_VIRT_RAM_END``
  就是
  （
  ``K_MEM_VIRT_RAM_START``
  +
  ``K_MEM_VIRT_RAM_SIZE``
  ）。

* ``K_MEM_KERNEL_VIRT_START``
  与
  链接
  脚本
  中
  指定
  的
  ``z_mapped_start``
  相同。
  这
  是
  启动
  时
  内核
  映像
  开头
  的
  虚拟
  地址。

* ``K_MEM_KERNEL_VIRT_END``
  与
  链接
  脚本
  中
  指定
  的
  ``z_mapped_end``
  相同。
  这
  是
  启动
  时
  内核
  映像
  末尾
  的
  虚拟
  地址。

* ``K_MEM_VM_FREE_START``
  是
  可以
  分配
  地址
  用于
  内存
  映射
  的
  虚拟
  地址
  空间
  开头。
  这
  取决于
  是否
  启用
  :kconfig:option:`CONFIG_ARCH_MAPS_ALL_RAM`
  。

  * 如果
    启用，
    意味着
    所有
    物理
    内存
    都
    映射
    在
    虚拟
    内存
    地址
    空间
    中，
    它
    与
    （
    :c:macro:`DT_CHOSEN_SRAM_ADDR`
    +
    :c:macro:`DT_CHOSEN_SRAM_SIZE`
    ）
    相同。

  * 如果
    禁用，
    ``K_MEM_VM_FREE_START``
    与
    ``K_MEM_KERNEL_VIRT_END``
    相同，
    这
    是
    内核
    映像
    的
    末尾。

* ``K_MEM_VM_RESERVED``
  是
  保留
  用于
  支持
  内核
  功能
  的
  区域。
  例如，
  一些
  地址
  被
  保留
  用于
  支持
  按需
  分页。


虚拟内存
映射
***********************

启动
时
设置
映射
===========================

一般来说，
大多数
受支持
的
架构
在
启动
时
按
如下
设置
内存
映射
：

* ``.text``
  段
  只读
  且
  可执行。
  它
  在
  内核
  和
  用户
  模式
  下
  都
  可
  访问。

* ``.rodata``
  段
  只读
  且
  不可
  执行。
  它
  在
  内核
  和
  用户
  模式
  下
  都
  可
  访问。

* 其他
  内核
  段，
  如
  ``.data``
  、
  ``.bss``
  和
  ``.noinit``
  ，
  可读
  写
  且
  不可
  执行。
  它们
  只在
  内核
  模式
  下
  可
  访问。

  * 用户
    模式
    线程
    的
    栈
    在
    线程
    创建
    时
    自动
    被授予
    其
    对应
    用户
    模式
    线程
    的
    可读
    写
    访问
    。

  * 全局
    变量
    默认
    对
    用户
    模式
    线程
    不可
    访问。
    参见
    :ref:`内存
    域
    和
    分区
    <memory_domain>`
    了解
    如何
    在
    用户
    模式
    线程
    中
    使用
    全局
    变量，
    以及
    如何
    在
    用户
    模式
    线程
    之间
    共享
    数据。

这些
映射
的
缓存
模式
因
架构
而异。
它们
可以
是
无
缓存、
写
回
或
写
直通。

注意
SoC
有
其
自己
启动
所需
的
附加
映射，
这些
映射
定义
在
其
自己的
SoC
配置
下。
这些
映射
通常
包括
设置
硬件
所需
的
设备
MMIO
区域。


映射
匿名
内存
========================

未
使用
的
物理
内存
可以
按需
映射
在
虚拟
地址
空间
中。
这
在
概念
上
类似
于
从
堆
分配
内存，
但
这些
映射
必须
按
页
大小
对齐，
并
有
更
精细
的
访问
控制。

* :c:func:`k_mem_map`
  可以
  用于
  映射
  未
  使用
  的
  物理
  内存
  ：

  * 请求
    的
    大小
    必须
    是
    页
    大小
    的
    倍数。

  * 返回
    的
    地址
    在
    ``K_MEM_VM_FREE_START``
    和
    ``K_MEM_VIRT_RAM_END``
    之间
    的
    虚拟
    地址
    空间
    内。

  * 映射
    的
    区域
    不
    保证
    在
    内存
    中
    物理
    连续。

  * 映射
    虚拟
    区域
    紧邻
    之前
    和
    之后
    的
    保护
    页
    自动
    分配，
    以
    捕获
    由于
    缓冲区
    下
    溢
    或
    上
    溢
    导致
    的
    访问
    问题。

* 映射
  的
  区域
  可以
  通过
  :c:func:`k_mem_unmap`
  解除
  映射
  （
  即
  释放
  ）
  ：

  * 必须
    注意
    向
    :c:func:`k_mem_map`
    和
    :c:func:`k_mem_unmap`
    都
    传递
    相同
    的
    区域
    大小。
    解除
    映射
    函数
    在
    解除
    映射
    前
    不
    检查
    它
    是否
    是
    有效
    的
    映射
    区域。


API
参考
*************

.. doxygengroup:: kernel_memory_management
