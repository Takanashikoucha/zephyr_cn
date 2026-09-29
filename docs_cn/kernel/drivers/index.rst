.. _device_model_api:

设备驱动模型
###################

介绍
************

Zephyr 内核支持多种设备驱动。
某个驱动是否可用取决于开发板和驱动本身。

Zephyr 设备模型为配置系统中的驱动
提供了一致的设备模型。设备模型负责
初始化配置到系统中的所有驱动。

每种类型的驱动（例如 UART、SPI、I2C）
都由一个通用类型 API 支持。

在该模型中，驱动在初始化期间
填入指向包含其 API 函数指针的
结构体的指针。这些
结构体按初始化级别顺序放入 RAM 段中。

.. image:: device_driver_model.svg
   :width: 40%
   :align: center
   :alt: 设备驱动模型

标准驱动
****************

存在于所有受支持开发板配置中的
设备驱动列于下方。

* **中断控制器**：该设备驱动由内核的
  中断管理子系统使用。

* **定时器**：该设备驱动由内核的系统时钟和
  硬件时钟子系统使用。

* **串行通信**：该设备驱动由内核的
  系统控制台子系统使用。

* **熵源（Entropy）**：该设备驱动为
  随机数生成器子系统提供熵数来源。

  .. important::

    使用 :ref:`随机 API 函数 <random_api>` 获取随机
    值。:ref:`熵函数 <entropy_api>` 不应
    直接用作随机数生成器来源，
    因为某些硬件
    实现被设计为随机
    数生成器的熵种子来源，
    不会提供密码学安全的
    随机数流。

同步调用
*****************

Zephyr 为多个开发板提供了一组设备驱动。
除非特定硬件不提供任何中断，否则每个驱动
都应支持基于中断的实现，而非轮询。

通过设备专用 API（如
:file:`i2c.h` 或 :file:`spi.h`）访问的高层调用
通常被设计为同步的。因此，
这些调用应当是阻塞的。

.. _device_driver_api:

驱动 API
***********

:file:`device.h` 提供以下设备驱动 API。
这些 API 仅用于设备驱动，
不应在应用中使用。

:c:macro:`DEVICE_DEFINE()`
   创建设备对象及相关数据结构，
   包括设置启动时初始化。

:c:macro:`DEVICE_NAME_GET()`
   将设备标识符转换为设备
   对象的全局标识符。

:c:macro:`DEVICE_GET()`
   按名称获取指向设备对象的指针。

:c:macro:`DEVICE_DECLARE()`
   声明一个设备对象。
   当需要前向引用一个尚未定义的
   设备时使用。

:c:macro:`DEVICE_API()`
   包装驱动 API 声明，将其分配到
   相应的链接器段。
   任何实现上游驱动
   类的驱动都必须使用此宏，
   因为 :c:macro:`DEVICE_API_GET` 和 :c:macro:`DEVICE_API_IS`
   依赖 API
   实例被放置在其类的链接器段中，
   以在运行时验证设备的
   API 类。

.. _device_struct:

驱动数据结构
**********************

设备初始化宏在构建时填充
一些数据结构，
这些结构体
被拆分为只读部分和运行时可变部分。
从高层次来看，我们有：

.. code-block:: C

  struct device {
  	const char *name;
  	const void *config;
  	const void *api;
  	void * const data;
  };

``config`` 成员用于构建时设置的只读配置数据。
例如，基地址内存映射 IO 地址、IRQ 线号，
或设备的其他固定
物理特性。这就是
传给 ``DEVICE_DEFINE()`` 及相关宏的 ``config`` 指针。

``data`` 结构体保存在 RAM 中，
供驱动用于
每实例的运行时管理。例如，
它可能包含引用计数、
信号量、临时缓冲区等。

``api`` 结构体将通用于件 API 映射到
驱动中的设备专用实现。它通常
是只读的，在构建时填充。
下一节将更详细地描述这一点。


子系统与 API 结构体
*****************************

大多数驱动实现的都是与设备无关的子系统 API。
应用只需针对该通用 API 编程即可，
应用代码
不针对任何特定驱动实现。

驱动 API 实例必须用 :c:macro:`DEVICE_API()` 声明，
以便它们被分配到相应的 API 链接器段。
这是 :c:macro:`DEVICE_API_GET` 和 :c:macro:`DEVICE_API_IS`
在运行时验证设备的
API 属于预期类所必需的。

子系统 API 定义通常如下所示：

