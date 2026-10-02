.. _binary_descriptors:

二进制描述符
##################

二进制描述符是存储关于二进制可执行文件信息的常量数据对象。
与"常规"常量不同，二进制描述符链接到二进制文件中的已知偏移量，
因此可被其他程序访问，例如运行在同一设备上的另一个镜像或主机工具。
一些适合作为二进制描述符的常量示例包括：内核版本、应用版本、
构建时间、编译器版本、环境变量、编译主机名等。

二进制描述符通过 ``DEFINE_BINDESC_*`` 宏创建。例如：

.. code-block:: c

   #include <zephyr/bindesc.h>

   BINDESC_STR_DEFINE(my_string, 2, "Hello world!"); // Unique ID is 2

之后可以通过以下方式访问 ``my_string``：

.. code-block:: c

   printk("my_string: %s\n", BINDESC_GET_STR(my_string));

它也可以由 ``west bindesc`` 获取：

.. code-block:: bash

   $ west bindesc custom_search STR 2 build/zephyr/zephyr.bin
   "Hello world!"

内部结构
*********

二进制描述符通过一个 TLV（tag、length、value，即标签、长度、值）头实现，
该头链接到二进制镜像中的已知偏移量。该偏移量可能因架构而异，
但通常描述符会尽可能链接到镜像的开头。
在镜像必须以向量表开头的架构中（例如
ARM），描述符链接在向量表之后。复位向量指向
文本段的开头，即描述符之后。
在镜像必须以可执行代码开头的架构中（例如 x86），
会在镜像开头注入一条跳转指令，以跳过紧随其后的
二进制描述符。

每个标签是一个 16 位无符号整数，其中最高位半字节（4 位）是类型
（目前为 uint、string 或 bytes），其余部分是 ID。
ID 对每个描述符全局唯一。例如，应用版本字符串的 ID 是 ``0x800``，
字符串由 0x1 表示，因此应用版本的标签为 ``0x1800``。
长度是一个 16 位数字，等于数据以字节为单位的长度。
数据是描述符的实际值。所有二进制描述符数字（魔数、标签、uint）
在内存中的布局采用 SoC 原生的字节序。
``west bindesc`` 默认假设小端，
因此如果镜像属于大端 SoC，应给工具提供相应标志。

二进制描述符头以魔数 ``0xb9863e5a7ea46046`` 开头。
其后是 TLV，并以 ``DESCRIPTORS_END``（``0xffff``）标签结尾。
标签始终按 32 位对齐。如果前一个描述符的值
长度未对齐，会添加零填充以确保当前标签对齐。

综合以上内容，上面的示例在小端 SoC 的内存中
看起来如下：

.. code-block::

    46 60 a4 7e 5a 3e 86 b9 02 10  0d 00  48 65 6c 6c 6f 20 77 6f 72 6c 64 21 00 00 00 00 ff ff 00 00
   |         magic         | tag |length| H  e  l  l  o     w  o  r  l  d  !    |   pad  |    end    |

用法
*****

二进制描述符总是通过 ``BINDESC_*_DEFINE`` 宏创建。
如上面示例所示，描述符可以从任何字符串或整数生成，
并使用任意 ID。但建议遵循 ``include/zephyr/bindesc.h``
中定义的标准标签，因为这样做有以下好处：

 1. ``west bindesc`` 工具能够识别描述符的含义并
    打印有意义的标签
 2. 可强制来自不同来源的多个应用之间的一致性
 3. 允许描述符生成的上游化（见标准描述符）

要使用标准标签定义描述符，只需使用从 ``bindesc.h`` 包含的标签：

.. code-block:: c

   #include <zephyr/bindesc.h>

   BINDESC_STR_DEFINE(app_version, BINDESC_ID_APP_VERSION_STRING, "1.2.3");

标准描述符
=================

一些描述符的实现可能很简单，因此可以
在上游 Zephyr 中按标准方式实现。之后
可通过 Kconfig 启用它们，
而无需每个用户都重新实现。这些包括构建时间、内核版本
和主机信息。例如，要将构建日期和时间作为字符串添加，
应启用以下配置：

.. code-block:: kconfig

   # Enable binary descriptors
   CONFIG_BINDESC=y

   # Enable definition of binary descriptors
   CONFIG_BINDESC_DEFINE=y

   # Enable default build time binary descriptors
   CONFIG_BINDESC_DEFINE_BUILD_TIME=y
   CONFIG_BINDESC_BUILD_DATE_TIME_STRING=y

为避免与用户自定义描述符冲突，标准描述符被分配了
``0x800-0xfff`` 之间的范围。这样 ``0x000-0x7ff`` 留给用户。
更多信息请阅读这些 Kconfig 符号的 ``help`` 部分。
按照约定，每个 Kconfig 符号对应一个二进制描述符，
其名称是 Kconfig 名称（去掉 ``CONFIG_BINDESC_``）的小写形式。
例如，
``CONFIG_BINDESC_KERNEL_VERSION_STRING`` 创建一个可通过
``BINDESC_GET_STR(kernel_version_string)`` 访问的描述符。

读取描述符
=================

也可以从应用读取和解析二进制描述符。
这对于尝试读取自身描述符的镜像，以及
尝试读取另一个镜像描述符的镜像都有用。
读取可通过三种后端之一执行：

 #. RAM — 假设描述符已被复制到 RAM（例如由引导加载器完成），
    可从其所在的缓冲区读取。

 #. 内存映射 flash — 如果要读取的镜像所在的 flash 是
    内存映射的，可通过程序的地址空间访问，
    则可直接从 flash 读取。
    该选项使用的 RAM 最少，但如果 flash 不是内存映射的则无法工作，
    出于安全考虑，不建议用它读取引导加载器的描述符。

 #. Flash — 使用内部缓冲区，通过 flash API 逐个读取描述符，
    并在其位于缓冲区中时交给用户。

要启用读取描述符，请启用 :kconfig:option:`CONFIG_BINDESC_READ`。
三种后端分别由以下 Kconfig 符号启用：
:kconfig:option:`CONFIG_BINDESC_READ_RAM`、
:kconfig:option:`CONFIG_BINDESC_READ_MEMORY_MAPPED_FLASH` 和
:kconfig:option:`CONFIG_BINDESC_READ_FLASH`。

要读取描述符，应先初始化一个指向描述符的句柄：

.. code-block:: c

   struct bindesc_handle handle;

   /* Assume buffer holds a copy of the descriptors */
   bindesc_open_ram(&handle, buffer);
``bindesc_open_*`` 函数是唯一与所用后端相关的函数。

API 的其余部分不关心数据位于何处。句柄初始化后，
即可与 API 的其余部分一起使用：

.. code-block:: c

   char *version;
   bindesc_find_str(&handle, BINDESC_ID_KERNEL_VERSION_STRING, &version);
   printk("Kernel version: %s\n", version);

west bindesc 工具
=================

``west`` 能够解析并显示给定可执行镜像中的二进制描述符。

更多信息请参见 ``west bindesc --help`` 或 :ref:`文档<west-bindesc>`。

API 参考
*************

.. doxygengroup:: bindesc_define

.. doxygengroup:: bindesc_read
