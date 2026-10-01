.. _rtc_api:

实时时钟（RTC）
#####################

概述
********

.. list-table:: **术语表**
    :widths: 30 80
    :header-rows: 1

    * - 术语
      - 定义
    * - 实时时钟（Real-time clock）
      - 使用分解时间（broken-down time）跟踪时间的低功耗设备
    * - 实时计数器（Real-time counter）
      - 可用于跟踪时间的低功耗计数器
    * - RTC
      - 实时时钟（real-time clock）的缩写

RTC 是一种使用分解时间跟踪时间的低功耗设备。它不应与有时共享相同名称、缩写或两者的低功耗计数器相混淆。

RTC 通常针对低能耗进行优化，并且通常在系统处于低功耗状态时仍保持运行。

RTC 通常包含一个或多个可配置为在指定时间触发的闹钟（alarm）。这些闹钟通常用于将系统从低功耗状态中唤醒。

设备树（devicetree）绑定
*******************

RTC 绑定必须包含 ``rtc-device.yaml`` 绑定，该绑定包含 ``base.yaml`` 绑定以及必需的 ``alarms-count`` 属性。

.. code-block:: yaml

   include: rtc-device.yaml

设备驱动程序设计
********************

驱动程序初始化
============

RTC 从不被系统断电。在初始化时，驱动程序应当预期 RTC 处于以下两种状态之一：

* 已通电、已配置且正在运行。
* 已通电、未配置且已停止。

在初始化时，驱动程序应确保 RTC 被正确配置，同时保留时间、闹钟和运行状态。

通过调用 :c:func:`rtc_set_time` 设置时间，此时 RTC 将开始运行。闹钟的挂起（pending）状态由 :c:func:`rtc_alarm_is_pending` 或由 :c:func:`rtc_alarm_set_callback` 产生的闹钟回调清除。

GPIO 路由的中断
======================

具有已连接中断输出引脚的 RTC 应在初始化时配置并启用这些引脚。主机可以启用和禁用其 GPIO 的中断，但 RTC 的中断输出引脚必须保持启用状态。

这确保了内部连接和外部连接的 RTC 之间行为一致，并允许通过任何已启用的 RTC 事件（如闹钟或更新事件）经由 GPIO 唤醒系统。

.. note::

   具有未连接中断输出引脚的 RTC 不允许通过定期轮询 RTC 来模拟其已连接的状态。
   在这种情况下，:c:func:`rtc_alarm_set_callback` 和
   :c:func:`rtc_update_set_callback` 应返回 ``-ENOTSUP``。

时钟输出
=============

如果支持时钟输出，其配置在设备树中定义。输出由驱动程序在初始化时配置。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_RTC`
* :kconfig:option:`CONFIG_RTC_ALARM`
* :kconfig:option:`CONFIG_RTC_UPDATE`
* :kconfig:option:`CONFIG_RTC_CALIBRATION`

API 参考
*************

.. doxygengroup:: rtc_interface

.. doxygengroup:: rtc_fake

RTC 设备驱动程序测试套件
****************************

该测试套件用于验证 RTC 设备驱动程序的行为。它被设计为可跨开发板移植，并使用设备树别名 ``rtc`` 来指定要测试的 RTC 设备。

此测试套件测试以下内容：

* 设置和获取时间。
* RTC 时间正确递增。
* 闹钟功能（如果硬件支持），包括启用和不启用回调两种情况
* 校准功能（如果硬件支持）。

校准测试会测试一系列数值，并将其打印到控制台供手动比对。用户必须检查所设置和所读取的数值，以确保其有效。

默认情况下，测试仅启用必需的时间设置和获取功能。要测试可选的闹钟、更新事件回调和时钟校准功能，必须通过选择 :kconfig:option:`CONFIG_RTC_ALARM`、:kconfig:option:`CONFIG_RTC_UPDATE` 和 :kconfig:option:`CONFIG_RTC_CALIBRATION` 来启用它们。

以下示例针对 ``native_sim`` 开发板构建测试套件。要为其他开发板构建测试套件，请用你的开发板替换 ``native_sim``。

要使用默认配置构建测试应用（仅测试必需功能），可以参考以下命令：

.. zephyr-app-commands::
   :tool: west
   :host-os: unix
   :board: native_sim
   :zephyr-app: tests/drivers/rtc/rtc_api
   :goals: build

要启用额外的 RTC 功能来构建测试，请使用 menuconfig 通过更新配置来启用这些额外功能。可以参考以下命令：

.. zephyr-app-commands::
   :tool: west
   :host-os: unix
   :board: native_sim
   :zephyr-app: tests/drivers/rtc/rtc_api
   :goals: menuconfig

然后使用以下命令构建测试应用：

.. zephyr-app-commands::
   :tool: west
   :host-os: unix
   :board: native_sim
   :zephyr-app: tests/drivers/rtc/rtc_api
   :maybe-skip-config:
   :goals: build

要运行测试套件，请在你的开发板上烧录并运行该应用，输出将打印到控制台。

.. note::

   如果测试的是真实硬件，每个测试最多耗时 30 秒。

.. _rtc_api_emul_dev:

RTC 模拟设备
*******************

模拟 RTC 设备完整实现了 RTC API，其行为与真实 RTC 设备一致，但存在以下限制：

* RTC 时间不会在应用程序初始化之间保持持久。
* RTC 闹钟不会在应用程序初始化之间保持持久。
* RTC 时间会随时间产生漂移。

每次应用程序初始化时，RTC 的时间和闹钟都会被重置。使用 :c:func:`rtc_get_time` 读取时间将返回 ``-ENODATA``，直到使用 :c:func:`rtc_set_time` 设置时间。之后 RTC 将表现得与真实 RTC 一致，直到应用程序被重置。

模拟 RTC 设备驱动程序针对 :dtcompatible:`zephyr,rtc-emul` 兼容项构建，并在选择 :kconfig:option:`CONFIG_RTC` 时会被包含。

Zephyr 中 RTC 的历史
*************************

在此 API 创建之前，RTC 已经通过 :ref:`counter_api` API 得到支持。Unix 时间戳用于在 RTC 驱动程序内部进行分解时间与 Unix 时间戳之间的转换，而 RTC 驱动程序内部使用的正是分解时间表示法。

这种方法的缺点是：硬件计数器无法被设置为特定计数值，导致所有 RTC 都必须使用设备特定的 API 来设置时间（将 Unix 时间转换为分解时间，在某些情况下这种转换是不必要的），并且缺少一些常见功能，例如输入时钟校准和更新回调。
