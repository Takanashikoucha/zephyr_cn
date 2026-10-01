.. _fuel_gauge_api:

电量计
##########

电量计子系统提供一个 API，用于统一访问电池电量计设备。

基本操作
***************

属性
==========

从根本上说，属性是电量计设备可以测量的量。

电量计通常支持多个属性，例如电池组的温度读数或实时电流/电压。

属性由客户端使用 :c:func:`fuel_gauge_get_prop` 逐个获取，或使用 :c:func:`fuel_gauge_get_props` 批量获取。缓冲区属性（例如设备名称）使用 :c:func:`fuel_gauge_get_buffer_prop` 获取。

属性由客户端使用 :c:func:`fuel_gauge_set_prop` 逐个设置，或使用 :c:func:`fuel_gauge_set_props` 批量设置。缓冲区属性（例如电池配置镜像）使用 :c:func:`fuel_gauge_set_buffer_prop` 设置。


电池截止
==============

许多嵌入电池包中的电量计暴露一个寄存器地址，向该地址写入特定数据时会执行电池截止。该电池截止通常被称为出货模式、搁置模式或睡眠模式，因为它在设备存储或运输期间减少电池消耗方面非常实用。

电量计 API 通过 :c:func:`fuel_gauge_battery_cutoff` 函数提供电池截止功能。

缓存
=======

电量计 API 明确不为其客户端提供缓存。


.. _fuel_gauge_api_reference:

API 参考
*************

.. doxygengroup:: fuel_gauge_interface
.. doxygengroup:: fuel_gauge_emulator_backend
