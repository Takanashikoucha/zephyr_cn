.. _comparator_api:

比较器
##########

概述
********

模拟比较器比较连接到其负输入与正输入的两个模拟信号的电压。如果正输入的电压高于负输入，比较器的输出为高；否则为低。

比较器通常可以设置一个在输出变化时触发的触发器。该触发器可以调用回调，也可以轮询其状态。

相关配置选项：

* :kconfig:option:`CONFIG_COMPARATOR`

配置
*************

嵌入式比较器通常可以在运行时配置。启用时，必须通过设备树提供初始配置。在运行时，比较器可以使用设备驱动特定的 API 更新其配置。配置将在比较器恢复（resume）时生效。

电源管理
****************

比较器通过电源管理来启用。恢复（resume）时，比较器会主动比较其输入，产生输出并检测边沿；挂起（suspend）时，比较器处于非活动状态。

比较器 shell
****************

比较器 shell 为 :ref:`shell <shell_api>` 模块提供带有子命令集的 ``comp`` 命令。

``comp`` shell 命令提供以下子命令：

* ``get_output`` 参见 :c:func:`comparator_get_output`
* ``set_trigger`` 参见 :c:func:`comparator_set_trigger`
* ``await_trigger`` 用以下流程等待触发：

  * 用 :c:func:`comparator_set_trigger_callback` 设置触发回调
  * 等待回调，或在默认或可选提供的超时后超时
  * 用 :c:func:`comparator_set_trigger_callback` 清除触发回调
* ``trigger_is_pending`` 参见 :c:func:`comparator_trigger_is_pending`

相关配置选项：

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_COMPARATOR_SHELL`
* :kconfig:option:`CONFIG_COMPARATOR_SHELL_AWAIT_TRIGGER_DEFAULT_TIMEOUT`
* :kconfig:option:`CONFIG_COMPARATOR_SHELL_AWAIT_TRIGGER_MAX_TIMEOUT`

.. note::
   电源管理 shell 可以可选地与比较器 shell 一起启用。

   相关配置选项：

   * :kconfig:option:`CONFIG_PM_DEVICE`
   * :kconfig:option:`CONFIG_PM_DEVICE_SHELL`

API 参考
*************

.. doxygengroup:: comparator_interface

.. doxygengroup:: comparator_fake
