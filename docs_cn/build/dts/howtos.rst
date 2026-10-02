.. _dt-howtos:

设备树 HOWTO
#################

本页提供使用设备树完成事情的
分步建议。

.. tip:: 故障排除建议见 :ref:`dt-trouble`。

.. _get-devicetree-outputs:

获取设备树与生成的头文件
****************************************

开发板的设备树（:ref:`BOARD.dts <devicetree-in-out-files>`）
通过 ``#include`` 预处理器指令引入
通用节点定义。这至少
包括 SoC 的 ``.dtsi``。确定设备树内容的
一种方式是打开这些文件，例如查看
``dts/<ARCH>/<vendor>/<soc>.dtsi``，但这可能耗时。

如果你只想查看开发板的"最终"设备树，
构建一个应用并打开构建目录中的 :file:`zephyr.dts` 文件。

.. tip::

   你可以构建 :zephyr:code-sample:`hello_world` 查看开发板的"基础"设备树
   （没有来自 :ref:`覆盖文件 <dt-input-files>` 的任何额外更改）。

例如，使用 :zephyr:board:`qemu_cortex_m3` 开发板构建
:zephyr:code-sample:`hello_world`：

.. code-block:: sh

   # --cmake-only 这里只是强制运行 CMake，
   # 跳过构建过程以节省时间。
   west build -b qemu_cortex_m3 samples/hello_world --cmake-only

你可以将 ``qemu_cortex_m3`` 更改为匹配你的开发板。

CMake 如下打印输入和输出文件位置：

.. code-block:: none

   -- Found BOARD.dts: .../zephyr/boards/arm/qemu_cortex_m3/qemu_cortex_m3.dts
   -- Generated zephyr.dts: .../zephyr/build/zephyr/zephyr.dts
   -- Generated devicetree_generated.h: .../zephyr/build/zephyr/include/generated/zephyr/devicetree_generated.h

:file:`zephyr.dts` 文件是 DTS 格式的最终设备树。

:file:`devicetree_generated.h` 文件是对应的生成头文件。

这些文件的细节见 :ref:`devicetree-in-out-files`。

.. _dt-get-device:

从设备树节点获取 struct device
******************************************

编写 Zephyr 应用时，你经常想获取
对应设备树节点的驱动级
:ref:`struct device <device_model_api>`。

例如，对于此设备树片段，你可能想获取
``serial@40002000`` 的 struct device：

.. code-block:: devicetree

   / {
           soc {
                   serial0: serial@40002000 {
                           status = "okay";
                           current-speed = <115200>;
                           /* ... */
                   };
           };

           aliases {
                   my-serial = &serial0;
           };

           chosen {
                   zephyr,console = &serial0;
           };
   };

先为你感兴趣的设备
创建一个 :ref:`节点标识符 <dt-node-identifiers>`。
有不同的方式这样做；选择最适合
你需求的方式。以下是一些示例：

.. code-block:: c

   /* Option 1: by node label */
   #define MY_SERIAL DT_NODELABEL(serial0)

   /* Option 2: by alias */
   #define MY_SERIAL DT_ALIAS(my_serial)

   /* Option 3: by chosen node */
   #define MY_SERIAL DT_CHOSEN(zephyr_console)

   /* Option 4: by path */
   #define MY_SERIAL DT_PATH(soc, serial_40002000)

有了节点标识符后，有两种方式继续。
获取设备的
一种方式是使用 :c:macro:`DEVICE_DT_GET`：

.. code-block:: c

   const struct device *const uart_dev = DEVICE_DT_GET(MY_SERIAL);

   if (!device_is_ready(uart_dev)) {
           /* Not ready, do not use */
           return -ENODEV;
   }

