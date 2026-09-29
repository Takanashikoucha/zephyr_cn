.. _kconfig_tips_and_tricks:

Kconfig - 技巧与最佳实践
#################################

本页
覆盖
一些
Kconfig 最佳
实践
并
解释
一些
Kconfig
行为
和
功能，
它们
可能
晦涩
或
容易
被
忽略。

.. note::

   官方
   Kconfig 文档
   是
   `kconfig-language.rst
   <https://www.kernel.org/doc/html/latest/kbuild/kconfig-language.html>`__
   和
   `kconfig-macro-language.rst
   <https://www.kernel.org/doc/html/latest/kbuild/kconfig-macro-language.html>`__。

.. contents::
   :local:
   :depth: 2


什么
应该
变成
Kconfig 选项
*********************************

决定
某事
是否
属于
Kconfig
时，
区分
有
prompt
的
符号
和
没有
的
符号
很有
帮助。

如果
符号
有
prompt（例如
``bool "Enable foo"``），
那么
用户
可以
在
``menuconfig`` 或
``guiconfig`` 接口
（见
:ref:`menuconfig`）
中
更改
符号
的
值，
或
通过
手动
编辑
配置
文件。
相反，
没有
prompt
的
符号
永远
不
能
被
用户
直接
更改，
即使
通过
手动
编辑
配置
文件。

只
在
用户
更改
其
值
有意义
时
才
给
符号
加
prompt。

没有
prompt
的
符号
称为
*隐藏*
或
*不可见*
符号，
因为
它们
不
显示
在
``menuconfig`` 和
``guiconfig`` 中。
有
prompt
的
符号
也
可以
不可见，
当
其
依赖
未
满足
时。

没有
prompt
的
符号
不
能
被
用户
直接
配置
（它们
的
值
来自
其他
符号），
因此
对
它们
适用
的
限制
更少。
如果
某个
派生
设置
在
Kconfig 中
计算
比
例如
在
构建
期间
更
容易，
那么
在
Kconfig 中
做，
但
记住
有
prompt
和
没有
prompt
的
符号
之间
的
区别。

见
`optional prompts`_ 章节
了解
处理
某些
机器
上
固定
而
其他
机器
上
可
配置
的
设置
的
方式。

什么
不应
变成
Kconfig 选项
*************************************

在
Zephyr 中，
Kconfig 配置
在
选择
目标
开发板
后
完成。
一般
来说，
使用
Kconfig 处理
对应
固定
的
机器
特定
设置
的
值
没有
意义。
通常，
这种
设置
应该
通过
:ref:`设备树 <dt-guide>` 处理。

特别
避免
添加
以下
类型
的
新
Kconfig 选项：

指定
系统中
设备
名称
的
选项
===================================================

例如，
如果
你
在
编写
I2C 设备
驱动，
避免
创建
名为
``MY_DEVICE_I2C_BUS_NAME`` 的
选项
来
指定
控制
你的
设备
的
总线
节点。
替代
方案
见
:ref:`dt-drivers-that-depend`。

类似
地，
如果
你的
应用
依赖
硬件
特定
的
PWM 设备
来
控制
RGB LED，
避免
创建
像
``MY_PWM_DEVICE_NAME`` 这样
的
选项。
替代
方案
见
:ref:`dt-apps-that-depend`。

指定
固定
硬件
配置
的
选项
================================================

例如，
避免
指定
GPIO 引脚
的
Kconfig 选项。

适用于
设备
驱动
的
替代
方案
是
在
设备
绑定
中
定义
类型
为
phandle-array 的
GPIO
说明符，
并从
C 使用
:ref:`devicetree-gpio-api` 设备树
API。
类似
的
建议
适用
于
其他
devicetree.h 提供
:ref:`devicetree-hw-api` 引用
系统中
其他
节点
的
情况。
在
源
代码
中
搜索
使用
这些
API 的
驱动
查找
示例。

应用
特定
的
设备树
:ref:`绑定 <dt-bindings>`
来
标识
开发板
特定
属性
可能
合适。
示例
见
:zephyr_file:`tests/drivers/gpio/gpio_basic_api`。

对于
应用，
设备树
基础
的
替代
方案
见
:zephyr:code-sample:`blinky`。

``select`` 语句
*********************

``select`` 语句
用于
每当
另一个
符号
为
``y`` 时
强制
一个
符号
为
``y``。
例如，
以下
代码
每当
``USB_CONSOLE`` 为
``y`` 时
强制
``CONSOLE`` 为
``y``：

.. code-block:: kconfig

   config CONSOLE
   	bool "Console support"

   ...

   config USB_CONSOLE
   	bool "USB console support"
   	select CONSOLE

