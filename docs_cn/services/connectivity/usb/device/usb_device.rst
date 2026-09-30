.. _usb_device_stack:

USB
device
support
（deprecated）
###############################

.. contents::
    :local:
    :depth:
    3

Overview
********

USB
device
stack
是
一
个
hardware
independent
的
interface
在
USB
device
controller
driver
和
USB
device
class
drivers
或
customer
applications
之间。
它
是
LPCUSB
device
stack
的
port
并
随
time
被
modified
和
expanded。
它
provide
以下
functionalities：

*
Use
由
device
controller
drivers
provided
的
:ref:`usb_dc_api`
与
USB
device
controller
interact。
*
Respond
到
standard
的
device
requests
并
return
standard
的
descriptors
essentially
handling
'Chapter
9'
processing
specific
地
universal
serial
bus
specification
revision
2.0
中
table
9-3
的
standard
device
requests。
*
Provide
一
个
programming
interface
用于
USB
device
classes
或
customer
applications
use。
APIs
在
:zephyr_file:`include/zephyr/usb/usb_device.h`
中
described

.. note::
   所有
   在
   :ref:`usb_api`
   中
   listed
   的
   APIs
   和
   依赖
   它们
   的
   functions
   被
   deprecated
   并
   将
   在
   v4.5.0
   中
   被
   remove。
   请
   use
   新
   的
   USB
   device
   support
   它
   由
   :ref:`usb_device_next_api`
   中
   的
   APIs
   represented。

Supported
USB
classes
*********************

Audio
=====

有
一
个
experimental
的
Audio
class
implementation。
它
follow
specification
version
1.00
（``bcdADC
0x0100``）
并
只
support
synchronous
synchronisation
type。


.. note::

   以下为原文（待翻译）

the best indication that host application has opened the tty device, Zephyr will
force :kconfig:option:`CONFIG_CDC_ACM_TX_DELAY_MS` millisecond delay before real
payload is sent. This should allow sufficient time for first, and only first,
application that opens the tty device to disable ECHO if ECHO is not desired.
If ECHO is not desired at all from CDC ACM device it is best to set up udev rule
to disable ECHO as soon as device is connected.

ECHO is particurarly unwanted when CDC ACM instance is used for Zephyr shell,
because the control characters to set color sent back to shell are interpreted
as (invalid) command and user will see garbage as a result. While minicom does
disable ECHO by default, on exit with reset it will restore the termios settings
to whatever was set on entry. Therefore, if minicom is the first application to
open the tty device, the exit with reset will enable ECHO back and thus set up
a problem for the next application (which cannot be mitigated at Zephyr side).
To prevent the issue it is recommended either to leave minicom without reset or
to disable ECHO before minicom is started.

DFU
===

USB DFU class implementation is tightly coupled to :ref:`dfu` and :ref:`mcuboot_api`.
This means that the target platform must support the :ref:`flash_img_api` API.

See :zephyr:code-sample:`legacy-usb-dfu` sample for reference.

USB Human Interface Devices (HID) support
=========================================

HID support abuses :ref:`device_model_api` simply to allow applications to use
the :c:func:`device_get_binding`. Note that there is no HID device API as such,
instead the interface is provided by :c:struct:`hid_ops`.
The default instance name is ``HID_n``, where n can be {0, 1, 2, ...} depending on
the :kconfig:option:`CONFIG_USB_HID_DEVICE_COUNT`.

Each HID instance requires a HID report descriptor. The interface to the core
and the report descriptor must be registered using :c:func:`usb_hid_register_device`.

As the USB HID specification is not only used by the USB subsystem, the USB HID API
reference is split into two parts, :ref:`usb_hid_common` and :ref:`usb_hid_device`.
HID helper macros from :ref:`usb_hid_common` should be used to compose a
HID report descriptor. Macro names correspond to those used in the USB HID specification.

For the HID class interface, an IN interrupt endpoint is required for each instance,
an OUT interrupt endpoint is optional. Thus, the minimum implementation requirement
for :c:struct:`hid_ops` is to provide ``int_in_ready`` callback.

