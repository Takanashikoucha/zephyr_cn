.. _dt-syntax:

语法与结构
####################

顾名思义，设备树是一棵树。
这棵树的
人类可读
文本格式
称为 DTS（devicetree source，
设备树源），
定义在
`设备树规范`_ 中。

.. _设备树规范: https://www.devicetree.org/

本页的目的是
以比规范
更渐进的方式
介绍设备树。
不过，
你可能
仍需
参考规范
才能
理解
一些
详细
情况。

.. contents:: 目录
   :local:

示例
*******

以下是一个示例 DTS 文件：

.. code-block:: devicetree

   /dts-v1/;

   / {
           a-node {
                   subnode_nodelabel: a-sub-node {
                           foo = <3>;
                   };
           };
   };

``/dts-v1/;`` 行
意味着
文件
内容
在
DTS
语法
版本
1 中，
它
已
取代
现在
过时
的
"版本 0"。

节点
*****

与
任何
树
数据结构
一样，
设备树
有
*节点*
的
层次
结构。
上面
的
树
有
三个
节点：

#. 一个
   根
   节点：``/``
#. 一个
   名为
   ``a-node`` 的
   节点，
   是
   根
   节点
   的
   子
   节点
#. 一个
   名为
   ``a-sub-node`` 的
   节点，
   是
   ``a-node`` 的
   子
   节点

.. _dt-node-labels:

节点
可以
被
分配
*节点
标签*，
这是
引用
带
标签
节点
的
唯一
简写。
上面，
``a-sub-node`` 有
节点
标签
``subnode_nodelabel``。
一个
节点
可以有
零个、
一个
或
多个
节点
标签。
你可以
使用
节点
标签
在
设备树
其他
地方
引用
该
节点。

设备树
节点
有
*路径*
标识
它们
在
树
中的
位置。
与
Unix
文件系统
路径
一样，
设备树
路径
是
用
斜杠
（``/``）
分隔
的
字符串，
根
节点
的
路径
是
单个
斜杠：``/``。
否则，
每个
节点
的
路径
通过
将
节点
的
祖先
名称
与
节点
自身
名称
拼接、
用
斜杠
分隔
来
形成。
例如，
``a-sub-node`` 的
完整
路径
是
``/a-node/a-sub-node``。

属性
**********

设备树
节点
还可以
有
*属性*。
属性
是
名称/值
对。
属性
值
可以是
任何
字节
序列。
在
某些
情况
下，
值
是
称为
*单元格*
（cell）
的
数组。
单元格
只是
一个
32 位
无符号
整数。

节点
``a-sub-node`` 有
一个
名为
``foo`` 的
属性，
其
值
是
值
为
3 的
单元格。
``foo``
值
的
大小
和
类型
由
DTS 中
的
尖
括号
（``<`` 和
``>``）
暗示。

更多
示例
属性
值
见
下面
的
:ref:`dt-writing-property-values`。

设备树
反映
硬件
****************************

在
实践
中，
设备树
节点
通常
对应
某些
硬件，
节点
层次
结构
反映
硬件
的
物理
布局。
例如，
考虑
一块
开发板，
其
SoC 上
的
I2C 总线
控制器
连接
着
三个
I2C 外设，
如下
所示：

.. figure:: zephyr_dt_i2c_high_level.png
   :alt: 带三个 I2C 外设的开发板表示
   :figclass: align-center

对应
I2C 总线
控制器
和
每个
I2C 外设
的
节点
都会
出现在
设备树
中。
反映
硬件
布局，
I2C 外设
节点
是
总线
控制器
节点
的
子
节点。
表示
其他
类型
硬件
的
类似
约定
也
存在。

DTS
看起来
类似
这样：

.. code-block:: devicetree

   /dts-v1/;

   / {
           soc {
                   i2c-bus-controller {
                           i2c-peripheral-1 {
                           };
                           i2c-peripheral-2 {
                           };
                           i2c-peripheral-3 {
                           };
                   };
           };
   };

实践中的属性
**********************

在
实践
中，
属性
通常
描述
或
配置
节点
所
代表
的
硬件。
例如，
I2C 外设
的
节点
有
一个
属性，
其
值
是
外设
在
总线
上
的
地址。