.. code-block:: C

  typedef int (*subsystem_do_this_t)(const struct device *dev, int foo, int bar);
  typedef void (*subsystem_do_that_t)(const struct device *dev, void *baz);

  __subsystem struct subsystem_driver_api {
        subsystem_do_this_t do_this;
        subsystem_do_that_t do_that;
  };

  static inline int subsystem_do_this(const struct device *dev, int foo, int bar)
  {
        return DEVICE_API_GET(subsystem, dev)->do_this(dev, foo, bar);
  }

  static inline void subsystem_do_that(const struct device *dev, void *baz)
  {
        DEVICE_API_GET(subsystem, dev)->do_that(dev, baz);
  }

实现某个特定子系统的驱动将定义
这些 API 的真实实现，并使用
:c:macro:`DEVICE_API()` 包装器填充
subsystem_driver_api 结构体的一个实例：

.. code-block:: C

  static int my_driver_do_this(const struct device *dev, int foo, int bar)
  {
        ...
  }

  static void my_driver_do_that(const struct device *dev, void *baz)
  {
        ...
  }

  static DEVICE_API(subsystem, my_driver_api_funcs) = {
        .do_this = my_driver_do_this,
        .do_that = my_driver_do_that,
  };

然后驱动将 ``my_driver_api_funcs`` 作为 ``api`` 参数
传给 ``DEVICE_DEFINE()``。

.. note::

        由于 API 函数的指针在 ``api``
        结构体中被引用，即使未使用它们
        也始终会被包含在二进制中；
        ``gc-sections`` 链接器选项总会看到
        至少一个对
        它们的引用。要为驱动 API 提供
        链接时大小优化，
        在大多数情况下需要
        由 Kconfig 选项控制可选特性。

API 类继承
*********************

一个子系统 API 可以扩展另一个子系统 API，
形成父子
关系。这使得实现了子 API 的设备
同时被识别为实现了父 API。
例如，I3C 控制器
扩展 I2C API，因此它可以在
任何期望 I2C 设备的地方使用。

要定义子 API，将父 API 结构体嵌入
子结构体的**第一个成员**中，
并用 :c:macro:`DEVICE_API_EXTENDS` 声明该关系：

.. code-block:: C

  __subsystem struct child_driver_api {
        struct subsystem_driver_api parent_api;
        child_do_extra_t do_extra;
  };

  DEVICE_API_EXTENDS(child, subsystem, parent_api);

实现子 API 的驱动同时填充
父方法和子方法：

.. code-block:: C

  static DEVICE_API(child, my_child_api) = {
        .parent_api = {
                .do_this = my_child_do_this,
                .do_that = my_child_do_that,
        },
        .do_extra = my_child_do_extra,
  };

就位后，:c:macro:`DEVICE_API_IS` 对子
类和父类都返回 true，:c:macro:`DEVICE_API_GET`
可以按
任一种类型获取 API：

.. code-block:: C

  /* Both return true for a child device */
  DEVICE_API_IS(subsystem, dev);
  DEVICE_API_IS(child, dev);

  /* Access through parent API */
  DEVICE_API_GET(subsystem, dev)->do_this(dev, foo, bar);

支持多级继承（例如孙类扩展子类，
子类扩展父类）。
兄弟关系也能正确工作：
两个扩展同一父 API 的不同子 API
会被 :c:macro:`DEVICE_API_IS` 区分开。

设备专用 API 扩展
******************************

某些设备可以转换为 GPIO 等
驱动子系统的实例，
但提供了无法通过
标准 API 暴露的附加功能。
这些设备将子系统操作与
设备专用 API 相结合，
后者在设备专用头文件中描述。

设备专用 API 定义通常如下所示：

.. code-block:: C

   #include <zephyr/drivers/subsystem.h>

   /* When extensions need not be invoked from user mode threads */
   int specific_do_that(const struct device *dev, int foo);

   /* When extensions must be invokable from user mode threads */
   __syscall int specific_from_user(const struct device *dev, int bar);

   /* Only needed when extensions include syscalls */
   #include <zephyr/syscalls/specific.h>

实现子系统扩展的驱动将同时定义
子系统 API 和专用 API 的
真实实现：

