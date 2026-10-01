.. _wifi_mgmt:

Wi-Fi Management
################

Overview
========

Wi-Fi management API 用于管理 Wi-Fi networks。其支持以下 modes：

* IEEE802.11 Station (STA)
* IEEE802.11 Access Point (AP)
* IEEE802.11 P2P (Wi-Fi Direct)

仅支持 personal mode security（带以下 types：

* Open
* OWE
* WEP
* WPA2-PSK
* WPA2-PSK-256
* WPA3-SAE

Wi-Fi management API 在 ``wifi_mgmt`` module 中实现（作为 networking L2 stack 的一部分。当前支持两种类型的 Wi-Fi drivers：

* Networking 或 socket offloaded drivers
* Native L2 Ethernet drivers

Compiled Features
*****************

为支持仅需 Wi-Fi features 特定子集的 applications（:kconfig:option:`CONFIG_WIFI_USAGE_MODE` 可用作 drivers 的 hint 以限制须编译的 functionality。可用以下 usage hints：

 * :kconfig:option:`CONFIG_WIFI_USAGE_MODE_STA`（连接到 access point）
 * :kconfig:option:`CONFIG_WIFI_USAGE_MODE_AP`（作为 access point）
 * :kconfig:option:`CONFIG_WIFI_USAGE_MODE_STA_AP`（既作为又连接到 access point）
 * :kconfig:option:`CONFIG_WIFI_USAGE_MODE_SCAN_ONLY`（仅 access point SSID scanning）

.. note::

    对请求 usage mode 的支持取决于 hardware。

Wi-Fi shell
***********

Wi-Fi shell 提供命令以通过 interactive interface 测试和探索 Wi-Fi management API（无需专用 application。启用 :kconfig:option:`CONFIG_NET_L2_WIFI_SHELL` option 以添加 ``wifi`` command。

主要 Wi-Fi shell subcommands 包括：

.. list-table:: Wi-Fi shell subcommands
   :header-rows: 1

   * - Subcommand
     - Description
   * - ``scan``
     - 扫描 Wi-Fi networks。
   * - ``connect``
     - 连接到 Wi-Fi network。
   * - ``disconnect``
     - 断开 Wi-Fi network。
   * - ``status``
     - 显示 Wi-Fi interface status。

用 ``wifi --help`` 列出所有可用 subcommands（用 ``wifi <subcommand> --help`` 获取 command-specific help。启用 Wi-Fi shell 的 sample application 参见 :zephyr:code-sample:`wifi-shell`。

.. warning::

   默认 Wi-Fi shell scan command 不限制 scan results。由于 UART shell backend 慢（打印所有 scan results 可能导致 network management events 被丢弃。要避免 warning（按需调整 :kconfig:option:`CONFIG_NET_MGMT_EVENT_QUEUE_TIMEOUT` 或 :kconfig:option:`CONFIG_NET_MGMT_EVENT_QUEUE_SIZE`。

Wi-Fi PSA crypto supported build
********************************

要启用支持 PSA crypto API 的 Wi-Fi build（须设置 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_ALT` 和 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA`。

Wi-Fi feature to crypto mapping
*******************************

Wi-Fi features（WPA3-SAE、DPP、SAE-PK、WPA2-PSK、Enterprise EAP 等）到 crypto primitives（bignum、ECDH、TLS、hashes、AES）的映射（以及哪些用 **Legacy crypto** 与 **PSA crypto**）参见专用 sub-page：

.. toctree::
   :maxdepth: 1

   wifi_crypto

Wi-Fi Enterprise test: X.509 Certificate management
***************************************************

Wi-Fi enterprise security 须使用 X.509 certificates（支持两种安装 certificates 的方法：

Compile time certificates
-------------------------

PEM 格式的 test certificates 提交到 repo 的 :zephyr_file:`samples/net/wifi/test_certs`（构建过程中 certificates 转换为 Wi-Fi shell module 包含的 C header file。

要用自己的 certificates（可用自己的 certificates 替换同目录中的现有 certificates。

