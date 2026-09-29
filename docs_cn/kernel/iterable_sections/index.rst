.. _iterable_sections_api:

可迭代段
#################

本页包含可迭代段（iterable sections）API 的参考文档，
可用于定义等大小数据结构的可迭代区域，
可以用 :c:macro:`STRUCT_SECTION_FOREACH` 对其进行迭代。

概述
********

可迭代段是一组静态定义的相同结构体的实例，
链接器将它们放入单个连续的输出段中。
运行时随后可以遍历所有实例，而无需维护
显式列表。

Zephyr 目前支持两条链接脚本流水线：一条基于模板的流水线，
消费通过 ``zephyr_linker_sources()`` 注册的
``.ld`` 脚本；另一条由 CMake 生成的流水线，
消费 ``zephyr_iterable_section()`` 调用。要在所有受支持的
工具链上工作，新的可迭代段目前必须在
两处都声明。

当 ``CONFIG_CMAKE_LINKER_GENERATOR=y`` 时，可迭代段的
输出段由 ``zephyr_iterable_section()`` 调用发出。
通过 ``zephyr_linker_sources()`` 注册的 ``.ld``
片段中的任何 ``ITERABLE_SECTION_RAM/ROM`` 定义
都会被忽略。
当 ``CONFIG_CMAKE_LINKER_GENERATOR=n`` 时，情况相反：
``zephyr_iterable_section()``
调用不会被消费，由 ``.ld`` 脚本提供段定义。

由于上游 Zephyr 必须在两种配置下构建，
新的可迭代段必须在两处都声明。

创建一个可迭代段需要三个部分，
它们必须在结构体名称和 RAM 与
ROM 放置方式上保持一致：

1. **C 代码**：定义结构体，并使用
   :c:macro:`STRUCT_SECTION_ITERABLE`（或其 ROM 的 ``const`` 变体）
   实例化条目。

2. **链接器放置**：以两种方式之一声明（*上游两者都需要*）：

   - **CMake**：由 CMake 生成流水线消费的 ``zephyr_iterable_section()``。
   - **链接器脚本**：由基于模板的流水线消费的、
     通过 ``zephyr_linker_sources()`` 注册的
     ``ITERABLE_SECTION_RAM/ROM``。


步骤 1：在 C 中定义数据
****************************

在公共头文件中定义结构体，并提供一个
用 :c:macro:`STRUCT_SECTION_ITERABLE` 实例化条目的
辅助宏：

.. code-block:: c

    struct my_data {
             int a, b;
    };

    #define DEFINE_DATA(name, _a, _b) \
             STRUCT_SECTION_ITERABLE(my_data, name) = { \
                     .a = _a, \
                     .b = _b, \
             }

    ...

    DEFINE_DATA(d1, 1, 2);
    DEFINE_DATA(d2, 3, 4);
    DEFINE_DATA(d3, 5, 6);

对于驻留 ROM 的可迭代段，实例必须声明为 ``const``，
以便编译器将它们发射到只读输入段中。
C 声明和 CMake 放置（见步骤 2）必须在
RAM 与 ROM 放置方式上保持一致。

步骤 2：在 CMake 中声明段
************************************

``zephyr_iterable_section()`` 的 ``NAME`` 参数
必须与传给 :c:macro:`STRUCT_SECTION_ITERABLE` 的
结构体名匹配。``GROUP`` 参数
选择生成的输出段被放入的链接器组。

驻留 RAM 的示例：

.. code-block:: cmake

   # CMakeLists.txt
   zephyr_iterable_section(NAME my_data GROUP DATA_REGION ${XIP_ALIGN_WITH_INPUT})

驻留 ROM 的示例（C 中实例声明为 ``const``）：

.. code-block:: cmake

   # CMakeLists.txt
   zephyr_iterable_section(NAME my_data GROUP RODATA_REGION)


完整参数列表以及可用 ``GROUP`` 选项的
更详细解释，参见 ``cmake/modules/extensions.cmake`` 中的
``zephyr_iterable_section()``。

步骤 3：提供链接器脚本
*******************************

链接器脚本使用 :c:macro:`ITERABLE_SECTION_RAM` 或
:c:macro:`ITERABLE_SECTION_ROM` 发射实际的段。

驻留 RAM：

.. code-block:: c

   /* sections-ram.ld */
   #include <zephyr/linker/iterable_sections.h>

   ITERABLE_SECTION_RAM(my_data, Z_LINK_ITERABLE_SUBALIGN)

驻留 ROM：

.. code-block:: c

   /* sections-rom.ld */
   #include <zephyr/linker/iterable_sections.h>

   ITERABLE_SECTION_ROM(my_data, Z_LINK_ITERABLE_SUBALIGN)

从 ``CMakeLists.txt`` 注册链接器脚本：

.. code-block:: cmake

   zephyr_linker_sources(<location> <path-to-ld-file>)

完整参数列表以及可用 ``<location>`` 选项的
更详细解释，参见 ``cmake/modules/extensions.cmake`` 中的
``zephyr_linker_sources()``。

遍历条目
**************************

段就位后，用
:c:macro:`STRUCT_SECTION_FOREACH` 遍历其条目：

.. code-block:: c

   STRUCT_SECTION_FOREACH(my_data, data) {
           printk("%p: a: %d, b: %d\n", data, data->a, data->b);
   }

.. note::
   链接器会按名称排序放置条目，
   因此无论代码中如何定义，
   上述示例都会按顺序访问 ``d1``、``d2`` 和 ``d3``。

API 参考
*************

.. doxygengroup:: iterable_section_apis
