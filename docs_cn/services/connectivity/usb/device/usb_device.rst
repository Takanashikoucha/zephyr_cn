.. _usb_device_stack:

USB device support (deprecated)
###############################

.. contents::
    :local:
    :depth: 3

Overview
********

USB device stack 为 USB
device controller driver 与 USB device class drivers 或 customer applications 间的 hardware independent interface。
其为 LPCUSB device stack 的移植（且随时间修改并扩展。其提供以下 functionalities：

* 用 device controller drivers 提供的 :ref:`usb_dc_api` 与
  USB device controller 交互。
* 响应 standard device requests 并返回 standard descriptors（
  本质上处理 'Chapter 9' processing（具体为 universal serial bus specification
  revision 2.0 中 table 9-3 的 standard
  device requests。
* 提供供 USB device classes 或
  customer applications 使用的 programming interface。APIs 描述在
  :zephyr_file:`include/zephyr/usb/usb_device.h`

.. note::
   :ref:`usb_api` 中列出的所有 APIs 及依赖它们的 functions
   已 deprecated（且将在 v4.5.0 移除。请用 :ref:`usb_device_next_api` 中
   APIs 代表的新 USB device
   支持。

Supported USB classes
*********************

Audio
=====

有 Audio class 的 experimental 实现。其遵循 specification
version 1.00（``bcdADC 0x0100``）（且仅支持 synchronous synchronisation type。
参见 :zephyr:code-sample:`usb-audio-headphones-microphone` 和
:zephyr:code-sample:`usb-audio-headset` samples 作 reference。

Bluetooth HCI USB transport layer
=================================

Bluetooth HCI USB transport layer 实现用 :ref:`bt_hci_raw`
向 host 暴露 HCI interface。其与 Bluetooth specification 中的描述
不完全一致（且仅由带 endpoint
configuration 的 interface 组成：

* 通过 control endpoint 的 HCI commands（仅 host-to-device）
* 通过 interrupt IN endpoint 的 HCI events
* 通过一个 bulk IN 和一个 bulk OUT endpoints 的 ACL data

未实现 voice channels 的第二个 interface（因为
:ref:`bluetooth` 中无对此 type 的支持。若 HCI USB transport layer 为
configuration 中出现的唯一 interface（这在 Linux 下不是大问题（
btusb driver 不会尝试 claim 第二个 (isochronous) interface。
后果是（若 HCI USB 用在 composite configuration 中且
为第一个 interface（则 Linux btusb driver 将 claim 第一个和
下一个 interface（阻止其他 composite functions 工作。
由于此问题（HCI USB 不应用在 composite configuration 中。
此问题在新 USB 支持的实现中已修复。

参见 :zephyr:code-sample:`bluetooth_hci_usb` sample 作 reference。

.. _usb_device_cdc_acm:

CDC ACM
=======

CDC ACM class 用作 Zephyr 中不同 subsystems 的 backend。
然而（其 configuration 对经验不足的 user 可能不易。
以下为不同 use cases 的描述及若干 pitfalls。

CDC ACM user 的 interface 为 :ref:`uart_api` driver API。
但与真实 UART controller 相比（行为上有两个重要差异：

* Data transfer 仅在 USB device stack 已
  初始化并启动后可能（在此之前任何 data 被丢弃
* 若 device 连接到 host（仍需 host 侧
  请求 data 的 application
* CDC ACM poll out 实现遵循 API（且
  仅当 hw-flow-control property 启用且
  从 non-ISR context 调用时在 TX
  ring buffer 满时阻塞。

CDC ACM UART 的 devicetree compatible property 为
:dtcompatible:`zephyr,cdc-acm-uart`。
启用 USB device 支持且 devicetree sources 中存在 compatible node 时
自动选择 CDC ACM 支持。必要时（
可用 :kconfig:option:`CONFIG_USB_CDC_ACM` 显式禁用 CDC ACM 支持。
可定义并使用约四个 CDC ACM UART instances（
受限于 controller 支持的最大 endpoints 数量。

CDC ACM UART node 应为 USB device controller node 的 child。
由于 controller nodes 的命名因 vendor 而异（
且我们的 samples 和 application 应尽可能通用（
默认 USB device controller 通常分配 ``zephyr_udc0``
node label。通常（CDC ACM UART 在 devicetree overlay file 中描述
（如下：

.. code-block:: devicetree

	&zephyr_udc0 {
		cdc_acm_uart0: cdc_acm_uart0 {
			compatible = "zephyr,cdc-acm-uart";
			label = "CDC_ACM_0";
		};
	};

