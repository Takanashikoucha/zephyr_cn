.. _wifi_mgmt:

Wi
Fi
Management
################

Overview
========

Wi
Fi
management
API
被
used
用于
manage
Wi
Fi
networks。
它
support
以下
modes：

*
IEEE802.11
Station
（STA）
*
IEEE802.11
Access
Point
（AP）
*
IEEE802.11
P2P
（Wi
Fi
Direct）

只
support
personal
mode
的
security
带
以下
types：

*
Open
*
OWE
*
WEP
*
WPA2-PSK
*
WPA2-PSK-256
*
WPA3-SAE

Wi
Fi
management
API
在
``wifi_mgmt``
module
中
implemented
作为
networking
L2
stack
的
一
part。
当前
两
type
的
Wi
Fi
drivers
被
supported：

*
Networking
或
socket
offloaded
的
drivers
*
Native
L2
Ethernet
的
drivers

Compiled
Features
*****************

要
support
只
require
特定
subset
的
Wi
Fi
features
的
applications
:kconfig:option:`CONFIG_WIFI_USAGE_MODE`
可
被
used
作为
hint
给
drivers
用于
limit
需要
被
compiled
in
的
functionality。
以下
usage
hints
available：

*
:kconfig:option:`CONFIG_WIFI_USAGE_MODE_STA`
（connect
到
一
个
access
point）
*
:kconfig:option:`CONFIG_WIFI_USAGE_MODE_AP`
（作为
一
个
access
point）
*
:kconfig:option:`CONFIG_WIFI_USAGE_MODE_STA_AP`
（两
个
都
是
并
connect
到
一
个
access
point）
*
:kconfig:option:`CONFIG_WIFI_USAGE_MODE_SCAN_ONLY`
（只
scan
access
point
SSID）


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
* Domain suffix match — Allows a certificate whose CN ends with the specified domain suffix.

To initiate a Wi-Fi connection using enterprise security with server certificate validation, use one of the following commands, depending on the desired validation mode:

* Exact domain match

  .. code-block:: console

     wifi connect -s <SSID> -c <channel> -k 12 -K <Private key Password> -e <Domain match>

* Domain suffix match

  .. code-block:: console

     wifi connect -s <SSID> -c <channel> -k 12 -K <Private key Password> -x <Domain suffix name>

Certificate requirements for EAP methods
----------------------------------------

Different EAP methods have varying client-side certificate requirements, as outlined below:

* EAP-TLS - Requires both a client certificate (and its private key) and a CA certificate on the client.
            The client authenticates itself to the server using its certificate.

* EAP-TTLS-MSCHAPV2 - Requires only the CA certificate on the client.
                      The client authenticates to the server using a username and password <MSCHAPV2> inside the TLS tunnel.
                      No client certificate is needed.

* EAP-PEAP-MSCHAPV2 - Requires only the CA certificate on the client.
                      Like TTLS, the client uses a username and password <MSCHAPV2> inside the TLS tunnel and does not require a client certificate.

.. note::

    The certificates are for testing purposes only and should not be used in production.
    They are generated using `FreeRADIUS raddb <https://github.com/FreeRADIUS/freeradius-server/tree/master/raddb/certs>`_ scripts.

.. note::

    When using TLS credentials subsystem, by default the volatile backend i.e., :kconfig:option:`CONFIG_TLS_CREDENTIALS_BACKEND_VOLATILE` is chosen. When using the volatile backend, the certificates are stored in RAM and are lost on reboot, so the certificates need to be installed again after reboot. As an alternative, the PS (protected storage) backend i.e., :kconfig:option:`CONFIG_TLS_CREDENTIALS_BACKEND_PROTECTED_STORAGE` can be used to store the certificates in the non-volatile storage.

How to Generate Test Certificates Using FreeRADIUS
--------------------------------------------------

The test certificates in ``samples/net/wifi/test_certs/rsa2k_no_des`` are generated using the `FreeRADIUS raddb/certs scripts <https://github.com/FreeRADIUS/freeradius-server/tree/master/raddb/certs>`_. You can generate your own certificates for testing as follows:

1. **Prerequisites**
   - Install OpenSSL and GNU Make.
   - Download the `FreeRADIUS raddb/certs directory <https://github.com/FreeRADIUS/freeradius-server/tree/master/raddb/certs>`_.

2. **Edit the Makefile**
   In the ``raddb/certs`` directory, edit the ``Makefile`` to add ``-nodes`` to the OpenSSL commands for server and client keys. This ensures the private keys are not password-protected (Zephyr Wi-Fi shell does not support private key passwords):

   ::

     $(OPENSSL) req -new -out server.csr -keyout server.key -nodes -config ./server.cnf
     $(OPENSSL) req -new -out client.csr -keyout client.key -nodes -config ./client.cnf

3. **(Optional) Edit the .cnf files**
   Customize ``server.cnf`` and ``client.cnf`` as needed for your environment.

4. **Generate Certificates**
   Run the following commands in the ``raddb/certs`` directory:

   ::

     make destroycerts
     make server
     make client

5. **Rename Files for Zephyr**
   Match the filenames used in Zephyr samples:

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
   Place the renamed files in your Zephyr project's certificate directory (e.g., ``samples/net/wifi/test_certs/rsa2k_no_des``).
   Encrypt private keys with AES (PBES2), not DES; see the existing ``rsa2k_no_des`` keys for reference.

.. note::
   These certificates are for testing only and should not be used in production.

.. _wifi_mgmt_p2p:

Wi-Fi P2P (Wi-Fi Direct)
************************

Wi-Fi P2P or Wi-Fi Direct enables devices to communicate directly with each other without requiring
a traditional access point. This feature is particularly useful for device-to-device communication
scenarios.

To enable and build with Wi-Fi P2P support:

.. code-block:: bash

    $ west build -p -b <board> samples/net/wifi/shell -- -DCONFIG_WIFI_NM_WPA_SUPPLICANT_P2P=y

Wi-Fi NAN (Neighbor Awareness Networking)
*****************************************

Wi-Fi NAN (Neighbor Awareness Networking), also known as Wi-Fi Aware, enables devices to discover
services and communicate with nearby devices without requiring a traditional access point or Internet
connection. This feature uses a publish-subscribe model where devices can publish services or
subscribe to discover services from nearby peers.

To enable and build with Wi-Fi NAN support:

.. code-block:: bash

    $ west build -p -b <board> samples/net/wifi/shell -- -DCONFIG_WIFI_NM_WPA_SUPPLICANT_NAN=y

API Reference
*************

.. doxygengroup:: wifi_mgmt