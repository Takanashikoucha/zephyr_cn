.. _setting_configuration_values:

设置 Kconfig 配置值
####################################

:ref:`menuconfig 和 guiconfig 接口 <menuconfig>`
可以
用于
在
应用
开发
期间
测试
配置。
本页
解释
如何
使
设置
永久
化。

所有
Kconfig 选项
都
可以
在
:ref:`Kconfig 搜索
页面 <kconfig-search>` 中
搜索。

.. note::

   在
   对
   Kconfig 文件
   做
   更改
   之前，
   也
   去
   过
   一遍
   :ref:`kconfig_tips_and_tricks` 页面
   是
   一个
   好
   主意。


可见
与
不可见
Kconfig 符号
*************************************

做
Kconfig 更改
时，
理解
*可见*
和
*不可见*
符号
之间
的
区别
很
重要。

- 可见
  符号
  是
  带有
  prompt
  定义
  的
  符号。
  可见
  符号
  显示
  在
  交互式
  配置
  接口
  中
  （因此
  *可见*），
  并
  可以
  在
  配置
  文件
  中
  设置。

  以下是
  一个
  可见
  符号
  的
  示例：

  .. code-block:: kconfig

     config FPU
     	bool "Support floating point operations"
     	depends on HAS_FPU

  该
  符号
  在
  ``menuconfig`` 中
  显示
  如下，
  可以
  切换：

  .. code-block:: none

     [ ] Support floating point operations

- *不可见*
  符号
  是
  没有
  prompt
  的
  符号。
  不可见
  符号
  不
  显示
  在
  交互式
  配置
  接口
  中，
  用户
  无法
  直接
  控制
  其
  值。
  它们
  的
  值
  来自
  默认
  值
  或
  其他
  符号。

  以下是
  一个
  不可见
  符号
  的
  示例：

  .. code-block:: kconfig

     config CPU_HAS_FPU
     	bool
     	help
     	  This symbol is y if the CPU has a hardware floating point unit.

  在
  这种
  情况
  下，
  ``CPU_HAS_FPU``
  通过
  其他
  具有
  ``select CPU_HAS_FPU`` 的
  符号
  启用。


在
配置
文件
中
设置
符号
**************************************

可见
符号
可以
通过
在
配置
文件
中
设置
来
配置。
初始
配置
通过
合并
开发板
的
:file:`*_defconfig` 文件
与
应用
设置
（通常
来自
:file:`prj.conf`）
生成。
更多
细节
见
下面
的
:ref:`initial-conf`。

配置
文件
中
的
赋值
使用
此
语法：

.. code-block:: cfg

   CONFIG_<symbol name>=<value>

等号
周围
不应
有
空格。

``bool`` 符号
可以
通过
分别
设置
为
``y`` 或
``n`` 来
启用
或
禁用。
上面
示例
中
的
``FPU`` 符号
可以
像
这样
启用：

.. code-block:: cfg

   CONFIG_FPU=y

.. note::

   布尔
   符号
   也
   可以
   设置
   为
   ``n``，
   使用
   像
   这样
   格式
   的
   注释：

   .. code-block:: cfg

      # CONFIG_SOME_OTHER_BOOL is not set

   这
   是
   你
   在
   保存
   到
   构建
   目录
   中
   :file:`zephyr/.config` 的
   合并
   配置
   中
   看到
   的
   格式。

   出于
   历史
   原因
   接受
   这种
   风格：
   Kconfig 配置
   文件
   可以
   被
   解析
   为
   makefile
   （尽管
   Zephyr 不
   使用
   这）。
   使
   ``n`` 值
   的
   符号
   对应
   未
   设置
   的
   变量
   简化
   了
   Make 中
   的
   测试。

其他
符号
类型
像
这样
赋值：

.. code-block:: cfg

   CONFIG_SOME_STRING="cool value"
   CONFIG_SOME_INT=123

注释
使用
#：

.. code-block:: cfg

   # This is a comment

配置
文件
中
的
赋值
只有
在
符号
的
依赖
满足
时
才
被
尊重。
否则
会
打印
警告。
要
弄清楚
符号
的
依赖
是
什么，
使用
:ref:`交互式
配置
接口 <menuconfig>` 之一
（你
可以
用
:kbd:`/` 直接
跳转
到
符号），
或
在
:ref:`Kconfig 搜索
页面 <kconfig-search>` 中
查找
符号。


