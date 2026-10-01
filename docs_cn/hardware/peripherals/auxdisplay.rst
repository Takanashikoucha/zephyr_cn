.. _auxdisplay_api:

辅助显示（auxdisplay）
##############################

概述
********

辅助显示（Auxiliary Display）是基于文本的显示设备，具有简单的接口，用于显示文本、数字或字母数字数据。与 :ref:`display_api` 不同，辅助显示不支持向显示设备输出自定义图形（且大多为单色显示），其支持的最先进的自定义功能是生成自定义字符。这些低成本显示设备通常有多种配置和尺寸，常见的显示尺寸为 16 字符 × 2 行。

此 API 尚不稳定，可能会发生变化。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_AUXDISPLAY`
* :kconfig:option:`CONFIG_AUXDISPLAY_INIT_PRIORITY`

API 参考
*************

.. doxygengroup:: auxdisplay_interface
