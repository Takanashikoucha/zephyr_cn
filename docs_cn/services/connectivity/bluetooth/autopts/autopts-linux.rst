.. _autopts-linux:

AutoPTS
on
Linux
################

这
个
tutorial
展示
如何
在
Linux
上
setup
AutoPTS
client
同时
AutoPTS
server
运行
在
Windows
10
virtual
machine
上。
在
Ubuntu
20.4
和
Linux
Mint
20.4
上
tested。

你
必须
已
setup
Zephyr
development
environment。
参考
:ref:`getting_started`
获取
details。

支持
的
测试
zephyr
bluetooth
host
的
methods：

-
Testing
Zephyr
Host
Stack
on
QEMU

-
Testing
Zephyr
Host
Stack
on
:zephyr:board:`native_sim
<native_sim>`

-
Testing
Zephyr
combined
（controller
+
host）
build
on
Real
hardware
（such
as
nRF52）

要
运行
QEMU
或
:zephyr:board:`native_sim
<native_sim>`
参考
:ref:`bluetooth_qemu_native`。

.. contents::
    :local:
    :depth:
    2

Setup
Linux
***********

参考
:ref:`getting_started`
获取
如何
setup
Linux
用于
build
和
flash
applications。

Setup
Windows
10/11
virtual
machine
***********************************

选择
并
install
你
的
hypervisor
如
VMWare
Workstation
（preferred）
或
VirtualBox。
在
VirtualBox
上
可能
有
一些
issues
如果
你
的
host
有
少于
6
个
CPU。

创建
Windows
virtual
machine
instance。
确保
它
有
至少
2
个
cores
并
install
了
guest
extensions。

Setup
在
VirtualBox
7.2.4
和
VMWare
Workstation
16.1.1
Pro
上
tested。


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
==================

With VirtualBox there should be no problem. Just find dongle in Devices -> USB and connect.

With VMWare you might need to use some trick, if you cannot find dongle in
VM -> Removable Devices. Type in Linux terminal:

.. code-block::

    usb-devices

and find in output your PTS Bluetooth USB dongle

.. image:: usb-devices_output.png
   :height: 100
   :width: 500
   :align: center

Note Vendor and ProdID number. Close VMWare Workstation and open .vmx of your virtual machine
(path similar to /home/codecoup/vmware/Windows 10/Windows 10.vmx) in text editor.
Write anywhere in the file following line:

.. code-block::

    usb.autoConnect.device0 = "0x0a12:0x0001"

just replace 0x0a12 with Vendor number and 0x0001 with ProdID number you found earlier.

Connect devices (only required in the actual hardware test mode)
****************************************************************

.. image:: devices_1.png
   :height: 400
   :width: 600
   :align: center

.. image:: devices_2.png
   :height: 700
   :width: 500
   :align: center

Setup auto-pts project
**********************

AutoPTS client on Linux
=======================

Clone auto-pts project:

.. code-block::

    git clone https://github.com/auto-pts/auto-pts.git


Install socat, that is used to transfer BTP data stream from UART's tty file:

.. code-block::

    sudo apt-get install python-setuptools socat

Install required python modules:

.. code-block::

   cd auto-pts
   pip3 install --user -r autoptsclient_requirements.txt

Autopts server on Windows virtual machine
=========================================
In Git Bash, clone auto-pts project repo:

.. code-block::

    git clone https://github.com/auto-pts/auto-pts.git

Install required python modules:

.. code-block::

   cd auto-pts
   pip3 install --user wheel
   pip3 install --user -r autoptsserver_requirements.txt

Restart virtual machine.

Running AutoPTS
***************

Please follow the information from
https://github.com/zephyrproject-rtos/zephyr/tree/main/tests/bluetooth/tester on how to build,
flash and run the Bluetooth Tester application.

Server and client by default will run on localhost address.
Run the server in the Windows virtual machine:

.. code-block::

    python ./autoptsserver.py

.. image:: autoptsserver_run_2.png
   :height: 120
   :width: 700
   :align: center