.. code-block:: C

   static int generic_do_this(const struct device *dev, void *arg)
   {
      ...
   }

   static struct generic_api api {
      ...
      .do_this = generic_do_this,
      ...
   };

   /* supervisor-only API is globally visible */
   int specific_do_that(const struct device *dev, int foo)
   {
      ...
   }

   /* syscall API passes through a translation */
   int z_impl_specific_from_user(const struct device *dev, int bar)
   {
      ...
   }

   #ifdef CONFIG_USERSPACE

   #include <zephyr/internal/syscall_handler.h>

   int z_vrfy_specific_from_user(const struct device *dev, int bar)
   {
       K_OOPS(K_SYSCALL_SPECIFIC_DRIVER(dev, K_OBJ_DRIVER_GENERIC, &api));
       return z_impl_specific_do_that(dev, bar)
   }

   #include <zephyr/syscalls/specific_from_user_mrsh.c>

   #endif /* CONFIG_USERSPACE */

应用通过子系统 API 和专用
API 两者使用设备。

单个驱动，多个实例
*********************************

某些驱动可以在给定系统中被实例化
多次。例如
可以有多个 GPIO 组，或多个 UART。
驱动的每个实例
都会有不同的 ``config`` 结构体和 ``data`` 结构体。

为多个驱动实例配置中断是一种特殊情况。
如果每个
实例需要配置不同的中断线，
可以通过使用每实例配置函数
来实现，
因为 ``IRQ_CONNECT()`` 的参数
需要在构建时可解析。

例如，假设我们需要配置两个
``my_driver`` 实例，
每个使用不同的中断线。
在 ``drivers/subsystem/subsystem_my_driver.h`` 中：

.. code-block:: C

  typedef void (*my_driver_config_irq_t)(const struct device *dev);

  struct my_driver_config {
        DEVICE_MMIO_ROM;
        my_driver_config_irq_t config_func;
  };

在公共 init 函数的实现中：

.. code-block:: C

  void my_driver_isr(const struct device *dev)
  {
        /* Handle interrupt */
        ...
  }

  int my_driver_init(const struct device *dev)
  {
        const struct my_driver_config *config = dev->config;

        DEVICE_MMIO_MAP(dev, K_MEM_CACHE_NONE);

        /* Do other initialization stuff */
        ...

        config->config_func(dev);

        return 0;
  }

然后在声明特定实例时：

.. code-block:: C

  #if CONFIG_MY_DRIVER_0

  DEVICE_DECLARE(my_driver_0);

  static void my_driver_config_irq_0(const struct device *dev)
  {
        IRQ_CONNECT(MY_DRIVER_0_IRQ, MY_DRIVER_0_PRI, my_driver_isr,
                    DEVICE_GET(my_driver_0), MY_DRIVER_0_FLAGS);
  }

  const static struct my_driver_config my_driver_config_0 = {
        DEVICE_MMIO_ROM_INIT(DT_DRV_INST(0)),
        .config_func = my_driver_config_irq_0
  }

  static struct my_data_0;

  DEVICE_DEFINE(my_driver_0, MY_DRIVER_0_NAME, my_driver_init,
                NULL, &my_data_0, &my_driver_config_0,
                POST_KERNEL, MY_DRIVER_0_PRIORITY, &my_api_funcs);

  #endif /* CONFIG_MY_DRIVER_0 */

注意使用 ``DEVICE_DECLARE()`` 来避免
提供 IRQ 处理函数参数与设备本身定义之间
的循环依赖。

初始化级别
*********************

驱动可能依赖其他驱动先被初始化，
或需要
使用内核服务。:c:func:`DEVICE_DEFINE()` 及相关 API
允许用户指定 init
函数在启动序列的什么时间执行。
任何驱动都会指定三个
初始化级别之一：

``PRE_KERNEL_1``
    用于没有依赖的设备，
    例如仅依赖
    处理器/SOC 中现有硬件的设备。
    这些设备在配置期间
    不能使用任何内核服务，
    因为内核服务
    尚不可用。不过中断子系统
    会被配置，
    因此设置中断是可以的。
    该级别的 init 函数
    在中断栈上运行。

``PRE_KERNEL_2``
    用于依赖
    ``PRE_KERNEL_1`` 级别初始化
    的设备初始化的设备。
    这些设备在配置期间
    不能使用任何内核服务，
    因为内核服务
    尚不可用。该级别的 init 函数
    在中断栈上运行。

``POST_KERNEL``
    用于配置期间
    需要内核服务的设备。
    该级别的 init 函数
    在内核主任务的上下文中运行。

在每个初始化级别内，
可以指定一个优先级，
相对于同一初始化级别中的其他设备。
优先级
指定为 0 到 999 范围内的整数值；
较低的值表示
更早初始化。 优先级
必须是一个不带前导零或符号的十进制整数字面量
（例如 32），或等效的符号名（例如
``\#define MY_INIT_PRIO 32``）；
不允许使用符号表达式（例如
``CONFIG_KERNEL_INIT_PRIORITY_DEFAULT + 5``）。

