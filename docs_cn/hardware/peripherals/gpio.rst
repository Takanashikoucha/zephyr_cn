.. _gpio_api:

通用输入/输出（GPIO）
###################################

概述
********

通用输入/输出（GPIO）是没有特定功能但可由软件控制作为输入或输出的数字信号引脚。

GPIO API 提供与通用输入/输出（GPIO）引脚交互的通用方法。它允许应用将引脚配置为输入或输出、读取和写入其状态，以及管理中断。关键特性包括：

**引脚配置**
  将引脚配置为输入、输出或断开。
  支持内部上拉/下拉电阻和驱动强度配置。

**数据访问**
  读取输入值和写入输出值。

**中断**
  配置引脚状态变化（上升沿、下降沿、低电平、高电平）上的中断，并注册回调函数处理这些中断。

**设备树集成**
  GPIO 通常在设备树中定义，允许驱动和应用使用 :c:struct:`gpio_dt_spec` 以硬件无关的方式引用它们。

设备树配置
************************

GPIO 控制器在设备树中定义为带有 ``gpio-controller`` 属性的节点。``#gpio-cells`` 属性通常指定使用 2 个单元描述 GPIO：引脚编号和标志。

GPIO 控制器定义的示例：

.. code-block:: devicetree

   gpio0: gpio@40022000 {
       compatible = "ti,cc13xx-cc26xx-gpio";
       reg = <0x40022000 0x400>;
       interrupts = <0 0>;
       gpio-controller;
       #gpio-cells = <2>;
   };

引用 GPIO 的示例：

.. code-block:: devicetree

   leds {
       compatible = "gpio-leds";
       led0: led_0 {
           gpios = <&gpio0 25 GPIO_ACTIVE_HIGH>;
           label = "Green LED";
       };
   };

基本操作
***************

GPIO 操作通常在 :c:struct:`gpio_dt_spec` 结构上执行，它是设备树中指定的 GPIO 引脚信息的容器。

此结构通常用 :c:macro:`GPIO_DT_SPEC_GET` 宏（或其任何变体）填充。

.. code-block:: c
   :caption: 为定义别名为 ``led0`` 的 GPIO 引脚填充 gpio_dt_spec 结构

   #define LED0_NODE DT_ALIAS(led0)
   static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);

然后可以用 :c:struct:`gpio_dt_spec` 结构执行 GPIO 操作。

.. code-block:: c
   :caption: 将 GPIO 引脚（``led`` 来自前面的片段）配置为输出、初始非活动，然后设置为其活动电平。

   int ret;

   ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE);
   if (ret < 0) {
       return ret;
   }

   ret = gpio_pin_set_dt(&led, 1);
   if (ret < 0) {
       return ret;
   }

参见 :zephyr:code-sample:`blinky` 获取使用 :c:struct:`gpio_dt_spec` 结构执行 GPIO 基本操作的完整示例。

GPIO 操作也可以直接在 GPIO 控制器设备上执行，在这种情况下将使用接受设备指针作为参数的 GPIO API 函数。例如 :c:func:`gpio_pin_configure` 而非 :c:func:`gpio_pin_configure_dt`。

GPIO 占用
*********

GPIO 占用（hogs）提供在系统初始化期间自动配置 GPIO 引脚的机制。这对于需要设置为特定状态（例如复位线、电源使能）且不需要应用运行时控制的引脚有用。

占用项在设备树中定义为 GPIO 控制器节点的子节点。

- ``gpio-hog`` 属性将节点标记为占用项。
- ``gpios`` 属性指定引脚及其活动状态。
- ``input``、``output-low`` 或 ``output-high`` 属性之一指定配置。

设备树覆盖层示例：

.. code-block:: devicetree

   &gpio0 {
       hog1 {
           gpio-hog;
           gpios = <1 GPIO_ACTIVE_LOW>;
           output-high;
       };

       hog2 {
           gpio-hog;
           gpios = <2 GPIO_ACTIVE_HIGH>;
           output-low;
       };
   };

如果你需要在系统初始化期间自动设置初始状态之外对配置为占用项的引脚进行运行时控制，可以考虑改用 :ref:`regulator_api` 配合 :dtcompatible:`regulator-fixed` 设备树节点。

配置选项
*********************

主要配置选项：

* :kconfig:option:`CONFIG_GPIO`
* :kconfig:option:`CONFIG_GPIO_SHELL`
* :kconfig:option:`CONFIG_GPIO_GET_DIRECTION`
* :kconfig:option:`CONFIG_GPIO_GET_CONFIG`
* :kconfig:option:`CONFIG_GPIO_HOGS`
* :kconfig:option:`CONFIG_GPIO_ENABLE_DISABLE_INTERRUPT`

API 参考
*************

.. doxygengroup:: gpio_interface
