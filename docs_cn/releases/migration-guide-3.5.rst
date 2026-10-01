:orphan:

.. _migration_3.5:

迁移到 Zephyr v3.5.0 的指南
################################

本文档描述了将应用程序从 Zephyr v3.4.0
迁移到 Zephyr v3.5.0 时必需或推荐的更改。

任何其他更改（与迁移应用程序不直接相关）
可在 :ref:`发布说明 <zephyr_3.5>` 中找到。

必需的更改
****************

内核
======

* 内核 :c:func:`k_mem_slab_free` 函数已更改其签名，
  现在接受 ``void *mem`` 指针而非 ``void **mem`` 双重指针。
  新签名不会立即触发编译器错误或警告，
  反而很可能在运行时导致无效内存访问。
  一个新的 ``_ASSERT`` 语句
  （你可以通过 :kconfig:option:`CONFIG_ASSERT` 启用）
  将检测你是否向该函数传递
  不属于内存块中内存的内存。

* :c:macro:`CONTAINER_OF` 现在执行类型检查。
  此前它非常常见地被误用
  为从 :c:struct:`k_work` 指针
  获取用户结构体，而不经过 :c:struct:`k_work_delayable`。
  这现在将导致构建错误，
  必须使用 :c:func:`k_work_delayable_from_work` 正确完成。

C 库
=========

* 大多数目标上使用的默认 C 库
  已从内置的最小 C 库改为 Picolibc。
  虽然两者都提供标准 C 库接口，
  且不应导致应用程序出现任何行为退化，
  但迁移到 Picolibc 时有几个副作用需要注意。

  * Picolibc 在受支持的地方
    启用线程局部存储
    （:kconfig:option:`CONFIG_THREAD_LOCAL_STORAGE`）。
    这改变了内核中一些内部操作，
    使用某些 TLS 变量来提升性能。
    Zephyr 将 TLS 变量放在为栈保留的内存中，
    因此每个线程的栈使用量将增加 8-16 字节。

  * Picolibc 使用与最小 C 库相同的 malloc 实现，
    但默认堆大小取决于使用的是哪个 C 库。
    使用最小 C 库时，默认堆为零字节，
    这意味着 malloc 将始终失败。
    使用 Picolibc 时，
    启用 :kconfig:option:`CONFIG_MMU` 或 :kconfig:option:`ARCH_POSIX` 时默认为 16kB，
    启用 :kconfig:option:`CONFIG_USERSPACE` 和
    :kconfig:option:`CONFIG_MPU_REQUIRES_POWER_OF_TWO_ALIGNMENT` 时默认为 2kB。
    对于所有其他目标，默认堆使用系统上所有剩余内存。
    你可以通过调整 :kconfig:option:`CONFIG_COMMON_LIBC_MALLOC_ARENA_SIZE`
    来更改这一点。

  * Picolibc 可以作为操作系统构建的一部分构建，
    也可以从工具链拉取。
    作为操作系统的一部分构建时，
    构建将增加约 1000 个文件。

  * 使用 Picolibc 的标准 C++ 库时，
    两者都必须来自工具链，
    因为标准 C++ 库依赖于 C 库 ABI。

  * Picolibc 移除了 ``-ffreestanding`` 编译器选项。
    这允许显著的编译器优化改进，
    但也意味着编译器现在将警告
    不符合 Zephyr 要求类型的 `main` 声明
    -- ``int main(void)``。

  * Picolibc 在 Zephyr 中支持四种不同的 printf/scanf 变体：
    'double'、'long long'、'integer' 和 'minimal'。
    'double' 提供完整的 printf 实现，
    支持十进制和十六进制格式的精确浮点数，
    完整的整数支持（包括 long long）、
    C99 整数大小说明符（j、z、t）和 POSIX 位置参数。
    'long long' 模式移除浮点支持，
    'integer' 移除 long long 支持，
    而 'minimal' 模式还移除对格式修饰符和位置参数的支持。
    将库作为模块构建允许对每个级别提供的功能集进行更细粒度的控制。

  * Picolibc 的默认浮点输入/输出代码
    大于最小 C 库版本
    （这对符合 C 语言对这些操作的“往返”要求是必需的）。
    如果你使用 :kconfig:option:`CONFIG_CBPRINTF_FP_SUPPORT`，
    你会看到内存使用量增加，
    除非你也禁用 :kconfig:option:`CONFIG_PICOLIBC_IO_FLOAT_EXACT`，
    该选项将 Picolibc 切换到更小但不精确的转换算法。
    这需要
    将 Picolibc 作为模块构建。

可选模块
================

