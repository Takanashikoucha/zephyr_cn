.. _stepper_api:

步进电机
########

步进电机驱动子系统由两个设备驱动 API 组成：

步进电机 API
***********

步进电机驱动 API 为步进电机驱动提供通用接口。

- 用 :c:func:`stepper_set_micro_step_res` 和 :c:func:`stepper_get_micro_step_res` 配置**微步分辨率**。
- 用 :c:func:`stepper_enable` **启用**步进电机驱动。
- 用 :c:func:`stepper_disable` **禁用**步进电机驱动。
- 用 :c:func:`stepper_set_event_cb` 注册**事件回调**。

步进电机运动控制器 API
*****************************

步进电机运动控制器 API 为步进电机运动控制器提供通用接口。

- 用 :c:func:`stepper_ctrl_set_reference_position` 和 :c:func:`stepper_ctrl_get_actual_position` 配置以微步为单位的**参考位置**。
- 用 :c:func:`stepper_ctrl_set_microstep_interval` 设置步与步之间以纳秒为单位的**步距间隔**。
- 用 :c:func:`stepper_ctrl_move_by` 以 +/- 微步**移动**，也称为**相对移动**。
- 用 :c:func:`stepper_ctrl_move_to` **移动到**特定位置，也称为**绝对移动**。
- 用 :c:func:`stepper_ctrl_run` 以特定方向**恒定步距间隔**连续运行直到检测到停止。
- 用 :c:func:`stepper_ctrl_stop` **停止**步进电机。
- 用 :c:func:`stepper_ctrl_is_moving` 检查步进电机是否**移动中**。
- 用 :c:func:`stepper_ctrl_set_event_cb` 注册**事件回调**。

.. _stepper-device-tree:

设备树
***********

在步进电机运动控制器的上下文中，设备树在每设备级别为步进电机驱动提供初始硬件配置。每个设备必须在 Zephyr 中指定一个设备树绑定，理想情况下，还有一组硬件配置选项，用于电流量设置、斜坡参数等。然后可以在板级设备树中使用它们来将步进电机驱动配置到其初始状态。

驱动组合场景
============================

以下是两个典型场景：

.. toctree::
    :maxdepth: 1

    integrated_controller_driver.rst
    individual_controller_driver.rst

步进电机运动控制器 API 测试套件
****************************************

步进电机运动控制器 API 测试套件提供一组测试，可用于验证步进电机运动控制器的功能。

.. zephyr-app-commands::
    :zephyr-app: tests/drivers/stepper/stepper_ctrl
    :board: <board>
    :west-args: --extra-dtc-overlay <path/to/board.overlay>
    :goals: build flash

示例输出
=============

以下是 h-bridge-stepper-ctrl 的测试输出片段。

.. code-block:: console

    ===================================================================
    TESTSUITE stepper succeeded

    ------ TESTSUITE SUMMARY START ------

    SUITE PASS - 100.00% [stepper_ctrl]: pass = 10, fail = 0, skip = 0, total = 10 duration = 6.869 seconds
     - PASS - [stepper_ctrl.test_actual_position] duration = 0.001 seconds
     - PASS - [stepper_ctrl.test_move_by_negative_step_count] duration = 2.207 seconds
     - PASS - [stepper_ctrl.test_move_by_positive_step_count] duration = 2.202 seconds
     - PASS - [stepper_ctrl.test_move_to_negative_step_count] duration = 1.106 seconds
     - PASS - [stepper_ctrl.test_move_to_positive_step_count] duration = 1.102 seconds
     - PASS - [stepper_ctrl.test_move_zero_steps] duration = 0.006 seconds
     - PASS - [stepper_ctrl.test_run_negative_direction] duration = 0.115 seconds
     - PASS - [stepper_ctrl.test_run_positive_direction] duration = 0.124 seconds
     - PASS - [stepper_ctrl.test_set_micro_step_interval_invalid_zero] duration = 0.002 seconds
     - PASS - [stepper_ctrl.test_stop] duration = 0.004 seconds

    ------ TESTSUITE SUMMARY END ------

    ===================================================================
    PROJECT EXECUTION SUCCESSFUL

API 参考
*************

.. _stepper-driver-api-reference:

所有步进电机驱动应实现的通用函数集。

.. doxygengroup:: stepper_hw_driver

.. _stepper-ctrl-api-reference:

所有步进电机运动控制器应实现的通用函数集。

.. doxygengroup:: stepper_ctrl

步进电机运动控制器特定 API
***************************************

Trinamic
========

.. doxygengroup:: trinamic_stepper_ctrl

.. _stepper discord:
    https://discord.com/channels/720317445772017664/1278263869982375946
