Trusted Firmware-M Overview
###########################

`Trusted Firmware-M (TF-M) <https://tf-m.docs.trustedfirmware.org/en/latest/>`__ 是平台安全架构（PSA）`IoT Security Framework <https://www.psacertified.org/what-is-psa-certified/>`__ 的参考实现。它定义并实现了一套架构和一组软件组件，旨在解决 IoT 产品中的主要安全顾虑。

Zephyr RTOS 自 Zephyr 2.0.0 配合 TF-M 1.0 起就已获得 PSA 认证，目前集成的版本是 TF-M 2.1.0。

What Does TF-M Offer?
*********************

通过一组安全服务并凭借其设计，TF-M 提供：

* 安全资源与非安全资源的隔离
* 适合嵌入式环境的加密
* 设备机密（密钥等）管理
* 固件验证（以及加密）
* 片外数据的受保护存储与读取
* 设备身份证明（device attestation）
* 审计日志

Build System Integration
************************

在支持的平台上使用 TF-M 时，TF-M 会自动在后台构建并链接，作为标准 Zephyr 构建流程的一部分。该构建过程对 TF-M 的使用方式做了若干假设，并对 Zephyr 应用镜像能做什么、不能做什么有一定的影响：

* 安全处理环境（安全启动和 TF-M）最先启动
* Zephyr 的资源分配依赖于安全镜像中所做的选择

Architecture Overview
*********************

一个 TF-M 应用通常包含以下三个部分，按可信程度从高到低、从左到右排列，代码执行按相同顺序进行（secure boot > secure image > ns image）。

虽然安全引导加载器是可选的，但默认启用，且安全启动是提供安全解决方案的重要部分：

::

    +-------------------------------------+           +--------------+
    | Secure Processing Environment (SPE) |           |     NSPE     |
    | +----------++---------------------+ |           | +----------+ |
    | |          ||                     | |           | |          | |
    | | bl2.bin  ||  tfm_s_signed.bin   | |           | |zephyr.bin| |
    | |          ||                     | | <- PSA -> | |          | |
    | |  Secure  || Trusted Firmware-M  | |    APIs   | |  Zephyr  | |
    | |   Boot   ||   (Secure Image)    | |           | |(NS Image)| |
    | |          ||                     | |           | |          | |
    | +----------++---------------------+ |           | +----------+ |
    +-------------------------------------+           +--------------+

（Zephyr）非安全处理环境（NSPE）与（TF-M）安全处理环境镜像之间的通信基于一组 PSA API 进行，通常会使用 TF-M 构建中附带、并在 Zephyr 中实现的 IPC 机制（参见 :zephyr_file:`modules/trusted-firmware-m/interface`）。

Root of Trust (RoT) Architecture
================================

TF-M 基于 **Root of Trust (RoT)**（可信根）架构。它允许从最可信到次可信再到最不可信的信任层级，为构建或访问可信服务和资源提供一个可靠的基础。

这种方案的好处在于，可信度较低的组件被阻止访问或破坏系统中更关键的部分，且可信度较低环境中出现的错误条件不会破坏更可信的、被隔离的资源。

TF-M 定义了以下可信根层级，按可信程度从高到低排列：

* PSA Root of Trust（**PRoT**），由以下部分组成：

  * PSA Immutable Root of Trust（不可变可信根）：安全启动
  * PSA Updateable Root of Trust（可更新可信根）：可信度最高的安全服务
* Application Root of Trust（**ARoT**）：被隔离的安全服务

**PSA Immutable Root of Trust** 是系统中可信度最高的代码，后续的可信根都锚定在它之上。在 TF-M 中，它就是安全启动镜像，负责验证安全镜像和非安全镜像有效、未被篡改、且来自可靠来源。由于内置了公钥签名密钥，安全引导加载器还会在固件更新过程中验证新镜像。顾名思义，该镜像是**不可变**的。

