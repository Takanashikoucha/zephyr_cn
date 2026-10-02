.. _bluetooth_mesh_models_health_srv:

健康服务器
#############

健康服务器模型为 :ref:`bluetooth_mesh_models_health_cli` 模型提供注意回调和节点诊断。它主要用于报告 Mesh 节点中的故障，并将 Mesh 节点映射到其物理位置。

如果存在，健康服务器模型必须在主元素上实例化。

故障
******

健康服务器模型可以报告设备生命周期中已发生的一组故障。通常，这些故障是可能改变节点行为的事件或状态，例如断电或外设故障。故障分为警告和错误。警告表示接近节点设计可承受极限但未必对设备造成损坏的状态。错误表示超出节点设计极限的状态，可能导致无效行为或对设备造成永久损坏。

故障值 ``0x01`` 到 ``0x7f`` 保留给蓝牙 Mesh 规范，规范定义的完整故障列表见 :ref:`bluetooth_mesh_health_faults`。故障值 ``0x80`` 到 ``0xff`` 是厂商特定的。故障列表始终附带公司 ID 报告，以帮助解释厂商特定的故障。

.. _bluetooth_mesh_models_health_srv_attention:

注意状态
***************

注意状态用于让设备通过某种物理行为（如闪烁、播放声音或振动）引起注意。注意状态可在配置过程中使用，以让用户知道正在配置哪台设备，也可在运行时通过健康模型使用。

启用时，注意状态总是被分配 1 到 255 秒范围内的超时。健康服务器 API 为应用提供两个回调来执行其引起注意的行为：:c:member:`bt_mesh_health_srv_cb.attn_on` 在注意周期开始时调用，:c:member:`bt_mesh_health_srv_cb.attn_off` 在结束时调用。

注意周期的剩余时间可通过 :c:member:`bt_mesh_health_srv.attn_timer` 查询。

API 参考
*************

.. doxygengroup:: bt_mesh_health_srv

.. _bluetooth_mesh_health_faults:

健康故障
=============

蓝牙 Mesh 规范定义的故障值。

.. doxygengroup:: bt_mesh_health_faults