本节
覆盖
``select`` 的
一些
陷阱
和
好
用途。


``select`` 陷阱
==================

``select``
起初
可能
看起来
是
一个
通用
有用
的
功能，
但
过度
使用
会
导致
配置
问题。

例如，
假设
上面
的
``CONSOLE`` 符号
被
一个
不
了解
``USB_CONSOLE`` 符号
（或
简单
忘记
它）
的
开发者
添加
了
新的
依赖：

.. code-block:: kconfig

   config CONSOLE
   	bool "Console support"
   	depends on STRING_ROUTINES

现在
启用
``USB_CONSOLE`` 会
强制
``CONSOLE`` 为
``y``，
即使
``STRING_ROUTINES`` 为
``n``。

要
修复
问题，
``STRING_ROUTINES`` 依赖
需要
也
添加
到
``USB_CONSOLE``：

.. code-block:: kconfig

   config USB_CONSOLE
   	bool "USB console support"
   	select CONSOLE
   	depends on STRING_ROUTINES

   ...

   config STRING_ROUTINES
   	bool "Include string routines"

从
``if`` 和
``menu`` 语句
继承
的
依赖
的
更
阴险
的
情况
很
常见。

解决
问题
的
另一种
尝试
可能
是
将
``depends on`` 变成
另一个
``select``：

.. code-block:: kconfig

   config CONSOLE
   	bool "Console support"
   	select STRING_ROUTINES

   ...

   config USB_CONSOLE
   	bool "USB console support"
   	select CONSOLE

实践
中，
这
通常
放大
问题，
因为
添加
到
``STRING_ROUTINES`` 的
任何
依赖
现在
需要
复制
到
``CONSOLE`` 和
``USB_CONSOLE`` 两者。

一般
来说，
每当
符号
的
依赖
更新
时，
所有
（直接
或
间接）
select
它的
符号
的
依赖
也
必须
更新。
这
在
实践
中
非常
经常
被
忽略，
即使
对于
上面
最
简单
的
情况。

符号
相互
select
的
链
应该
特别
避免，
除了
下面
:ref:`good_select_use` 中
覆盖
的
简单
辅助
符号。

``select`` 的
滥用
也
倾向
使
Kconfig 文件
更
难
阅读，
既
因为
额外
的
依赖，
也
因为
``select`` 的
非
局部
性质，
它
隐藏
了
符号
可能
被
启用
的
方式。


``select`` 的
替代
方案
==========================

对于
上一节
的
示例，
更好
的
解决
方案
通常
是
将
``select`` 变成
``depends on``：

.. code-block:: kconfig

   config CONSOLE
   	bool "Console support"

   ...

   config USB_CONSOLE
   	bool "USB console support"
   	depends on CONSOLE

这
使
生成
无效
配置
变得
不可能，
并
意味着
依赖
永远
只
需要
在
单个
位置
更新。

对
这里
使用
``depends on`` 的
反对
可能
是
启用
``USB_CONSOLE`` 的
配置
文件
现在
也
需要
启用
``CONSOLE``：

.. code-block:: cfg

   CONFIG_CONSOLE=y
   CONFIG_USB_CONSOLE=y

这
归结
为
权衡，
但
如果
启用
``CONSOLE`` 是
常态，
那么
缓解
措施
是
使
``CONSOLE`` 默认
为
``y``：

.. code-block:: kconfig

   config CONSOLE
   	bool "Console support"
   	default y

这
给出
配置
文件
中
只
有
单个
赋值：

.. code-block:: cfg

   CONFIG_USB_CONSOLE=y

注意
不
想要
``CONSOLE`` 启用
的
配置
文件
现在
必须
显式
禁用
它：

.. code-block:: cfg

   CONFIG_CONSOLE=n


.. _good_select_use:

使用
``select`` 处理
辅助
符号
==================================

``select`` 的
一个
好
且
安全
的
用途
是
设置
捕获
某些
条件
的
"辅助"
符号。
这种
辅助
符号
最好
没有
prompt
或
依赖。

例如，
指示
特定
CPU/SoC 有
FPU 的
辅助
符号
可以
定义
如下：

.. code-block:: kconfig

   config CPU_HAS_FPU
   	bool
   	help
   	  If y, the CPU has an FPU

   ...

   config SOC_FOO
       bool
       select CPU_HAS_FPU

   ...

   config SOC_BAR
       bool
       select CPU_HAS_FPU

这
使
其他
符号
可以
以
通用
方式
检查
FPU 支持，
而
不
需要
查找
特定
架构：