.. _initial-conf:

初始
配置
*************************

应用
的
初始
配置
来自
合并
三个
来源
的
配置
设置：

1. 存储在
   :file:`boards/<VENDOR>/<BOARD>/<BOARD>_defconfig` 的
   ``BOARD`` 特定
   配置
   文件

2. 任何
   以
   ``CONFIG_`` 为
   前缀
   的
   CMake 缓存
   条目

3. 应用
   配置

应用
配置
可以
来自
下面
的
来源
（每个
文件
都
称为
Kconfig
片段，
它们
然后
被
合并
以
获取
用于
特定
构建
的
最终
配置）。
默认
情况下，
使用
:file:`prj.conf`。

#. 如果
   设置
   了
   ``CONF_FILE``，
   其中
   指定
   的
   配置
   文件
   被
   合并
   并
   用作
   应用
   配置。
   ``CONF_FILE``
   可以
   通过
   多种
   方式
   设置：

   1. 在
      :file:`CMakeLists.txt` 中，
      在
      调用
      ``find_package(Zephyr)`` 之前

   2. 通过
      传递
      ``-DCONF_FILE=<conf file(s)>``，
      直接
      或
      通过
      ``west``

   3. 从
      CMake 变量
      缓存

#. 否则，
   如果
   :file:`boards/<BOARD>.conf`
   存在
   于
   应用
   配置
   目录
   中，
   使用
   它
   与
   :file:`prj.conf` 的
   合并
   结果。

#. 否则，
   如果
   使用
   开发板
   修订
   版本
   且
   :file:`boards/<BOARD>_<revision>.conf`
   存在
   于
   应用
   配置
   目录
   中，
   使用
   它
   与
   :file:`prj.conf` 和
   :file:`boards/<BOARD>.conf` 的
   合并
   结果。

#. 否则，
   从
   应用
   配置
   目录
   使用
   :file:`prj.conf`。
   如果
   它
   不
   存在，
   则
   会
   发出
   致命
   错误。

此外，
应用
可以
有
SoC Kconfig
片段
添加
到
配置，
如果
存在，
文件
:file:`socs/<SOC>_<BOARD_QUALIFIERS>.conf`
将
在
主
项目
配置
应用
后
且
任何
开发板
Kconfig
片段
文件
应用
前
被
应用。

所有
配置
文件
都
从
应用
的
配置
目录
获取，
除了
使用
``CONF_FILE``、``EXTRA_CONF_FILE``、``DTC_OVERLAY_FILE`` 和
``EXTRA_DTC_OVERLAY_FILE`` 参数
给出
的
绝对
路径
文件。
对于
这些，
Zephyr
模块
中
的
文件
可以
通过
转义
Zephyr
模块
目录
变量
来
引用，
像
这样
``\${ZEPHYR_<module>_MODULE_DIR}/<path-to>/<file>``
当
在
应用
的
:file:`CMakeLists.txt` 中
设置
任何
上述
变量
时。

如何
定义
应用
配置
目录
见
:ref:`Application Configuration Directory <application-configuration-directory>`。

如果
符号
同时
在
:file:`<BOARD>_defconfig` 和
应用
配置
中
赋值，
应用
配置
中
设置
的
值
优先。

合并
的
配置
保存
到
构建
目录
中
的
:file:`zephyr/.config`。

只要
:file:`zephyr/.config` 存在
且
是
最新
的
（比
任何
``BOARD`` 和
应用
配置
文件
新），
它
将
被
优先
使用
于
生成
新的
合并
配置。
:file:`zephyr/.config` 也
是
在
:ref:`交互式
配置
接口 <menuconfig>` 中
做
更改
时
被
修改
的
配置。


.. _kconfig_warning_as_error:

将
Kconfig 警告
视为
错误
***********************************

一些
Kconfig 警告
默认
中止
构建，
例如
对
未
定义
符号
的
赋值。
其他
只
被
打印，
例如
当
符号
被
设置
多
于
一次，
或
当
赋值
被
忽略
因为
符号
的
依赖
未
满足。

设置
:makevar:`KCONFIG_WARNING_AS_ERROR` CMake 变量
将
*每个*
Kconfig 警告
视为
错误：

.. code-block:: console

   west build -b <board> <app> -- -DKCONFIG_WARNING_AS_ERROR=y

