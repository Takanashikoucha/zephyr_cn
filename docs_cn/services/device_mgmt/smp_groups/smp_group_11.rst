.. _mcumgr_smp_group_11:

Transport
Management
Group
##########################

Transport
management
group
define
以下
commands：

.. table::
    :align:
    center

    +----------------+------------------------------------+
    |
    ``Command
    ID``
    |
    Command
    description
    |
    +================+====================================+
    |
    ``0``
    |
    Connect
    （bridge）
    transport
    |
    +----------------+------------------------------------+
    |
    ``1``
    |
    Disconnect
    bridged
    transport
    |
    +----------------+------------------------------------+
    |
    ``2``
    |
    Fetch
    bridge/transport
    status
    |
    +----------------+------------------------------------+
    |
    ``6``
    |
    List
    transports
    |
    +----------------+------------------------------------+
    |
    ``7``
    |
    Details
    on
    transport
    modes
    |
    +----------------+------------------------------------+
    |
    ``8``
    |
    Details
    on
    transport
    configuration
    |
    +----------------+------------------------------------+

.. note::
    Transport
    management
    是
    experimental
    的
    并
    subject
    to
    change
    without
    notice。

Connect
（bridge）
transport
command
**********************************

Bridge
received
MCUmgr
packet
的
transport
到
另
一
个
MCUmgr
transport。

Connect
（bridge）
transport
request
==================================

Connect
（bridge）
transport
request
header
fields：

.. table::
