.. _autopts-win10:

在 Windows 10 上使用 nRF52 板卡的 AutoPTS
#######################################

本教程介绍如何搭建 AutoPTS 客户端和服务器，使两者都运行在
Windows 10 上。我们使用 WSL1 搭配 Ubuntu，仅用于将 Zephyr 项目
构建为 elf 文件，因为 Zephyr SDK 在 Windows 上尚不可用。
本教程仅涵盖 nrf52840dk。

.. contents::
    :local:
    :depth: 2

更新 Windows 和驱动程序
===========================

按以下路径更新 Windows：

开始 -> 设置 -> 更新和安全 -> Windows 更新

更新驱动程序，请按照你的硬件厂商的说明操作。

安装 Python 3
=================

下载并安装 `Python 3 <https://www.python.org/downloads/>`_。
本教程在 >=3.8 版本上测试通过。让安装程序将 Python
安装目录添加到 PATH，并禁用路径长度限制。

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

安装 PTS 8
=============

从 https://www.bluetooth.org 安装最新的 PTS。记得从
安装目录安装驱动程序
"C:/Program Files (x86)/Bluetooth SIG/Bluetooth PTS/PTS Driver/win64/CSRBlueCoreUSB.inf"

.. image:: install_pts_drivers.png
   :height: 250
   :width: 850
   :align: center

.. note::

    从 PTS 8.0.1 开始，不再包含 Bluetooth Protocol Viewer。
    因此要捕获 Bluetooth 事件，你必须单独下载它。

为 Windows 搭建 Zephyr 项目
=================================

执行 :ref:`Getting Started Guide <getting_started>` 中的 Windows 搭建步骤。

安装 nrftools
=================

在 Windows 上从网站
https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Command-Line-Tools/Download 下载最新的 nrftools（版本 >= 10.12.1），
并运行默认安装。

.. image:: download_nrftools_windows.png
   :height: 350
   :width: 500
   :align: center

连接设备
================

.. image:: devices_1.png
   :height: 400
   :width: 600
   :align: center

.. image:: devices_2.png
   :height: 700
   :width: 500
   :align: center

烧录板卡
============

在设备管理器中找到你的 nrf 板卡的 COM 端口。在我的情况下是 COM3。

.. image:: device_manager.png
   :height: 400
   :width: 450
   :align: center

在 Git Bash 中，进入 zephyrproject

.. code-block::

    cd ~/zephyrproject

构建 auto-pts tester 应用

.. code-block::

    west build -p auto -b nrf52840dk/nrf52840 zephyr/tests/bluetooth/tester/

你可以用以下命令显示烧录选项：

.. code-block::

    west flash --help

并用之前构建的 elf 文件烧录板卡：

.. code-block::

    west flash --no-rebuild --board-dir /dev/ttyS2 --elf-file ~/zephyrproject/build/zephyr/zephyr.elf

注意 west 不接受 COM 端口，因此使用 /dev/ttyS2 作为 COM3 的等价物，
/dev/ttyS2 作为 COM3 的等价物，依此类推（/dev/ttyS + 递减的 COM 编号）。

搭建 auto-pts 项目
=======================

在 Git Bash 中克隆项目仓库：

.. code-block::

    git clone https://github.com/auto-pts/auto-pts.git

进入项目文件夹：

.. code-block::

    cd auto-pts

安装所需的 python 模块：

.. code-block::

   pip3 install --user wheel
   pip3 install --user -r autoptsserver_requirements.txt
   pip3 install --user -r autoptsclient_requirements.txt

安装 socat.exe
==================

从 https://sourceforge.net/projects/unix-utils/files/socat/1.7.3.2/ 下载并解压 socat.exe
到文件夹 ~/socat-1.7.3.2-1-x86_64/。

.. image:: download_socat.png
   :height: 400
   :width: 450
   :align: center

将 socat.exe 所在目录的路径添加到 PATH：

.. image:: add_socat_to_path.png
   :height: 400
   :width: 450
   :align: center

运行 AutoPTS
================

服务器和客户端默认将运行在 localhost 地址上。运行服务器：

.. code-block::

    python ./autoptsserver.py -S 65000

.. image:: autoptsserver_run.png
   :height: 200
   :width: 800
   :align: center

.. note::

    如果全新搭建后出现错误 "ImportError: No module named pywintypes"，
    请卸载并重新安装 pywin32 模块：

    .. code-block::

        pip install --upgrade --force-reinstall pywin32

运行客户端：

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master ~/zephyrproject/build/zephyr/zephyr.elf -t COM3 -b nrf52 -S 65000 -C 65001

.. image:: autoptsclient_run.png
   :height: 200
   :width: 800
   :align: center

首次运行时，当 Windows 询问时，允许通过防火墙连接：

.. image:: allow_firewall.png
   :height: 450
   :width: 600
   :align: center

故障排除
================

- "运行真实硬件测试模式时，我只遇到 BTP TIMEOUT。"

这是 auto-pts 客户端与板卡之间连接的问题。可能有多种原因。尝试：

- 使用以下命令清理你的 auto-pts 和 zephyr 仓库

.. warning::

    该命令将强制不可逆地删除仓库中所有未提交的文件。

.. code-block::

    git clean -fdx

然后重新构建并烧录 tester elf。

- 如果你在虚拟机上搭建了 Windows，检查 guest 扩展是否正确安装，或将虚拟机设置中的 USB 兼容性模式改为 USB 2.0。

- 检查防火墙是否没有阻止 python.exe 或 socat.exe。

- 检查板卡在重启后是否发送 ready 事件（十六进制 00 00 80 ff 00 00）。使用例如 PuTTy 以正确的 COM 和波特率打开与板卡的串行连接。板卡复位后你应该能在控制台中看到一些字符串。

- 检查 socat.exe 是否创建到板卡的隧道。在控制台中运行

.. code-block::

    socat.exe -x -v tcp-listen:65123 /dev/ttyS2,raw,b115200

其中 /dev/ttyS2 是 COM3 的等价物。打开 PuTTY，将连接类型设为 Raw，IP 设为 127.0.0.1，端口设为 65123。板卡复位后你应该能在控制台中看到一些字符串。
