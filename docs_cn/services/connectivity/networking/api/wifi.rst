.. _wifi_mgmt:

Wi-Fi 管理
################

概述
========

Wi-Fi 管理 API 用于管理 Wi-Fi 网络。它支持以下模式：

* IEEE802.11 站点（STA）
* IEEE802.11 接入点（AP）
* IEEE802.11 P2P（Wi-Fi Direct）

仅支持个人模式安全，类型如下：

* Open
* OWE
* WEP
* WPA2-PSK
* WPA2-PSK-256
* WPA3-SAE

Wi-Fi 管理 API 在 ``wifi_mgmt`` 模块中实现，是网络 L2 栈的一部分。
目前支持两种类型的 Wi-Fi 驱动程序：

* 网络或套接字卸载驱动程序
* 原生 L2 以太网驱动程序

编译特性
*****************

为了支持只需要 Wi-Fi 功能子集的应用程序，可以使用 :kconfig:option:`CONFIG_WIFI_USAGE_MODE` 作为驱动程序的限制提示，限定需要编译的功能。可用的使用提示如下：

 * :kconfig:option:`CONFIG_WIFI_USAGE_MODE_STA`（连接到接入点）
 * :kconfig:option:`CONFIG_WIFI_USAGE_MODE_AP`（作为接入点）
 * :kconfig:option:`CONFIG_WIFI_USAGE_MODE_STA_AP`（既作为接入点又连接到接入点）
 * :kconfig:option:`CONFIG_WIFI_USAGE_MODE_SCAN_ONLY`（仅扫描接入点 SSID）

.. note::

    所请求使用模式的支持取决于硬件。

Wi-Fi shell
***********

Wi-Fi shell 通过交互式界面提供命令，用于测试和探索 Wi-Fi 管理 API，无需专用应用程序。
启用 :kconfig:option:`CONFIG_NET_L2_WIFI_SHELL` 选项以添加 ``wifi`` 命令。

主要的 Wi-Fi shell 子命令包括：

.. list-table:: Wi-Fi shell 子命令
   :header-rows: 1

   * - 子命令
     - 描述
   * - ``scan``
     - 扫描 Wi-Fi 网络。
   * - ``connect``
     - 连接到 Wi-Fi 网络。
   * - ``disconnect``
     - 断开与 Wi-Fi 网络的连接。
   * - ``status``
     - 显示 Wi-Fi 接口状态。

使用 ``wifi --help`` 列出所有可用子命令，使用 ``wifi <subcommand> --help`` 获取特定命令的帮助。
参见 :zephyr:code-sample:`wifi-shell` 了解启用 Wi-Fi shell 的示例应用程序。

.. warning::

   默认情况下，Wi-Fi shell 的 scan 命令不限制扫描结果。由于 UART shell 后端速度较慢，打印所有扫描结果可能导致网络管理事件被丢弃。
   如需避免此警告，请调整 :kconfig:option:`CONFIG_NET_MGMT_EVENT_QUEUE_TIMEOUT` 或
   :kconfig:option:`CONFIG_NET_MGMT_EVENT_QUEUE_SIZE`。

支持 Wi-Fi PSA crypto 的构建
********************************

要启用支持 PSA crypto API 的 Wi-Fi 构建，需要设置 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_ALT` 和 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA`。

Wi-Fi 功能与 crypto 的映射
*******************************

要将 Wi-Fi 功能（WPA3-SAE、DPP、SAE-PK、WPA2-PSK、企业 EAP 等）映射到
crypto 原语（bignum、ECDH、TLS、hashes、AES）以及哪些使用 **Legacy crypto** 和哪些使用 **PSA
crypto**，请参见专用子页面：

.. toctree::
   :maxdepth: 1

   wifi_crypto

Wi-Fi 企业测试：X.509 证书管理
***************************************************

Wi-Fi 企业安全需要使用 X.509 证书，支持两种安装证书的方法：

编译时证书
-------------------------

PEM 格式的测试证书已提交到仓库的 :zephyr_file:`samples/net/wifi/test_certs`，在
构建过程中证书会被转换为 C 头文件，该头文件由 Wi-Fi shell
模块包含。

如果想使用自己的证书，可以用自己的证书替换同一目录中的现有证书。

