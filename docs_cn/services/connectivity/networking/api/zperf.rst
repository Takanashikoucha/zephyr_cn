.. _zperf:

zperf:
Network
Traffic
Generator
################################

.. contents::
    :local:
    :depth:
    2

Overview
********

zperf
是
一
个
shell
utility
它
允许
在
Zephyr
中
generate
network
traffic。
该
tool
可
被
used
用于
evaluate
network
bandwidth。

zperf
与
iPerf
2.0.10
及
更新
版本
compatible。
要
与
较
old
版本
compatible
enable
:kconfig:option:`CONFIG_NET_ZPERF_LEGACY_HEADER_COMPAT`。
或者
zperf
可以
speak
iperf3
参考
:ref:`zperf_iperf3`。
一
个
build
speak
两
个
中
的
一
个。

zperf
可以
在
任何
application
中
被
enabled
Zephyr
中
也
有
一
个
dedicated
的
sample。
参考
:zephyr:code-sample:`zperf
sample
application
<zperf>`
获取
details。

Sample
Usage
************

如果
Zephyr
作为
client
iPerf
必须
被
executed
在
server
mode。
例如
以下
command
line
必须
被
used
用于
UDP
testing：

.. code-block::
   console

   $
   iperf
   -s
   -l
   1K
   -u
   -V
   -B
   2001:db8::2

对于
TCP
testing
command
line
将
看起来
如
这
个：

.. code-block::
   console

   $
   iperf
   -s
   -l
   1K
   -V
   -B
   2001:db8::2


在
Zephyr
console
中
zperf
可以
被
executed
如
下：