.. code-block:: bash

    $ export WIFI_TEST_CERTS_DIR=samples/net/wifi/test_certs/rsa3k
    $ cp client.pem $WIFI_TEST_CERTS_DIR
    $ cp client-key.pem $WIFI_TEST_CERTS_DIR
    $ cp ca.pem $WIFI_TEST_CERTS_DIR
    $ cp client2.pem $WIFI_TEST_CERTS_DIR
    $ cp client-key2.pem $WIFI_TEST_CERTS_DIR
    $ cp ca2.pem $WIFI_TEST_CERTS_DIR
    $ west build -p -b <board> samples/net/wifi -S wifi-enterprise

对 RSA 2048-bit certificates（用 ``rsa2k_no_des``。

.. code-block:: bash

    $ export WIFI_TEST_CERTS_DIR=samples/net/wifi/test_certs/rsa2k_no_des

或者可将 :envvar:`WIFI_TEST_CERTS_DIR` 环境变量设为指向包含 certificates 的目录。

.. code-block:: bash

    $ west build -p -b <board> samples/net/wifi -S wifi-enterprise -- -DWIFI_TEST_CERTS_DIR=<path_to_your_certificates>

Run time certificates
---------------------

Wi-Fi shell module 用 TLS credentials subsystem 存储和管理 certificates。Certificates 可用 shell commands 在 runtime 添加（更多细节参见 :ref:`tls_credentials_shell`。Sample 或 application 须启用 :kconfig:option:`CONFIG_WIFI_SHELL_RUNTIME_CERTIFICATES` option 以使用此 feature。

为便利安装 certificates（提供 helper script（用法见下。

.. code-block:: bash

    $ ./scripts/utils/wifi_ent_cert_installer.py -p samples/net/wifi/test_certs/rsa2k_no_des

Script 将通过 UART（用 TLS credentials shell commands 将 certificates 安装到 device 中的 TLS credentials store。


要发起用 enterprise security 的 Wi-Fi connection（根据 EAP method 用以下命令之一：

* EAP-TLS

  .. code-block:: console

     uart:~$ wifi connect -s <SSID> -c <channel> -k 7 -w 2 -a <Anonymous identity> --key1-pwd <Password EAP phase1> --key2-pwd <Password EAP phase2>

* EAP-TTLS-MSCHAPV2

  .. code-block:: console

     uart:~$ wifi connect -s <SSID> -c <channel> -k 14 -K <Private key Password> --eap-id1 <Client Identity> --eap-pwd1 <Client Password> -a <Anonymous identity>

* EAP-PEAP-MSCHAPV2

  .. code-block:: console

     uart:~$ wifi connect -s <SSID> -c <channel> -k 12 -K <Private key Password> --eap-id1 <Client Identity> --eap-pwd1 <Client Password> -a <Anonymous identity>

Server certificate 也在同目录中提供以用于测试目的。任何 AAA server 可用于测试目的（例如 ``FreeRADIUS`` 或 ``hostapd``。

Server certificate domain name verification
-------------------------------------------

Authentication server 的 identity 通过验证从 server 收到的 X.509 certificate 中的 domain name 验证（用 ``Common Name``（CN）field。

* Exact domain match — 验证 certificate 的 CN 与指定 domain 完全匹配。

* Domain suffix match — 允许 CN 以指定 domain suffix 结尾的 certificate。

要发起用 enterprise security（带 server certificate validation 的 Wi-Fi connection（根据期望的 validation mode 用以下命令之一：

* Exact domain match

  .. code-block:: console

     wifi connect -s <SSID> -c <channel> -k 12 -K <Private key Password> -e <Domain match>

* Domain suffix match

  .. code-block:: console

     wifi connect -s <SSID> -c <channel> -k 12 -K <Private key Password> -x <Domain suffix name>

Certificate requirements for EAP methods
----------------------------------------

不同 EAP methods 有不同的 client-side certificate requirements（如下概述：

* EAP-TLS - 需 client 上既有 client certificate（及其 private key）又有 CA certificate。
            Client 用其 certificate 向 server 认证自身。

* EAP-TTLS-MSCHAPV2 - 仅需 client 上的 CA certificate。
                      Client 用 TLS tunnel 内的 username 和 password <MSCHAPV2> 向 server 认证。
                      无需 client certificate。

* EAP-PEAP-MSCHAPV2 - 仅需 client 上的 CA certificate。
                      类似 TTLS（client 用 TLS tunnel 内的 username 和 password <MSCHAPV2>（且无需 client certificate。

