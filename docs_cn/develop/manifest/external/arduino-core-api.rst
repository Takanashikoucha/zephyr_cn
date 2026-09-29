.. _external_module_arduino_core_api:

Arduino Core API
################

简介
****

Arduino-Core-Zephyr 模块起源于 `Google Summer of Code 2022 项目`_，
旨在为 Zephyr RTOS 应用提供 Arduino 风格的 API。该模块作为一个抽象
层，让熟悉 Arduino 编程的开发人员无需学习全新的 API 和库，即可利用
Zephyr 的能力。

理解其组件
==========

该模块由两个协同工作的关键组件组成：

**1. ArduinoCore-API（通用 Arduino API 定义）**

`ArduinoCore-API <https://github.com/arduino/ArduinoCore-API>`_ 是 Arduino 官方的
硬件抽象层，定义了通用的 Arduino API。它包含抽象 API 定义**以及**与硬件无关
功能的实现。

主要特点：

* 同时包含 API 定义（头文件）和与硬件无关的实现
* 提供 ``String``、``Print``、``Stream``、``IPAddress`` 等类及其完整实现
* 为硬件相关的类（如 ``HardwareSerial``、``HardwareSPI``）定义接口
* 在所有现代 Arduino 平台间共享，以保持一致性
* 实现细节参见 `ArduinoCore-API README <https://github.com/arduino/ArduinoCore-API#arduinocore-api>`_
* 采用 GNU LESSER GENERAL PUBLIC LICENSE Version 2.1 许可

**2. ArduinoCore-Zephyr（Zephyr 特定实现）**

`Arduino-Core-Zephyr <https://github.com/zephyrproject-rtos/ArduinoCore-zephyr>`_ 模块
提供 Arduino API 的**Zephyr 特定实现**。依赖硬件的 Arduino 函数在这里使用
Zephyr 原生 API 和驱动实现。

主要特点：

* 包含 ``cores/arduino`` 目录，内含 Zephyr 实现（``zephyrCommon.cpp``、``zephyrSerial.cpp`` 等）
* 提供带引脚映射和 Device Tree overlay 的板级变体
* 集成 Zephyr 构建系统（CMake、Kconfig、west.yml）
* 链接 ArduinoCore-API 以继承通用实现
* 实现细节参见 `项目文档 <https://github.com/zephyrproject-rtos/ArduinoCore-zephyr/tree/main/documentation>`_
* 采用 Apache-2.0 许可

提供的功能
==========

这些组件共同提供：

* 标准的 Arduino API 函数，如 ``pinMode()``、``digitalWrite()``、``analogRead()`` 等
* 支持 Arduino 风格的 ``setup()`` 和 ``loop()`` 函数
* Arduino 引脚编号与 Zephyr GPIO 定义之间的引脚映射
* 支持常见 Arduino 通信协议（Serial、I2C、SPI）
* 兼容现有 Arduino 库
* 支持 Zephyr 中已有的各硬件平台的板级变体

该模块将 Arduino 风格的编程引入 Zephyr，为从 Arduino 转向 Zephyr 的开发者
提供更平缓的学习曲线，同时仍能受益于 Zephyr 的高级特性、可扩展性和广泛的
硬件支持。

在 Zephyr 中使用
****************

将 Arduino Core API 添加到 Zephyr 项目
======================================

#. 要将 Arduino Core for Zephyr 作为 Zephyr 模块引入，可以将其作为 West
   项目添加到 west.yml 文件，或通过添加子 manifest（例如
   ``zephyr/submanifests/arduinocore.yaml``）文件引入，内容如下：

   .. code-block:: yaml

      # Arduino API repository
      - name: ArduinoCore-zephyr
        path: modules/lib/arduinocore-zephyr
        revision: main
        url: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr

#. 运行以下命令更新项目：

   .. code-block:: bash

      west update

#. 对于 Linux 用户，模块中有一个 ``install.sh`` 脚本，会自动链接
   ArduinoCore-API。如果无法使用该脚本，请按照以下手动步骤操作。

   .. note::

      如果 install.sh 脚本运行成功，请跳过下一步。下一步面向 Linux 用户，
      其模块安装位置可能有所不同，或使用了带自定义路径的自定义
      Zephyr 配置。

#. 通过将 ArduinoCore-API 仓库中的 API 文件夹链接到 arduinocore-zephyr
   文件夹，完成核心设置：

   .. code-block:: bash

      west blobs fetch

   ``cores`` 文件夹位于 ``<zephyr-project-path>/modules/lib/arduinocore-zephyr/cores``。

在应用中使用 Arduino Core API
==============================

#. 在应用的 ``prj.conf`` 文件中，启用 Arduino API 配置，方式类似于
   `blinky_arduino 示例`_ 中的做法。

#. 使用 Arduino 风格代码创建应用：

   .. code-block:: cpp

      #include <Arduino.h>

      void setup() {
        pinMode(LED_BUILTIN, OUTPUT);
      }

      void loop() {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(1000);
        digitalWrite(LED_BUILTIN, LOW);
        delay(1000);
      }

#. 针对目标板构建应用：

   .. code-block:: bash

      west build -b <board_name> path/to/your/app

添加自定义板级支持
==================

受支持的板位于 arduinocore-zephyr 的 ``variants/`` 目录中。
要为自定义板添加支持：

#. 在 ``variants/`` 目录中创建一个以板名命名的新文件夹
#. 添加与板名匹配的 overlay 文件和 pinmap 头文件
#. 将新头文件添加到 ``variant.h`` 文件中的 ``#ifdef`` 语句中

有关添加板级变体的详细步骤，请参阅 `board variants 文档`_。

使用外部 Arduino 库
===================

要在 Zephyr 项目中使用外部 Arduino 库：

#. 将库的源文件（例如 ``MyLibrary.h`` 和 ``MyLibrary.cpp``）添加到项目的 ``src`` 文件夹
#. 更新应用的 ``CMakeLists.txt`` 以包含这些文件：

   .. code-block:: cmake

      target_sources(app PRIVATE src/MyLibrary.cpp)

#. 在源代码中包含该库：

   .. code-block:: cpp

      #include "MyLibrary.h"

有关使用外部库的更多细节，请参阅 `Arduino libraries 文档`_。

参考资料
********

#. `Arduino-Core-Zephyr GitHub 仓库`_
#. `ArduinoCore-API 仓库`_
#. `Golioth 文章：Zephyr + Arduino：一个 Google Summer of Code 的故事`_

.. target-notes::

.. _Arduino Core API: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr
.. _board variants 文档: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr/blob/main/documentation/variants.md
.. _Arduino libraries 文档: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr/blob/main/documentation/arduino_libs.md
.. _Arduino-Core-Zephyr GitHub 仓库: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr
.. _ArduinoCore-API 仓库: https://github.com/arduino/ArduinoCore-API
.. _Google Summer of Code 2022 项目: https://dhruvag2000.github.io/Blog-GSoC22/
.. _Golioth 文章\: Zephyr + Arduino\: 一个 Google Summer of Code 的故事: https://blog.golioth.io/zephyr-arduino-a-google-summer-of-code-story/
.. _blinky_arduino 示例: https://github.com/zephyrproject-rtos/ArduinoCore-zephyr/blob/next/samples/blinky_arduino/prj.conf
