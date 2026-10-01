.. _mpipe:

多媒体流水线（Multimedia Pipeline，mpipe）
###########################

.. contents::
   :local:
   :depth: 2

概述
********

多媒体流水线子系统（mpipe）由称为**元素**（element）的自包含处理组件构建媒体流。应用程序声明它所需的元素，
将它们链接成一个图（graph），并用状态机驱动该图；mpipe 在相邻元素之间协商数据格式，确定哪个缓冲区池（buffer pool）提供缓冲区，并将那些缓冲区从一个元素传递到下一个。

.. graphviz::
   :align: center
   :caption: 流水线是一个元素在其 pad 处连接的图。

   digraph pipeline {
     rankdir=LR;
     node [shape=record, style=filled, fillcolor="#e8e8e8", fontname="sans"];
     edge [fontname="sans", fontsize=10];

     src   [label="{ source | { <o> src pad } }"];
     trans [label="{ { <i> sink pad } | transform | { <o> src pad } }"];
     sink  [label="{ { <i> sink pad } | sink }"];

     src:o   -> trans:i [label="negotiated format"];
     trans:o -> sink:i  [label="negotiated format"];
   }

mpipe 提供的是构件和它们组合的规则，而不是现成的解决方案，因此流水线的组装方式很像用 LEGO 积木搭建：相同的图可以在不同的板卡上运行，
只需将它的元素绑定到不同的设备；而新的需求通常只是多一个元素而不是重写。

元素本身位于**插件**（plugin）中，按媒体域分组。一个插件带有自己的目录、自己的 Kconfig 和自己的头文件，
构建无需修改框架即可将其纳入，因此芯片供应商或中间件提供商可以发布元素而无需改动核心。

mpipe 不执行动态分配：缓冲区来自在流水线启动时确定大小的池，而协商路径上的一切都是固定大小的、按值（by value）
持有。代价落在栈上。协商运行在 :c:func:`mpipe_element_set_state` 内部，在调用它的任何线程上执行，
并会同时持有若干能力（capability）——请在该线程上为此预留空间，对于下面的示例而言，即运行 ``main`` 的那个线程。

mpipe 是可选的，而且并不总是合适的工具。一个驱动单个设备的应用程序，直接使用该设备的 API 会更合适。一旦多个设备必须就格式达成一致并相互传递缓冲区，mpipe 才体现出其价值。

构建流水线
*******************

应用程序包含 ``<zephyr/mpipe/mpipe.h>``，仅此而已，即可使用整个核心 API；它实例化的每个元素还会添加该元素自己的头文件。

元素是应用程序拥有的普通对象；mpipe 不分配其中的任何一个。每种元素类型都有自己的初始化函数，接收该类型和一个 id：

.. code-block:: c

   /* 具体元素类型来自插件；每个都有自己的头文件。 */
   static struct mpipe pipe;
   static struct my_src source;
   static struct my_sink sink;

   ret = mpipe_pipeline_init(&pipe, PIPE_ID);
   ret = my_src_init(&source, SRC_ID);
   ret = my_sink_init(&sink, SINK_ID);

Id 只需在流水线内唯一即可。元素通过属性（property）配置，这就是元素如何在不让调用者知道其具体类型的情况下被设置：

.. code-block:: c

   ret = mpipe_object_set_properties((struct mpipe_object *)&source,
                                     MY_SRC_PROP_PATH, "/SD:/in.bin",
                                     MPIPE_PROP_LIST_END);

然后它们被添加到流水线中，顺序任意，并按流顺序链接：

.. code-block:: c

   ret = mpipe_bin_add((struct mpipe_bin *)&pipe,
                       (struct mpipe_element *)&source,
                       (struct mpipe_element *)&sink, NULL);

   ret = mpipe_element_link((struct mpipe_element *)&source,
                            (struct mpipe_element *)&sink, NULL);

类型转换是明确定义的，因为每个元素将其基类作为第一个成员嵌入。链接会拒绝能力不可能相交的一对元素，因此不可能的图在构建时而非启动时就会失败。

将流水线设置为 ``MPIPE_STATE_PLAYING`` 并不是直接跳到该状态。流水线及其子元素按顺序逐步经过各个状态，
``READY`` 到 ``PAUSED`` 再到 ``PLAYING``，这就是为什么格式在途中被协商、池在途中被启动。

