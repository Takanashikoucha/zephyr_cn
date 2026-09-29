.. _ftp_client_interface:

FTP
client
##########

.. contents::
   :local:
   :depth:
   2

Overview
********

FTP
client
library
可
用
来
download
或
upload
files
到
FTP
server。

FTP
client
library
用
两
个
separate
的
callback
functions
:c:member:`ftp_client.ctrl_callback`
和
:c:member:`ftp_client.data_callback`
report
FTP
control
message
和
download
data。
Library
可
被
configured
自动
send
KEEPALIVE
message
到
server
通过
一
个
timer
如果
:kconfig:option:`CONFIG_FTP_CLIENT_KEEPALIVE_TIME`
不
是
zero。
KEEPALIVE
message
被
periodically
sent
在
:kconfig:option:`CONFIG_FTP_CLIENT_KEEPALIVE_TIME`
value
indicated
的
time
interval
completion
时。

Protocols
*********

Library
根据
:rfc:`959`
specification
implemented。

Limitations
***********

Library
当前
只
implement
一
个
minimal
的
commands
set。
不过
新
command
support
可
轻松
added。

由于
FTP
servers
的
implementation
差异
library
可能
需要
customization
才能
与
特定
的
server
work。

API
Reference
*************

.. doxygengroup::
   ftp_client
