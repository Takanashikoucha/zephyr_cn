.. _coap_oscore_interface:

OSCORE Support (:rfc:`8613`)
############################

.. contents::
    :local:
    :depth: 2


Overview
========

Zephyr CoAP library 提供按 :rfc:`8613` 指定的 Object Security for Constrained RESTful Environments（OSCORE）支持。OSCORE 用 COSE（CBOR Object Signing and Encryption）提供 CoAP messages 的 end-to-end 保护。

OSCORE 在 application 层保护 CoAP messages（提供：

1. **Confidentiality**：Message payloads 和 sensitive options 被加密
2. **Integrity**：Messages 用 MAC 认证
3. **Replay protection**：Sequence numbers 防止 replay attacks
4. **Proxy-friendly**：Outer options 对 routing 保持可见

与 DTLS 不同（OSCORE 提供在不同 transport protocols（UDP、TCP、HTTP）之间 proxy translation 中存活的 end-to-end 安全。

额外 OSCORE configuration options：

- :kconfig:option:`CONFIG_COAP_OSCORE_MAX_CONTEXTS`：OSCORE security contexts 的最大数
- :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_CACHE_SIZE`：每个 service 跟踪的 OSCORE exchanges 数
- :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS`：用于保护 deferred（separate）responses 的跟踪 OSCORE exchanges 的 lifetime
- :kconfig:option:`CONFIG_COAP_OSCORE_CONTEXT_REUSE`：启用 OSCORE 对跨 reboots 的 context 复用支持
- :kconfig:option:`CONFIG_COAP_OSCORE_MASTER_SECRET_MAX_LEN`：OSCORE Master Secret 的最大长度（bytes）
- :kconfig:option:`CONFIG_COAP_OSCORE_MASTER_SALT_MAX_LEN`：OSCORE Master Salt 的最大长度（bytes）

Configuration
=============

用 :kconfig:option:`CONFIG_COAP_OSCORE` 启用 OSCORE 支持。此 option 依赖于 uoscore-uedhoc module 和 PSA Crypto support：

.. code-block:: kconfig

   CONFIG_COAP_OSCORE=y
   CONFIG_UOSCORE=y
   CONFIG_PSA_CRYPTO=y

Uoscore module 自动选择所需的 PSA crypto algorithms（AES-CCM、HKDF-SHA256 等）。

Server Usage
============

要在 CoAP service 上启用 OSCORE（用 :c:macro:`COAP_SERVICE_DEFINE_OSCORE`（或 DTLS 的 :c:macro:`COAPS_SERVICE_DEFINE_OSCORE`）定义 service。Macro 静态分配 per-service OSCORE exchange cache。Security contexts 通过 Zephyr OSCORE API 单独创建（并添加到共享 pool；applications 不直接包含底层 uoscore-uedhoc headers。Incoming requests 按其 Recipient ID 和 ID Context 匹配到正确的 context（因此单个 service 可服务多个 clients（每个带其自己的 context：

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

可一次性分配的 contexts 数由 :kconfig:option:`CONFIG_COAP_OSCORE_MAX_CONTEXTS` 控制。用 ``coap_oscore_context_remove()`` 释放 context。Contexts 为 reference-counted：当 in-flight request、active exchange 或 observer 仍引用 context 时（``coap_oscore_context_remove()`` 返回 ``-EAGAIN``（且 context 被保留。那些 references 被释放后重试移除。

当 service 为 OSCORE-enabled（用 ``OSCORE`` macro 创建且至少一个 context 被添加到 pool）：

1. **Incoming requests**：Server 自动验证并解密 OSCORE-protected requests（:rfc:`8613` Section 8.2）。Resource handlers 收到 Inner options 可见的 decrypted CoAP messages。

2. **Outgoing responses**：Server 自动 OSCORE-protect 源自 OSCORE exchange 的 responses 和 notifications（:rfc:`8613` Section 8.3）。给定 outgoing message 是否须被保护按如下决定：

   - **Synchronous responses**（在 request 处理期间产生）与 per-service exchange cache 匹配（找到匹配 entry 时保护。这些 entries 在 :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS` 后过期。在 mixed service（OSCORE 和 non-OSCORE clients）上（exchange cache entry 过期后发送 synchronous response 将导致 plaintext response。
   - **Observe notifications** 基于 observer 存储的 OSCORE state 保护（其存活于 observation 期间。
   - **Deferred（separate）responses**（在 request handler 返回后产生）与 per-service exchange cache 匹配（找到匹配 entry 时保护。这些 entries 在 :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS` 后过期。在 mixed service（OSCORE 和 non-OSCORE clients）上（exchange cache entry 过期后发送 deferred response 将导致 plaintext response。