Sample :zephyr:code-sample:`usb-cdc-acm` 有类似 overlay files。
且由于无特殊 properties 存在（用
devicetree 描述 CDC ACM UART 似乎过度。使用 devicetree
的动机为 application 中真实 UART controller 与 CDC ACM UART
的易互换性。

Console over CDC ACM UART
-------------------------

用上述 CDC ACM UART node 和
chosen node 的 ``zephyr,console`` property（可描述
CDC ACM UART 要与 console 一起使用。
:zephyr:code-sample:`usb-cdc-acm-console` sample 用类似 overlay file。

.. code-block:: devicetree

	/ {
		chosen {
			zephyr,console = &cdc_acm_uart0;
		};
	};

	&zephyr_udc0 {
		cdc_acm_uart0: cdc_acm_uart0 {
			compatible = "zephyr,cdc-acm-uart";
			label = "CDC_ACM_0";
		};
	};

Application 使用 console 前（建议等待
DTR signal：

.. code-block:: c

	const struct device *const dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_console));
	uint32_t dtr = 0;

	if (usb_enable(NULL)) {
		return;
	}

	while (!dtr) {
		uart_line_ctrl_get(dev, UART_LINE_CTRL_DTR, &dtr);
		k_sleep(K_MSEC(100));
	}

	printk("nuqneH\n");

CDC ACM UART as backend
-----------------------

与 console sample 一样（可通过设置 :ref:`devicetree-chosen-nodes`
properties 将 CDC ACM UART 配置为
其他 subsystems 的 backend。

若干 Zephyr 特定 chosen properties 列表（可用于选择
CDC ACM UART 作为 subsystem 或 application 的 backend：

* ``zephyr,bt-c2h-uart`` 用于 Bluetooth（
  例如参见 :zephyr:code-sample:`bluetooth_hci_uart`
* ``zephyr,ot-uart`` 用于 OpenThread（
  例如参见 :zephyr:code-sample:`openthread-coprocessor`
* ``zephyr,shell-uart`` 由 shell 用于 serial backend（
  例如参见 :zephyr_file:`samples/subsys/shell/shell_module`
* ``zephyr,uart-mcumgr`` 由 :zephyr:code-sample:`smp-svr` sample 使用

POSIX default tty ECHO mitigation
---------------------------------

POSIX systems（如 Linux（默认对 tty devices 启用 ECHO。Host side
application 可通过对 tty device 调用 ``open()``（并发出
``ioctl()``（最好通过 ``tcsetattr()``）禁用不期望的
echo。不幸的是（``open()`` 和 ``ioctl()`` 间有固有 race（
ECHO 已启用（且任何收到的 characters（即使 host application
不调用 ``read()``）将被 echo 回。此问题在
CDC ACM port 使用而另一侧无真实 UART 时特别明显（
因为无 baud rate 导致的任意 delay。

为缓解此问题（Zephyr CDC ACM 实现在 device 配置后
用 ZLP arm IN endpoint。Host 读取 ZLP 时（这是
host application 已打开 tty device 的最佳指示（Zephyr 将
在发送真实
payload 前强制 :kconfig:option:`CONFIG_CDC_ACM_TX_DELAY_MS` millisecond delay。这应允许
足够时间供第一个（且仅第一个）
打开 tty device 的 application 在不需要 ECHO 时禁用 ECHO。
若完全不期望 CDC ACM device 的 ECHO（最好设置 udev rule
在 device 连接时立即禁用 ECHO。

当 CDC ACM instance 用于 Zephyr shell 时（ECHO 特别不期望（
因为发送回 shell 设置颜色的 control characters 被解释
为 (invalid) command（且 user 将看到 garbage 作为结果。虽然 minicom 默认
禁用 ECHO（但带 reset 退出时将 termios settings
恢复为进入时设置的值。因此（若 minicom 为
打开 tty device 的第一个 application（带 reset 退出将重新启用 ECHO（从而为
下一个 application 设置问题（Zephyr 侧无法缓解）。
为防止此问题（建议 minicom 不带 reset 退出（或
在 minicom 启动前禁用 ECHO。

DFU
===

USB DFU class 实现与 :ref:`dfu` 和 :ref:`mcuboot_api` 紧密耦合。
这意味着 target platform 须支持 :ref:`flash_img_api` API。

参见 :zephyr:code-sample:`legacy-usb-dfu` sample 作 reference。

USB Human Interface Devices (HID) support
=========================================

