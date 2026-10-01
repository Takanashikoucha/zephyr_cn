.. _peci_api:

平台环境控制接口（PECI）
#############################################

概述
********
平台环境控制接口（Platform Environment Control Interface，缩写为 PECI）是一种热管理标准，于 2006 年随 Intel Core 2 Duo 微处理器推出。
PECI 接口允许外部设备读取处理器温度、执行处理器可管理性功能，并管理处理器接口的调优与诊断。
PECI 总线驱动 API 实现了嵌入式微控制器与 CPU 之间的交互。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_PECI`

API 参考
*************

.. doxygengroup:: peci_interface
