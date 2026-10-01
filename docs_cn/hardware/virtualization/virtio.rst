.. _virtio:

虚拟 I/O（VIRTIO）
##########################

概述
********

虚拟 I/O（VIRTIO）是一种用于与各种设备通信的协议，通常用于虚拟化环境。其主要目标是为虚拟机内部与虚拟设备的交互提供高效且标准化的机制。通信依赖于 virtqueue（虚拟队列）以及 PCI 或 MMIO 等标准传输方式。

概念
********

Virtio 定义了通信和初始化过程中使用的各种组件。它同时规定了主机侧（在规范中称为"设备"）和来宾侧（在规范中称为"驱动程序"）。目前 Zephyr 只能作为来宾（guest）运行。在 Virtio 驱动程序提供的功能之上，可以进一步实现特定设备（如网卡）的驱动程序。

带有 Virtio 设备的系统的高层概览如下图所示。

.. graphviz::
   :caption: 虚拟 I/O 概览

   digraph {

       subgraph cluster_host {
           style=filled;
           color=lightgrey;
           label = "Host";
           labeljust=r;

           virtio_device [label = "virtio device"];
       }

       transfer_method [label = "virtio transfer method"];

       subgraph cluster_guest {
           style=filled;
           color=lightgrey;
           label = "Guest";
           labeljust=r;

           virtio_driver [label = "virtio driver"];
           specific_device_driver [label = "specific device driver"];
           device_user [label = "device user"];
       }

       virtio_device -> transfer_method;
       transfer_method -> virtio_device;
       transfer_method -> virtio_driver;
       virtio_driver -> transfer_method;
       virtio_driver -> specific_device_driver;
       specific_device_driver -> virtio_driver;
       specific_device_driver -> device_user;
       device_user -> specific_device_driver;
   }

配置空间
===================
每个设备都提供配置空间，用于初始化和配置。它允许选择设备和驱动程序的特性、启用特定的 virtqueue 并设置其地址。一旦设备配置完成，在不重置设备的情况下，其大部分配置无法更改。配置空间的具体布局取决于传输方式。

驱动程序与设备特性
--------------------------
配置空间提供了一种协商特性位（feature bits）的方式，用以确定设备的一些非强制功能。具体可用的特性位取决于设备和平台。

设备特定配置
-----------------------------
某些设备提供设备特定的配置空间，提供额外的配置选项。

Virtqueue（虚拟队列）
==========
在主机和来宾之间传输数据的主要机制是 virtqueue。不同设备拥有的 virtqueue 数量不同，例如支持双向传输的设备通常有一个或多个 tx/rx virtqueue 对。Virtio 规定了两种类型的 virtqueue：分离式（split）virtqueue 和打包式（packed）virtqueue。Zephyr 目前仅支持分离式 virtqueue。

分离式 virtqueue
----------------
一个分离式 virtqueue 由三部分组成：描述符表（descriptor table）、可用环（available ring）和已用环（used ring）。

描述符表保存缓冲区的描述符，即其物理地址、长度和标志。每个描述符要么是设备可写的，要么是驱动程序可写的。描述符可以链接，形成描述符链。通常，链以包含设备要读取的数据的描述符开始，以设备可写部分结束，设备在该部分放置其响应。

可用环的主要部分是一个循环缓冲区，保存指向描述符表中描述符的引用（以索引形式）。当来宾决定向主机发送数据时，它将描述符链头部的索引添加到可用环的顶部。

已用环与可用环类似，但它由主机使用，用于向来宾返回描述符。除了保存描述符索引外，它还提供关于写入数据量的信息。

通用 Virtio 库
***********************

Zephyr 提供了一套用于与 Virtio 设备和 virtqueue 交互的 API，允许在 Virtio 设备的整个生命周期中执行必要的操作。

设备初始化
====================
一旦 Virtio 驱动程序完成使用给定传输方式的所有设备通用的低层初始化（例如在总线（bus）上查找设备并映射 Virtio 结构），设备特定驱动程序就会介入，并在 Virtio API 的帮助下执行初始化的后续阶段。

设备特定驱动程序做的第一件事是特性位协商。它使用 :c:func:`virtio_read_device_feature_bit` 确定设备提供哪些特性，然后使用 :c:func:`virtio_write_driver_feature_bit` 选择其需要的特性。在所有必需特性选定后，设备特定驱动程序调用 :c:func:`virtio_commit_feature_bits`。随后，使用 :c:func:`virtio_init_virtqueues` 初始化 virtqueue。该函数枚举 virtqueue，调用所提供的回调 :c:type:`virtio_enumerate_queues` 以确定每个 virtqueue 所需的尺寸。初始化过程通过调用 :c:func:`virtio_finalize_init` 完成。从此点起，如果没有任何函数返回错误，virtqueue 即可投入运行。如果特定设备提供了设备特定配置，则可以通过调用 :c:func:`virtio_get_device_specific_config` 获取。

Virtqueue 操作
===================
一旦 virtqueue 投入运行，即可用于发送和接收数据。为此，必须使用 :c:func:`virtio_get_virtqueue` 获取第 n 个 virtqueue 的指针。要发送由描述符链组成的数据，必须使用 :c:func:`virtq_add_buffer_chain`。沿描述符链，它接收一个回调指针，该回调在设备返回给定描述符链时被调用。之后，必须使用 Virtio API 的 :c:func:`virtio_notify_virtqueue` 通知 virtqueue。

来宾侧 Virtio 驱动程序
*************************
目前 Zephyr 提供了基于 PCI 的 Virtio 和基于 MMIO 的 Virtio 驱动程序，以及使用 virtio 的三种设备的驱动程序——virtiofs（用于访问主机文件系统）、virtio-entropy（用作熵源）和 virtio-blk（用于访问块设备）。

Virtiofs
================
该驱动程序支持 `virtiofs <https://virtio-fs.gitlab.io/>`_——一种允许虚拟机来宾访问主机上目录的文件系统。它使用 FUSE 消息在主机和来宾之间通信，以执行打开和读取文件等文件系统操作。每当来宾想要执行某个文件系统操作时，它就在 virtqueue 中放置一个描述符链：以设备可读部分（包含 FUSE 输入头和输入数据）开始，以设备可写部分（包含 FUSE 输出头和输出数据的空间）结束。

Virtio-entropy
================
该驱动程序允许在 Zephyr 中将 virtio-entropy 用作熵源。该设备的操作很简单——驱动程序在 virtqueue 中放置一个缓冲区并接收其返回，其中填充了随机数据。

Virtio-blk
==========
该驱动程序向 Zephyr 的磁盘访问层暴露 virtio-blk 块设备，因此可以通过 :ref:`磁盘访问 API <disk_access_api>` 使用，在其之上还可以挂载文件系统。它保持单个在途（in-flight）请求，提交由请求头、调用方的数据缓冲区（作为一个或多个分散-聚集段）以及一个状态字节组成的描述符链。详见 :ref:`disk_virtio_blk`。

Virtio 示例
**************
一个展示依赖 Virtio 的驱动程序用法的示例在 :zephyr:code-sample:`virtiofs` 中提供。如果你想查看直接与 Virtio 驱动程序交互的代码，可以查看 virtiofs 驱动程序，特别是用于初始化的 :c:func:`virtiofs_init`，以及用于与 Virtio 设备收发数据的 :c:func:`virtiofs_send_receive` 和 :c:func:`virtiofs_recv_cb`。

API 参考
*************

.. doxygengroup:: virtio_interface
.. doxygengroup:: virtqueue_interface