See also https://github.com/auto-pts/auto-pts for additional information on how to run auto-pts.

Testing Zephyr Host Stack on hardware
=====================================

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master -t /dev/ttyACM0 -b BOARD -i SERVER_IP -l LOCAL_IP

Where ``/dev/ttyACM0`` is the tty for the board,
``BOARD`` is the board to use (e.g. ``nrf53_audio``),
``SERVER_IP`` is the IP of the AutoPTS server,
``LOCAL_IP`` is the local IP of the Linux machine.

Testing Zephyr Host Stack on QEMU
=================================

A Bluetooth controller needs to be mounted.
For running with HCI UART, please visit :zephyr:code-sample:`bluetooth_hci_uart`.

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master BUILD_DIR/zephyr/zephyr.elf -i SERVER_IP -l LOCAL_IP

Where ``BUILD_DIR`` is the build directory,
``SERVER_IP`` is the IP of the AutoPTS server,
``LOCAL_IP`` is the local IP of the Linux machine.

Testing Zephyr Host Stack on :zephyr:board:`native_sim <native_sim>`
====================================================================

When tester application has been built for :zephyr:board:`native_sim <native_sim>` it produces a
``zephyr.exe`` file, that can be run as a native Linux application.
Depending on your system,
you may need to perform the following steps to successfully run ``zephyr.exe``.

Setting capabilities
--------------------

Since the application will need access to connect to a socket for HCI,
you may need to perform the following

.. code-block::

    setcap cap_net_raw,cap_net_admin,cap_sys_admin+ep zephyr.exe

This is not required if you run ``zephyr.exe`` or ``./autoptsclient-zephyr.py`` with e.g. ``sudo``.

Downing the HCI controller
--------------------------

You may also need to "down" or "power off" the HCI controller before running ``zephyr.exe``.
This can be done either with ``hciconfig`` as

.. code-block::

    hciconfig hciX down

Where ``hciX`` is a value like ``hci0``. You may run ``hciconfig`` to get a list of your HCI devices.

Since ``hciconfig`` is deprecated on some systems, you may need to use

.. code-block::

    btmgmt -i hciX power off

Similar to ``hciconfig``, ``btmgmt info`` may be used to list current controllers and their states.

Both ``hciconfig`` and ``btmgmt`` may require ``sudo`` when powering down a controller.

Running the client
------------------

The application can be run as

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master --hci HCI BUILD_DIR/zephyr/zephyr.exe -i SERVER_IP -l LOCAL_IP

Where ``HCI`` is the HCI index, e.g. ``0`` or ``1``,
``BUILD_DIR`` is the build directory,
``SERVER_IP`` is the IP of the AutoPTS server,
``LOCAL_IP`` is the local IP of the Linux machine.

Troubleshooting
****************

After running one test, I need to restart my Windows virtual machine to run another, because of fail verdict from APICOM in PTS logs
====================================================================================================================================

It means your virtual machine has not enough processor cores or memory. Try to add more in
settings. Note that a host with 4 CPUs could be not enough with VirtualBox as hypervisor.
In this case, choose rather VMWare Workstation.

I cannot start autoptsserver-zephyr.py. I always get a Python error
===================================================================

.. image:: autoptsserver_typical_error.png
   :height: 300
   :width: 650
   :align: center

One or more of the following steps should help:

- Close all PTS Windows.

- Replug PTS bluetooth dongle.

- Delete temporary workspace. You will find it in auto-pts-code/workspaces/zephyr/zephyr-master/ as temp_zephyr-master. Be careful, do not remove the original one zephyr-master.pqw6.

- Restart Windows virtual machine.

The PTS automation window keeps opening and closing
===================================================

This indicates that it fails to capture a PTS dongle.
If the AutoPTS server is able to find and use a PTS dongle,
then the title of the window will show the Bluetooth address of the dongle.
If this does not happen then ensure that the dongle is plugged in, updated and recognized by PTS.

.. image:: pts_automation_window.png
   :width: 500
   :align: center

If it still fails to run tests after this,
please ensure that the Bluetooth Protocol Viewer is installed.