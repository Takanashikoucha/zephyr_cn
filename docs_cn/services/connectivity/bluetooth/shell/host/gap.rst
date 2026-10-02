Bluetooth: GAP 外壳
####################

GAP 外壳是 Bluetooth 的"主"外壳，负责连接管理、扫描、广播等。


身份
**********

身份（Identities）是 Zephyr 主机的概念，允许单个物理设备表现得像多个逻辑 Bluetooth 设备。

外壳允许创建多个身份，最大数量由 Kconfig 符号 :kconfig:option:`CONFIG_BT_ID_MAX` 设定。要创建新身份，请使用 :code:`bt id-create` 命令。然后可以用其 ID 通过 :code:`bt id-select <id>` 选择它。最后，你可以用 :code:`id-show` 列出所有可用身份。

扫描设备
****************

使用 :code:`bt scan on` 命令开始扫描。根据你所处的环境，你可能会在 shell 上看到打印许多行。要停止扫描，运行 :code:`bt scan off`，滚动应该会停止。

以下是你可能预期看到的示例：

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

如你所见，这可能导致大量结果。要减少该数量并轻松找到特定设备，你可以启用扫描过滤器。有四种过滤器类型：按名称、按 RSSI、按地址和按周期性广播间隔。要应用过滤器，请使用 :code:`bt scan-set-filter` 命令后跟过滤器类型。你可以再次使用命令添加多个过滤器。

例如，如果你只想查找名称为 *test shell* 的设备：

.. code-block:: console

        uart:~$ bt scan-filter-set name "test shell"

或者如果你想查找非常近距离的设备：

.. code-block:: console

        uart:~$ bt scan-filter-set rssi -40
        RSSI cutoff set at -40 dB

最后，如果你想移除所有过滤器：

.. code-block:: console

        uart:~$ bt scan-filter-clear all

你可以使用 :code:`bt scan on` 命令创建一个*主动*扫描器，意味着扫描器将通过发送*扫描请求*数据包向广播器请求更多信息。或者，你可以使用 :code:`bt scan passive` 命令创建一个*被动扫描器*，这样扫描器就不会向广播器请求更多信息。

启用 :kconfig:option:`CONFIG_BT_SCAN_EXT_FILTER_POLICY` 后，
:code:`bt scan --ext-filter-policy on` 命令以扩展扫描器过滤策略启动扫描器。控制器还会报告其目标地址为无法解析的可解析私有地址的定向广播。定向广播的目标地址会单独打印在一行。这需要支持扩展扫描器过滤策略的控制器，否则命令会失败。

连接到设备
**********************

要连接到设备，你需要知道其地址和地址类型，并使用
:code:`bt connect` 命令，以地址和类型作为参数。

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

你可以使用 :code:`bt connections` 命令列出 shell 的活跃连接。Shell 的最大连接数由 :kconfig:option:`CONFIG_BT_MAX_CONN` 定义。你可以用
:code:`bt disconnect <address: P:XX:XX:XX:XX:XX:XX or R:XX:XX:XX:XX:XX:XX>` 命令从连接断开。

.. note::

        如果你刚刚在扫描，你可以通过简单运行 :code:`bt connect` 命令连接到最后扫描到的设备。

        或者，你可以使用 :code:`bt connect-name <name>` 命令自动启用带名称过滤的扫描并连接到第一个匹配项。

广播
***********

使用 :code:`bt advertise on` 命令开始广播。这将使用默认参数，并以设备名称广播一个可解析私有地址。你可以通过运行 :code:`bt advertise on identity` 选择改用身份地址。要停止广播，请使用 :code:`bt advertise off` 命令。

要启用广播的更多高级功能，你应该使用
:code:`bt adv-create` 命令创建一个广播器。广播器的参数可以在创建时传递，也可以使用 :code:`bt adv-param` 命令。要使用这个新创建的广播器开始广播，请使用 :code:`bt adv-start` 命令，然后用 :code:`bt adv-stop` 命令停止
广播。

使用自定义广播器时，你可以选择它是否可连接或可扫描。这导致
四个选项：:code:`conn-scan`、:code:`conn-nscan`、:code:`nconn-scan` 和 :code:`nconn-nscan`。
创建广播器或更新其参数时，这些参数是必需的。

例如，如果你想创建一个可连接且可扫描的广播器并启动它：

.. code-block:: console

        uart:~$ bt adv-create conn-scan
        Created adv id: 0, adv: 0x200022f0
        uart:~$ bt adv-start
        Advertiser[0] 0x200022f0 set started

你可能注意到，用这种方式，自定义广播器不会广播设备名称；你需要
添加它。继续之前的示例：

.. code-block:: console

        uart:~$ bt adv-stop
        Advertiser set stopped
        uart:~$ bt adv-data dev-name
        uart:~$ bt adv-start
        Advertiser[0] 0x200022f0 set started

现在你应该能在广播数据中看到设备名称。你也可以用
:code:`name <custom name>` 代替 :code:`dev-name` 设置自定义名称。还可用
:code:`bt adv-data` 命令手动设置广播数据。以下示例展示了
如何使用原始广播数据来设置广播器名称：

.. code-block:: console

        uart:~$ bt adv-create conn-scan
        Created adv id: 0, adv: 0x20002348
        uart:~$ bt adv-data 1009426C7565746F6F74682D5368656C6C
        uart:~$ bt adv-start
        Advertiser[0] 0x20002348 set started