这里
是
一个
表示
相同
示例
的
树，
但
带有
处理
I2C 设备
时
可能
看到
的
真实
世界
节点
名称
和
属性。

.. figure:: zephyr_dt_i2c_example.png
   :figclass: align-center

   带真实世界名称和属性的 I2C 设备树示例。
   节点名称位于每个节点顶部，灰色背景。
   属性显示为"名称=值"行。

这是
对应的
DTS：

.. code-block:: devicetree

   /dts-v1/;

   / {
           soc {
                   i2c@40003000 {
                           compatible = "nordic,nrf-twim";
                           reg = <0x40003000 0x1000>;

                           apds9960@39 {
                                   compatible = "avago,apds9960";
                                   reg = <0x39>;
                           };
                           ti_hdc@43 {
                                   compatible = "ti,hdc", "ti,hdc1010";
                                   reg = <0x43>;
                           };
                           mma8652fc@1d {
                                   compatible = "nxp,fxos8700", "nxp,mma8652fc";
                                   reg = <0x1d>;
                           };
                   };
           };
   };

.. _dt-unit-address:

单元地址
**************

除了
展示
更多
真实
世界
名称
和
属性
外，
上面
的
示例
引入
了
一个
新的
设备树
概念：
单元
地址。
单元
地址
是
节点
名称
中
"at"
符号
（``@``）
之后
的
部分，
如
``i2c@40003000`` 中
的
``40003000``，
或
``apds9960@39`` 中
的
``39``。
单元
地址
是
可选
的：
``soc`` 节点
没有
一个。

在
设备树
中，
单元
地址
给出
节点
在其
父
节点
地址
空间
中
的
地址。
以下是
不同
类型
硬件
的
一些
示例
单元
地址。

内存
映射
外设
    外设
    寄存器
    映射
    基
    地址。
    例如，
    名为
    ``i2c@40003000`` 的
    节点
    代表
    一个
    I2C 控制器，
    其
    寄存器
    映射
    基
    地址
    是
    0x40003000。

I2C 外设
    外设
    在
    I2C 总线
    上
    的
    地址。
    例如，
    上一节
    I2C 控制器
    的
    子
    节点
    ``apds9960@39`` 的
    I2C 地址
    是
    0x39。

SPI 外设
    表示
    外设
    片
    选
    线
    编号
    的
    索引。
    （如果
    没有
    片
    选
    线，
    使用
    0。）

内存
    物理
    起始
    地址。
    例如，
    名为
    ``memory@2000000`` 的
    节点
    代表
    从
    物理
    地址
    0x2000000 开始
    的
    RAM。

内存
映射
flash
    与
    RAM 一样，
    物理
    起始
    地址。
    例如，
    名为
    ``flash@8000000`` 的
    节点
    代表
    物理
    起始
    地址
    为
    0x8000000 的
    flash 设备。

固定
flash 分区
    当
    设备树
    用于
    存储
    flash 分区
    表
    时
    适用。
    单元
    地址
    是
    分区
    在
    flash 内存
    中
    的
    起始
    偏移。
    例如，
    考虑
    这个
    flash 设备
    及其
    分区：

    .. code-block:: devicetree

       flash@8000000 {
           /* ... */
           partitions {
                   partition@0 { /* ... */ };
                   partition@20000 {  /* ... */ };
                   /* ... */
           };
       };

    名为
    ``partition@0`` 的
    节点
    与其
    flash
    设备
    起始
    的
    偏移
    为
    0，
    因此
    其
    基
    地址
    是
    0x8000000。
    类似
    地，
    名为
    ``partition@20000`` 的
    节点
    的
    基
    地址
    是
    0x8020000。

.. _dt-important-props:

重要属性
********************

.. 文档维护者：如果你向此列表添加属性，
   确保它也从 gen_devicetree_rest.py 链接过来。

设备树
规范
定义
了
几个
标准
属性。
一些
最
重要
的
是：

