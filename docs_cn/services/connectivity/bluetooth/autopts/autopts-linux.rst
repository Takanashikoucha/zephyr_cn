.. _autopts-linux:

Linux 上的 AutoPTS
################

本教程介绍如何在 Linux 上搭建 AutoPTS 客户端，而 AutoPTS 服务器运行在 Windows 10 虚拟机中。已在 Ubuntu 20.4 和 Linux Mint 20.4 上测试。

你必须已搭建好 Zephyr 开发环境。详情参见 :ref:`getting_started`。

测试 Zephyr 蓝牙主机所支持的方法：

- 在 QEMU 上测试 Zephyr Host Stack

- 在 :zephyr:board:`native_sim <native_sim>` 上测试 Zephyr Host Stack

- 在真实硬件（如 nRF52）上测试 Zephyr 组合（controller + host）构建

有关在 QEMU 或 :zephyr:board:`native_sim <native_sim>` 上运行的方法，参见 :ref:`bluetooth_qemu_native`。

.. contents::
    :local:
    :depth: 2

搭建 Linux
***********

请按照 :ref:`getting_started` 了解如何为构建和烧录应用程序搭建 Linux 环境。

搭建 Windows 10/11 虚拟机
***********************************

选择并安装你的 hypervisor，例如 VMWare Workstation（推荐）或 VirtualBox。如果主机 CPU 少于 6 个，使用 VirtualBox 可能会遇到一些问题。

创建 Windows 虚拟机实例。确保它至少有 2 个核心，并已安装 guest 扩展。

本教程在 VirtualBox 7.2.4 和 VMWare Workstation 16.1.1 Pro 上测试通过。

更新 Windows
=============

按以下路径更新 Windows：

开始 -> 设置 -> 更新和安全 -> Windows 更新

配置 NAT
=========

可以使用 NAT 和端口转发来建立 Linux 主机与 Windows 客户机之间的通信。这是 VirtualBox 最简单的配置方式，无需配置任何静态 IP，也不会被 Windows 防火墙拦截。

VirtualBox
----------

打开虚拟机的网络设置。在适配器 1 上，默认会创建 NAT。
打开 Port Forwarding 菜单并添加你想要的端口。


.. image:: virtualbox_nat_1.png
   :width: 500
   :align: center

例如，设置以下内容后，你就可以使用
``localhost:65000`` 和 ``localhost:65002``（或 ``127.0.0.0:65000`` 和 ``127.0.0.0:65002``）
来连接运行在 Windows 中 65000 和 65002 端口上的 AutoPTS 服务器。

.. image:: virtualbox_nat_2.png
   :width: 500
   :align: center

配置静态 IP
==============

如果你不能或不想使用 NAT，也可以配置静态 IP。

VMWare Workstation
----------------

在 Linux 上，打开 Virtual Network Editor 应用并创建网络：

.. image:: vmware_static_ip_1.png
   :height: 400
   :width: 500
   :align: center

打开虚拟机的网络设置。添加自定义适配器：

.. image:: vmware_static_ip_2.png
   :height: 400
   :width: 500
   :align: center

如果你在终端中输入 'ifconfig'，你应该能找到你的主机 IP：

.. image:: vmware_static_ip_3.png
   :height: 150
   :width: 550
   :align: center

VirtualBox
----------

在 Linux、macOS 和 Solaris 上，Oracle VM VirtualBox 只允许将 ``192.168.56.0/21`` 范围内的 IP 地址分配给 host-only 适配器，因此如果使用 VirtualBox 配置静态地址，这是唯一可用的地址范围。

转到：

文件 -> 工具 -> 网络管理器

并创建网络：

.. image:: virtualbox_static_ip_1.png
   :width: 500
   :align: center

打开虚拟机的网络设置。在适配器 1 上，默认会创建 NAT。
添加适配器 2：

.. image:: virtualbox_static_ip_2.png
   :width: 500
   :align: center

Windows
-------

在 Windows 虚拟机上配置静态 IP。转到

设置 -> 网络和 Internet -> 以太网 -> 未识别的网络 -> 编辑

并设置：

.. image:: windows_static_ip.png
   :height: 400
   :width: 400
   :align: center


安装 Python 3
===============

