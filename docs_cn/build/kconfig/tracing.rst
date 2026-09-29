.. _kconfig_traceconfig:

跟踪
值
到
其
来源
##############################

保存
到
:file:`zephyr/.config` 的
合并
配置
包含
将
用户
配置
文件
应用
到
整个
Kconfig 文件
树
的
结果。
这个
过程
可能
很
难
跟踪，
特别
是
当
不可见
符号
从
树
的
任何
地方
被
隐式
选择
时。
为
帮助
这，
``traceconfig`` 目标
可以
用于
在
构建
目录
中
生成
一个
详细
说明
每个
符号
如何
得到
其
最终
值
的
文件。

按
通常
方式
构建
Zephyr 项目
后，
可以
使用
以下
命令
之一
生成
Kconfig 跟踪：

   .. code-block:: bash

      west build -t traceconfig

   .. code-block:: bash

      ninja traceconfig

.. note::
   生成
   的
   信息
   只
   在
   干净
   构建
   上
   有用，
   因为
   否则
   ``.config`` 文件
   "固定"
   所有
   设置
   到
   特定
   值
   （如
   :ref:`Stuck symbols <stuck_symbols>` 中
   所述）。
   因此，
   推荐
   在
   生成
   跟踪
   前
   运行
   :ref:`pristine build <west-building-pristine>`。

输出
将
在
构建
目录
中
的
:file:`zephyr/kconfig-trace.md` 文件
中。
这
个
文件
最好
在
IDE 中
查看
以
利用
Markdown
元素
（表格、
高亮、
可
点击
链接），
但
即使
直接
用
任何
文本
编辑器
打开
也
容易
理解。

报告
分为
三个
部分：

#. 可见
   符号
#. 不可见
   符号
#. 未
   设置
   符号

对于
第
1 和
2 部分，
呈现
一个
表格，
其中
每个
符号
显示
其
类型、
名称
和
当前
值。
第
四
列
详细
说明
导致
值
被
应用
的
语句
类型，
可以
是
以下
之一：

 - *assigned*，
   当
   从
   配置
   文件
   读取
   显式
   赋值，
   形式
   为
   ``CONFIG_xxx=y``；

 - *default*，
   当
   没有
   用户
   赋值，
   但
   从
   Kconfig 树
   读取
   适用
   的
   默认
   值；

 - *selected* 或
   *implied*，
   当
   来自
   单独
   符号
   的
   ``select`` 或
   ``imply`` 语句
   导致
   符号
   被
   设置。

第
五
列
详细
说明
源
语句
的
位置。
对于
前
两种
语句
类型，
提供
精确
位置
（文件
名
和
行号）；
在
后
两种
情况
下，
它
包含
导致
符号
被
设置
的
表达式。

最后，
第
3 部分
简单
列出
所有
未
定义
符号。
这些
没有
附加
信息，
因为
它们
从未
通过
上述
任何
方式
接收
值。