驱动和其他系统工具可以用
:c:func:`k_is_pre_kernel`
函数判断启动
是否仍处于内核前状态。

延迟初始化
***********************

设备初始化也可以延迟到稍后时间。
在这种情况下，
设备不会在启动时由 Zephyr 自动初始化。
相反，
设备在应用调用 :c:func:`device_init`
时初始化。
要延迟设备驱动初始化，
在 DTS 文件中为关联的设备节点
添加属性 ``zephyr,deferred-init``。
例如：

.. code-block:: devicetree

   / {
           a-driver@40000000 {
                   reg = <0x40000000 0x1000>;
                   zephyr,deferred-init;
           };
   };

系统驱动
**************

在某些情况下，
可能只需要在启动时运行一个函数。
对于这种情况，
可以使用
:c:macro:`SYS_INIT`。
该宏不接受任何配置或运行时
数据结构，
也没有办法之后按名称获取设备指针。
初始化级别和优先级的相同设备策略适用。

检查初始化序列
**************************************

用 :c:macro:`DEVICE_DEFINE`（或其任何变体）
和 :c:macro:`SYS_INIT` 声明的设备驱动
在启动时处理，
相应的
初始化函数按其指定的
级别和优先级依次调用。

有时检查链接器生成的最终
初始化函数
调用序列会很有用。
为此，
使用 ``initlevels`` CMake
目标，
例如 ``west build -t initlevels``。

错误处理
**********************

一般来说，
除非失败预计会在正常运行过程中发生
（例如存储设备
已满），否则最好使用 ``__ASSERT()`` 宏
而不是
传播返回值。
坏参数、编程错误、一致性检查、
病态/不可恢复的失败等，
应通过
断言处理。

当适合返回错误条件供调用者
检查时，
成功应返回 0，
失败应返回 POSIX :file:`errno.h` 代码。
详见
https://github.com/zephyrproject-rtos/zephyr/wiki/Naming-Conventions#return-codes

内存映射
**********************

在某些系统中，
外设内存映射 IO（MMIO）
区域的线性地址
无法在构建时确定：

- IO 范围必须从总线在运行时探测，
  例如
  PCI express
- 内存管理单元（MMU）处于活动状态，
  MMIO 范围的物理地址
  必须被映射到内核确定的某个虚拟
  内存位置的页表中。

这些系统必须在 RAM 中维护
MMIO 范围的存储，
并在驱动的 init 函数中
建立映射。
其他系统
不需要关心这一点，
可以直接从
DTS 使用 MMIO 物理地址，
不需要任何基于 RAM 的存储。

对于可能需要处理这种情况的驱动，
定义了 DEVICE_MMIO 范围内的一组
API，
以及映射函数
:c:func:`device_map`。

具有单个 MMIO 区域的设备模型驱动
=========================================

最简单的情况是
需要维护一个 MMIO 区域的驱动。
这些驱动需要在 ``config_info``
和 ``driver_data`` 结构的定义中
使用 ``DEVICE_MMIO_ROM`` 和
``DEVICE_MMIO_RAM`` 宏，
并用 ``DEVICE_MMIO_ROM_INIT``
从 DTS 初始化 ``config_info``。
在 init 函数中
调用 ``DEVICE_MMIO_MAP()``：

.. code-block:: C

   struct my_driver_config {
      DEVICE_MMIO_ROM; /* Must be first */
      ...
   }

   struct my_driver_dev_data {
      DEVICE_MMIO_RAM; /* Must be first */
      ...
   }

   const static struct my_driver_config my_driver_config_0 = {
      DEVICE_MMIO_ROM_INIT(DT_DRV_INST(...)),
      ...
   }

   int my_driver_init(const struct device *dev)
   {
      ...
      DEVICE_MMIO_MAP(dev, K_MEM_CACHE_NONE);
      ...
   }

   int my_driver_some_function(const struct device *dev)
   {
      ...
      /* Write some data to the MMIO region */
      sys_write32(0xDEADBEEF, DEVICE_MMIO_GET(dev));
      ...
   }

这些宏的具体展开取决于配置。
在没有 MMU 或 PCI-e 的设备上，
``DEVICE_MMIO_MAP`` 和
``DEVICE_MMIO_RAM`` 展开为空。

具有多个 MMIO 区域的设备模型驱动
===============================================

