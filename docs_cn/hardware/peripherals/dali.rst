.. _dali_api:

DALI
####

DALI 是数字可寻址照明接口，一种用于专业照明解决方案的通信标准。
此 API 不稳定且可能更改。

基本操作
***************

DALI 标准使用基于通过总线系统交换帧的通信模型。
帧是曼彻斯特编码的数据，以停止条件终止。DALI 标准
要求发射器和接收器的特定行为。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_DALI`
* :kconfig:option:`CONFIG_DALI_PWM`


API 参考
*************

.. doxygengroup:: dali_interface
