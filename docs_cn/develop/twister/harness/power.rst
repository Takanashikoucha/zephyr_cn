.. _twister_power_harness:

Power
#####

``power``
harness
用
来
测量
和
验证
电流
消耗。
它
与
'pytest'
集成
用
硬件
power
monitor
执行
自动化
数据
收集
和
分析。

harness
执行
以下
步骤：

1. 通过
   ``PowerMonitor``
   抽象
   接口
   初始化
   power
   监控
   设备
   （例如
   ``stm_powershield``）。
#. 为
   定义
   的
   ``measurement_duration``
   开始
   电流
   测量。
#. 收集
   原始
   电流
   波形
   数据。
#. 用
   peak
   检测
   算法
   基于
   power
   转换
   将
   数据
   分段
   为
   定义
   的
   执行
   阶段。
#. 用
   工具
   函数
   计算
   每个
   阶段
   的
   RMS
   电流
   值。
#. 将
   计算
   的
   值
   与
   用户
   定义
   的
   预期
   RMS
   值
   比较。

.. code-block:: yaml

   harness:
   power
   harness_config:
     fixture:
     pm_probe
     power_measurements:
       elements_to_trim:
       100
       min_peak_distance:
       40
       min_peak_height:
       0.008
       peak_padding:
       40
       measurement_duration:
       6
       num_of_transitions:
       4
       expected_rms_values:
       [56.0,
       4.0,
       1.2,
       0.26,
       140]
       tolerance_percentage:
       20

- **elements_to_trim**
  –
  测量
  开始
  时
  丢弃
  的
  样本
  数
  以
  消除
  噪声。
- **min_peak_distance**
  –
  检测
  到
  的
  电流
  peaks
  之间
  的
  最小
  距离
  （帮助
  检测
  不同
  转换）。
- **min_peak_height**
  –
  资格
  为
  peak
  的
  最小
  电流
  阈值
  （以
  安培
  计）。
- **peak_padding**
  –
  每个
  检测
  到
  的
  peak
  周围
  扩展
  的
  样本
  数。
- **measurement_duration**
  –
  记录
  电流
  数据
  的
  总
  时间
  （以
  秒
  计）。
- **num_of_transitions**
  –
  测试
  执行
  期间
  DUT
  中
  预期
  的
  power
  状态
  转换
  数。
- **expected_rms_values**
  –
  每个
  识别
  的
  执行
  阶段
  的
  目标
  RMS
  值
  （以
  毫安
  计）。
- **tolerance_percentage**
  –
  从
  预期
  RMS
  值
  的
  允许
  偏差
  百分比。
