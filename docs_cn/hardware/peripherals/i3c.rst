.. _i3c_api:

I3C（Improved Inter-Integrated Circuit，改进型集成电路总线）
###########################################

I3C（Improved Inter-Integrated Circuit）是一种双信号共享外设接口总线。
总线上的设备可以扮演两种角色：
作为发起事务并控制时钟的“控制器”，
或作为响应事务命令的“目标”。

目前，该 API 基于 `I3C Specification`_ 版本 1.1.1。

.. contents::
    :local:
    :depth: 2

.. _i3c-controller-api:

I3C 控制器 API
******************

当 I3C 控制器控制总线（特别是起始和停止条件以及时钟）时，
使用 Zephyr 的 I3C 控制器 API。
这是最常用的模式，用于与传感器等 I3C 目标设备交互。

由于 I3C 的特性，总线上的设备在上电时可能没有地址。
因此，I3C 控制器需要执行额外的动态地址分配。
为此，控制器需要维护独立的数据结构来跟踪设备状态。
这可以在构建时完成，例如为 I3C 和 I\ :sup:`2`\ C 设备
创建设备描述符数组：

.. code-block:: c

   static struct i3c_device_desc i3c_device_array[] = I3C_DEVICE_ARRAY_DT_INST(inst);
   static struct i3c_i2c_device_desc i2c_device_array[] = I3C_I2C_DEVICE_ARRAY_DT_INST(inst);

宏 :c:macro:`I3C_DEVICE_ARRAY_DT_INST` 和
:c:macro:`I3C_I2C_DEVICE_ARRAY_DT_INST` 是辅助宏，
用于创建对应 I3C 控制器下设备树节点的设备描述符数组。

以下是设备驱动初始化函数中初始化 I3C 控制器和 I3C 总线
的一般步骤：

#. 初始化 I3C 控制器设备驱动实例的数据结构。
   可以使用 :c:macro:`DEVICE_DT_INST_DEFINE` 等常规设备定义宏，
   并提供作为宏参数的初始化函数。

   * :c:struct:`i3c_addr_slots` 和 :c:struct:`i3c_dev_list`
     是用于辅助地址分配和设备列表管理的结构体。
     如果使用，需要通过调用 :c:func:`i3c_addr_slots_init` 初始化。
     这两个结构体也可以与各种辅助函数一起使用。

   * 如控制器驱动需要，初始化设备描述符。

#. 初始化硬件，包括但不限于：

   * 设置引脚复用和方向。

   * 设置控制器的时钟。

   * 开启硬件电源。

   * 配置硬件（例如 SCL 时钟频率）。

#. 执行总线初始化。有一个通用辅助函数
   :c:func:`i3c_bus_init`，它执行以下步骤。
   如果控制器在总线初始化期间不需要任何特殊处理，可以使用此函数。

   #. 执行 ``RSTDAA`` 重置已连接设备的动态地址。
      如果某些已连接设备已被分配地址，
      簿记数据结构中没有这些记录的痕迹，例如在上电时。
      因此，重置并分配新地址是个好主意。

   #. 执行 ``DISEC`` 禁用来自设备的事件。

   #. 执行 ``SETDASA``，使用设备的静态地址分配动态地址（如果希望）。

      * ``SETAASA`` 可能不为所有已连接设备支持
        将静态地址分配为动态地址。

      * BCR 和 DCR 需要单独获取，以填充
        I3C 目标设备描述符结构体中的相关字段。

   #. 执行 ``ENTDAA`` 开始动态地址分配（如果仍有未分配地址的设备）。

      * 如果有设备正在等待地址，它会返回其 Provisioned ID、BCR 和 DCR。
        将接收到的 Provisioned ID 与已注册的 I3C 设备列表匹配。

        * 如果匹配，分配一个地址
          （如果尚未执行 ``SETDASA``，则使用所述静态地址，或使用空闲地址）。

          * 同时，设置设备描述符结构体中的 BCR 和 DCR 字段。

        * 如果不匹配，根据策略，可以分配一个空闲地址，
          或者设备驱动可以停止分配过程并报错。

          * 注意 I3C API 需要设备描述符才能工作。
            没有设备描述符的设备无法通过 API 访问。

      * 如果没有已连接设备需要 DAA，可以跳过此步骤。

   #. 以下步骤可选但强烈建议执行：

      * 执行 ``GETMRL`` 和 ``GETMWL`` 获取最大读取/写入长度。

      * 执行 ``GETMXDS`` 获取最大读取/写入速度和最大读取周转时间。

      * 辅助函数 :c:func:`i3c_bus_init` 会获取
        BCR、DCR、MRL 和 MWL 等基本设备信息。

   #. 执行 ``ENEC`` 重新启用来自设备的事件。

      * 辅助函数 :c:func:`i3c_bus_init` 仅重新启用 hot-join 事件。
        IBI 事件应仅在启用某设备的 IBI 时才启用。

