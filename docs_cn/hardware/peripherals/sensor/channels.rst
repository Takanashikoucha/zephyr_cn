.. _sensor-channel:

传感器通道
###############

:dfn:`通道`，在 :c:enum:`sensor_channel` 中枚举，是传感器设备可以测量的量。

传感器可以有多个通道，要么用于表示同一物理量的不同轴（例如加速度）；要么因为它们
可以测量完全不同的属性（环境温度、压力和湿度）。传感器也可以有同一测量类型的多个
通道，以便测量大量读数，例如温度、光强度、电流、电压或电容。

在 Zephyr 中，通道使用 :c:struct:`sensor_chan_spec` 指定，它是一个包含通道类型
（:c:enum:`sensor_channel`）和通道索引的对。有时只使用 :c:enum:`sensor_channel`，
但自 Zephyr 3.7 引入 :c:struct:`sensor_chan_spec` 之后，这种做法应被视为历史遗留。
