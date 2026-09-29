.. _external_module_wolfssh:

wolfSSH
#######

简介
****

wolfSSH 是一个轻量级、可移植的 SSH 库，针对嵌入式系统、RTOS 环境
和资源受限设备优化。它提供安全 shell 功能，包括 SSH 服务器和客户端
实现、SCP 和 SFTP 支持。其对多种构建配置的支持使其适用于使用
Zephyr RTOS 的广泛应用和硬件平台。

wolfSSH 支持 Zephyr 网络栈，应用可使用 wolfSSH API 通过网络与其他
设备或服务建立安全的 SSH 连接。

wolfSSH 采用 GPLv3 和商业许可的双重许可。

GitHub 仓库：`wolfSSH 仓库`_

要求
****

* 用于加密操作的 :ref:`external_module_wolfssl`

在 Zephyr 中使用
****************

将 wolfSSH 作为项目添加到 west.yml：

.. code-block:: yaml

  manifest:
    remotes:
    # <your other remotes>
    - name: wolfssh
      url-base: https://github.com/wolfssl
  projects:
    # <your other projects>
    - name: wolfssh
      path: modules/lib/wolfssh
      revision: master
      remote: wolfssh

更新 west 的模块：

.. code-block:: bash

   west update

现在 west 将 ``wolfssh`` 识别为模块，并将其 Kconfig 和
CMakeLists.txt 纳入构建系统。

有关 wolfSSH 与 Zephyr 使用的更多内容，请参见 `wolfSSH Zephyr 示例用法`_。

Zephyr 中的应用代码示例请参见 `wolfSSL NXP AppCodeHub`_。

wolfSSH API 文档请参见 `wolfSSH 文档`_。

参考资料
********

.. target-notes::

.. _wolfSSH 仓库:
    https://github.com/wolfSSL/wolfssh

.. _wolfSSH Zephyr 示例用法:
    https://github.com/wolfSSL/wolfssh/blob/master/zephyr/README.md#build-and-run-samples

.. _wolfSSL NXP AppCodeHub:
    https://github.com/wolfSSL/nxp-appcodehub

.. _wolfSSH 文档:
    https://www.wolfssl.com/documentation/manuals/wolfssh/
