.. _emulators:

Zephyr 的设备模拟器/仿真器
####################################

概述
========

Zephyr 在其代码库中包含一组设备模拟器/仿真器。这里指的是与嵌入式软件一起构建、并向系统其余部分呈现为某一设备类别的设备软件组件。

这些设备模拟器/仿真器可以为任何具有足够 RAM 和 flash 的目标构建，即使其中某些可能带有仅在部分目标上可用的额外功能。

.. note::

   | Zephyr 还包含并使用许多其他类型的仿真器/模拟器，包括 CPU 和平台仿真器、无线电仿真器，以及若干允许在开发主机上运行嵌入式代码的构建目标。
   | Zephyr 的一些通信控制器/驱动也包括回环（loopback）模式或回环设备。
   | 本页不涵盖上述任何内容。

.. note::
   某些特定于平台的驱动（例如通过连接主机 API 来模拟某一外设类的 :ref:`native_sim 特定驱动 <native_sim_peripherals>`）不在本页涵盖范围之内。


可用的模拟器
===================

**ADC 模拟器**
  * 一个伪装成真实 ADC 的假驱动，可用于测试 ADC 设备的高层 API。
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_ADC_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,adc-emul`

**DMA 模拟器**
  * 模拟的 DMA 控制器
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_DMA_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,dma-emul`

**EEPROM 模拟器**
  * 在 flash 分区上模拟 EEPROM
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_EEPROM_EMULATOR`
  * 设备树绑定：:dtcompatible:`zephyr,emu-eeprom`

.. _emul_eeprom_simu_brief:

**EEPROM 仿真器**
  * 在 RAM 上模拟 EEPROM
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_EEPROM_SIMULATOR`
  * 设备树绑定：:dtcompatible:`zephyr,sim-eeprom`
  * 注意：对于 :zephyr:board:`native 目标 <native_sim>`，还可以将内容保留为主机文件系统上的文件。

**外部总线及总线连接外设模拟器**
  * :ref:`文档 <bus_emul>`
  * 允许模拟 I2C 或 SPI 等外部总线以及连接到这些总线的外设。

.. _emul_flash_simu_brief:

**flash 仿真器**
  * 在 RAM 上模拟 flash
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_FLASH_SIMULATOR`
  * 设备树绑定：:dtcompatible:`zephyr,sim-flash`
  * 注意：对于 native 目标，还可以将内容保留为主机文件系统上的文件。参见 :ref:`native_sim flash 仿真器部分 <nsim_per_flash_simu>`。

**GPIO 模拟器**
  * 可由软件驱动的模拟 GPIO 控制器
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_GPIO_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,gpio-emul`

**I2C 模拟器**
  * 模拟的 I2C 总线。参见 :ref:`总线模拟器 <bus_emul>`。
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_I2C_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,i2c-emul-controller`

**RTC 模拟器**
  * 模拟的 RTC 外设。参见 :ref:`RTC 模拟设备部分 <rtc_api_emul_dev>`
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_RTC_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,rtc-emul`

**SPI 模拟器**
  * 模拟的 SPI 总线。参见 :ref:`总线模拟器 <bus_emul>`。
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_SPI_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,spi-emul-controller`

**MSPI 模拟器**
  * 模拟的 MSPI 总线。参见 :ref:`总线模拟器 <bus_emul>`。
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_MSPI_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,mspi-emul-controller`

**UART 模拟器**
  * 模拟的 UART 总线。参见 :ref:`总线模拟器 <bus_emul>`。
  * 主要 Kconfig 选项：:kconfig:option:`CONFIG_UART_EMUL`
  * 设备树绑定：:dtcompatible:`zephyr,uart-emul`
