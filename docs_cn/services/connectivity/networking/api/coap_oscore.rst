.. _coap_oscore_interface:

OSCORE 支持（:rfc:`8613`）
############################

.. contents::
    :local:
    :depth: 2


概述
========

Zephyr CoAP 库提供对 Object Security for Constrained RESTful
Environments（OSCORE，受限 RESTful 环境对象安全）的支持，
规范见 :rfc:`8613`。OSCORE 使用 COSE（CBOR Object Signing and Encryption，
CBOR 对象签名与加密）为 CoAP 消息提供端到端保护。

OSCORE 在应用层保护 CoAP 消息，提供：

1. **机密性**：消息负载和敏感选项被加密
2. **完整性**：消息通过 MAC 进行认证
3. **防重放**：序列号防止重放攻击
4. **对代理友好**：外层选项对路由保持可见

与 DTLS 不同，OSCORE 提供端到端安全，
能够经受不同传输协议（UDP、TCP、HTTP）之间的
代理转换。

其他 OSCORE 配置选项：

- :kconfig:option:`CONFIG_COAP_OSCORE_MAX_CONTEXTS`：OSCORE 安全上下文的最大数量
- :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_CACHE_SIZE`：每个服务跟踪的 OSCORE 交换数量
- :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS`：所跟踪的 OSCORE 交换的生命周期，
   用于保护延迟（separate）响应
- :kconfig:option:`CONFIG_COAP_OSCORE_CONTEXT_REUSE`：启用 OSCORE 跨重启的上下文复用支持
- :kconfig:option:`CONFIG_COAP_OSCORE_MASTER_SECRET_MAX_LEN`：OSCORE 主密钥（Master Secret）的最大长度（字节）
- :kconfig:option:`CONFIG_COAP_OSCORE_MASTER_SALT_MAX_LEN`：OSCORE 主加盐值（Master Salt）的最大长度（字节）

配置
=============

通过 :kconfig:option:`CONFIG_COAP_OSCORE` 启用 OSCORE 支持。该选项
依赖于 uoscore-uedhoc 模块和 PSA Crypto 支持：

.. code-block:: kconfig

   CONFIG_COAP_OSCORE=y
   CONFIG_UOSCORE=y
   CONFIG_PSA_CRYPTO=y

uoscore 模块会自动选择所需的 PSA crypto 算法（AES-CCM、
HKDF-SHA256 等）。

服务器用法
===========

要在 CoAP 服务上启用 OSCORE，使用
:c:macro:`COAP_SERVICE_DEFINE_OSCORE` 定义该服务
（DTLS 则使用 :c:macro:`COAPS_SERVICE_DEFINE_OSCORE`）。
该宏为每个服务静态分配 OSCORE 交换缓存。
安全上下文通过 Zephyr OSCORE API 单独创建，
并添加到共享池；应用不直接包含底层
uoscore-uedhoc 头文件。入站请求按其
Recipient ID 和 ID Context 匹配到正确的上下文，
因此单个服务可以为多个客户端提供服务，
每个客户端拥有自己的上下文：

.. code-block:: c

   #include <zephyr/net/coap_oscore.h>
   #include <zephyr/net/coap_service.h>

   static struct coap_oscore_context *my_oscore_ctx;

   static uint16_t my_service_port = 5683;

   /* Final argument "true" requires OSCORE for all requests. */
   COAP_SERVICE_DEFINE_OSCORE(my_service, NULL, &my_service_port,
                              COAP_SERVICE_AUTOSTART, true);

   int my_service_oscore_init(void)
   {
       /* coap_oscore_context_add() copies the key material, so these
        * buffers need not outlive the call and can live on the stack.
        */
       const uint8_t master_secret[16] = { /* ... */ };
       const uint8_t master_salt[8] = { /* ... */ };
       const uint8_t sender_id[] = { /* ... */ };
       const uint8_t recipient_id[] = { /* ... */ };

       struct coap_oscore_init_params params = {
           .master_secret = master_secret,
           .master_secret_len = sizeof(master_secret),
           .sender_id = sender_id,
           .sender_id_len = sizeof(sender_id),
           .recipient_id = recipient_id,
           .recipient_id_len = sizeof(recipient_id),
           .master_salt = master_salt,
           .master_salt_len = sizeof(master_salt),
           .aead_alg = COAP_OSCORE_AEAD_AES_CCM_16_64_128,
           .hkdf = COAP_OSCORE_HKDF_SHA_256,
           .fresh_master_secret_salt = true,
       };

       /* Add the context to the shared pool once its key material is
        * available. Call once per client identity (Recipient ID).
        */
       return coap_oscore_context_add(&params, &my_oscore_ctx);
   }

可一次性分配的上下文数量由
:kconfig:option:`CONFIG_COAP_OSCORE_MAX_CONTEXTS` 控制。使用
``coap_oscore_context_remove()`` 释放上下文。
上下文是引用计数的：只要某个
正在处理中的请求、活跃的交换或观察者
仍在引用该上下文，
``coap_oscore_context_remove()`` 就会返回 ``-EAGAIN``，
且该上下文会被保留。
等这些引用释放后重试移除即可。

当服务启用了 OSCORE（使用 ``OSCORE`` 宏创建，
且至少有一个上下文被添加到池中）时：

1. **入站请求**：服务器自动验证并解密 OSCORE 保护的
   请求（:rfc:`8613` 第 8.2 节）。资源处理函数
   收到解密后的 CoAP 消息，内部选项可见。