然后应用程序观察流水线的消息通道，既用于了解运行如何结束，也用于对失败采取行动。错误消息会指明产生它的元素及其所处的阶段，
因此应用程序可以报告"元素 3 的能力协商失败"，而不仅仅是"运行停止了"。将图恢复为 ``MPIPE_STATE_READY`` 会将其拆除：

.. code-block:: c

   /* 需要 CONFIG_ZBUS_MSG_SUBSCRIBER=y */
   ZBUS_MSG_SUBSCRIBER_DEFINE(main_sub);

   struct zbus_channel *bus = mpipe_element_get_bus_chan((struct mpipe_element *)&pipe);

   ret = zbus_chan_add_obs(bus, &main_sub, K_FOREVER);

   if (mpipe_element_set_state((struct mpipe_element *)&pipe, MPIPE_STATE_PLAYING) != 0) {
           /* 拒绝的元素仍处于其先前状态 */
   }

   do {
           ret = zbus_sub_wait_msg(&main_sub, &chan, &msg, K_FOREVER);
   } while ((msg.type & (MPIPE_MESSAGE_ERROR | MPIPE_MESSAGE_EOS)) == 0);

   (void)mpipe_element_set_state((struct mpipe_element *)&pipe, MPIPE_STATE_READY);

元素、pad 和链接
************************

每个 mpipe *元素* 通过将其作为第一个成员嵌入而派生自 :c:struct:`mpipe_object`。对象层携带框架对所持任何对象所需的内容：
一个 id、持有它的容器、列表链接和属性回调。在其之上，:c:struct:`mpipe_element` 添加状态机和 pad，
元素基类对其进行特化。仅携带数据的类型——能力、消息、调度——是该层级之外的普通结构体：

.. graphviz::
   :align: center
   :caption: 继承是结构体嵌入，因此向上转型是一个普通的 C 类型转换。

   digraph inheritance {
     rankdir=BT;
     node [shape=box, style=filled, fillcolor="#e8e8e8", fontname="sans"];

     object    [label="mpipe_object", fillcolor="#d0d8e8"];
     element   [label="mpipe_element"];

     src       [label="mpipe_src"];
     sink      [label="mpipe_sink"];
     transform [label="mpipe_transform"];
     parser    [label="mpipe_parser"];
     bin       [label="mpipe_bin"];
     pipeline  [label="mpipe"];

     element -> object;
     src -> element;
     sink -> element;
     transform -> element;
     parser -> element;
     bin -> element;
     pipeline -> bin;

     subgraph cluster_data {
       label="plain data, outside the hierarchy";
       fontname="sans";
       style=dashed;
       color="#999999";
       node [style="filled,dashed", fillcolor="#f5f5f5"];
       structure [label="mpipe_structure"];
       value     [label="mpipe_value"];
       message   [label="mpipe_message"];
       dispatch  [label="mpipe_dispatch"];
     }
   }

* :c:struct:`mpipe_src` 产生缓冲区，只有源 pad。它还驱动协商，因为它位于图的头部。
* :c:struct:`mpipe_sink` 消费缓冲区，只有汇 pad。
* :c:struct:`mpipe_transform` 各有一个，将输入转换为输出。
* :c:struct:`mpipe_parser` 将无格式的字节流切割为完整的帧，这与将一种格式转换为另一种格式是不同的工作。
* :c:struct:`mpipe_bin` 持有其他元素，并按转换所需的顺序向其转发状态变更。
* :c:struct:`mpipe` 是顶层 bin：它拥有流线程和消息通道。

:c:struct:`mpipe_pad` 是两个元素相遇之处。它携带方向（源或汇）、它所链接的对端、在其上协商的能力，以及框架分发的回调：
``chain_fn`` 接收缓冲区，``query_fn`` 应答查询，``event_fn`` 处理事件。链接两个元素就是将一个源 pad 链接到一个汇 pad，流的每一跳都是这样一个对。

状态机
*****************

元素处于三种状态之一，并在相邻状态之间一次一步移动：

.. graphviz::
   :align: center
   :caption: 每个转换做什么。

   digraph states {
     rankdir=LR;
     node [shape=box, style="rounded,filled", fillcolor="#e8e8e8", fontname="sans"];
     edge [fontname="sans", fontsize=10];

     READY -> PAUSED   [label=" negotiate the format,\l settle and start the pools\l"];
     PAUSED -> PLAYING [label=" start the source thread\l"];
     PLAYING -> PAUSED [label=" pause the source thread,\l keep what is queued\l"];
     PAUSED -> READY   [label=" flush, stop the pools,\l drop the negotiated formats\l"];
   }