这在
CI 中
很有
用，
那里
被
静默
忽略
的
配置
设置
很可能
是
错误。
它
通过
``zephyr_get()`` 读取，
因此
也
可以
作为
:ref:`环境变量 <env_vars>` 或
通过
:ref:`cmake_build_config_package` 给出。


跟踪
Kconfig 符号
************************

可以
创建
Kconfig 符号
取
另一个
Kconfig 符号
的
默认
值。

当你
想要
一个
特定
于
应用
或
子系统
的
符号
但
不
想
直接
依赖
通用
符号
时，
这
很有
价值。
例如，
你
可能
想要
解耦
设置
以便
它们
可以
独立
配置，
或
确保
你
始终
有
一个
本地
命名
的
设置，
即使
外部
设置
名称
之后
更改。

例如，
考虑
通用
的
``FOO_STRING`` 设置，
子系统
想要
有
``SUB_FOO_STRING`` 但
仍
允许
自定义。

可以
像
这样
做：

.. code-block:: kconfig

    config FOO_STRING
            string "Foo"
            default "foo"

    config SUB_FOO_STRING
            string "Sub-foo"
            default FOO_STRING

这
确保
``SUB_FOO_STRING`` 的
默认
值
与
``FOO_STRING`` 相同，
同时
仍
允许
用户
独立
配置
两个
设置。

也
可以
使
``SUB_FOO_STRING`` 不可见
并
由此
保持
两个
符号
同步，
除非
跟踪
符号
的
值
在
:file:`defconfig` 文件
中
被
更改。

.. code-block:: kconfig

    config FOO_STRING
            string "Foo"
            default "foo"

    config SUB_FOO_STRING
            string
            default FOO_STRING
            help
              Hidden symbol which follows FOO_STRING
              Can be changed through *.defconfig files.


配置
不可见
Kconfig 符号
*************************************

对
开发板
的
默认
配置
做
更改
时，
你
可能
必须
配置
不可见
符号。
这
在
:file:`boards/<VENDOR>/<BOARD>/Kconfig.defconfig` 中
完成，
它
是
一个
普通
的
:file:`Kconfig` 文件。

.. note::

    :file:`.config` 文件
    中
    的
    赋值
    对
    不可见
    符号
    没有
    影响，
    因此
    这种
    方案
    不
    只是
    一个
    组织
    问题。

:file:`Kconfig.defconfig` 中
的
赋值
依赖
于
在
多个
位置
定义
Kconfig 符号。
作为
示例，
假设
我们
想要
将
下面
的
``FOO_WIDTH`` 设置
为
32：

.. code-block:: kconfig

    config FOO_WIDTH
    	int

要
做到
这，
我们
在
:file:`Kconfig.defconfig` 中
按
如下
方式
扩展
``FOO_WIDTH`` 的
定义：

.. code-block:: kconfig

    if BOARD_MY_BOARD

    config FOO_WIDTH
    	default 32

    endif

.. note::

   由于
   符号
   的
   类型
   （``int``）
   已
   在
   第一个
   定义
   位置
   给出，
   这里
   不
   需要
   重复。
   只
   在
   符号
   的
   "基础"
   定义
   中
   给出
   类型
   一次
   是
   一个
   好
   主意，
   原因
   在
   :ref:`kconfig_shorthands` 中
   解释。

:file:`Kconfig.defconfig` 文件
中
的
``default`` 值
优先
于
符号
"基础"
定义
中
给出
的
``default`` 值。
内部，
这
通过
先
包含
:file:`Kconfig.defconfig` 文件
实现。
Kconfig
使用
第一个
条件
满足
的
``default``，
其中
空
条件
对应
``if y``（始终
满足）。

注意
来自
周围
顶层
``if``\ s 的
条件
传播
到
符号
属性，
因此
上面
的
``default`` 等价于
``default 32 if BOARD_MY_BOARD``。

.. _multiple_symbol_definitions:

多个
符号
定义
---------------------------

当
符号
在
多个
位置
定义
时，
每个
定义
作为
一个
碰巧
共享
相同
名称
的
独立
符号
起作用。
这意味着
属性
不
被
追加
到
先前
的
定义。
如果
**任何**
定义
的
条件
导致
符号
解析
为
``y``，
符号
将
是
``y``。
因此
不
可能
通过
在
多个
位置
定义
使
符号
的
依赖
更
严格。

例如，
下面
符号
``FOO`` 的
依赖
在
``DEP1`` **或** ``DEP2`` 为
真
时
满足，
不
要求
两者
都
是：

