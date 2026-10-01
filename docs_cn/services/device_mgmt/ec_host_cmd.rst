.. _ec_host_cmd_backend_api:

EC Host Command
###############

Overview
********
Host command protocol 定义 host（或 application processor）与
target embedded controller (EC) 通信的 interface。EC Host command subsystem 实现
protocol 的 target 侧（生成对 host 发送 commands 的 responses。Host command
protocol interface 支持多个 versions（但此 subsystem 实现仅支持
protocol version 3。

Architecture
************
Host Command subsystem 包含若干 components：

* Backend
* General handler
* Command handler

Backend 为 peripheral driver 与 general handler 间的层。其负责
通过 chosen peripheral 发送和接收 commands。

General handler 验证来自 backend 的 data（如检查 sizes、checksum 等。若 command
有效且 user 为收到的 command id 提供了 handler（则调用
command handler。

.. image:: ec_host_cmd.png
   :align: center

SHI (Serial Host Interface) 与此不同（因为其仅用于与
host 通信。SHI 本身无 API（故 backend 和 peripheral driver layers 合并为
一个 backend layer。

.. image:: ec_host_cmd_shi.png
   :align: center

另一情况为 SPI。不幸的是（当前 SPI API 不能用于处理
host commands
communication。主要问题为 host 发送的未知 command size（SPI transaction
发送/接收特定数量 bytes）和需持续发送 status byte（SPI module
按 transaction 启用和禁用。这强制在 backend 内实现 SPI driver（
如 SHI 所做。这意味着 SPI backend 须按 chip family 实现。然而（
一旦 SPI API 扩展到 host command 需要（将来可更改。请查看 `the
discussion <https://github.com/zephyrproject-rtos/zephyr/issues/56091>`_。

此方法须以特殊方式配置 SPI dts node。
SPI node 的主要 compatible string 已更改为使用 SPI driver 的 Host Command 版本。其余
properties 应按常规配置。STM32 的 SPI node 示例：

.. code-block:: devicetree

   &spi1 {
           /* Change the compatible string to use the Host Command version of the
            * STM32 SPI driver
            */
           compatible = "st,stm32-spi-host-cmd";
           status = "okay";

           dmas = <&dma2 3 3 0x38440 0x03>,
                <&dma2 0 3 0x38480 0x03>;
           dma-names = "tx", "rx";
           /* This field is used to point at our CS pin */
           cs-gpios = <&gpioa 4 (GPIO_ACTIVE_LOW | GPIO_PULL_UP)>;
   };

STM32 SPI host command backend driver 支持 :dtcompatible:`st,stm32h7-spi` 和
:dtcompatible:`st,stm32-spi-fifo` variant 实现。要启用这些 variants（追加
相应 compatible string。例如（要启用 FIFO 支持和
STM32H7
SoCs 支持（按所示修改 compatible string。

.. code-block:: devicetree

   &spi1 {
       compatible = "st,stm32h7-spi", "st,stm32-spi-fifo", "st,stm32-spi-host-cmd";
       ...
   };

运行 Zephyr 的 chip 为 SPI slave（且 ``cs-gpios`` property 用于指向
CS pin。
对 SPI（须设置 backend chosen node ``zephyr,host-cmd-spi-backend``。

支持的 backend 和 peripheral drivers：

* Simulator
* SHI - ITE 和 NPCX
* eSPI - 支持 :kconfig:option:`CONFIG_ESPI_PERIPHERAL_EC_HOST_CMD` 和
  :kconfig:option:`CONFIG_ESPI_PERIPHERAL_CUSTOM_OPCODE` 的任何 eSPI slave driver
* UART - 支持 asynchronous API 的任何 UART driver
* SPI - STM32

Initialization
**************

若 application 配置以下 backend chosen nodes 之一且
:kconfig:option:`CONFIG_EC_HOST_CMD_INITIALIZE_AT_BOOT` 已设置（则相应 backend
通过调用 :c:func:`ec_host_cmd_init` 初始化
host command subsystem：

* ``zephyr,host-cmd-espi-backend``
* ``zephyr,host-cmd-shi-backend``
* ``zephyr,host-cmd-uart-backend``
* ``zephyr,host-cmd-spi-backend``

若未配置 backend chosen node（application 须直接调用 :c:func:`ec_host_cmd_init`
function。此初始化方式在 backend 在
runtime 基于如 GPIO state 选择时有用。

Buffers
*******

Host command communication 需 rx 和 tx 的 buffers。若
:kconfig:option:`CONFIG_EC_HOST_CMD_HANDLER_RX_BUFFER_SIZE` > 0 则 general handler 提供
rx buffer（
:kconfig:option:`CONFIG_EC_HOST_CMD_HANDLER_TX_BUFFER_SIZE` > 0 则提供
tx buffer。共享
buffers 对使用多个 backends 的 applications 有用。每个
backend 定义单独 buffers 将增加 memory 使用。然而（某些 buffers 可由 peripheral driver
定义（如 eSPI。这些应尽可能复用。

Logging
*******

Host command 有内嵌 logging system 记录 ongoing communication。有若干 logging
levels：

* :c:macro:`LOG_INF` 用于记录新 command 的 command id 和 not success responses。相同
  command 的 repeats 不记录
* :c:macro:`LOG_DBG` 记录每个 command（即使 repeats
* :c:macro:`LOG_DBG` + :kconfig:option:`CONFIG_EC_HOST_CMD_LOG_DBG_BUFFERS` 记录每个 command 和 responses
  及 data buffers

API Reference
*************

.. doxygengroup:: ec_host_cmd_interface
