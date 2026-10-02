.. _bluetooth_mesh_provisioning:

配置
############

配置（Provisioning）是将设备添加到 Mesh 网络的过程。它需要两台分别运行以下角色的设备：

* *provisioner* 代表网络所有者，负责将新节点添加到 Mesh 网络。
* *provisionee* 是通过配置过程被添加到网络中的设备。在配置过程开始前，
  provisionee 是一台 *未配置设备*。

Zephyr 蓝牙 Mesh 协议栈中的配置模块同时支持 provisionee 角色的广播配置和 GATT 配置承载方式，
以及 provisioner 角色的广播配置承载方式。

配置过程
************************

所有蓝牙 Mesh 节点在参与蓝牙 Mesh 网络之前都必须完成配置。配置 API 提供了设备成为
已配置 Mesh 节点所需的全部功能。配置是一个五步过程，包含以下步骤：

* 信标广播（Beaconing）
* 邀请（Invitation）
* 公钥交换
* 认证
* 配置数据传输

信标广播
=========

要启动配置过程，未配置设备必须首先开始广播未配置信标。这样它就能被附近的
provisioner 发现，从而启动配置。要表示设备需要被配置，调用 :c:func:`bt_mesh_prov_enable`。
设备会开始广播包含设备 UUID 和 ``OOB information`` 字段的未配置信标，
如传递给 :c:func:`bt_mesh_init` 的 ``prov`` 参数中所指定。此外，还可以指定
统一资源标识符（URI），它可以将 provisioner 指向某些带外（Out Of Band）信息的位置，
例如设备的公钥或认证值数据库。URI 在单独的广播中通告，并在未配置信标中包含
URI hash，以将两者关联起来。


统一资源标识符
---------------------------

统一资源标识符应遵循蓝牙核心规范补充（Bluetooth Core Specification Supplement）中规定的格式。
URI 必须以 URI scheme 开头，编码为单个 utf-8 数据点；或者使用特殊的 ``none`` scheme，
编码为 ``0x01``。可用 scheme 列表见 `Bluetooth 官网
<https://www.bluetooth.com/specifications/assigned-numbers/>`_。

编码 URI 示例：

.. list-table:: URI 编码示例

  * - URI
    - 编码结果
  * - ``http://example.com``
    - ``\x16//example.com``
  * - ``https://www.zephyrproject.org/``
    - ``\x17//www.zephyrproject.org/``
  * - ``just a string``
    - ``\x01just a string``

配置邀请
=======================

provisioner 通过发送配置邀请启动配置过程。该邀请会提示 provisionee
（如果可用）使用健康服务器 :ref:`bluetooth_mesh_models_health_srv_attention`
引起注意。

未配置设备会自动响应邀请，展示其能力列表，包括支持的带外认证方法和算法。

公钥交换
=================

在配置过程开始之前，provisioner 和未配置设备需要交换公钥，
可以带内（in-band）或带外（Out of Band, OOB）进行。

带内公钥交换是配置过程的一部分，未配置设备和 provisioner 始终支持。

如果应用程序希望支持通过 OOB 交换公钥，需要向 Mesh 协议栈提供公钥和私钥。
未配置设备会在其能力中反映这一点。provisioner 通过任意可用的 OOB 机制获取公钥
（例如设备可能广播包含公钥的数据包，或者公钥可以编码在印在设备包装上的二维码中）。
需要注意的是，即使未配置设备已指定用于带外交换的公钥，provisioner 也可能选择
在带内交换公钥，如果它无法通过 OOB 机制获取公钥。在这种情况下，
Mesh 协议栈会为每次配置过程生成新的密钥对。

要在未配置设备端启用 OOB 公钥支持，需要启用
:kconfig:option:`CONFIG_BT_MESH_PROV_OOB_PUBLIC_KEY`。应用程序必须在配置过程启动之前
通过初始化 :c:member:`bt_mesh_prov.public_key_be`
和 :c:member:`bt_mesh_prov.private_key_be` 指针来提供公钥和私钥。
密钥需要以大端字节序提供。

要提供通过 OOB 获取的设备公钥，在 provisioner 端调用
:c:func:`bt_mesh_prov_remote_pub_key_set`。

认证
=============

在初始交换之后，provisioner 选择一种带外（OOB）认证方法。
这允许用户确认 provisioner 所连接的设备确实是其预期设备，而不是恶意第三方。

配置 API 支持以下用于 provisionee 的认证方法：

* **Static OOB：** 在生产线中为设备分配一个认证值，provisioner 可以通过某些
  应用特定的方式查询该值。对于使用 BTM_ECDH_P256_HMAC_SHA256_AES_CCM 算法的
  安全配置，Static OOB 值应包含超过 128 位的熵，以提供足够的安全防护。
* **Input OOB：** 用户输入认证值。可用输入操作列在 :c:enum:`bt_mesh_input_action_t` 中。
* **Output OOB：** 向用户显示认证值。可用输出操作列在 :c:enum:`bt_mesh_output_action_t` 中。

应用程序必须在 :c:struct:`bt_mesh_prov` 中为支持的认证方法提供回调，
并在 :c:member:`bt_mesh_prov.output_actions` 和
:c:member:`bt_mesh_prov.input_actions` 中启用支持的操作。

当选择 Output OOB 操作时，应在输出回调被调用时向用户展示认证值，
并一直保持到 :c:member:`bt_mesh_prov.input_complete` 或 :c:member:`bt_mesh_prov.complete`
回调被调用。如果操作是 ``blink``、``beep`` 或 ``vibrate``，序列应在至少 3 秒的
延迟后重复。

当选择 Input OOB 操作时，应在应用程序收到 :c:member:`bt_mesh_prov.input` 回调时
提示用户。用户响应应通过 :c:func:`bt_mesh_input_string` 或
:c:func:`bt_mesh_input_numeric` 反馈给配置 API。如果在 60 秒内未记录到用户响应，
配置过程将中止。

如果 Provisionee 希望强制使用 OOB 认证，则必须使用
BT_MESH_ECDH_P256_HMAC_SHA256_AES_CCM 算法。

数据传输
=============

设备成功认证后，provisioner 传输配置数据：

* 单播地址
* 一个网络密钥
* IV index
* 网络标志

  * Key refresh
  * IV update

此外，还会为节点生成 device key。所有这些数据都由 Mesh 协议栈存储，
配置 :c:member:`bt_mesh_prov.complete` 回调随后被调用。

配置安全
*********************

根据公钥交换机制和认证方法的选择，配置过程可以是安全的或不安全的。

2021 年 5 月 24 日，ANSSI `披露 <https://kb.cert.org/vuls/id/799380>`_
了蓝牙 Mesh 配置协议中的一组漏洞，展示了 Blink、Vibrate、Push、Twist 以及
Input/Output 数值型 OOB 方法提供的低熵如何被利用于冒充和中间人攻击。
作为回应，蓝牙 SIG 在蓝牙 Mesh 配置文件规范 v1.0.1 的 `erratum 16350
<https://www.bluetooth.org/docman/handlers/DownloadDoc.ashx?doc_id=516072>`_ 中，
将这些 OOB 方法重新归类为不安全方法，因为 AuthValue 可能被实时暴力破解。
为确保安全配置，应用程序应使用静态 OOB 值和 OOB 公钥传输。

API 参考
*************

.. doxygengroup:: bt_mesh_prov