HID 支持滥用 :ref:`device_model_api` 仅允许 applications 使用
:c:func:`device_get_binding`。注意无 HID device API 本身（
相反 interface 由 :c:struct:`hid_ops` 提供。
默认 instance 名为 ``HID_n``（其中 n 可取决于
:kconfig:option:`CONFIG_USB_HID_DEVICE_COUNT` 为 {0, 1, 2, ...}。

每个 HID instance 需 HID report descriptor。与 core 的
interface 和 report descriptor 须用 :c:func:`usb_hid_register_device` 注册。

由于 USB HID specification 不仅用于 USB subsystem（USB HID API
reference 分为两部分（:ref:`usb_hid_common` 和 :ref:`usb_hid_device`。
:ref:`usb_hid_common` 的 HID helper macros 应用于组合
HID report descriptor。Macro 名对应 USB HID specification 中使用的。

对 HID class interface（每个 instance 需 IN interrupt endpoint（
OUT interrupt endpoint 可选。因此（
:c:struct:`hid_ops` 的最小实现要求
为提供 ``int_in_ready`` callback。

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


若 application 想通过 OUT interrupt endpoint 接收 output reports（
须启用 :kconfig:option:`CONFIG_ENABLE_HID_INT_OUT_EP`（并提供
``int_out_ready`` callback。
缺点为
:kconfig:option:`CONFIG_ENABLE_HID_INT_OUT_EP` 或
:kconfig:option:`CONFIG_HID_INTERRUPT_EP_MPS` 等 Kconfig options
适用于所有 instances。此 design
issue 将在新 USB 支持的 HID class 实现中修复。

参见 :zephyr:code-sample:`usb-hid-mouse` sample 作 reference。

Mass Storage Class
==================

MSC 遵循 Bulk-Only Transport specification（且用 :ref:`disk_access_api`
向 host 访问并暴露 RAM disk（flash partition 上的 emulated block device（
或 SD Card。一次仅可导出一个 disk instance。

实现所用的 disc 由
:kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME` 设置（且应
与 application 想向 host 暴露的 disc access driver 使用的
名称相同。Flash、RAM 和 SDMMC/MMC disk drivers 用 node property ``disk-name``
设置 disk 名。

对 flash partition 上的 emulated block device（所用 flash partition 和
flash disk 须在 devicetree 中描述。若 storage partition
已在 board 层描述（application devicetree overlay 还须
先删除 ``storage_partition`` node。:kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME`
应与 ``disk-name`` property 相同。

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

``disk-property`` "NAND" 可能令人困惑（但这仅是某些 file
systems 识别 disc 的方式。因此（若 application 也访问
暴露 disc 上的 file system（应使用默认 names（参见
:zephyr:code-sample:`usb-mass` sample 作 reference。

Networking
==========

有三个以类似方式工作的实现（提供远端 (USB host) 与 Zephyr network 支持间的虚拟
Ethernet connection。

* CDC ECM class（用 :kconfig:option:`CONFIG_USB_DEVICE_NETWORK_ECM` 启用
* CDC EEM class（用 :kconfig:option:`CONFIG_USB_DEVICE_NETWORK_EEM` 启用
* RNDIS 支持（用 :kconfig:option:`CONFIG_USB_DEVICE_NETWORK_RNDIS` 启用

参见 :zephyr:code-sample:`legacy-netusb` sample 作 reference。

使用 RNDIS 支持的 Applications 应为运行 Microsoft Windows OS 的 host
上更好的 user experience 启用 :kconfig:option:`CONFIG_USB_DEVICE_OS_DESC`。

Binary Device Object Store (BOS) support
****************************************

BOS handling 可用 Kconfig option :kconfig:option:`CONFIG_USB_DEVICE_BOS` 启用。
此 option 还有将 device descriptor ``bcdUSB`` 改为 ``0210`` 的效果。
Application 应用 :c:func:`usb_bos_register_cap` 注册如 Capability Descriptor
等 descriptors。注册的 descriptors 被添加到 root
BOS descriptor（并由 stack 处理。

参见 :zephyr:code-sample:`legacy-webusb` sample 作 reference。

Interface number and endpoint address assignment
************************************************

在 USB 术语中（``function`` 为向
host 提供 capability 的 device（如实现 keyboard 的 HID class device。Function
包含 ``interfaces`` 集合；至少需一个 interface。
Interface 可包含 device ``endpoints``；例如（
实现 HID class device 至少需一个 input
endpoint（实现 USB DFU class 无需 endpoints。组合 functions 的 USB device
为 multifunction USB device（例如
HID class device 和
CDC ACM device 的组合。

