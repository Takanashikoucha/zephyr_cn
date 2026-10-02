.. _bluetooth_shell:

Shell
#####

蓝牙 Shell 是基于 :ref:`shell_api` 模块构建的应用。它提供一组命令，用于便捷地与蓝牙协议栈交互。

关于具体的蓝牙功能，还请参见以下 Shell 文档

.. toctree::
   :maxdepth: 1

   shell/audio/bap.rst
   shell/audio/bap_broadcast_assistant.rst
   shell/audio/bap_scan_delegator.rst
   shell/audio/cap.rst
   shell/audio/ccp.rst
   shell/audio/csip.rst
   shell/audio/gmap.rst
   shell/audio/mcp.rst
   shell/audio/tbs.rst
   shell/audio/tmap.rst
   shell/audio/pbp.rst
   shell/classic/a2dp.rst
   shell/classic/avrcp.rst
   shell/classic/goep.rst
   shell/classic/hfp.rst
   shell/classic/l2cap.rst
   shell/classic/map.rst
   shell/classic/pbap.rst
   shell/classic/spp.rst
   shell/host/gap.rst
   shell/host/gatt.rst
   shell/host/iso.rst
   shell/host/l2cap.rst

蓝牙 Shell 的设置与使用
*******************************

首先需要构建并烧录带蓝牙 Shell 的板子。具体方法参见
:ref:`getting_started`。蓝牙 Shell 本身位于
:zephyr_file:`tests/bluetooth/shell/`。

完成后，使用你喜欢的串口终端应用连接到 CLI。你应该看到如下提示符：

.. code-block:: console

        uart:~$

关于 Shell 通用用法的更多细节，参见 :ref:`shell_api`。

第一步是启用蓝牙。为此，使用 :code:`bt init` 命令。以下消息会打印出来以确认蓝牙已初始化。

.. code-block:: console

        uart:~$ bt init
        Bluetooth initialized
        Settings Loaded
        [00:02:26.771,148] <inf> fs_nvs: nvs_mount: 8 Sectors of 4096 bytes
        [00:02:26.771,148] <inf> fs_nvs: nvs_mount: alloc wra: 0, fe8
        [00:02:26.771,179] <inf> fs_nvs: nvs_mount: data wra: 0, 0
        [00:02:26.777,984] <inf> bt_hci_core: hci_vs_init: HW Platform: Nordic Semiconductor (0x0002)
        [00:02:26.778,015] <inf> bt_hci_core: hci_vs_init: HW Variant: nRF52x (0x0002)
        [00:02:26.778,045] <inf> bt_hci_core: hci_vs_init: Controller: Zephyr Bluetooth Controller (0x00) manufacturer 0x05f1 Version 3.2 Build 99
        [00:02:26.778,656] <inf> bt_hci_core: bt_init: No ID address. App must call settings_load()
        [00:02:26.794,738] <inf> bt_hci_core: bt_dev_show_info: Identity: R:EB:BF:36:26:42:09
        [00:02:26.794,769] <inf> bt_hci_core: bt_dev_show_info: HCI: version 5.3 (0x0c) revision 0x0000, manufacturer 0x05f1
        [00:02:26.794,799] <inf> bt_hci_core: bt_dev_show_info: LMP: version 5.3 (0x0c) subver 0xffff


日志
*******

可以在运行时按模块配置日志级别。这取决于编译时设定的最大日志级别。配置时使用 :code:`log` 命令。以下是一些示例：

* 列出可用模块及其当前日志级别

.. code-block:: console

        uart:~$ log status

* 禁用 *bt_hci_core* 的日志

.. code-block:: console

        uart:~$ log disable bt_hci_core

* 为 *bt_att* 和 *bt_smp* 启用错误日志

.. code-block:: console

        uart:~$ log enable err bt_att bt_smp

* 禁用所有模块的日志

.. code-block:: console

        uart:~$ log disable

* 为所有模块启用警告日志

.. code-block:: console

        uart:~$ log enable wrn
