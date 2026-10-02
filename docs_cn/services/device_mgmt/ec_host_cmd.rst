.. _ec_host_cmd_backend_api:

EC Host Command
###############

概述
********
主机命令协议（Host Command protocol）定义了主机（或应用处理器）
与目标嵌入式控制器（EC）通信的接口。EC Host 命令子系统实现
该协议的目标端，生成对主机发送命令的响应。主机命令
协议接口支持多个版本，但本子系统实现仅支持
协议版本 3。

架构
************
Host Command 子系统包含几个组件：

* 后端（Backend）
* 通用处理器（General handler）
* 命令处理器（Command handler）

后端是外设驱动程序与通用处理器之间的一层。它负责
通过所选外设发送和接收命令。

通用处理器验证来自后端的数据，例如检查长度、校验和等。如果命令
有效且用户已为收到的命令 id 提供了处理器，则调用
命令处理器。

.. image:: ec_host_cmd.png
   :align: center

SHI（串行主机接口）与此不同，因为它仅用于与
主机通信。SHI 本身没有 API，因此后端和外设驱动层被合并为
一个后端层。

.. image:: ec_host_cmd_shi.png
   :align: center

另一种情况是 SPI。不幸的是，当前的 SPI API 不能用于处理
主机命令
通信。主要问题是主机发送的命令大小未知（SPI 事务
发送/接收特定数量的字节）以及需要持续发送状态字节（SPI 模块
按事务启用和禁用）。这迫使在后端内实现 SPI 驱动，
如同 SHI 所做的那样。这意味着 SPI 后端必须按芯片系列实现。然而，
一旦 SPI API 扩展到满足主机命令的需要，将来可以更改。请查看 `the
discussion <https://github.com/zephyrproject-rtos/zephyr/issues/56091>`_。

该方法要求以特殊方式配置 SPI dts 节点。
SPI 节点的主要 compatible 字符串已更改为使用 SPI 驱动的 Host Command 版本。其余
属性应按常规配置。STM32 的 SPI 节点示例：

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

STM32 SPI 主机命令后端驱动程序支持 :dtcompatible:`st,stm32h7-spi` 和
:dtcompatible:`st,stm32-spi-fifo` 变体实现。要启用这些变体，请追加
相应的 compatible 字符串。例如，要启用 FIFO 支持和
STM32H7
SoC 支持，请按所示修改 compatible 字符串。

.. code-block:: devicetree

   &spi1 {
       compatible = "st,stm32h7-spi", "st,stm32-spi-fifo", "st,stm32-spi-host-cmd";
       ...
   };

运行 Zephyr 的芯片是 SPI 从设备，``cs-gpios`` 属性用于指向
CS 引脚。
对于 SPI，必须设置后端 chosen 节点 ``zephyr,host-cmd-spi-backend``。

支持的后端和外设驱动程序：

* 模拟器（Simulator）
* SHI - ITE 和 NPCX
* eSPI - 支持 :kconfig:option:`CONFIG_ESPI_PERIPHERAL_EC_HOST_CMD` 和
  :kconfig:option:`CONFIG_ESPI_PERIPHERAL_CUSTOM_OPCODE` 的任何 eSPI 从设备驱动
* UART - 支持异步 API 的任何 UART 驱动
* SPI - STM32

初始化
**************

如果应用程序配置了以下后端 chosen 节点之一且
:kconfig:option:`CONFIG_EC_HOST_CMD_INITIALIZE_AT_BOOT` 已设置，则相应后端
通过调用 :c:func:`ec_host_cmd_init` 初始化
主机命令子系统：

* ``zephyr,host-cmd-espi-backend``
* ``zephyr,host-cmd-shi-backend``
* ``zephyr,host-cmd-uart-backend``
* ``zephyr,host-cmd-spi-backend``

如果未配置后端 chosen 节点，应用程序必须直接调用 :c:func:`ec_host_cmd_init`
函数。这种初始化方式在后端于
运行时基于例如 GPIO 状态选择时有用。

缓冲区
*******

主机命令通信需要 rx 和 tx 缓冲区。如果
:kconfig:option:`CONFIG_EC_HOST_CMD_HANDLER_RX_BUFFER_SIZE` > 0，则通用处理器提供
rx 缓冲区；
如果 :kconfig:option:`CONFIG_EC_HOST_CMD_HANDLER_TX_BUFFER_SIZE` > 0，则提供
tx 缓冲区。共享
缓冲区对使用多个后端的有用。每个
后端定义单独的缓冲区将增加内存使用。然而，某些缓冲区可由外设驱动
定义，例如 eSPI。这些应尽可能复用。

日志
*******

主机命令有一个内嵌日志系统，记录正在进行的通信。有若干日志
级别：

* :c:macro:`LOG_INF` 用于记录新命令的命令 id 和未成功的响应。相同
  命令的重复不记录
* :c:macro:`LOG_DBG` 记录每个命令，即使重复
* :c:macro:`LOG_DBG` + :kconfig:option:`CONFIG_EC_HOST_CMD_LOG_DBG_BUFFERS` 记录每个命令和响应
  以及数据缓冲区

API 参考
*************

.. doxygengroup:: ec_host_cmd_interface
