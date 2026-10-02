.. _wifi_crypto_mapping:

Wi-Fi 功能到加密的映射
###############################

本页面将 Zephyr 中支持的 Wi-Fi 功能（通过基于 hostap 的 wpa_supplicant）映射到
底层的 MbedTLS 加密原语。使用它可以查看哪些功能需要 bignum（大数）、ECDH、TLS 等，
以及当启用 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA` 时，
哪些代码路径使用 **Legacy 加密**（MbedTLS legacy API）而哪些使用 **PSA 加密**
（平台安全架构 API）。

实现位于 hostap 模块中：``crypto_mbedtls_alt.c``（通用加密）和
``tls_mbedtls_alt.c``（TLS/EAP）。此处仅考虑 MbedTLS 后端。

功能集（来自 hostap Kconfig）
*********************************

功能由 Kconfig 控制。相关选项包括：

* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WEP` — WEP（legacy）
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3_COMMON` — 选择 Internal 或
  External 时的 WPA3-SAE（``WIFI_NM_WPA_SUPPLICANT_WPA3_IMPLEMENTATION``；默认 Internal）。
  :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3` 无提示（promptless），当选择 Internal 时
  会启用内部 bignum SAE 路径（实现方式的选择在 ``prj.conf`` 中设置，
  而不是此符号）。
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_DPP` — Wi-Fi Easy Connect（DPP）
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPS` — Wi-Fi Protected Setup
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_P2P` — P2P / Wi-Fi Direct（隐含 WPS）
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_ENTERPRISE` — EAP（EAP-TLS, EAP-TTLS-MSCHAPV2,
  EAP-PEAP-MSCHAPV2, EAP-PEAP-GTC, EAP-PEAP-TLS）

只要 crypto 未设置为 ``CRYPTO_NONE``，WPA2-PSK 和 WPA2-PSK-256 就可用。

功能 → 加密原语（MbedTLS）
*************************************

.. list-table:: Wi-Fi 功能到加密的映射
   :widths: 18 22 30 30
   :header-rows: 1

   * - 功能
     - 加密原语
     - Legacy 加密
     - PSA 加密
   * - **WPA3-SAE**
     - * Bignum（mpi）、取模、指数运算
       * EC 群
       * HMAC-SHA256
       * AES（CCMP）。SAE 使用 Dragonfly（PWE），配合 bignum + 取模。
     - * Bignum（mbedtls_mpi）
       * EC
       * HMAC、AES（PSA 构建除外）
     - * 启用 PSA 时，哈希、HMAC、AES 使用 PSA
       * Bignum/EC 仍为 legacy
   * - **SAE-PK**
     - 与 WPA3-SAE 相同，外加 ECDH 和 EC 密钥操作（基于证书的 SAE）。
     - ECDH/EC 密钥操作（根据配置使用 legacy MbedTLS 或 PSA ECDH）。
     - * ECDH 可使用 PSA
       * Bignum/SAE 核心仍为 legacy
   * - **DPP（Easy Connect）**
     - * ECDH（P-256, P-384, P-521）
       * EC 密钥生成/签名/验证
       * 哈希、AES。DPP2 增加 PKCS#7；DPP3 增加 HPKE。
     - * ECDH、EC、RSA（如使用）
       * X.509/CSR 位于 TLS/crypto 层
     - * 哈希、HMAC、AES 通过 PSA
       * ECDH/EC 可使用 PSA
       * TLS/CSR/PKCS#7/HPKE 层为 legacy
   * - **WPA2-PSK / WPA2-PSK-256**
     - * PBKDF2-SHA1（-256 为 SHA256）
       * HMAC
       * AES（CCMP）
       * OMAC1-AES（密钥封装）
     - PSA 禁用时全部通过 mbedtls（PBKDF2, HMAC, AES, CMAC）。
     - 启用 PSA 时，PBKDF2、HMAC、AES、OMAC1 通过 PSA 实现。
   * - **WEP**
     - * RC4/ARC4（流密码）
       * 某些封装可选 AES。已弃用。
     - 仅 Legacy MbedTLS（当前代码中 WEP 无 PSA 路径）。
     - 不适用（WEP 未迁移到 PSA）。
   * - **WPS**
     - * DH（有限域）
       * Bignum
       * 哈希、HMAC、AES、TLS-PRF。Registrar 使用 TLS。
     - * DH（mbedtls_dhm）、bignum（mbedtls_mpi）
       * TLS 位于 tls_mbedtls_alt
     - * 哈希、HMAC、AES、PBKDF2 通过 PSA
       * DH/bignum 和 TLS 为 legacy
   * - **EAP-TLS / EAP-TTLS / EAP-PEAP**
     - * TLS 1.2（可选 1.3）
       * RSA
       * X.509 解析/验证
       * 哈希、HMAC、AES（密码套件）
     - * 完整 TLS 栈（mbedtls_ssl_*、mbedtls_x509_*）
       * RSA
       * tls_mbedtls_alt 中无 PSA
     - * TLS 层仍为 legacy
       * 底层哈希/HMAC/AES 可在 crypto_mbedtls_alt 中使用 PSA
   * - **EAP-PWD**
     - * TLS-PRF
       * Bignum
       * DH（有限域）
       * EC（可选）
       * 哈希、HMAC
     - Bignum、DH、EC（如使用）通过 legacy MbedTLS。
     - * 哈希/HMAC 通过 PSA
       * Bignum/DH/EC 为 legacy
   * - **EAP-IKEV2**
     - * 密码（AES）、bignum、DH
       * TLS-PRF 风格操作
     - Legacy 密码、bignum、DH。
     - * AES/哈希/HMAC 通过 PSA
       * Bignum/DH 为 legacy
   * - **Open**
     - 无认证/加密。
     - 不适用
     - 不适用

