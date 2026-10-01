.. _led_api:

发光二极管（LED）
##################

概述
****

LED API 提供对发光二极管的访问，既支持单个 LED，也支持灯带形式。它在少量通用操作的背后，抽象了简单 GPIO 驱动的 LED、PWM 可调光 LED、专用 LED 控制器 IC 以及可寻址 LED 灯带之间的差异。

暴露了两个相关子系统：

* **LED** —— 控制分立或控制器驱动的 LED（开/关、亮度、颜色、闪烁）的通用 API
* **LED Strip** —— 针对 WS2812 和 APA102 等可寻址 LED 灯串的 API，其中每个像素携带自己的颜色值

LED 操作
********

驱动实现下列操作的一个子集。对可选操作的调用，如果底层驱动未提供，则返回 ``-ENOSYS``。

必选操作（至少一个）：

* :c:func:`led_on` / :c:func:`led_off` —— 将 LED 完全点亮或熄灭
* :c:func:`led_set_brightness` —— 设置 0 到
  :c:macro:`LED_BRIGHTNESS_MAX`（100）范围内的亮度；实现时，
  :c:func:`led_on` 和 :c:func:`led_off` 也会自动使用它

可选操作：

* :c:func:`led_blink` —— 以给定的亮/灭时长开始 LED 闪烁
* :c:func:`led_set_color` —— 设置多色 LED 的各通道颜色值
* :c:func:`led_get_info` —— 获取描述特定 LED（标签、索引、颜色映射）的
  :c:struct:`led_info`
* :c:func:`led_write_channels` —— 写入一段原始通道值，用于将 LED 表示为通道数组的驱动

LED 索引
********

驱动控制的每个 LED 都由基于零的 ``led`` 索引寻址。多色 LED 占用一个索引；其颜色通道一起提交给 :c:func:`led_set_color`。

多色 LED 的颜色通道顺序由 :c:struct:`led_info` 的 ``color_mapping`` 字段描述。每个条目都是 :file:`include/zephyr/dt-bindings/led/led.h` 中定义的 ``LED_COLOR_ID_*`` 值之一：

* ``LED_COLOR_ID_WHITE``
* ``LED_COLOR_ID_RED``
* ``LED_COLOR_ID_GREEN``
* ``LED_COLOR_ID_BLUE``
* ``LED_COLOR_ID_AMBER``
* ``LED_COLOR_ID_VIOLET``
* ``LED_COLOR_ID_YELLOW``
* ``LED_COLOR_ID_IR``

设备树配置
**********

简单 LED 通常描述为 LED 控制器的子节点，并通过设备树别名引用：

.. code-block:: dts

   / {
       aliases {
           led0 = &status_led;
       };

       leds {
           compatible = "gpio-leds";
           status_led: led_0 {
               gpios = <&gpio0 13 GPIO_ACTIVE_HIGH>;
               label = "Status LED";
           };
       };
   };

对于多色 LED，颜色信息用 ``color-mapping`` 属性编码，使用
:file:`include/zephyr/dt-bindings/led/led.h` 中的 ``LED_COLOR_ID_*`` 值。

使用示例
********

使用设备树别名进行基本的开/关控制：

.. code-block:: c

   #include <zephyr/drivers/led.h>
   #include <zephyr/devicetree.h>

   #define LED_NODE DT_ALIAS(led0)
   static const struct device *led_dev = DEVICE_DT_GET(DT_PARENT(LED_NODE));
   static const uint32_t led_idx = DT_NODE_CHILD_IDX(LED_NODE);

   int turn_on_status_led(void)
   {
       if (!device_is_ready(led_dev)) {
           return -ENODEV;
       }
       return led_on(led_dev, led_idx);
   }

设置亮度（0 到 100）：

.. code-block:: c

   /* Dim the LED to 25% brightness */
   led_set_brightness(led_dev, led_idx, 25);

以 500 毫秒亮 / 500 毫秒灭的模式闪烁：

.. code-block:: c

   int err = led_blink(led_dev, led_idx, 500, 500);

   if (err == -ENOSYS) {
       /* Driver does not implement blink natively */
   }

设置多色（RGB）LED 的颜色：

.. code-block:: c

   /* Order of the values must match the color_mapping reported by
    * led_get_info(); for a standard RGB mapping the order is R, G, B.
    */
   const uint8_t purple[] = { 0x80, 0x00, 0x80 };

   led_set_color(led_dev, led_idx, ARRAY_SIZE(purple), purple);

配置选项
*********

相关配置选项：

* :kconfig:option:`CONFIG_LED`
* :kconfig:option:`CONFIG_LED_STRIP`
* :kconfig:option:`CONFIG_LED_SHELL`
* :kconfig:option:`CONFIG_LED_INIT_PRIORITY`

API 参考
********

LED
===

.. doxygengroup:: led_interface

LED 灯带
========

.. doxygengroup:: led_strip_interface

模拟 LED 控制器
================

.. doxygengroup:: led_fake
