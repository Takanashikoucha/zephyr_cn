.. _external_module_libiio:

libiio
######

简介
****

`libiio`_ 是一个开源库，主要由 Analog Devices 开发，用于与 Linux
工业输入/输出（IIO）设备交互。这包括但不限于 ADC、DAC、加速度计、
陀螺仪、IMU、压力和温度传感器，以及 RF 收发器。libiio 可以在 target
上原生使用，也可以从运行 Linux、Windows 或 macOS 的主机通过 USB、
以太网或串口与 target 远程通信。

libiio 仓库包含一个 Zephyr 模块，可将 Zephyr 应用变成这样一个可远程
访问的 target。IIO 设备和通道与 Zephyr 设备模型集成，内置驱动适配现有
的 Zephyr 传感器和 ADC/DAC 驱动，而 **iiod**（IIO 守护进程）的 Zephyr
移植则通过网络 socket、UART 控制台、USB CDC-ACM 或原生 USB vendor
类将这些设备暴露给远程主机。现有的 libiio Python 绑定、命令行工具
（如 ``iio_info``）和 `Scopy`_ 桌面应用无需修改即可直接作用于
Zephyr target，从运行 Linux、Windows 或 macOS 的主机使用。完整情况
请参见 `Zephyr 移植文档`_。

核心库采用 GNU Lesser General Public License（LGPL）2.1 版发布，
其示例/测试应用采用 GNU General Public License（GPL）2.0 版发布。
上文描述的 Zephyr 集成采用 MIT 许可，其静态链接的核心文件同样采用
MIT 许可。

在 Zephyr 中使用
****************

要将 libiio 作为 Zephyr 模块引入，可以将其作为 West 项目添加到
``west.yml`` 文件，或通过添加子 manifest（例如
``zephyr/submanifests/libiio.yaml``）文件引入，内容如下，然后运行
``west update``：

.. code-block:: yaml

   manifest:
     remotes:
       - name: analogdevicesinc
         url-base: https://github.com/analogdevicesinc

     projects:
       - name: libiio
         remote: analogdevicesinc
         revision: main
         path: modules/lib/libiio

参考资料
********

.. target-notes::

.. _libiio:
   https://github.com/analogdevicesinc/libiio

.. _Zephyr 移植文档:
   https://analogdevicesinc.github.io/libiio/main/zephyr/

.. _Scopy:
   https://analogdevicesinc.github.io/scopy
