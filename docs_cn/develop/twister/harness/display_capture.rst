.. _twister_display_capture_harness:

Display
capture
###############

``display_capture``
harness
用
来
用
相机
捕获
并
分析
显示
输出
验证
显示
驱动
功能。
它
与
pytest
集成
用
视频
fingerprints
执行
自动化
视觉
测试。

.. figure::
   figures/twister_display_capture_success.webp
   :align:
   center
   :alt:
   A
   window
   showing
   a
   camera
   preview
   of
   a
   device
   display
   with
   colored
   blocks
   in
   the
   corners,
   with
   a
   text
   overlay
   indicating
   a
   successful
   test
   match.

   窗口
   在
   "compare"
   运行
   中
   显示
   其中
   fingerprint
   与
   参考
   90%
   匹配。

硬件
设置
=============

display
capture
harness
需要：

- UVC
  兼容
  相机
  至少
  2
  兆
  像素
  （例如
  1080p
  分辨率）
- 遮光
  外壳
  或
  黑色
  窗帘
  确保
  一致
  的
  照明
- PC
  主机
  带
  相机
  连接
  用于
  捕获
  显示
  输出
- DUT
  连接
  到
  同一
  个
  PC
  用于
  烧录
  和
  串口
  控制台
  访问

配置
=============

harness
用
一
个
YAML
配置
文件
定义
相机
设置、
测试
参数
和
视频
signature
分析
选项。
典型
配置
显示
在
下面：

.. code-block:: yaml
   :caption:
   display_config.yaml

   case_config:
     device_id:
     0
     res_x:
     1280
     res_y:
     720
     fps:
     30
