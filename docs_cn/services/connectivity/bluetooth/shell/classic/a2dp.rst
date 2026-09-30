Bluetooth:
A2DP
Shell
#####################

:code:`a2dp`
command
expose
A2DP
API
的
parts。

以下
examples
假设
你
已
有
两
个
devices
被
connected。

.. _a2dp_conn_disconn:

A2DP
Connection
***************

Demonstrate
创建
A2DP
connection
的
flow：

*
两
侧
用
:code:`a2dp
register_cb`
register
A2DP
callbacks。
*
任一
侧
establish
一
个
A2DP
connection
它
将
create
AVDTP
Signaling
channel
用
:code:`a2dp
connect`。
*
任一
侧
可以
用
:code:`a2dp
get_conn`
获取
ACL
connection。
*
任一
侧
可以
用
:code:`a2dp
disconnect`
disconnect
A2DP
connection。

.. tabs::

        .. group-tab::
           Device
           A
           (initiator)

                .. code-block::
                   console

                        uart:~$
                        a2dp
                        register_cb
                        success
                        uart:~$
                        a2dp
                        connect
                        Bonded
                        with
                        XX:XX:XX:XX:XX:XX
                        Security
                        changed:
                        XX:XX:XX:XX:XX:XX
                        level
                        2
                        a2dp
                        connected
                        uart:~$
                        a2dp
                        get_conn
                        a2dp
                        conn
                        is:
                        0xXXXXXXXX
                        uart:~$
                        a2dp
                        disconnect
                        a2dp
                        disconnected

        .. group-tab::
           Device
           B
           (acceptor)

                .. code-block::
                   console


.. note::

   以下为原文（待翻译）

                        uart:~$ a2dp send_delay_report
                        success to send report delay
                        <input `a2dp start` in initiator side>
                        receive requesting start and accept
                        stream started
                        <input `a2dp send_media` in source side>
                        received, num of frames: 1, data length: 160
                        data: 1, 2, 3, 4, 5, 6 ......
                        <input `a2dp suspend` in initiator side>
                        receive requesting suspend and accept
                        stream suspended
                        <input `a2dp release` in initiator side>
                        receive requesting release and accept
                        stream released

Abort Operation
***************

Demonstrate the abort operation:

* Establish an A2DP stream based on :ref:`basic a2dp operations <a2dp_basic_operations>`.
* Initiator aborts the stream using :code:`a2dp abort`.

.. tabs::

        .. group-tab:: Device A (initiator)

                .. code-block:: console

                        uart:~$ a2dp abort
                        success to abort
                        stream released

        .. group-tab:: Device B (acceptor)

                .. code-block:: console

                        <input `a2dp abort` in initiator side>
                        receive requesting abort and accept
                        stream released

Get Configuration and Reconfigure Operation
********************************************

Demonstrate the get configuration and reconfigure operations:

* Establish an A2DP stream based on :ref:`basic a2dp operations <a2dp_basic_operations>`.
* Initiator gets configuration using :code:`a2dp get_config`.
* Initiator reconfigures the stream using :code:`a2dp reconfigure`.

.. tabs::

        .. group-tab:: Device A (initiator)

                .. code-block:: console

                        uart:~$ a2dp get_config
                        get config result: 0
                        sample rate 44100Hz
                        uart:~$ a2dp reconfigure
                        success to configure
                        stream configured

        .. group-tab:: Device B (acceptor)

                .. code-block:: console

                        <input `a2dp get_config` in initiator side>
                        receive get config request and accept
                        <input `a2dp reconfigure` in initiator side>
                        receive requesting reconfig and accept
                        sample rate 44100Hz
                        stream configured