.. code-block:: bash

    $ export WIFI_TEST_CERTS_DIR=samples/net/wifi/test_certs/rsa3k
    $ cp client.pem $WIFI_TEST_CERTS_DIR
    $ cp client-key.pem $WIFI_TEST_CERTS_DIR
    $ cp ca.pem $WIFI_TEST_CERTS_DIR
    $ cp client2.pem $WIFI_TEST_CERTS_DIR
    $ cp client-key2.pem $WIFI_TEST_CERTS_DIR
    $ cp ca2.pem $WIFI_TEST_CERTS_DIR
    $ west build -p -b <board> samples/net/wifi -S wifi-enterprise

对于 RSA 2048 位证书，请使用 ``rsa2k_no_des``。

.. code-block:: bash

    $ export WIFI_TEST_CERTS_DIR=samples/net/wifi/test_certs/rsa2k_no_des

或者可以设置 :envvar:`WIFI_TEST_CERTS_DIR` 环境变量，指向包含证书的目录。

.. code-block:: bash

    $ west build -p -b <board> samples/net/wifi -S wifi-enterprise -- -DWIFI_TEST_CERTS_DIR=<path_to_your_certificates>

运行时证书
---------------------

Wi-Fi shell 模块使用 TLS 凭据子系统来存储和管理证书。证书可以在运行时使用 shell 命令添加，详见 :ref:`tls_credentials_shell`。
示例或应用程序需要启用 :kconfig:option:`CONFIG_WIFI_SHELL_RUNTIME_CERTIFICATES` 选项才能使用此功能。

为了方便安装证书，提供了一个辅助脚本，用法如下。

.. code-block:: bash

    $ ./scripts/utils/wifi_ent_cert_installer.py -p samples/net/wifi/test_certs/rsa2k_no_des

该脚本将通过 UART 使用 TLS 凭据 shell 命令将证书安装到设备的 TLS 凭据存储中。


要使用企业安全发起 Wi-Fi 连接，请根据 EAP 方法使用以下命令之一：

* EAP-TLS

  .. code-block:: console

     uart:~$ wifi connect -s <SSID> -c <channel> -k 7 -w 2 -a <Anonymous identity> --key1-pwd <Password EAP phase1> --key2-pwd <Password EAP phase2>

* EAP-TTLS-MSCHAPV2

  .. code-block:: console

     uart:~$ wifi connect -s <SSID> -c <channel> -k 14 -K <Private key Password> --eap-id1 <Client Identity> --eap-pwd1 <Client Password> -a <Anonymous identity>

* EAP-PEAP-MSCHAPV2

  .. code-block:: console

     uart:~$ wifi connect -s <SSID> -c <channel> -k 12 -K <Private key Password> --eap-id1 <Client Identity> --eap-pwd1 <Client Password> -a <Anonymous identity>

同一目录中还提供了服务器证书用于测试。
任何 AAA 服务器都可以用于测试，例如 ``FreeRADIUS`` 或 ``hostapd``。

服务器证书域名验证
-------------------------------------------

通过验证从服务器接收的 X.509 证书中的域名来验证身份，使用 ``Common Name``（CN）字段。

* 精确域名匹配 — 验证证书的 CN 与指定域名完全匹配。

* 域名后缀匹配 — 允许证书的 CN 以指定的域名后缀结尾。

要使用服务器证书验证发起企业安全的 Wi-Fi 连接，请根据所需的验证模式使用以下命令之一：

* 精确域名匹配

  .. code-block:: console

     wifi connect -s <SSID> -c <channel> -k 12 -K <Private key Password> -e <Domain match>

* 域名后缀匹配

  .. code-block:: console

     wifi connect -s <SSID> -c <channel> -k 12 -K <Private key Password> -x <Domain suffix name>

EAP 方法的证书要求
----------------------------------------

不同的 EAP 方法有不同的客户端证书要求，如下所述：

* EAP-TLS - 需要客户端证书（及其私钥）和客户端 CA 证书。
            客户端使用其证书向服务器进行身份验证。

* EAP-TTLS-MSCHAPV2 - 只需要客户端 CA 证书。
                      客户端在 TLS 隧道内使用用户名和密码 <MSCHAPV2> 向服务器进行身份验证。
                      不需要客户端证书。