以下模块已变为可选，
默认不再通过 `west update` 下载：

* ``chre``
* ``lz4``
* ``nanopb``
* ``psa-arch-tests``
* ``sof``
* ``tf-m-tests``
* ``tflite-micro``
* ``thrift``
* ``zscilib``

要重新启用它们，
使用 ``west config manifest.project-filter -- +<module name>`` 命令，
或使用 ``west config manifest.group-filter -- +optional`` 启用所有可选模块，
然后再次运行 ``west update``。

设备驱动程序和设备树
==============================

* ``zephyr,memory-region-mpu`` 已重命名为 ``zephyr,memory-attr``，
  其类型从 'enum' 移到 'int'。
  要实现无缝转换，这是设备树中必需的更改：

  .. code-block:: none

     - "RAM"         -> <( DT_MEM_ARM(ATTR_MPU_RAM) )>
     - "RAM_NOCACHE" -> <( DT_MEM_ARM(ATTR_MPU_RAM_NOCACHE) )>
     - "FLASH"       -> <( DT_MEM_ARM(ATTR_MPU_FLASH) )>
     - "PPB"         -> <( DT_MEM_ARM(ATTR_MPU_PPB) )>
     - "IO"          -> <( DT_MEM_ARM(ATTR_MPU_IO) )>
     - "EXTMEM"      -> <( DT_MEM_ARM(ATTR_MPU_EXTMEM) )>

* 设备依赖项（在某些地方被错误地称为“设备句柄”）
  现在是 :kconfig:option:`CONFIG_DEVICE_DEPS` 启用的可选功能。
  这意味着如果未启用该选项，则不再需要额外的链接器阶段。

* 在所有 STM32 ADC 上，
  不再可能使用 ADC 驱动程序读取传感器通道（Vref、Vbat 或温度）。
  应改用专门的传感器驱动程序。
  此更改源于 STM32F4 的限制，
  其中温度和 Vbat 的通道相同，
  且仅使用 ADC API 无法确定要测量什么。

* RAM 磁盘驱动程序已更改以支持多个实例
  以及使用设备树实例化。
  因此，Kconfig 选项 :kconfig:option:`CONFIG_DISK_RAM_VOLUME_SIZE`
  和 Kconfig 选项 :kconfig:option:`CONFIG_DISK_RAM_VOLUME_NAME` 已被移除，
  使用 RAM 磁盘的应用程序必须使用设备树实例化它，
  如下例所示：

  .. code-block:: devicetree

    / {
        ramdisk0 {
            compatible = "zephyr,ram-disk";
            disk-name = "RAM";
            sector-size = <512>;
            sector-count = <192>;
        };
    };

* :dtcompatible:`goodix,gt911`、:dtcompatible:`xptek,xpt2046`
  和 :dtcompatible:`hynitron,cst816s` 驱动程序
  已从 Kscan 转换为 Input，
  它们仍可通过添加 :dtcompatible:`zephyr,kscan-input` 节点
  与 Kscan 应用程序一起使用。

* ``zephyr,gpio-keys`` 绑定已合并到 :dtcompatible:`gpio-keys`，
  回调定义已从 ``INPUT_LISTENER_CB_DEFINE``
  重命名为 :c:macro:`INPUT_CALLBACK_DEFINE`。

* :dtcompatible:`ti,bq274xx` 驱动程序
  对容量和功率通道使用了不正确的单位，
  这些已得到修复，并从先前实现按 x1000 因子缩放，
  使用它们的任何应用程序都必须相应更改。

* SSD1306 显示驱动程序
  的配置选项现在
  可以通过设备树绑定
  :dtcompatible:`solomon,ssd1306fb`
  提供。
  以下 Kconfig 选项：
  ``CONFIG_SSD1306_DEFAULT``、
  ``CONFIG_SSD1306_SH1106_COMPATIBLE``
  和 ``CONFIG_SSD1306_REVERSE_MODE``
  已被移除。

  * 你可以在不做任何其他修改的情况下移除 ``CONFIG_SSD1306_DEFAULT``。

  * ``CONFIG_SSD1306_SH1106_COMPATIBLE`` 用于断言设备（兼容）SH1106。
    这已被专门的 dts compatible 声明取代。
    你可以更新现有的 sh1106 节点，
    将 ``compatible`` 指定从 :dtcompatible:`solomon,ssd1306fb`
    改为 :dtcompatible:`sinowealth,sh1106`。

  * ``CONFIG_SSD1306_REVERSE_MODE`` 现在使用
    设备树节点的 ``inversion-on`` 属性设置。