.. code-block:: c

	#define REPORT_ID		1
	static bool configured;
	static const struct device *hdev;

	static void int_in_ready_cb(const struct device *dev)
	{
		static uint8_t report[2] = {REPORT_ID, 0};

		if (hid_int_ep_write(hdev, report, sizeof(report), NULL)) {
			LOG_ERR("Failed to submit report");
		} else {
			report[1]++;
		}
	}

	static void status_cb(enum usb_dc_status_code status, const uint8_t *param)
	{
		if (status == USB_DC_RESET) {
			configured = false;
		}

		if (status == USB_DC_CONFIGURED && !configured) {
			int_in_ready_cb(hdev);
			configured = true;
		}
	}

	static const uint8_t hid_report_desc[] = {
		HID_USAGE_PAGE(HID_USAGE_GEN_DESKTOP),
		HID_USAGE(HID_USAGE_GEN_DESKTOP_UNDEFINED),
		HID_COLLECTION(HID_COLLECTION_APPLICATION),
		HID_LOGICAL_MIN8(0x00),
		HID_LOGICAL_MAX16(0xFF, 0x00),
		HID_REPORT_ID(REPORT_ID),
		HID_REPORT_SIZE(8),
		HID_REPORT_COUNT(1),
		HID_USAGE(HID_USAGE_GEN_DESKTOP_UNDEFINED),
		HID_INPUT(0x02),
		HID_END_COLLECTION,
	};

	static const struct hid_ops my_ops = {
		.int_in_ready = int_in_ready_cb,
	};

	int main(void)
	{
		int ret;

		hdev = device_get_binding("HID_0");
		if (hdev == NULL) {
			return -ENODEV;
		}

		usb_hid_register_device(hdev, hid_report_desc, sizeof(hid_report_desc),
					&my_ops);

		ret = usb_hid_init(hdev);
		if (ret) {
			return ret;
		}

		return usb_enable(status_cb);
	}


If the application wishes to receive output reports via the OUT interrupt endpoint,
it must enable :kconfig:option:`CONFIG_ENABLE_HID_INT_OUT_EP` and provide
``int_out_ready`` callback.
The disadvantage of this is that Kconfig options such as
:kconfig:option:`CONFIG_ENABLE_HID_INT_OUT_EP` or
:kconfig:option:`CONFIG_HID_INTERRUPT_EP_MPS` apply to all instances. This design
issue will be fixed in the HID class implementation for the new USB support.

See :zephyr:code-sample:`usb-hid-mouse` sample for reference.

Mass Storage Class
==================

MSC follows Bulk-Only Transport specification and uses :ref:`disk_access_api` to
access and expose a RAM disk, emulated block device on a flash partition,
or SD Card to the host. Only one disk instance can be exported at a time.

The disc to be used by the implementation is set by the
:kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME` and should be the same as the
name used by the disc access driver that the application wants to expose to the
host. Flash, RAM, and SDMMC/MMC disk drivers use node property ``disk-name`` to
set the disk name.

For the emulated block device on a flash partition, the flash partition and
flash disk to be used must be described in the devicetree. If a storage partition
is already described at the board level, application devicetree overlay must also
delete ``storage_partition`` node first. :kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME`
should be the same as ``disk-name`` property.

.. code-block:: devicetree

	/delete-node/ &storage_partition;

	&mx25r64 {
		partitions {
			compatible = "fixed-partitions";
			#address-cells = <1>;
			#size-cells = <1>;

			storage_partition: partition@0 {
				label = "storage";
				reg = <0x00000000 0x00020000>;
			};
		};
	};

	/ {
		msc_disk0 {
			compatible = "zephyr,flash-disk";
			partition = <&storage_partition>;
			disk-name = "NAND";
			cache-size = <4096>;
		};
	};

The ``disk-property`` "NAND" may be confusing, but it is simply how some file
systems identifies the disc. Therefore, if the application also accesses the
file system on the exposed disc, default names should be used, see
:zephyr:code-sample:`usb-mass` sample for reference.

