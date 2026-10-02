.. _bluetooth-qual:

资格认证
#############

关于蓝牙 SIG 资格认证流程的详细信息可在以下地址查看：
https://www.bluetooth.com/develop-with-bluetooth/qualify

资格认证环境搭建
*******************

.. _AutoPTS automation software:
   https://github.com/auto-pts/auto-pts

Zephyr 蓝牙 Host 可以使用蓝牙 PTS（Profile Tuning Suite）软件进行资格认证。该流程原本为手动流程，通过使用 `AutoPTS automation software`_ 实现了自动化。

环境搭建的详细描述见下方链接的页面。

.. toctree::
   :maxdepth: 1

   autopts/autopts-win10.rst
   autopts/autopts-linux.rst

ICS 特性
************

.. _Bluetooth Qualification website:
   https://qualification.bluetooth.com/

Zephyr Host 特性的 ICS 文件可在此下载：
:download:`ICS_Zephyr_Bluetooth_Host.pts
</tests/bluetooth/qualification/ICS_Zephyr_Bluetooth_Host.pts>`。

使用 `Bluetooth Qualification website`_ 查看和编辑 ICS。

已认证版本
******************

.. _Bluetooth qualification listing 332380:
   https://qualification.bluetooth.com/ListingDetails/332380

Zephyr 项目提供预先认证的蓝牙 Host 协议栈，方便用户构建符合资格认证的蓝牙产品。它可以纳入产品资格认证设计，提供特性覆盖并减少认证工作量。认证范围可能因版本而异，详情可在下方查看。

.. list-table::
   :header-rows: 1

   * - 版本
     - 设计编号
     - 详情
   * - v4.4
     - Q385945
     - `Bluetooth qualification listing 332380`_
