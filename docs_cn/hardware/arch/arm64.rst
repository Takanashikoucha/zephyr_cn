.. _arm64_developer_guide:

ARM64 开发者指南
#####################

带超时的等待（WFxT）
************************

Arm WFxT 扩展提供 WFET 和 WFIT 指令，它们接受绝对虚拟计数器值作为超时。
Zephyr 在运行时从 ``ID_AA64ISAR2_EL1`` 中的 ``WFxT`` 字段检测该扩展。
Arm64 架构代码可以用 ``is_wfxt_implemented()`` 查询此支持，
声明在 :zephyr_file:`include/zephyr/arch/arm64/lib_helpers.h` 中。

当 Arm 架构定时器实现 :c:func:`arch_busy_wait` 时，如果实现了 WFxT，
Arm64 路径对 :c:func:`k_busy_wait` 使用 WFET。它从 ``CNTVCT_EL0`` 计算
截止时间并重复 WFET 直到计数器达到该截止时间。循环是必需的，因为 WFET
被允许在超时前返回。没有 WFxT 的 CPU 使用计数器轮询。
参见 :zephyr_file:`drivers/timer/arm_arch_timer.c` 获取实现。

默认的 Arm64 :c:func:`arch_cpu_idle` 实现继续使用 WFI。带 Arm 架构定时器时，
内核的下一个超时在系统定时器中编程，其中断唤醒 CPU。保留该中断的同时
用 WFIT 替换 WFI 不会移除定时器编程或中断处理。避免中断需要对内核超时
记账、重新调度和 SMP 截止时间协调进行复杂更改，在没有证明收益的情况下
增加显著风险和维护成本。

.. _arm64_mmu_dt_regions:

基于设备树的 MMU 区域映射
************************************

在 ARM64 平台上，MMU 页表可以在编译时从设备树自动填充。
任何带有 ``compatible = "zephyr,memory-region"`` 且带有
``zephyr,memory-attr`` 属性的节点都会被架构启动代码转换为静态
``arm_mmu_region`` 条目——无需每个 SoC 的 ``mmu_regions.c`` 更改。

支持的内存属性
============================

只接受 **Normal**（普通）内存类型。Device（设备）内存（外设 MMIO）
必须通过 ``DEVICE_MMIO`` API 映射（参见 :ref:`device_model_api`）。

属性宏定义在
:zephyr_file:`include/zephyr/dt-bindings/memory-attr/memory-attr-arm64.h`
中，作为通用 ``DT_MEM_CACHEABLE`` 标志和架构特定子属性的可组合组合：

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - DT 宏
     - 描述
   * - ``DT_MEM_ARM64_MMU_NORMAL``
     - 普通可写回缓存（``DT_MEM_CACHEABLE | ATTR_ARM64_CACHE_WB``）
   * - ``DT_MEM_ARM64_MMU_NORMAL_NC``
     - 普通不可缓存（``0``）
   * - ``DT_MEM_ARM64_MMU_NORMAL_WT``
     - 普通可写通缓存（``DT_MEM_CACHEABLE``）

示例设备树 overlay
===========================

.. code-block:: devicetree

   #include <zephyr/dt-bindings/memory-attr/memory-attr.h>
   #include <zephyr/dt-bindings/memory-attr/memory-attr-arm64.h>

   / {
       soc {
           /* 可缓存共享内存池 */
           shm0: memory@42000000 {
               compatible = "zephyr,memory-region";
               reg = <0x0 0x42000000 0x0 0x1000>;
               zephyr,memory-region = "SHM0";
               zephyr,memory-attr = <DT_MEM_ARM64_MMU_NORMAL>;
           };

           /* 不可缓存 DMA 缓冲区 */
           dma_buf: memory@43000000 {
               compatible = "zephyr,memory-region";
               reg = <0x0 0x43000000 0x0 0x1000>;
               zephyr,memory-region = "DMA_BUF";
               zephyr,memory-attr = <DT_MEM_ARM64_MMU_NORMAL_NC>;
           };
       };
   };

每个区域用 ``MT_P_RW_U_NA | MT_DEFAULT_SECURE_STATE`` 与从
``zephyr,memory-attr`` 派生的内存类型组合映射。

转换表大小
=========================

每个映射的区域如果落在不同的 2 MB 边界上，需要一个额外的
Level 3（第三级）页表。如果添加新区域后启动静默挂起，
在板级或测试配置中增加 :kconfig:option:`CONFIG_MAX_XLAT_TABLES`：

.. code-block:: kconfig

   CONFIG_MAX_XLAT_TABLES=16

支持的属性组合
=================================

所有非设备属性组合都有效：``DT_MEM_CACHEABLE`` 通用位选择可缓存
与不可缓存，架构特定的 ``ATTR_ARM64_CACHE_WB`` 子位在可缓存时
选择写回与写通。
