.. _external_module_wolftpm:

wolfTPM
#######

简介
************

wolfTPM 是一个轻量级、可移植的 TPM 2.0 库，针对嵌入式系统、RTOS 环境和资源受限设备进行了优化。它提供完整的 TPM 2.0 实现，包括对加密操作、密钥生成、安全存储和证明（attestation）的支持。

wolfTPM 已作为 Zephyr 模块集成，支持 CMake 和 Kconfig，便于在任何基于 Zephyr 的项目中引入 TPM 功能。该模块支持设备树（devicetree）集成，以便通过 I2C 与 TPM 设备通信——可将 ``user_settings.h`` 中的 ``WOLFTPM_ZEPHYR_I2C_BUS`` 设置为描述设备上 I2C 总线的节点来配置 I2C 总线。I2C 速度可通过 ``WOLFTPM_ZEPHYR_I2C_SPEED`` 配置。

wolfTPM 采用 GPLv3 和商业许可的双重许可。

GitHub 仓库：`wolfTPM 仓库`_

要求
************

* 用于加密操作的 :ref:`external_module_wolfssl`

在 Zephyr 中使用
*****************

将 wolfTPM 作为项目添加到 west.yml：

.. code-block:: yaml

  manifest:
    remotes:
    # <your other remotes>
    - name: wolftpm
      url-base: https://github.com/wolfssl
  projects:
    # <your other projects>
    - name: wolftpm
      path: modules/crypto/wolftpm
      revision: v3.10.0
      remote: wolftpm

.. note::

   上面显示的 revision 仅为示例。请查看 `wolfTPM 仓库`_ 的 releases 页面获取最新的 release tag，确保使用所需版本。

更新 west 的模块：

.. code-block:: bash

   west update

现在 west 将 ``wolftpm`` 识别为模块，并将其 Kconfig 和 CMakeLists.txt 纳入构建系统。

示例应用
***********

wolfTPM 包含两个 Zephyr 示例应用：

* **wolftpm_wrap_test** — 测试核心 TPM wrapper 功能
* **wolftpm_wrap_caps** — 显示 TPM 能力

两个示例都能在 qemu_x86 上成功构建和运行，为开发提供了坚实基础。

配置
*************

该模块使用 ``user_settings.h`` 配置文件，可按项目特定需求进行定制。要与 TPM 设备进行 I2C 通信，请配置：

* ``WOLFTPM_ZEPHYR_I2C_BUS`` — 设置为描述 I2C 总线的设备树节点
* ``WOLFTPM_ZEPHYR_I2C_SPEED`` — 设置 I2C 线路速度

更多资源
********************

有关 wolfTPM 与 Zephyr 使用的更多内容，请参见 `wolfTPM Zephyr 示例用法`_ 和 `wolfTPM Zephyr 公告`_。

Zephyr 中的应用代码示例请参见 `wolfSSL NXP AppCodeHub`_。

wolfTPM API 文档请参见 `wolfTPM 文档`_。

参考资料
*********

.. target-notes::

.. _wolfTPM 仓库:
    https://github.com/wolfSSL/wolfTPM

.. _wolfTPM Zephyr 示例用法:
    https://github.com/wolfSSL/wolfTPM/blob/master/zephyr/README.md

.. _wolfSSL NXP AppCodeHub:
    https://github.com/wolfSSL/nxp-appcodehub

.. _wolfTPM 文档:
    https://www.wolfssl.com/documentation/manuals/wolftpm/

.. _wolfTPM Zephyr 公告:
    https://www.wolfssl.com/wolftpm-support-for-zephyr-rtos/