某些驱动可能有多个 MMIO 区域。
此外，
某些驱动
可能已经实现了某种形式的继承，
需要
将其他数据放在
``config_info`` 和 ``driver_data``
结构体的最前面。

这可以用 ``DEVICE_MMIO_NAMED`` 变体宏
来管理。
这些
宏要求定义 ``DEV_CFG()`` 和 ``DEV_DATA()`` 宏，
以获取
指向驱动 config_info 或 dev_data 结构体的
正确类型指针。
例如：

.. code-block:: C

   struct my_driver_config {
      ...
     	DEVICE_MMIO_NAMED_ROM(corge);
    	DEVICE_MMIO_NAMED_ROM(grault);
      ...
   }

   struct my_driver_dev_data {
     	   ...
    	DEVICE_MMIO_NAMED_RAM(corge);
    	DEVICE_MMIO_NAMED_RAM(grault);
    	...
   }

   #define DEV_CFG(_dev) \
      ((const struct my_driver_config *)((_dev)->config))

   #define DEV_DATA(_dev) \
      ((struct my_driver_dev_data *)((_dev)->data))

   const static struct my_driver_config my_driver_config_0 = {
      ...
      DEVICE_MMIO_NAMED_ROM_INIT(corge, DT_DRV_INST(...)),
      DEVICE_MMIO_NAMED_ROM_INIT(grault, DT_DRV_INST(...)),
      ...
   }

   int my_driver_init(const struct device *dev)
   {
      ...
      DEVICE_MMIO_NAMED_MAP(dev, corge, K_MEM_CACHE_NONE);
      DEVICE_MMIO_NAMED_MAP(dev, grault, K_MEM_CACHE_NONE);
      ...
   }

   int my_driver_some_function(const struct device *dev)
   {
      ...
      /* Write some data to the MMIO regions */
      sys_write32(0xDEADBEEF, DEVICE_MMIO_GET(dev, grault));
      sys_write32(0xF0CCAC1A, DEVICE_MMIO_GET(dev, corge));
      ...
   }

同一 DT 节点中具有多个 MMIO 区域的设备模型驱动
===================================================================

某些驱动可能有多个 MMIO 区域，
定义在同一个 DT 设备
节点中，
用 ``reg-names`` 属性区分它们，
例如：

.. code-block:: devicetree

   /dts-v1/;

   / {
           a-driver@40000000 {
                   reg = <0x40000000 0x1000>,
                         <0x40001000 0x1000>;
                   reg-names = "corge", "grault";
           };
   };

这可以像上一节那样管理，
但这次使用
``DEVICE_MMIO_NAMED_ROM_INIT_BY_NAME`` 宏。
因此唯一的
区别就在驱动配置结构体中：

.. code-block:: C

   const static struct my_driver_config my_driver_config_0 = {
      ...
      DEVICE_MMIO_NAMED_ROM_INIT_BY_NAME(corge, DT_DRV_INST(...)),
      DEVICE_MMIO_NAMED_ROM_INIT_BY_NAME(grault, DT_DRV_INST(...)),
      ...
   }

不使用 Zephyr 设备模型的驱动
===========================================

某些驱动或类似驱动的代码可能不使用
Zephyr 的设备模型，
必须
为 MMIO 数据安排替代存储。
一个
例子是定时器驱动，
或中断控制器代码。

这可以用 ``DEVICE_MMIO_TOPLEVEL`` 宏组
来管理，
例如：

.. code-block:: C

   DEVICE_MMIO_TOPLEVEL_STATIC(my_regs, DT_DRV_INST(..));

   void some_init_code(...)
   {
      ...
      DEVICE_MMIO_TOPLEVEL_MAP(my_regs, K_MEM_CACHE_NONE);
      ...
   }

   void some_function(...)
      ...
      sys_write32(DEVICE_MMIO_TOPLEVEL_GET(my_regs), 0xDEADBEEF);
      ...
   }

不使用 DTS 的驱动
===========================

某些驱动可能不从 DTS 获取 MMIO 物理地址，
例如
PCI-E 的情况。
在这种情况下
可以直接使用 :c:func:`device_map` 函数：

.. code-block:: C

   void some_init_code(...)
   {
      ...
      struct pcie_bar mbar;
      bool bar_found = pcie_get_mbar(bdf, index, &mbar);

      device_map(DEVICE_MMIO_RAM_PTR(dev), mbar.phys_addr, mbar.size, K_MEM_CACHE_NONE);
      ...
   }

对于这些情况，
可以省略 DEVICE_MMIO_ROM 指令。

API 参考
**********************

.. doxygengroup:: device_model
