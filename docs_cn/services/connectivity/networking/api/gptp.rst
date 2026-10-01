.. _gptp_interface:

generic Precision Time Protocol (gPTP)
######################################

.. contents::
    :local:
    :depth: 2

Overview
********

此 gPTP stack 支持按 `IEEE 802.1AS-2011 standard`_（Bridged Local Area Networks 中 Time-Sensitive Applications 的 Timing and Synchronization）定义的 protocol 和 procedures。

Supported features
*******************

Stack 处理 `IEEE 802.15.4-2011 standard`_ 中定义的 communications 和 state machines。Standard 的 Annex A 中定义的 full-duplex point-to-point link endpoint 的 mandatory requirements 被支持。

Stack 原则上能处理多个 network interfaces（standard 中也定义为 "ports"）上的 communications（从而充当 802.1AS bridge。然而（此 operation mode 未在 Zephyr OS 上验证。

Stack 还可作为按 IEEE 802.1AS automotive profile（不交换 Announce messages 的 networks）上静态配置的 time receiver 运行。参见下文 `Static timeReceiver operation`_。

Supported hardware
******************

虽然 stack 本身为 hardware independent（但须在 ethernet drivers 中启用 Ethernet frame timestamping 支持。

Supported boards：

- :zephyr:board:`frdm_k64f`
- :zephyr:board:`nucleo_h743zi`
- :zephyr:board:`nucleo_h745zi_q`
- :zephyr:board:`nucleo_f767zi`
- :zephyr:board:`sam_e70_xplained`
- :zephyr:board:`native_sim`（仅可用于简单测试（因缺乏 hardware clock 能力有限）
- :zephyr:board:`qemu_x86`（emulated（因缺乏 hardware clock 能力有限）

Enabling the stack
******************

以下 configuration option 须在 :file:`prj.conf` 文件中启用。

- :kconfig:option:`CONFIG_NET_GPTP`

Static timeReceiver operation
*****************************

按 IEEE 802.1AS automotive profile（AVnu "Automotive Ethernet AVB Functional and Interoperability Specification"）构建的 networks 使用静态 port roles 而非 Best Master Clock Algorithm。此类 network 上的 bridge 传输 Sync 和 Follow_Up messages（但不传输 Announce messages（且无需在其 timeTransmitter ports 上响应 Pdelay requests。Default stack 无法与此类 bridge 同步：无收到的 Announce（port 永不达到 time receiver（"slave"）role。

启用 :kconfig:option:`CONFIG_NET_GPTP_STATIC_TIME_RECEIVER` 将 node 配置为静态配置的 time receiver：BMCA 和所有 Announce 处理被绕过（每个 port 被固定到 time receiver role（asCapable 被强制（使 synchronization 不依赖 Pdelay measurement（且 local clock 仅从收到的 Sync 和 Follow_Up messages 校准。Node 永不成为 grandmaster（且从不传输 Sync 或 Announce messages（即使设置了 :kconfig:option:`CONFIG_NET_GPTP_GM_CAPABLE`。这镜像 linuxptp ptp4l 的 automotive time receiver configuration（BMCA "noop"、clientOnly、inhibit_announce、asCapable "true"、ignore_source_id。以这种方式禁用 BMCA 的 standards analog 为 IEEE 802.1AS-2020 的 external port configuration（clause 10.3.14（源自 IEEE 1588-2019 clause 17.6.2）。

Application interfaces
**********************

以下 Application Interfaces 按 standard 的 section 9 定义可用：

- ``ClockSourceTime`` interface（:c:func:`gptp_clk_src_time_invoke`）
- ``ClockTargetPhaseDiscontinuity`` interface（:c:func:`gptp_register_phase_dis_cb`）
- ``ClockTargetEventCapture`` interface（:c:func:`gptp_event_capture`）

Testing
*******

Stack 已用 `OpenAVnu gPTP <https://github.com/AVnu/gptp>`_ 和 `Linux ptp4l <https://linuxptp.sourceforge.net/>`_ daemons 非正式测试。Zephyr source distribution 中的 :zephyr:code-sample:`gPTP sample application <gptp>` 可用于测试。

.. _IEEE 802.1AS-2011 standard:
   https://standards.ieee.org/findstds/standard/802.1AS-2011.html

API Reference
*************

.. doxygengroup:: gptp