.. note::

   WEP 必须通过 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WEP` 显式启用。
   它已弃用且不安全；仅用于 legacy 网络。

汇总：Legacy 与 PSA（MbedTLS 后端）
****************************************

当启用 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA` 时，
``crypto_mbedtls_alt.c``（以及 ``supp_psa_api.h`` / ``supp_psa_api.c``）中的
实现按如下方式拆分。使用下表查看哪些操作使用 **PSA** 而哪些使用 **Legacy** MbedTLS。

.. list-table:: 按加密操作划分的 Legacy 与 PSA
   :widths: 28 10 42
   :header-rows: 1

   * - 操作
     - API
     - 使用方/备注
   * - 消息摘要（MD5, SHA1, SHA256, SHA384, SHA512）
     - PSA
     -
   * - HMAC（上述所有哈希类型）
     - PSA
     -
   * - PBKDF2-SHA1
     - PSA
     - WPA2-PSK 密钥派生
   * - AES（分组、CBC、CTR、OMAC1-AES）
     - PSA
     - 密钥封装、CCMP 等
   * - Bignum（crypto_bignum_*）
     - Legacy
     - SAE、EAP-PWD、EAP-EKE、EAP-IKEV2、WPS；hostap 中无 PSA bignum
   * - ECDH / EC 密钥操作
     - Legacy
     - DPP、SAE-PK、EAP-PWD（EC）。当
       ``MBEDTLS_ECDH_C`` / ``CONFIG_PSA_WANT_ALG_ECDH`` 启用时可能由 PSA 支撑；
       封装层通用
   * - TLS/SSL
     - Legacy
     - EAP-TLS、EAP-TTLS、EAP-PEAP；完整栈位于 ``tls_mbedtls_alt.c``
   * - RSA
     - Legacy
     - TLS、X.509
   * - X.509 / CSR
     - Legacy
     - 解析和生成
   * - WEP
     - Legacy
     - 无 PSA 路径

因此：**WPA2-PSK 和 WPA2-PSK-256** 的加密仅使用 PSA；**WPA3-SAE**、**DPP**、**SAE-PK**、
**WPS** 和 **企业 EAP** 仍依赖 legacy bignum、EC 或 TLS。
有关逐功能的影响，请参阅上表。