.. code-block:: kconfig

   config FPU
   	bool "Support floating point operations"
   	depends on CPU_HAS_FPU

替代
方案
是
有
像
以下
这样
的
依赖，
可能
在
几个
位置
重复：

.. code-block:: kconfig

   config FPU
   	bool "Support floating point operations"
   	depends on SOC_FOO || SOC_BAR || ...

不可见
辅助
符号
没有
``select`` 也
可以
有用。
例如，
以下
代码
定义
一个
如果
机器
有
某些
任意
定义
的
"大"
内存
量
就
有
值
``y`` 的
辅助
符号：

.. code-block:: kconfig

   config LARGE_MEM
   	def_bool MEM_SIZE >= 64

.. note::

   这
   是
   以下
   的
   简写：

   .. code-block:: kconfig

      config LARGE_MEM
      	bool
      	default MEM_SIZE >= 64


``select`` 建议
==========================

总结
来说，
这里
是
``select`` 的
一些
推荐
实践：

- 避免
  select
  有
  prompt
  或
  依赖
  的
  符号。
  偏好
  ``depends on``。
  如果
  ``depends on`` 导致
  配置
  文件
  中
  烦人
  的
  膨胀，
  考虑
  为
  最
  常见
  值
  添加
  Kconfig 默认
  值。

  罕见
  的
  例外
  可能
  包括
  你
  确信
  select
  和
  被
  select
  符号
  的
  依赖
  永远
  不
  会
  失
  同步
  的
  情况，
  例如
  处理
  同一
  ``if`` 中
  定义
  在
  彼此
  附近
  的
  两个
  简单
  符号
  时。

  常识
  适用，
  但
  注意
  ``select`` 在
  实践
  中
  经常
  导致
  问题。
  ``depends on`` 通常
  是
  更
  干净
  且
  更
  安全
  的
  解决
  方案。

- 尽管
  多
  也
  随便
  select
  没有
  prompt
  和
  依赖
  的
  简单
  辅助
  符号。
  它们
  是
  简化
  Kconfig 文件
  的
  好
  工具。

- 一个
  豁免
  是
  I2C 和
  SPI 这样
  的
  总线，
  以及
  遵循
  相同
  思路
  的
  MFD 等。
  这些
  总线
  上
  的
  驱动
  应该
  使用
  ``select`` 允许
  当
  总线
  上
  的
  设备
  在
  设备树
  中
  启用
  时
  自动
  激活
  必要
  的
  总线
  驱动。

.. code-block:: kconfig

   config ADC_FOO
      bool "external SPI ADC foo driver"
      select SPI

（缺少）
条件
包含
******************************

``if`` 块
为
``if`` 内
的
每个
项
添加
依赖，
就像
使用
``depends
on`` 一样。

与
``if`` 相关
的
一个
常见
误解
是
认为
以下
代码
条件
地
包含
文件
:file:`Kconfig.other`：

.. code-block:: kconfig

   if DEP

   source "Kconfig.other"

   endif

实际上，
Kconfig 中
没有
条件
包含。
``if``
在
``source`` 周围
没有
特殊
含义。

.. note::

   条件
   包含
   不可能
   实现，
   因为
   ``if``
   条件
   可能
   （直接
   或
   间接）
   包含
   对
   尚未
   定义
   符号
   的
   前向
   引用。

假设
上面
的
:file:`Kconfig.other` 包含
这个
定义：

.. code-block:: kconfig

   config FOO
   	bool "Support foo"

在
这种
情况
下，
``FOO`` 最终
会有
这个
定义：

.. code-block:: kconfig

   config FOO
   	bool "Support foo"
   	depends on DEP

注意
在
:file:`Kconfig.other` 中
``FOO`` 的
定义
添加
``depends on DEP``
是
冗余
的，
因为
``DEP`` 依赖
已经
被
``if DEP`` 添加。

一般
来说，
尽量
避免
添加
冗余
依赖。
它们
可以
使
Kconfig 文件
的
结构
更
难
理解，
也
使
更改
更
容易
出错，
因为
可能
很
难
发现
相同
的
依赖
被
添加
两次。


.. _stuck_symbols:

menuconfig 和
guiconfig 中
"卡住"
的
符号
*******************************************

与
相互
依赖
的
带
prompt
的
配置
符号
相关
的
一个
常见
微妙
陷阱。
考虑
这些
符号：

.. code-block:: kconfig

   config FOO
   	bool "Foo"

   config STACK_SIZE
   	hex "Stack size"
   	default 0x200 if FOO
   	default 0x100

