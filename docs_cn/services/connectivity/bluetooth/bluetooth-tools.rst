.. _bluetooth-tools:

Tools
#####

这
页
list
并
describe
可以
用
来
assist
Bluetooth
stack
或
application
development
期间
的
tools
以
帮助、
simplify
和
speed
up
development
process。

.. contents::
    :local:
    :depth:
    2

.. _bluetooth-mobile-apps:

Mobile
applications
*******************

利用
现有
的
mobile
applications
与
运行
Zephyr
的
hardware
交互
通常
是
有用
的
以
测试
functionality
而
不
需要
写
任何
额外
的
code
或
需要
extra
的
hardware。

推荐
的
与
Zephyr
交互
的
mobile
applications：

*
Android：

   *
   `nRF
   Connect
   for
   Android`_
   *
   `nRF
   Mesh
   for
   Android`_
   *
   `LightBlue
   for
   Android`_

*
iOS：

   *
   `nRF
   Connect
   for
   iOS`_
   *
   `nRF
   Mesh
   for
   iOS`_
   *
   `LightBlue
   for
   iOS`_

.. _bluetooth_bluez:

Using
BlueZ
with
Zephyr
***********************


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
* Choose one of the Bluetooth sample applications located in
  :literal:`samples/bluetooth`.

* To run a Bluetooth application in QEMU, type:

  .. zephyr-app-commands::
     :zephyr-app: samples/bluetooth/<sample>
     :host-os: unix
     :board: qemu_x86
     :goals: run
     :compact:

  Running QEMU now results in a connection with the second serial line to
  the :literal:`bt-server-bredr` UNIX socket, letting the application
  access the Bluetooth controller.

* To run a Bluetooth application in :zephyr:board:`native_sim <native_sim>`, first build it:

  .. zephyr-app-commands::
     :zephyr-app: samples/bluetooth/<sample>
     :host-os: unix
     :board: native_sim
     :goals: build
     :compact:

  And then run it with::

     $ sudo ./build/zephyr/zephyr.exe --bt-dev=hci0

Using a Zephyr-based Bluetooth Controller
=========================================

Depending on which hardware you have available, you can choose between two
transports when building a single-mode, Zephyr-based Bluetooth Controller:

* UART: Use the :zephyr:code-sample:`bluetooth_hci_uart` sample and follow
  the instructions in :ref:`bluetooth-hci-uart-qemu-posix`.
* USB: Use the :zephyr:code-sample:`bluetooth_hci_usb` sample and then
  treat it as a Host System Bluetooth Controller (see previous section)

.. _bluetooth-hci-tracing:

HCI Tracing
===========

When running the Host on a computer connected to an external Controller, it
is very useful to be able to see the full log of exchanges between the two,
in the format of a :ref:`bluetooth-hci` log.
In order to see those logs, you can use the built-in ``btmon`` tool from BlueZ:

.. code-block:: console

   $ btmon

The output looks like this::

   = New Index: 00:00:00:00:00:00 (Primary,Virtual,Control)                     0.274200
   = Open Index: 00:00:00:00:00:00                                              0.274500
   < HCI Command: Reset (0x03|0x0003) plen 0                                 #1 0.274600
   > HCI Event: Command Complete (0x0e) plen 4                               #2 0.274700
         Reset (0x03|0x0003) ncmd 1
         Status: Success (0x00)
   < HCI Command: Read Local Supported Features (0x04|0x0003) plen 0         #3 0.274800
   > HCI Event: Command Complete (0x0e) plen 12                              #4 0.274900
         Read Local Supported Features (0x04|0x0003) ncmd 1
         Status: Success (0x00)
         Features: 0x00 0x00 0x00 0x00 0x60 0x00 0x00 0x00
            BR/EDR Not Supported
            LE Supported (Controller)

.. _bluetooth-embedded-hci-tracing:

Embedded HCI tracing
--------------------

When running both Host and Controller in actual Integrated Circuits, you will
only see normal log messages on the console by default, without any way of
accessing the HCI traffic between the Host and the Controller.  However, there
is a special Bluetooth logging mode that converts the console to use a binary
protocol that interleaves both normal log messages as well as the HCI traffic.

Set the following Kconfig options to enable this protocol before building your
application:

.. code-block:: cfg

   CONFIG_BT_DEBUG_MONITOR_UART=y
   CONFIG_UART_CONSOLE=n

- Setting :kconfig:option:`CONFIG_BT_DEBUG_MONITOR_UART` activates the formatting
- Clearing :kconfig:option:`CONFIG_UART_CONSOLE` makes the UART unavailable for
  the system console. E.g. for ``printk`` and the :kconfig:option:`boot banner
  <CONFIG_BOOT_BANNER>`

Optionally, on boards whose monitor UART driver supports the interrupt API,
setting :kconfig:option:`CONFIG_BT_DEBUG_MONITOR_UART_INTERRUPT_DRIVEN` queues
complete monitor records and transmits them from the UART interrupt handler
instead of blocking while each byte is transmitted. Records that do not fit in
the buffer are dropped and reported in the next monitor record. The buffer
size can be adjusted with
:kconfig:option:`CONFIG_BT_DEBUG_MONITOR_UART_BUFFER_SIZE`.

