.. _ipc_service:

IPC service
###########

.. contents::
   :local:
   :depth: 2

IPC service API 提供了一个在两个 domain 或 CPU 之间交换数据的接口。

Overview
========

一个 IPC service 通信通道由一个 instance 和一个或多个与该 instance 关联的 endpoint 组成。

一个 instance 是两个 domain 或 CPU 之间物理通信通道的外部表示。instance 的实际实现和内部表示因每个 backend 而异。

单个 instance 不直接用于在 domains/CPUs 之间发送数据。要发送和接收数据，用户必须在该 instance 中创建（注册）一个 endpoint。这使得两个感兴趣的 domain 之间可以建立连接。

单个 instance 可以拥有零个或多个 endpoint，可能带有不同的优先级，并可使用每个 endpoint 来交换数据。Endpoint 优先级排序和多 instance 能力在很大程度上取决于所使用的 backend。

endpoint 是用户必须用来在两个 domain（由 instance 连接）之间发送和接收数据的实体。endpoint 始终与一个 instance 关联。

instance 的创建交由 backend 完成，通常在初始化时进行。endpoint 的注册交由用户完成，通常在运行时进行。

该 API 不强制规定 backend 创建 instance 的方式，但强烈建议使用 devicetree 来获取 instance 的配置参数。目前，每个 backend 定义自己的 DT-compatible 配置，用于在启动时配置接口。

支持以下使用场景：

* 简单数据交换。
* 使用 no-copy API 的数据交换。

Simple data exchange
====================

要在 domain 或 CPU 之间发送数据，必须在一个 instance 上注册一个 endpoint。

参见以下示例：

.. note::

   在注册 endpoint 之前，必须使用 :c:func:`ipc_service_open_instance` 函数打开该 instance。


.. code-block:: c

   #include <zephyr/ipc/ipc_service.h>

   static void bound_cb(void *priv)
   {
      /* Endpoint bounded */
   }

   static void recv_cb(const void *data, size_t len, void *priv)
   {
      /* Data received */
   }

   static struct ipc_ept_cfg ept0_cfg = {
      .name = "ept0",
      .cb = {
         .bound    = bound_cb,
         .received = recv_cb,
      },
   };

   int main(void)
   {
      const struct device *inst0;
      struct ipc_ept ept0;
      int ret;

      inst0 = DEVICE_DT_GET(DT_NODELABEL(ipc0));
      ret = ipc_service_open_instance(inst0);
      ret = ipc_service_register_endpoint(inst0, &ept0, &ept0_cfg);

      /* Wait for endpoint bound (bound_cb called) */

      unsigned char message[] = "hello world";
      ret = ipc_service_send(&ept0, &message, sizeof(message));
   }

Data exchange using the no-copy API
===================================

如果 backend 支持 no-copy API，你可以使用它来直接读写共享内存区域。

参见以下示例：

.. code-block:: c

   #include <zephyr/ipc/ipc_service.h>
   #include <stdint.h>
   #include <string.h>

   static struct ipc_ept ept0;

   static void bound_cb(void *priv)
   {
      /* Endpoint bounded */
   }

   static void recv_cb_nocopy(const void *data, size_t len, void *priv)
   {
      int ret;

      ret = ipc_service_hold_rx_buffer(&ept0, (void *)data);
      /* Process directly or put the buffer somewhere else and release. */
      ret = ipc_service_release_rx_buffer(&ept0, (void *)data);
   }

   static struct ipc_ept_cfg ept0_cfg = {
      .name = "ept0",
      .cb = {
         .bound    = bound_cb,
         .received = recv_cb,
      },
   };

   int main(void)
   {
      const struct device *inst0;
      int ret;

      inst0 = DEVICE_DT_GET(DT_NODELABEL(ipc0));
      ret = ipc_service_open_instance(inst0);
      ret = ipc_service_register_endpoint(inst0, &ept0, &ept0_cfg);

      /* Wait for endpoint bound (bound_cb called) */
      void *data;
      unsigned char message[] = "hello world";
      uint32_t len = sizeof(message);

      ret = ipc_service_get_tx_buffer(&ept0, &data, &len, K_FOREVER);

      memcpy(data, message, len);

      ret = ipc_service_send_nocopy(&ept0, data, sizeof(message));
   }

Backends
========

实现 backend 所需的各项要求为 IPC service 提供了灵活性。这使得可以添加仅具备部分功能、面向特定使用场景的专用 backend。

backend 至少必须支持以下内容：

* 在初始化时创建 instance。
* 在运行时向 instance 注册 endpoint。

此外，backend 还可以支持以下内容：

* 在运行时从 instance 注销 endpoint。
* 在运行时关闭 instance。
* no-copy API。

每个 backend 可以有自己的限制和功能，使该 backend 独具特色并专用于特定使用场景。IPC service API 可以同时使用多个 backend，结合每个 backend 的优缺点。

.. toctree::
   :maxdepth: 1

   backends/ipc_service_icmsg.rst
   backends/ipc_service_icbmsg.rst

API Reference
=============

IPC service API
***************

.. doxygengroup:: ipc_service_api

IPC service backend API
***********************

.. doxygengroup:: ipc_service_backend