数据必须按照 Bluetooth 核心规范格式化（参见 5.3 版，第 3 卷，
C 部分，11 节）。在此示例中，第一个字节是数据的大小（数据和用于
数据类型的 1 个字节），第二个是数据类型，``0x09`` 是完整本地名称，
其余数据是 ASCII 的名称。因此，在另一台设备上你应该看到名称
*Bluetooth-Shell*。

广播时，如果其他设备使用*主动*扫描器，你可能会收到*扫描请求*数据包。
要可视化这些数据包，你可以向广播器的参数中添加 :code:`scan-reports`。

定向广播
====================

如果你想重新连接到设备，可以在 shell 上使用定向广播。
以下示例演示了如何创建定向广播器，地址紧跟在参数 :code:`directed` 之后指定。:code:`low` 参数表示我们想使用
低占空比模式，:code:`dir-rpa` 参数在远端设备
启用了隐私且支持定向广播中目标地址的地址解析时是必需的。

.. code-block:: console

        uart:~$ bt adv-create conn-scan directed R:D7:54:03:CE:F3:B4 low dir-rpa
        Created adv id: 0, adv: 0x20002348

之后，你可以启动广播器，然后目标设备就能重新连接。

扩展广播
====================

现在让我们来看一些扩展广播功能。要启用扩展广播，请使用
``ext-adv`` 参数。

.. code-block:: console

        uart:~$ bt adv-create conn-nscan ext-adv
        Created adv id: 0, adv: 0x200022f0
        uart:~$ bt adv-start
        Advertiser[0] 0x200022f0 set started

这将创建一个可连接且不可扫描的扩展广播器。

加密广播数据
==========================

Zephyr 支持加密广播数据功能。:code:`bt encrypted-ad`
子命令允许管理给定广播器的广播数据。

要加密广播数据，需要提供密钥材料，可以用 :code:`bt
encrypted-ad set-keys <session key> <init vector>` 完成。会话密钥长 16 字节，
初始化向量长 8 字节。

你可以使用 :code:`bt encrypted-ad add-ad` 和 :code:`bt encrypted-ad
add-ead` 添加广播数据。前者将添加一个广播数据结构（如核心
规范所定义），后者将读取给定数据、加密它们，然后添加生成的
加密广播数据结构。可以混合加密和非加密数据，
添加广播数据完成后，:code:`bt encrypted-ad commit-ad` 可用于将更改
应用到所选广播器的数据。之后可以按前述方式启动广播器。
可以用 :code:`bt encrypted-ad clear-ad` 清除广播数据。

在中心设备一侧，可以通过设置如前述的正确密钥材料，然后用
:code:`bt encrypted-ad decrypt-scan on` 启用数据解密，
来解密接收到的加密广播数据。

.. note::

        要在扫描报告中看到广播数据，需要启用 :code:`bt scan-verbose-output`。

.. note::

        可以通过增大 :kconfig:option:`CONFIG_BT_CTLR_ADV_DATA_LEN_MAX` 和
        :kconfig:option:`CONFIG_BT_CTLR_SCAN_DATA_LEN_MAX` 的值来增大广播数据的长度。

以下是展示 EAD 用法的简单示例：

.. tabs::

        .. group-tab:: 外围设备

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
                        uart:~$ bt encrypted-ad add-ad 06097368656C6C
                        uart:~$ bt encrypted-ad add-ead 03ffdead03ffbeef
                        uart:~$ bt encrypted-ad commit-ad
                        Advertising data for Advertiser[0] 0x81769a0 updated.
                        uart:~$ bt adv-start
                        Advertiser[0] 0x81769a0 set started

        .. group-tab:: 中心设备

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

过滤接受列表
******************

可以创建允许地址的列表，用于
自动连接到这些地址。以下是如何做到：

.. code-block:: console

        uart:~$ bt fal-add R:47:38:76:EA:29:36
        uart:~$ bt fal-add R:66:C8:80:2A:05:73
        uart:~$ bt fal-connect on

然后 shell 将连接到第一个可用设备。在示例中，如果两个设备
同时广播，我们将连接到添加到列表的第一个地址。

过滤接受列表也可以用 :code:`fal` 选项用于扫描或广播。
例如，如果我们想扫描一组选定的地址，我们可以设置一个过滤接受
列表：

.. code-block:: console

        uart:~$ bt fal-add R:65:4B:9E:83:AF:73
        uart:~$ bt fal-add R:73:72:82:B4:8F:B9
        uart:~$ bt fal-add R:5D:85:50:1C:72:64
        uart:~$ bt scan on fal

你应该只看到扫描器报告的这三个地址。

启用安全
*****************

连接到设备时，你可以启用多个安全级别，以下是
Bluetooth LE 的列表：

* **1** 无加密且无认证；
* **2** 加密且无认证；
* **3** 加密和认证；
* **4** Bluetooth LE 安全连接。

要启用安全，请使用 :code:`bt security <level>` 命令。对于需要认证
的级别（3 级及以上），你必须先设置认证方法。为此，你可以使用
:code:`bt auth all` 命令。之后，当你设置安全级别时，你将被要求
在两台设备上确认配对密钥。在 shell 一侧，用命令
:code:`bt auth-passkey-confirm` 完成。

配对
=======

启用认证要求设备可绑定。默认情况下 shell 是可绑定的。你
可以用 :code:`bt bondable off` 使 shell 不可绑定。你可以用 :code:`bt bonds` 命令列出所有已配对的设备。

最大配对设备数用 :kconfig:option:`CONFIG_BT_MAX_PAIRED` 设置。你可以
用 :code:`bt clear <address: P:XX:XX:XX:XX:XX:XX or R:XX:XX:XX:XX:XX:XX>`
移除一个配对设备，或用 :code:`bt clear all` 命令移除所有配对设备。
