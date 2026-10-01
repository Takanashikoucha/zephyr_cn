.. _wifi_crypto_mapping:

Wi-Fi feature to crypto mapping
###############################

此页面将 Zephyr 中支持的 Wi-Fi features（通过 hostap-based wpa_supplicant）映射到底层 MbedTLS crypto primitives。用它查看哪些 features 需 bignum、ECDH、TLS 等（以及哪些 code paths 用 **Legacy crypto**（MbedTLS legacy APIs）与 **PSA crypto**（Platform Security Architecture APIs）（当 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA` 启用时。

实现在 hostap module 中：``crypto_mbedtls_alt.c``（generic crypto）和 ``tls_mbedtls_alt.c``（TLS/EAP）。此处仅考虑 MbedTLS backend。

Feature set (from hostap Kconfig)
*********************************

Features 由 Kconfig 门控。相关 options 包括：

* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WEP` — WEP（legacy）
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3_COMMON` — 选择 Internal 或 External 时的 WPA3-SAE（``WIFI_NM_WPA_SUPPLICANT_WPA3_IMPLEMENTATION``；默认 Internal）。:kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3` 无 prompt（选择 Internal 时启用内部 bignum SAE path（在 ``prj.conf`` 中设置 implementation choice（而非此 symbol）。
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_DPP` — Wi-Fi Easy Connect（DPP）
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPS` — Wi-Fi Protected Setup
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_P2P` — P2P / Wi-Fi Direct（隐含 WPS）
* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_ENTERPRISE` — EAP（EAP-TLS、EAP-TTLS-MSCHAPV2、EAP-PEAP-MSCHAPV2、EAP-PEAP-GTC、EAP-PEAP-TLS）

只要 crypto 未设为 ``CRYPTO_NONE``（WPA2-PSK 和 WPA2-PSK-256 可用。

Feature → crypto primitives (MbedTLS)
*************************************

.. list-table:: Wi-Fi feature to crypto mapping
   :widths: 18 22 30 30
   :header-rows: 1

   * - Feature
     - Crypto primitives
     - Legacy crypto
     - PSA crypto
   * - **WPA3-SAE**
     - * Bignum (mpi), modulo, exponentiation
       * EC group
       * HMAC-SHA256
       * AES (CCMP). SAE uses Dragonfly (PWE) with bignum + modulo.
     - * Bignum (mbedtls_mpi)
       * EC
       * HMAC, AES (unless PSA build)
     - * Hashes, HMAC, AES when PSA enabled
       * Bignum/EC still legacy
   * - **SAE-PK**
     - Same as WPA3-SAE plus ECDH and EC key operations (certificate-based SAE).
     - ECDH/EC key ops (legacy MbedTLS or PSA ECDH depending on config).
     - * ECDH can use PSA
       * Bignum/SAE core remain legacy
   * - **DPP (Easy Connect)**
     - * ECDH (P-256, P-384, P-521)
       * EC key gen/sign/verify
       * Hashes, AES. DPP2 adds PKCS#7; DPP3 adds HPKE.
     - * ECDH, EC, RSA (if used)
       * X.509/CSR in TLS/crypto layer
     - * Hashes, HMAC, AES via PSA
       * ECDH/EC may use PSA
       * TLS/CSR/PKCS#7/HPKE layer legacy
   * - **WPA2-PSK / WPA2-PSK-256**
     - * PBKDF2-SHA1 (or SHA256 for -256)
       * HMAC
       * AES (CCMP)
       * OMAC1-AES (key wrap)
     - All via mbedtls (PBKDF2, HMAC, AES, CMAC) if PSA disabled.
     - PBKDF2, HMAC, AES, OMAC1 implemented via PSA when PSA enabled.
   * - **WEP**
     - * RC4/ARC4 (stream cipher)
       * Optionally AES for some wrappers. Deprecated.
     - Legacy MbedTLS only (no PSA path for WEP in current code).
     - N/A (WEP not migrated to PSA).
   * - **WPS**
     - * DH (finite-field)
       * Bignum
       * Hashes, HMAC, AES, TLS-PRF. Registrar uses TLS.
     - * DH (mbedtls_dhm), bignum (mbedtls_mpi)
       * TLS in tls_mbedtls_alt
     - * Hashes, HMAC, AES, PBKDF2 via PSA
       * DH/bignum and TLS legacy
   * - **EAP-TLS / EAP-TTLS / EAP-PEAP**
     - * TLS 1.2 (and optionally 1.3)
       * RSA
       * X.509 parse/verify
       * Hashes, HMAC, AES (cipher suites)
     - * Full TLS stack (mbedtls_ssl_*, mbedtls_x509_*)
       * RSA
       * No PSA in tls_mbedtls_alt
     - * TLS layer remains legacy
       * Underlying hashes/HMAC/AES can use PSA in crypto_mbedtls_alt
   * - **EAP-PWD**
     - * TLS-PRF
       * Bignum
       * DH (finite-field)
       * EC (optional)
       * Hashes, HMAC
     - Bignum, DH, EC (if used) via legacy MbedTLS.
     - * Hashes/HMAC via PSA
       * Bignum/DH/EC legacy
   * - **EAP-IKEV2**
     - * Cipher (AES), bignum, DH
       * TLS-PRF style operations
     - Legacy cipher, bignum, DH.
     - * AES/hashes/HMAC via PSA
       * Bignum/DH legacy
   * - **Open**
     - No authentication/encryption.
     - N/A
     - N/A

.. note::

   WEP 须用 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WEP` 显式启用。其已 deprecated 且不安全；仅用于 legacy networks。

Summary: Legacy vs PSA (MbedTLS backend)
****************************************

当 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA` 启用时（``crypto_mbedtls_alt.c``（及 ``supp_psa_api.h`` / ``supp_psa_api.c``）中的实现按以下拆分。用此 table 查看哪些 operations 用 **PSA** 与 **Legacy** MbedTLS。

.. list-table:: Legacy vs PSA by crypto operation
   :widths: 28 10 42
   :header-rows: 1

   * - Operation
     - API
     - Used by / notes
   * - Message digests (MD5, SHA1, SHA256, SHA384, SHA512)
     - PSA
     -
   * - HMAC (all above hash types)
     - PSA
     -
   * - PBKDF2-SHA1
     - PSA
     - WPA2-PSK key derivation
   * - AES (block, CBC, CTR, OMAC1-AES)
     - PSA
     - Key wrap, CCMP, etc.
   * - Bignum (crypto_bignum_*)
     - Legacy
     - SAE, EAP-PWD, EAP-EKE, EAP-IKEV2, WPS; no PSA bignum in hostap
   * - ECDH / EC key operations
     - Legacy
     - DPP, SAE-PK, EAP-PWD (EC). May be PSA-backed when
       ``MBEDTLS_ECDH_C`` / ``CONFIG_PSA_WANT_ALG_ECDH``; wrapper layer common
   * - TLS/SSL
     - Legacy
     - EAP-TLS, EAP-TTLS, EAP-PEAP; full stack in ``tls_mbedtls_alt.c``
   * - RSA
     - Legacy
     - TLS, X.509
   * - X.509 / CSR
     - Legacy
     - Parse and generation
   * - WEP
     - Legacy
     - No PSA path

因此：**WPA2-PSK 和 WPA2-PSK-256** 仅用 PSA 执行其 crypto；**WPA3-SAE**、**DPP**、**SAE-PK**、**WPS** 和 **Enterprise EAP** 仍依赖 legacy bignum、EC 或 TLS。per-feature 影响参见上方 feature table。
