.. _binary_descriptors:

二进制描述符
##################

二进制描述符是存储关于二进制可执行文件信息的常量数据对象。
与"常规"常量不同，二进制描述符链接到二进制中已知的偏移量，
使其可被其他程序访问，例如在同一设备上运行的不同镜像或主机工具。
一些可作为有用二进制描述符的常量示例包括：内核版本、应用程序版本、
构建时间、编译器版本、环境变量、编译主机名等。

二进制描述符通过使用 ``DEFINE_BINDESC_*`` 宏创建。例如：

.. code-block:: c

   #include <zephyr/bindesc.h>

   BINDESC_STR_DEFINE(my_string, 2, "Hello world!"); // 唯一 ID 为 2

``my_string`` 随后可以使用以下方式访问：

.. code-block:: c

   printk("my_string: %s\n", BINDESC_GET_STR(my_string));

但它也可以通过 ``west bindesc`` 检索：

.. code-block:: bash

   $ west bindesc custom_search STR 2 build/zephyr/zephyr.bin
   "Hello world!"

内部实现
*********
二进制描述符使用链接到二进制镜像中已知偏移量的 TLV（标签、长度、值）头实现。
该偏移量可能因架构而异，
但通常描述符尽可能链接到镜像开头附近。
在镜像必须以向量表开头的架构中（例如
ARM），描述符链接在向量表之后。重置向量指向
文本段的开头，即在描述符之后。在
镜像必须以可执行代码开头的架构中（例如 x86），在
镜像开头注入一条跳转指令，
以跳过紧跟在跳转指令之后的二进制描述符。

每个标签是一个 16 位无符号整数，最高位半字节（4 位）是类型
（当前为 uint、string 或 bytes），其余是 ID。ID 对每个
描述符全局唯一。例如，应用程序版本字符串的 ID 为 ``0x800``，字符串
由 0x1 表示，使应用程序版本标签为 ``0x1800``。长度是一个 16 位
数字，等于数据的字节长度。数据是实际的描述符
值。所有二进制描述符数字（魔数、标签、uint）在内存中
以 SoC 原生字节序排列。``west bindesc`` 默认假设小端，
所以如果镜像属于大端 SoC，应给
工具适当的标志。

二进制描述符头以魔数 ``0xb9863e5a7ea46046`` 开头。其后
是 TLV，以 ``DESCRIPTORS_END``（``0xffff``）标签结尾。标签
始终对齐到 32 位。如果前一个描述符的值
长度未对齐，将添加零填充以确保当前标签对齐。

综合以上所有内容，上面示例在内存中的样子如下
（小端 SoC）：

.. code-block::

    46 60 a4 7e 5a 3e 86 b9 02 10  0d 00  48 65 6c 6c 6f 20 77 6f 72 6c 64 21 00 00 00 00 ff ff 00 00
   |         magic         | tag |length| H  e  l  l  o     w  o  r  l  d  !    |   pad  |    end    |

使用
*****
二进制描述符始终由 ``BINDESC_*_DEFINE`` 宏创建。如
上面示例所示，描述符可以从任何字符串或整数生成，
具有任何 ID。但是，建议遵循 ``include/zephyr/bindesc.h`` 中定义的标准标签，
因为这将带来以下好处：

  1. ``west bindesc`` 工具将能够识别描述符的含义并
     打印有意义的标签
  2. 它将强制来自不同来源的各种应用程序之间的一致性
  3. 它允许描述符生成的上游化（参见标准描述符）

要定义具有标准标签的描述符，只需使用从 ``bindesc.h`` 包含的标签：

.. code-block:: c

   #include <zephyr/bindesc.h>

   BINDESC_STR_DEFINE(app_version, BINDESC_ID_APP_VERSION_STRING, "1.2.3");

标准描述符
===================
一些描述符可能很简单实现，因此可以
在上游 Zephyr 中以标准方式实现。这些
可以通过 Kconfig 启用，
而不需要每个用户重新实现。这些包括构建时间、内核版本、
和主机信息。例如，要将构建日期和时间作为字符串添加，
应启用以下配置：

.. code-block:: kconfig

   # 启用二进制描述符
   CONFIG_BINDESC=y

   # 启用二进制描述符定义
   CONFIG_BINDESC_DEFINE=y

   # 启用默认构建时间二进制描述符
   CONFIG_BINDESC_DEFINE_BUILD_TIME=y
   CONFIG_BINDESC_BUILD_DATE_TIME_STRING=y

为了避免与用户定义的描述符冲突，标准描述符被分配
了 ``0x800-0xfff`` 范围。这留给用户 ``0x000-0x7ff``。
更多信息请阅读这些 Kconfig 符号的 ``help`` 部分。
按照惯例，每个 Kconfig 符号对应一个二进制描述符，
名称是 Kconfig 名称（去掉 ``CONFIG_BINDESC_``）的小写形式。例如，
``CONFIG_BINDESC_KERNEL_VERSION_STRING`` 创建一个描述符，
可以使用 ``BINDESC_GET_STR(kernel_version_string)`` 访问。

读取描述符
===================
也可以从应用程序读取和解析二进制描述符。
这对试图读取自身描述符的镜像和
试图读取另一个镜像描述符的镜像都有用。读取可以通过
三个后端之一执行：

 #. RAM - 假设描述符已复制到 RAM（例如由引导加载器），
    可以从它们所在的缓冲区读取。

 #. 内存映射闪存 - 如果要读取的镜像所在的闪存
    可通过程序的地址空间访问，
    可以直接从闪存读取。
    此选项使用最少的 RAM，但如果闪存不是内存映射的则不起作用，
    由于安全原因不建议读取引导加载器的描述符。

 #. 闪存 - 使用内部缓冲区，描述符使用闪存 API 逐个读取，
    并在缓冲区中时交给用户。

要启用读取描述符，启用 :kconfig:option:`CONFIG_BINDESC_READ`。三个后端
分别由这些 Kconfig 符号启用：:kconfig:option:`CONFIG_BINDESC_READ_RAM`、
:kconfig:option:`CONFIG_BINDESC_READ_MEMORY_MAPPED_FLASH` 和 :kconfig:option:`CONFIG_BINDESC_READ_FLASH`。

要读取描述符，应首先初始化描述符的句柄：

.. code-block:: c

   struct bindesc_handle handle;

   /* 假设缓冲区包含描述符的副本 */
   bindesc_open_ram(&handle, buffer);

``bindesc_open_*`` 函数是唯一涉及所用后端的函数。
API 的其余部分不关心数据在哪里。句柄初始化后，
可以与 API 的其余部分一起使用：

.. code-block:: c

   char *version;
   bindesc_find_str(&handle, BINDESC_ID_KERNEL_VERSION_STRING, &version);
   printk("内核版本: %s\n", version);

west bindesc 工具
=================
``west`` 能够解析和显示给定可执行镜像的二进制描述符。

更多信息请参见 ``west bindesc --help`` 或 :ref:`文档<west-bindesc>`。

API 参考
*************

.. doxygengroup:: bindesc_define

.. doxygengroup:: bindesc_read
