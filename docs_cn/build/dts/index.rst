.. _devicetree:

设备树
##########

*设备树*（devicetree）是一种主要用于描述硬件的
层次化数据结构。Zephyr 以两种主要方式使用设备树：

- 向 :ref:`device_model_api` 描述硬件
- 提供该硬件的初始配置

本页链接到设备树的高层指南以及
参考材料。

.. _dt-guide:

设备树指南
****************

本节的页面是使用设备树进行 Zephyr
开发的高层指南。

.. toctree::
   :maxdepth: 2

   intro.rst
   design.rst
   bindings.rst
   api-usage.rst
   phandles.rst
   zephyr-user-node.rst
   howtos.rst
   troubleshooting.rst
   dt-vs-kconfig.rst

.. _dt-reference:

设备树参考
********************

这些页面包含 Zephyr 设备树 API 和
内置绑定的参考材料。

平台无关的细节见 `设备树规范`_。

.. _设备树规范: https://www.devicetree.org/

.. 这里使用 ":glob:" 和 "*" 来添加生成的绑定页面。

.. toctree::
   :maxdepth: 3
   :glob:

   api/*
