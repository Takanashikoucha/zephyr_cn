.. _ocpp_interface:

Open Charge Point Protocol (OCPP)
#################################

.. contents::
    :local:
    :depth: 2

概述
********

Open Charge Point Protocol（OCPP，开放充电点协议）是一种应用层协议，用于充电点（电动汽车（EV）充电站）与中央管理系统（也称为充电站网络）之间的通信。OCPP 是由 Open Charge Alliance（开放充电联盟）定义的`标准 <https://openchargealliance.org/protocols/open-charge-point-protocol/>`_，其目标是为充电点与中央系统之间的通信方式提供统一的解决方案。借助该协议，可以连接任意中央系统与任意充电点，而不受厂商限制。

Zephyr 提供了一个 OCPP 充电点（CP）库，构建在 websocket API 之上，负载采用 json 格式。该库可以通过 :kconfig:option:`CONFIG_OCPP` Kconfig 选项启用。目前支持 OCPP 1.6 及基础核心配置。

OCPP 充电点（CP）需要一个中央系统（CS）服务器进行连接。出于开发目的，应在本地搭建一个开源的 SteVe 服务器，有关搭建的更多信息请参见 `SteVe 服务器 <https://github.com/steve-community/steve/blob/master/README.md>`_。

Zephyr OCPP CP 库实现了以下内容：

* 处理套接字连接和事件的引擎
* OCPP 核心功能，用于封装/解析负载、OCPP 事件的用户通知以及心跳通知

示例用法
************

使用完整的 CP 和 CS 信息初始化 ocpp 库。在初始化 OCPP 库之前，应通过以太网或 wifi 或调制解调器准备好网络接口。需要向 ocpp_init 传入已填充的 CP、CS 结构体以及用户回调。

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

    /* OCPP 配置 */
    ocpp_cp_info_t cpi = { "basic", "zephyr", .num_of_con = 1};
    ocpp_cs_info_t csi =  {"192.168.1.3",   /* ip 地址 */
                           "/steve/websocket/CentralSystemService/zephyr",
                           8180,
                           AF_INET};

    ret = ocpp_init(&cpi, &csi, user_notify_cb, NULL);

在调用任何 ocpp 事务 API 之前，必须为每个物理连接器打开一个唯一的会话。

.. code-block:: c

    ocpp_session_handle_t sh = NULL;
    ret = ocpp_session_open(&sh);

idtag 是 EV 用户的认证令牌，应与 CS 上的列表相匹配。在开始向 EV 传输能量之前，必须调用授权请求以确保 idtag 的有效性（如果充电请求源自本地 CP）。

.. code-block:: c

    ocpp_auth_status_t status;
    ret = ocpp_authorize(sh, idtag, &status, 500);

成功时，授权状态可在 status 中获取。

除了本地 CP 之外，充电请求也可能源自 CS，并通过 OCPP_USR_START_CHARGING 在回调中通知用户，此时授权请求调用是可选的。当 CS 准备好向 EV 供电时，使用 ocpp_start_transaction 将启动事务连同电表读数和连接器 id 一起通知给 CS。

.. code-block:: c

    const int idcon = 1;
    const int mval = 25; //电表读数，单位为 wh
    ret = ocpp_start_transaction(sh, mval, idcon, 200);

启动事务成功后，会调用用户回调从库中获取电表读数。回调不应被长时间占用。

API 参考
*************

.. doxygengroup:: ocpp_api