.. note::

    Certificates 仅用于测试目的（不应在生产中使用。其用 `FreeRADIUS raddb <https://github.com/FreeRADIUS/freeradius-server/tree/master/raddb/certs>`_ scripts 生成。

.. note::

    使用 TLS credentials subsystem 时（默认选择 volatile backend（即 :kconfig:option:`CONFIG_TLS_CREDENTIALS_BACKEND_VOLATILE`。使用 volatile backend 时（certificates 存储在 RAM 中（重启时丢失（故重启后须重新安装 certificates。作为替代（可用 PS（protected storage）backend（即 :kconfig:option:`CONFIG_TLS_CREDENTIALS_BACKEND_PROTECTED_STORAGE`）将 certificates 存储在 non-volatile storage 中。

How to Generate Test Certificates Using FreeRADIUS
--------------------------------------------------

``samples/net/wifi/test_certs/rsa2k_no_des`` 中的 test certificates 用 `FreeRADIUS raddb/certs scripts <https://github.com/FreeRADIUS/freeradius-server/tree/master/raddb/certs>`_ 生成。可按如下生成自己的 certificates 以用于测试：

1. **Prerequisites**
   - 安装 OpenSSL 和 GNU Make。
   - 下载 `FreeRADIUS raddb/certs directory <https://github.com/FreeRADIUS/freeradius-server/tree/master/raddb/certs>`_。

2. **Edit the Makefile**
   在 ``raddb/certs`` directory 中（编辑 ``Makefile`` 以向 server 和 client keys 的 OpenSSL commands 添加 ``-nodes``。这确保 private keys 无 password 保护（Zephyr Wi-Fi shell 不支持 private key passwords）：

   ::

     $(OPENSSL) req -new -out server.csr -keyout server.key -nodes -config ./server.cnf
     $(OPENSSL) req -new -out client.csr -keyout client.key -nodes -config ./client.cnf

3. **(Optional) Edit the .cnf files**
   按需为 environment 定制 ``server.cnf`` 和 ``client.cnf``。

4. **Generate Certificates**
   在 ``raddb/certs`` directory 中运行以下 commands：

   ::

     make destroycerts
     make server
     make client

5. **Rename Files for Zephyr**
   匹配 Zephyr samples 中用的 filenames：

   +-------------------+---------------------+
   | FreeRADIUS Output | Zephyr Sample Name  |
   +===================+=====================+
   | ca.pem            | ca.pem              |
   | server.key        | server-key.pem      |
   | server.pem        | server.pem          |
   | client.key        | client-key.pem      |
   | client.pem        | client.pem          |
   +-------------------+---------------------+

6. **Copy the files**
   将重命名的 files 放入 Zephyr 项目的 certificate directory（如 ``samples/net/wifi/test_certs/rsa2k_no_des``）。用 AES（PBES2）（而非 DES）加密 private keys；参见现有 ``rsa2k_no_des`` keys 参考。

.. note::
   这些 certificates 仅用于测试（不应在生产中使用。

.. _wifi_mgmt_p2p:

Wi-Fi P2P (Wi-Fi Direct)
************************

Wi-Fi P2P 或 Wi-Fi Direct 允许 devices 直接相互通信（无需传统 access point。此 feature 对 device-to-device communication scenarios 特别有用。

要启用并带 Wi-Fi P2P 支持构建：

.. code-block:: bash

    $ west build -p -b <board> samples/net/wifi/shell -- -DCONFIG_WIFI_NM_WPA_SUPPLICANT_P2P=y

Wi-Fi NAN (Neighbor Awareness Networking)
*****************************************

Wi-Fi NAN（Neighbor Awareness Networking）（也称 Wi-Fi Aware）允许 devices 发现 services（并与附近 devices 通信（无需传统 access point 或 Internet connection。此 feature 用 publish-subscribe model（devices 可发布 services 或订阅以发现附近 peers 的 services。

要启用并带 Wi-Fi NAN 支持构建：

.. code-block:: bash

    $ west build -p -b <board> samples/net/wifi/shell -- -DCONFIG_WIFI_NM_WPA_SUPPLICANT_NAN=y

API Reference
*************

.. doxygengroup:: wifi_mgmt
