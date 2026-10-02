.. _fido2_api:

FIDO2 认证器
###################

概述
********

FIDO2 认证器子系统实现了 `FIDO2 CTAP2 规范`_
（客户端到认证器协议，Client to Authenticator Protocol），
使 Zephyr 设备能够作为用于无密码认证的硬件安全密钥。
该子系统可通过 :kconfig:option:`CONFIG_FIDO2` 选项启用。

FIDO2 安全密钥与 `WebAuthn 规范`_ Web 标准配合使用。
依赖方（网站或服务）通过客户端（浏览器或操作系统平台）
与认证器交互，以注册和验证用户凭据。
认证器使用设备上的密钥执行密码学操作，
这些密钥永远不会离开硬件。

该子系统目前支持以下 CTAP2 命令：

- ``authenticatorMakeCredential``
- ``authenticatorGetAssertion``
- ``authenticatorGetInfo``
- ``authenticatorClientPIN``
- ``authenticatorGetNextAssertion``
- ``authenticatorSelection``

架构
************

该子系统组织为可插拔的后端组件，
每个组件都可在构建时通过 Kconfig 选择：

传输层
    负责主机与认证器之间的线路协议通信。
    传输层使用 :c:macro:`FIDO2_TRANSPORT_DEFINE` 宏注册，
    并在启动时遍历。
    可用的传输层：

    - **USB HID（CTAPHID）** — :kconfig:option:`CONFIG_FIDO2_TRANSPORT_USB_HID`
    - **蓝牙 LE（CTAPBLE）** — :kconfig:option:`CONFIG_FIDO2_TRANSPORT_BLE`

用户在场（UP）
    确认有人物理在场。后端通过
    :kconfig:option:`CONFIG_FIDO2_UP_BACKEND` 选择：

    - **输入设备** — :kconfig:option:`CONFIG_FIDO2_UP_INPUT`
    - **始终批准** — :kconfig:option:`CONFIG_FIDO2_UP_ALWAYS`
    - **自定义** — :kconfig:option:`CONFIG_FIDO2_UP_CUSTOM`（由应用提供）

凭据存储
    持久化可发现（驻留）凭据。后端通过
    :kconfig:option:`CONFIG_FIDO2_STORAGE_BACKEND` 选择：

    - **设置子系统** — :kconfig:option:`CONFIG_FIDO2_STORAGE_SETTINGS`
    - **无** — :kconfig:option:`CONFIG_FIDO2_STORAGE_NONE`（仅支持不可发现凭据）

证明
    对新创建的凭据进行签名以证明其来源。
    后端通过 :kconfig:option:`CONFIG_FIDO2_ATTESTATION_BACKEND` 选择：

    - **自证明** — :kconfig:option:`CONFIG_FIDO2_ATTESTATION_SELF`（默认）
    - **无** — :kconfig:option:`CONFIG_FIDO2_ATTESTATION_NONE`
    - **自定义** — :kconfig:option:`CONFIG_FIDO2_ATTESTATION_CUSTOM`（由应用提供）

用法
*****

要使用 FIDO2 子系统，请包含主头文件：

.. code-block:: c

   #include <zephyr/authentication/fido2/fido2.h>

基本初始化
====================

认证器必须至少启用一个传输层才能与主机通信。

完整的初始化序列参见 :zephyr:code-sample:`fido2`。

运行时状态监控
========================

该子系统提供了一个运行时状态回调，
应用可用它来驱动状态指示器（例如 LED）：

.. code-block:: c

   #include <zephyr/authentication/fido2/fido2.h>

   static void on_state_change(enum fido2_runtime_state state, void *user_data)
   {
       switch (state) {
       case FIDO2_RUNTIME_STATE_IDLE:
           /* LED off */
           break;
       case FIDO2_RUNTIME_STATE_WAITING_USER_PRESENCE:
           /* Blink LED */
           break;
       case FIDO2_RUNTIME_STATE_PROCESSING:
           /* LED on solid */
           break;
       default:
           break;
       }
   }

   fido2_set_state_callback(on_state_change, NULL);

扩展
**********

CTAP2 扩展尚未实现。以下 Kconfig 选项
为将来实现而保留：

- **credProtect** — :kconfig:option:`CONFIG_FIDO2_EXT_CRED_PROTECT`
- **hmac-secret** — :kconfig:option:`CONFIG_FIDO2_EXT_HMAC_SECRET`
- **largeBlobKey** — :kconfig:option:`CONFIG_FIDO2_EXT_LARGE_BLOB_KEY`
- **credBlob** — :kconfig:option:`CONFIG_FIDO2_EXT_CRED_BLOB`
- **thirdPartyPayment** — :kconfig:option:`CONFIG_FIDO2_EXT_THIRD_PARTY_PAYMENT`

参考资料
**********

* `FIDO2 CTAP2 规范`_

.. _FIDO2 CTAP2 Specification:
   https://fidoalliance.org/specs/fido-v2.2-rd-20230321/fido-client-to-authenticator-protocol-v2.2-rd-20230321.html

* `WebAuthn 规范`_

.. _WebAuthn Specification:
   https://www.w3.org/TR/webauthn-2/

* `FIDO Alliance`_

.. _FIDO Alliance:
   https://fidoalliance.org/

API 参考
*************

.. doxygengroup:: fido2