Networking
==========

There are three implementations that work in a similar way, providing a virtual
Ethernet connection between the remote (USB host) and Zephyr network support.

* CDC ECM class, enabled with :kconfig:option:`CONFIG_USB_DEVICE_NETWORK_ECM`
* CDC EEM class, enabled with :kconfig:option:`CONFIG_USB_DEVICE_NETWORK_EEM`
* RNDIS support, enabled with :kconfig:option:`CONFIG_USB_DEVICE_NETWORK_RNDIS`

See :zephyr:code-sample:`legacy-netusb` sample for reference.

Applications using RNDIS support should enable :kconfig:option:`CONFIG_USB_DEVICE_OS_DESC`
for a better user experience on a host running Microsoft Windows OS.

Binary Device Object Store (BOS) support
****************************************

BOS handling can be enabled with Kconfig option :kconfig:option:`CONFIG_USB_DEVICE_BOS`.
This option also has the effect of changing device descriptor ``bcdUSB`` to ``0210``.
The application should register descriptors such as Capability Descriptor
using :c:func:`usb_bos_register_cap`. Registered descriptors are added to the root
BOS descriptor and handled by the stack.

See :zephyr:code-sample:`legacy-webusb` sample for reference.

Interface number and endpoint address assignment
************************************************

In USB terminology, a ``function`` is a device that provides a capability to the
host, such as a HID class device that implements a keyboard. A function
contains a collection of ``interfaces``; at least one interface is required. An
interface may contain device ``endpoints``; for example, at least one input
endpoint is required to implement a HID class device, and no endpoints are
required to implement a USB DFU class. A USB device that combines functions is
a multifunction USB device, for example, a combination of a HID class device
and a CDC ACM device.

With Zephyr RTOS USB support, various combinations are possible with built-in USB
classes/functions or custom user implementations. The limitation is the number
of available device endpoints. Each device endpoint is uniquely addressable.
The endpoint address is a combination of endpoint direction and endpoint
number, a four-bit value. Endpoint number zero is used for the default control
method to initialize and configure a USB device. By specification, a maximum of
``15 IN`` and ``15 OUT`` device endpoints are also available for use in functions.
The actual number depends on the device controller used. Not all controllers
support the maximum number of endpoints and all endpoint types. For example, a
device controller might support one IN and one OUT isochronous endpoint, but
only for endpoint number 8, resulting in endpoint addresses 0x88 and 0x08.
Also, one controller may be able to have IN/OUT endpoints on the same endpoint
number, interrupt IN endpoint 0x81 and bulk OUT endpoint 0x01, while the other
may only be able to handle one endpoint per endpoint number. Information about
the number of interfaces, interface associations, endpoint types, and addresses
is provided to the host by the interface, interface specific, and endpoint
descriptors.

Host driver for specific function, uses interface and endpoint descriptor to
obtain endpoint addresses, types, and other properties. This allows function
host drivers to be generic, for example, a multi-function device consisting of
one or more CDC ACM and one or more CDC ECM class implementations is possible
and no specific drivers are required.

Interface and endpoint descriptors of built-in USB class/function
implementations in Zephyr RTOS typically have default interface numbers and
endpoint addresses assigned in ascending order. During initialization,
default interface numbers may be reassigned based on the number of interfaces in
a given configuration. Endpoint addresses are reassigned based on controller
capabilities, since certain endpoint combinations are not possible with every
controller, and the number of interfaces in a given configuration. This also
means that the device side class/function in the Zephyr RTOS must check the
actual interface and endpoint descriptor values at runtime.
This mechanism also allows as to provide generic samples and generic
multifunction samples that are limited only by the resources provided by the
controller, such as the number of endpoints and the size of the endpoint FIFOs.

