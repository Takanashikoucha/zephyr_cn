.. _mailboxes_v2:

邮箱
#########

:dfn:`邮箱`（mailbox）是一种内核对象，提供超越消息队列对象能力的
增强消息队列功能。
邮箱允许线程同步或异步地收发任意大小的消息。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的邮箱（仅受可用 RAM 限制）。
每个邮箱通过其内存地址引用。

邮箱具有以下关键属性：

* 一个**发送队列**，保存已发送但尚未接收的消息。

* 一个**接收队列**，保存正在等待接收消息的线程。

邮箱在使用前必须初始化。初始化会将两个队列都置为空。

邮箱允许线程（但不允许 ISR）交换消息。
发送消息的线程称为**发送线程**，
接收消息的线程称为**接收线程**。
每条消息只能被一个线程接收
（即不支持点到多点或广播消息）。

使用邮箱交换的消息以非匿名方式处理，
使得参与交换的两个线程都能知道
（甚至指定）对方线程的身份。

消息格式
=============

**消息描述符**是一个数据结构，
指定消息数据的位置，
以及消息应如何被邮箱处理。
发送线程和接收线程访问邮箱时都提供消息描述符。
邮箱使用消息描述符在兼容的发送线程和接收线程之间
执行消息交换。
邮箱还会在交换过程中更新消息描述符的某些字段，
使两个线程都能了解发生了什么。

邮箱消息包含零个或多个字节的**消息数据**。
消息数据的大小和格式由应用定义，
可以一条消息接一条消息地变化。

**消息缓冲区**是由发送或接收消息数据的线程提供的内存区域。
数组或结构体变量通常可用于此目的。

两种消息数据都没有的消息称为**空消息**。

.. note::
    消息缓冲区存在但实际数据为零字节的消息
    *不是*空消息。

消息生命周期
=================

消息的生命周期很简单。
消息在发送线程将其交给邮箱时创建。
之后消息由邮箱所有，直到交给接收线程。
接收线程可以在从邮箱接收到消息时
提取消息数据，也可以在随后第二次邮箱操作期间
提取数据。只有当数据提取发生后，
消息才会被邮箱删除。

线程兼容性
==================

发送线程可以指定要向其发送消息的线程地址，
或者通过指定 :c:macro:`K_ANY` 发送给任意线程。
同样，接收线程可以指定希望从其接收消息的线程地址，
或者通过指定 :c:macro:`K_ANY` 从任意线程接收消息。
只有当发送线程和接收线程的要求都满足时，
消息才会被交换；这样的线程称为**兼容**。

例如，如果线程 A 将消息发送给线程 B（且仅发送给线程 B），
那么当线程 B 尝试从线程 A 接收消息时，
或线程 B 尝试从任意线程接收消息时，
该消息会被线程 B 接收。
如果线程 B 尝试从线程 C 接收消息，
交换不会发生。即使线程 C 尝试从线程 A（或从任意线程）
接收消息，该消息也永远不会被线程 C 接收。

消息流控
==================

邮箱消息可以**同步**或**异步**交换。
在同步交换中，发送线程阻塞，
直到消息被接收线程完全处理。
在异步交换中，发送线程在消息被另一个线程接收之前
不等待即继续执行；这使得发送线程可以在消息
交给接收线程并完全处理*之前*
做其他工作（例如收集将用于下一条消息的数据）。
某次消息交换使用的技术由发送线程决定。

同步交换技术提供了一种隐式的流控形式，
防止发送线程以快于接收线程消耗消息的速度
生成消息。异步交换技术提供了一种显式的流控形式，
允许发送线程在发送后续消息之前
判断之前发送的消息是否仍然存在。

实现
**************

定义邮箱
==================

邮箱使用类型为 :c:struct:`k_mbox` 的变量定义。
之后必须通过调用 :c:func:`k_mbox_init` 进行初始化。

以下代码定义并初始化一个空邮箱。

.. code-block:: c

    struct k_mbox my_mailbox;

    k_mbox_init(&my_mailbox);

或者，可以通过调用 :c:macro:`K_MBOX_DEFINE`
在编译时定义并初始化一个邮箱。

以下代码与上面代码段的效果相同。

.. code-block:: c

    K_MBOX_DEFINE(my_mailbox);

消息描述符
==================

消息描述符是类型为 :c:struct:`k_mbox_msg` 的结构体。
只应使用下面列出的字段；其他字段仅供邮箱内部使用。

*info*
    一个 32 位值，在消息发送方和接收方之间交换，
    其含义由应用定义。该交换是双向的，
    允许发送方在任何消息交换期间
    向接收方传递一个值，
    也允许接收方在同步消息交换期间
    向发送方传递一个值。

*size*
    消息数据的大小（以字节计）。发送空消息时
    或发送不含实际数据的消息缓冲区时，
    将其设为零。接收消息时，
    将其设为希望获取的最大数据量，
    或者在不需要消息数据时设为零。
    消息接收后，邮箱用实际交换的数据字节数
    更新该字段。

*tx_data*
    指向发送线程消息缓冲区的指针。
    发送空消息时将其设为 ``NULL``。
    接收消息时保持该字段未初始化。

