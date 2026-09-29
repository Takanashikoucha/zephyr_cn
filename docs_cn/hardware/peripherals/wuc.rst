.. _wuc_api:

Wakeup
Controller
（WUC）
#######################

Overview
********

Wakeup
Controller
（WUC）
API
为
启用
和
管理
wakeup
sources
提供
一
个
common
interface
它们
可以
将
system
从
low
power
states
唤醒。
WUC
devices
通常
在
Devicetree
中
被
described
并
由
clients
用
:c:struct:`wuc_dt_spec`
引用。

Devicetree
Configuration
************************

Wakeup
controllers
从
client
nodes
用
``wakeup-ctrls``
property
引用。
该
property
编码
一
个
到
WUC
device
的
phandle
和
wakeup
source
的
identifier。

Example
Devicetree
fragment：

.. code-block:: devicetree

   wuc0:
   wakeup
   controller@40000000
   {
       compatible
       =
       "nxp,mcx-wuc";
       reg
       =
       <0x40000000
       0x1000>;
       #wakeup
       ctrl
       cells
       =
       <1>;
   };

   button0:
   button@0
   {
       wakeup
       ctrls
       =
       <&wuc0
       10>;
   };

Basic
Operation
***************

应用
通常
用
:c:macro:`WUC_DT_SPEC_GET`
获取
一
个
:c:struct:`wuc_dt_spec`
然后
根据
需要
启用
或
禁用
wakeup
source。
