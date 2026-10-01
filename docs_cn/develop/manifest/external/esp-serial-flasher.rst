.. _external_module_esp_serial_flasher:

ESP Serial Flasher
##################

简介
****

ESP Serial Flasher 是由 Espressif Systems 开发并维护的可移植 C 库，支持从运行嵌入式操作系统的主机微控制器对 Espressif SoC（ESP8266、ESP32 系列）进行编程和交互。该库为跨多种通信接口（包括 UART、USB CDC ACM、SPI 和 SDIO）的闪存操作、RAM 下载与执行以及设备管理提供统一 API。

对于需要编程或操作 Espressif 目标设备、且无需 PC 或 Python 运行环境的基于 Zephyr 的应用，该模块尤其有价值。它提供与 esptool 类似的功能，但针对资源受限的嵌入式系统进行了优化，非常适合生产编程工具、bootloader 和固件更新机制。

ESP Serial Flasher 支持广泛的 Espressif SoC。支持的目标列表及更多信息请参见 `ESP Serial Flasher GitHub`_。

ESP Serial Flasher 采用 Apache License 2.0。

在 Zephyr 中使用
*****************

要将 ESP Serial Flasher 作为 Zephyr 模块引入，可以将其作为 West 项目添加到 ``west.yml`` 文件，或通过添加子 manifest（例如 ``zephyr/submanifests/esp-serial-flasher.yaml``）引入，内容如下，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: esp-serial-flasher
         url: https://github.com/espressif/esp-serial-flasher
         revision: master
         path: modules/esp-serial-flasher # adjust path or leave blank for west workspace root directory

添加模块后，可在应用代码中包含主头文件：

.. code-block:: c

   #include <esp_loader.h>

Zephyr 集成提供设备树绑定 ``espressif,esp-loader``，必须在应用的设备树中至少定义一次。使用 ``zephyr,esp-loader`` chosen 属性选择激活的实例。驱动负责 UART 通信、boot 和 reset 引脚的 GPIO 控制，并提供闪存操作、设备连接和目标管理的高层 API。

目标的固件镜像可嵌入主机应用中。将二进制文件放入 ``target-firmware/`` 文件夹，并在 ``target-firmware/images.csv`` 中描述闪存地址：每行一个镜像，格式为 ``<filename>;<offset>``，offset 为十六进制且**不带** ``0x`` 前缀（例如 ``app.bin;10000``）。

包含 ``bin_images_sections.cmake``（来自 Zephyr 示例）后，应用 ``CMakeLists.txt`` 中的 ``create_resources()`` 会把这些文件转换为 C 数组。在 ``prj.conf`` 中通过 ``CONFIG_ESP_SERIAL_FLASHER=y`` 启用驱动。``images.csv``、CMake 和设备树的设置请参见 `ESP Serial Flasher GitHub`_ 仓库中的 ``examples/zephyr_example``。

要基于 Shell 交互，使用 ``CONFIG_ESP_SERIAL_FLASHER_SHELL=y`` 构建 ``examples/zephyr_example``。该示例提供 ``esf`` Shell 命令组，可从 Zephyr Shell 连接 ESP 目标、读写闪存内存、检测闪存大小、擦除闪存，以及读写寄存器。

参考资料
*********

- `ESP Serial Flasher 组件注册中心`_
- `Zephyr 模块文档`_

.. target-notes::

.. _ESP Serial Flasher GitHub:
   https://github.com/espressif/esp-serial-flasher

.. _ESP Serial Flasher 组件注册中心:
   https://components.espressif.com/components/espressif/esp-serial-flasher

.. _Zephyr 模块文档:
   https://docs.zephyrproject.org/latest/develop/modules.html
