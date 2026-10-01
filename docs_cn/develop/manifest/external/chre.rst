.. _external_module_chre:

Context Hub Runtime Environment（CHRE）
######################################

简介
****

`Context Hub Runtime Environment`_（CHRE）是 Android 的常开应用平台，这类应用称为 *nanoapps*，运行在与运行 Android 的应用处理器相邻的低功耗处理器上。Nanoapps 面向跨平台标准化的 CHRE API 编写，由 CHRE 框架托管，该框架是此 API 的 AOSP 参考实现。

`zephyrproject-rtos/chre`_ 仓库是 AOSP 框架的一个 fork，在 ``platform/zephyr`` 下包含 Zephyr 移植。该移植在专用线程中运行 CHRE 事件循环，并提供框架所需的平台原语（内存、定时器、系统时间、日志和主机链路）。音频、GNSS、传感器、WiFi 和 WWAN 的平台抽象层（PAL）未针对 Zephyr 实现。

CHRE 采用 Apache-2.0 许可。

在 Zephyr 中使用
****************

要将 CHRE 作为 Zephyr :ref:`模块 <modules>` 引入，可以将其作为 West 项目添加到 ``west.yaml`` 文件，或通过添加子 manifest（例如 ``zephyr/submanifests/chre.yaml``）文件引入，内容如下，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: chre
         url: https://github.com/zephyrproject-rtos/chre
         revision: zephyr
         path: modules/lib/chre # adjust the path as needed

通过 ``CONFIG_CHRE=y`` 启用框架。CHRE 使用 C++ 编写，并选择 :kconfig:option:`CONFIG_REQUIRES_FULL_LIBCPP`，因此工具链必须提供完整的 C++ 标准库。模块 ``platform/zephyr/Kconfig`` 中其余的 ``CONFIG_CHRE_*`` 选项用于设置事件循环线程和内存池大小，并启用各个 PAL 框架。

模块在 ``zephyr/sample`` 下包含一个示例应用，它会启动事件循环、加载一个 nanoapp、向其投递一个事件然后关闭。使用以下命令在 :zephyr:board:`native_sim` 上构建并运行：

.. code-block:: console

   west build -b native_sim modules/lib/chre/zephyr/sample -t run

参考资料
********

.. target-notes::

.. _Context Hub Runtime Environment:
   https://source.android.com/docs/core/interaction/contexthub

.. _zephyrproject-rtos/chre:
   https://github.com/zephyrproject-rtos/chre