*tx_target_thread*
    期望的接收线程的地址。
    将其设为 :c:macro:`K_ANY`
    以允许任意线程接收该消息。
    接收消息时保持该字段未初始化。
    消息接收后，邮箱用实际接收者的地址
    更新该字段。

*rx_source_thread*
    期望的发送线程的地址。
    将其设为 :c:macro:`K_ANY`
    以接收任意线程发送的消息。
    发送消息时保持该字段未初始化。
    消息放入邮箱时，邮箱用实际发送者的地址
    更新该字段。

发送消息
================

线程发送消息时，首先创建其消息数据（如有）。

接着，发送线程创建一个消息描述符，
如上一节所述，描述要发送的消息。

最后，发送线程调用邮箱发送 API 启动消息交换。
如果当前有兼容的接收线程正在等待，
消息会立即交给该接收线程。
否则，消息被添加到邮箱的发送队列。

发送队列上可以同时存在任意数量的消息。
发送队列中的消息按发送线程的优先级排序。
优先级相同的消息按最旧的消息最先被接收的顺序排列。

对于同步发送操作，操作通常在接收线程
既接收了消息又提取了消息数据时完成。
如果在发送线程指定的等待期结束前
消息未被接收，消息从邮箱的发送队列中移除，
发送操作失败。发送操作成功完成后，
发送线程可以检查消息描述符以确定
哪个线程接收了消息、交换了多少数据，
以及接收线程提供的应用定义的 info 值。

.. note::
    同步发送操作可能会无限期地阻塞发送线程，
    即使线程指定了最大等待期。
    等待期只限制邮箱在消息被另一个线程接收之前
    等待多久。一旦消息被接收，
    接收线程提取消息数据并解除发送线程阻塞
    所花费的时间*没有*上限。

对于异步发送操作，操作总是立即完成。
这使得发送线程无论消息是立即交给接收线程
还是被添加到发送队列，都可以继续处理。
发送线程可以可选地指定一个信号量，
当消息被邮箱删除时（例如，当消息被接收线程
接收并提取其数据后）邮箱释放该信号量。
信号量的使用使得发送线程可以轻松地实现
流控机制，确保邮箱在任何时刻
最多只保存来自某个发送线程（或一组发送线程）
应用指定数量的消息。

.. note::
    异步发送消息的线程无法确定
    哪个线程接收了消息、交换了多少数据，
    或接收线程提供的应用定义的 info 值。

发送空消息
-------------------------

以下代码使用邮箱同步地向任意想要一个的消费者线程
传递 4 字节随机值。消息的 "info" 字段
足以承载要交换的信息，因此消息的数据部分未被使用。

.. code-block:: c

    void producer_thread(void)
    {
        struct k_mbox_msg send_msg;

        while (1) {

            /* generate random value to send */
            uint32_t random_value = sys_rand32_get();

            /* prepare to send empty message */
            send_msg.info = random_value;
            send_msg.size = 0;
            send_msg.tx_data = NULL;
            send_msg.tx_target_thread = K_ANY;

            /* send message and wait until a consumer receives it */
            k_mbox_put(&my_mailbox, &send_msg, K_FOREVER);
        }
    }

使用消息缓冲区发送数据
-----------------------------------

以下代码使用邮箱同步地将可变大小的请求
从生产者线程传递给任意想要它的消费者线程。
消息的 "info" 字段用于交换
关于每个线程可处理的最大消息缓冲区大小的信息。

.. code-block:: c

    void producer_thread(void)
    {
        char buffer[100];
        int buffer_bytes_used;

        struct k_mbox_msg send_msg;

        while (1) {

            /* generate data to send */
            ...
            buffer_bytes_used = ... ;
            memcpy(buffer, source, buffer_bytes_used);

            /* prepare to send message */
            send_msg.info = buffer_bytes_used;
            send_msg.size = buffer_bytes_used;
            send_msg.tx_data = buffer;
            send_msg.tx_target_thread = K_ANY;

            /* send message and wait until a consumer receives it */
            k_mbox_put(&my_mailbox, &send_msg, K_FOREVER);

            /* info, size, and tx_target_thread fields have been updated */

            /* verify that message data was fully received */
            if (send_msg.size < buffer_bytes_used) {
                printf("some message data dropped during transfer!");
                printf("receiver only had room for %d bytes", send_msg.info);
            }
        }
    }

接收消息
==================

线程接收消息时，首先创建一个消息描述符，
描述其想要接收的消息。然后调用其中一个
邮箱接收 API。邮箱搜索其发送队列，
从找到的第一个兼容线程处取出消息。
如果不存在兼容线程，接收线程可以选择等待。
如果在接收线程指定的等待期结束前
没有出现兼容线程，接收操作失败。
接收操作成功完成后，接收线程
可以检查消息描述符以确定哪个线程发送了消息、
交换了多少数据，
以及发送线程提供的应用定义的 info 值。

任意数量的接收线程可以同时等待在邮箱的
接收队列上。线程按其优先级排序；
优先级相同的线程按最先开始等待的
最先接收消息的顺序排列。

