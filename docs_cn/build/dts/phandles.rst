.. _dt-phandles:

Phandle
########

设备树中*phandle*的概念与
C 中的
指针
非常
类似。
你可以
像
使用
指针
引用
C 中
的
结构
一样，
使用
phandle
引用
设备树
中
的
节点。

.. contents:: 目录
   :local:

获取 phandle
****************

获取
设备树
节点
phandle 的
通常
方式
是
从
其
节点
标签
之一
获取。
例如，
对于
此
设备树：

.. code-block:: DTS

   / {
           lbl_a: node-1 {};
           lbl_b: lbl_c: node-2 {};
   };

你可以
编写
phandle 为：

- ``/node-1`` 写
  为
  ``&lbl_a``
- ``/node-2`` 写
  为
  ``&lbl_b`` 或
  ``&lbl_c``

注意
``&nodelabel`` 设备树
语法
与
"取
地址"
C 语法
的
相似
之处。

使用 phandle
**************

.. note::

   本节
   中
   的
   "类型"
   指
   设备树
   绑定
   文档
   :ref:`dt-bindings-properties` 中
   记录
   的
   类型
   名称
   之一。

以下是
你
将
使用
phandle 的
主要
方式。

一个
节点：
phandle 类型
=====================

你可以
使用
phandle
从
``node-a`` 引用
``node-b``，
其中
``node-b``
以
某种
方式
与
``node-a`` 相关。

一个
常见
示例
是
``node-a`` 代表
生成
中断
的
某些
硬件，
``node-b`` 代表
接收
被
置位
中断
的
中断
控制器。
在
这种
情况
下，
你可以
编写：

.. code-block:: DTS

   node_b: node-b {
           interrupt-controller;
   };

   node-a {
           interrupt-parent = <&node_b>;
   };

这
使用
设备树
规范
中
定义
的
标准
``interrupt-parent`` 属性
来
捕获
两个
节点
之间
的
关系。

这些
属性
类型
为
``phandle``。

零
个
或
多个
节点：
phandles 类型
=================================

你可以
使用
phandle
创建
引用
其他
节点
的
数组。

一个
常见
示例
出现在
:ref:`引脚
控制 <pinctrl-guide>` 中。
引脚
控制
属性
如
``pinctrl-0``、``pinctrl-1`` 等
可能
包含
多个
phandle，
每个
"指向"
包含
与
该
硬件
外设
引脚
配置
相关
信息
的
节点。
以下是
单个
属性
中
六个
phandle 的
示例：

.. code-block:: DTS

   pinctrl-0 = <&quadspi_clk_pe10 &quadspi_ncs_pe11
               &quadspi_bk1_io0_pe12 &quadspi_bk1_io1_pe13
               &quadspi_bk1_io2_pe14 &quadspi_bk1_io3_pe15>;

这些
属性
类型
为
``phandles``。

带
元
数据
的
零
个
或
多个
节点：
phandle-array 类型
===================================================

你可以
使用
phandle
引用
并
配置
一个
或
多个
由
其他
节点
"拥有"
的
资源。

这是
最
复杂
的
情况。
下一节
有
示例
和
更多
细节。

这些
属性
类型
为
``phandle-array``。

.. _dt-phandle-arrays:

phandle-array 属性
************************

这些
属性
通常
用于
指定
由
另一个
节点
拥有
的
资源
以及
关于
该
资源
的
附加
元
数据。

高层
描述
=====================

通常，
这种
类型
的
属性
写
得
像
此
示例
中
的
``phandle-array-prop``：

.. code-block:: dts

   node {
           phandle-array-prop = <&foo 1 2>, <&bar 3>, <&baz 4 5>;
   };

即，
属性
值
写
为
逗号
分隔
的
"组"
序列，
每个
"组"
写
在
尖
括号
（``< ... >``）
内。
每个
"组"
以
一个
phandle
（``&foo``、``&bar``、``&baz``）
开头。
每个
"组"
中
phandle
之后
的
值
称为
*说明符*。
上面
示例
有
三个
说明符：

#. ``1 2``
#. ``3``
#. ``4 5``

每个
"组"
中
的
phandle
用于
"指向"
控制
你
感兴趣
的
资源
的
硬件。
说明符
描述
资源
本身，
连同
任何
必要的
附加
元
数据。

本节
其余
部分
描述
一个
常见
示例。
后续
部分
记录
实践
中
如何
使用
phandle-array 属性
的
更多
规则。

示例
phandle-array：
GPIO
=============================

phandle-array 属性
最
常见
的
使用
场景
是
指定
SoC 上
一个
或
多个
GPIO，
开发板
上
的
另一个
芯片
连接
到
这些
GPIO。
因此，
这里
我们
聚焦
该
使用
场景。
不过，
**还有
许多
其他
使用
场景**
在
设备树
中
通过
phandle-array 属性
处理。