用 Zephyr RTOS USB 支持（内置 USB
classes/functions 或自定义 user implementations 可实现各种组合。限制为
可用 device endpoints 数量。每个 device endpoint 可唯一寻址。
Endpoint address 为 endpoint direction 和 endpoint
number 的组合（四-bit value。Endpoint number zero 用于
初始化并配置 USB device 的默认 control
method。按 specification（functions 还可使用最多
``15 IN`` 和 ``15 OUT`` device endpoints。
实际数量取决于所用 device controller。并非所有 controllers
支持最大 endpoints 数量和所有 endpoint types。例如（
device controller 可能支持一个 IN 和一个 OUT isochronous endpoint（
但仅用于 endpoint number 8（结果为 endpoint addresses 0x88 和 0x08。
另外（一个 controller 可在同一 endpoint
number 上有 IN/OUT endpoints（interrupt IN endpoint 0x81 和 bulk OUT endpoint 0x01（而另一个
可能仅能处理每个 endpoint number 一个 endpoint。关于
interfaces 数量、interface associations、endpoint types 和 addresses
的信息由 interface、interface specific 和 endpoint
descriptors 提供给 host。

特定 function 的 Host driver 用 interface 和 endpoint descriptor
获取 endpoint addresses、types 和其他 properties。这允许 function
host drivers 通用（例如（由
一个或多个 CDC ACM 和一个或多个 CDC ECM class implementations 组成的
multifunction device 可能（且无需特定 drivers。

Zephyr RTOS 中内置 USB class/function
实现的 interface 和 endpoint descriptors 通常按升序分配
默认 interface numbers 和
endpoint addresses。初始化期间（
默认 interface numbers 可能基于
给定 configuration 中 interfaces 数量重新分配。Endpoint addresses 基于 controller
capabilities 重新分配（因为并非每个
controller 都可能有某些 endpoint 组合（以及
给定 configuration 中 interfaces 数量。这也
意味着 Zephyr RTOS 中的 device 侧 class/function 须在
runtime 检查实际 interface 和 endpoint descriptor 值。
此机制还允许我们提供受限于
controller 提供资源（如
endpoints 数量和 endpoint FIFOs size）的通用 samples 和通用
multifunction samples。

可能有特定 function 的 host drivers（例如在
Linux
Kernel 中（其 function driver 不读取 interface 和 endpoint
descriptors 检查 interface numbers 或 endpoint addresses（而改用
hardcoded values。因此（host driver 不能通用使用（
意味着其不能与不同 device controllers 和
不同 device configurations 组合其他 functions 一起使用。这可能还
因为 driver 为特定 hardware 设计（且
不打算用于此特定 hardware 的 clone。相反（若 driver
本质上通用且应工作于不同 hardware variants（则
不得使用 hardcoded interface numbers 和 endpoint addresses。
Zephyr RTOS 中不可能禁用 endpoint 重新分配（这可能
阻止实现 hardware-clone firmware。相反（若可能（
应修复 host driver 实现以使用 interface
和 endpoint descriptor 中的值。

.. _testing_USB_native_sim:

Testing over USBIP in native_sim
********************************

通过 USBIP 实现的虚拟 USB controller 可用于测试 USB
device stack。遵循通用 build procedure 为
:zephyr:board:`native_sim <native_sim>` configuration 构建 USB sample。

用以下运行构建的 sample：

.. code-block:: console

   west build -t run

在 terminal window 中运行以下 command 列出 USB devices：

.. code-block:: console

   $ usbip list -r localhost
   Exportable USB devices
   ======================
    - 127.0.0.1
           1-1: unknown vendor : unknown product (2fe3:0100)
              : /sys/devices/pci0000:00/0000:00:01.2/usb1/1-1
              : (Defined at Interface level) (00/00/00)
              :  0 - Vendor Specific Class / unknown subclass / unknown protocol (ff/00/00)

在 terminal window 中运行以下 command 附加 USB device：

.. code-block:: console

   $ sudo usbip attach -r localhost -b 1-1

USB device 应连接到 Linux host（且可用
以下 commands 验证：

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

Zephyr project 的 USB Vendor ID 为 ``0x2FE3``。
当 vendor
将 Zephyr USB device 支持集成到其自己的 product 时（不得使用
此 USB Vendor ID。

每个 USB :zephyr:code-sample-category:`sample<usb>` 有其自己的唯一 Product ID。
USB maintainer（若已指派）（否则 Zephyr Technical
Steering Committee（可基于有充分动机且
有记录的 requests 分配其他 USB Product IDs。

当前使用的 Product IDs 如下：

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

USB device descriptor 字段 ``bcdUSB`` (Device Release Number) 代表
Zephyr kernel major 和 minor versions（作为 binary coded decimal value。
