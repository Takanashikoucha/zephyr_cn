.. _ftp_client_interface:

FTP 客户端
##########

.. contents::
   :local:
   :depth: 2

概述
****

FTP 客户端库可用于向 FTP 服务器下载或上传文件。

FTP 客户端库通过两个独立的回调函数 :c:member:`ftp_client.ctrl_callback` 和 :c:member:`ftp_client.data_callback` 报告 FTP 控制消息和下载数据。
如果 :kconfig:option:`CONFIG_FTP_CLIENT_KEEPALIVE_TIME` 不为零，可以将库配置为通过定时器自动向服务器发送 KEEPALIVE 消息。
KEEPALIVE 消息会按照 :kconfig:option:`CONFIG_FTP_CLIENT_KEEPALIVE_TIME` 值所指示的时间间隔完成时定期发送。

协议
****

该库按照 :rfc:`959` 规范实现。

限制
****

目前该库仅实现了最小的一组命令。
不过，可以轻松地添加对新命令的支持。

由于 FTP 服务器的实现存在差异，该库可能需要定制才能与特定服务器配合工作。

API 参考
*********

.. doxygengroup:: ftp_client
