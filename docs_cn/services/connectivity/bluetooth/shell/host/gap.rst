Bluetooth: GAP Shell
####################

GAP shell 是 Bluetooth 的"主"shell（处理 connection management、scanning、advertising 等。


Identities
**********

Identities 是 Zephyr host 概念（允许单个物理 device 表现得像多个 logical Bluetooth devices。

Shell 允许创建多个 identities（最大数由 Kconfig symbol :kconfig:option:`CONFIG_BT_ID_MAX` 设置。要创建新 identity（使用 :code:`bt id-create` 命令。然后可用其 ID 选择它 :code:`bt id-select <id>`。最后（可用 :code:`id-show` 列出所有可用 identities。

Scan for devices
****************

用 :code:`bt scan on` 命令开始 scanning。根据您所在的环境（您可能看到 shell 上打印许多行。要停止 scan（运行 :code:`bt scan off`（滚动应停止。

以下是您可预期看到的示例：

.. code-block:: console

        uart:~$ bt scan on
        Bluetooth active scan enabled
        [DEVICE]: R:CB:01:1A:2D:6E:AE, AD evt type 0, RSSI -78  C:1 S:1 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:20:C2:EE:59:85:5B, AD evt type 3, RSSI -62  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:E3:72:76:87:2F:E8, AD evt type 3, RSSI -74  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:1E:19:25:8A:CB:84, AD evt type 3, RSSI -67  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:26:42:F3:D5:A0:86, AD evt type 3, RSSI -73  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:0C:61:D1:B9:5D:9E, AD evt type 3, RSSI -87  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:20:C2:EE:59:85:5B, AD evt type 3, RSSI -66  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        [DEVICE]: R:25:3F:7A:EE:0F:55, AD evt type 3, RSSI -83  C:0 S:0 D:0 SR:0 E:0 Prim: LE 1M, Secn: No packets, Interval: 0x0000 (0 us), SID: 0xff
        uart:~$ bt scan off
        Scan successfully stopped

如您所见（这可能导致大量 results。要减少该数量并轻松找到特定 device（可启用 scan filters。有四种 filter 类型：按 name、按 RSSI、按 address 和按 periodic advertising interval。要应用 filter（使用 :code:`bt scan-set-filter` 命令后跟 filter 类型。可再次使用命令添加多个 filters。

例如（若您只想查找 name 为 *test shell* 的 devices：

.. code-block:: console

        uart:~$ bt scan-filter-set name "test shell"

或者若您想查找非常近距离的 devices：

.. code-block:: console

        uart:~$ bt scan-filter-set rssi -40
        RSSI cutoff set at -40 dB

最后（若您想移除所有 filters：

.. code-block:: console

        uart:~$ bt scan-filter-clear all

可用 :code:`bt scan on` 命令创建 *active* scanner（即 scanner 将通过发送 *scan request* packet 向 advertisers 请求更多信息。或者（可用 :code:`bt scan passive` 命令创建 *passive scanner*（这样 scanner 不会向 advertiser 请求更多信息。

启用 :kconfig:option:`CONFIG_BT_SCAN_EXT_FILTER_POLICY` 时（:code:`bt scan --ext-filter-policy on` 命令以 extended scanner filter policy 启动 scanner。Controller 还会报告其无法解析的 target address 为 resolvable private address 的 directed advertisements。Directed advertisement 的 target address 单独打印在一行。这需要支持 Extended Scanner Filter Policies 的 Controller（否则命令失败。

Connecting to a device
**********************

要连接到 device（需知道其 address 和 address 类型（并使用 :code:`bt connect` 命令以 address 和类型为 arguments。

以下是示例：

.. code-block:: console

        uart:~$ bt connect R:52:84:F6:BD:CE:48
        Connection pending
        Connected: R:52:84:F6:BD:CE:48
        Remote LMP version 5.3 (0x0c) subversion 0xffff manufacturer 0x05f1
        LE Features: 0x000000000001412f
        LE PHY updated: TX PHY LE 2M, RX PHY LE 2M
        LE conn  param req: int (0x0018, 0x0028) lat 0 to 42
        LE conn param updated: int 0x0028 lat 0 to 42

可用 :code:`bt connections` 命令列出 shell 的 active connections。Shell 最大 connections 数由 :kconfig:option:`CONFIG_BT_MAX_CONN` 定义。可用 :code:`bt disconnect <address: P:XX:XX:XX:XX:XX:XX or R:XX:XX:XX:XX:XX:XX>` 命令从 connection 断开。

.. note::

        若刚在 scanning（可仅运行 :code:`bt connect` 命令连接到最后扫描的 device。

        或者（可用 :code:`bt connect-name <name>` 命令自动启用带 name filter 的 scanning 并连接到第一个匹配。

Advertising
***********

用 :code:`bt advertise on` 命令开始 advertising。这将使用默认 parameters 并以 device name advertise resolvable private address。可运行 :code:`bt advertise on identity` 选择改用 identity address。要停止 advertising（使用 :code:`bt advertise off` 命令。

