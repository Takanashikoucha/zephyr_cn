.. _dt-inferred-bindings:
.. _dt-zephyr-user:

``/zephyr,user`` 节点
#########################

Zephyr 的设备树脚本将 ``/zephyr,user`` 节点作为特殊情况处理：
你可以在其中放入基本上任意的属性，
无需编写绑定即可获取其值。
它旨在作为
仅需要少量简单属性时的
便捷容器。
类型从
分配给
属性的
值推断。

.. note::

   此节点
   用于
   示例
   代码
   和
   用户
   应用。
   不应
   在
   上游
   Zephyr 源
   代码
   （设备
   驱动、
   子
   系统等）
   中
   使用。

简单值
*************

如果
你
想
在
构建
时
通过
设备树
配置
数值
或
数组
值，
可以
将其
存储
在
``/zephyr,user`` 中。

例如，
对于
此
设备树
覆盖：

.. code-block:: devicetree

   / {
   	zephyr,user {
   		boolean;
   		bytes = [81 82 83];
   		number = <23>;
   		numbers = <1>, <2>, <3>;
   		string = "text";
   		strings = "a", "b", "c";
   	};
   };

你可以
像
这样
在
C/C++ 代码
中
获取
上面
的
属性
值：

.. code-block:: C

   #define ZEPHYR_USER_NODE DT_PATH(zephyr_user)

   DT_PROP(ZEPHYR_USER_NODE, boolean) // 1
   DT_PROP(ZEPHYR_USER_NODE, bytes)   // {0x81, 0x82, 0x83}
   DT_PROP(ZEPHYR_USER_NODE, number)  // 23
   DT_PROP(ZEPHYR_USER_NODE, numbers) // {1, 2, 3}
   DT_PROP(ZEPHYR_USER_NODE, string)  // "text"
   DT_PROP(ZEPHYR_USER_NODE, strings) // {"a", "b", "c"}

设备
*******

如果
你
想
在
简单
情况
下
使用
设备树
覆盖
重新
配置
应用
使用
的
设备，
可以
在
``/zephyr,user`` 中
存储
:ref:`phandle <dt-phandles>`。

例如，
对于
此
设备树
覆盖：

.. code-block:: devicetree

   / {
   	zephyr,user {
   		handle = <&gpio0>;
   		handles = <&gpio0>, <&gpio1>;
        };
   };

你可以
像
这样
将
``handle`` 和
``handles`` 属性
中
的
phandle
转换
为
设备
指针：

.. code-block:: C

   /*
    * Same thing as:
    *
    * ... my_dev = DEVICE_DT_GET(DT_NODELABEL(gpio0));
    */
   const struct device *my_device =
   	DEVICE_DT_GET(DT_PROP(ZEPHYR_USER_NODE, handle));

   /*
    * Same thing as:
    *
    * ... *my_devices[] = {
    *         DEVICE_DT_GET(DT_NODELABEL(gpio0)),
    *         DEVICE_DT_GET(DT_NODELABEL(gpio1))
    * };
    */
   const struct device *my_devices[] = {
       DT_FOREACH_PROP_ELEM_SEP(ZEPHYR_USER_NODE, handles, DEVICE_DT_GET_BY_IDX, (,))
   };

GPIO
*****

``/zephyr,user`` 节点
是
存储
你
想
用
设备树
覆盖
重新
配置
的
应用
特定
GPIO 的
便捷
位置。

.. note::

   所有
   值
   包含
   至少
   一个
   phandle
   和
   一个
   数字
   的
   属性
   都
   会
   被
   推断
   为
   phandle-array。
   例如
   ``<&adc0 1>``。

例如，
对于
此
设备树
覆盖：

.. code-block:: devicetree

   #include <zephyr/dt-bindings/gpio/gpio.h>

   / {
   	zephyr,user {
   		signal-gpios = <&gpio0 1 GPIO_ACTIVE_HIGH>;
        };
   };

你可以
将
``signal-gpios`` 中
定义
的
引脚
转换
为
``struct
gpio_dt_spec``，
然后
像
这样
使用：

.. code-block:: C

   #include <zephyr/drivers/gpio.h>

   #define ZEPHYR_USER_NODE DT_PATH(zephyr_user)

   const struct gpio_dt_spec signal =
           GPIO_DT_SPEC_GET(ZEPHYR_USER_NODE, signal_gpios);

   /* Configure the pin */
   gpio_pin_configure_dt(&signal, GPIO_OUTPUT_INACTIVE);

   /* Set the pin to its active level */
   gpio_pin_set_dt(&signal, 1);

（这些
API 的
细节
见
:c:struct:`gpio_dt_spec`、:c:macro:`GPIO_DT_SPEC_GET` 和
:c:func:`gpio_pin_configure_dt`。）