compatible
    节点
    所
    代表
    硬件
    设备
    的
    名称。

    推荐
    格式
    是
    ``"vendor,device"``，
    如
    ``"avago,apds9960"``，
    或
    这些
    的
    序列，
    如
    ``"ti,hdc", "ti,hdc1010"``。
    ``vendor``
    部分
    是
    厂商
    的
    缩写
    名称。
    文件
    :zephyr_file:`dts/bindings/vendor-prefixes.txt` 包含
    一个
    通常
    接受
    的
    ``vendor`` 名称
    列表。
    ``device`` 部分
    通常
    取自
    数据
    手册。

    当
    硬件
    行为
    是
    通用
    的
    时，
    它
    也
    有时
    是
    像
    ``gpio-keys``、``mmio-sram`` 或
    ``fixed-clock`` 这样
    的
    值。

    构建
    系统
    使用
    compatible 属性
    查找
    节点
    的
    正确
    :ref:`绑定 <dt-bindings>`。
    设备
    驱动
    使用
    ``devicetree.h`` 查找
    具有
    相关
    compatible 的
    节点，
    以
    确定
    可
    管理
    的
    可用
    硬件。

    ``compatible`` 属性
    可以
    有
    多个
    值。
    当
    设备
    是
    更
    通用
    家族
    的
    特定
    实例
    时，
    额外
    值
    很有
    用，
    允许
    系统
    从
    最
    特定
    到
    最不
    特定
    匹配
    设备
    驱动。

    在
    Zephyr 的
    绑定
    语法
    中，
    此
    属性
    类型
    为
    ``string-array``。

reg
    用于
    寻址
    设备
    的
    信息。
    值
    特定
    于
    设备
    （即
    根据
    compatible 属性
    不同）。

    ``reg`` 属性
    是
    ``(address, length)``
    对
    的
    序列。
    每个
    对
    称为
    "寄存器
    块"。
    值
    按
    惯例
    用
    十六
    进制
    书写。

    以下是
    一些
    常见
    模式：

    - 通过
      内存
      映射
      I/O 寄存器
      访问
      的
      设备
      （如
      ``i2c@40003000``）：
      ``address`` 通常
      是
      I/O 寄存器
      空间
      的
      基
      地址，
      ``length`` 是
      寄存器
      占用
      的
      字节
      数。
    - I2C 设备
      （如
      ``apds9960@39`` 及其
      兄弟
      节点）：
      ``address`` 是
      I2C 总线
      上
      的
      从
      地址。
      没有
      ``length`` 值。
    - SPI 设备：``address`` 是
      片
      选
      线
      编号；
      没有
      ``length``。

    你可能
    会
    注意
    到
    ``reg`` 属性
    与
    上面
    描述
    的
    常见
    单元
    地址
    之间
    的
    一些
    相似
    之处。
    这
    不是
    巧合。
    ``reg`` 属性
    可以
    看作
    比
    单元
    地址
    更
    详细
    的
    设备
    内
    可
    寻址
    资源
    的
    视图。

status
    描述
    节点
    是否
    启用
    的
    字符串。

    设备树
    规范
    允许
    此
    属性
    有
    ``"okay"``、``"disabled"``、``"reserved"``、``"fail"`` 和
    ``"fail-sss"`` 值。
    Zephyr 将
    任何
    非
    ``"okay"`` 值
    视为
    禁用。
    特别是，
    ``"reserved"`` 用于
    记录
    节点
    存在
    但
    在
    其他
    地方
    启用
    （例如
    多
    域
    应用
    中
    由
    另一个
    核心
    或
    域
    启用）；
    它
    由
    ``edtlib`` 以
    与
    ``"disabled"`` 相同
    的
    方式
    处理。
    其余
    值
    （``"fail"`` 和
    ``"fail-sss"``）的
    使用
    目前
    未被
    Zephyr 使用。

    如果
    节点
    的
    status 属性
    是
    ``"okay"`` 或
    未
    定义
    （即
    不
    存在
    于
    设备树
    源
    中），
    则
    该
    节点
    被视为
    启用。
    status 为
    ``"disabled"`` 的
    节点
    被
    显式
    禁用。
    对应
    物理
    设备
    的
    设备树
    节点
    必须
    启用，
    Zephyr 驱动
    模型
    中
    对应的
    ``struct device`` 才会
    被
    分配
    和
    初始化。

    注意
    当
    父
    节点
    被
    禁用
    时，
    子
    节点
    不
    会
    被
    隐式
    禁用，
    即
    如果
    需要，
    子
    节点
    应
    被
    显式
    禁用。

