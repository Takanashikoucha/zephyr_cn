.. _build-signing:

签名二进制文件
################

二进制文件可以选择在构建时自动使用 CMake 代码进行签名，也可以使用 ``west sign`` 来签名二进制文件。
本页描述前者，后者记录在 :ref:`west-sign` 中。

MCUboot / imgtool
*****************

Zephyr 构建系统对使用其开发者提供的 `imgtool`_ 程序为 `MCUboot`_ 引导加载器签名二进制文件有特殊支持。
你可以通过设置一些 Kconfig 选项，在一个步骤中构建并签名这种类型的应用二进制文件。
如果你这样做，``west flash`` 将使用签名后的二进制文件。

这里是一个示例工作流程，构建并烧录 MCUboot，以及供 MCUboot 链加载的
:zephyr:code-sample:`hello_world` 应用。从你在 :ref:`getting_started` 中创建的
:file:`zephyrproject` 工作区运行这些命令：

.. code-block:: console

   west build -b YOUR_BOARD zephyr/samples/hello_world --sysbuild -d build-hello-signed -- \
       -DSB_CONFIG_BOOTLOADER_MCUBOOT=y

   west flash -d build-hello-signed

上面命令的注意事项：

- ``YOUR_BOARD`` 应更改为你的开发板
- 签名密钥值是 MCUboot 为开发和测试提供并使用的不安全默认值
- 你可以将 ``hello_world`` 应用目录更改为任何可被 MCUboot 加载的其他应用，
  例如 :zephyr:code-sample:`smp-svr` 示例。

关于这些和其他相关配置选项的更多信息，见：

- :kconfig:option:`SB_CONFIG_BOOTLOADER_MCUBOOT`：构建供 MCUboot 加载的应用
- :kconfig:option:`SB_CONFIG_BOOT_SIGNATURE_KEY_FILE`：签名镜像时使用的密钥文件，或逗号分隔的
  密钥文件列表。如果你有自己密钥，请相应更改；使用绝对路径或 ``${APP_DIR}`` 这样的 CMake
  变量参见 :ref:`build-signing-keys`。
  给出列表时，MCUboot 嵌入每个密钥的公钥部分，并接受用其中任何一个签名的镜像；
  第一个条目也用于签名应用，第一个之后的每个条目必须是相同签名类型的仅公钥 PEM 供
  ``imgtool`` 使用。
- :kconfig:option:`CONFIG_MCUBOOT_EXTRA_IMGTOOL_ARGS`：``imgtool`` 的可选附加命令行参数
- :kconfig:option:`CONFIG_MCUBOOT_GENERATE_CONFIRMED_IMAGE`：也生成一个已确认镜像，
  它可能比可 OTA 的默认镜像更适合在生产环境中烧录
- 在 Windows 上，如果你遇到 "Access denied" 问题，推荐的修复方法是运行
  ``pip3 install imgtool``，然后用干净的构建目录重试。

关于在 QEMU 下端到端验证多密钥引导加载器的完整示例，见
:zephyr_file:`tests/boot/mcuboot_multiple_keys` 测试。

如果你的 ``west flash`` :ref:`runner <west-runner>` 使用 imgtool 支持的镜像格式，
运行 ``west flash -d build-hello-signed`` 时，你应该在设备的串口控制台上看到类似以下内容：

.. code-block:: none

   *** Booting Zephyr OS build zephyr-v2.3.0-2310-gcebac69c8ae1  ***
   [00:00:00.004,669] <inf> mcuboot: Starting bootloader
   [00:00:00.011,169] <inf> mcuboot: Primary image: magic=unset, swap_type=0x1, copy_done=0x3, image_ok=0x3
   [00:00:00.021,636] <inf> mcuboot: Boot source: none
   [00:00:00.027,374] <inf> mcuboot: Swap type: none
   [00:00:00.115,142] <inf> mcuboot: Bootloader chainload address offset: 0xc000
   [00:00:00.123,168] <inf> mcuboot: Jumping to the first image slot
   *** Booting Zephyr OS build zephyr-v2.3.0-2310-gcebac69c8ae1  ***
   Hello World! nrf52840dk_nrf52840

``west flash`` 是否支持此功能取决于你的 runner。``nrfjprog`` 和
``pyocd`` runner 与上面的流程配合工作。如果你的 runner 不支持此流程且你希望它支持，
请发送补丁或提交 issue 以添加支持。

.. _build-signing-keys:

签名密钥文件
*****************

