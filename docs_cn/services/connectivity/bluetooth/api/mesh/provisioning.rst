.. _bluetooth_mesh_provisioning:

配置
############

配置是将设备添加到 Mesh 网络的过程。它需要
两个执行以下角色的设备：

* *配置器*（provisioner）代表网络所有者，负责
  将新节点添加到 Mesh 网络。
* *被配置设备*（provisionee）是通过配置过程
  添加到网络的设备。在配置过程开始之前，
  被配置设备是一个*未配置设备*。

Zephyr 蓝牙 Mesh 协议栈中的配置模块支持被配置设备角色的
广播和 GATT 配置承载方式，
以及配置器角色的广播配置承载方式。

配置过程
************************

所有蓝牙 Mesh 节点在参与蓝牙 Mesh 网络之前
必须经过配置。配置 API 提供设备成为已配置 Mesh 节点所需的所有功能。
配置是一个五步过程，包括以下步骤：

* 信标广播
* 邀请
* 公钥交换
* 认证
* 配置数据传输

信标广播
=========

要开始配置过程，未配置设备必须首先开始
广播未配置信标。这使其对附近的
配置器可见，配置器可以发起配置。要表示设备
需要配置，调用 :c:func:`bt_mesh_prov_enable`。设备
开始广播包含设备 UUID 和
``OOB 信息``字段的未配置信标，如传递给
:c:func:`bt_mesh_init` 的 ``prov`` 参数中指定。此外，
可以指定统一资源标识符（URI），
它可以指向配置器一些带外信息的位置，
例如设备的公钥或认证值数据库。URI 在单独的
信标中广播，未配置信标中包含 URI 哈希，
将两者关联起来。

统一资源标识符
---------------------------

统一资源标识符应遵循蓝牙核心规范补充中指定的格式。URI 必须以 URI 方案开头，
编码为单个 utf-8 数据点，或特殊 ``none`` 方案，
编码为 ``0x01``。可用方案列在 `Bluetooth 网站
<https://www.bluetooth.com/specifications/assigned-numbers/>`_ 上。

编码 URI 示例：

.. list-table:: URI 编码示例

  * - URI
    - 编码
  * - ``http://example.com``
    - ``\x16//example.com``
  * - ``https://www.zephyrproject.org/``
    - ``\x17//www.zephyrproject.org/``
  * - ``just a string``
    - ``\x01just a string``

配置邀请
=======================

配置器通过发送配置邀请来发起配置过程。
邀请提示被配置设备使用健康服务器
:ref:`bluetooth_mesh_models_health_srv_attention`（如果可用）引起注意。

未配置设备自动通过展示其能力列表来响应邀请，
包括支持的带外认证方法和算法。

公钥交换
=================

在配置过程可以开始之前，配置器和未配置设备
交换公钥，通过带内或带外（OOB）方式。

带内公钥交换是配置过程的一部分，
始终由未配置设备和配置器支持。

如果应用程序想支持通过 OOB 交换公钥，
它需要向 Mesh 协议栈提供公钥和私钥。未配置设备
会在其能力中反映这一点。配置器通过任何可用的 OOB 机制获取公钥
（例如设备可以广播包含公钥的分组，
或者公钥可以编码在打印在设备包装上的二维码中）。注意，即使未配置设备已指定
带外交换的公钥，配置器也可以选择在带内交换公钥
如果它无法通过 OOB 机制获取公钥。在这种情况下，
Mesh 协议栈将为每个配置过程生成新的密钥对。

要在未配置设备端启用 OOB 公钥支持，
需要启用 :kconfig:option:`CONFIG_BT_MESH_PROV_OOB_PUBLIC_KEY`。
应用程序必须在配置过程开始之前提供公钥和私钥，
通过初始化指向
:c:member:`bt_mesh_prov.public_key_be`
和 :c:member:`bt_mesh_prov.private_key_be` 的指针。密钥需要
以大端字节序提供。

要提供通过 OOB 获取的设备公钥，
在配置器端调用 :c:func:`bt_mesh_prov_remote_pub_key_set`。

认证
=============

在初始交换之后，配置器选择带外（OOB）
认证方法。这允许用户确认配置器连接的设备
确实是他们意图连接的设备，而不是
恶意第三方。

配置 API 支持被配置设备的以下认证方法：

* **静态 OOB：** 在 production 中为设备分配认证值，
  配置器可以通过某些应用程序特定的方式查询。对于使用 BTM_ECDH_P256_HMAC_SHA256_AES_CCM 算法的安全配置，
  静态 OOB 值应包含超过 128 位的熵
  以提供对攻击的充分安全保护。
* **输入 OOB：** 用户输入认证值。可用的输入
  操作列在 :c:enum:`bt_mesh_input_action_t` 中。
* **输出 OOB：** 向用户展示认证值。可用的输出
  操作列在 :c:enum:`bt_mesh_output_action_t` 中。

应用程序必须在 :c:struct:`bt_mesh_prov` 中提供支持的认证
方法的回调，
并在 :c:member:`bt_mesh_prov.output_actions` 和
:c:member:`bt_mesh_prov.input_actions` 中启用支持的操作。

当选择输出 OOB 操作时，应在调用输出回调时
向用户展示认证值，
并保持在 :c:member:`bt_mesh_prov.input_complete` 或 :c:member:`bt_mesh_prov.complete`
回调被调用之前。如果操作是 ``blink``、``beep`` 或 ``vibrate``，
序列应在三秒或更长的延迟后重复。

当选择输入 OOB 操作时，应在应用程序接收
:c:member:`bt_mesh_prov.input` 回调时提示用户。用户
响应应通过 :c:func:`bt_mesh_input_string` 或 :c:func:`bt_mesh_input_numeric` 反馈给配置 API。
如果在 60 秒内未记录用户响应，配置过程
中止。

如果被配置设备想要强制 OOB 认证，必须使用
BT_MESH_ECDH_P256_HMAC_SHA256_AES_CCM 算法。

数据传输
=============

在设备成功认证后，配置器
传输配置数据：

* 单播地址
* 一个网络密钥
* IV 索引
* 网络标志

  * 密钥刷新
  * IV 更新

此外，为节点生成设备密钥。所有这些数据
由 Mesh 协议栈存储，配置 :c:member:`bt_mesh_prov.complete`
回调被调用。

配置安全
*********************

根据公钥交换机制和认证方法的选择，
配置过程可以是安全的或不安全的。

2021 年 5 月 24 日，ANSSI `披露 <https://kb.cert.org/vuls/id/799380>`_
了蓝牙 Mesh 配置协议中的一组漏洞，展示了
Blink、Vibrate、Push、Twist 和
输入/输出数字 OOB 方法提供的低熵
如何被利用进行冒充和 MITM 攻击。作为回应，蓝牙 SIG 已在蓝牙 Mesh 配置文件规范 v1.0.1 `勘误 16350 <https://www.bluetooth.org/docman/handlers/DownloadDoc.ashx?doc_id=516072>`_ 中将这些 OOB 方法重新分类为不安全，
因为 AuthValue 可以实时暴力破解。要确保安全配置，应用程序
应使用静态 OOB 值和 OOB 公钥传输。

API 参考
*************

.. doxygengroup:: bt_mesh_prov