.. note::
    由于消息描述符规定的线程兼容性约束，
    接收线程并不总是按先进先出（FIFO）顺序
    接收消息。例如，如果线程 A 等待
    只从线程 X 接收消息，然后线程 B 等待
    从线程 Y 接收消息，那么来自线程 Y
    发给任意线程的传入消息会交给线程 B，
    而线程 A 继续等待。

接收线程既控制其从传入消息中提取的数据量，
也控制数据最终去向。线程可以选择
获取消息中的所有数据、只获取数据的前半部分，
或不获取任何数据。同样，线程可以选择
将数据复制到其选择的消息缓冲区中。

以下各节概述了接收线程在提取消息数据时
可采用的各种方法。

接收时提取数据
-------------------------------

线程提取消息数据最直接的方式是
在接收消息时指定一个消息缓冲区。
线程同时指明消息缓冲区的位置（不得为 ``NULL``）
及其大小。

邮箱作为接收操作的一部分，
将消息数据复制到消息缓冲区。
如果消息缓冲区不足以容纳消息的全部数据，
未复制的数据将丢失。如果消息不足以
用数据填满缓冲区的全部空间，
消息缓冲区的未使用部分保持不变。
在所有情况下，邮箱都会更新接收线程的
消息描述符，指示复制了多少数据字节（如有）。

立即数据提取技术最适合消息较小
且消息最大尺寸可预先知晓的场景。

以下代码使用邮箱处理来自任意生产者线程的
可变大小请求，使用立即数据提取技术。
消息的 "info" 字段用于交换
关于每个线程可处理的最大消息缓冲区大小的信息。

.. code-block:: c

    void consumer_thread(void)
    {
        struct k_mbox_msg recv_msg;
        char buffer[100];

        int i;
        int total;

        while (1) {
            /* prepare to receive message */
            recv_msg.info = 100;
            recv_msg.size = 100;
            recv_msg.rx_source_thread = K_ANY;

            /* get a data item, waiting as long as needed */
            k_mbox_get(&my_mailbox, &recv_msg, buffer, K_FOREVER);

            /* info, size, and rx_source_thread fields have been updated */

            /* verify that message data was fully received */
            if (recv_msg.info != recv_msg.size) {
                printf("some message data dropped during transfer!");
                printf("sender tried to send %d bytes", recv_msg.info);
            }

            /* compute sum of all message bytes (from 0 to 100 of them) */
            total = 0;
            for (i = 0; i < recv_msg.size; i++) {
                total += buffer[i];
            }
        }
    }

之后使用消息缓冲区提取数据
--------------------------------------------

接收线程可以选择在接收消息时
推迟消息数据提取，以便稍后
将数据提取到消息缓冲区中。
线程通过指定消息缓冲区位置为 ``NULL``
以及一个表示其愿意稍后提取的最大数据量的大小
来实现这一点。

邮箱不会作为接收操作的一部分
复制任何消息数据。
但是，邮箱仍会更新接收线程的消息描述符，
指示有多少数据字节可供提取。

接收线程必须按以下方式响应：

* 如果消息描述符大小为零，则要么发送方的消息
  不含数据，要么接收线程不想接收任何数据。
  接收线程无需采取进一步操作，
  因为邮箱已完成数据提取并删除了消息。

* 如果消息描述符大小非零且接收线程仍想提取数据，
  线程必须调用 :c:func:`k_mbox_data_get`
  并提供一个足以容纳数据的消息缓冲区。
  邮箱将数据复制到消息缓冲区并删除消息。

* 如果消息描述符大小非零且接收线程*不想*提取数据，
  线程必须调用 :c:func:`k_mbox_data_get`
  并指定消息缓冲区为 ``NULL``。
  邮箱不复制数据即删除消息。

后续数据提取技术适用于不希望立即提取消息数据的应用。
例如，当内存限制使得接收线程
无法总是提供足以容纳最大可能传入消息的
消息缓冲区时，可以使用该技术。

以下代码使用邮箱的延迟数据提取机制，
仅当消息满足某些条件时
才从生产者线程获取消息数据，
从而消除不必要的数据复制。
发送方提供的消息 "info" 字段用于对消息分类。

.. code-block:: c

    void consumer_thread(void)
    {
        struct k_mbox_msg recv_msg;
        char buffer[10000];

        while (1) {
            /* prepare to receive message */
            recv_msg.size = 10000;
            recv_msg.rx_source_thread = K_ANY;

            /* get message, but not its data */
            k_mbox_get(&my_mailbox, &recv_msg, NULL, K_FOREVER);

            /* get message data for only certain types of messages */
            if (is_message_type_ok(recv_msg.info)) {
                /* retrieve message data and delete the message */
                k_mbox_data_get(&recv_msg, buffer);

                /* process data in "buffer" */
                ...
            } else {
                /* ignore message data and delete the message */
                k_mbox_data_get(&recv_msg, NULL);
            }
        }
    }

建议使用
**************

当消息队列的能力不足时，
使用邮箱在线程之间传输数据项。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_NUM_MBOX_ASYNC_MSGS`

API 参考
*************

.. doxygengroup:: mailbox_apis
