.. _zdsp_api:

Digital Signal Processing (DSP)
###############################

.. contents::
    :local:
    :depth: 2

DSP API 提供
architecture agnostic 的 signal processing 方式。
当前（API 在任何
architecture 上工作（但很可能不
optimized。各
architectures 的状态如下：

============ =============
Architecture Status
============ =============
ARC          Optimized
ARM          Optimized
ARM64        Optimized
MIPS         Unoptimized
POSIX        Unoptimized
RISCV        Unoptimized
RISCV64      Unoptimized
SPARC        Unoptimized
X86          Unoptimized
XTENSA       Unoptimized
============ =============

Using zDSP
**********

zDSP 提供
application 自动选择的
various backend options。默认（包含
CMSIS module 将启用
所有
architectures 使用
zDSP APIs。可通过设置::

	CONFIG_CMSIS_DSP=y

完成。

若 application 需
某些额外
customization（可
启用 :kconfig:option:`CONFIG_DSP_BACKEND_CUSTOM`（这意味着
application 负责
提供
zDSP
library 的
implementation。

Optimizing for your architecture
********************************

若你的
architecture 显示为
``Unoptimized``（可
添加
新
zDSP
backend 以
更好地
支持
它。为此（应
向
:file:`subsys/dsp/Kconfig` 添加
新
Kconfig
option（连同
所需
dependencies（并将
``DSP_BACKEND``
Kconfig
choice 的
``default`` 设置。

接下来（应
在
``subsys/dsp/<backend>/`` 添加
implementation（并在
:file:`subsys/dsp/CMakeLists.txt` link 入。要
添加
architecture-specific
attributes（其
相应
Kconfig
option 应
添加到
:file:`subsys/dsp/Kconfig`（并
用
它们
更新
:file:`include/zephyr/dsp/dsp.h` 的
``DSP_DATA`` 和
``DSP_STATIC_DATA``。

API Reference
*************

.. doxygengroup:: math_dsp

.. _subsys/dsp/Kconfig: https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dsp/Kconfig
.. _subsys/dsp/CMakeLists.txt: https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dsp/CMakeLists.txt
.. _include/zephyr/dsp/dsp.h: https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/dsp/dsp.h
