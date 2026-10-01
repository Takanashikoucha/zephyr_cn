.. _buzzer_api:

蜂鸣器
######

蜂鸣器子系统暴露一个 API，用于统一驱动蜂鸣器硬件，
无论底层部件是由 PWM 通道驱动的无源压电蜂鸣器，
还是由单个 GPIO 引脚控制的有源蜂鸣器。

基本操作
***************

应用通过设备树（devicetree）获取蜂鸣器设备，
并通过 :zephyr_file:`include/zephyr/drivers/buzzer.h` 中的函数驱动它：

蜂鸣器 API 调用不会等待所请求的音调持续时间。持续时间描述的是
硬件应保持发声多长时间，而不是调用线程应睡眠多长时间；
使用 :c:macro:`BUZZER_DURATION_FOREVER` 可一直播放，直到显式停止。

- :c:func:`buzzer_tone` 以特定频率播放持续特定时间的音调。硬件会按请求的持续时间
  持续发声，随后驱动会自动将其静音。
- :c:func:`buzzer_beep` 播放蜂鸣器的自然工作频率，该频率由板级文件
  编码在 ``pwms`` 设备树属性的周期（period）单元中（通常是压电元件的机械共振频率，
  即该部件能产生的最响音调）。对于有源蜂鸣器，该调用等效于
  将 GPIO 引脚置高电平，因为实际音高由硬件振荡器决定。
- :c:func:`buzzer_set_volume` 调整感知响度。零值立即静音；非零值
  会被保存，并在下一次播放音调时应用。有源蜂鸣器没有模拟音量控制，
  因此将零值映射为静音，将任何非零值映射为其唯一可听音量等级。
- :c:func:`buzzer_stop` 立即取消任何正在进行的音调。

后端
********

提供两种可通过设备树发现的后端：

- :dtcompatible:`pwm-buzzer` 用于由 PWM 通道驱动的无源压电蜂鸣器。
  PWM 通道的周期决定音频频率，占空比（duty cycle）决定感知音量；
  驱动从应用的音调和音量请求中派生出这两者。
- :dtcompatible:`gpio-buzzer` 用于通过单个 GPIO 驱动的有源蜂鸣器。
  驱动对任何非零频率将该引脚置高，
  对 :c:macro:`BUZZER_FREQ_REST` 则将其置低。

API 参考
*************

.. doxygengroup:: buzzer_interface
