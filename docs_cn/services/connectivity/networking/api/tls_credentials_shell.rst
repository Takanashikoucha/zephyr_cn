.. _tls_credentials_shell:

TLS
Credentials
Shell
#####################

TLS
Credentials
shell
提供
一
个
command
line
interface
用于
manage
installed
的
TLS
credentials。

Commands
********

.. _tls_credentials_shell_buf_cred:

Buffer
Credential
（``buf``）
===========================

Buffer
data
incrementally
到
credential
buffer
使
它
可以
用
:ref:`tls_credentials_shell_add_cred`
command
added。

或者：

   -
   Clear
   credential
   buffer。

   -
   Load
   credential
   直接
   到
   credential
   buffer
   以
   ``Ctrl
   +
   c``
   结束。

Usage
-----

要
append
``<DATA>``
到
credential
buffer
用：

.. code-block::
   shell

   cred
   buf
   <DATA>

用
这
个
多
少
次
都
可以
直到
full
的
credential
被
loaded
到
credential
buffer
然后
用
:ref:`tls_credentials_shell_add_cred`
command
store
它。

要
load
``<DATA>``
直接
到
credential
buffer
用：

.. code-block::
   shell

   cred
   buf
   load
   <DATA>
