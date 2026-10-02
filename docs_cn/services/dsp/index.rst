.. _zdsp_api:

数字信号处理（DSP）
###############################

.. contents::
    :local:
    :depth: 2

DSP API 提供了一种架构无关的信号处理方式。
当前，该 API 可在任何架构上工作，但很可能未
做优化。各架构的状态如下：

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

zDSP 提供多种后端选项，由应用自动选择。
默认情况下，包含 CMSIS 模块将启用所有
架构使用 zDSP API。可通过设置::

	CONFIG_CMSIS_DSP=y

完成。

若应用需要某些额外
自定义，可
启用 :kconfig:option:`CONFIG_DSP_BACKEND_CUSTOM`，这意味着
应用负责
提供
zDSP
库的
实现。

为你的架构做优化
********************************

若你的
架构显示为
``未优化``，可
添加
新的
zDSP
后端以
更好地
支持
它。为此，应
向
:file:`subsys/dsp/Kconfig` 添加
新的
Kconfig
选项，连同
所需
依赖项，并将
``DSP_BACKEND``
Kconfig
choice 的
``default`` 设置。

接下来，应
在
``subsys/dsp/<backend>/`` 添加
实现，并在
:file:`subsys/dsp/CMakeLists.txt` 链接入。要
添加
架构特定
属性，其
相应
Kconfig
选项应
添加到
:file:`subsys/dsp/Kconfig`，并
用
它们
更新
:file:`include/zephyr/dsp/dsp.h` 的
``DSP_DATA`` 和
``DSP_STATIC_DATA``。

API 参考
*************

.. doxygengroup:: math_dsp

.. _subsys/dsp/Kconfig: https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dsp/Kconfig
.. _subsys/dsp/CMakeLists.txt: https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/dsp/CMakeLists.txt
.. _include/zephyr/dsp/dsp.h: https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/dsp/dsp.h