2. **出站响应**：服务器自动对源自 OSCORE 交换的
   响应和通知进行 OSCORE 保护（:rfc:`8613` 第 8.3 节）。
   某条出站消息是否必须被保护，按如下方式决定：

   - **同步响应**（在请求处理期间产生）
     会与每个服务的交换缓存进行匹配，
     找到匹配条目时予以保护。
     这些条目在 :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS` 后过期。
     在混合服务（同时有 OSCORE 和非 OSCORE 客户端）上，
     在交换缓存条目过期后发送同步响应，
     将产生明文响应。
   - **Observe 通知**基于观察者保存的 OSCORE
     状态进行保护，该状态在整个观察期间
     保持有效。
   - **延迟（separate）响应**（在请求处理函数
     返回后产生）会与每个服务的交换缓存进行匹配，
     找到匹配条目时予以保护。这些条目在
     :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS` 后过期。
     在混合服务（同时有 OSCORE 和非 OSCORE 客户端）上，
     在交换缓存条目过期后发送延迟响应，
     将产生明文响应。

3. **错误处理**：OSCORE 验证错误
   作为**不带** OSCORE 处理的简单 CoAP 响应
   发送（:rfc:`8613` 第 8.2 节）：
   - COSE 解码失败 → 4.02 Bad Option
   - 未找到安全上下文 → 4.01 Unauthorized
   - 解密失败 → 4.00 Bad Request

4. **OSCORE 必需**：如果服务定义时
   ``_oscore_required`` 参数设为 true，
   未受保护的请求将以 4.01 Unauthorized 拒绝。

5. **失败关闭（fail-closed）行为**：如果响应的 OSCORE 保护失败，
   服务器不会回退到发送明文响应。在
   OSCORE 必需的服务上，
   无法匹配到任何 OSCORE 状态的出站响应
   同样会被丢弃，而不是以明文发送。
   Observe 通知绝不会被降级。在混合服务上，
   任何（同步或延迟）响应
   如果其交换缓存条目已过期，
   就再也无法匹配，将以不受保护的方式发送。
   实际上这影响的是延迟（separate）响应，
   因为同步响应会匹配到
   请求处理期间刚创建的条目
   （参见第 2 项和 :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS`）。


已知限制
============================

1. **混合服务中交换过期后的明文响应**：在混合服务
   （同时服务 OSCORE 和非 OSCORE 客户端的服务）上，
   交换缓存条目已过期
   的响应再也无法匹配到其 OSCORE 状态，
   将以明文发送。
   这同时影响同步响应和延迟（separate）响应（参见
   :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS`）。对于任何
   承载敏感数据的服务，应将其定义为 OSCORE 必需
   （将 ``_oscore_required`` 参数传为 true，
   例如通过 :c:macro:`COAP_SERVICE_DEFINE_OSCORE`），
   而不是运行混合服务。
   OSCORE 必需的服务会拒绝未受保护的请求，
   并丢弃无法保护的响应，
   因此永远不会降级到明文。

安全上下文派生
============================

OSCORE 安全上下文从一组少量参数派生（:rfc:`8613` 第 3 节）：

**必需参数**：

- **Master Secret（主密钥）**：共享密钥（AES-CCM-16-64-128 通常为 16 字节）
- **Sender ID（发送方 ID）**：发送方的唯一标识符
- **Recipient ID（接收方 ID）**：接收方的唯一标识符

**可选参数**：

- **Master Salt（主加盐值）**：额外熵（推荐，通常为 8 字节）
- **ID Context（ID 上下文）**：额外的上下文标识符
- **AEAD 算法**：默认为 AES-CCM-16-64-128
- **KDF（密钥派生函数）**：默认为 HKDF-SHA-256

这些参数通常通过以下方式建立：

1. **预共享密钥**：在设备配置（provisioning）时配置
2. **EDHOC**：Ephemeral Diffie-Hellman Over COSE（基于 COSE 的临时 Diffie-Hellman，参见 uoscore-uedhoc 模块）

安全注意事项
=======================

1. **序列号溢出**：对于 AES-CCM-16-64-128，
   发送方序列号（SSN）不得超过 2^23-1。
   uoscore 库会强制该限制。

2. **主密钥保护**：主密钥必须安全存储（例如
   安全存储区，或从 EDHOC 派生）。

3. **跨重启的持久化**：如果重启后
   复用了相同的主密钥
   （即主密钥未重新派生，
   例如通过 EDHOC），
   则必须将发送方序列号
   持久化到非易失性存储器中，
   以防止 nonce 复用——
   nonce 复用会破坏机密性和完整性。
   接收方的重放窗口无需持久化：
   它保存在内存中，重启后
   按 :rfc:`8613` 附录 B.1.2 的描述
   使用 Echo 选项重新同步。

不支持 OSCORE 时的处理
-----------------------------------

当未启用 OSCORE 支持（:kconfig:option:`CONFIG_COAP_OSCORE` 未设置）时，
Zephyr CoAP 协议栈按
:rfc:`7252` 第 5.4.1 节为 OSCORE 选项
实现失败关闭行为：

**服务器行为**（当 ``CONFIG_COAP_OSCORE=n`` 时）：

- 带 OSCORE 选项的 **CON 请求**：返回 **4.02（Bad Option）** 响应
- 带 OSCORE 选项的 **NON 请求**：静默拒绝（丢弃）该消息
- 带 OSCORE 选项的 **响应**：CON 发送 RST，静默丢弃 NON/ACK

API 参考
=============

.. doxygengroup:: coap_oscore