:c:macro:`DEVICE_DT_GET` 有诸如
:c:macro:`DEVICE_DT_GET_OR_NULL`、:c:macro:`DEVICE_DT_GET_ONE` 或
:c:macro:`DEVICE_DT_GET_ANY` 之类的变体。此惯用法在
构建时获取设备指针，这意味着没有运行时开销。
如果你想将设备指针存储为配置数据，
此方法有用。但由于
设备可能未初始化或初始化失败，
在将设备传递给任何 API 函数之前
必须验证设备已就绪
（:c:func:`device_get_binding` 会为你做此检查）。

在某些情况下，设备无法在构建时确定，
例如它取决于
shell 应用中的用户输入。在这种情况下，
你可以将 :c:func:`device_get_binding` 与设备
名组合来获取
``struct device``：

.. code-block:: c

   const char *dev_name = /* TODO: insert device name from user */;
   const struct device *uart_dev = device_get_binding(dev_name);

然后你可以使用 :ref:`uart_api` API 函数（如
:c:func:`uart_configure`）使用 ``uart_dev``。
类似代码可用于其他设备类型；只需
确保你使用设备的正确 API。

如果遇到问题，见 :ref:`dt-trouble`。
首先要检查的
是节点具有 ``status = "okay"``，如下所示：

.. code-block:: c

   #define MY_SERIAL DT_NODELABEL(my_serial)

   #if DT_NODE_HAS_STATUS(MY_SERIAL, okay)
   const struct device *const uart_dev = DEVICE_DT_GET(MY_SERIAL);
   #else
   #error "Node is disabled"
   #endif

如果你看到 ``#error`` 输出，
确保在设备树中启用该节点。
在某些情况下，你的代码可以编译但链接会失败，
并出现类似以下消息：