**PSA Updateable Root of Trust** 实现了 TF-M 中可信度最高的安全服务和组件，例如 Secure Partition Manager (SPM)，以及 PSA Crypto、Internal Trusted Storage (ITS) 等共享安全服务。PSA Updateable Root of Trust 中的服务可以访问同一可信根中的其他资源。

**Application Root of Trust** 是安全处理环境中的一个降权区域，根据构建 TF-M 时所选的隔离级别，它对 PRoT 的访问受限，在最高隔离级别下甚至对其他 ARoT 服务的访问也受限。ARoT 中存在一些标准服务，例如 Protected Storage (PS)，通常你实现的自定义安全服务应放在 ARoT 中，除非有充分的理由将其放在 PRoT 中。

这些划分与**不可信代码**是分开的，不可信代码运行在非安全环境中，在系统中的权限最低。在本例中它就是 Zephyr 应用镜像。

Isolation Levels
----------------

目前，TF-M 中定义了三种不同的**隔离级别**，区域之间的边界逐渐严格。所使用的隔离级别取决于你的安全需求以及可用的系统资源。

* **Isolation Level 1**（隔离级别 1）是最低的隔离级别，唯一的重大边界位于安全处理环境与非安全处理环境之间，通常通过 Armv-M 处理器上的 Arm TrustZone 实现。这里不区分 PSA Updateable Root of Trust (PRoT) 和 Application Root of Trust (ARoT)，它们在同一权限级别执行。该隔离级别会产生最小的合并应用镜像。
* **Isolation Level 2**（隔离级别 2）在级别 1 的基础上引入了 PSA Updateable Root of Trust 与 Application Root of Trust 之间的区分，其中 ARoT 服务对 PRoT 服务的访问受限，只能通过 PRoT 服务暴露的公共 API 与其通信。不过，ARoT 服务之间并未严格隔离。
* **Isolation Level 3**（隔离级别 3）是最高隔离级别，在级别 2 的基础上将各 ARoT 服务彼此隔离，使每个 ARoT 本质上与其他服务隔离开来。这提供了最高级别的隔离，但代价是服务之间额外的开销和代码重复。

当前隔离级别可通过 :kconfig:option:`CONFIG_TFM_ISOLATION_LEVEL` 查看。

Secure Boot
===========

TF-M 中的默认安全引导加载器基于 `MCUBoot <https://www.mcuboot.com/>`__，在 TF-M 中被称为 ``BL2``（二级引导加载器，可能位于安全 MCU 上的基于硬件的引导加载器之后）。

TF-M 中的所有镜像都会进行哈希和签名，哈希和签名在固件更新过程中由 MCUBoot 验证。

MCUBoot 在 TF-M 中使用的几个关键特性包括：

* 公钥签名密钥被烧录在引导加载器中
* S 和 NS 镜像可以使用不同的密钥签名
* 固件镜像可选加密
* 客户端软件负责将新镜像写入 secondary slot
* 默认使用两个相同大小内存区域的静态 flash 布局
* 可选的安全计数器用于回滚保护

处理（可选的）加密镜像时：

* 只有 payload 被加密（header、TLVs 为明文）
* 哈希和签名应用于未加密的数据
* 加密使用 ``AES-CTR-128`` 或 ``AES-CTR-256``
* 每个加密周期随机化加密密钥（通过 ``imgtool``）
* ``AES-CTR`` 密钥包含在镜像中，可使用以下算法对其进行加密：

  * ``RSA-OAEP``
  * ``AES-KW``（128 位或 256 位，取决于 ``AES-CTR`` 密钥长度）
  * ``ECIES-P256``
  * ``ECIES-X25519``

用于控制 Zephyr 中安全启动的关键配置属性包括：

* :kconfig:option:`CONFIG_TFM_BL2` 切换引导加载器（默认 = ``y``）。
* :kconfig:option:`CONFIG_TFM_KEY_FILE_S` 覆盖安全签名密钥。
* :kconfig:option:`CONFIG_TFM_KEY_FILE_NS` 覆盖非安全签名密钥。

Secure Processing Environment
=============================

