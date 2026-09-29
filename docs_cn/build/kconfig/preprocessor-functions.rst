.. _kconfig-functions:

自定义 Kconfig 预处理器函数
#####################################

Kconfiglib
支持
用
Python
编写
的
自定义
Kconfig
预处理器
函数。
这些
函数
定义
在
:zephyr_file:`scripts/kconfig/kconfigfunctions.py`。

.. note::

   官方
   Kconfig
   预处理器
   文档
   可以
   在
   `这里
   <https://www.kernel.org/doc/html/latest/kbuild/kconfig-macro-language.html>`__
   找到。

关于
详细
文档
见
:zephyr_file:`scripts/kconfig/kconfigfunctions.py` 中
的
Python
docstring。
大多数
自定义
预处理器
函数
用于
将
设备树
信息
获取
到
Kconfig 中。
例如，
Kconfig 符号
的
默认
值
可以
从
设备树
``reg`` 属性
获取。

设备树
相关
函数
****************************

下面
列出
的
函数
用于
将
设备树
信息
获取
到
Kconfig 中。
每个
函数
的
``*_int`` 版本
将
值
作为
十
进制
整数
返回，
而
``*_hex`` 版本
返回
以
``0x`` 开头
的
十六
进制
值。

.. code-block:: none

   $(dt_alias_enabled,<node alias>)
   $(dt_chosen_bool_prop, <property in /chosen>, <prop>)
   $(dt_chosen_enabled,<property in /chosen>)
   $(dt_chosen_has_compat,<property in /chosen>,<compatible string>)
   $(dt_chosen_label,<property in /chosen>)
   $(dt_chosen_partition,addr_hex,<chosen>[,<index>,<unit>])
   $(dt_chosen_partition,addr_int,<chosen>[,<index>,<unit>])
   $(dt_chosen_path,<property in /chosen>)
   $(dt_chosen_reg_addr_hex,<property in /chosen>[,<index>,<unit>])
   $(dt_chosen_reg_addr_int,<property in /chosen>[,<index>,<unit>])
   $(dt_chosen_reg_size_hex,<property in /chosen>[,<index>,<unit>])
   $(dt_chosen_reg_size_int,<property in /chosen>[,<index>,<unit>])
   $(dt_class_enabled,<class name>)
   $(dt_compat_all_has_prop,<compatible string>,<prop>[,<value>])
   $(dt_compat_any_has_prop,<compatible string>,<prop>[,<value>])
   $(dt_compat_any_on_bus,<compatible string>,<prop>)
   $(dt_compat_enabled,<compatible string>)
   $(dt_compat_enabled_num,<compatible string>)
   $(dt_compat_on_bus,<compatible string>,<bus>)
   $(dt_gpio_hogs_enabled)
   $(dt_has_compat,<compatible string>)
   $(dt_highest_controller_irq_number,<node path>,<cell>)
   $(dt_node_array_prop_has_val,<node path>,<prop>,<value>)
   $(dt_node_array_prop_hex,<node path>,<prop>,<index>[,<unit>])
   $(dt_node_array_prop_int,<node path>,<prop>,<index>[,<unit>])
   $(dt_node_bool_prop,<node path>,<prop>)
   $(dt_node_has_compat,<node path>,<compatible string>)
   $(dt_node_has_prop,<node path>,<prop>)
   $(dt_node_int_prop_hex,<node path>,<prop>[,<unit>])
   $(dt_node_int_prop_int,<node path>,<prop>[,<unit>])
   $(dt_node_parent,<node path>)
   $(dt_node_ph_array_prop_hex,<node path>,<prop>,<index>,<cell>[,<unit>])
   $(dt_node_ph_array_prop_int,<node path>,<prop>,<index>,<cell>[,<unit>])
   $(dt_node_ph_prop_path,<node path>,<prop>)
   $(dt_node_reg_addr_hex,<node path>[,<index>,<unit>])
   $(dt_node_reg_addr_int,<node path>[,<index>,<unit>])
   $(dt_node_reg_size_hex,<node path>[,<index>,<unit>])
   $(dt_node_reg_size_int,<node path>[,<index>,<unit>])
   $(dt_node_str_prop_equals,<node path>,<prop>,<value>)
   $(dt_nodelabel_array_prop_has_val, <node label>, <prop>, <value>)
   $(dt_nodelabel_bool_prop,<node label>,<prop>)
   $(dt_nodelabel_enabled,<node label>)
   $(dt_nodelabel_enabled_with_compat,<node label>,<compatible string>)
   $(dt_nodelabel_exists,<node label>)
   $(dt_nodelabel_has_compat,<node label>,<compatible string>)
   $(dt_nodelabel_has_prop,<node label>,<prop>)
   $(dt_nodelabel_path,<node label>)
   $(dt_nodelabel_reg_addr_hex,<node label>[,<index>,<unit>])
   $(dt_nodelabel_reg_addr_int,<node label>[,<index>,<unit>])
   $(dt_nodelabel_reg_size_hex,<node label>[,<index>,<unit>])
   $(dt_nodelabel_reg_size_int,<node label>[,<index>,<unit>])
   $(dt_path_enabled,<node path>)
   $(dt_partition_mtd,<node path>)


