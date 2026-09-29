.. _stepper_api:

Steppers
########

Stepper
driver
subsystem
由
两
个
device
driver
APIs
组成：

Stepper
API
***********

Stepper
driver
API
为
stepper
drivers
提供
一
个
common
interface。

- 用
  :c:func:`stepper_set_micro_step_res`
  和
  :c:func:`stepper_get_micro_step_res`
  配置
  **micro-stepping
  resolution**
- 用
  :c:func:`stepper_enable`
  **启用**
  stepper
  driver
- 用
  :c:func:`stepper_disable`
  **禁用**
  stepper
  driver
- 用
  :c:func:`stepper_set_event_cb`
  注册
  **event
  callback**

Stepper
Motion
Controller
API
*****************************

Stepper
motion
controller
API
为
stepper
motion
controllers
提供
一
个
common
interface。

- 用
  :c:func:`stepper_ctrl_set_reference_position`
  和
  :c:func:`stepper_ctrl_get_actual_position`
  配置
  **reference
  position**
  以
  microsteps
  为
  单位
- 用
  :c:func:`stepper_ctrl_set_microstep_interval`
  设置
  steps
  之间
  的
  **step
  interval**
  以
  nanoseconds
  为
  单位
- 用
  :c:func:`stepper_ctrl_move_by`
  **move
  by**
  +/-
  micro-steps
  也
  称为
  **relative
  movement**
- 用
  :c:func:`stepper_ctrl_move_to`
  **move
  to**
  特定
  position
  也
  称为
  **absolute
  movement**
- 用
  :c:func:`stepper_ctrl_run`
  以
  特定
  direction
  的
  **constant
  step
  interval**
  连续
  运行
  直到
  检测到
  stop
- 用
  :c:func:`stepper_ctrl_stop`
  **停止**
  stepper
- 用
  :c:func:`stepper_ctrl_is_moving`
  检查
  stepper
  是否
  **moving**
- 用
  :c:func:`stepper_ctrl_set_event_cb`
  注册
  **event
  callback**

.. _stepper-device-tree:

Device
Tree
***********

在
stepper
motion
controllers
的
context
中
devicetree
提供
初始
hardware