``READY`` 意味着已构建并链接，不持有任何格式和缓冲区。``READY`` 到 ``PAUSED`` 的转换是工作发生之处：源驱动整个图的能力协商，缓冲区池查询确定谁提供缓冲区以及提供多少，然后池被启动。

转换的方向决定 bin 处理其子元素的顺序：

* 向**上**时，子元素从汇向源方向转换，因此下游元素在任何东西被推入之前就处于就绪状态。
* 向**下**时，子元素从源向汇方向转换，因此没有元素继续向已被拆除的元素生产。

失败的转换不会回滚。拒绝转换的元素保持在其原处，而已经移动的元素保持其新状态，这是有意为之：结果图精确显示哪个元素拒绝了、在哪个转换中拒绝了。

能力协商
**********************

**能力**（capability）描述跨越链接的数据：一种媒体类型加上一组字段，每个字段是一个 :c:enum:`mpipe_caps_field`
 标识符与一个 :c:struct:`mpipe_value` 配对。它是一个 :c:struct:`mpipe_structure`，一个按值持有的固定大小类型：

.. code-block:: c

   struct mpipe_structure s;

   mpipe_structure_init_fields(&s, MPIPE_MEDIA_VIDEO,
       MPIPE_CAPS_PIXEL_FORMAT, MPIPE_TYPE_UINT, VIDEO_PIX_FMT_RGB565,
       MPIPE_CAPS_IMAGE_WIDTH, MPIPE_TYPE_UINT_RANGE, 16, 1280, 2,
       MPIPE_CAPS_IMAGE_HEIGHT, MPIPE_TYPE_UINT_RANGE, 16, 720, 2,
       MPIPE_CAPS_END);

一个字段要么持有单个值，要么持有写为 ``[min, max, step]`` 的范围，因此上述能力覆盖从 16 到 1280、步长为 2 的所有宽度。
两个能力相交当且仅当它们共享一种媒体类型、至少有一个共同的字段标识符，且每个共享字段的值相交。结果是两者的并集：共享字段持有相交后的值，
只有一方持有的字段原样通过——这正是约束能够沿着本身不关心它的元素链传递的原因。*ANY* 能力不约束任何东西，与任何东西相交——这是 pad 在协商之前所持有的——而*空*能力不携带任何字段，与任何东西都不相交。

源在 ``READY`` 到 ``PAUSED`` 时驱动协商，分两个阶段：

.. mermaid::
   :align: center
   :caption: 能力协商，由源在 READY 到 PAUSED 时驱动
   :alt: 时序图，显示能力查询从源 pad 经过 transform 的两个 pad 到汇，应答返回，然后源将格式固定，能力事件沿同一路径传播，每个元素用 set_caps 应用它。

   %%{init: {'themeVariables': {'fontSize': '18px'}, 'sequence':
    {'actorFontSize': 18, 'messageFontSize': 18, 'noteFontSize': 18}}}%%
   sequenceDiagram
     autonumber
     participant so as src pad
     participant ti as sink pad
     participant to as src pad
     participant si as sink pad
     box rgba(79, 143, 214, 0.18) Source
     participant so
     end
     box rgba(148, 108, 196, 0.18) Transform
     participant ti
     participant to
     end
     box rgba(76, 168, 128, 0.18) Sink
     participant si
     end

     Note over so, si: Pass 1 - the caps query
     so ->> ti: can you take this format?
     ti ->> to: transform_caps()
     to ->> si: can you take this format?
     si -->> to: what I accept
     to ->> ti: transform_caps() back
     ti -->> so: what the chain accepts
     so ->> so: fixate to one format

     Note over so, si: Pass 2 - the caps event
     so ->> ti: this is the format
     ti ->> to: transform_caps(), narrowed
     to ->> si: this is the format
     si ->> si: set_caps()
     to ->> ti: set_caps() on both sides
     so ->> so: set_caps()

能力查询向下游传播，每个元素在询问其自身下游之前先将其与支持的能力取交集，应答返回时被收窄为整条链的公共部分。如果某个元素拒绝，源只是提供其支持的下一个格式，而不是让协商失败。

