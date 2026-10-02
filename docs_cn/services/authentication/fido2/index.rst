.. _fido2_api:

FIDO2 认证器
###################

概述
********

FIDO2 认证器子系统实现了 `FIDO2 CTAP2 规范`_
（客户端到认证器协议），允许 Zephyr 设备作为
无密码认证的硬件安全密钥。该子系统
可通过 :kconfig:option:`CONFIG_FIDO2` 选项启用。

FIDO2 安全密钥与 `WebAuthn 规范`_ Web 标准配合使用。
依赖方（网站或服务）通过客户端（浏览器或操作系统平台）与认证器交互，
以注册和验证用户凭据。
认证器使用设备上永不出硬件的密钥执行加密操作。

该子系统当前支持以下 CTAP2 命令：

- ``authenticatorMakeCredential``
- ``authenticatorGetAssertion``
- ``authenticatorGetInfo``
- ``authenticatorClientPIN``
- ``authenticatorGetNextAssertion``
- ``authenticatorSelection``

架构
************

该子系统组织为可插拔后端组件，每个组件
可通过 Kconfig 在构建时选择：

传输
   处理主机和认证器之间的线路协议通信。
   传输使用 :c:macro:`FIDO2_TRANSPORT_DEFINE` 宏注册
   并在启动时迭代。
   可用传输：

   - **USB HID（CTAPHID）** — :kconfig:option:`CONFIG_FIDO2_TRANSPORT_USB_HID`
   - **蓝牙低功耗（CTAPBLE）** — :kconfig:option:`CONFIG_FIDO2_TRANSPORT_BLE`

用户在场（UP）
   确认人类物理在场。后端通过
   :kconfig:option:`CONFIG_FIDO2_UP_BACKEND` 选择：

   - **输入设备** — :kconfig:option:`CONFIG_FIDO2_UP_INPUT`
   - **始终批准** — :kconfig:option:`CONFIG_FIDO2_UP_ALWAYS`
   - **自定义** — :kconfig:option:`CONFIG_FIDO2_UP_CUSTOM`（应用程序提供）

凭据存储
   持久化可发现（驻留）凭据。后端
   通过 :kconfig:option:`CONFIG_FIDO2_STORAGE_BACKEND` 选择：

   - **设置子系统** — :kconfig:option:`CONFIG_FIDO2_STORAGE_SETTINGS`
   - **无** — :kconfig:option:`CONFIG_FIDO2_STORAGE_NONE`（仅不可发现凭据）

证明
   对新创建的凭据进行签名以证明其来源。后端通过
   :kconfig:option:`CONFIG_FIDO2_ATTESTATION_BACKEND` 选择：

   - **自证明** — :kconfig:option:`CONFIG_FIDO2_ATTESTATION_SELF`（默认）
   - **无** — :kconfig:option:`CONFIG_FIDO2_ATTESTATION_NONE`
   - **自定义** — :kconfig:option:`CONFIG_FIDO2_ATTESTATION_CUSTOM`（应用程序提供）

使用
*****

要使用 FIDO2 子系统，包含主头文件：

.. code-block:: c

   #include <zephyr/authentication/fido2/fido2.h>

基本初始化
====================

认证器必须至少启用一个传输才能与主机通信。

参见 :zephyr:code-sample:`fido2` 了解完整初始化序列。

运行时状态监控
========================

该子系统暴露一个运行时状态回调，应用程序可用于
驱动 LED 等状态指示器：

.. code-block:: c

   #include <zephyr/authentication/fido2/fido2.h>

   static void on_state_change(enum fido2_runtime_state state, void *user_data)
   {
       switch (state) {
       case FIDO2_RUNTIME_STATE_IDLE:
           /* LED 关闭 */
           break;
       case FIDO2_RUNTIME_STATE_WAITING_USER_PRESENCE:
           /* LED 闪烁 */
           break;
       case FIDO2_RUNTIME_STATE_PROCESSING:
           /* LED 常亮 */
           break;
       default:
           break;
       }
   }

   fido2_set_state_callback(on_state_change, NULL);

扩展
**********

CTAP2 扩展尚未实现。以下 Kconfig 选项
供将来实现使用：

- **credProtect** — :kconfig:option:`CONFIG_FIDO2_EXT_CRED_PROTECT`
- **hmac-secret** — :kconfig:option:`CONFIG_FIDO2_EXT_HMAC_SECRET`
- **largeBlobKey** — :kconfig:option:`CONFIG_FIDO2_EXT_LARGE_BLOB_KEY`
- **credBlob** — :kconfig:option:`CONFIG_FIDO2_EXT_CRED_BLOB`
- **thirdPartyPayment** — :kconfig:option:`CONFIG_FIDO2_EXT_THIRD_PARTY_PAYMENT`

参考
**********

* `FIDO2 CTAP2 规范`_

.. _FIDO2 CTAP2 Specification:
   https://fidoalliance.org/specs/fido-v2.2-rd-20230321/fido-client-to-authenticator-protocol-v2.2-rd-20230321.html

* `WebAuthn 规范`_

.. _WebAuthn Specification:
   https://www.w3.org/TR/webauthn-2/

* `FIDO 联盟`_

.. _FIDO Alliance:
   https://fidoalliance.org/

API 参考
*************

.. doxygengroup:: fido2
