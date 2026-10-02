.. _blinfo_api:

引导加载器信息
######################

引导加载器信息（缩写为 blinfo）子系统是 :ref:`retention_api` 的扩展，允许从引导加载器读取共享数据，并允许应用程序查询它。它有一个可选特性：将从引导加载器获取的信息进行组织，并以 ``blinfo/`` 前缀存储在 :ref:`settings_api` 中。

设备树配置
****************

要使用引导加载器信息子系统，需要创建一个 retention 区域，其父节点是一个保留数据（retained data）段，通常使用 non-init RAM 来实现这一目的。参见以下示例（本指南中的示例基于 :zephyr:board:`nrf52840dk` 板级及其内存布局）：

.. code-block:: devicetree

	/ {
		sram@2003FC00 {
			compatible = "zephyr,memory-region", "mmio-sram";
			reg = <0x2003FC00 DT_SIZE_K(1)>;
			zephyr,memory-region = "RetainedMem";
			status = "okay";

			retainedmem {
				compatible = "zephyr,retained-ram";
				status = "okay";
				#address-cells = <1>;
				#size-cells = <1>;

				boot_info0: boot_info@0 {
					compatible = "zephyr,retention";
					status = "okay";
					reg = <0x0 0x100>;
				};
			};
		};

		chosen {
			zephyr,bootloader-info = &boot_info0;
		};
	};


	/* 减少 SRAM0 使用量 1KB，以容纳 non-init 区域 */
	&sram0 {
		reg = <0x20000000 DT_SIZE_K(255)>;
	};

注意，该配置必须同时应用于引导加载器（MCUboot）和应用程序才能使用。它可以与其他 retention 系统 API（例如 :ref:`boot_mode_api`）组合使用。

MCUboot 配置
*************

应用上述设备树配置后，MCUboot 需要被配置为将共享数据存储在该区域，为此需要设置以下 Kconfig：

* :kconfig:option:`CONFIG_RETAINED_MEM` — 启用保留内存驱动
* :kconfig:option:`CONFIG_RETENTION` — 启用 retention 系统
* :kconfig:option:`CONFIG_BOOT_SHARE_DATA` — 启用共享数据
* :kconfig:option:`CONFIG_BOOT_SHARE_DATA_BOOTINFO` — 启用 boot 信息
  共享数据类型
* :kconfig:option:`CONFIG_BOOT_SHARE_BACKEND_RETENTION` — 使用
  retention/blinfo 子系统存储共享数据

应用程序配置
*****************

应用程序必须启用以下基础 Kconfig 选项，引导加载器信息子系统才能工作：

* :kconfig:option:`CONFIG_RETAINED_MEM`
* :kconfig:option:`CONFIG_RETENTION`
* :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO`
* :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO_TYPE_MCUBOOT`

使用引导加载器信息子系统需要以下头文件包含：

.. code-block:: C

	#include <zephyr/retention/blinfo.h>

默认情况下，只提供查找函数：:c:func:`blinfo_lookup`，
应用程序可以调用该函数从引导加载器查询信息。该函数默认由
:kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO_OUTPUT_FUNCTION` 启用，不过，
应用程序也可以选择改用 settings 存储特性。
在该模式下，可以通过使用 settings 键来查询引导加载器信息，
该模式需要启用以下 Kconfig 选项：

* :kconfig:option:`CONFIG_SETTINGS`
* :kconfig:option:`CONFIG_SETTINGS_RUNTIME`
* :kconfig:option:`CONFIG_RETENTION_BOOTLOADER_INFO_OUTPUT_SETTINGS`

这使得可以通过
:c:func:`settings_runtime_get` 函数使用以下键查询信息：

* ``blinfo/mode`` MCUboot 被配置的模式
  （``enum mcuboot_mode`` 值）
* ``blinfo/signature_type`` MCUboot 被配置的签名类型
  （``enum mcuboot_signature_type`` 值）
* ``blinfo/recovery`` MCUboot 中启用的恢复类型
  （``enum mcuboot_recovery_mode`` 值）
* ``blinfo/running_slot`` 正在运行的 slot，对于 direct-XIP 模式有用，
  用于知道更新时应使用哪个 slot
* ``blinfo/bootloader_version`` 引导加载器的版本
  （``struct image_version`` 对象）
* ``blinfo/max_application_size`` 可加载应用程序的最大大小（字节）

除之前的头文件包含外，该模式还需要以下头文件包含：

.. code-block:: C

	#include <bootutil/boot_status.h>
	#include <bootutil/image.h>
	#include <zephyr/mcuboot_version.h>
	#include <zephyr/settings/settings.h>

API 参考
*************

引导加载器信息 API
==========================

.. doxygengroup:: bootloader_info_interface
