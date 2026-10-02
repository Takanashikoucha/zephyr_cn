.. _secure_storage:

安全存储（Secure Storage）
##############

| 安全存储子系统提供 `平台安全架构（PSA）安全存储 API <https://arm-software.github.io/psa-api/storage/>`_ 中定义的函数的一种实现。
| 它可以在尚没有该 API 实现的 :term:`board targets<board target>` 上启用。

概述
********

安全存储子系统使 PSA 安全存储 API 在所有支持非易失性存储器的板级目标上可用。
因此，它在尚没有该 API 实现的目标上提供了该 API 的一种实现，确保该 API 的功能支持。
例如，启用了 :ref:`tfm` 的板级目标（以 ``/ns`` 结尾）
无法启用该子系统，因为 TF-M 已经提供了该 API 的一种实现。

| 除了提供该 API 的功能支持之外，根据
  设备特定的安全特性和配置，该子系统
  可能保护通过 PSA 安全存储 API 存储的数据在静止状态（at rest）下的安全。
| 但请记住，尽可能时优先使用 TF-M 等安全处理环境，
  因为它由于隔离保证能够提供更多的安全性。

限制
***********

安全存储子系统对 PSA 安全存储 API 的实现：

* 不追求与规范的完全合规。

  | 它的首要目标是在所有板级目标上提供该 API 的功能支持。
  | 参见下文，了解该实现偏离规范的重要方面。

* 不保证它所存储的数据在所有情况下静止状态下都是安全的。

  这取决于设备特定的安全特性和配置。

* 截至本文撰写时，尚未提供受保护存储（PS）API 的实现。

  相反，PS API 直接调用内部可信存储（ITS）API
  （除非提供了 PS API 的 `自定义实现 <#whole-api>`_）。

以下是该实现有意偏离规范的一些方面及其原因说明。这并非一个详尽的列表。

* UID 类型默认只有 30 位。（对照 `2.5 UIDs <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#uids>`_。）

  | 这是一项优化，旨在使直接将 UID 用作
    存储条目 ID 更方便（例如，启用
    :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_STORE_IMPLEMENTATION_ZMS` 时与 :ref:`ZMS <zms_api>` 配合使用）。
  | Zephyr 定义了供该 API 不同使用者使用的数值范围，保证
    没有冲突且它们都能容纳在 30 位内。
    更多信息参见 :zephyr_file:`include/zephyr/psa` 中的头文件。

* 存储在 ITS 中的数据默认被加密和认证。（对照
  `3.2. 内部可信存储要求 <https://arm-software.github.io/psa-api/storage/1.0/overview/requirements.html#internal-trusted-storage-requirements>`_ 中的 ``1.``。）

  | 规范认为 ITS 底层的存储是
    ``隐式机密且受防重放保护的``
    （`2.4. 内部可信存储 API <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#the-internal-trusted-storage-api>`_），
    因为 ``大多数嵌入式微处理器（MCU）具有片上 flash 存储，
    它可以被设置为除运行在 MCU 上的软件外不可访问``
    （`2.2. 技术背景 <https://arm-software.github.io/psa-api/storage/1.0/overview/architecture.html#technical-background>`_）。
  | 并非所有 MCU 都如此。因此，为所存储的数据提供了额外的保护。

  然而，这并不保证所存储的数据在所有情况下静止状态下都是安全的，
  因为这取决于设备特定的安全特性和配置。
  它需要一个随机熵源，特别是需要一个安全的加密密钥提供者
  （:kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_KEY_PROVIDER`）。

  此外，存储在 ITS 中的数据不受重放攻击保护，
  因为这需要受硬件保护的存储。

* 通过 PSA 安全存储 API 存储的数据不受软件或调试直接
  读写的保护。（对照
  `3.2. 内部可信存储要求 <https://arm-software.github.io/psa-api/storage/1.0/overview/requirements.html#internal-trusted-storage-requirements>`_ 中的 ``2.`` 和 ``10.``。）

  它仅在静止状态下受保护。同时在运行时保护它
  需要支持此功能的特定硬件机制。

* ``PSA_STORAGE_FLAG_WRITE_ONCE`` 标志仅保护条目不被通过
  API 修改，而不保护存储介质本身不被修改。

  | 维护该标志需要知道一个条目最初是否被创建过，
    这是必须在存储介质被重写后仍然存留的状态。与重放保护一样，
    这需要受硬件保护的存储。
  | 因此，能够写入存储介质的攻击者可以使一次性写入条目
    被覆盖或删除：要么通过篡改它，之后子系统将其视为
    损坏并允许替换；要么简单地擦除它，之后它看起来从未
    存在过。加密和认证条目也无法防止这两种情况。

* ``psa_its_get*()`` 函数可以返回 ``PSA_ERROR_INVALID_SIGNATURE`` 和
  ``PSA_ERROR_DATA_CORRUPT``。

  规范没有为 ITS API 定义这些错误码，因为它假设底层存储
  受硬件保护，因此从中读回的数据总是完整的。
  这里并非如此，因此这些错误码被传递出去，使调用方能够区分
  被篡改的条目和内部故障。

配置
*************

要配置 Zephyr 提供的 PSA 安全存储 API 实现，请查看
可用的 :kconfig:option-regex:`Kconfig 选项 <CONFIG_SECURE_STORAGE_.*>`。
它们定义在 :zephyr_file:`subsys/secure_storage/` 下的各个 Kconfig 文件中。

自定义
*************

如果现有实现提供的功能不够，自定义实现也可以在不同层次替换 Zephyr 的实现。

整个 API
=========

如果你已经拥有整个 ITS 或 PS API 的实现并希望加以利用，
可以通过启用以下 Kconfig 选项并实现相关函数来实现：

* :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_IMPLEMENTATION_CUSTOM`，用于 ITS API。
* :kconfig:option:`CONFIG_SECURE_STORAGE_PS_IMPLEMENTATION_CUSTOM`，用于 PS API。

ITS API
=======

Zephyr 对 ITS API 的实现
（:kconfig:option:`CONFIG_SECURE_STORAGE_ITS_IMPLEMENTATION_ZEPHYR`）
使用了 ITS transform 和 store 模块，它们可以分别配置和自定义。
查看 :kconfig:option-regex:`ITS transform 和 store Kconfig 选项
<CONFIG_SECURE_STORAGE_ITS_(TRANSFORM|STORE)_.*>` 以了解不同的配置可能性。

特别建议使用或实现一个安全的 :kconfig:option-regex:`加密
密钥提供者 <CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_KEY_PROVIDER_.*>`。

示例
*******

* :zephyr:code-sample:`persistent_key`
* :zephyr:code-sample:`psa_its`

PSA 安全存储 API 参考
********************************

.. doxygengroup:: psa_secure_storage
