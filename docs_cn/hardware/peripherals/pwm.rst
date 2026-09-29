.. _pwm_api:

Pulse
Width
Modulation
（PWM）
############################

Overview
********

Pulse
Width
Modulation
（PWM）
是
通过
变化
digital
signal
的
duty
cycle
编码
information
或
控制
power
delivery
的
technique。
PWM
signal
以
固定
frequency
在
high
和
low
states
之间
切换；
每个
period
中
花
在
high
state
的
fraction
是
*duty
cycle*。

PWM
在
embedded
systems
中
的
常见
用途：

* **LED
  brightness
  control**
  —
  duty
  cycle
  直接
  map
  到
  perceived
  brightness
* **DC
  motor
  speed
  control**
  —
  average
  voltage
  与
  duty
  cycle
  成
  比例
* **Servo
  motor
  positioning**
  —
  pulse
  width
  编码
  期望
  的
  angle
* **Audio
  tone
  generation**
  —
  变化
  frequency
  产生
  audible
  tones
* **Power
  conversion**
  —
  buck/boost
  converters
  和
  class-D
  amplifiers

PWM
Signal
Parameters
*********************

PWM
signal
由
三
个
values
描述：

* **Period**
  —
  一
  个
  on/off
  cycle
  的
  总
  duration
  以
  nanoseconds
  为
  单位
* **Pulse
  width**
  —
  high
  （active）
  portion
  的
  duration
  以
  nanoseconds
  为
  单位
* **Duty
  cycle**
  —
  pulse
  width
  与
  period
  的
  ratio
  （以
  percentage
  表达）；
  50%
  duty
  cycle
  意味着
  signal
  在
  period
  的
  一
  半
  时间
  是
  high

.. code-block:: none

   |<--
   pulse
   -->|
   +--------------+
            +-
   |              |
            |
   +              +------------+
   |<-----------
   period
   -------->|

Zephyr
PWM
Driver
Model
