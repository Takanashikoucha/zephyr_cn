.. _mac_address_config:

MAC Address Configuration
*************************

Ethernet drivers 可在初始化时将大部分 MAC address 处理委托给 :c:struct:`net_eth_mac_config` 和 :c:func:`net_eth_mac_load`。结构通常存储在 driver configuration 中（并用 :c:macro:`NET_ETH_MAC_DT_CONFIG_INIT` 或 :c:macro:`NET_ETH_MAC_DT_INST_CONFIG_INIT` 初始化（其将 devicetree properties 翻译为以下行为之一：

* :c:enumerator:`NET_ETH_MAC_STATIC` – 使用完整的 ``local-mac-address`` property。
* :c:enumerator:`NET_ETH_MAC_RANDOM` – 生成随机 locally administered MAC address（可选用 ``zephyr,mac-address-prefix`` 提供的 bytes 作为前几个 octets。
* :c:enumerator:`NET_ETH_MAC_NVMEM` – 从 ``"mac-address"`` :ref:`NVMEM<nvmem>` cell 读取剩余 bytes（再次可选以 ``zephyr,mac-address-prefix`` 为前缀。
* :c:enumerator:`NET_ETH_MAC_DEFAULT` – fallback 到 driver 的默认 logic（例如存储在 peripheral registers 中的 factory-programmed MAC address。

Driver integration
==================

在 driver 的 configuration 中嵌入 :c:struct:`net_eth_mac_config` 结构（并在 driver 的 data 中嵌入 static buffer：

.. code-block:: c

   struct my_eth_config {
       struct net_eth_mac_config mac_cfg;
       /* more config fields */
   };

   struct my_eth_data {
       uint8_t mac_addr[NET_ETH_ADDR_LEN];
       /* more data fields */
   };

   static const struct my_eth_config my_eth_config_0 = {
       .mac_cfg = NET_ETH_MAC_DT_INST_CONFIG_INIT(0),
   };
   static struct my_eth_data my_eth_data_0;

初始化期间（在将 address 注册到 network interface 之前调用 :c:func:`net_eth_mac_load`。Helper 复制任何静态提供的 bytes（填充剩余 octets（并执行必要的 validation。Drivers 仍可在未提供 configuration 时 fallback 到 SoC-specific storage：

.. code-block:: c

   static int my_eth_init(const struct device *dev)
   {
       const struct my_eth_config *cfg = dev->config;
       struct my_eth_data *data = dev->data;
       int ret;

       ret = net_eth_mac_load(&cfg->mac_cfg, data->mac_addr);
       if (ret == -ENODATA) {
           ret = my_eth_hw_read_mac(dev, data->mac_addr);
       }

       return ret;
   }

   static void my_eth_iface_init(struct net_if *iface)
   {
       const struct device *dev = net_if_get_device(iface);
       struct my_eth_data *data = dev->data;

       net_if_set_link_addr(iface, data->mac_addr, sizeof(data->mac_addr), NET_LINK_ETHERNET);
   }

Devicetree examples
===================

以下示例展示如何为 ``&eth0`` 等 ethernet controller node 选择 MAC address configuration。

Static MAC address
------------------

.. code-block:: devicetree

   &eth0 {
       local-mac-address = [00 11 22 33 44 55];
   };

Random MAC address with prefix
------------------------------

.. code-block:: devicetree

   &eth0 {
       zephyr,mac-address-prefix = [00 04 25];
       zephyr,random-mac-address;
   };

NVMEM-provided MAC address with prefix
--------------------------------------

MAC address 可通过 :ref:`NVMEM API<nvmem>` 从非易失 memory（通常为 EEPROM）获取。

.. code-block:: devicetree

   &eth0 {
       zephyr,mac-address-prefix = [00 12 34];
       nvmem-cells = <&macaddr_cell>;
       nvmem-cell-names = "mac-address";
   };

   &eeprom0 {
       nvmem-layout {
           compatible = "fixed-layout";
           #address-cells = <1>;
           #size-cells = <1>;

           macaddr_cell: cell@0 {
               reg = <0x0 0x6>;
               #nvmem-cell-cells = <0>;
           };
       };
   };

当无 MAC 相关 properties 时（:c:func:`net_eth_mac_load` 返回 ``-ENODATA``（且预期 driver 使用其现有 mechanism（例如读取 hardware registers 或使用 build-time constant。

Changing the MAC address at runtime
===================================

需动态设置 MAC addresses 的 applications（例如采用从 management interface 获得的 address）需用 :kconfig:option:`CONFIG_NET_MGMT` 启用 networking management API（并用 :c:macro:`net_mgmt` 与 :c:macro:`NET_REQUEST_ETHERNET_SET_MAC_ADDRESS`。Request 内部调用 driver 的 :c:func:`ethernet_api.set_config` 实现。

.. code-block:: c

   static int app_set_mac_address(const struct device *dev)
   {
       struct net_if *iface = net_if_lookup_by_dev(dev);
       struct ethernet_req_params params = {
           .mac_address = { { 0x02, 0x00, 0x5E, 0x01, 0x02, 0x03 } },
       };

       /* Make sure the iface is down */

       return net_mgmt(NET_REQUEST_ETHERNET_SET_MAC_ADDRESS, iface,
                       &params, sizeof(params));
   }
