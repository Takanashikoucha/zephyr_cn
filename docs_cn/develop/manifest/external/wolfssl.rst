.. _external_module_wolfssl:

wolfSSL
#######

简介
************

wolfSSL 是一个轻量级、可移植的 SSL/TLS 库，针对嵌入式系统、RTOS 环境和资源受限设备进行了优化。它提供一系列加密功能，以及安全通信协议（最高支持 TLS 1.3 和 DTLS 1.3），并支持后量子密码学。其对多种构建配置的支持使其适用于使用 Zephyr RTOS 的广泛应用和硬件平台。

wolfSSL 支持 Zephyr 网络栈，应用可使用 wolfSSL API 通过网络与其他设备或服务建立安全连接。

wolfSSL 采用 GPLv3 和商业许可的双重许可。

GitHub 仓库：`wolfSSL 仓库`_

在 Zephyr 中使用
*****************

将 wolfssl 作为项目添加到 west.yml：

.. code-block:: yaml

  manifest:
    remotes:
    # <your other remotes>
    - name: wolfssl
      url-base: https://github.com/wolfssl
  projects:
    # <your other projects>
    - name: wolfssl
      path: modules/crypto/wolfssl
      revision: master
      remote: wolfssl

更新 west 的模块：

.. code-block:: bash

   west update

现在 west 将 ``wolfssl`` 识别为模块，并将其 Kconfig 和 CMakeLists.txt 纳入构建系统。

有关 wolfSSL 与 Zephyr 使用的更多内容，请参见 `wolfSSL Zephyr 示例用法`_。

Zephyr 中的应用代码示例请参见 `wolfSSL NXP AppCodeHub`_。

wolfSSL API 文档请参见 `wolfSSL 文档`_。

参考资料
*********

.. target-notes::

.. _wolfssl 仓库:
    https://github.com/wolfSSL/wolfssl

.. _wolfSSL Zephyr 示例用法:
    https://github.com/wolfSSL/wolfssl/blob/master/zephyr/README.md#build-and-run-wolfcrypt-benchmark-application

.. _wolfSSL NXP AppCodeHub:
    https://github.com/wolfSSL/nxp-appcodehub

.. _wolfSSL 文档:
    https://www.wolfssl.com/docs/