在 Windows 上下载并安装最新的 `Python 3 <https://www.python.org/downloads/>`_。
让安装程序将 Python 安装目录添加到 PATH，并禁用路径长度限制。

.. image:: install_python1.png
   :height: 300
   :width: 450
   :align: center

.. image:: install_python2.png
   :height: 300
   :width: 450
   :align: center

安装 Git
===========

下载并安装 `Git <https://git-scm.com/downloads>`_。
安装期间启用选项：Enable experimental support for pseudo
consoles。我们将使用 Git Bash 作为 Windows 终端。

.. image:: install_git.png
   :height: 350
   :width: 400
   :align: center

安装 PTS
===========

在 Windows 虚拟机上，从 https://pts.bluetooth.com/download 安装最新的 PTS。
记得从安装目录安装驱动程序
"C:/Program Files (x86)/Bluetooth SIG/Bluetooth PTS/PTS Driver/win64/CSRBlueCoreUSB.inf"

.. image:: install_pts_drivers.png
   :height: 250
   :width: 850
   :align: center

.. note::

    从 PTS 8.0.1 开始，不再包含 Bluetooth Protocol Viewer。
    因此要捕获 Bluetooth 事件，你必须单独下载它。

连接 PTS 适配器
==================

使用 VirtualBox 应该没有问题。只需在 设备 -> USB 中找到适配器并连接即可。

使用 VMWare 时你可能需要采用一些技巧，如果你在
VM -> 可移动设备中找不到适配器。在 Linux 终端中输入：

.. code-block::

    usb-devices

并在输出中找到你的 PTS 蓝牙 USB 适配器

.. image:: usb-devices_output.png
   :height: 100
   :width: 500
   :align: center

记下 Vendor 和 ProdID 号。关闭 VMWare Workstation 并用文本编辑器打开你的虚拟机 .vmx 文件
（路径类似于 /home/codecoup/vmware/Windows 10/Windows 10.vmx）。
在文件中任意位置写入以下行：

.. code-block::

    usb.autoConnect.device0 = "0x0a12:0x0001"

只需将 0x0a12 替换为你找到的 Vendor 号，将 0x0001 替换为你找到的 ProdID 号。

连接设备（仅在真实硬件测试模式下需要）
****************************************************************

.. image:: devices_1.png
   :height: 400
   :width: 600
   :align: center

.. image:: devices_2.png
   :height: 700
   :width: 500
   :align: center

搭建 auto-pts 项目
**********************

Linux 上的 AutoPTS 客户端
=======================

克隆 auto-pts 项目：

.. code-block::

    git clone https://github.com/auto-pts/auto-pts.git


安装 socat，它用于从 UART 的 tty 文件传输 BTP 数据流：

.. code-block::

    sudo apt-get install python-setuptools socat

安装所需的 python 模块：

.. code-block::

   cd auto-pts
   pip3 install --user -r autoptsclient_requirements.txt

Windows 虚拟机上的 AutoPTS 服务器
=========================================

在 Git Bash 中克隆 auto-pts 项目仓库：

.. code-block::

    git clone https://github.com/auto-pts/auto-pts.git

安装所需的 python 模块：

.. code-block::

   cd auto-pts
   pip3 install --user wheel
   pip3 install --user -r autoptsserver_requirements.txt

重启虚拟机。

运行 AutoPTS
***************

请按照
https://github.com/zephyrproject-rtos/zephyr/tree/main/tests/bluetooth/tester 中的信息了解如何构建、
烧录并运行 Bluetooth Tester 应用程序。

服务器和客户端默认将运行在 localhost 地址上。
在 Windows 虚拟机中运行服务器：

.. code-block::

    python ./autoptsserver.py

.. image:: autoptsserver_run_2.png
   :height: 120
   :width: 700
   :align: center

另请参阅 https://github.com/auto-pts/auto-pts 了解如何运行 auto-pts 的更多信息。

在硬件上测试 Zephyr Host Stack
=====================================

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master -t /dev/ttyACM0 -b BOARD -i SERVER_IP -l LOCAL_IP

其中 ``/dev/ttyACM0`` 是该板卡的 tty，
``BOARD`` 是要使用的板卡（例如 ``nrf53_audio``），
``SERVER_IP`` 是 AutoPTS 服务器的 IP，
``LOCAL_IP`` 是 Linux 机器的本地 IP。

