.. _autopts-win10:

AutoPTS
on
Windows
10
with
nRF52
board
#######################################

这
个
tutorial
展示
如何
setup
AutoPTS
client
和
server
都
运行
在
Windows
10
上。
我们
用
WSL1
带
Ubuntu
只
为
了
build
Zephyr
project
到
elf
file
因为
Zephyr
SDK
还
不
可用
于
Windows。
Tutorial
只
cover
nrf52840dk。

.. contents::
    :local:
    :depth:
    2

Update
Windows
and
drivers
===========================

在
以下
位置
Update
Windows：

Start
->
Settings
->
Update
&
Security
->
Windows
Update

Update
drivers
遵循
你
的
hardware
vendor
的
instructions。

Install
Python
3
================

Download
并
install
`Python
3
<https://www.python.org/downloads/>`_。
Setup
在
versions
>=3.8
上
tested。
让
installer
将
Python
installation
directory
添加
到
PATH
并
disable
path
length
limitation。

.. image::
   install_python1.png
   :height:
   300
   :width:
   450
   :align:
   center

.. image::
   install_python2.png
   :height:
   300
   :width:
   450
   :align:
   center


.. note::

   以下为原文（待翻译）

.. code-block::

    git clone https://github.com/auto-pts/auto-pts.git

Go into the project folder:

.. code-block::

    cd auto-pts

Install required python modules:

.. code-block::

   pip3 install --user wheel
   pip3 install --user -r autoptsserver_requirements.txt
   pip3 install --user -r autoptsclient_requirements.txt

Install socat.exe
==================

Download and extract socat.exe from https://sourceforge.net/projects/unix-utils/files/socat/1.7.3.2/
into folder ~/socat-1.7.3.2-1-x86_64/.

.. image:: download_socat.png
   :height: 400
   :width: 450
   :align: center

Add path to directory of socat.exe to PATH:

.. image:: add_socat_to_path.png
   :height: 400
   :width: 450
   :align: center

Running AutoPTS
================

Server and client by default will run on localhost address. Run server:

.. code-block::

    python ./autoptsserver.py -S 65000

.. image:: autoptsserver_run.png
   :height: 200
   :width: 800
   :align: center

.. note::

    If the error "ImportError: No module named pywintypes" appeared after the fresh setup,
    uninstall and install the pywin32 module:

    .. code-block::

        pip install --upgrade --force-reinstall pywin32

Run client:

.. code-block::

    python ./autoptsclient-zephyr.py zephyr-master ~/zephyrproject/build/zephyr/zephyr.elf -t COM3 -b nrf52 -S 65000 -C 65001

.. image:: autoptsclient_run.png
   :height: 200
   :width: 800
   :align: center

At the first run, when Windows asks, enable connection through firewall:

.. image:: allow_firewall.png
   :height: 450
   :width: 600
   :align: center

Troubleshooting
================

- "When running actual hardware test mode, I have only BTP TIMEOUTs."

This is a problem with connection between auto-pts client and board. There are many possible causes. Try:

- Clean your auto-pts and zephyr repos with

.. warning::

    This command will force the irreversible removal of all uncommitted files in the repo.

.. code-block::

    git clean -fdx

then build and flash tester elf again.

- If you have set up Windows on virtual machine, check if guest extensions are installed properly or change USB compatibility mode in VM settings to USB 2.0.

- Check, if firewall in not blocking python.exe or socat.exe.

- Check if board sends ready event after restart (hex 00 00 80 ff 00 00). Open serial connection to board with e.g. PuTTy with proper COM and baud rate. After board reset you should see some strings in console.

- Check if socat.exe creates tunnel to board. Run in console

.. code-block::

    socat.exe -x -v tcp-listen:65123 /dev/ttyS2,raw,b115200

where /dev/ttyS2 is the COM3 equivalent. Open PuTTY, set connection type to Raw, IP to 127.0.0.1, port to 65123. After board reset you should see some strings in console.