带内中断（IBI）
=======================

如果目标设备可以生成带内中断（IBI），
需要让控制器知晓。

* 使用 :c:func:`i3c_ibi_enable` 启用目标设备的 IBI。

  * 某些控制器硬件具有 IBI 槽位，需要编程，
    以便控制器能识别来自特定目标设备的传入 IBI。

    * 如果硬件具有 IBI 槽位，:c:func:`i3c_ibi_enable`
      需要编程这些 IBI 槽位。

    * 注意控制器上通常只有有限的 IBI 槽位，
      因此此操作可能失败。

  * 驱动中的实现还应发送 ``ENEC`` 命令
    以启用该目标设备的中断。

* 使用 :c:func:`i3c_ibi_disable` 禁用目标设备的 IBI。

  * 如果控制器硬件使用 IBI 槽位，这会移除
    槽位中该目标设备的描述。

  * 驱动中的实现还应发送 ``DISEC`` 命令
    以禁用该目标设备的中断。

设备树
===========

以下是在设备树中定义 I3C 控制器的示例：

.. code-block:: devicetree

   i3c0: i3c@10000 {
           compatible = "vendor,i3c";

           #address-cells = <0x3>;
           #size-cells = <0x0>;

           reg = <0x10000 0x1000>;
           interrupts = <0x1F 0x0>;

           pinctrl-0 = <&pinmux-i3c>;
           pinctrl-names = "default";

           i2c-scl-hz = <400000>;

           i3c-scl-hz = <12000000>;

           status = "okay";

           i3c-dev0: i3c-dev0@420000ABCD12345678 {
                   compatible = "vendor,i3c-dev";

                   reg = <0x42 0xABCD 0x12345678>;

                   status = "okay";
           };

           i2c-dev0: i2c-dev0@380000000000000050 {
                   compatible = "vendor-i2c-dev";

                   reg = <0x38 0x0 0x50>;

                   status = "okay";
           };
   };

I3C 设备
-----------

对于 I3C 设备，``reg`` 属性有 3 个元素：

* 第一个是设备的静态地址。

  * 如果未使用静态地址，可以为零。
    地址将在 DAA（动态地址分配）期间分配。

  * 如果非零且未设置 ``assigned-address`` 属性，
    这将成为发出 SETDASA
    （从静态地址设置动态地址）后的设备地址。

* 第二个元素是 Provisioned ID（PID）的高 16 位，
  包含左移 1 的制造商 ID。
  这是 48 位 Provisioned ID 的位 33-47（零基）。

  * 必须非零。第二个元素为零会将节点标记为
    I\ :sup:`2`\ C 设备（如下所述），因此辅助宏
    会为其创建传统 I\ :sup:`2`\ C 描述符而非 I3C 描述符。
    即使设备通过 SETDASA 寻址且 PID 否则未使用，也应指定 PID。

* 第三个元素包含 Provisioned ID 的低 32 位，
  是部件 ID（左移 16，PID 的位 16-31）
  和实例 ID（左移 12，PID 的位 12-15）的组合。

注意，单元地址（``@`` 之后的部分）必须与 ``reg`` 属性完全匹配，
每个元素视为 32 位整数，组合形成一个 96 位整数。
这是正确生成设备树宏所必需的。

I\ :sup:`2`\ C 设备
----------------------

