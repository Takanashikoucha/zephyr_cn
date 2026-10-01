.. _ocpp_interface:

Open Charge Point Protocol (OCPP)
#################################

.. contents::
    :local:
    :depth: 2

Overview
********

Open Charge Point Protocol（OCPP）是 Charge Points（Electric vehicle（EV）charging stations）与 central management system（也称 charging station network）之间通信的 application protocol。OCPP 为 The Open Charge Alliance 定义的 `standard <https://openchargealliance.org/protocols/open-charge-point-protocol/>`_（目标为提供 charge point 与 central system 之间通信方法的 uniform solution。用此 protocol（可连接任何 central system 与任何 charge point（无论 vendor。

Zephyr 提供构建于 websocket API 之上（payload 为 json 格式）的 OCPP Charge Point（CP）library。Library 可用 :kconfig:option:`CONFIG_OCPP` Kconfig option 启用。当前支持带 basic core profile 的 OCPP 1.6。

OCPP charge point（CP）需连接 Central System（CS）server（开发目的应本地设置 open source SteVe server。setup 更多信息参见 `SteVe server <https://github.com/steve-community/steve/blob/master/README.md>`_。

Zephyr OCPP CP library 实现以下 items：

* 处理 socket connectivity 和 events 的 engine
* OCPP core functions 以 frame/parse payload（OCPP events 的 user notification（heartbeat notification

Sample usage
************

用整体 CP 和 CS 信息初始化 ocpp library。初始化 OCPP library 前（network interface 应使用 ethernet 或 wifi 或 modem 就绪。填充的 CP、CS structure 和 user callback 须传入 ocpp_init。

.. code-block:: c

   static int user_notify_cb(ocpp_notify_reason_t reason,
                             ocpp_io_value_t *io,
                             void *user_data)
   {

        switch (reason) {
        case OCPP_USR_GET_METER_VALUE:
                ...
                break;

        case OCPP_USR_START_CHARGING:
                ...
                break;

                ...
                ...
   }

   /* OCPP configuration */
   ocpp_cp_info_t cpi = { "basic", "zephyr", .num_of_con = 1};
   ocpp_cs_info_t csi =  {"192.168.1.3",   /* ip address */
                          "/steve/websocket/CentralSystemService/zephyr",
                          8180,
                          AF_INET};

   ret = ocpp_init(&cpi, &csi, user_notify_cb, NULL);

任何 ocpp transaction API 调用前（须为每个物理 connector 打开唯一 session。

.. code-block:: c

   ocpp_session_handle_t sh = NULL;
   ret = ocpp_session_open(&sh);

Idtag 为 EV user 的 authentication token（应匹配 CS 上的 list。须调用 Authorize request 以确保 idtag 的有效性（若 charging request 源自 local CP）（在向 EV 开始 energy transfer 前。

.. code-block:: c

    ocpp_auth_status_t status;
    ret = ocpp_authorize(sh, idtag, &status, 500);

成功时（authorization status 在 status 中可用。

除 local CP 外（charging request 可能源自 CS（在 callback 中以 OCPP_USR_START_CHARGING 通知 user（此处 authorize request 调用为可选。当 CS 准备好向 EV 供电时（用 ocpp_start_transaction 将带 meter reading 和 connector id 的 start transaction 通知 CS。

.. code-block:: c

   const int idcon = 1;
   const int mval = 25; //meter reading in wh
   ret = ocpp_start_transaction(sh, mval, idcon, 200);

Start transaction 成功后（调用 user callback 以从 library 获取 meter readings。Callback 不应保持更长时间。

API Reference
*************

.. doxygengroup:: ocpp_api