假设
这里
的
意图
是
每当
``FOO`` 启用
时
使用
更
大
的
栈，
且
配置
初始
时
``FOO`` 禁用。
也
记住
Zephyr 通过
合并
配置
文件
（包括
例如
:file:`prj.conf`）
在
构建
目录
中
的
:file:`zephyr/.config` 创建
初始
配置。
这
个
配置
文件
在
运行
``menuconfig`` 或
``guiconfig`` 之前
就
存在。

首次
进入
配置
接口
时，
``STACK_SIZE`` 的
值
是
0x100，
如
预期。
启用
``FOO`` 后，
你
可能
合理
地
期望
``STACK_SIZE`` 的
值
更改
为
0x200，
但
它
保持
0x100。

要
理解
发生
了
什么，
记住
``STACK_SIZE`` 有
prompt，
意味着
它
是
用户
可
配置
的，
并
考虑
所有
Kconfig 必须
从
初始
配置
继续
的
是
这：

.. code-block:: cfg

   CONFIG_STACK_SIZE=0x100

由于
Kconfig 不
能
知道
0x100 值
来自
``default`` 还是
用户
输入
的，
它
必须
假设
它
来自
用户。
由于
``STACK_SIZE`` 是
用户
可
配置
的，
配置
文件
中
的
值
被
尊重，
任何
符号
默认
值
被
忽略。
这
就是
为什么
``STACK_SIZE`` 的
值
在
切换
``FOO`` 时
看起来
"冻结"
在
0x100。

正确
的
修复
取决于
意图
是
什么。
这里
是
一些
不同
场景
及
建议：

- 如果
  ``STACK_SIZE`` 始终
  可以
  自动
  派生
  且
  不
  需要
  用户
  可
  配置，
  那么
  简单
  移除
  prompt：

  .. code-block:: kconfig

     config STACK_SIZE
     	hex
     	default 0x200 if FOO
     	default 0x100

  没有
  prompt
  的
  符号
  忽略
  保存
  配置
  中
  的
  任何
  值。

- 如果
  ``STACK_SIZE`` 通常
  应该
  用户
  可
  配置，
  但
  当
  ``FOO`` 启用
  时
  需要
  设置
  为
  0x200，
  那么
  当
  ``FOO`` 启用
  时
  禁用
  其
  prompt，
  如
  `optional prompts`_ 中
  所述：

  .. code-block:: kconfig

     config STACK_SIZE
     	hex "Stack size" if !FOO
     	default 0x200 if FOO
     	default 0x100

- 如果
  ``STACK_SIZE`` 通常
  应该
  自动
  派生，
  但
  在
  罕见
  情况
  下
  需要
  设置
  为
  自定义
  值，
  那么
  添加
  另一个
  选项
  使
  ``STACK_SIZE`` 用户
  可
  配置：

  .. code-block:: kconfig

     config CUSTOM_STACK_SIZE
     	bool "Use a custom stack size"
     	help
     	  Enable this if you need to use a custom stack size. When disabled, a
     	  suitable stack size is calculated automatically.

     config STACK_SIZE
     	hex "Stack size" if CUSTOM_STACK_SIZE
     	default 0x200 if FOO
     	default 0x100

  只要
  ``CUSTOM_STACK_SIZE`` 禁用，
  ``STACK_SIZE`` 将
  忽略
  保存
  配置
  中
  的
  值。

在
``menuconfig`` 或
``guiconfig`` 接口
中
试验
更改
是
一个
好
主意，
确保
事情
按
你
期望
的
方式
行为。
做
这些
中等
复杂
的
更改
时
特别
如此。


配置
文件
中
对
无
prompt
符号
的
赋值
********************************************************

配置
文件
中
对
隐藏
（无
prompt，
也
称为
*不可见*）
符号
的
赋值
始终
被
忽略。
隐藏
符号
的
值
间接
来自
其他
符号，
通过
例如
``default`` 和
``select``。

一个
常见
的
混淆
来源
是
打开
输出
配置
文件
（:file:`zephyr/.config`），
看到
一堆
对
隐藏
符号
的
赋值，
并
假设
那些
赋值
必须
在
Kconfig 读
回
配置
时
被
尊重。
实际上，
:file:`zephyr/.config` 中
对
隐藏
符号
的
所有
赋值
被
Kconfig 忽略，
如
其他
配置
文件
一样。

要
理解
为什么
:file:`zephyr/.config` 仍
包含
对
隐藏
符号
的
赋值，
有
帮助
的
是
意识到
:file:`zephyr/.config` 服务
两个
分开
的
目的：

1. 它
   持有
   保存
   的
   配置，
   且

2. 它
   持有
   配置
   输出。
   :file:`zephyr/.config` 被
   CMake 文件
   解析
   以
   允许
   它们
   查询
   配置
   设置，
   例如。

