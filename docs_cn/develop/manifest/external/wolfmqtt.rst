.. _external_module_wolfmqtt:

wolfMQTT
########

简介
****

wolfMQTT 是一个轻量级、可移植的 MQTT 客户端库，针对嵌入式系统、
RTOS 环境和资源受限设备优化。它提供 MQTT 协议的客户端实现，支持
MQTT v3.1.1 和 v5.0。该库提供 QoS 等级 0-2、Last Will and
Testament（LWT，遗嘱与遗嘱执行）等特性，并与多种 MQTT broker 兼容。
其对多种构建配置的支持使其适用于使用 Zephyr RTOS 的广泛 IoT 应用
和硬件平台。

wolfMQTT 支持 Zephyr 网络栈，应用可使用 wolfMQTT API 通过网络与
broker 及其他设备或服务建立 MQTT 连接。

wolfMQTT 采用 GPLv3 和商业许可的双重许可。

GitHub 仓库：`wolfMQTT 仓库`_

要求
****

* 用于安全通信（TLS 支持）的 :ref:`external_module_wolfssl`

在 Zephyr 中使用
****************

将 wolfMQTT 作为项目添加到 west.yml：

.. code-block:: yaml

  manifest:
    remotes:
    # <your other remotes>
    - name: wolfmqtt
      url-base: https://github.com/wolfssl
  projects:
    # <your other projects>
    - name: wolfmqtt
      path: modules/lib/wolfmqtt
      revision: v1.21.0
      remote: wolfmqtt

.. note::

   上面显示的 revision 仅为示例。请查看 `wolfMQTT 仓库`_
   的 releases 页面获取最新的 release tag，确保使用所需版本。

更新 west 的模块：

.. code-block:: bash

   west update

现在 west 将 ``wolfmqtt`` 识别为模块，并将其 Kconfig 和
CMakeLists.txt 纳入构建系统。

有关 wolfMQTT 与 Zephyr 使用的更多内容，请参见
`wolfMQTT Zephyr 示例用法`_。

Zephyr 中的应用代码示例请参见 `wolfSSL NXP AppCodeHub`_。

wolfMQTT API 文档请参见 `wolfMQTT 文档`_。

参考资料
********

.. target-notes::

.. _wolfMQTT 仓库:
    https://github.com/wolfSSL/wolfMQTT

.. _wolfMQTT Zephyr 示例用法:
    https://github.com/wolfSSL/wolfMQTT/tree/master/zephyr

.. _wolfSSL NXP AppCodeHub:
    https://github.com/wolfSSL/nxp-appcodehub

.. _wolfMQTT 文档:
    https://www.wolfssl.com/documentation/manuals/wolfmqtt/
