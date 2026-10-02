.. _bluetooth-features:

支持的特性
##################

.. contents::
    :local:
    :depth: 2

自诞生以来，Zephyr 一直高度重视蓝牙，尤其是蓝牙低功耗（Bluetooth Low Energy，LE）。得益于参与蓝牙规范现有开源实现（Linux 的 BlueZ）以及蓝牙 LE 射频硬件设计与开发的多家公司和个人的贡献，Zephyr 中的协议栈已发展得成熟且功能丰富，如下节所示。

* 符合 Bluetooth v5.3

  * 高度可配置

      * 特性、缓冲区大小/数量、协议栈大小等。

  * 可移植到 Zephyr 支持的所有架构（包括大端和小端、各种对齐方式等）

  * 支持 :ref:`Host 与 Controller 构建的所有组合 <bluetooth-hw-setup>`：

    * 仅 Controller（HCI），基于 UART、SPI、USB 和 IPC 物理传输
    * 仅 Host，基于 UART、SPI 和 IPC（共享内存）
    * 组合（Host + Controller）

* :ref:`可通过 Bluetooth-SIG 认证 <bluetooth-qual>`

  * 定期在所有层次（除 BT Classic 外的 Controller 和 Host）的 Nordic Semiconductor 硬件上运行一致性测试。

* :ref:`蓝牙低功耗 Controller <bluetooth-ctlr-arch>`（LE 链路层）

  * 角色与连接数量无限制，支持所有角色
  * 支持 v5.3 规范的全部特性（少数小项除外）
  * 已就绪支持并发多协议
  * 智能调度角色以最小化重叠
  * 可移植设计，适用于任何开放蓝牙 LE 射频，目前支持 Nordic Semiconductor nRF52x 和 nRF53x SoC 系列，以及专有射频
  * 支持小端和大端架构，并将硬实时的具体细节抽象化，使其可封装在硬件相关模块中
  * 支持基于不同物理传输的 Controller（HCI）构建
  * 等时信道

* :ref:`蓝牙 Host <bluetooth_le_host>`

  * 通用访问配置文件（GAP），支持所有可能的 LE 角色

    * Peripheral 与 Central
    * Observer 与 Broadcaster
    * 多 PHY 支持（2Mbit/s、Coded）
    * 扩展广播
    * 周期广播（含 Sync Transfer）

  * GATT（通用属性配置文件）

    * Server（作为传感器）
    * Client（连接传感器）
    * 增强 ATT（EATT）
    * GATT 数据库哈希
    * GATT 多通知

  * 配对支持，包括 Bluetooth 4.2 的 Secure Connections 特性

  * 非易失性存储支持，用于永久存储蓝牙专属设置和数据

  * 蓝牙 Mesh 支持

    * Relay、Friend Node、Low-Power Node（LPN）和 GATT Proxy 特性
    * 支持两种 Provisioning 角色和承载方式（PB-ADV 与 PB-GATT）
    * 内置基础模型
    * 高度可配置，可适配小至 16k RAM 的设备

  * 基础蓝牙 BR/EDR（Classic）支持

    * 通用访问配置文件（GAP）
    * 逻辑链路控制与适配协议（L2CAP）
    * 串行端口仿真（RFCOMM 协议）
    * 服务发现协议（SDP）

  * 干净的 HCI 驱动抽象

    * 3-Wire（H:5）与 5-Wire（H:4）UART
    * SPI
    * 作为虚拟 HCI 驱动的本地控制器支持

  * 已与多款主流控制器验证
  * 等时信道
  * :ref:`LE Audio <bluetooth_le_audio_arch>`