3. **Error handling**：OSCORE verification errors 作为**无** OSCORE 处理的简单 CoAP responses 发送（:rfc:`8613` Section 8.2）：
   - COSE decode 失败 → 4.02 Bad Option
   - Security context 未找到 → 4.01 Unauthorized
   - 解密失败 → 4.00 Bad Request

4. **Required OSCORE**：若 service 定义时 ``_oscore_required`` argument 设为 true（unprotected requests 被 4.01 Unauthorized 拒绝。

5. **Fail-closed behavior**：若 response 的 OSCORE 保护失败（server 不 fallback 到发送 plaintext response。OSCORE-required service 上（无法匹配到任何 OSCORE state 的 outgoing response 也被丢弃而非明文发送。Observe notifications 从不降级。Mixed service 上（exchange cache entry 过期的任何 response（synchronous 或 deferred）再无法匹配（以 unprotected 发送。实际上这影响 deferred（separate）responses（因为 synchronous response 与 request 处理期间刚创建的 entry 匹配（参见 item 2 和 :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS`）。


Known Limitations
============================

1. **Mixed-Service Expired-Exchange Plaintext**：在 mixed service（同时服务 OSCORE 和 non-OSCORE clients 的）上（exchange cache entry 过期的 response 再无法匹配到其 OSCORE state（以 plaintext 发送。这影响 synchronous 和 deferred（separate）responses（参见 :kconfig:option:`CONFIG_COAP_OSCORE_EXCHANGE_LIFETIME_MS`。对携带 sensitive data 的任何 service（将其定义为 OSCORE-required（将 ``_oscore_required`` argument 传为 true（例如通过 :c:macro:`COAP_SERVICE_DEFINE_OSCORE`））而非运行 mixed service。OSCORE-required service 拒绝 unprotected requests（并丢弃无法保护的 responses（因此从不降级到 plaintext。

Security Context Derivation
============================

OSCORE security contexts 从少量 parameters 派生（:rfc:`8613` Section 3）：

**Required parameters**：

- **Master Secret**：Shared secret（AES-CCM-16-64-128 通常 16 bytes）
- **Sender ID**：Sender 的唯一 identifier
- **Recipient ID**：Recipient 的唯一 identifier

**Optional parameters**：

- **Master Salt**：额外 entropy（推荐（通常 8 bytes）
- **ID Context**：额外 context identifier
- **AEAD Algorithm**：默认 AES-CCM-16-64-128
- **KDF**：默认 HKDF-SHA-256

这些 parameters 通常通过以下建立：

1. **Pre-shared keys**：在 device provisioning 时配置
2. **EDHOC**：Ephemeral Diffie-Hellman Over COSE（参见 uoscore-uedhoc module）

Security Considerations
=======================

1. **Sequence number overflow**：Sender sequence number（SSN）对 AES-CCM-16-64-128 不得超过 2^23-1。Uoscore library 强制此限制。

2. **Master secret protection**：Master secrets 须安全存储（例如在 secure storage 中或从 EDHOC 派生。

3. **Persistence across reboots**：若相同 master secret 在 reboot 后复用（即 master secrets 未重新派生（例如通过 EDHOC）（sender sequence number 须持久化到非易失 memory 以防止 nonce 复用（其将破坏 confidentiality 和 integrity。Receiver 的 replay window 无需持久化：其保持在 memory 中（且 reboot 后按 :rfc:`8613` Appendix B.1.2 描述用 Echo option 重新同步。

Handling OSCORE When Not Supported
-----------------------------------

当 OSCORE support 未启用（:kconfig:option:`CONFIG_COAP_OSCORE` 未设置）时（Zephyr CoAP stack 按 :rfc:`7252` Section 5.4.1 为 OSCORE option 实现 fail-closed behavior：

**Server behavior**（当 ``CONFIG_COAP_OSCORE=n``）：

- 带 OSCORE option 的 **CON requests**：返回 **4.02（Bad Option）** response
- 带 OSCORE option 的 **NON requests**：静默拒绝（丢弃）message
- 带 OSCORE option 的 **Responses**：CON 发送 RST（静默丢弃 NON/ACK

API Reference
=============

.. doxygengroup:: coap_oscore