* 未实现 IRQ 相关操作的 GPIO 驱动程序
  现在必须向相关操作提供 ``NULL``：
  ``pin_interrupt_configure``、``manage_callback``、``get_pending_int``。
  公共 API 将在这些不可用时返回 ``-ENOSYS``，
  而不是 ``-ENOTSUP``。

* STM32 以太网驱动程序
  误用了 :c:func:`hwinfo_get_device_id`
  来生成 mac 地址的最后 3 个字节，
  导致使用同一批次的 SoC 时碰撞风险很高。
  这现已修复为使用唯一 ID（96 位）可用的整个熵范围。
  使用基于唯一 ID 的 mac 地址的设备
  将看到其 MAC 地址的最后 3 个字节因该更改而被修改。

* 在所有 STM32 上（除 F1x 和 F37x 系列外），
  两个新的必需属性已添加到 ADC，
  用于配置源时钟和预分频器。
  ``st,adc-clock-source`` 允许选择同步或异步时钟源。
  ``st,adc-prescaler`` 允许为所选时钟源设置预分频器的值。
  并非所有组合都被允许。
  请参阅相应的 RefMan 了解更多信息。
  选择异步时钟时，内核源时钟的选择
  在 ``clocks`` 节点中完成，
  与其他外设的做法相同，
  例如，为 STM32G0 选择 HSI16 作为时钟源：

  .. code-block:: devicetree

     &adc {
         clocks = <&rcc STM32_CLOCK_BUS_APB1_2 0x00100000>,
                  <&rcc STM32_SRC_HSI ADC_SEL(2)>;
       };

* 在带 LPC DMA 的 NXP 开发板上，
  DMA 控制器节点过去在开发板 DTS 中
  设置其 ``dma-channels`` 属性，
  作为配置驱动程序将分配的结构体数量的方式。
  这与 zephyr dma-controller 绑定不匹配，
  因此该属性现在已得到修复，
  并在 SoC 设备树定义中设置。
  下游开发板不应覆盖该属性，
  而应改用新的驱动程序 Kconfig
  :kconfig:option:`CONFIG_DMA_MCUX_LPC_NUMBER_OF_CHANNELS_ALLOCATED`。

* LPC55XXX 系列 SoC（除 LPC55S06 外）
  的默认主时钟已从以 144MHZ 运行的 XTAL32K
  更新为 PLL1 源。
  如果新的 kconfig 选项 :kconfig:option:`CONFIG_INIT_PLL1` 被禁用，
  则主时钟如先前一样多路复用到 FRO_HR。

* Kconfig 选项 ``CONFIG_GPIO_NCT38XX_INTERRUPT``
  已重命名为 :kconfig:option:`CONFIG_GPIO_NCT38XX_ALERT`。

* CAN 控制器时序 API 函数
  :c:func:`can_set_timing` 和 :c:func:`can_set_timing_data`
  在遇到对应 ``CAN_SJW_NO_CHANGE`` 的 SJW 值时
  （该值不再可用）
  不再回退到给定 CAN 控制器的设备树属性中设置的
  （重新）同步跳宽（SJW）值。
  因此调用者将需要填充 :c:struct:`can_timing` 中的 ``sjw`` 字段。
  为此，:c:func:`can_calc_timing` 和 :c:func:`can_calc_timing_data`
  函数现在自动计算适当的 SJW。
  计算出的 SJW 可在需要时被调用者覆盖。
  CAN 控制器 API 函数 :c:func:`can_set_bitrate`
  和 :c:func:`can_set_bitrate_data`
  现在也自动计算适当的 SJW，
  但其 SJW 不能被调用者覆盖。

* :c:struct:`isotp_msg_id` 中的
  CAN ISO-TP 消息配置
  已更改为使用以下标志而非位域：

  * :c:macro:`ISOTP_MSG_EXT_ADDR` 启用 ISO-TP 扩展寻址
  * :c:macro:`ISOTP_MSG_FIXED_ADDR` 启用 ISO-TP 固定寻址
  * :c:macro:`ISOTP_MSG_IDE` 使用扩展（29 位）CAN ID

  两个新标志 :c:macro:`ISOTP_MSG_FDF` 和 :c:macro:`ISOTP_MSG_BRS`
  已为 CAN FD 模式添加。

* 基于 NXP i.MX RT 的开发板
  现在应在
  使用 RT bootrom 的 DCD 时
  在开发板级别
  启用 :kconfig:option:`CONFIG_DEVICE_CONFIGURATION_DATA`，
  并在通过 SEMC 使用外部 SDRAM 时
  启用 :kconfig:option:`CONFIG_NXP_IMX_EXTERNAL_SDRAM`

