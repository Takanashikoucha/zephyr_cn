.. _otp_api:

OTP API
#######

概述
********

OTP API 提供了对 :abbr:`OTP(一次性可编程)` 内存设备进行配置（写入）和读取的手段。

API 实现参考
****************************
.. doxygengroup:: otp_interface

配置选项
*********************

OTP 相关配置选项：

* :kconfig:option:`CONFIG_OTP`
* :kconfig:option:`CONFIG_OTP_PROGRAM`
* :kconfig:option:`CONFIG_OTP_INIT_PRIORITY`
* :kconfig:option-regex:`CONFIG_OTP_SHELL.*`