要启用 advertising 的更多高级 features（应使用 :code:`bt adv-create` 命令创建 advertiser。Advertiser 的 parameters 可在创建时传递或使用 :code:`bt adv-param` 命令。要使用此新创建的 advertiser 开始 advertising（使用 :code:`bt adv-start` 命令（然后用 :code:`bt adv-stop` 命令停止 advertising。

使用 custom advertisers 时（可选择其是否为 connectable 或 scannable。这导致四个选项：:code:`conn-scan`、:code:`conn-nscan`、:code:`nconn-scan` 和 :code:`nconn-nscan`。创建 advertiser 或更新其 parameters 时这些 parameters 为 mandatory。

例如（若您想创建 connectable 且 scannable 的 advertiser 并启动它：

.. code-block:: console

        uart:~$ bt adv-create conn-scan
        Created adv id: 0, adv: 0x200022f0
        uart:~$ bt adv-start
        Advertiser[0] 0x200022f0 set started

您可能注意到用此（custom advertiser 不 advertise device name；需添加它。继续之前的示例：

.. code-block:: console

        uart:~$ bt adv-stop
        Advertiser set stopped
        uart:~$ bt adv-data dev-name
        uart:~$ bt adv-start
        Advertiser[0] 0x200022f0 set started

现在应在 advertising data 中看到 device name。也可用 :code:`name <custom name>` 代替 :code:`dev-name` 设置 custom name。还可用 :code:`bt adv-data` 命令手动设置 advertising data。以下示例展示如何用 raw advertising data 设置 advertiser name：

.. code-block:: console

        uart:~$ bt adv-create conn-scan
        Created adv id: 0, adv: 0x20002348
        uart:~$ bt adv-data 1009426C7565746F6F74682D5368656C6C
        uart:~$ bt adv-start
        Advertiser[0] 0x20002348 set started

Data 必须按 Bluetooth Core Specification 格式化（参见 version 5.3、vol. 3、part C、11）。此示例中（第一个 octet 为 data 的 size（data 和一个 octet 的 data type（第二个为 data type（``0x09`` 为 Complete Local Name（其余 data 为 ASCII 的 name。因此（在另一 device 上应看到 name *Bluetooth-Shell*。

Advertising 时（若其他 devices 使用 *active* scanner（可能收到 *scan request* packets。要可视化这些 packets（可向 advertiser 的 parameters 添加 :code:`scan-reports`。

Directed Advertising
====================

若想在 shell 上重新连接到 device（可使用 directed advertising。以下示例展示如何在 :code:`directed` parameter 后紧接指定 address 创建 directed advertiser。:code:`low` parameter 表示想使用 low duty cycle mode（:code:`dir-rpa` parameter 在远端 device 启用 privacy 且支持 directed advertisement 中 target address 的 address resolution 时为 required。

.. code-block:: console

        uart:~$ bt adv-create conn-scan directed R:D7:54:03:CE:F3:B4 low dir-rpa
        Created adv id: 0, adv: 0x20002348

之后（可启动 advertiser（然后 target device 将能重新连接。

Extended Advertising
====================

现在来看一些 extended advertising features。要启用 extended advertising（使用 ``ext-adv`` parameter。

.. code-block:: console

        uart:~$ bt adv-create conn-nscan ext-adv
        Created adv id: 0, adv: 0x200022f0
        uart:~$ bt adv-start
        Advertiser[0] 0x200022f0 set started

这将创建 connectable 且 non-scannable 的 extended advertiser。

Encrypted Advertising Data
==========================

Zephyr 支持 Encrypted Advertising Data feature。:code:`bt encrypted-ad` sub-commands 允许管理给定 advertiser 的 advertising data。

要加密 advertising data（需提供 key materials（可用 :code:`bt encrypted-ad set-keys <session key> <init vector>` 完成。Session key 长 16 bytes（initialisation vector 长 8 bytes。

可用 :code:`bt encrypted-ad add-ad` 和 :code:`bt encrypted-ad add-ead` 添加 advertising data。前者将添加一个 advertising data 结构（如 Core Specification 所定义（后者将读取给定 data（加密它们（然后添加生成的 encrypted advertising data 结构。可混合 encrypted 和 non-encrypted data（添加 advertising data 完成后（可用 :code:`bt encrypted-ad commit-ad` 将更改应用到选定 advertiser 的 data。之后可按前述启动 advertiser。可用 :code:`bt encrypted-ad clear-ad` 清除 advertising data。

在 Central 端（可设置如前述的正确 key materials 然后用 :code:`bt encrypted-ad decrypt-scan on` 启用 data 的解密以解密收到的 encrypted advertising data。

.. note::

        要在 scan report 中看到 advertising data（需启用 :code:`bt scan-verbose-output`。

.. note::

        可通过增大 :kconfig:option:`CONFIG_BT_CTLR_ADV_DATA_LEN_MAX` 和 :kconfig:option:`CONFIG_BT_CTLR_SCAN_DATA_LEN_MAX` 的值来增大 advertising data 的长度。

