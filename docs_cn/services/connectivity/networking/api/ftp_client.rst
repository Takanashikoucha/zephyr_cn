.. _ftp_client_interface:

FTP client
##########

.. contents::
   :local:
   :depth: 2

Overview
********

FTP client library 可用于向 FTP server 下载或上传 files。

FTP client library 用两个单独的 callback functions :c:member:`ftp_client.ctrl_callback` 和 :c:member:`ftp_client.data_callback` 报告 FTP control message 和 download data。若 :kconfig:option:`CONFIG_FTP_CLIENT_KEEPALIVE_TIME` 非零（库可配置为通过 timer 自动向 server 发送 KEEPALIVE message。KEEPALIVE message 按 :kconfig:option:`CONFIG_FTP_CLIENT_KEEPALIVE_TIME` 值指示的 time interval 完成时周期性发送。

Protocols
*********

库按 :rfc:`959` specification 实现。

Limitations
***********

库当前仅实现最小 commands 集。然而（新 command 支持可轻松添加。

由于 FTP servers 实现差异（库可能需要定制以与特定 server 工作。

API Reference
*************

.. doxygengroup:: ftp_client
