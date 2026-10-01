.. _flash_api:

闪存
#####

概述
********

**闪存偏移量概念**

用户 API 使用的偏移量是相对于闪存内存起始地址表达的。此规则应适用于所有可通过 API 检索页面布局的闪存控制器常规内存（参见 :kconfig:option:`CONFIG_FLASH_PAGE_LAYOUT`）。

该规则的一个例外可应用于特定厂商的闪存专用区域（此类区域显然无法被页面布局检索 API 覆盖）。



用户 API 参考
******************
.. doxygengroup:: flash_interface

实现接口 API 参考
**************************************
.. doxygengroup:: flash_internal_interface
