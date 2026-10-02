.. _kconfig-functions:

自定义 Kconfig 预处理器函数
#####################################

Kconfiglib 支持用 Python 编写的自定义 Kconfig 预处理器函数。这些函数定义在
:zephyr_file:`scripts/kconfig/kconfigfunctions.py`。

.. note::

   官方 Kconfig 预处理器文档可以在
   `这里
   <https://www.kernel.org/doc/html/latest/kbuild/kconfig-macro-language.html>`__
   找到。

关于详细文档见 :zephyr_file:`scripts/kconfig/kconfigfunctions.py` 中的 Python
docstring。大多数自定义预处理器函数用于将设备树信息获取到 Kconfig 中。例如，
Kconfig 符号的默认值可以从设备树 ``reg`` 属性获取。

设备树相关函数
****************************

下面列出的函数用于将设备树信息获取到 Kconfig 中。每个函数的 ``*_int`` 版本将
值作为十进制整数返回，而 ``*_hex`` 版本返回以 ``0x`` 开头的十六进制值。

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


整数函数
*****************

下面列出的函数可以用于对整数变量执行算术运算，如加法、减法和更多。名称中
带和不带 ``_hex`` 后缀的函数分别返回十六进制和十进制值。

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


字符串函数
****************

下面列出的函数可以用于修改字符串变量。

.. code-block:: none

   $(normalize_upper,<string>)
   $(substring,<string>,<start>[,<stop>])


其他函数
***************

执行特定操作的函数，目前只有检查是否指定了 shield 名称。

.. code-block:: none

   $(shields_list_contains,<shield name>)

Shield 名称不能包含空白。逗号后的空格，如 ``$(shields_list_contains, foo)``
中的那样，被去除并打印警告，因此查找仍匹配 ``foo``。


示例用法
============

假设某个开发板的设备树看起来像这样：

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

``spi@1001400`` 中 ``reg`` 的第二个条目（``<0x20010000 0x3c0900>``）对应
``mem``，地址为 ``0x20010000``。这个地址可以按如下方式插入 Kconfig：

.. code-block:: kconfig

   config FLASH_BASE_ADDRESS
   	default $(dt_node_reg_addr_hex,/soc/spi@1001400,1)

预处理器展开后，这变成下面的定义：

.. code-block:: kconfig

   config FLASH_BASE_ADDRESS
   	default 0x20010000
