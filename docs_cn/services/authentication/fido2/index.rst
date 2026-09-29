.. _fido2_api:

FIDO2
Authenticator
###################

Overview
********

FIDO2
authenticator
subsystem
实现
`FIDO2
CTAP2
Specification`_
（Client
to
Authenticator
Protocol）
使
Zephyr
device
能
作为
passwordless
authentication
的
hardware
security
key。
Subsystem
可以
用
:kconfig:option:`CONFIG_FIDO2`
option
启用。

FIDO2
security
keys
与
`WebAuthn
Specification`_
web
standard
一起
使用。
一
个
relying
party
（website
或
service）
通过
client
（browser
或
OS
platform）
与
authenticator
交互
以
注册
和
验证
user
credentials。
Authenticator
用
on
device
keys
执行
cryptographic
operations
这些
keys
从不
离开
hardware。

Subsystem
当前
支持
以下
CTAP2
commands：

- ``authenticatorMakeCredential``
- ``authenticatorGetAssertion``
- ``authenticatorGetInfo``
- ``authenticatorClientPIN``
- ``authenticatorGetNextAssertion``
- ``authenticatorSelection``

Architecture
************

Subsystem
被
组织
为
pluggable
backend
components
每个
可以
在
build
time
通过
Kconfig
选择：

Transport
   处理
host
和
authenticator
之间
的
wire
protocol
communication。
Transports
用
:c:macro:`FIDO2_TRANSPORT_DEFINE`
macro
注册
并
在
startup
时
被
iterated。
可用
的
transports：
