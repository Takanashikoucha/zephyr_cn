.. _pwm_api:

脉宽调制（PWM）
############################

概述
********

脉宽调制（PWM）是通过改变数字信号的占空比来编码信息或控制电源交付的技术。PWM 信号以固定频率在高和低状态之间切换；每个周期中处于高状态的时间分数是*占空比*。

PWM 在嵌入式系统中的常见用途：

* **LED 亮度控制** — 占空比直接映射到感知亮度
* **直流电机速度控制** — 平均电压与占空比成正比
* **舵机定位** — 脉冲宽度编码期望角度
* **音频音调生成** — 变化频率产生可听音调
* **电源转换** — 降压/升压转换器和 D 类放大器

PWM 信号参数
*********************

PWM 信号由三个值描述：

* **周期** — 一个开/关周期的总持续时间，以纳秒为单位
* **脉冲宽度** — 高（有效）部分的持续时间，以纳秒为单位
* **占空比** — 脉冲宽度与周期的比率（以百分比表示）；50% 占空比意味着信号在半个周期内为高

.. code-block:: none

   |<-- pulse -->|
   +--------------+            +-
   |              |            |
   +              +------------+
   |<----------- period -------->|

Zephyr PWM 驱动程序模型
***********************

每个 PWM 控制器暴露一个或多个独立*通道*。通道由零基索引标识并驱动单个输出引脚。

所有 PWM 驱动程序实现在 :file:`include/zephyr/drivers/pwm.h` 中定义的相同 API。中心函数是 :c:func:`pwm_set`，它为通道编程周期和脉冲宽度。辅助宏将常见时间单位转换为纳秒：

* :c:macro:`PWM_HZ` — 以 Hz 为单位的频率（例如 ``PWM_HZ(1000)`` → 1 ms 周期）
* :c:macro:`PWM_KHZ` — 以 kHz 为单位的频率
* :c:macro:`PWM_USEC` — 以微秒为单位的周期或脉冲宽度
* :c:macro:`PWM_MSEC` — 以毫秒为单位的周期或脉冲宽度

设备树配置
*************************

PWM 引脚在设备树的 ``pwms`` 属性下描述。每个条目指定控制器句柄、通道号、以纳秒为单位的周期和可选极性标志：

.. code-block:: dts

   / {
       my_node {
           pwms = <&pwm0 0 PWM_MSEC(20) PWM_POLARITY_NORMAL>;
           pwm-names = "servo";
       };
   };

在 C 中，用 :c:macro:`PWM_DT_SPEC_GET` 宏系列获取规格：

.. code-block:: c

   static const struct pwm_dt_spec servo =
       PWM_DT_SPEC_GET(DT_NODELABEL(my_node));

使用示例
**************

用 ``pwm_dt_spec`` 设置占空比：

.. code-block:: c

   #include <zephyr/drivers/pwm.h>

   static const struct pwm_dt_spec led_pwm =
       PWM_DT_SPEC_GET(DT_ALIAS(pwm_led0));

   int set_led_brightness(uint8_t percent)
   {
       if (!device_is_ready(led_pwm.dev)) {
           return -ENODEV;
       }

       /* pulse = period * duty_cycle / 100 */
       uint32_t pulse = led_pwm.period / 100 * percent;

       return pwm_set_dt(&led_pwm, led_pwm.period, pulse);
   }

设置舵机位置（20 ms 周期内 1–2 ms 脉冲）：

.. code-block:: c

   #include <zephyr/drivers/pwm.h>

   #define SERVO_PERIOD_NS   PWM_MSEC(20)
   #define SERVO_MIN_PULSE   PWM_USEC(1000)
   #define SERVO_MAX_PULSE   PWM_USEC(2000)

   int set_servo_angle(const struct device *pwm_dev, uint32_t channel,
                       uint8_t angle_deg)
   {
       uint32_t pulse = SERVO_MIN_PULSE +
           (SERVO_MAX_PULSE - SERVO_MIN_PULSE) * angle_deg / 180;

       return pwm_set(pwm_dev, channel, SERVO_PERIOD_NS, pulse,
                      PWM_POLARITY_NORMAL);
   }

PWM 捕获
***********

某些 PWM 控制器支持*输入捕获*，它测量传入信号的周期和/或脉冲宽度。这对于解码来自外部源（如遥控接收器或传感器输出）的 PWM 信号有用。

用 :c:func:`pwm_configure_capture` 和 :c:func:`pwm_enable_capture` 启用捕获：

.. code-block:: c

   void pwm_capture_cb(const struct device *dev, uint32_t channel,
                       uint32_t period_cycles, uint32_t pulse_cycles,
                       int status, void *user_data)
   {
       if (status != 0) {
           return;
       }
       /* convert cycles to nanoseconds using pwm_get_cycles_per_sec() */
   }

   /* configure for single-shot capture of both period and pulse */
   pwm_configure_capture(dev, channel,
                         PWM_CAPTURE_TYPE_BOTH | PWM_CAPTURE_MODE_SINGLE,
                         pwm_capture_cb, NULL);
   pwm_enable_capture(dev, channel);

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_PWM`
* :kconfig:option:`CONFIG_PWM_SHELL`
* :kconfig:option:`CONFIG_PWM_CAPTURE`
* :kconfig:option:`CONFIG_PWM_EVENT`

API 参考
*************

.. doxygengroup:: pwm_interface

.. doxygengroup:: pwm_fake