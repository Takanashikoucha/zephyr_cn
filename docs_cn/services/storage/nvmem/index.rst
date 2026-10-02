.. _nvmem:

非易失性存储器（NVMEM）
###########################

NVMEM 子系统为访问非易失性存储器设备提供通用接口。它抽象底层硬件，并提供统一的 API 用于读写数据。

关键概念
************

NVMEM 提供者
=============

NVMEM 提供者是暴露 NVMEM 单元（cell）的驱动。例如，EEPROM 驱动可以是一个 NVMEM 提供者。NVMEM 提供者负责向底层硬件读写数据。

NVMEM 单元
==========

NVMEM 单元是非易失性存储器的一块区域。它在设备树中定义，具有偏移量、大小和只读状态等属性。

NVMEM 消费方
=============

NVMEM 消费方是使用 NVMEM 单元存储或读取数据的驱动或应用程序。

配置
*************

* :kconfig:option:`CONFIG_NVMEM`：启用 NVMEM 子系统。
* :kconfig:option:`CONFIG_NVMEM_BBRAM`：启用对电池备份 RAM（Battery Backed RAM）的 NVMEM 支持。
* :kconfig:option:`CONFIG_NVMEM_EEPROM`：启用对 EEPROM 设备的 NVMEM 支持。
* :kconfig:option-regex:`CONFIG_NVMEM_FLASH.*`：配置对 flash 设备的 NVMEM 支持。
* :kconfig:option-regex:`CONFIG_NVMEM_OTP.*`：配置对 OTP 设备的 NVMEM 支持。

设备树绑定
*******************

NVMEM 子系统依赖设备树绑定来定义 NVMEM 单元。以下是在设备树中定义 NVMEM 提供者和单元的示例：

.. literalinclude:: devicetree_bindings.txt
   :language: dts

reg 属性是一个数组，包含：

* 创建该单元所在内存中的偏移量，
* 单元的大小，以字节为单位。

``#nvmem-cell-cells`` 描述 phandle 中属性项的数量，参见 :ref:`dt-bindings-cells`，通常设置为零。

消费方随后可以这样引用 NVMEM 单元：

.. literalinclude:: my_consumer.txt
   :language: dts


使用示例
*************

以下是使用 NVMEM API 从 NVMEM 单元读取数据的示例：

.. literalinclude:: usage_example.txt
   :language: c


API 参考
*************

.. doxygengroup:: nvmem_interface