:file:`zephyr/.config` 中
对
隐藏
符号
的
赋值
只是
配置
输出。
Kconfig 本身
在
计算
符号
值
时
忽略
对
隐藏
符号
的
赋值。

.. note::

   *最小
   配置*，
   可以
   从
   :ref:`menuconfig 和
   guiconfig 接口 <menuconfig>` 内
   生成，
   可以
   被认为
   更接近
   只
   是
   保存
   的
   配置，
   没有
   完整
   的
   配置
   输出。


``depends on`` 和
``string``/``int``/``hex`` 符号
*****************************************************

``depends on``
不仅
对
``bool`` 符号
有效，
也
对
``string``、``int`` 和
``hex`` 符号
（以及
choice）
有效。

下面
的
Kconfig 定义
将
在
``FOO_DEVICE`` 禁用
时
隐藏
``FOO_DEVICE_FREQUENCY`` 符号
并
禁用
其
任何
配置
输出。

.. code-block:: kconfig

   config FOO_DEVICE
   	bool "Foo device"

   config FOO_DEVICE_FREQUENCY
   	int "Foo device frequency"
   	depends on FOO_DEVICE

一般
来说，
检查
只有
相关
符号
永远
显示
在
``menuconfig``/``guiconfig`` 接口
中
是
一个
好
主意。
``FOO_DEVICE`` 禁用
（且
可能
隐藏）
时
``FOO_DEVICE_FREQUENCY`` 显示
使
符号
之间
的
关系
更
难
理解，
即使
代码
永远
不
在
``FOO_DEVICE`` 禁用
时
查看
``FOO_DEVICE_FREQUENCY``。


``menuconfig`` 符号
**********************

如果
符号
``FOO`` 的
定义
紧
跟
其他
依赖
``FOO`` 的
符号，
那么
那些
符号
成为
``FOO`` 的
子
项。
如果
``FOO`` 用
``config FOO`` 定义，
那么
子
项
显示
为
相对
于
``FOO`` 缩进。
改为
用
``menuconfig FOO`` 定义
``FOO``
将
子
项
放在
以
``FOO`` 为
根
的
单独
菜单
中。

``menuconfig``
对
求值
没有
影响。
它
只是
一个
显示
选项。

``menuconfig``
可以
减少
菜单
数量
并
使
菜单
结构
更
容易
导航。
例如，
假设
你
有
以下
定义：

.. code-block:: kconfig

   menu "Foo subsystem"

   config FOO_SUBSYSTEM
   	bool "Foo subsystem"

   if FOO_SUBSYSTEM

   config FOO_FEATURE_1
   	bool "Foo feature 1"

   config FOO_FEATURE_2
   	bool "Foo feature 2"

   config FOO_FREQUENCY
   	int "Foo frequency"

   ... lots of other FOO-related symbols

   endif # FOO_SUBSYSTEM

   endmenu

在
这种
情况
下，
可能
更好
的
是
去掉
``menu`` 并
将
``FOO_SUBSYSTEM`` 变成
``menuconfig`` 符号：

.. code-block:: kconfig

   menuconfig FOO_SUBSYSTEM
   	bool "Foo subsystem"

   if FOO_SUBSYSTEM

   config FOO_FEATURE_1
   	bool "Foo feature 1"

   config FOO_FEATURE_2
   	bool "Foo feature 2"

   config FOO_FREQUENCY
   	int "Foo frequency"

   ... lots of other FOO-related symbols

   endif # FOO_SUBSYSTEM

在
``menuconfig`` 接口
中，
这
将
显示
如下：

.. code-block:: none

   [*] Foo subsystem  --->

注意
使
没有
子
项
的
符号
成为
``menuconfig``
是
无
意义
的。
应该
避免，
因为
它
看起来
与
所有
子
项
不可见
的
符号
相同：

.. code-block:: none

   [*] I have no children  ----
   [*] All my children are invisible  ----


宏
参数
中
的
逗号
*************************

Kconfig
使用
逗号
分隔
宏
参数。
这意味着
像
这样
的
结构
会
失败：

.. code-block:: kconfig

    config FOO
        bool
        default y if $(dt_chosen_enabled,"zephyr,bar")

要
解决
这个
问题，
创建
一个
带
文本
的
变量
并
使用
这
个
变量
作为
参数，
如下：

.. code-block:: kconfig

    DT_CHOSEN_ZEPHYR_BAR := zephyr,bar

    config FOO
        bool
        default y if $(dt_chosen_enabled,$(DT_CHOSEN_ZEPHYR_BAR))

