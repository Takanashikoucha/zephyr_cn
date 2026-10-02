.. _lib_wifi_credentials:

Wi-Fi 凭据库
#########################

.. contents::
   :local:
   :depth: 2

Wi-Fi 凭据库提供了加载和存储 Wi-Fi® 网络凭据的手段。

概述
********

该库使用 Zephyr 的 settings 子系统或平台安全架构（PSA）内部可信存储（ITS）来存储凭据。
它还在 RAM 中维护一个 SSID 列表，以便使用 SSID 作为键提供类似字典的访问。

配置
*************

要使用 Wi-Fi 凭据库，请启用 :kconfig:option:`CONFIG_WIFI_CREDENTIALS` Kconfig 选项。

可以使用以下选项选择后端：

* :kconfig:option:`CONFIG_WIFI_CREDENTIALS_BACKEND_PSA` - 非安全目标（包含 TF-M 分区的目标，即非最小化 TF-M profile 类型）的默认选项。
* :kconfig:option:`CONFIG_WIFI_CREDENTIALS_BACKEND_SETTINGS` - 安全目标的默认选项。

要配置网络的最大数量，请使用 :kconfig:option:`CONFIG_WIFI_CREDENTIALS_MAX_ENTRIES` Kconfig 选项。

IEEE 802.11 标准未规定 SAE 密码的最大长度。
要更改默认值，请使用 :kconfig:option:`CONFIG_WIFI_CREDENTIALS_SAE_PASSWORD_LENGTH` Kconfig 选项。

添加凭据
******************

你可以使用 :c:func:`wifi_credentials_set_personal` 和 :c:func:`wifi_credentials_set_personal_struct` 函数添加凭据。
前者从给定字段构建内部使用的结构体，后者直接接收结构体。
如果你两次添加具有相同 SSID 的凭据，较旧的条目将被覆盖。

查询凭据
********************

借助 SSID，你可以使用 :c:func:`wifi_credentials_get_by_ssid_personal` 和 :c:func:`wifi_credentials_get_by_ssid_personal_struct` 函数查询凭据。

你可以使用 :c:func:`wifi_credentials_for_each_ssid` 函数遍历所有已存储的凭据。
允许在遍历过程中删除或覆盖凭据，因为这些操作不会改变内部索引。

删除凭据
********************

你可以使用 :c:func:`wifi_credentials_delete_by_ssid` 函数删除凭据。

Shell 命令
**************

``wifi cred`` 是 Wi-Fi 命令行的扩展。
它添加了以下子命令，用于与 Wi-Fi 凭据库交互：

.. list-table:: Wi-Fi 凭据 shell 子命令
   :header-rows: 1

   * - 子命令
     - 说明
   * - add
     - | 使用以下参数向凭据存储添加一个网络：
       | <-s --ssid \"<SSID>\">: SSID。
       | [-c --channel]: 连接时需要扫描的信道。0:任意信道
       | [-b, --band] 0: 任意频段（2:2.4GHz, 5:5GHz, 6:6GHz）
       | [-p, --passphrase]: 密码（仅对安全 SSID 有效）
       | [-k, --key-mgmt]: 密钥管理类型。
       | 0:None, 1:WPA2-PSK, 2:WPA2-PSK-256, 3:SAE-HNP, 4:SAE-H2E, 5:SAE-AUTO, 6:WAPI,"
       | " 7:EAP-TLS, 8:WEP, 9: WPA-PSK, 10: WPA-Auto-Personal, 11: DPP
       | [-w, --ieee-80211w]: MFP（可选：需要指定安全类型）
       | : 0:Disable, 1:Optional, 2:Required.
       | [-m, --bssid]: AP 的 MAC 地址（BSSID）。
       | [-t, --timeout]: 连接尝试需要失败之前的持续时间。
       | [-a, --identity]: 企业模式的身份。
       | [-K, --key-passwd]: 企业模式的私钥密码。
       | [-h, --help]: 打印 connect 命令的帮助信息。
   * - delete <SSID>
     - 从凭据存储中删除网络。
   * - list
     - 列出凭据存储中的网络。
   * - auto_connect
     - 自动连接到任意已存储的网络。

限制
***********

该库具有以下限制：

* 尽管 IEEE 802.11 标准允许，但该库不支持零长度 SSID。
* Wi-Fi 保护访问（WPA）企业凭据仅得到部分支持。
* 存储的网络数量在编译时固定。

API 文档
*****************

以下章节概述了 Zephyr 中可用的 Wi-Fi 凭据 API 并提供了参考：

.. doxygengroup:: wifi_credentials