例如，
考虑
一个
外部
芯片，
其
中断
引脚
连接
到
SoC 上
的
GPIO。
你
通常
需要
向
该
芯片
的
:ref:`设备
驱动
<device_model_api>`
提供
该
GPIO 的
信息
（GPIO 控制器
和
引脚
编号）。
你
通常
还需要
向
驱动
提供
关于
GPIO 的
其他
元
数据，
如
它是
低
电平
有效
还
是
高
电平
有效、
应
启用
SoC 内
哪种
内部
上拉
电阻
才能
与
设备
通信
等。

在
设备树
中，
将
有一个
代表
控制
一组
引脚
的
GPIO 控制器
的
节点。
这
反映
GPIO IP 块
通常
在
硬件
中
的
开发
方式。
因此，
设备树
中
没有
单个
代表
GPIO 引脚
的
节点，
你
不能
使用
单个
phandle
代表
它。

相反，
你会
使用
phandle-array 属性，
如下
所示：

.. code-block::

   my-external-ic {
           irq-gpios = <&gpioX pin flags>;
   };

此
示例
中，
``irq-gpios`` 是
一个
phandle-array 属性，
其
值
只有
一个
"组"。
``&gpioX`` 是
控制
该
引脚
的
GPIO 控制器
节点
的
phandle。
``pin`` 是
引脚
编号
（0、1、2、...）。
``flags`` 是
描述
引脚
元
数据
的
位
掩码
（例如
``(GPIO_ACTIVE_LOW |
GPIO_PULL_UP)``）；
更多
细节
见
:zephyr_file:`include/zephyr/dt-bindings/gpio/gpio.h`。

处理
``my-external-ic`` 节点
的
设备
驱动
然后
可以
使用
``irq-gpios`` 属性
的
值
为
芯片
设置
中断
处理，
如
其
在
开发板
上
使用
的
方式。
这
允许
你
在
设备树
中
配置
设备
驱动，
而
不
更改
驱动
的
源
代码。

这类
属性
也
可以
包含
多个
值：

.. code-block::

   my-other-external-ic {
           handshake-gpios = <&gpioX pinX flagsX>, <&gpioY pinY flagsY>;
   };

上面
示例
指定
两个
引脚：

- phandle
  为
  ``&gpioX`` 的
  GPIO 控制器
  上
  的
  ``pinX``，
  标志
  ``flagsX``
- ``&gpioY`` 上
  的
  ``pinY``，
  标志
  ``flagsY``

你
可能
会
好奇
"引脚
和
标志"
约定
如何
建立
和
强制
执行。
要
回答
这个
问题，
我们
需要
在
继续
一些
关于
设备树
绑定
的
信息
之前
引入
一个
称为
说明符
空间
的
概念。

.. _dt-specifier-spaces:

说明符
空间
****************

*说明符
空间*
是
一种
允许
节点
描述
你
应
如何
在
phandle-array 属性
中
使用
它们
的
方式。

我们
从
DTS 文件
中
说明符
空间
如何
工作
的
抽象
高层
描述
开始，
然后
转向
一个
具体
示例
并
提供
参考，
了解
使用
DTS 文件
和
绑定
文件
在
实践
中
这一切
如何
工作。

高层
描述
=====================

如上
所述，
phandle-array 属性
是
"组"
的
序列，
每个
phandle
之后
跟
若干
单元格：

.. code-block:: dts

   node {
           phandle-array-prop = <&foo 1 2>, <&bar 3>;
   };

每个
phandle
之后
的
单元格
称为
*说明符*。
此
示例
中，
有
两个
说明符：

#. ``1 2``：
   两个
   单元格
#. ``3``：
   一个
   单元格

每个
phandle-array 属性
有
一个
关联
的
*说明符
空间*。
这
听
起来
复杂，
但
它
其实
只是
一种
以
硬件
特定
方式
为
每个
phandle
之后
的
单元格
分配
含义
的
方式。
每个
说明符
空间
有
唯一
名称。
常用
硬件
有
几个
"标准"
名称，
但
你
也
可以
创建
自己
的。

设备树
节点
通过
名称
使用
``#SPACE_NAME-cells`` 属性
编码
说明符
中
必须
出现
的
单元格
数量。
例如，
假设
``phandle-array-prop`` 的
说明符
空间
名为
``baz``。
那么
``foo`` 和
``bar`` 节点
需要
有
以下
``#baz-cells`` 属性：

.. code-block:: DTS

   foo: node@1000 {
           #baz-cells = <2>;
   };

   bar: node@2000 {
           #baz-cells = <1>;
   };

没有
``#baz-cells`` 属性，
设备树
工具
将
无法
验证
``phandle-array-prop`` 中
每个
说明符
的
单元格
数量。