* EAP-PEAP-MSCHAPV2 - 只需要客户端 CA 证书。
                      与 TTLS 类似，客户端在 TLS 隧道内使用用户名和密码 <MSCHAPV2>，不需要客户端证书。

.. note::

    这些证书仅用于测试目的，不应在生产环境中使用。
    它们使用 `FreeRADIUS raddb <https://github.com/FreeRADIUS/freeradius-server/tree/master/raddb/certs>`_ 脚本生成。

.. note::

    使用 TLS 凭据子系统时，默认选择易失后端，即 :kconfig:option:`CONFIG_TLS_CREDENTIALS_BACKEND_VOLATILE`。使用易失后端时，证书存储在 RAM 中，重启后会丢失，因此重启后需要重新安装证书。作为替代方案，可以使用 PS（受保护存储）后端，即 :kconfig:option:`CONFIG_TLS_CREDENTIALS_BACKEND_PROTECTED_STORAGE`，将证书存储在非易失性存储中。

如何使用 FreeRADIUS 生成测试证书
--------------------------------------------------

``samples/net/wifi/test_certs/rsa2k_no_des`` 中的测试证书使用 `FreeRADIUS raddb/certs 脚本 <https://github.com/FreeRADIUS/freeradius-server/tree/master/raddb/certs>`_ 生成。可以按照以下步骤生成自己的测试证书：

1. **先决条件**
   - 安装 OpenSSL 和 GNU Make。
   - 下载 `FreeRADIUS raddb/certs 目录 <https://github.com/FreeRADIUS/freeradius-server/tree/master/raddb/certs>`_。

2. **编辑 Makefile**
   在 ``raddb/certs`` 目录中，编辑 ``Makefile`` 为服务器和客户端密钥的 OpenSSL 命令添加 ``-nodes``。这确保私钥没有密码保护（Zephyr Wi-Fi shell 不支持私钥密码）：

   ::

     $(OPENSSL) req -new -out server.csr -keyout server.key -nodes -config ./server.cnf
     $(OPENSSL) req -new -out client.csr -keyout client.key -nodes -config ./client.cnf

3. **（可选）编辑 .cnf 文件**
   根据需要自定义 ``server.cnf`` 和 ``client.cnf`` 以适应你的环境。

4. **生成证书**
   在 ``raddb/certs`` 目录中运行以下命令：

   ::

     make destroycerts
     make server
     make client

5. **为 Zephyr 重命名文件**
   匹配 Zephyr 示例中使用的文件名：

   +-------------------+---------------------+
   | FreeRADIUS 输出 | Zephyr 示例名称  |
   +===================+=====================+
   | ca.pem            | ca.pem              |
   | server.key        | server-key.pem      |
   | server.pem        | server.pem          |
   | client.key        | client-key.pem      |
   | client.pem        | client.pem          |
   +-------------------+---------------------+

6. **复制文件**
   将重命名后的文件放入 Zephyr 项目的证书目录（例如 ``samples/net/wifi/test_certs/rsa2k_no_des``）。
   使用 AES（PBES2）加密私钥，而不是 DES；参考现有 ``rsa2k_no_des`` 密钥。

.. note::
   这些证书仅用于测试，不应在生产环境中使用。

.. _wifi_mgmt_p2p:

Wi-Fi P2P（Wi-Fi Direct）
************************

Wi-Fi P2P 或 Wi-Fi Direct 使设备能够直接相互通信，无需传统接入点。此功能特别适用于设备到设备通信
场景。

要启用并构建支持 Wi-Fi P2P：

.. code-block:: bash

    $ west build -p -b <board> samples/net/wifi/shell -- -DCONFIG_WIFI_NM_WPA_SUPPLICANT_P2P=y

Wi-Fi NAN（邻居感知网络）
*****************************************

Wi-Fi NAN（邻居感知网络），也称为 Wi-Fi Aware，使设备能够发现
服务并与附近设备通信，无需传统接入点或互联网
连接。此功能使用发布-订阅模型，设备可以发布服务或
订阅发现附近对等设备的发现服务。

要启用并构建支持 Wi-Fi NAN：

.. code-block:: bash

    $ west build -p -b <board> samples/net/wifi/shell -- -DCONFIG_WIFI_NM_WPA_SUPPLICANT_NAN=y

API 参考
*************

.. doxygengroup:: wifi_mgmt
