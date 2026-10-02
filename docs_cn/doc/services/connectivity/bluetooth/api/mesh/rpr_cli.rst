.. _bluetooth_mesh_models_rpr_cli:

远程配置客户端
##########################

远程配置客户端模型是蓝牙 Mesh 规范定义的基础模型。该模型通过
:kconfig:option:`CONFIG_BT_MESH_RPR_CLI` 选项启用。

远程配置客户端模型在蓝牙 Mesh 协议规范 1.1 版中引入。
该模型提供远程将设备配置到 Mesh 网络的功能，并通过与支持
:ref:`bluetooth_mesh_models_rpr_srv` 模型的 Mesh 节点交互，执行
Node Provisioning Protocol Interface 过程。

远程配置客户端模型使用包含目标远程配置服务器模型实例的节点的 device key，
与远程配置服务器模型进行通信。

如果存在，远程配置客户端模型必须实例化在主元素上。

扫描
********

扫描过程用于扫描位于远程配置服务器附近的未配置设备。
远程配置客户端通过调用 :c:func:`bt_mesh_rpr_scan_start` 启动扫描过程：

.. code-block:: C

      static void rpr_scan_report(struct bt_mesh_rpr_cli *cli,
                  const struct bt_mesh_rpr_node *srv,
                  struct bt_mesh_rpr_unprov *unprov,
                  struct net_buf_simple *adv_data)
      {

      }

      struct bt_mesh_rpr_cli rpr_cli = {
         .scan_report = rpr_scan_report,
      };

      const struct bt_mesh_rpr_node srv = {
         .addr = 0x0004,
         .net_idx = 0,
         .ttl = BT_MESH_TTL_DEFAULT,
      };

      struct bt_mesh_rpr_scan_status status;
      uint8_t *uuid = NULL;
      uint8_t timeout = 10;
      uint8_t max_devs = 3;

      bt_mesh_rpr_scan_start(&rpr_cli, &srv, uuid, timeout, max_devs, &status);

上面的示例展示了在目标远程配置服务器节点上启动扫描过程的伪代码。
该过程将启动一个 10 秒的多设备扫描，生成的扫描报告最多包含 3 台未配置设备。
如果指定了 UUID 参数，同一过程只会扫描具有对应 UUID 的设备。
过程完成后，服务器发送扫描报告，该报告将在客户端的
:c:member:`bt_mesh_rpr_cli.scan_report` 回调中处理。

此外，远程配置客户端模型还支持通过 :c:func:`bt_mesh_rpr_scan_start_ext`
调用进行扩展扫描。扩展扫描通过允许远程配置服务器报告特定设备的附加数据，
对常规扫描进行补充。如果未配置设备支持，远程配置服务器将使用主动扫描
向未配置设备请求扫描响应。

配置
************

远程配置客户端通过调用 :c:func:`bt_mesh_provision_remote` 启动配置过程：

.. code-block:: C

      struct bt_mesh_rpr_cli rpr_cli;

      const struct bt_mesh_rpr_node srv = {
         .addr = 0x0004,
         .net_idx = 0,
         .ttl = BT_MESH_TTL_DEFAULT,
      };

      uint8_t uuid[16] = { 0xaa };
      uint16_t addr = 0x0006;
      uint16_t net_idx = 0;

      bt_mesh_provision_remote(&rpr_cli, &srv, uuid, net_idx, addr);

上面的示例展示了通过远程配置服务器节点远程配置设备的伪代码。
该过程将尝试配置具有对应 UUID 的设备，并使用位于索引 0 处的网络密钥
将其主元素分配地址 0x0006。

.. note::
   在远程配置期间，触发的 :c:struct:`bt_mesh_prov` 回调与普通配置相同。
   详见 :ref:`bluetooth_mesh_provisioning` 章节。

重新配置
***************

除了扫描和配置功能外，远程配置客户端还提供手段来重新配置支持
:ref:`bluetooth_mesh_models_rpr_srv` 模型的设备的节点地址、device key
和 Composition Data。这通过 Node Provisioning Protocol Interface（NPPI）提供，
支持以下三种过程：

* Device Key Refresh 过程：用于在无需重新配置节点的情况下更改目标节点的 device key。
* Node Address Refresh 过程：用于更改节点的 device key 和单播地址。
* Node Composition Refresh 过程：用于更改节点的 device key，
  并添加或删除节点的模型或功能。

三种 NPPI 过程可通过 :c:func:`bt_mesh_reprovision_remote` 调用启动：

.. code-block:: C

      struct bt_mesh_rpr_cli rpr_cli;
      struct bt_mesh_rpr_node srv = {
         .addr = 0x0006,
         .net_idx = 0,
         .ttl = BT_MESH_TTL_DEFAULT,
      };

      bool composition_changed = false;
      uint16_t new_addr = 0x0009;

      bt_mesh_reprovision_remote(&rpr_cli, &srv, new_addr, composition_changed);

上面的示例展示了在目标节点上触发 Node Address Refresh 过程的伪代码。
具体过程不是直接选择的，而是通过输入的其他参数选择。
在示例中，我们可以看到目标节点当前的单播地址为 0x0006，
而新地址被设置为 0x0009。如果两个地址相同，且
``composition_changed`` 标志被设置为 true，这段代码将触发
Node Composition Refresh 过程。如果两个地址相同，且
``composition_changed`` 标志被设置为 false，这段代码将触发
Device Key Refresh 过程。

API 参考
*************

.. doxygengroup:: bt_mesh_rpr_cli
