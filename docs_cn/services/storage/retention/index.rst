.. _retention_api:

Retention（数据保留）系统
################

Retention 系统提供一个 API，允许应用程序从在设备供电期间保留数据的内存区域或设备中读写数据。这使得可以在不同应用程序之间或在单个应用程序内共享信息，而在设备重启时不会丢失状态信息。所存储的数据在发生电源故障（或在某些设备上某些低功耗模式期间）时不应持久保存，也不应存储到 :ref:`flash_api`、:ref:`eeprom_api` 或电池备份 RAM 等非易失性存储中。

Retention 系统构建在 retained data（保留数据）驱动之上，并为其添加额外的软件层特性以确保数据的有效性。可选地，可以使用一个 magic header（魔数头）来检查保留数据内存段的开头是否包含该特定值；还可以将所存储数据的可选校验和（大小为 1、2 或 4 字节）追加到数据末尾。此外，retention 系统 API 允许将保留数据段划分为多个不同的区域。例如，一个 64 字节的保留数据区域可以拆分为 4 字节用于 boot mode、16 字节用于时间戳、44 字节用于最后一条日志消息。所有这些段都可以独立访问或更新。前缀（prefix）和校验和可以通过设备树按实例（per-instance）设置。

设备树配置
****************

要使用 retention 系统，必须为你正在使用的板级设置一个 retained data 驱动；有一个 Zephyr 驱动可以使用，它会将一部分 RAM 作为 non-init 区域用于此目的。然后 retention 系统作为该设备的子节点被初始化一次或多次——注意，内存区域需要相应减少，以计入这部分预留的 RAM。参见以下示例（本指南中的示例基于 :zephyr:board:`nrf52840dk` 板级及其内存布局）：

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

				/* 这创建一个 256 字节的分区 */
				retention0: retention@0 {
					compatible = "zephyr,retention";
					status = "okay";

					/* 该区域的总大小为 256
					 * 字节，包含前缀和校验和，
					 * 这意味着可用的数据存储区域为
					 * 256 - 3 = 253 字节
					 */
					reg = <0x0 0x100>;

					/* 这是必须出现在数据开头的前缀
					 */
					prefix = [08 04];

					/* 这里使用 1 字节校验和 */
					checksum = <1>;
				};

				/* 这创建一个 768 字节的分区 */
				retention1: retention@100 {
					compatible = "zephyr,retention";
					status = "okay";

					/* 起始位置必须位于上一个分区结束之后。
					 * 该区域的总大小为 768 字节，
					 * 包含前缀和校验和，
					 * 这意味着可用的数据存储区域为
					 * 768 - 6 = 762 字节
					 */
					reg = <0x100 0x300>;

					/* 这是必须出现在数据开头的前缀
					 */
					prefix = [00 11 55 88 fa bc];

					/* 如果省略，则没有校验和
					 */
				};
			};
		};
	};

	/* 减少 SRAM0 使用量 1KB，以容纳 non-init 区域 */
	&sram0 {
		reg = <0x20000000 DT_SIZE_K(255)>;
	};

然后，retention 区域可以通过数据保留 API 访问（前提是通过 :kconfig:option:`CONFIG_RETENTION` 启用，
这要求启用 :kconfig:option:`CONFIG_RETAINED_MEM`），方式为：

.. code-block:: C

	#include <zephyr/device.h>
	#include <zephyr/retention/retention.h>

	const struct device *retention0 = DEVICE_DT_GET(DT_NODELABEL(retention0));
	const struct device *retention1 = DEVICE_DT_GET(DT_NODELABEL(retention1));

当写函数被调用时，magic header 和校验和（如果启用）将被设置到该区域，
从那一刻起该区域将被标记为有效。

互斥锁保护
****************

当应用程序以多线程支持编译时，retention 区域的互斥锁保护默认启用。这意味着不同线程可以安全地调用 retention 函数，而不会与其他并发线程的函数使用发生冲突；但也意味着 retention 函数不能从中断（ISR）中使用。可以通过启用 :kconfig:option:`CONFIG_RETENTION_MUTEX_FORCE_DISABLE` 全局禁用所有 retention 区域的互斥锁保护——此时用户负责确保函数调用之间不发生冲突。注意，要使用此选项，还必须通过启用 :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE` 禁用 retention 驱动的互斥锁支持。

.. _boot_mode_api:

Boot mode
*********

Retention 子系统的一个附加内容是 boot mode 接口，它可以在设备重启时用于动态更改应用程序的状态，或运行一个不同的应用程序（带有一组最小的函数；一个示例是从主应用程序以无按钮的方式进入 mcuboot 的 serial recovery 特性）。

要使用 boot mode 特性，设备树中必须存在一个数据保留项，专门用于 boot mode 选择（用户区域数据大小只需一个字节），并且该区域被分配给 ``zephyr,boot-mode`` 的 chosen 节点。参见以下示例：

.. code-block:: devicetree

	/ {
		sram@2003FFFF {
			compatible = "zephyr,memory-region", "mmio-sram";
			reg = <0x2003FFFF 0x1>;
			zephyr,memory-region = "RetainedMem";
			status = "okay";

			retainedmem {
				compatible = "zephyr,retained-ram";
				status = "okay";
				#address-cells = <1>;
				#size-cells = <1>;

				retention0: retention@0 {
					compatible = "zephyr,retention";
					status = "okay";
					reg = <0x0 0x1>;
				};
			};
		};

		chosen {
			zephyr,boot-mode = &retention0;
		};
	};

	/* 减少 SRAM0 使用量 1 字节，以容纳 non-init 区域 */
	&sram0 {
		reg = <0x20000000 0x3FFFF>;
	};

boot mode 接口可以通过 :kconfig:option:`CONFIG_RETENTION_BOOT_MODE` 启用，然后使用 boot mode 函数访问。如果在使用 mcuboot 的 serial recovery，可以以启用 ``CONFIG_MCUBOOT_SERIAL`` 和 ``CONFIG_BOOT_SERIAL_BOOT_MODE`` 构建，这样就可以使用以下方式直接重启进入 serial recovery 模式：

.. code-block:: C

	#include <zephyr/retention/bootmode.h>
	#include <zephyr/sys/reboot.h>

	bootmode_set(BOOT_MODE_TYPE_BOOTLOADER);
	sys_reboot(0);

Retention 系统模块
************************

模块可以通过将 retention 系统用作传输层（例如在引导加载器和应用程序之间）来扩展其功能。

.. toctree::
    :maxdepth: 1

    blinfo.rst

API 参考
*************

Retention 系统 API
===================

.. doxygengroup:: retention_api

Boot mode 接口
==================

.. doxygengroup:: boot_mode_interface