There may be host drivers for a specific function, for example in the Linux
Kernel, where the function driver does not read interface and endpoint
descriptors to check interface numbers or endpoint addresses, but instead uses
hardcoded values. Therefore, the host driver cannot be used in a generic way,
meaning it cannot be used with different device controllers and different
device configurations in combination with other functions. This may also be
because the driver is designed for a specific hardware and is not intended to
be used with a clone of this specific hardware. On the contrary, if the driver
is generic in nature and should work with different hardware variants, then it
must not use hardcoded interface numbers and endpoint addresses.
It is not possible to disable endpoint reassignment in Zephyr RTOS, which may
prevent you from implementing a hardware-clone firmware. Instead, if possible,
the host driver implementation should be fixed to use values from the interface
and endpoint descriptor.

.. _testing_USB_native_sim:

Testing over USBIP in native_sim
********************************

A virtual USB controller implemented through USBIP might be used to test the USB
device stack. Follow the general build procedure to build the USB sample for
the :zephyr:board:`native_sim <native_sim>` configuration.

Run built sample with:

.. code-block:: console

   west build -t run

In a terminal window, run the following command to list USB devices:

.. code-block:: console

   $ usbip list -r localhost
   Exportable USB devices
   ======================
    - 127.0.0.1
           1-1: unknown vendor : unknown product (2fe3:0100)
              : /sys/devices/pci0000:00/0000:00:01.2/usb1/1-1
              : (Defined at Interface level) (00/00/00)
              :  0 - Vendor Specific Class / unknown subclass / unknown protocol (ff/00/00)

In a terminal window, run the following command to attach the USB device:

.. code-block:: console

   $ sudo usbip attach -r localhost -b 1-1

The USB device should be connected to your Linux host, and verified with the
following commands:

.. code-block:: console

   $ sudo usbip port
   Imported USB devices
   ====================
   Port 00: <Port in Use> at Full Speed(12Mbps)
          unknown vendor : unknown product (2fe3:0100)
          7-1 -> usbip://localhost:3240/1-1
              -> remote bus/dev 001/002
   $ lsusb -d 2fe3:0100
   Bus 007 Device 004: ID 2fe3:0100

USB Vendor and Product identifiers
**********************************

The USB Vendor ID for the Zephyr project is ``0x2FE3``.
This USB Vendor ID must not be used when a vendor
integrates Zephyr USB device support into its own product.

Each USB :zephyr:code-sample-category:`sample<usb>` has its own unique Product ID.
The USB maintainer, if one is assigned, or otherwise the Zephyr Technical
Steering Committee, may allocate other USB Product IDs based on well-motivated
and documented requests.

The following Product IDs are currently used:

+----------------------------------------------------+--------+
| Sample                                             | PID    |
+====================================================+========+
| :zephyr:code-sample:`usb-cdc-acm`                  | 0x0001 |
+----------------------------------------------------+--------+
| Reserved (previously: usb-cdc-acm-composite)       | 0x0002 |
+----------------------------------------------------+--------+
| Reserved (previously: usb-hid-cdc)                 | 0x0003 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`usb-cdc-acm-console`          | 0x0004 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`usb-dfu` (Run-Time)           | 0x0005 |
+----------------------------------------------------+--------+
| Reserved (previously: usb-hid)                     | 0x0006 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`usb-hid-mouse`                | 0x0007 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`usb-mass`                     | 0x0008 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`testusb-app`                  | 0x0009 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`webusb`                       | 0x000A |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`bluetooth_hci_usb`            | 0x000B |
+----------------------------------------------------+--------+
| Reserved (previously: bluetooth_hci_usb_h4)        | 0x000C |
+----------------------------------------------------+--------+
| Reserved (previously: wpan-usb)                    | 0x000D |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`uac2-explicit-feedback`       | 0x000E |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`uac2-implicit-feedback`       | 0x000F |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`uvc`                          | 0x0011 |
+----------------------------------------------------+--------+
| :zephyr:code-sample:`usb-dfu` (DFU Mode)           | 0xFFFF |
+----------------------------------------------------+--------+

The USB device descriptor field ``bcdDevice`` (Device Release Number) represents
the Zephyr kernel major and minor versions as a binary coded decimal value.