.. code-block:: none

   ...undefined reference to `__device_dts_ord_N'
   collect2: error: ld returned 1 exit status

这很可能意味着存在阻止设备驱动
构建的 Kconfig 问题，
导致引用不存在的符号。如果代码编译
成功，最后要检查的是设备是否就绪，如下所示：

.. code-block:: c

   if (!device_is_ready(uart_dev)) {
        printk("Device not ready\n");
   }

如果发现设备未就绪，
很可能意味着设备的
初始化函数失败。启用日志记录
或调试驱动代码可能有助于此类情况。
注意你还可以使用 :c:func:`device_get_binding` 在运行时获取引用。
如果返回 ``NULL``，可能意味着该设备的驱动初始化失败或该设备不存在。

.. _dts-find-binding:

查找设备树绑定
*************************

:ref:`dt-bindings` 是声明
所描述节点可做什么的 YAML 文件，
因此能够为你正在使用的节点
找到它们至关重要。

如果你还没有，:ref:`获取设备树输出 <get-devicetree-outputs>`。要查找节点
的绑定，打开生成的头文件，
它以一个块注释中的节点列表开头：

.. code-block:: c

   /*
    * [...]
    * Nodes in dependency order (ordinal and path):
    *   0   /
    *   1   /aliases
    *   2   /chosen
    *   3   /flash@0
    *   4   /memory@20000000
    *          (etc.)
    * [...]
    */

记下要查找的节点路径，如 ``/flash@0``。
在文件中搜索节点的输出，
如果节点
有匹配的绑定，它以下列内容开头：

.. code-block:: c

   /*
    * Devicetree node:
    *   /flash@0
    *
    * Binding (compatible = soc-nv-flash):
    *   $ZEPHYR_BASE/dts/bindings/mtd/soc-nv-flash.yaml
    * [...]
    */

故障排除见 :ref:`missing-dt-binding`。

.. _set-devicetree-overlays:

设置设备树覆盖
***********************

设备树覆盖在 :ref:`devicetree-intro` 中有解释。
CMake
变量 :makevar:`DTC_OVERLAY_FILE` 包含要使用的
覆盖文件列表（空格或分号分隔）。
如果 :makevar:`DTC_OVERLAY_FILE` 指定多个
文件，它们按该顺序被 C 预处理器包含。
Zephyr 模块中的文件可以通过
转义 Zephyr 模块目录变量
（如 ``\${ZEPHYR_<module>_MODULE_DIR}/<path-to>/dts.overlay``）
来引用
（设置 DTC_OVERLAY_FILE 变量时）。

你可以将 :makevar:`DTC_OVERLAY_FILE` 设置为
恰好包含你想使用的文件。
这里有一个使用
``west build`` 的 :ref:`示例 <west-building-dtc-overlay-file>`。

如果不设置 :makevar:`DTC_OVERLAY_FILE`，
构建系统将按以下步骤
在你的应用配置目录中查找
用作设备树覆盖的文件：

#. 如果文件 :file:`socs/<SOC>_<BOARD_QUALIFIERS>.overlay` 存在，将使用它。
#. 如果文件 :file:`boards/<BOARD>.overlay` 存在，将在上述基础上使用它。
#. 如果当前开发板有 :ref:`多个修订版本 <porting_board_revisions>`
   且 :file:`boards/<BOARD>_<revision>.overlay` 存在，将在上述基础上使用它。
#. 如果前几步找到一个或多个文件，构建系统
   停止查找并只使用那些文件。
#. 否则，如果 :file:`<BOARD>.overlay` 存在，将使用它，
   构建
   系统停止查找更多文件。
#. 否则，如果 :file:`app.overlay` 存在，将使用它。

可以使用 ``EXTRA_DTC_OVERLAY_FILE`` 提供
额外的设备树覆盖，
同时仍允许构建系统
自动使用上述步骤中描述的设备树覆盖。

处理设备树覆盖时，构建系统将
``EXTRA_DTC_OVERLAY_FILE`` 中指定的覆盖
追加到 ``DTC_OVERLAY_FILE`` 中的覆盖之后。
这意味着通过 ``EXTRA_DTC_OVERLAY_FILE`` 所做的更改
优先于通过 ``DTC_OVERLAY_FILE`` 所做的更改。

除通过
``DTC_OVERLAY_FILE`` 或 ``EXTRA_DTC_OVERLAY_FILE`` 参数
给出的绝对路径文件外，
所有配置文件都取自应用的配置
目录。

应用配置目录的定义
见 :ref:`Application Configuration Directory <application-configuration-directory>`。

使用 :ref:`shields` 也会添加设备树覆盖文件。

:makevar:`DTC_OVERLAY_FILE` 值存储在 CMake 缓存中
并在后续构建中使用。

:ref:`构建系统 <build_overview>` 在配置阶段打印
它找到的所有设备树覆盖，如下所示：

.. code-block:: none

   -- Found devicetree overlay: .../some/file.overlay

.. _use-dt-overlays:

使用设备树覆盖
***********************

如何向构建添加覆盖，
见 :ref:`set-devicetree-overlays`。

覆盖可以通过多种方式覆盖
节点属性值。
例如，如果 BOARD.dts 包含此节点：

.. code-block:: devicetree

   / {
           soc {
                   serial0: serial@40002000 {
                           status = "okay";
                           current-speed = <115200>;
                           /* ... */
                   };
           };
   };

以下是在覆盖中
覆盖 ``current-speed`` 值的等效方式：

.. Disable syntax highlighting as this construct does not seem supported by pygments
.. code-block:: none

   /* Option 1 */
   &serial0 {
   	current-speed = <9600>;
   };

   /* Option 2 */
   &{/soc/serial@40002000} {
   	current-speed = <9600>;
   };

后续示例将使用 ``&serial0`` 风格。

你可以使用覆盖向设备树添加别名：
别名只是
``/aliases`` 节点的属性。例如：

.. code-block:: devicetree

   / {
   	aliases {
   		my-serial = &serial0;
   	};
   };

Chosen 节点工作方式相同。例如：

.. code-block:: devicetree

   / {
   	chosen {
   		zephyr,console = &serial0;
   	};
   };

要删除属性（除一般删除属性外，
如果布尔属性在 BOARD.dts 中为真，
这也是将其设为假的方式）：

.. code-block:: devicetree

   &serial0 {
   	/delete-property/ some-unwanted-property;
   };

你可以使用覆盖添加子节点。例如，
要在现有总线节点上配置 SPI 或 I2C
子设备，
做类似以下事情：

.. code-block:: devicetree

   /* SPI device example */
   &spi1 {
   	my_spi_device: temp-sensor@0 {
   		compatible = "...";
   		label = "TEMP_SENSOR_0";
   		/* reg is the chip select number, if needed;
   		 * If present, it must match the node's unit address. */
   		reg = <0>;

   		/* Configure other SPI device properties as needed.
   		 * Find your device's DT binding for details. */
   		spi-max-frequency = <DT_FREQ_M(4)>;
   	};
   };

   /* I2C device example */
   &i2c2 {
   	my_i2c_device: touchscreen@76 {
   		compatible = "...";
   		label = "TOUCHSCREEN";
   		/* reg is the I2C device address.
   		 * It must match the node's unit address. */
   		reg = <76>;

   		/* Configure other I2C device properties as needed.
   		 * Find your device's DT binding for details. */
   	};
   };

其他总线设备可以类似配置：

- 将设备创建为父总线的子节点
- 按其绑定设置其属性

假设你有与
``my_spi_device`` 和 ``my_i2c_device`` compatible
关联的合适设备驱动，
现在你应该
能通过 Kconfig 启用驱动并
:ref:`获取新增总线节点的 struct device <dt-get-device>`，
然后用该驱动 API 使用它。

.. _dt-create-devices:

使用设备树 API 编写设备驱动
******************************************

"设备树感知"的 :ref:`设备驱动 <device_model_api>` 应为
每个具有特定 :ref:`compatible <dt-important-props>`（或驱动
支持的关联 compatible 集合）且 ``status = "okay"`` 的设备树节点
创建 ``struct device``。

编写设备树感知驱动
从为驱动支持的设备定义 :ref:`设备树绑定
<dt-bindings>` 开始。使用
类似驱动的现有绑定作为起点。
开始用的骨架绑定
只需以下这些：

.. code-block:: yaml

   description: <Human-readable description of your binding>
   compatible: "foo-company,bar-device"
   include: base.yaml

定位现有绑定的更多建议
见 :ref:`dts-find-binding`。

编写绑定后，驱动 C 文件
可以使用设备树 API
查找具有期望 compatible 且 ``status = "okay"`` 的节点，
并为每个节点
实例化一个 ``struct device``。
实例化每个
``struct device`` 有两种选择：
使用实例编号和使用节点标签。

无论哪种情况：

- 每个 ``struct device`` 的名称
  应设置为其设备树节点的
  ``label`` 属性。这允许驱动使用者
  以通常方式 :ref:`dt-get-device`。

- 每个设备的初始配置
  应尽可能使用
  设备树
  属性中的值。这允许用户使用
  :ref:`设备树覆盖 <use-dt-overlays>` 配置驱动。

如何做到此点的示例如下。假设你已实现设备特定的配置和数据结构及 API 函数，如下所示：

.. code-block:: c

   /* my_driver.c */
   #include <zephyr/drivers/some_api.h>

   /* Define data (RAM) and configuration (ROM) structures: */
   struct my_dev_data {
   	/* per-device values to store in RAM */
   };
   struct my_dev_cfg {
   	uint32_t freq; /* Just an example: initial clock frequency in Hz */
   	/* other configuration to store in ROM */
   };

   /* Implement driver API functions (drivers/some_api.h callbacks): */
   static int my_driver_api_func1(const struct device *dev, uint32_t *foo) { /* ... */ }
   static int my_driver_api_func2(const struct device *dev, uint64_t bar) { /* ... */ }
   static struct some_api my_api_funcs = {
   	.func1 = my_driver_api_func1,
   	.func2 = my_driver_api_func2,
   };

.. _dt-create-devices-inst:

选项 1：使用实例编号创建设备
===============================================

尽可能使用此选项（它使用
:ref:`devicetree-inst-apis`）。不过，
它们仅在你的驱动 ``compatible`` 的设备树节点
全部等效且
你不需要区分它们时才有效。

要使用基于实例的 API，
首先将 ``DT_DRV_COMPAT`` 定义为
设备驱动支持的 compatible 的小写加下划线版本。
例如，如果驱动在
设备树中的 compatible 是 ``"vnd,my-device"``，
则在驱动 C 文件中
将 ``DT_DRV_COMPAT`` 定义为 ``vnd_my_device``：

.. code-block:: c

   /*
    * Put this near the top of the file. After the includes is a good place.
    * (Note that you can therefore run "git grep DT_DRV_COMPAT drivers" in
    * the zephyr Git repository to look for example drivers using this style).
    */
   #define DT_DRV_COMPAT vnd_my_device

.. important::

   如所示，DT_DRV_COMPAT 宏
   不应有引号或特殊
   字符。从 compatible 属性创建 ``DT_DRV_COMPAT`` 时
   去除引号并将特殊字符
   转换为下划线。

最后，定义一个实例化宏，
使用实例编号
创建每个 ``struct device``。
在定义 ``my_api_funcs`` 之后做此操作。

.. code-block:: c

   /*
    * This instantiation macro is named "CREATE_MY_DEVICE".
    * Its "inst" argument is an arbitrary instance number.
    *
    * Put this near the end of the file, e.g. after defining "my_api_funcs".
    */
   #define CREATE_MY_DEVICE(inst)					\
   	static struct my_dev_data my_data_##inst = {			\
   		/* initialize RAM values as needed, e.g.: */		\
   		.freq = DT_INST_PROP(inst, clock_frequency),		\
   	};								\
   	static const struct my_dev_cfg my_cfg_##inst = {		\
   		/* initialize ROM values as needed. */			\
   	};								\
   	DEVICE_DT_INST_DEFINE(inst,					\
   			      my_dev_init_function,			\
 			      NULL,             			\
   			      &my_data_##inst,				\
   			      &my_cfg_##inst,				\
   			      MY_DEV_INIT_LEVEL, MY_DEV_INIT_PRIORITY,	\
   			      &my_api_funcs);

注意使用 :c:macro:`DT_INST_PROP` 和
:c:macro:`DEVICE_DT_INST_DEFINE` 之类的
API 访问设备树节点数据。
这些
API 从设备树获取
``DT_DRV_COMPAT`` 确定的 compatible 的
节点实例编号 ``inst`` 的数据。

最后，将实例化宏传递给 :c:macro:`DT_INST_FOREACH_STATUS_OKAY`：

.. code-block:: c

   /* Call the device creation macro for each instance: */
   DT_INST_FOREACH_STATUS_OKAY(CREATE_MY_DEVICE)

``DT_INST_FOREACH_STATUS_OKAY`` 展开为
对每个启用的
``DT_DRV_COMPAT`` 确定的 compatible 的节点
调用一次 ``CREATE_MY_DEVICE`` 的代码。
它不会在
``CREATE_MY_DEVICE`` 展开的末尾添加分号，
因此宏的展开必须以
分号或函数定义结尾以支持
多个设备。

选项 2：使用节点标签创建设备
==========================================

某些设备驱动无法使用实例编号。
一个示例是
依赖厂商 HAL API（为
单个 IP 块专门定制）实现 Zephyr 驱动
回调的 SoC
外设驱动。
此类情况应使用
:c:macro:`DT_NODELABEL`
引用设备树中表示
SoC 上支持外设的
单个节点。
然后可以使用
devicetree.h 的
:ref:`devicetree-generic-apis`
访问节点数据。

要使其工作，你的 :ref:`SoC 的 dtsi 文件 <dt-input-files>`
必须为你的驱动支持的
IP 块适当定义
``mydevice0``、``mydevice1`` 等节点
标签。
结果设备树通常如下所示：

.. code-block:: devicetree

   / {
           soc {
                   mydevice0: dev@0 {
                           compatible = "vnd,my-device";
                   };
                   mydevice1: dev@1 {
                           compatible = "vnd,my-device";
                   };
           };
   };

驱动可以使用
设备树中的 ``mydevice0`` 和 ``mydevice1`` 节点标签
操作特定设备节点：

.. code-block:: c

   /*
    * This is a convenience macro for creating a node identifier for
    * the relevant devices. An example use is MYDEV(0) to refer to
    * the node with label "mydevice0".
    */
   #define MYDEV(idx) DT_NODELABEL(mydevice ## idx)

   /*
    * Define your instantiation macro; "idx" is a number like 0 for mydevice0
    * or 1 for mydevice1. It uses MYDEV() to create the node label from the
    * index.
    */
   #define CREATE_MY_DEVICE(idx)					\
   	static struct my_dev_data my_data_##idx = {			\
   		/* initialize RAM values as needed, e.g.: */		\
   		.freq = DT_PROP(MYDEV(idx), clock_frequency),		\
   	};								\
   	static const struct my_dev_cfg my_cfg_##idx = { /* ... */ };	\
   	DEVICE_DT_DEFINE(MYDEV(idx),					\
   			my_dev_init_function,				\
 			NULL,           				\
 			&my_data_##idx,					\
 			&my_cfg_##idx,					\
 			MY_DEV_INIT_LEVEL, MY_DEV_INIT_PRIORITY,	\
 			&my_api_funcs)

注意使用 :c:macro:`DT_PROP` 和
:c:macro:`DEVICE_DT_DEFINE` 之类的
API 访问设备树节点数据。

最后，手动检测每个启用的设备树节点
并使用
``CREATE_MY_DEVICE`` 实例化每个 ``struct device``：

.. code-block:: c

   #if DT_NODE_HAS_STATUS(DT_NODELABEL(mydevice0), okay)
   CREATE_MY_DEVICE(0)
   #endif

   #if DT_NODE_HAS_STATUS(DT_NODELABEL(mydevice1), okay)
   CREATE_MY_DEVICE(1)
   #endif

由于此风格不使用 ``DT_INST_FOREACH_STATUS_OKAY()``，
驱动
作者负责
为每个可能的
节点调用 ``CREATE_MY_DEVICE()``，
例如使用
关于支持 SoC 上
可用外设的知识。

.. _dt-drivers-that-depend:

依赖其他设备的设备驱动
*******************************************

有时，一个 ``struct device`` 依赖于
另一个 ``struct device``
并需要其指针。例如，
传感器设备可能需要
其 SPI 总线控制器设备的指针。
一些建议：

- 尽可能以允许使用
  devicetree.h 的
  :ref:`devicetree-hw-api` 的方式
  编写设备树绑定。
- 特别是，对于总线设备，
  驱动的绑定应包含
  如 :zephyr_file:`dts/bindings/spi/spi-device.yaml`
  之类的文件，
  它提供
  通过特定总线可寻址设备的
  通用定义。
  这允许
  使用 :c:macro:`DT_BUS` 之类的
  API 获取
  总线
  节点的节点标识符。
  然后可以按通常方式为总线
  :ref:`dt-get-device`。

在现有绑定和设备驱动中查找示例。

.. _dt-apps-that-depend:

依赖开发板特定设备的应用
**************************************************

允许应用代码在多个开发板上不做修改运行的一种方式是支持设备树别名来指定硬件特定部分，
如 :zephyr:code-sample:`blinky` 示例所做的那样。
然后应用可以在
:ref:`BOARD.dts <devicetree-in-out-files>` 文件中
或通过 :ref:`设备树
覆盖 <use-dt-overlays>` 配置。