这种
灵活性
允许
你
在
单个
设备树
属性
中
写下
硬件
资源
数组，
即使
描述
每个
资源
所需
的
元
数据
量
对
不同
节点
可能
不同。

单个
节点
也
可以
在
不同
说明符
空间
中
有
不同
数量
的
单元格。
例如，
我们
可能
有：

.. code-block:: DTS

   foo: node@1000 {
           #baz-cells = <2>;
           #bob-cells = <1>;
   }


有了
它，
如果
``phandle-array-prop-2`` 有
说明符
空间
``bob``，
我们
可以
编写：

.. code-block:: DTS

   node {
           phandle-array-prop = <&foo 1 2>, <&bar 3>;
           phandle-array-prop-2 = <&foo 4>;
   };

这种
灵活性
允许
你
有
一个
同时
管理
多种
不同
类型
资源
的
节点。
节点
使用
不同
的
``#SPACE_NAME-cells`` 属性
描述
描述
每种
类型
资源
所需
的
元
数据
量
（每种
情况
需要
多少
单元格）。

示例
说明符
空间：
gpio
============================

从
上面
示例，
你
已经
熟悉
一个
说明符
空间
如何
工作：
在
"gpio" 空间
中，
说明符
几乎
总是
有
两个
单元格：

#. 一个
   引脚
   编号
#. 一个
   与
   引脚
   相关
   的
   标志
   位
   掩码

因此，
实践
中
你
将
看到
的
几乎
所有
GPIO 控制器
节点
都
看起来
像
这样：

.. code-block:: DTS

   gpioX: gpio-controller@deadbeef {
           gpio-controller;
           #gpio-cells = <2>;
   };

将
属性
与
说明符
空间
关联
********************************************

上面，
我们
描述
了：

- 每个
  phandle-array 属性
  有
  一个
  关联
  说明符
  空间
- 说明符
  空间
  通过
  名称
  标识
- 设备树
  节点
  使用
  ``#SPECIFIER_NAME-cells`` 属性
  配置
  说明符
  中
  必须
  出现
  的
  单元格
  数量

本节
解释
phandle-array 属性
如何
获得
其
说明符
空间。

高层
描述
=====================

一般
而言，
名为
``foos`` 的
``phandle-array`` 属性
隐式
有
说明符
空间
``foo``。
例如：

.. code-block:: YAML

   properties:
     dmas:
       type: phandle-array
     pwms:
       type: phandle-array

``dmas`` 属性
的
说明符
空间
是
"dma"。
``pwms`` 属性
的
说明符
空间
是
``pwm``。

特殊
情况：
GPIO 和
IO 通道
===================================

``*-gpios`` 和
``*-io-channels`` 属性
被
特殊
处理，
使
例如
``foo-gpios`` 和
``bar-io-channels`` 分别
解析
为
``#gpio-cells`` 和
``#io-channel-cells``，
而非
``#foo-gpio-cells`` 和
``#bar-io-channel-cells``。

手动
指定
空间
===========================

你可以
手动
指定
任何
``phandle-array`` 属性
的
说明符
空间。
见
:ref:`dt-bindings-specifier-space`。

为
说明符
中
的
单元格
命名
*******************************

编写
绑定时，
你
应
为
硬件
支持
的
每个
说明符
空间
中
的
单元格
命名。
如何
做
的
细节
见
:ref:`dt-bindings-cells`。

这
允许
C 代码
使用
以下
设备树
API
等
按
名称
查询
说明符
中
单元格
的
信息
并
获取
其
值：

- :c:macro:`DT_PHA_BY_IDX`
- :c:macro:`DT_PHA_BY_NAME`

这个
功能
和
这些
宏
被
众多
硬件
特定
API 内部
使用。
以下是
几个
示例：

- :c:macro:`DT_GPIO_PIN_BY_IDX`
- :c:macro:`DT_PWMS_CHANNEL_BY_IDX`
- :c:macro:`DT_DMAS_CELL_BY_NAME`
- :c:macro:`DT_IO_CHANNELS_INPUT_BY_IDX`
- :c:macro:`DT_CLOCKS_CELL_BY_NAME`

另见
********

- :ref:`dt-writing-property-values`：
  如何
  在
  设备树
  属性
  中
  编写
  phandle

- :ref:`dt-bindings-properties`：
  如何
  为
  phandle 类型
  （``phandle``、``phandles``、``phandle-array``）
  的
  属性
  编写
  绑定

- :ref:`dt-bindings-specifier-space`：
  如何
  手动
  指定
  phandle-array 属性
  的
  说明符
  空间

- :ref:`dt-bindings-dependency-mode`：
  如何
  使用
  phandle 属性
  控制
  节点
  依赖
