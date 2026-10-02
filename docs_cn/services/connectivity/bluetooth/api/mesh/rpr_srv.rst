.. _bluetooth_mesh_models_rpr_srv:

远程配置服务器
##########################

远程配置服务器模型是蓝牙 Mesh 规范定义的基础模型。通过
:kconfig:option:`CONFIG_BT_MESH_RPR_SRV` 选项启用。

远程配置服务器模型引入于蓝牙 Mesh 协议规范
版本 1.1，用于支持远程将设备配置到 Mesh 网络的功能。

远程配置服务器没有自己的 API，但依赖于
:ref:`bluetooth_mesh_models_rpr_cli` 来控制。远程配置服务器
模型只接受使用节点设备密钥加密的消息。

如果存在，远程配置服务器模型必须实例化在主元素上。

注意，在通过节点配置协议接口（NPPI）过程刷新设备密钥、节点地址或组合数据后，
:c:member:`bt_mesh_prov.reprovisioned`
回调被触发。有关更多详情，请参见 :ref:`bluetooth_mesh_models_rpr_cli` 章节。

如何将模型集成到应用程序中
-----------------------------------------------

要在应用程序中添加远程配置服务器模型，请执行以下操作：

1. 在项目配置中启用 Kconfig：

   .. code-block:: cfg

      CONFIG_BT_MESH_RPR_SRV=y

2. 使用 :c:macro:`BT_MESH_MODEL_RPR_SRV` 宏将模型实例添加到主元素的模型列表 :c:member:`bt_mesh_elem.models` 中，例如：

   .. code-block:: c

      static const struct bt_mesh_model models[] = {
              BT_MESH_MODEL_CFG_SRV,
              BT_MESH_MODEL_HEALTH_SRV(&health_srv, &health_pub),
              BT_MESH_MODEL_RPR_SRV,
              /* ... */
      };

      static const struct bt_mesh_elem elements[] = {
              BT_MESH_ELEM(0, models, BT_MESH_MODEL_NONE),
      };

3. 通过调用 :c:func:`bt_mesh_prov_enable` 并传入
   :c:enumerator:`BT_MESH_PROV_REMOTE` 来启用 PB-Remote：

   .. code-block:: c

      err = bt_mesh_prov_enable(BT_MESH_PROV_REMOTE);
      if (err) {
              printk("PB-Remote enable failed (err %d)\n", err);
      }

限制
-----------

以下限制适用于远程配置服务器模型：

* 不支持使用 PB-GATT 配置未配置设备。
* 支持所有节点配置协议接口（NPPI）过程。但是，如果设备固件更新后设备的组合数据发生变化（参见 :ref:`firmware effect <bluetooth_mesh_dfu_firmware_effect>`），设备无法保持已配置状态。如果预期设备的组合数据会变化，应取消设备的配置。


API 参考
*************

.. doxygengroup:: bt_mesh_rpr_srv