以下是展示 EAD 用法的简单示例：

.. tabs::

        .. group-tab:: Peripheral

                .. code-block:: console

                        uart:~$ bt init
                        ...
                        uart:~$ bt adv-create conn-nscan ext-adv
                        Created adv id: 0, adv: 0x81769a0
                        uart:~$ bt encrypted-ad set-keys 9ba22d3824efc70feb800c80294cba38 2e83f3d4d47695b6
                        session key set to:
                        00000000: 9b a2 2d 38 24 ef c7 0f  eb 80 0c 80 29 4c ba 38 |..-8$... ....)L.8|
                        initialisation vector set to:
                        00000000: 2e 83 f3 d4 d4 76 95 b6                          |.....v..         |
                        uart:~$ bt encrypted-ad add-ad 06097368656c6c
                        uart:~$ bt encrypted-ad add-ead 03ffdead03ffbeef
                        uart:~$ bt encrypted-ad commit-ad
                        Advertising data for Advertiser[0] 0x81769a0 updated.
                        uart:~$ bt adv-start
                        Advertiser[0] 0x81769a0 set started

        .. group-tab:: Central

                .. code-block:: console

                        uart:~$ bt init
                        ...
                        uart:~$ bt scan-verbose-output on
                        uart:~$ bt encrypted-ad set-keys 9ba22d3824efc70feb800c80294cba38 2e83f3d4d47695b6
                        session key set to:
                        00000000: 9b a2 2d 38 24 ef c7 0f  eb 80 0c 80 29 4c ba 38 |..-8$... ....)L.8|
                        initialisation vector set to:
                        00000000: 2e 83 f3 d4 d4 76 95 b6                          |.....v..         |
                        uart:~$ bt encrypted-ad decrypt-scan on
                        Received encrypted advertising data will now be decrypted using provided key materials.
                        uart:~$ bt scan on
                        Bluetooth active scan enabled
                        [DEVICE]: R:68:49:30:68:49:30, AD evt type 5, RSSI -59   shell C:1 S:0 D:0 SR:0 E:1 Prim: LE 1M, Secn: LE 2M, Interval: 0x0000 (0 us), SID: 0x0
                                [SCAN DATA START - EXT_ADV]
                                Type 0x09:    shell
                                Type 0x31: Encrypted Advertising Data: 0xe2, 0x17, 0xed, 0x04, 0xe7, 0x02, 0x1d, 0xc9, 0x40, 0x07, uart:~0x18, 0x90, 0x6c, 0x4b, 0xfe, 0x34, 0xad
                                [START DECRYPTED DATA]
                                Type 0xff: 0xde, 0xad
                                Type 0xff: 0xbe, 0xef
                                [END DECRYPTED DATA]
                                [SCAN DATA END]
                        ...

Filter Accept List
******************

可创建允许 addresses 的列表（可用于自动连接到这些 addresses。以下是如何做到：

.. code-block:: console

        uart:~$ bt fal-add R:47:38:76:EA:29:36
        uart:~$ bt fal-add R:66:C8:80:2A:05:73
        uart:~$ bt fal-connect on

Shell 然后连接到第一个可用 device。示例中（若两个 devices 同时 advertising（将连接到添加到列表的第一个 address。

Filter Accept List 也可用 :code:`fal` option 用于 scanning 或 advertising。例如（若想扫描一组选定的 addresses（可设置 Filter Accept List：

.. code-block:: console

        uart:~$ bt fal-add R:65:4B:9E:83:AF:73
        uart:~$ bt fal-add R:73:72:82:B4:8F:B9
        uart:~$ bt fal-add R:5D:85:50:1C:72:64
        uart:~$ bt scan on fal

应只看到 scanner 报告的这三个 addresses。

Enabling security
*****************

连接到 device 时（可启用多个安全级别（以下是 Bluetooth LE 的列表：

* **1** 无 encryption 且无 authentication；
* **2** Encryption 且无 authentication；
* **3** Encryption 和 authentication；
* **4** Bluetooth LE Secure Connection。

要启用 security（使用 :code:`bt security <level>` 命令。对于需要 authentication 的级别（level 3 及以上（须先设置 authentication 方法。为此（可用 :code:`bt auth all` 命令。之后（设置 security level 时（将在两个 devices 上被要求确认 passkey。在 shell 端（用 :code:`bt auth-passkey-confirm` 命令完成。

Pairing
=======

启用 authentication 要求 devices 为 bondable。默认 shell 为 bondable。可用 :code:`bt bondable off` 使 shell 非 bondable。可用 :code:`bt bonds` 命令列出所有已配对的 devices。

最大 paired devices 数用 :kconfig:option:`CONFIG_BT_MAX_PAIRED` 设置。可用 :code:`bt clear <address: P:XX:XX:XX:XX:XX:XX or R:XX:XX:XX:XX:XX:XX>` 移除 paired device（或用 :code:`bt clear all` 命令移除所有 paired devices。
