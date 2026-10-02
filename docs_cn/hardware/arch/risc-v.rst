Zephyr 在 RISC-V 处理器上的支持状态
##########################################

概述
********

本页介绍 Zephyr 在 RISC-V 处理器上的当前支持状态。
目前，已支持部分开发板，以及 QEMU 支持，
还支持 neorv32 和 litex_vexriscv 等一些 FPGA 实现。

Zephyr 的支持内容包括 PMP、:ref:`用户模式<usermode_api>`、若干
ISA 扩展以及 :ref:`半主机<semihost_guide>`。

用户模式与 PMP 支持
**************************

当平台支持物理内存保护（PMP）时，
在 Zephyr 中启用它即可选择支持用户空间和栈保护。

ISA 扩展
**************

可以在 Zephyr 中设置某一平台可用的 ISA 扩展（RV32/64I(E)MAFD(G)QC），
方法是设置相应的 ``CONFIG_RISCV_ISA_*`` kconfig。
更多信息请参阅 :file:`arch/riscv/Kconfig.isa`。

请注意，Zephyr SDK 工具链可能并未为所有组合提供支持。

监管者模式（S 模式）
************************

当启用 :kconfig:option:`CONFIG_RISCV_S_MODE` 时，Zephyr 内核
运行在 RISC-V 监管者模式（S 模式）而非机器模式（M 模式）。
这遵循应用类操作系统所使用的标准 RISC-V 特权架构，
也是 MMU 支持所必需的。

树内的一个最小 M 模式运行时（``arch/riscv/core/sbi.S``）充当固件。
它在启动时执行从 M 模式到 S 模式的初始切换，
并通过 RISC-V 监管者二进制接口（SBI）处理 S 模式的请求：

- **启动流程**：M 模式配置 PMP、``medeleg``、``mideleg``、
  ``mcounteren`` 和 ``mtvec``，当存在 Zkr 扩展时通过
  ``mseccfg`` 授予 S 模式对 ``seed`` CSR 的访问权限，
  然后通过 ``mret`` 切换到 S 模式。
- **定时器**：机器定时器中断（MTIP）被转发为 S 模式的
  监管者定时器中断（STIP）。S 模式通过 SBI 的 ``TIME`` 扩展
  （``sbi_set_timer``）编程下一个定时器截止时间。
- **ecall**：S 模式的 ecall（异常原因 9）通过 ``medeleg``
  路由到 M 模式运行时；其他所有异常和中断都委托给 S 模式。
  详见下文 :ref:`riscv-smode-ecall-constraint`。

无需外部固件；树内运行时是自包含的。

已知限制
=================

**PLIC 外部中断**：PLIC 驱动始终为 hart 0 配置 M 模式上下文。
在 S 模式下正确的上下文是监管者上下文，
因此由 PLIC 投递的外部中断（UART、GPIO、SPI、I2C 等）
无法到达 CPU。定时器中断不受影响，因为它由 M 模式运行时
通过 ``sip.STIP`` 直接转发，绕过了 PLIC。

.. _riscv-smode-ecall-constraint:

S 模式 ecall 约束
=======================

在 M 模式下，Zephyr 将 ``ecall`` 指令用作内核内部自陷入：
因为内核无条件地拥有 M 模式，``ecall`` 触发异常原因 11
（M 模式 ecall），由 ``_isr_wrapper`` 将其分派到所请求的
内核服务（致命错误、``irq_offload``、上下文切换）。

在 S 模式下该机制不可用。来自 S 模式的 ``ecall`` 始终触发
原因 9，而原因 9 **并未**委托给 S 模式（``medeleg`` 第 9 位 = 0），
因为它必须到达 M 模式的 SBI 处理程序——这是 S 模式请求
M 模式服务的唯一途径，例如通过 ``sbi_set_timer`` 编程定时器。
``medeleg`` 位无法按寄存器值进行区分：将原因 9 委托给 S 模式
会破坏 SBI；将其保留在 M 模式则使原因 9 无法用于内核内部用途。

S 模式移植的实际规则是：

   ``ecall`` 为 SBI 接口所保留。任何在 M 模式下使用 ``ecall``
   的内核机制都必须改用直接的 S 模式路径重新实现。

本移植中的两个具体示例：

- :c:macro:`ARCH_EXCEPT`（``include/zephyr/arch/riscv/error.h``）——
  它不再发出 ``ecall`` 以通过 ``_isr_wrapper`` 触发致命错误入口，
  而是直接调用 :c:func:`z_riscv_fatal_error`。

- ``arch_irq_offload``（``arch/riscv/core/irq_offload.c``）——
  它不再发出 ``ecall`` 以进入 ``_isr_wrapper`` 的 ``do_irq_offload``
  路径，而是直接模拟 ISR 上下文：关闭中断、递增 ``nested``、
  调用例程、递减 ``nested``、重新启用中断，然后调用
  :c:func:`z_reschedule_unlocked` 处理在例程内部变为就绪状态的线程。

将 `OpenSBI`_ 等外部 SBI 实现作为 West 模块使用的支持
留作后续工作。

SMP 支持
***********

RISC-V 上的 SMP 同时支持 QEMU 虚拟化平台和基于硬件的平台。
要测试 SMP 支持，QEMU 平台可以使用 :zephyr:board:`qemu_riscv32`
或 :zephyr:board:`qemu_riscv64`，基于硬件的平台则可以使用
:zephyr:board:`beaglev_fire` 或 :zephyr:board:`mpfs_icicle`。

.. _OpenSBI: https://github.com/riscv-software-src/opensbi