使用 sysbuild 构建时，:kconfig:option:`SB_CONFIG_BOOT_SIGNATURE_KEY_FILE` 选择用于签名镜像的密钥。
其值传播到两个镜像：

- 应用镜像，作为 :kconfig:option:`CONFIG_MCUBOOT_SIGNATURE_KEY_FILE`，``imgtool`` 用它签名应用；
  以及
- MCUboot 镜像，作为 ``CONFIG_BOOT_SIGNATURE_KEY_FILE``，其公钥部分被构建到引导加载器中
  以验证该签名。

.. warning::

   默认值指向与 MCUboot 捆绑的不安全开发密钥之一（例如 :file:`root-ec-p256.pem`）。
   这些密钥是公开的——它们随每个 Zephyr 和 MCUboot checkout 一起分发——因此只适合开发和测试。
   对于其他任何用途，请生成你自己的密钥，并将私钥保持在任何你不控制的仓库或构建目录之外。

sysbuild 如何解析密钥文件路径
=======================================

:kconfig:option:`SB_CONFIG_BOOT_SIGNATURE_KEY_FILE` 的值使用 CMake 的
``string(CONFIGURE)`` 命令处理，因此其中包含的任何 ``${VARIABLE}`` 引用在使用路径前
都会作为 CMake 变量展开。展开后，绝对路径按原样使用；相对路径由每个镜像独立解析：

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 镜像
     - 相对路径的搜索顺序
   * - 应用（:kconfig:option:`CONFIG_MCUBOOT_SIGNATURE_KEY_FILE`）
     - ``APPLICATION_CONFIG_DIR``，然后 west 工作区 topdir（``WEST_TOPDIR``）
   * - MCUboot（``CONFIG_BOOT_SIGNATURE_KEY_FILE``）
     - ``APPLICATION_CONFIG_DIR``，然后 MCUboot 模块目录

.. warning::

   每个镜像相对于不同的基础解析相对路径，因此裸相对路径对每个镜像指向不同的文件，
   通常导致构建失败。不要使用裸相对路径：请给出绝对路径，或用 CMake 变量锚定路径。

``${APP_DIR}``（主应用的源目录）是推荐的锚点：它将密钥保持在你自己的应用内，
且两个镜像都将其解析为相同的文件。值展开时可用的任何 CMake 变量都可以使用：

.. code-block:: cfg

   # sysbuild.conf
   SB_CONFIG_BOOT_SIGNATURE_KEY_FILE="${APP_DIR}/keys/my-signing-key.pem"

相同的解析规则也适用于可选的加密密钥文件（:kconfig:option:`CONFIG_MCUBOOT_ENCRYPTION_KEY_FILE`）。

.. _west-extending-signing:

从外部扩展签名
****************************

运行 ``west flash`` 时使用的签名脚本可以被扩展或替换，以更改功能或引入不同的签名机制。
默认启用 MCUboot 时，签名由 Zephyr 中的 :file:`cmake/mcuboot.cmake` 文件设置，
它添加额外的构建后命令以生成签名镜像。用于签名的文件可以从 sysbuild 作用域（如果使用）
或从 zephyr/zephyr 模块作用域替换，其优先级为：

* Sysbuild
* Zephyr 属性
* 默认 MCUboot 脚本（如果启用）

从 sysbuild 出发，``-D<target>_SIGNING_SCRIPT`` 可用于为特定镜像设置签名脚本，
或 ``-DSIGNING_SCRIPT`` 可用于为所有镜像设置签名脚本，例如：

.. code-block:: console

   west build -b <board> <application> -DSIGNING_SCRIPT=<file>

Zephyr 属性方法通过调整 ``zephyr_property_target`` 上的 ``SIGNING_SCRIPT`` 属性实现，
理想情况下由模块通过以下方式完成：

.. code-block:: cmake

   if(CONFIG_BOOTLOADER_MCUBOOT)
     set_target_properties(zephyr_property_target PROPERTIES SIGNING_SCRIPT ${CMAKE_CURRENT_LIST_DIR}/custom_signing.cmake)
   endif()

当项目在启用 MCUboot 签名支持的情况下构建时，这将包含自定义签名 CMake 文件
而非默认的 Zephyr 文件。基础 Zephyr MCUboot 签名文件可以作为创建新签名系统
或扩展默认行为的参考。

.. _MCUboot:
   https://mcuboot.com/

.. _imgtool:
   https://pypi.org/project/imgtool/