transform 是有趣的情况，因为其两侧可能讲不同的格式：解码器接收一种格式并产生另一种格式。它们不必如此——一个就地工作的元素在其所在之处重写缓冲区，
因此相同的格式跨越它——但当它们不同时，``transform_caps`` 钩子是将能力从元素一侧映射到另一侧可能是什么的东西。
查询以两个方向穿过该元素：向外询问下游对端，返回时将应答重新表达为输入侧的术语。

应答可能仍持有范围，因此源将其**固定**（fixate）——每个范围缩减为单个值——并将结果作为能力事件向下游通告。每个元素通过其 ``set_caps`` 钩子应用其一侧，
硬件正是在此处被实际配置。

由于 pad 持有单个能力而非一组，支持多种格式的元素按索引遍历：框架先询问其能力 0，然后 1，依此类推，直到它报告没有更多了。
格式来自设备的元素通过询问其驱动来应答每个索引，因此无需预先物化任何东西。

缓冲区池协商
***********************

仅凭格式无法说明一个图需要多少缓冲区、它们必须多大、必须如何对齐、或谁的池提供它们。第二个查询在格式固定后立即、在同一转换中解决这些问题：

.. mermaid::
   :align: center
   :caption: 缓冲区池协商，在格式固定后立即进行
   :alt: 时序图，显示缓冲区池查询向下游传播到汇，汇提出池或配置，每个元素在提案返回上游时决定并启动其自身的池。

   %%{init: {'themeVariables': {'fontSize': '18px'}, 'sequence':
    {'actorFontSize': 18, 'messageFontSize': 18, 'noteFontSize': 18}}}%%
   sequenceDiagram
     autonumber
     participant so as src pad
     participant ti as sink pad
     participant to as src pad
     participant si as sink pad
     box rgba(79, 143, 214, 0.18) Source
     participant so
     end
     box rgba(148, 108, 196, 0.18) Transform
     participant ti
     participant to
     end
     box rgba(76, 168, 128, 0.18) Sink
     participant si
     end

     so ->> ti: buffer pool query
     ti ->> to: forwarded downstream first
     to ->> si: buffer pool pool query
     si -->> to: propose_buffer_pool()
     to ->> to: decide_buffer_pool(), start out_pool
     ti -->> so: propose_buffer_pool()
     so ->> so: decide_buffer_pool(), start pool

查询向下传播到汇，提案在返回上游途中被写出，因此元素在决定任何东西之前总是握有其下游的提案。

transform 的两侧独立确定：``decide_buffer_pool`` 使用其下游提出的内容确定**输出**池，
而 ``propose_buffer_pool`` 用该元素在其**输入**上所需的内容应答上游查询。例外是直通（passthrough），其中一个缓冲区跨越元素，只有一个池需要确定。

提案要么是整个池，要么是裸配置。提供池让上游元素采用它以避免拷贝；提供配置陈述要求而不交出任何东西。无论如何，需求只有通过
 :c:func:`mpipe_buffer_pool_set_config` 才能到达提案者仍拥有的池，池的所有者对其进行验证、钳制或拒绝。

谁启动池就由谁停止，在 ``PAUSED`` 到 ``READY`` 时。这种对称性使停止和重放表现得像首次运行。

缓冲区流
***********

**缓冲区流是零拷贝的。** 每个产生数据的元素拥有一个 :c:struct:`mpipe_buffer_pool`，而池是一个
 vtable——``configure``、``set_config``、``start``、``stop``、``acquire_buffer``、``release_buffer``——覆盖任何支撑它的东西。这种间接性让插件交出其驱动已拥有的缓冲区而非其副本，因此摄像头捕获的帧到达显示器时从未被移动。元素之间传递的是引用，而非像素。

缓冲区是 Zephyr :c:struct:`net_buf` 分配，旁边有一个 :c:struct:`mpipe_buffer_meta` 携带框架需要了解的信息：
拥有它的池、其中多少是有效的、时间戳。

:c:func:`mpipe_push_buffer` 将缓冲区向下游推进：对于每一跳，它取源 pad 的对端，检查该 pad 的刷新门，
调用其 ``chain_fn``，并跟随该元素产生的缓冲区到下一个元素。NULL 输出意味着缓冲区被消费，推进停止。链函数拥有其接收的缓冲区，即使失败也会释放它，因此所有权从不依赖于所走的错误路径。

