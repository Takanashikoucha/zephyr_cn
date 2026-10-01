.. _usbd_cdc_acm:

USB device CDC ACM
##################

USB device stack 提供的 CDC ACM function 仅实现 Abstract
Control Model Serial Emulation。其唯一目的是模拟 serial lines（如其名所示。大多数现代 operating systems 应开箱即
支持其。

CDC ACM function 在 host 和
device 两侧表示为 serial interface（而 user 或 application interface 为 :ref:`uart_api`
driver API。这允许已使用 UART API 的 applications 使用
CDC ACM function 提供的 serial interface（而无需更改负责
data communication 的 code。仅需额外 configuration 和 USB
device stack 初始化。

CDC ACM UART configuration
==========================

与真实 UART controller 一样（虚拟 CDC ACM UART 在
device tree 中描述。CDC ACM UART 的 devicetree compatible property 为
:dtcompatible:`zephyr,cdc-acm-uart`。

启用 USB device 支持且 devicetree sources 中存在 compatible node 时
自动选择 CDC ACM 支持。必要时（可用 :kconfig:option:`CONFIG_USBD_CDC_ACM_CLASS` 显式禁用 CDC ACM
支持。可能的 CDC ACM instances 数量取决于 USB device controller 支持的
endpoints 数量。每个 CDC ACM instance 需三个
endpoints：两个 bulk endpoints（一个 IN（一个 OUT）（以及 MaxPacketSize 为 16 的一个 interrupt IN。
CDC ACM node 可用 ``label`` property 区分
host 侧不同 interfaces。以下为 devicetree overlay file 示例。

.. code-block:: devicetree

	&zephyr_udc0 {
		cdc_acm_uart0: cdc_acm_uart0 {
			compatible = "zephyr,cdc-acm-uart";
			label = "CDC_ACM_0";
		};
	};

Application 使用 CDC ACM UART 前（可能想等待 DTR
signal。如何实现
此功能参见 :zephyr:code-sample:`usb-cdc-acm`。

.. note::
  要与 host 通信（除 UART configuration 外（application
  须启用 USB device stack（为此参见
  :ref:`usb_device_next_howto_configure`（并仔细阅读下一章。对
  从 legacy stack 迁移的 users 和 applications（这是其
  须适配的唯一部分。

.. _cdc_acm_uart_as_serial_backend:

CDC ACM UART as serial backend
==============================

用上述示例和 ``zephyr,console`` chosen node property（可
将 CDC ACM UART 配置为 console device。

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

与上述示例中 console 配置为使用
CDC ACM UART 相同（``zephyr,shell-uart`` chosen node property 可用于
配置 shell 使用 CDC ACM UART 作为 serial backend。参见 sample
:zephyr:code-sample:`shell-module` 和 :ref:`chosen nodes documentation
<devicetree-chosen-nodes>`。

由于作为 serial backend 的 use case 非常常见（且 CDC ACM UART 在 runtime 无需 configuration（stack 提供执行 :ref:`usb_device_next_howto_configure` 中所述步骤的 helper。
Helper 由 :kconfig:option:`CONFIG_CDC_ACM_SERIAL_INITIALIZE_AT_BOOT`
启用（并用单个 CDC ACM instance 初始化 USB device stack。Sample
:zephyr:code-sample:`usb-cdc-acm-console` 演示如何使用。

像 :zephyr:board:`nrf52840dongle` 这类 board 也应使用
:kconfig:option:`CONFIG_CDC_ACM_SERIAL_INITIALIZE_AT_BOOT`（其无 debug
adapter 但有 USB device controller（且想用 CDC ACM UART 作为 logging 和 shell 的默认
serial backend。
由于任何 board 的 configuration 都相同（有通用
:zephyr_file:`devicetree file <boards/common/usb/cdc_acm_serial.dtsi>` 和
:zephyr_file:`Kconfig file <boards/common/usb/Kconfig.cdc_acm_serial.defconfig>`
须包含在 board 的 devicetree 和 Kconfig.defconfig files 中。

Using CDC ACM UART in the application
=====================================

CDC ACM 实现虚拟 UART controller（并提供 Interrupt-driven UART
API 和 Polling UART API。ASYNC API 尚不支持。若
application 想通过 CDC ACM UART 通信（首选方式为
使用 Interrupt-driven UART API。理解 API documentation 至关重要（
尽管如此（以下若干 notes。

Interrupt-driven UART API
-------------------------

内部（CDC ACM UART 实现用两个 ringbuffers。这些接管
:ref:`uart_interrupt_api` 的 TX/RX FIFOs (TX/RX buffers)
的功能。

如 :ref:`uart_interrupt_api` 中所述（functions
:c:func:`uart_irq_update()`、:c:func:`uart_irq_is_pending`、
:c:func:`uart_irq_rx_ready()`、:c:func:`uart_irq_tx_ready()`、
:c:func:`uart_fifo_read()` 和 :c:func:`uart_fifo_fill()`
应从 interrupt handler 调用（参见
:c:func:`uart_irq_callback_user_data_set()`。为防止 undefined behavior（
这些 functions 的实现检查其在何 context 中被调用（
若非 interrupt handler 则失败。

另外（如 UART API 中所述（:c:func:`uart_irq_is_pending`、
:c:func:`uart_irq_rx_ready()` 和 :c:func:`uart_irq_tx_ready()`
仅可在 :c:func:`uart_irq_update()` 后调用。

简化（application interrupt handler 应类似：

.. code-block:: c

	static void interrupt_handler(const struct device *dev, void *user_data)
	{
		while (true) {
			uart_irq_update(dev);

			if (uart_irq_is_pending(dev) <= 0) {
				break;
			}

			if (uart_irq_rx_ready(dev)) {
				int len;
				int n;

				/* ... */
				n = uart_fifo_read(dev, buffer, len);
				/* ... */
			}

			if (uart_irq_tx_ready(dev)) {
				int len;
				int n;

				/* ... */
				n = uart_fifo_fill(dev, buffer, len);
			  /* ... */
			}
		}
	}

所有这些 functions 不直接依赖 USB device 的 status。
填充 TX FIFO 不意味着 data 正在发送到 host。且
成功读取 RX FIFO 不意味着 device 仍
连接到 host。若 TX FIFO 有空间（且 TX interrupt
已启用（:c:func:`uart_irq_tx_ready()` 将成功。若 RX FIFO 有 data（且 RX interrupt
已启用（:c:func:`uart_irq_rx_ready()` 将
成功。Function :c:func:`uart_irq_tx_complete()` 尚未实现。

Polling UART API
----------------

CDC ACM poll out 实现遵循 :ref:`uart_polling_api`（且
仅当 hw-flow-control property 启用且
从 non-ISR context 调用时在 TX FIFO 满时阻塞。
