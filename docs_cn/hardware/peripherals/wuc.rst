.. _wuc_api:

唤醒控制器（WUC）
#######################

概述
********

唤醒控制器（WUC）接口提供了一组通用接口，用于启用和管理唤醒源（wakeup source），这些唤醒源可以将系统从低功耗状态中唤醒。WUC 设备通常在设备树（Devicetree）中描述，客户端使用 :c:struct:`wuc_dt_spec` 引用它们。

设备树配置
************************

唤醒控制器通过 ``wakeup-ctrls`` 属性从客户端节点引用。该属性编码了指向 WUC 设备的 phandle 以及唤醒源的标识符。

设备树片段示例：

.. code-block:: devicetree

   wuc0: wakeup-controller@40000000 {
       compatible = "nxp,mcx-wuc";
       reg = <0x40000000 0x1000>;
       #wakeup-ctrl-cells = <1>;
   };

   button0: button@0 {
       wakeup-ctrls = <&wuc0 10>;
   };

基本操作
***************

应用程序通常使用 :c:macro:`WUC_DT_SPEC_GET` 获取 :c:struct:`wuc_dt_spec`，然后按需启用或禁用唤醒源。

.. code-block:: c
   :caption: 从设备树启用唤醒源

   #define BUTTON0_NODE DT_NODELABEL(button0)

   static const struct wuc_dt_spec button_wuc =
       WUC_DT_SPEC_GET(BUTTON0_NODE);

   if (!device_is_ready(button_wuc.dev)) {
       return -ENODEV;
   }

   return wuc_enable_wakeup_source_dt(&button_wuc);

如果驱动程序支持，应用程序可以检查并清除唤醒源的被触发（triggered）状态。未实现时，相关接口返回 ``-ENOSYS``。

.. code-block:: c
   :caption: 检查并清除唤醒源

   int ret;

   ret = wuc_check_wakeup_source_triggered_dt(&button_wuc);
   if (ret > 0) {
       (void)wuc_clear_wakeup_source_triggered_dt(&button_wuc);
   }

接口参考
*************

.. doxygengroup:: wuc_interface