.. note::

   变量
   :samp:`DT_COMPAT_{VND_MY_DEVICE} := {vnd,my-device}`
   由
   Zephyr
   为
   设备树
   绑定
   中
   找到
   的
   每个
   ``compatible`` 自动
   创建；
   不
   需要
   定义
   这种
   变量。
   细节
   见
   :ref:`auto-dts-kconfig`。

在
menuconfig/guiconfig 中
检查
更改
****************************************

添加
新
符号
或
对
Kconfig 文件
做
其他
更改
时，
之后
在
:ref:`menuconfig 或
guiconfig <menuconfig>` 中
查找
符号
是
一个
好
主意。
要
快速
到达
符号，
使用
跳转
功能
（按
:kbd:`/`）。

这里
是
一些
要
检查
的
事情：

* 符号
  放在
  好
  的
  位置
  吗？
  检查
  它们
  显示
  在
  有意义
  的
  菜单
  中，
  靠近
  相关
  符号。

  如果
  一个
  符号
  依赖
  另一个，
  那么
  通常
  是
  一个
  好
  主意
  将
  它
  放在
  它
  依赖
  的
  符号
  紧
  后面。
  然后
  它
  在
  ``menuconfig`` 接口
  中
  显示
  为
  相对
  于
  它
  依赖
  的
  符号
  缩进，
  在
  ``guiconfig`` 中
  显示
  为
  以
  符号
  为
  根
  的
  单独
  菜单。
  如果
  几个
  符号
  放在
  它们
  依赖
  的
  符号
  后面，
  这
  也
  有效。

* 从
  prompt
  容易
  猜
  出
  符号
  做
  什么
  吗？

* 如果
  添加
  许多
  符号，
  它们
  可以
  被
  设置
  为
  的
  所有
  值
  组合
  都
  有意义
  吗？

  例如，
  如果
  添加
  两个
  符号
  ``FOO_SUPPORT`` 和
  ``NO_FOO_SUPPORT``，
  且
  两者
  可以
  同时
  启用，
  那么
  那
  是
  一个
  无
  意义
  的
  配置。
  在
  这种
  情况
  下，
  可能
  更好
  的
  是
  有
  单个
  ``FOO_SUPPORT`` 符号。

* 有
  重复
  的
  依赖
  吗？

  这
  可以
  通过
  选择
  符号
  并
  按
  :kbd:`?` 查看
  符号
  信息
  来
  检查。
  如果
  有
  重复
  的
  依赖，
  那么
  使用
  符号
  信息
  中
  显示
  的
  ``Included via ...`` 路径
  弄清楚
  它们
  来自
  哪里。


用
:file:`scripts/kconfig/lint.py` 检查
更改
*****************************************************

做
Kconfig 更改
后，
你
可以
使用
:zephyr_file:`scripts/kconfig/lint.py` 脚本
检查
一些
潜在
问题，
如
未
使用
的
符号
和
不可能
启用
的
符号。
使用
``--help`` 查看
可用
选项。

一些
检查
必然
有点
启发式，
因此
符号
被
检查
标记
不
一定
意味着
有
问题。
如果
检查
返回
假
阳性
（例如
由于
C 中
的
令牌
粘贴
（``CONFIG_FOO_##index##_BAR``）），
简单
忽略
它。

调查
未知
符号
``FOO_BAR`` 时，
运行
``git grep FOO_BAR`` 查找
引用
是
一个
好
主意。
用
例如
``git grep FOO`` 和
``git grep BAR`` 搜索
符号
名称
的
某些
组件
也
是
一个
好
主意，
因为
它
可以
帮助
发现
令牌
粘贴。


风格
建议
和
简写
************************************

本节
给出
一些
风格
建议
并
解释
一些
常见
的
Kconfig 简写。


提取
通用
依赖
=================================

如果
一系列
符号/choice
共享
通用
依赖，
依赖
可以
用
``if`` 提取。

作为
示例，
考虑
以下
代码：

.. code-block:: kconfig

   config FOO
   	bool "Foo"
   	depends on DEP

   config BAR
   	bool "Bar"
   	depends on DEP

   choice
   	prompt "Choice"
   	depends on DEP

   config BAZ
   	bool "Baz"

   config QAZ
   	bool "Qaz"

   endchoice

这里，
``DEP`` 依赖
可以
像
这样
提取：

.. code-block:: kconfig

   if DEP

   config FOO
   	bool "Foo"

   config BAR
   	bool "Bar"

   choice
   	prompt "Choice"

   config BAZ
   	bool "Baz"

   config QAZ
   	bool "Qaz"

   endchoice

   endif # DEP

