.. _reset_api:

复位控制器
################

概述
********

复位控制器（reset controller）是控制发往多个外设的复位信号的单元。复位控制器 API 允许外设驱动程序请求对其复位输入信号的控制权，包括置位（assert）、取消置位（deassert）和翻转（toggle）这些信号的能力。此外，还可以检查复位输入信号的复位状态。

主要而言，line_assert 和 line_deassert 这两个 API 函数是可选的，因为在大多数情况下我们只需要翻转复位信号。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_RESET`

API 参考
*************

.. doxygengroup:: reset_controller_interface