在 QEMU 上测试 Zephyr Host Stack
=================================

需要挂载一个 Bluetooth controller。
有关使用 HCI UART 运行的方法，请参见 :zephyr:code-sample:`bluetooth_hci_uart`。

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master BUILD_DIR/zephyr/zephyr.elf -i SERVER_IP -l LOCAL_IP

其中 ``BUILD_DIR`` 是构建目录，
``SERVER_IP`` 是 AutoPTS 服务器的 IP，
``LOCAL_IP`` 是 Linux 机器的本地 IP。

在 :zephyr:board:`native_sim <native_sim>` 上测试 Zephyr Host Stack
===================================================================

当 tester 应用程序为 :zephyr:board:`native_sim <native_sim>` 构建后，它会生成一个
``zephyr.exe`` 文件，可以作为原生 Linux 应用程序运行。
根据你的系统，
你可能需要执行以下步骤才能成功运行 ``zephyr.exe``。

设置 capabilities
--------------------

由于该应用程序需要访问用于连接 HCI 套接字的权限，
你可能需要执行以下操作

.. code-block::

    setcap cap_net_raw,cap_net_admin,cap_sys_admin+ep zephyr.exe

如果你使用例如 ``sudo`` 运行 ``zephyr.exe`` 或 ``./autoptsclient-zephyr.py``，则不需要此操作。

关闭 HCI controller
--------------------------

在运行 ``zephyr.exe`` 之前，你可能还需要"down"（关闭）或"power off"（断电）HCI controller。
可以使用 ``hciconfig`` 完成：

.. code-block::

    hciconfig hciX down

其中 ``hciX`` 是类似 ``hci0`` 的值。你可以运行 ``hciconfig`` 获取你的 HCI 设备列表。

由于 ``hciconfig`` 在某些系统上已被弃用，你可能需要使用

.. code-block::

    btmgmt -i hciX power off

与 ``hciconfig`` 类似，``btmgmt info`` 可用于列出当前 controller 及其状态。

关闭 controller 电源时，``hciconfig`` 和 ``btmgmt`` 都可能需要 ``sudo``。

运行客户端
------------------

该应用程序可以这样运行：

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master --hci HCI BUILD_DIR/zephyr/zephyr.exe -i SERVER_IP -l LOCAL_IP

其中 ``HCI`` 是 HCI 索引，例如 ``0`` 或 ``1``，
``BUILD_DIR`` 是构建目录，
``SERVER_IP`` 是 AutoPTS 服务器的 IP，
``LOCAL_IP`` 是 Linux 机器的本地 IP。

故障排除
****************

运行完一个测试后，我需要重启 Windows 虚拟机才能运行另一个测试，因为 PTS 日志中 APICOM 的 fail verdict
===================================================================================================================================

这意味着你的虚拟机处理器核心或内存不足。尝试在
设置中添加更多。注意，使用 VirtualBox 作为 hypervisor 时，4 个 CPU 的主机可能不够。
在这种情况下，建议选择 VMWare Workstation。

我无法启动 autoptsserver-zephyr.py。我总是遇到 Python 错误
===================================================================

.. image:: autoptsserver_typical_error.png
   :height: 300
   :width: 650
   :align: center

以下一个或多个步骤应该有帮助：

- 关闭所有 PTS 窗口。

- 重新插拔 PTS 蓝牙适配器。

- 删除临时工作区。你可以在 auto-pts-code/workspaces/zephyr/zephyr-master/ 中找到它，名为 temp_zephyr-master。小心，不要删除原始工作区 zephyr-master.pqw6。

- 重启 Windows 虚拟机。

PTS 自动化窗口不断打开和关闭
===================================================

这表明它无法捕获 PTS 适配器。
如果 AutoPTS 服务器能够找到并使用 PTS 适配器，
则该窗口标题将显示该适配器的 Bluetooth 地址。
如果没有发生这种情况，请确保适配器已插入、已更新并被 PTS 识别。

.. image:: pts_automation_window.png
   :width: 500
   :align: center

如果之后仍然无法运行测试，
请确保已安装 Bluetooth Protocol Viewer。