.. note::

   内部，
   代码
   的
   第二
   版本
   被
   转换
   为
   第一
   版本。

如果
一系列
有
共享
依赖
的
符号/choice
都
在
同一
菜单
中，
依赖
可以
放在
菜单
本身
上：

.. code-block:: kconfig

   menu "Foo features"
   	depends on FOO_SUPPORT

   config FOO_FEATURE_1
   	bool "Foo feature 1"

   config FOO_FEATURE_2
   	bool "Foo feature 2"

   endmenu

如果
``FOO_SUPPORT`` 为
``n``，
整个
菜单
消失。


冗余
默认
值
=========================

``bool`` 符号
隐式
默认
为
``n``，
``string`` 符号
隐式
默认
为
空
字符串。
因此，
``default n`` 和
``default ""``
（几乎）
始终
冗余。

Zephyr 中
推荐
的
风格
是
跳过
``bool`` 和
``string`` 符号
的
冗余
默认
值。
那
也
生成
更
清晰
的
文档：
（*隐式
默认
为
n*
而非
*n if <依赖，
可能
继承>*）。

不过，
``int`` 和
``hex`` 符号
*应该*
始终
给出
默认
值，
因为
它们
隐式
默认
为
空
字符串。
这
部分
是
为了
与
C Kconfig 工具
兼容，
尽管
隐式
0 默认
值
可能
比
其他
符号
类型
更
不
可能
是
意图
所在。

``default n``/``default ""`` 不
冗余
的
唯一
情况
是
在
多个
位置
定义
符号
并
想要
覆盖
例如
后面
定义
中
的
``default y``。
注意
``default n``
不
覆盖
先前
定义
的
``default y``。

即，
下面
示例
中
FOO
将
被
设置
为
``n``。
如果
第一个
定义
中
省略
了
``default n``，
FOO
将
被
设置
为
``y``。

  .. code-block:: kconfig

     config FOO
     	bool "foo"
     	default n

     config FOO
     	bool "foo"
     	default y

在
下面
示例
中
FOO
将
得到
值
``y``。

  .. code-block:: kconfig

     config FOO
     	bool "foo"
     	default y

     config FOO
     	bool "foo"
     	default n

.. _kconfig_shorthands:

常见
Kconfig 简写
=========================

Kconfig
有
两个
处理
prompt
和
默认
值
的
简写。

- ``<type> "prompt"``
  是
  同时
  给
  符号/choice
  类型
  和
  prompt
  的
  简写。
  这
  两个
  定义
  相等：

  .. code-block:: kconfig

     config FOO
     	bool "foo"

  .. code-block:: kconfig

     config FOO
     	bool
     	prompt "foo"

  Zephyr 中
  偏好
  第一
  种
  带
  简写
  的
  风格。

- ``def_<type> <value>``
  是
  同时
  给
  类型
  和
  值
  的
  简写。
  这
  两个
  定义
  相等：

  .. code-block:: kconfig

     config FOO
     	def_bool BAR && BAZ

  .. code-block:: kconfig

     config FOO
     	bool
     	default BAR && BAZ

在
同一
定义
中
同时
使用
``<type> "prompt"`` 和
``def_<type> <value>`` 简写
是
冗余
的，
因为
它
两次
给出
类型。

``def_<type> <value>`` 简写
一般
只
对
没有
prompt
的
符号
有用，
且
有点
晦涩。

.. note::

   对于
   在
   多个
   位置
   定义
   的
   符号
   （例如
   在
   Zephyr 的
   ``Kconfig.defconfig`` 文件
   中），
   最好
   只
   为
   符号
   的
   "基础"
   定义
   给出
   符号
   类型，
   并
   对
   其余
   定义
   使用
   ``default``（而非
   ``def_<type>
   value``）。
   这样，
   如果
   符号
   基础
   定义
   被
   移除，
   符号
   最终
   没有
   类型，
   这
   生成
   一个
   指向
   其他
   定义
   的
   警告。
   这
   使
   额外
   定义
   更
   容易
   发现
   和
   移除。


Prompt
字符串
================

对于
启用
驱动/子系统
FOO 的
Kconfig 符号，
考虑
只
有
"Foo"
作为
prompt，
而非
"Enable Foo support" 或
类似
的。
在
可以
开关
的
选项
上下文
中
通常
会
清楚，
并
使
事情
一致。

风格
=====

风格
指南
见
:ref:`coding_style`。

较少
知名/使用
的
Kconfig 功能
**********************************

本节
列出
一些
更
晦涩
的
Kconfig 行为
和
功能，
它们
可能
仍
派
上用
场。


``imply`` 语句
======================