安全引导加载器执行完毕后，基于 TF-M 的安全镜像开始在**安全处理环境**中执行。设备会在此处完成初始配置，所有安全服务也会在此初始化。

请注意，设备的初始状态由安全固件控制，这意味着当非安全 Zephyr 应用启动时，外设可能并不处于硬件默认复位状态。如有疑问，务必查阅 TF-M 中的板级支持包，它们位于 TF-M 模块的 ``platform/ext/target/`` 文件夹中（在默认的 Zephyr west 工作区中位于 ``modules/tee/tf-m/trusted-firmware-m/``）。

Secure Services
---------------

从 TF-M 1.8.0 起，以下安全服务通常可用（不过厂商支持可能有所不同）：

* Crypto（加密）
* Firmware Update (FWU，固件更新)
* Initial Attestation（初始证明）
* Platform（平台）
* Secure Storage（安全存储），包含两个部分：

  * Internal Trusted Storage (ITS，内部可信存储)
  * Protected Storage (PS，受保护存储)

此外，还存在用于创建自定义服务的模板。

关于这些服务及其暴露 API 的完整细节，请查阅 `TF-M Documentation <https://tf-m.docs.trustedfirmware.org/en/latest/>`__。

Key Management and Derivation
-----------------------------

密钥和机密管理是任何安全设备的关键部分。你需要确保密钥材料只对需要它的区域可用，而对其他任何区域不可用，并且以安全的方式存储，使其难以被篡改或恶意访问。

TF-M 中的 **Internal Trusted Storage** 服务被 **PSA Crypto** 服务（其本身使用 mbedtls）用来存储密钥，并确保私钥永远只能被安全处理环境访问。使用密钥材料的加密操作（例如对 payload 签名或解密敏感数据时）全部通过密钥句柄进行。在任何时候，密钥材料都不应暴露给 NS 环境。

一个例外是，私钥可以作为单向操作被预置到安全处理环境中，例如在工厂预置过程中进行，但即便如此也应尽可能避免，而应向 SPE（通过 PSA Crypto 服务）发起请求，由其本身生成新的私钥，其公钥可以在预置过程中请求出来并记录在工厂中。这确保了私钥材料在预置阶段从未暴露，甚至无人知晓。

TF-M 还大量使用 **Hardware Unique Key (HUK)**（硬件唯一密钥），每个 TF-M 设备都必须提供它。例如，**Protected Storage** 服务使用该设备唯一密钥来加密存储在外部内存中的信息。这确保了 flash 内存的内容在被移除并放到新设备上后无法被解密，因为每个设备在首次加密内存内容时都使用自己唯一的 HUK。

HUK 还为开发者提供额外优势：它可以用于派生新密钥，而**派生密钥**无需存储，因为它们可以在启动时从 HUK 重新生成（使用额外的 salt/seed 值，具体取决于所使用的密钥派生算法）。这消除了存储问题以及一个常见的攻击向量。HUK 本身在安全设备中通常受到高度保护，用户无法直接访问。

``TFM_CRYPTO_ALG_HUK_DERIVATION`` 标识使用软件实现时默认采用的密钥派生算法。当前默认算法是带 SHA-256 哈希的 ``HKDF``（:rfc:`5869`）。某些平台上可能还有其他硬件实现可用。

Non-Secure Processing Environment
================================

Zephyr 用于 NSPE，使用 TF-M 支持的、已启用 :kconfig:option:`CONFIG_BUILD_WITH_TFM` 标志的板级。

通常，你只需选择一个有效板级的 ``*/ns`` 板级目标（例如 ``mps2/an521/cpu0/ns``），它会将你的 Zephyr 应用配置为在 NSPE 中运行，正确构建并与 TF-M 安全镜像链接，对安全镜像和非安全镜像进行签名，并将三个二进制文件合并为单个 ``tfm_merged.hex`` 文件。在此配置下，:ref:`west flash <west-flashing>` 命令默认会烧录 ``tfm_merged.hex``。

目前，Zephyr 无法被配置为用作安全处理环境。
