.. _dt-inferred-bindings:
.. _dt-zephyr-user:

``/zephyr,user`` 节点
#########################

Zephyr 的设备树脚本将 ``/zephyr,user`` 节点作为特殊情况处理：你可以在其中放入
基本上任意的属性，无需编写绑定即可获取其值。它旨在作为仅需要少量简单属性时的
便捷容器。类型从分配给属性的值推断。

.. note::

   此节点用于示例代码和用户应用。不应在上游 Zephyr 源代码（设备驱动、子系统
   等）中使用。

简单值
*************

如果你想让数值或数组值在构建时可通过设备树配置，可以将其存储在
``/zephyr,user`` 中。

例如，对于此设备树覆盖：

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

你可以像这样在 C/C++ 代码中获取上面的属性值：

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

如果你想能在简单情况下使用设备树覆盖重新配置应用使用的设备，可以在
``/zephyr,user`` 中存储 :ref:`phandle <dt-phandles>`。

例如，对于此设备树覆盖：

.. code-block:: devicetree

   / {
   	zephyr,user {
   		handle = <&gpio0>;
   		handles = <&gpio0>, <&gpio1>;
         };
   };

你可以像这样将 ``handle`` 和 ``handles`` 属性中的 phandle 转换为设备指针：

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

``/zephyr,user`` 节点是存储你想用设备树覆盖重新配置的应用特定 GPIO 的便捷位置。

.. note::

   所有值包含至少一个 phandle 和一个数字的属性都会被推断为 phandle-array。
   例如 ``<&adc0 1>``。

例如，对于此设备树覆盖：

.. code-block:: devicetree

   #include <zephyr/dt-bindings/gpio/gpio.h>

   / {
   	zephyr,user {
   		signal-gpios = <&gpio0 1 GPIO_ACTIVE_HIGH>;
         };
   };

你可以在源代码中将 ``signal-gpios`` 中定义的引脚转换为 ``struct gpio_dt_spec``，
然后像这样使用：

.. code-block:: C

   #include <zephyr/drivers/gpio.h>

   #define ZEPHYR_USER_NODE DT_PATH(zephyr_user)

   const struct gpio_dt_spec signal =
           GPIO_DT_SPEC_GET(ZEPHYR_USER_NODE, signal_gpios);

   /* Configure the pin */
   gpio_pin_configure_dt(&signal, GPIO_OUTPUT_INACTIVE);

   /* Set the pin to its active level */
   gpio_pin_set_dt(&signal, 1);

（这些 API 的细节见 :c:struct:`gpio_dt_spec`、:c:macro:`GPIO_DT_SPEC_GET` 和
:c:func:`gpio_pin_configure_dt`。）