* NXP i.MX RT11xx 系列 SNVS 引脚控制名称标识符
  已更新以与这些 SoC 的源数据匹配。
  引脚名称已添加后缀 ``dig``。
  例如，``iomuxc_snvs_wakeup_gpio13_io00``
  已重命名为 ``iomuxc_snvs_wakeup_dig_gpio13_io00``

电源管理
================

* 实现电源管理钩子的平台
  必须在 Kconfig 中显式选择 :kconfig:option:`CONFIG_HAS_PM`。
  这现在是 :kconfig:option:`CONFIG_PM` 的依赖项。
  在此更改之前，所有平台都可以启用 :kconfig:option:`CONFIG_PM`，
  因为提供了空的弱存根，然而这不再受支持。
  作为此更改的结果，电源管理钩子不再被定义为弱符号。

* 多个平台不再支持使用 :c:func:`pm_state_force` 关闭系统电源。
  必须使用新的 :c:func:`sys_poweroff` API。
  已迁移的平台包括 Nordic nRF、STM32、ESP32 和 TI CC13XX/26XX。
  新的 API 独立于 :kconfig:option:`CONFIG_PM`。
  它需要启用 :kconfig:option:`CONFIG_POWEROFF`，
  该选项依赖于 :kconfig:option:`CONFIG_HAS_POWEROFF`，
  一个由实现所需新钩子的平台选择的选项。

引导加载程序
==========

* :kconfig:option:`CONFIG_BOOTLOADER_SRAM_SIZE` 的默认值
  现在为 ``0``（此前为 ``16``）。
  使用 SRAM 一部分的引导加载程序
  应将该值设置为适当的大小。
  :github:`60371`

蓝牙
=========

* :c:struct:`bt_l2cap_server` 中 ``accept()`` 回调的签名
  已更改为
  ``int (*accept)(struct bt_conn *conn, struct bt_l2cap_server *server, struct bt_l2cap_chan **chan)``，
  添加了新的 ``server`` 参数，
  指向该回调所关联的 :c:struct:`bt_l2cap_server` 结构体实例。
  :github:`60536`

网络
==========

* 新的网络 Kconfig 选项 :kconfig:option:`CONFIG_NET_INTERFACE_NAME`
  默认为 ``y``。
  该选项允许用户为网络接口设置名称。
  在系统启动期间，会为网络接口分配默认名称，
  例如为第一个以太网网络接口分配 ``eth0``。
  该选项影响 ``SO_BINDTODEVICE`` BSD socket 选项的行为。
  如果 Kconfig 选项设置为 ``n``（即系统先前的工作方式），
  则分配给网络接口的设备名称被 ``SO_BINDTODEVICE`` socket 选项使用。
  如果 Kconfig 选项设置为 ``y``（当前默认值），
  则网络接口名称被 ``SO_BINDTODEVICE`` socket 选项使用。

* 以太网 PHY 设备树绑定
  已更新为使用标准 ``reg`` 属性
  而非自定义 ``address`` 属性来指定 PHY 地址。
  因此，MDIO 控制器节点现在需要
  ``#address-cells`` 和 ``#size-cells`` 属性。
  类似地，以太网 PHY 设备树节点和对应的驱动程序
  已更新为一致使用节点名称 ``ethernet-phy`` 而非 ``phy``。
  设备树和叠加层必须相应更新：

  .. code-block:: devicetree

     mdio {
         compatible = "mdio-controller";
         #address-cells = <1>;
         #size-cells = <0>;

         ethernet-phy@0 {
             compatible = "ethernet-phy";
             reg = <0>;
         };
     };

其他子系统
================

