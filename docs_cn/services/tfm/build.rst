.. _tfm_build_system:

TF-M Build System
#################

在构建一个有效的 ``_ns`` 板级目标时，TF-M 会在后台被构建，并与 Zephyr 非安全应用一起链接。大多数情况下无需了解 TF-M 的构建系统，下面这条命令即可构建 TF-M 与 Zephyr 镜像对，并在 qemu 中运行，无需任何额外步骤：

   .. code-block:: bash

     $ west build -p auto -b mps2/an521/cpu0/ns samples/tfm_integration/psa_protected_storage/ -t run

构建过程的输出和某些关键步骤在此处说明，不过由于你需要理解并处理这些输出，并且在部署前对安全镜像和非安全镜像进行签名，因此了解这些内容仍然很有必要。

Images Created by the TF-M Build
********************************

TF-M 构建系统会创建以下可执行文件：

* tfm_s - TF-M 安全固件
* tfm_ns - TF-M 非安全应用（仅用于回归测试）
* bl2 - TF-M MCUboot（如果启用）

对于其中每一个，都会创建 .bin、.hex、.elf 和 .axf 文件。

TF-M 构建系统还会创建 tfm_s 和 tfm_ns 的签名版本，以及一个将两者合并的文件：

* tfm_s_signed
* tfm_ns_signed
* tfm_s_ns_signed

对于其中每一个，只会创建 .bin 文件。

除了运行 TF-M 回归测试套件之外，TF-M 非安全应用会被丢弃，改用 Zephyr 非安全应用。

Zephyr 构建系统通常会对 tfm_s 和 Zephyr 非安全应用本身都进行签名。详情见下文。

"tfm" 目标包含所有这些路径的属性。例如，下面这条表达式将解析为 ``<path>/tfm_s.hex``：

   .. code-block::

      $<TARGET_PROPERTY:tfm,TFM_S_HEX_FILE>

参见 tfm 模块顶层的 CMakeLists.txt 文件，可以了解所有属性的概览。

Signing Images
**************

当 :kconfig:option:`CONFIG_TFM_BL2` 设置为 ``y`` 时，TF-M 会使用一个安全引导加载器（BL2），固件镜像必须用私钥签名。在更新过程中，引导加载器会使用对应的公钥验证固件镜像，该公钥存储在安全引导加载器固件镜像内部。

默认情况下，使用 ``<tfm-dir>/bl2/ext/mcuboot/root-rsa-3072.pem`` 对安全镜像进行签名，使用 ``<tfm-dir>/bl2/ext/mcuboot/root-rsa-3072_1.pem`` 对非安全镜像进行签名。这些默认 .pem 密钥可以（而且**应该**）通过 :kconfig:option:`CONFIG_TFM_KEY_FILE_S` 和 :kconfig:option:`CONFIG_TFM_KEY_FILE_NS` 配置项覆盖。

为了满足 `PSA Certified Level 1`_ 的要求，**你必须用新的密钥对替换默认 .pem 文件！**

要生成新的公钥/私钥对，运行以下命令：

   .. code-block:: bash

     $ imgtool keygen -k root-rsa-3072_s.pem -t rsa-3072
     $ imgtool keygen -k root-rsa-3072_ns.pem -t rsa-3072

之后你可以将新的 .pem 文件放到其他位置（例如你的 Zephyr 应用目录），并通过 :kconfig:option:`CONFIG_TFM_KEY_FILE_S` 和 :kconfig:option:`CONFIG_TFM_KEY_FILE_NS` 配置项在 ``prj.conf`` 文件中引用它们。

   .. warning::

      务必将私钥文件保存在安全、可靠的位置！如果你丢失了这个密钥文件，将无法再对任何后续固件镜像进行签名，设备在现场也将无法再更新！

内置签名脚本运行后，会创建一个 ``tfm_merged.hex``（以及 ``tfm_merged.bin``）文件，其中包含全部三个二进制文件：bl2、tfm_s 和 zephyr 应用。之后可以将这些文件烧录到开发板，或在 QEMU 中运行。

.. _PSA Certified Level 1:
  https://www.psacertified.org/security-certification/psa-certified-level-1/
.. _PSA Certified Firmware Update API:
  https://arm-software.github.io/psa-api/fwu/

Output Files
************

Zephyr TF-M 构建完成后，将存在以下输出文件：

.. csv-table:: TF-M Output Files
  :header: Filename, Created From, Bootloader Flags, Usage

  ``tfm_s_signed.{hex/bin}``, "TF-M Secure", Signed, OTA Upgrades (:kconfig:option:`CONFIG_TFM_MCUBOOT_IMAGE_NUMBER` == 2)
  ``zephyr_ns_signed.{hex/bin}``, "Zephyr Nonsecure", Signed, OTA Upgrades (:kconfig:option:`CONFIG_TFM_MCUBOOT_IMAGE_NUMBER` == 2)
  ``tfm_s_zephyr_ns_signed.{hex/bin}``, "TF-M Secure, Zephyr Nonsecure", Signed, OTA Upgrades (:kconfig:option:`CONFIG_TFM_MCUBOOT_IMAGE_NUMBER` == 1)
  ``tfm_merged.{hex/bin}``, "Bootloader, TF-M Secure, Zephyr Nonsecure", "Signed, Confirmed", "Production Programming, flashed by ``west flash``"

Custom CMake arguments
======================

在构建带 TF-M 的 Zephyr 应用时，可能需要控制传递给 TF-M 构建的 CMake 参数。

Zephyr TF-M 构建提供了一些用于控制构建的 Kconfig 选项，但并不能覆盖 TF-M 构建系统支持的所有 CMake 参数。

``zephyr_property_target`` 上的 ``TFM_CMAKE_OPTIONS`` 属性可用于向 TF-M 构建系统传递自定义 CMake 参数。

要向 TF-M 构建系统传递 CMake 参数 ``-DFOO=bar``，请在 CMakeLists.txt 文件中放入以下 CMake 代码段。

   .. code-block:: cmake

     set_property(TARGET zephyr_property_target
                  APPEND PROPERTY TFM_CMAKE_OPTIONS
                  -DFOO=bar
     )

.. note::
   ``TFM_CMAKE_OPTIONS`` 是一个列表，因此可以追加多个选项。同时支持 CMake 生成器表达式，例如 ``$<1:-DFOO=bar>``。

由于 ``TFM_CMAKE_OPTIONS`` 是列表参数，在传递给 TF-M 构建系统之前会先被展开。因此，带有列表参数的选项必须正确转义，以避免被当作列表展开。

   .. code-block:: cmake

     set_property(TARGET zephyr_property_target
                  APPEND PROPERTY TFM_CMAKE_OPTIONS
                  -DFOO="bar\\\;baz"
     )

Footprint and Memory Usage
**************************

构建系统提供了用于查看和分析生成镜像中 RAM 和 ROM 用量的目标。这些工具运行在最终镜像上，给出 RAM 和 ROM 中各符号及代码大小的信息。关于这些工具的更多信息，请参见：:ref:`footprint_tools`

使用 ``tfm_ram_report`` 获取 TF-M 安全固件（tfm_s）的 RAM 报告。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: tfm_ram_report

使用 ``tfm_rom_report`` 获取 TF-M 安全固件（tfm_s）的 ROM 报告。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: tfm_rom_report

使用 ``bl2_ram_report`` 获取 TF-M MCUboot 的 RAM 报告（如果启用）。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: bl2_ram_report

使用 ``bl2_rom_report`` 获取 TF-M MCUboot 的 ROM 报告（如果启用）。

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: mps2/an521/cpu0/ns
    :goals: bl2_rom_report
