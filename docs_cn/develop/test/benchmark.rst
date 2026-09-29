.. _ztest_benchmarking:

基准
测试
框架
######################

Zephyr
基准
测试
框架
提供
周期
精确
的
性能
测量。
它
自动化
数据
收集
和
统计
计算，
提供
一
种
标准化
方式
评估
Zephyr
生态
系统
中
的
执行
指标。

概览
********

这
个
框架
通过
提供
以下
帮助
识别
回归
并
优化
关键
路径：

* **标准化
  API**：
  与
  现有
  ``ztest``
  约定
  对齐
  的
  宏。
* **统计
  分析**：
  均值、
  标准
  偏差、
  标准
  误差
  和
  Min/Max
  值
  的
  计算。
* **开销
  补偿**：
  包含
  一
  个
  对照
  测试
  以
  考虑
  基准
  测试
  框架
  自己
  的
  执行
  时间。

配置
*************

要
使用
基准
测试
框架，
你
必须
启用
以下
Kconfig
选项：

.. code-block:: cfg

   CONFIG_ZTEST=y
   CONFIG_ZTEST_BENCHMARK=y

使用
*****

基准
测试
套件
与
普通
ztest
测试
套件
类似
定义，
首先
用
``ZTEST_BENCHMARK_SUITE``
定义
套件，
然后
用
``ZTEST_BENCHMARK``
或
``ZTEST_BENCHMARK_TIMED``
宏
向
套件
添加
单个
基准
测试。

.. code-block:: c

   #include
   <zephyr/ztest.h>

   ZTEST_BENCHMARK_SUITE(<test
   suite
   name>,
   <setup_fn>,
   <teardown_fn>);


标准
基准
测试
===================

标准
基准
测试
是
基于
样本
的，
意味着
它们
执行
测试
指定
的
次数
并
测量
总
周期
数。
这
对
基准
测试
你
想
理解
原始
CPU
性能
（以
周期
为
单位）
的
关键
路径
有用。
它
提供
关于
代码
效率
的
洞察
并
帮助
识别
CPU
使用
方面
的
瓶颈。
这
个
基准
测试
方法
适合
执行
时间
一致
且
不
受
外部
因素
（如
I/O
操作
或
上下文
切换）
严重
影响
的
代码。

.. code-block:: c

   #include
   <zephyr/ztest.h>