.. code-block:: none

   config FOO
     ...
     depends on DEP1

   config FOO
     ...
     depends on DEP2

.. warning::
   没有
   显式
   依赖
   的
   符号
   仍
   遵循
   上面
   的
   规则。
   没有
   任何
   依赖
   的
   符号
   将
   导致
   符号
   始终
   可
   赋值。
   下面
   的
   定义
   将
   导致
   ``FOO`` 始终
   默认
   启用，
   无论
   ``DEP1`` 的
   值
   如何。

   .. code-block:: kconfig

      config FOO
         bool "FOO"
         depends on DEP1

      config FOO
         default y

   这种
   依赖
   削弱
   可以
   通过
   :ref:`configdefault
   <kconfig_extensions>` 扩展
   避免，
   如果
   意图
   只是
   添加
   新的
   默认
   值
   而
   不
   修改
   符号
   的
   其他
   行为。

.. note::
   对
   :file:`Kconfig.defconfig` 文件
   做
   更改
   时，
   之后
   始终
   在
   :ref:`交互式
   配置
   接口 <menuconfig>` 之一
   中
   检查
   符号
   的
   直接
   依赖。
   通常
   需要
   重复
   符号
   基础
   定义
   中
   的
   依赖
   以
   避免
   削弱
   符号
   的
   依赖。


Kconfig.defconfig 文件
的
动机
--------------------------------------

这种
配置
方案
的
一个
动机
是
避免
使
固定
的
``BOARD`` 特定
设置
在
交互式
配置
接口
中
可
配置。
如果
所有
开发板
配置
都
通过
:file:`<BOARD>_defconfig` 完成，
所有
符号
都
必须
可见，
因为
:file:`<BOARD>_defconfig` 中
给出
的
值
对
不可见
符号
没有
影响。

使
固定
设置
可
由
用户
配置
会
使
配置
接口
杂乱
并
使
它们
更
难
理解，
并
使
意外
创建
损坏
的
配置
更
容易。

处理
固定
的
开发板
特定
设置
时，
也
考虑
它们
是否
应该
通过
:ref:`设备树 <dt-guide>` 处理。


配置
choice
-------------------

有两种
方式
配置
Kconfig ``choice``：

1. 通过
   在
   配置
   文件
   中
   将
   choice
   符号
   之一
   设置
   为
   ``y``。

   将
   一个
   choice
   符号
   设置
   为
   ``y``
   自动
   给
   所有
   其他
   choice
   符号
   值
   ``n``。

   如果
   多个
   choice
   符号
   被
   设置
   为
   ``y``，
   只有
   最后
   设置
   为
   ``y`` 的
   被
   尊重
   （其余
   得到
   值
   ``n``）。
   这
   允许
   从
   开发板
   :file:`defconfig` 文件
   的
   choice
   选择
   被
   应用
   :file:`prj.conf` 文件
   覆盖。

2. 通过
   在
   :file:`Kconfig.defconfig` 中
   更改
   choice 的
   ``default``。

   与
   符号
   一样，
   更改
   choice 的
   默认
   通过
   在
   多个
   位置
   定义
   choice 完成。
   要
   使
   这
   工作，
   choice
   必须
   有
   名称。

   作为
   示例，
   假设
   choice 有
   以下
   基础
   定义
   （这里，
   choice 的
   名称
   是
   ``FOO``）：

   .. code-block:: kconfig

      choice FOO
          bool "Foo choice"
          default B

      config A
          bool "A"

      config B
          bool "B"

      endchoice

   要
   将
   ``FOO`` 的
   默认
   符号
   更改
   为
   ``A``，
   你
   会
   添加
   以下
   定义
   到
   :file:`Kconfig.defconfig`：

   .. code-block:: kconfig

      choice FOO
          default A
      endchoice

:file:`Kconfig.defconfig` 方法
应该
在
choice 的
依赖
可能
未
满足
时
使用。
在
那种
情况
下，
你
在
用户
使
choice
可见
的
任何
时候
设置
默认
选择。


更多
Kconfig 资源
====================

:ref:`kconfig_tips_and_tricks` 页面
有
一些
编写
Kconfig 文件
的
技巧。

:zephyr_file:`kconfiglib.py <scripts/kconfig/kconfiglib.py>` 的
docstring
（文件
顶部）
详细
介绍
符号
值
如何
计算。
