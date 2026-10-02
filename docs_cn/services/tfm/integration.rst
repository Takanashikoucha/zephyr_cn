Trusted Firmware-M Integration
##############################

Trusted Firmware-M (TF-M) 章节包含有关 TF-M 与 Zephyr RTOS 之间集成方式的信息。利用这些信息可以理解如何在 Cortex-M 平台上将 TF-M 与 Zephyr 集成，并在 Zephyr 应用中使用其安全运行时服务。

Board Definitions
*****************

当 :kconfig:option:`CONFIG_BUILD_WITH_TFM` 标志设置为 ``y`` 时，TF-M 将与安全处理环境一起、与 Zephyr 一同构建。

一般来说，该值绝不应该在应用层设置，所有 TF-M 所需的配置项都应在带 ``_ns`` 后缀的板级变体中设置。

该板级变体必须定义合适的 flash、SRAM 和外设配置，并考虑安全处理环境中的初始化过程。还必须通过 `modules/trusted-firmware-m/Kconfig.tfm <https://github.com/zephyrproject-rtos/zephyr/blob/main/modules/trusted-firmware-m/Kconfig.tfm>`__ 将 :kconfig:option:`CONFIG_TFM_BOARD` 设置为 TF-M 针对该目标所期望的板级名称，使其知道应该为安全处理环境构建哪个目标。

Example: ``mps2/an521/cpu0/ns``
===============================

``mps2/an521/cpu0`` 板级目标是一款双核 Arm Cortex-M33 评估板，它生成一个安全的 Zephyr 二进制文件。

不过，可选的 ``mps2/an521/cpu0/ns`` 板级目标会额外设置以下 kconfig 标志，表示 Zephyr 应作为非安全镜像构建，作为外部项目与 TF-M 链接，并可选地包含安全引导加载器：

* :kconfig:option:`CONFIG_TRUSTED_EXECUTION_NONSECURE` ``y``
* :kconfig:option:`CONFIG_ARM_TRUSTZONE_M` ``y``

对比 :zephyr_file:`boards/arm/mps2/mps2_an521_cpu0.dts` 和 :zephyr_file:`boards/arm/mps2/mps2_an521_cpu0_ns.dts` 两个文件，可以看到 ``ns`` 版本在 flash 和 SRAM 内存中定义了偏移量，为 TF-M 和安全引导加载器留出所需的空间：

::

    reserved-memory {
        #address-cells = <1>;
        #size-cells = <1>;
        ranges;

        /* The memory regions defined below must match what the TF-M
         * project has defined for that board - a single image boot is
         * assumed. Please see the memory layout in:
         * https://git.trustedfirmware.org/TF-M/trusted-firmware-m.git/tree/platform/ext/target/mps2/an521/partition/flash_layout.h
         */

        code: memory@100000 {
            reg = <0x00100000 DT_SIZE_K(512)>;
        };

        ram: memory@28100000 {
            reg = <0x28100000 DT_SIZE_M(1)>;
        };
    };

这为安全启动和 TF-M 保留了 1 MB 代码内存和 1 MB RAM，因此非安全 Zephyr 应用代码从 0x10000 开始，RAM 位于 0x28100000。NS zephyr 镜像有 512 KB 代码内存可用，外加 1 MB RAM。

这与 TF-M ``flash_layout.h`` 中看到的 flash 内存布局一致：

::

    * 0x0000_0000 BL2 - MCUBoot (0.5 MB)
    * 0x0008_0000 Secure image     primary slot (0.5 MB)
    * 0x0010_0000 Non-secure image primary slot (0.5 MB)
    * 0x0018_0000 Secure image     secondary slot (0.5 MB)
    * 0x0020_0000 Non-secure image secondary slot (0.5 MB)
    * 0x0028_0000 Scratch area (0.5 MB)
    * 0x0030_0000 Protected Storage Area (20 KB)
    * 0x0030_5000 Internal Trusted Storage Area (16 KB)
    * 0x0030_9000 NV counters area (4 KB)
    * 0x0030_A000 Unused (984 KB)

``mps2/an521`` 将作为板级目标传递给 Tf-M，通过 :kconfig:option:`CONFIG_TFM_BOARD` 指定。