* ZBus 运行时观察者实现
  现在依赖 HEAP 内存而非内存块。
  因此，zbus 与运行时观察者相关的配置（kconfig）已更改。
  要保持你的运行时观察者代码正确工作，你需要：

  - 用布尔 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS`
    替换整数 ``CONFIG_ZBUS_RUNTIME_OBSERVERS_POOL_SIZE``；
  - 用 :kconfig:option:`CONFIG_HEAP_MEM_POOL_SIZE` 设置 HEAP 大小。

* zbus VDED 投递顺序已更改。
  检查 :ref:`文档 <zbus delivery sequence>`
  以验证其是否会影响你的代码。

* MCUmgr SMP 版本 2 错误代码条目已更改，
  因为与 shell_mgmt 中现有响应冲突。
  此前，这些错误有条目 ``ret``，但现在有条目 ``err``。
  ``smp_add_cmd_ret()`` 现在已弃用，
  应改用 :c:func:`smp_add_cmd_err`，
  ``MGMT_CB_ERROR_RET`` 现在已弃用，
  应改用 :c:enumerator:`MGMT_CB_ERROR_ERR`。
  树内模块的 SMP 版本 2 错误代码定义已更新，
  将 ``*_RET_RC_*`` 部分替换为 ``*_ERR_*``。

* MCUmgr SMP 版本 2 错误转换（到旧版 MCUmgr 错误代码）
  现在在函数处理程序中处理，
  通过在注册组时设置 :c:struct:`mgmt_group` 的
  ``mg_translate_error`` 函数指针。
  参见 :c:type:`smp_translate_error_fn` 了解函数详情。
  为 Zephyr 3.4 制作的任何 SMP 版本 2 处理程序
  需要更新，在组注册时包含这些转换函数。

ARM
===

* ARM SoC 初始化例程
  不再需要调用 `NMI_INIT()`。
  该宏调用已被移除，
  因为它没有做任何有用的事情。

RISC V
======

* :kconfig:option:`CONFIG_RISCV_MTVEC_VECTORED_MODE` Kconfig 选项
  已重命名为 :kconfig:option:`CONFIG_RISCV_VECTORED_MODE`。

推荐的更改
*******************

* 通过在 Kconfig 中直接选择
  :kconfig:option:`CONFIG_GIC_V1`、:kconfig:option:`CONFIG_GIC_V2`
  和 :kconfig:option:`CONFIG_GIC_V3`
  来设置 GIC 架构版本已被弃用。
  GIC 版本现在应通过向设备树中的 GIC 节点
  添加适当的 compatible 来指定，
  例如 :dtcompatible:`arm,gic-v2`。

* 使用 :kconfig:option:`CONFIG_NFCT_PINS_AS_GPIOS`
  将 NFCT 引脚配置为 GPIOs 的
  基于 Nordic nRF 的开发板
  应改为在设备树中设置新的 UICR ``nfct-pins-as-gpios`` 属性。
  它可以在开发板设备树文件中这样设置：

  .. code-block:: devicetree

     &uicr {
         nfct-pins-as-gpios;
     };

* 使用 :kconfig:option:`CONFIG_GPIO_AS_PINRESET`
  将复位 GPIO 配置为 nRESET 的
  基于 Nordic nRF 的开发板
  应改为在设备树中设置新的 UICR ``gpio-as-nreset`` 属性。
  它可以在开发板设备树文件中这样设置：

  .. code-block:: devicetree

     &uicr {
         gpio-as-nreset;
     };

* :kconfig:option:`CONFIG_MODEM_GSM_PPP` 调制解调器驱动程序已过时。
  相反，应使用新的 :kconfig:option:`CONFIG_MODEM_CELLULAR` 驱动程序。
  作为此更改的一部分，
  :kconfig:option:`CONFIG_GSM_MUX` 和 :kconfig:option:`CONFIG_UART_MUX`
  也被标记为已弃用。
  应改用新的调制解调器子系统
  :kconfig:option:`CONFIG_MODEM_CMUX` 和 :kconfig:option:`CONFIG_MODEM_PPP`。

* 设备驱动程序现在应被限制为
  ``PRE_KERNEL_1``、``PRE_KERNEL_2`` 和 ``POST_KERNEL`` 初始化级别。
  其他设备初始化级别，
  包括 ``EARLY``、``APPLICATION`` 和 ``SMP``，
  已被弃用，并将在未来版本中被移除。
  注意这些更改不适用于在 ``init.h`` API 上下文中使用的初始化级别，
  例如 :c:macro:`SYS_INIT`。

* 以下 CAN 控制器设备树属性现在已被弃用，
  改为使用 ``bus-speed``、``sample-point``、``bus-speed-data``
  和 ``sample-point-data`` 属性来指定初始 CAN 比特率：

  * ``sjw``
  * ``prop-seg``
  * ``phase-seg1``
  * ``phase-seg1``
  * ``sjw-data``
  * ``prop-seg-data``
  * ``phase-seg1-data``
  * ``phase-seg1-data``

* ``<zephyr/arch/arm/aarch32/cortex_a_r/cmsis.h>``
  和 ``<zephyr/arch/arm/aarch32/cortex_m/cmsis.h>``
  现在已被弃用，改为包含 ``<cmsis_core.h>``。
  新的头文件是 ``modules`` 目录中 CMSIS 胶水代码的一部分。

* 随机 API 头文件 ``<zephyr/random/rand32.h>``
  已被弃用，改为 ``<zephyr/random/random.h>``。
  旧的头文件将在未来版本中被移除，应避免使用它。
