.. _audio_dmic_api:

数字麦克风（DMIC）
#########################

概述
********

音频 DMIC 接口提供对数字麦克风的访问。

数字麦克风通常输出 PDM（脉冲密度调制）位流，而不是模拟音频。PDM 使用 1 位高速信号，音频幅度由随时间变化的 1 和 0 的密度来表示。

由于应用通常消费 PCM（脉冲编码调制）采样数据而非原始 PDM 数据，DMIC 控制器会将麦克风流转换为 PCM 音频。该转换包括滤波和抽取：滤波用于去除被整形到 PDM 流中的高频噪声，抽取则将位流速率降低到所需的 PCM 采样率。

从 Zephyr 的角度看，DMIC 设备是一种音频采集外设。应用配置麦克风和控制器，启动采集，并从驱动程序读取 PCM 缓冲区。

关键概念
************

DMIC API 将配置分为三个部分，与采集路径一一对应：

#. 麦克风在 PDM 侧如何被驱动，
#. 传入的 PDM 通道如何排列，以及
#. 转换后的 PCM 采样如何交付给应用。

这些部分组合在 :c:struct:`dmic_cfg` 结构中，并传递给 :c:func:`dmic_configure`。

**PDM 输入/输出配置**（:c:member:`dmic_cfg.io`）
  描述麦克风接口的电气与时序要求，例如支持的 PDM 时钟频率范围、占空比，以及任何控制器特定的信号极性设置。

**通道配置**（:c:member:`dmic_cfg.channel`）
  告诉驱动程序哪个物理 PDM 控制器、以及左或右麦克风通道应作为 PCM 输出中的每个逻辑音频通道出现。它还声明应用希望使用的通道数和流数。

**PCM 流配置**（:c:member:`dmic_cfg.streams`）
  定义驱动程序输出的 PCM 数据，包括采样率、采样宽度、块大小，以及用于为每个启用的流分配接收缓冲区的 :c:struct:`k_mem_slab`。

典型应用流程
========================

DMIC API 的典型使用流程如下：

#. 获取 DMIC 设备，通常从设备树获取。
#. 用输入/输出、通道和流设置填充 :c:struct:`dmic_cfg` 结构。关于如何定义 DMIC 用于存储所接收 PCM 数据的内存缓冲区，更多细节见下文 :ref:`dmic_buffering` 一节。
#. 调用 :c:func:`dmic_configure`，传入配置结构。
#. 使用 :c:func:`dmic_trigger` 配合 :c:enumerator:`DMIC_TRIGGER_START` 启动采集。
#. 使用 :c:func:`dmic_read` 获取 PCM 数据。
#. 根据需要使用其他触发命令停止、暂停或重置采集。

.. _dmic_buffering:

缓冲区
=========

接收到的 PCM 数据通过由驱动程序持有的缓冲区返回。应用通过每个已配置的 PCM 流所引用的 :c:struct:`k_mem_slab` 提供后备内存。

一种常见模式是静态声明该内存块：

.. code-block:: c
  :caption: 为 PCM 接收缓冲区静态声明内存块

   K_MEM_SLAB_DEFINE_STATIC(mem_slab,
                           SAMPLES_PER_BUFFER * sizeof(int16_t),
                           BUFFER_COUNT,
                           sizeof(void *));

在此示例中，每个 slab 块存储一个 PCM 缓冲区，``BUFFER_COUNT`` 决定在应用使用 :c:func:`dmic_read` 读取之前内部可以排队的缓冲区数量。

Shell 命令
**************

启用 :kconfig:option:`CONFIG_AUDIO_DMIC_SHELL` 后，可使用一组 ``dmic`` 命令。它们允许交互式地从 DMIC 设备采集音频，而无需编写专门的应用。

每个子命令以 DMIC 设备名作为第一个参数，可选地后跟音频采集参数（采样率、通道数、PCM 采样宽度）。

可用的子命令如下：

``dmic read <device> [<count> [<rate_hz> [<channels> [<pcm_width>]]]]``
  采集 ``count`` 个音频块，并打印每个通道的峰值电平。``count`` 默认为 5；每个块为 50 ms 的音频。

``dmic vu <device> [<rate_hz> [<channels> [<pcm_width>]]]``
  显示一个实时的、带颜色编码的电平表，具有峰值保持和削波指示，每个通道一条电平条。运行直到按下任意键为止。

``dmic dump <device> [<seconds> [<rate_hz> [<channels> [<pcm_width>]]]]``
  采集 ``seconds`` 秒的音频，并以 base64 编码的原始 PCM 形式打印出来，同时给出在主机上解码并回放所需的命令。时长默认为 2 秒。

内置帮助（例如 ``dmic read --help``）会列出各参数及其默认值。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_AUDIO_DMIC`
* :kconfig:option:`CONFIG_AUDIO_DMIC_SHELL`

API 参考
*************

.. doxygengroup:: audio_dmic_interface
