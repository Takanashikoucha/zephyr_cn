.. _zdsp_api:

数字信号处理（DSP）
###############################

.. contents::
    :local:
    :depth: 2

DSP API 提供了一种与架构无关的信号处理方式。
目前，该 API 可在任何架构上工作，但很可能未经优化。
各架构的状态如下：

============= =============
架构          状态
============= =============
ARC          已优化
ARM          已优化
ARM64        已优化
MIPS         未优化
POSIX        未优化
RISCV        未优化
RISCV64      未优化
SPARC        未优化
X86          未优化
XTENSA       未优化
============= =============

使用 zDSP
**********

zDSP 提供多种后端选项，会为应用自动选择。
默认情况下，包含 CMSIS 模块即可让所有
架构使用 zDSP API。可通过如下设置实现::

	CONFIG_CMSIS_DSP=y

如果应用需要一些额外的定制，可以
启用 :kconfig:option:`CONFIG_DSP_BACKEND_CUSTOM`，这意味着
应用负责提供 zDSP
库的实现。

为你的架构优化
********************************

如果你的架构显示为 ``Unoptimized``，可以添加新的
zDSP 后端以更好地支持它。为此，应
在 :file:`subsys/dsp/Kconfig` 中添加一个新的 Kconfig 选项，并附上所需的依赖项以及
``DSP_BACKEND`` Kconfig 选项的 ``default`` 设置。

接下来，实现应添加到 ``subsys/dsp/<backend>/``，
并在 :file:`subsys/dsp/CMakeLists.txt` 中链接。要添加架构特定的属性，
应将相应的 Kconfig 选项添加到 :file:`subsys/dsp/Kconfig`，并
使用它们更新 :file:`include/zephyr/dsp/dsp.h` 中的 ``DSP_DATA`` 和 ``DSP_STATIC_DATA``。

API 参考
*************

.. doxygengroup:: math_dsp

.. _subsys/dsp/Kconfig: https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dsp/Kconfig
.. _subsys/dsp/CMakeLists.txt: https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dsp/CMakeLists.txt
.. _include/zephyr/dsp/dsp.h: https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/dsp/dsp.h
