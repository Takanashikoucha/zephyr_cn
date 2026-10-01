.. _biometrics_api:

生物识别
##########

概述
********

生物识别 API 为指纹扫描仪、虹膜扫描仪和人脸识别模块等生物识别传感器提供统一接口。
这些传感器通常用于嵌入式系统、访问控制设备和物联网（IoT）应用中的安全认证。

该 API 支持生物识别操作的全生命周期，包括注册、模板管理和匹配。
传感器可以根据硬件能力在设备本地或主机系统上存储模板。

典型的指纹注册过程需要捕获同一手指的多个样本，以创建可靠的模板。
匹配过程将捕获的样本与已存储的模板进行比较，以验证身份。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_BIOMETRICS`
* :kconfig:option:`CONFIG_BIOMETRICS_INIT_PRIORITY`

API 参考
*************

.. doxygengroup:: biometrics_interface