对于设备驱动支持在 I3C 总线下工作的 I\ :sup:`2`\ C 设备，
设备节点可以描述为 I3C 控制器的子节点。
如果设备驱动编写为仅与 I\ :sup:`2`\ C 控制器工作，
则如下所述在 I\ :sup:`2`\ C 虚拟控制器下定义节点。
否则，``reg`` 属性与 I3C 设备类似，
有 3 个元素：

* 第一个是设备的静态地址。这必须是有效地址，
  因为 I\ :sup:`2`\ C 设备不支持动态地址分配。

* 第二个元素始终为零。

  * 这由各种辅助宏用于确定设备树条目
    是否对应 I\ :sup:`2`\ C 设备。

* 第三个元素是 LVR（Legacy Virtual Register，传统虚拟寄存器）：

  * bit[31:8] 未使用。

  * bit[7:5] 是 I\ :sup:`2`\ C 设备索引：

    * 索引 ``0``

      * I3C 设备具有 50 ns 尖峰滤波器，
        不受 SCL 上高频影响。

    * 索引 ``1``

      * I\ :sup:`2`\ C 设备没有 50 ns 尖峰滤波器，
        但可以与 SCL 上高频工作。

    * 索引 ``2``

      * I3C 设备没有 50 ns 尖峰滤波器，
        且不能与 SCL 上高频工作。

  * bit[4] 是 I\ :sup:`2`\ C 模式指示器：

    * ``0`` 是 FM+ 模式。

    * ``1`` 是 FM 模式。

与 I3C 设备类似，单元地址必须与 ``reg`` 属性完全匹配，
每个元素视为 32 位整数，组合形成一个 96 位整数。

I3C 设备的设备驱动
==============================

I3C 控制器 API 的所有传输函数都需要使用
设备描述符 :c:struct:`i3c_device_desc`。
该结构体包含 I3C 设备的运行时信息，
例如动态地址、BCR、DCR、MRL 和 MWL。
因此，I3C 设备的设备驱动应使用
:c:func:`i3c_device_find` 从控制器获取
指向该设备描述符的指针。
该函数接受类型为 :c:struct:`i3c_device_id` 的 ID 参数用于匹配。
返回的指针可用于后续对控制器的 API 调用。

I3C 总线下的 I\ :sup:`2`\ C 设备
====================================

由于 I3C 向后兼容 I\ :sup:`2`\ C，
如果控制器设备驱动实现了 I2C API，
I3C 控制器 API 可以在不修改的情况下容纳 I2C API 调用。
这的优势是可以直接使用现有 I2C 设备，
无需修改其设备驱动。
然而，由于 I3C 控制器 API 基于设备描述符工作，
任何对 I2C API 的调用都需要从 I2C 设备地址
查找对应的设备描述符。
这给任何 I2C API 调用增加了一点处理成本。

另一方面，设备驱动可以扩展为通过 I3C 控制器 API
利用原生 I2C 设备支持。
在设备初始化期间，需要调用 :c:func:`i3c_i2c_device_find`
以获取设备描述符的指针。
该指针可用于后续 API 调用。

注意，使用上述任一方法时，
I2C 设备的设备树节点必须根据 I3C 标准声明：

I\ :sup:`2`\ C 虚拟控制器设备驱动提供一种
接口 I3C 总线上 I\ :sup:`2`\ C 设备的方式，
其中关联的设备驱动可以原样使用而无需修改。
这需要在设备树中添加一个中间节点：

.. code-block:: devicetree

   i3c0: i3c@10000 {
           <... I3C controller related properties ...>
           <... Nodes of I3C devices, if any ...>

           i2c-dev0: i2c-dev0@420000000000000050 {
                   compatible = "vendor-i2c-dev";

                   reg = <0x42 0x0 0x50>;

                   status = "okay";
           };
   };

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_I3C`
* :kconfig:option:`CONFIG_I3C_USE_IBI`
* :kconfig:option:`CONFIG_I3C_IBI_MAX_PAYLOAD_SIZE`
* :kconfig:option:`CONFIG_I3C_CONTROLLER_INIT_PRIORITY`

API 参考
*************

.. doxygengroup:: i3c_interface
.. doxygengroup:: i3c_ccc
.. doxygengroup:: i3c_addresses
.. doxygengroup:: i3c_target_device

.. _I3C Specification: https://www.mipi.org/specifications/i3c-sensor-specification
