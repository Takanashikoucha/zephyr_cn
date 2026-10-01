.. _i2s_api:

IC 间音频（I2S）总线
########################

概述
********

I2S（IC 间音频）API 支持标准 I2S 接口，以及常见的非标准扩展，例如 PCM 短/长帧同步（PCM Short/Long Frame Sync）和左/右对齐数据格式（Left/Right Justified Data Formats）。

Shell
*****

启用 :kconfig:option:`CONFIG_I2S_SHELL` 后，可使用 ``i2s`` shell 命令，无需编写应用代码即可在任意 I2S 控制器上输出生成的正弦测试音。它仅负责传输；请将其与 ``codec`` shell 命令配合使用，以便通过 codec 路由音频。

测试音命令分组在 ``i2s tone`` 之下：

* ``i2s tone start <device> [frequency_hz] [sample_rate] [bits]`` 在指定的 I2S 设备上启动立体声测试音。``frequency_hz`` 默认为 440 Hz，``sample_rate`` 默认为 48000 Hz，``bits`` 默认为 16（有效值为 16、24 和 32）。
* ``i2s tone stop`` 停止正在播放的测试音。
* ``i2s tone info`` 显示当前测试音流的状态。

例如，要输出一个 1 kHz、48 kHz、16 位的测试音：

.. code-block:: console

   uart:~$ i2s tone start i2s@0 1000 48000 16
   Streaming 1000 Hz tone on i2s@0 @ 48000 Hz, 16-bit stereo
   uart:~$ i2s tone info
   state    : streaming
   i2s dev  : i2s@0
   tone     : 1000 Hz
   rate     : 48000 Hz
   format   : 16-bit stereo, 64-frame blocks x 8
   uart:~$ i2s tone stop
   Stopped

shell 使用的发送（TX）缓冲由 :kconfig:option:`CONFIG_I2S_SHELL_BLOCK_FRAMES` 和 :kconfig:option:`CONFIG_I2S_SHELL_BLOCK_COUNT` 控制。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_I2S`
* :kconfig:option:`CONFIG_I2S_SHELL`

API 参考
*************

.. doxygengroup:: i2s_interface