流水线运行时
****************

流水线自身的线程驱动源：它获取缓冲区并向下游推进，直到源报告其数据结束，此时它向下游发送流结束事件并暂停自身。需要解耦图的两半到不同线程的元素，通过在它们之间放置一个排队元素来实现。

拆除正在运行的图需要仔细排序，而这个顺序正是它不丢失数据或不死锁的原因：

* ``PLAYING`` 到 ``PAUSED`` 只是暂停源线程。任何已排队的内容都被保留，因此恢复继续而无损失。这是暂停，不是拆除。
* ``PAUSED`` 到 ``READY`` 在子元素拆除其池*之前*在每个 pad 上抬起刷新门，因此仍在途中的缓冲区被丢弃，而不是被推进到已被拆除的元素中。流线程只在子元素排空*之后*才 join，因为仍持有该线程在满队列中的子元素否则会使 join 死锁。

消息通过流水线的消息通道（一个可用 :c:func:`mpipe_element_get_bus_chan` 访问的 zbus 通道）
传递到应用程序。消息携带某事发生之处——发出它的元素——以及发生了什么：一个类型，加上在失败时一个指明失败阶段的域和一个说明原因的 errno。
它不携带面向人类的字符串；描述失败的句子属于检测到它的站点的日志，而应用程序按域和 errno 分支。

具有多个汇的流水线每个汇产生一个流结束消息。流水线对它们计数，只传递最后一个，因此应用程序恰好被通知一次，且不会在某个分支仍在运行时拆除图。

编写元素
******************

元素在框架之外编写，无需对其做任何更改。它将其基类之一作为第一个成员嵌入，用其自身的 id 调用该基类的 init，并只覆盖它关心的内容：

.. code-block:: c

   struct my_sink {
           struct mpipe_sink sink;   /* 必须是第一个 */
           const struct device *dev;
   };

   int my_sink_init(struct my_sink *self, uint8_t id)
   {
           int ret = mpipe_sink_init(&self->sink, id);

           if (ret != 0) {
                   return ret;
           }

           self->sink.sink_pad.enum_caps_fn = my_sink_enum_caps;
           self->sink.set_caps = my_sink_set_caps;

           return 0;
   }

覆盖 ``change_state`` 的元素必须链接到其基类，基类执行每个元素都被期望做的能力重置和池拆除。

另一半是说明该元素支持什么。构建时已知的能力是一个 ``static const struct mpipe_structure``，
元素从中拷贝；``MPIPE_STRUCTURE_DEFINE`` 将一个放入 ``.rodata``；多个则是它们的数组。
由设备支撑的元素改为在其 ``enum_caps_fn`` 中通过询问驱动来构建每个能力，而由应用程序配置的元素从属性中获取。

配置选项
*********************

* :kconfig:option:`CONFIG_MPIPE` 启用框架。每个插件有自己的选项并贡献自己的 Kconfig 文件。
* :kconfig:option:`CONFIG_MPIPE_STRUCTURE_MAX_FIELDS` 确定单个能力的大小。按能在一个交集中相遇的最大字段并集来定大小，而不是按元素设置的字段数，因为交集会携带只有一方约束的字段。
* :kconfig:option:`CONFIG_MPIPE_NET_BUF_POOL_COUNT` 确定共享 ``net_buf`` 池的大小：所有流水线在途缓冲区的总和。
* :kconfig:option:`CONFIG_MPIPE_BIN_MAX_CHILDREN` 限制一个 bin 中的元素数，这确定了状态变更期间用于排序它们的数组的大小。
* :kconfig:option:`CONFIG_MPIPE_THREADS_NUM`、:kconfig:option:`CONFIG_MPIPE_THREAD_STACK_SIZE` 和 :kconfig:option:`CONFIG_MPIPE_THREAD_DEFAULT_PRIORITY` 配置流水线取用的池化线程。
* :kconfig:option:`CONFIG_MPIPE_WORKQUEUE` 让元素将有限的工作项卸载到共享优先级工作队列。
* :kconfig:option:`CONFIG_MPIPE_RPC` 构建运行其处理在另一个核心上的客户端侧元素。
* :kconfig:option:`CONFIG_MPIPE_FAKE_SRC` 提供合成数据源，用于在真实源需要硬件时验证图。

API 参考
*************

.. doxygengroup:: mpipe_framework