``imply`` 语句
类似
``select``，
但
尊重
依赖
且
不
强制
值。
例如，
以下
代码
可以
用于
在
FOO SoC 上
默认
启用
USB 键盘
支持，
同时
仍
允许
用户
关闭
它：

.. code-block:: kconfig

   config SOC_FOO
       bool
       imply USB_KEYBOARD

   ...

   config USB_KEYBOARD
   	bool "USB keyboard support"

``imply``
像
建议
一样
作用，
而
``select``
强制
值。


可选
prompt
================

可以
对
符号
的
prompt
放
条件
以
使
它
可选
地
由
用户
配置。
例如，
某些
开发板
上
硬编码
为
0xFF 而
其他
开发板
上
可
配置
的
值
``MASK``
可以
表达
如下：

.. code-block:: kconfig

   config MASK
   	hex "Bitmask" if HAS_CONFIGURABLE_MASK
   	default 0xFF

.. note::

   这
   是
   以下
   的
   简写：

   .. code-block:: kconfig

      config MASK
      	hex
      	prompt "Bitmask" if HAS_CONFIGURABLE_MASK
      	default 0xFF

``HAS_CONFIGURABLE_MASK`` 辅助
符号
将
被
开发板
select
以
指示
``MASK`` 可
配置。
当
``MASK`` 可
配置
时，
它
也
默认
为
0xFF。


可选
choice
================

用
``optional`` 关键字
定义
choice
允许
整个
choice
被
关闭
以
不
选择
任何
符号：

.. code-block:: kconfig

   choice
   	prompt "Use legacy protocol"
   	optional

   config LEGACY_PROTOCOL_1
   	bool "Legacy protocol 1"

   config LEGACY_PROTOCOL_2
   	bool "Legacy protocol 2"

   endchoice

在
``menuconfig`` 接口
中，
这
将
例如
显示
为
``[*] Use legacy protocol (Legacy protocol 1) --->``，
其中
choice
可以
被
关闭
以
不
启用
任何
符号。


``visible if`` 条件
=========================

对
菜单
放
``visible if`` 条件
隐藏
菜单
和
其中
所有
符号，
同时
仍
允许
符号
默认
值
生效。

作为
动机
示例，
考虑
以下
代码：

.. code-block:: kconfig

   menu "Foo subsystem"
   	depends on HAS_CONFIGURABLE_FOO

   config FOO_SETTING_1
   	int "Foo setting 1"
   	default 1

   config FOO_SETTING_2
   	int "Foo setting 2"
   	default 2

   endmenu

当
``HAS_CONFIGURABLE_FOO`` 为
``n`` 时，
``FOO_SETTING_1`` 和
``FOO_SETTING_2`` 不
生成
配置
输出，
因为
上面
的
代码
逻辑
上
等价
于
以下
代码：

.. code-block:: kconfig

   config FOO_SETTING_1
   	int "Foo setting 1"
   	default 1
   	depends on HAS_CONFIGURABLE_FOO

   config FOO_SETTING_2
   	int "Foo setting 2"
   	default 2
   	depends on HAS_CONFIGURABLE_FOO

如果
我们
想要
符号
即使
``HAS_CONFIGURABLE_FOO`` 为
``n`` 仍
得到
其
默认
值，
但
不
能
由
用户
配置，
那么
我们
可以
改用
``visible if``：

.. code-block:: kconfig

   menu "Foo subsystem"
   	visible if HAS_CONFIGURABLE_FOO

   config FOO_SETTING_1
   	int "Foo setting 1"
   	default 1

   config FOO_SETTING_2
   	int "Foo setting 2"
   	default 2

   endmenu

这
逻辑
上
等价
于
以下：

.. code-block:: kconfig

   config FOO_SETTING_1
   	int "Foo setting 1" if HAS_CONFIGURABLE_FOO
   	default 1

   config FOO_SETTING_2
   	int "Foo setting 2" if HAS_CONFIGURABLE_FOO
   	default 2

.. note::

   见
   `optional prompts`_ 章节
   了解
   prompt
   上
   条件
   的
   含义。

当
``HAS_CONFIGURABLE_FOO`` 为
``n`` 时，
我们
现在
得到
符号
的
以下
配置
输出，
而非
没有
输出：

.. code-block:: cfg

   ...
   CONFIG_FOO_SETTING_1=1
   CONFIG_FOO_SETTING_2=2
   ...


其他
资源
***************

`Kconfiglib docstring
<https://github.com/zephyrproject-rtos/Kconfiglib/blob/main/kconfiglib.py>`__ 中
的
*Intro to symbol values* 章节
更
详细
地
介绍
符号
值
如何
计算。