interrupts
    设备
    生成
    的
    中断
    的
    信息，
    编码
    为
    一个
    或
    多个
    *中断
    说明符*
    的
    数组。
    每个
    中断
    说明符
    有
    若干
    单元格。
    更多
    细节
    见
    `设备树
    规范
    release v0.3`_
    第
    2.4 节，
    *Interrupts and Interrupt Mapping*
    （中断
    和
    中断
    映射）。

.. _设备树规范release-v0.3:
   https://www.devicetree.org/specifications/

.. highlight:: none

.. note::

   早期
   版本
   的
   Zephyr 经常
   使用
   ``label`` 属性，
   它
   与
   标准
   :ref:`节点
   标签 <dt-node-labels>` 不同。
   在
   新
   设备树
   绑定
   中
   使用
   label*属性*，
   以及
   在
   新
   代码
   中
   使用
   :c:macro:`DT_LABEL` 宏，
   被
   积极
   不
   推荐。
   出于
   历史
   原因，
   label
   属性
   继续
   存在
   于
   某些
   现有
   绑定
   和
   覆盖
   中，
   但
   不应
   在
   新
   绑定
   或
   设备
   实现
   中
   使用。

.. _dt-writing-property-values:

编写属性值
***********************

本节
描述
如何
在
DTS 格式
中
编写
属性
值。
下面
表格
中
的
属性
类型
在
:ref:`dt-bindings` 中
详细
描述。

为
保持
简单，
跳过
了
一些
具体
内容；
如果
你
对
细节
好奇，
见
设备树
规范。

.. list-table::
   :header-rows: 1
   :widths: 1 4 4

   * - 属性
     类型
     - 如何
     编写
     - 示例

   * - string
     - 双
     引号
     - ``a-string = "hello, world!";``

   * - int
     - 尖
     括号
     （``<`` 和
     ``>``）
     之间
     - ``an-int = <1>;``

   * - boolean
     - 为
     ``true`` 时
     无
     值
     （为
     ``false``，
     使用
     ``/delete-property/``）
     - ``my-true-boolean;``

   * - array
     - 尖
     括号
     （``<`` 和
     ``>``）
     之间，
     用
     空格
     分隔
     - ``foo = <0xdeadbeef 1234 0>;``

   * - uint8-array
     - 十六
     进制
     *无*
     前导
     ``0x``，
     方
     括号
     （``[`` 和
     ``]``）
     之间。
     - ``a-byte-array = [00 01 ab];``

   * - string-array
     - 用
     逗号
     分隔
     - ``a-string-array = "string one", "string two", "string three";``

   * - phandle
     - 尖
     括号
     （``<`` 和
     ``>``）
     之间
     - ``a-phandle = <&mynode>;``

   * - phandles
     - 尖
     括号
     （``<`` 和
     ``>``）
     之间，
     用
     空格
     分隔
     - ``some-phandles = <&mynode0 &mynode1 &mynode2>;``

   * - phandle-array
     - 尖
     括号
     （``<`` 和
     ``>``）
     之间，
     用
     空格
     分隔
     - ``a-phandle-array = <&mynode0 1 2>, <&mynode1 3 4>;``

上面
的
附加
说明：

- ``phandle``、``phandles`` 和
  ``phandle-array`` 类型
  中
  的
  值
  在
  :ref:`dt-phandles` 中
  进一步
  描述

- 布尔
  属性
  存在
  即
  为
  真。
  它
  不应
  有
  值。
  布尔
  属性
  只有
  在
  DTS 中
  完全
  缺失
  时
  才
  为
  假。

- 上面
  的
  ``foo`` 属性
  值
  有
  三个
  *单元格*，
  值
  依次
  为
  0xdeadbeef、1234 和
  0。
  注意
  允许
  十六
  进制
  和
  十
  进制
  数字
  且
  可以
  混合
  使用。
  由于
  Zephyr 将
  DTS 转换
  为
  C 源
  代码，
  这里
  不
  需要
  指定
  单个
  单元格
  的
  字节
  序。

- 64 位
  整数
  写
  为
  两个
  32 位
  单元格，
  大
  端
  顺序。
  值
  0xaaaa0000bbbb1111 写
  为
  ``<0xaaaa0000 0xbbbb1111>``。

- ``a-byte-array`` 属性
  值
  是
  三个
  字节
  0x00、0x01 和
  0xab，
  依次
  排列。

