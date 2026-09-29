.. _sntp_interface:

Simple
Network
Time
Protocol
Library
####################################

.. contents::
    :local:
    :depth:
    2

Overview
********

SNTP
library
implement
:rfc:`4330`。

SNTP
提供
一
个
way
synchronize
computer
networks
中
的
clocks。

Client
（:kconfig:option:`CONFIG_SNTP`）
从
SNTP
server
query
time。
Server
（:kconfig:option:`CONFIG_SNTP_SERVER`）
在
UDP
port
123
上
answer
这样
的
queries
在
每个
enabled
的
address
family
上。
Application
负责
set
system
clock
并
用
:c:func:`sntp_server_clock_source`
告诉
server
它
的
time
来自
哪里。
直到
它
做
到
这
个
server
用
leap
indicator
set
到
"clock
not
synchronized"
和
stratum
16
answer
使
clients
discard
它
的
timestamps。

API
Reference
*************

.. doxygengroup::
   sntp

.. doxygengroup::
   sntp_server