整数
函数
*****************

下面
列出
的
函数
可以
用于
对
整数
变量
执行
算术
运算，
如
加法、
减法
和
更多。
名称
中
带
和不
带
``_hex`` 后缀
的
函数
分别
返回
十六
进制
和
十
进制
值。

.. code-block:: none

   $(add,<value>[,value]...)
   $(add_hex,<value>[,value]...)
   $(dec,<value>[,value]...)
   $(dec_hex,<value>[,value]...)
   $(div,<value>[,value]...)
   $(div_hex,<value>[,value]...)
   $(inc,<value>[,value]...)
   $(inc_hex,<value>[,value]...)
   $(max,<value>[,value]...)
   $(max_hex,<value>[,value]...)
   $(min,<value>[,value]...)
   $(min_hex,<value>[,value]...)
   $(mod,<value>[,value]...)
   $(mod_hex,<value>[,value]...)
   $(mul,<value>[,value]...)
   $(mul_hex,<value>[,value]...)
   $(sub,<value>[,value]...)
   $(sub_hex,<value>[,value]...)


字符串
函数
****************

下面
列出
的
函数
可以
用于
修改
字符串
变量。

.. code-block:: none

   $(normalize_upper,<string>)
   $(substring,<string>,<start>[,<stop>])


其他
函数
***************

执行
特定
操作
的
函数，
目前
只有
检查
是否
指定
了
shield
名称。

.. code-block:: none

   $(shields_list_contains,<shield name>)

Shield
名称
不能
包含
空白。
逗号
后
的
空格，
如
``$(shields_list_contains, foo)`` 中
的
那样，
被
去除
并
打印
警告，
因此
查找
仍
匹配
``foo``。


示例
用法
============

假设
某个
开发板
的
设备树
看起来
像
这样：

.. code-block:: devicetree

   {
   	soc {
   		#address-cells = <1>;
   		#size-cells = <1>;

   		spi0: spi@10014000 {
   			compatible = "sifive,spi0";
   			reg = <0x10014000 0x1000 0x20010000 0x3c0900>;
   			reg-names = "control", "mem";
   			...
   		};
   };

``spi@1001400`` 中
``reg`` 的
第二个
条目
（``<0x20010000 0x3c0900>``）
对应
``mem``，
地址
为
``0x20010000``。
这个
地址
可以
按
如下
方式
插入
Kconfig：

.. code-block:: kconfig

   config FLASH_BASE_ADDRESS
   	default $(dt_node_reg_addr_hex,/soc/spi@1001400,1)

预处理器
展开
后，
这
变成
下面
的
定义：

.. code-block:: kconfig

   config FLASH_BASE_ADDRESS
   	default 0x20010000
