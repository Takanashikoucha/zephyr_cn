.. _pipes_v2:

管道
#####

:dfn:`管道`（pipe）是一种内核对象，允许一个线程向另一个线程发送字节流。管道支持高效的线程间通信，可用于同步地整体或部分传输数据块。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的管道，仅受可用 RAM 限制。每个管道都通过其内存地址来引用。

管道具有以下关键属性：

* 一个**大小**，指示管道环形缓冲区的容量。注意大小为 0 时定义的是一个没有环形缓冲区的管道。

管道在使用前必须初始化，初始化后管道为空。

线程与管道的交互方式如下：

- **写入**：线程将数据同步写入管道，可整体或部分写入。被接受的数据要么直接复制到等待的读取线程，要么复制到管道的环形缓冲区。如果环形缓冲区已满或根本不存在，该操作会阻塞，直到有足够空间可用或指定的超时到期。

- **读取**：线程从管道同步读取数据，可整体或部分读取。被接受的数据要么从管道的环形缓冲区复制，要么直接从等待的发送线程复制。如果环形缓冲区为空或根本不存在，该操作会阻塞，直到有数据可用或指定的超时到期。

- **重置**：线程可以重置管道，这会重置其内部状态，并以错误码结束所有挂起的读取和写入操作。

管道非常适合生产者-消费者模式，或线程间流式数据等场景。

实现
**************

管道使用类型为 :c:struct:`k_pipe` 的变量和一个字节缓冲区来定义，之后必须通过调用 :c:func:`k_pipe_init` 进行初始化。

以下代码定义并初始化一个空管道，其环形缓冲区可容纳 100 字节，并对齐到 4 字节边界：

.. code-block:: c

    uint8_t __aligned(4) my_ring_buffer[100];
    struct k_pipe my_pipe;

    k_pipe_init(&my_pipe, my_ring_buffer, sizeof(my_ring_buffer));

或者，可以使用 :c:macro:`K_PIPE_DEFINE` 宏在编译时定义并初始化一个管道，该宏同时定义管道及其环形缓冲区：

.. code-block:: c

    K_PIPE_DEFINE(my_pipe, 100, 4);

这与上面代码的效果相同。

当不使用环形缓冲区时，缓冲区指针参数应为 NULL，大小参数应为 0。

写入管道
================

通过调用 :c:func:`k_pipe_write` 将数据添加到管道。

以下示例演示使用管道将数据从生产者线程发送给一个或多个消费者线程。如果管道的环形缓冲区被填满，生产者线程会等待指定的时间。

.. code-block:: c

   struct message_header {
        size_t num_data_bytes; /* Example field */
        ...
    };

    void producer_thread(void)
    {
        int rc;
        uint8_t *data;
        size_t total_size;
        size_t bytes_written;

        while (1) {
            /* Craft message to send in the pipe */
            make_message(data, &total_size);
            bytes_written = 0;

            /* Write data to the pipe, handling partial writes */
            while (bytes_written < total_size) {
                rc = k_pipe_write(&my_pipe, &data[bytes_written], total_size - bytes_written, K_NO_WAIT);

                if (rc < 0) {
                    /* Error occurred */
                    ...
                    break;
                } else {
                    /* Partial or full write succeeded; adjust for next iteration */
                    bytes_written += rc;
                }
            }

            /* Reset bytes_written for the next message */
            bytes_written = 0;
            ...
        }
    }

从管道读取
==================

通过调用 :c:func:`k_pipe_read` 从管道获取数据。

以下示例基于上面的生产者线程示例，展示了一个处理生产者所生成数据的消费者线程。

.. code-block:: c

   struct message_header {
        size_t num_data_bytes; /* Example field */
        ...
    };

    void consumer_thread(void)
    {
        int rc;
        uint8_t buffer[128];
        size_t bytes_read = 0;
        struct message_header *header = (struct message_header *)buffer;

        while (1) {
            /* Step 1: Read the message header */
            bytes_read = 0;
       read_header:
            while (bytes_read < sizeof(*header)) {
                rc = k_pipe_read(&my_pipe, &buffer[bytes_read], sizeof(*header) - bytes_read, &bytes_read, K_NO_WAIT);

                if (rc < 0) {
                    /* Error occurred */
                    ...
                    goto read_header;
                }

                /* Adjust for partial reads */
                bytes_read += rc;
            }

            /* Step 2: Read the message body */
            bytes_read = 0;
            while (bytes_read < header->num_data_bytes) {
                rc = k_pipe_read(&my_pipe, &buffer[sizeof(*header) + bytes_read], header->num_data_bytes - bytes_read, K_NO_WAIT);

                if (rc < 0) {
                    /* Error occurred */
                    ...
                    goto read_header;
                }

                /* Adjust for partial reads */
                bytes_read += rc;
            }
            /* Successfully received the complete message */
        }
    }

重置管道
================

通过调用 :c:func:`k_pipe_reset` 重置管道。重置管道会重置其内部状态，并以错误码结束所有挂起操作。

以下示例演示在检测到严重错误时重置整个管道：

.. code-block:: c

    void monitor_thread(void)
    {
        while (1) {
            ...
            /* Critical error detected: reset the entire pipe to reset it. */
            k_pipe_reset(&my_pipe);
            ...
        }
    }

建议使用
**************

管道适用于在线程之间发送数据流。典型应用包括：

- 实现生产者-消费者模式。
- 在线程之间流式传输日志或数据包。
- 处理实时系统中的变长消息传递。

API 参考
*************

.. doxygengroup:: pipe_apis
