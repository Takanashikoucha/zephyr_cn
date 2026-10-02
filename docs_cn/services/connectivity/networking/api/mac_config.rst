.. _mac_address_config:

MAC 地址配置
*************************

以太网驱动程序可以在初始化时将大部分 MAC 地址处理委托给 :c:struct:`net_eth_mac_config` 和 :c:func:`net_eth_mac_load`。该结构通常存储在驱动程序配置中，并使用 :c:macro:`NET_ETH_MAC_DT_CONFIG_INIT` 或 :c:macro:`NET_ETH_MAC_DT_INST_CONFIG_INIT` 进行初始化，后者将设备树属性翻译为以下行为之一：

* :c:enumerator:`NET_ETH_MAC_STATIC` – 使用完整的 ``local-mac-address`` 属性。
* :c:enumerator:`NET_ETH_MAC_RANDOM` – 生成随机的本地管理 MAC 地址，可选使用 ``zephyr,mac-address-prefix`` 中提供的字节作为前几个八位组。
* :c:enumerator:`NET_ETH_MAC_NVMEM` – 从 ``"mac-address"`` :ref:`NVMEM<nvmem>` 单元读取剩余字节，同样可选以 ``zephyr,mac-address-prefix`` 为前缀。
* :c:enumerator:`NET_ETH_MAC_DEFAULT` – 回退到驱动程序的默认逻辑（例如，存储在 peripherals 寄存器中的出厂预编程 MAC 地址）。

驱动程序集成
==================

在驱动程序配置中嵌入 :c:struct:`net_eth_mac_config` 结构，在驱动程序数据中嵌入静态缓冲区：

.. code-block:: c

   struct my_eth_config {
       struct net_eth_mac_config mac_cfg;
       /* 更多配置字段 */
   };

   struct my_eth_data {
       uint8_t mac_addr[NET_ETH_ADDR_LEN];
       /* 更多数据字段 */
   };

   static const struct my_eth_config my_eth_config_0 = {
       .mac_cfg = NET_ETH_MAC_DT_INST_CONFIG_INIT(0),
   };
   static struct my_eth_data my_eth_data_0;

初始化期间，在将地址注册到网络接口之前调用 :c:func:`net_eth_mac_load`。该辅助函数复制任何静态提供的字节，填充剩余的八位组，并执行必要的验证。驱动程序仍可在未提供配置时回退到 SoC 特定的存储：

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

设备树示例
==================

以下示例展示如何为 ``&eth0`` 等以太网控制器节点选择 MAC 地址配置。

静态 MAC 地址
------------------

.. code-block:: devicetree

   &eth0 {
       local-mac-address = [00 11 22 33 44 55];
   };

带前缀的随机 MAC 地址
------------------------------

.. code-block:: devicetree

   &eth0 {
       zephyr,mac-address-prefix = [00 04 25];
       zephyr,random-mac-address;
   };

带前缀的 NVMEM 提供的 MAC 地址
--------------------------------------

MAC 地址可通过 :ref:`NVMEM API<nvmem>` 从非易失性存储器（通常为 EEPROM）中获取。

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

当不存在任何 MAC 相关属性时，:c:func:`net_eth_mac_load` 返回 ``-ENODATA``，驱动程序应使用其现有机制（例如，读取硬件寄存器或使用构建时常量）。

运行时更改 MAC 地址
==================================

需要动态设置 MAC 地址的应用程序（例如采用从管理接口获得的地址）需要启用 :kconfig:option:`CONFIG_NET_MGMT` 来使用网络管理 API，并使用 :c:macro:`net_mgmt` 与 :c:macro:`NET_REQUEST_ETHERNET_SET_MAC_ADDRESS`。该请求内部调用驱动程序的 :c:func:`ethernet_api.set_config` 实现。

.. code-block:: c

   static int app_set_mac_address(const struct device *dev)
   {
       struct net_if *iface = net_if_lookup_by_dev(dev);
       struct ethernet_req_params params = {
           .mac_address = { { 0x02, 0x00, 0x5E, 0x01, 0x02, 0x03 } },
       };

       /* 确保接口已关闭 */

       return net_mgmt(NET_REQUEST_ETHERNET_SET_MAC_ADDRESS, iface,
                       &params, sizeof(params));
   }
