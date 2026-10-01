.. _lib_wifi_credentials:

Wi-Fi credentials Library
#########################

.. contents::
   :local:
   :depth: 2

Wi-Fi credentials library 提供加载和存储 Wi-Fi® network credentials 的手段。

Overview
********

此 library 用 Zephyr 的 settings subsystem 或 Platform Security Architecture（PSA）Internal Trusted Storage（ITS）存储 credentials。其还在 RAM 中持有 SSIDs 列表（以 SSIDs 作为 keys 提供 dictionary-like access。

Configuration
*************

要用 Wi-Fi credentials library（启用 :kconfig:option:`CONFIG_WIFI_CREDENTIALS` Kconfig option。

可用以下 options 选择 backend：

* :kconfig:option:`CONFIG_WIFI_CREDENTIALS_BACKEND_PSA` - 非 secure targets（含 TF-M partition（non-minimal TF-M profile type）的默认 option。
* :kconfig:option:`CONFIG_WIFI_CREDENTIALS_BACKEND_SETTINGS` - secure targets 的默认 option。

要用 :kconfig:option:`CONFIG_WIFI_CREDENTIALS_MAX_ENTRIES` Kconfig option 配置最大 networks 数。

IEEE 802.11 standard 未指定 SAE passwords 的最大长度。要更改默认值（用 :kconfig:option:`CONFIG_WIFI_CREDENTIALS_SAE_PASSWORD_LENGTH` Kconfig option。

Adding credentials
******************

可用 :c:func:`wifi_credentials_set_personal` 和 :c:func:`wifi_credentials_set_personal_struct` functions 添加 credentials。前者从给定 fields 构建内部使用的 struct（后者直接接受 struct。若两次添加相同 SSID 的 credentials（较旧的 entry 被覆盖。

Querying credentials
********************

用 SSID（可用 :c:func:`wifi_credentials_get_by_ssid_personal` 和 :c:func:`wifi_credentials_get_by_ssid_personal_struct` functions 查询 credentials。

可用 :c:func:`wifi_credentials_for_each_ssid` function 遍历所有存储的 credentials。遍历时删除或覆盖 credentials 是允许的（因为这些 operations 不更改内部 indices。

Removing credentials
********************

可用 :c:func:`wifi_credentials_delete_by_ssid` function 移除 credentials。

Shell commands
**************

``wifi cred`` 为 Wi-Fi command line 的扩展。其添加以下 subcommands 以与 Wi-Fi credentials library 交互：

.. list-table:: Wi-Fi credentials shell subcommands
   :header-rows: 1

   * - Subcommands
     - Description
   * - add
     - | 用以下 parameters 向 credentials storage 添加 network：
       | <-s --ssid \"<SSID>\">: SSID。
       | [-c --channel]: 需扫描以连接的 Channel。0:any channel
       | [-b, --band] 0: any band (2:2.4GHz, 5:5GHz, 6:6GHz)
       | [-p, --passphrase]: Passphrase（仅对 secure SSIDs 有效）
       | [-k, --key-mgmt]: Key management type。
       | 0:None, 1:WPA2-PSK, 2:WPA2-PSK-256, 3:SAE-HNP, 4:SAE-H2E, 5:SAE-AUTO, 6:WAPI,"
       | " 7:EAP-TLS, 8:WEP, 9: WPA-PSK, 10: WPA-Auto-Personal, 11: DPP
       | [-w, --ieee-80211w]: MFP（optional: 须指定 security type）
       | : 0:Disable, 1:Optional, 2:Required。
       | [-m, --bssid]: AP 的 MAC address（BSSID）。
       | [-t, --timeout]: 连接尝试须失败的时长。
       | [-a, --identity]: Enterprise mode 的 Identity。
       | [-K, --key-passwd]: Enterprise mode 的 Private key passwd。
       | [-h, --help]: 打印 connect command 的 help。
   * - delete <SSID>
     - 从 credentials storage 移除 network。
   * - list
     - 列出 credential storage 中的 networks。
   * - auto_connect
     - 自动连接到任何存储的 network。

Limitations
***********

Library 有以下 limitations：

* 虽然 IEEE 802.11 standard 允许（此 library 不支持 zero-length SSIDs。
* Wi-Fi Protected Access（WPA）Enterprise credentials 仅部分支持。
* 存储的 networks 数在 compile time 固定。

API documentation
*****************

以下 section 提供 Zephyr 中可用 Wi-Fi credentials API 的概述和 reference：

.. doxygengroup:: wifi_credentials