- 允许
  圆
  括号、
  算术
  运算符
  和
  按
  位
  运算符。
  ``bar`` 属性
  包含
  一个
  值
  为
  64 的
  单元格：

  .. code-block:: devicetree

     bar = <(2 * (1 << 5))>;

  注意
  整个
  表达式
  必须
  用
  圆
  括号
  括
  起来。

- 圆
  括号
  表达式
  求
  值
  为
  负
  值
  的
  单元格，
  如
  ``<(-1)>`` 或
  ``<(4 - 6)>``，
  对
  ``int`` 和
  ``array`` 类型
  属性
  保留
  为
  有
  符号
  值。
  写
  为
  正
  十
  进制
  或
  十六
  进制
  字面
  量
  （包括
  ``0xffffffff``）
  或
  表达式
  求
  值
  为
  非
  负
  值
  的
  单元格
  保持
  无
  符号。

- 属性
  值
  通过
  *phandle*
  引用
  设备树
  中
  的
  其他
  节点。
  你可以
  使用
  ``&foo`` 编写
  phandle，
  其中
  ``foo`` 是
  :ref:`节点
  标签
  <dt-node-labels>`。
  以下是
  一个
  示例
  设备树
  片段：

  .. code-block:: devicetree

     foo: device@0 { };
     device@1 {
             sibling = <&foo 1 2>;
     };

  节点
  ``device@1`` 的
  ``sibling`` 属性
  包含
  三个
  单元格，
  按
  此
  顺序：

  #. ``device@0`` 节点
     的
     phandle，
     这里
     写
     为
     ``&foo``，
     因为
     ``device@0`` 节点
     有
     节点
     标签
     ``foo``
  #. 值
     1
  #. 值
     2

  在
  设备树
  中，
  phandle 值
  是
  一个
  单元格
  --
  再次
  只是
  一个
  32 位
  无
  符号
  int。
  不过，
  Zephyr 设备树
  API 通常
  将
  这些
  值
  暴露
  为
  *节点
  标识符*。
  节点
  标识符
  在
  :ref:`dt-from-c` 中
  更
  详细
  地
  介绍。

- 数组
  和
  类似
  类型
  属性
  值
  可以
  拆分
  为
  若干
  ``<>``
  块，
  如下
  所示：

  .. code-block:: devicetree

     foo = <1 2>, <3 4>;                         // 'type: array' 可用
     foo = <&label1 &label2>, <&label3 &label4>; // 'type: phandles' 可用
     foo = <&label1 1 2>, <&label2 3 4>;         // 'type: phandle-array' 可用

  如果
  值
  可以
  逻辑
  分组
  为
  子
  值
  块，
  可能
  时
  为
  可
  读性
  推荐
  此
  方式。

.. _dt-alias-chosen:

别名与 chosen 节点
************************

除
:ref:`节点
标签 <dt-node-labels>` 外，
还有
两种
额外
方式
可以
不
指定
完整
路径
而
引用
特定
节点：
通过
别名，
或
通过
chosen 节点。

以下是
一个
同时
使用
两者
的
示例
设备树：

.. code-block:: devicetree

   /dts-v1/;

   / {
   	chosen {
   		zephyr,console = &uart0;
        };

   	aliases {
   		my-uart = &uart0;
   	};

   	soc {
   		uart0: serial@12340000 {
   			...
   		};
   	};
   };

``/aliases`` 和
``/chosen`` 节点
不
引用
实际
硬件
设备。
它们
的
目的
是
指定
设备树
中
的
其他
节点。

上面，
``my-uart`` 是
路径
为
``/soc/serial@12340000`` 的
节点
的
别名。
使用
其
节点
标签
``uart0``，
相同
的
节点
被
设置
为
chosen
``zephyr,console`` 节点
的
值。

Zephyr 示例
应用
有时
使用
别名
允许
以
通用
方式
覆盖
应用
使用
的
特定
硬件
设备。
例如，
:zephyr:code-sample:`blinky` 使用
它
通过
``led0`` 别名
抽象
要
闪烁
的
LED。

``/chosen`` 节点
的
属性
用于
配置
系统
或
子系统
范围
的
值。
更多
信息
见
:ref:`devicetree-chosen-nodes`。