To decode the binary protocol that will now be sent to the console UART you need
to use the btmon tool from :ref:`BlueZ <bluetooth_bluez>`:

.. code-block:: console

   $ btmon --tty <console TTY> --tty-speed 115200

If UART is not available (or you still want non-binary logs), you can set
:kconfig:option:`CONFIG_BT_DEBUG_MONITOR_RTT` instead, which will use Segger
RTT. For example, if trying to connect to a nRF52840DK with S/N 683578642:

.. code-block:: console

   $ btmon --jlink nRF52840_xxAA,683578642

.. _bluetooth_virtual_posix:

Running on a Virtual Controller and native_sim
**********************************************

An alternative to a Bluetooth physical controller is the use of a virtual
controller. This controller can be connected over an HCI TCP server.
This TCP server must support the HCI H4 protocol. In comparison to the physical controller
variant, the virtual controller allows to test a Zephyr application running on the native
boards without a physical Bluetooth controller.

The main use case for a virtual controller is to do Bluetooth connectivity tests without
the need of Bluetooth hardware. This allows to automate Bluetooth integration tests with
external applications such as a Bluetooth gateway or a mobile application.

To demonstrate this functionality an example is given to interact with a virtual controller.
For this purpose, the experimental python module `Bumble`_ from Google is used as it allows to create
a TCP Bluetooth virtual controller and connect with the Zephyr Bluetooth host. To install
bumble follow the `Bumble Getting Started Guide`_.

.. note::
   If your Zephyr application requires the use of the HCI LE Set extended commands, install
   the branch ``controller-extended-advertising`` from Bumble.

Android Emulator
=================

You can test the virtual controller by connecting a Bluetooth Zephyr application
to the `Android Emulator`_.

To connect your application to the Android Emulator follow the next steps:

    #. Build your Zephyr application and disable the HCI ACL flow
       control (i.e. ``CONFIG_BT_HCI_ACL_FLOW_CONTROL=n``) as the
       virtual controller from android does not support it at the moment.

    #. Install Android Emulator version >= 33.1.4.0. The easiest way to do this is by installing
       the latest `Android Studio Preview`_ version.

    #. Create a new Android Virtual Device (AVD) with the `Android Device Manager`_. The AVD should use at least SDK API 34.

    #. Run the Android Emulator via terminal as follows:

       ``emulator avd YOUR_AVD -packet-streamer-endpoint default``

    #. Create a Bluetooth bridge between the Zephyr application and
       the virtual controller from Android Emulator with the `Bumble`_ utility ``hci-bridge``.

       ``bumble-hci-bridge tcp-server:_:1234 android-netsim``

       This command will create a TCP server bridge on the local host IP address ``127.0.0.1``
       and port number ``1234``.

    #. Run the Zephyr application and connect to the TCP server created in the last step.

       ``./zephyr.exe --bt-dev=127.0.0.1:1234``

After following these steps the Zephyr application will be available to the Android Emulator
over the virtual Bluetooth controller that was bridged with Bumble. You can verify that the
Zephyr application can communicate over Bluetooth by opening the Bluetooth settings in your
AVD and scanning for your Zephyr application device. To test this you can build the Bluetooth
peripheral samples such as :zephyr:code-sample:`ble_peripheral_hr` or
:zephyr:code-sample:`ble_peripheral_dis`.

.. _bluetooth_ctlr_bluez:

Using Zephyr-based Controllers with BlueZ
*****************************************

If you want to test a Zephyr-powered Bluetooth Controller using BlueZ's Bluetooth
Host, you will need a few tools described in the :ref:`bluetooth_bluez` section.
Once you have installed the tools you can then use them to interact with your
Zephyr-based controller:

   .. code-block:: console

      sudo tools/btmgmt --index 0
      [hci0]# auto-power
      [hci0]# find -l

You might need to replace :literal:`--index 0` with the index of the Controller
you wish to manage.
Additional information about :file:`btmgmt` can be found in its manual pages.


.. _nRF Connect for Android: https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=en
.. _nRF Connect for iOS: https://itunes.apple.com/us/app/nrf-connect/id1054362403
.. _LightBlue for Android: https://play.google.com/store/apps/details?id=com.punchthrough.lightblueexplorer&hl=en_US
.. _LightBlue for iOS: https://itunes.apple.com/us/app/lightblue-explorer/id557428110
.. _nRF Mesh for Android: https://play.google.com/store/apps/details?id=no.nordicsemi.android.nrfmeshprovisioner&hl=en
.. _nRF Mesh for iOS: https://itunes.apple.com/us/app/nrf-mesh/id1380726771
.. _Bumble: https://github.com/google/bumble
.. _Bumble Getting Started Guide: https://google.github.io/bumble/getting_started.html
.. _Android Emulator: https://developer.android.com/studio/run/emulator
.. _Android Device Manager: https://developer.android.com/studio/run/managing-avds
.. _Android Studio Preview: https://developer.android.com/studio/preview