.. _footprint:

优化占用空间
########################

栈大小
***********

各种系统线程的栈大小被宽裕地指定，以允许在尽可能多的受支持平台上的不同场景中使用。你应该通过审查所有栈大小并针对你的应用调整它们来开始优化过程：

:kconfig:option:`CONFIG_ISR_STACK_SIZE`
    默认设置为 2048

:kconfig:option:`CONFIG_MAIN_STACK_SIZE`
    默认设置为 1024

:kconfig:option:`CONFIG_IDLE_STACK_SIZE`
    默认设置为 320

:kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`
    默认设置为 1024

:kconfig:option:`CONFIG_PRIVILEGED_STACK_SIZE`
    默认设置为 1024，取决于 userspace 功能。


未使用的外设
******************

某些外设默认启用。你可以在项目配置中禁用未使用的外设，例如::


        CONFIG_GPIO=n
        CONFIG_SPI=n

各种调试/信息选项
***********************************

以下选项输出更多关于运行中应用的信息，并提供调试和错误处理的手段：

:kconfig:option:`CONFIG_BOOT_BANNER`
    此选项可以禁用以节省几个字节。

:kconfig:option:`CONFIG_DEBUG`
    此选项可以启用用于调试构建。

注意启动横幅（boot banner）默认启用。


MPU/MMU 支持
***************

根据你的应用和平台需求，你可以禁用 MPU/MMU 支持以节省一些内存并改进性能。不过要考虑这一配置选择的后果，因为你将失去高级栈检查功能及其支持。
