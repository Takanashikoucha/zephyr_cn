.. _external_module_requests:

requests
########

介绍
************

`requests`_
项目
提供
一个
易用
的
接口
用于
执行
通用
HTTP(S)
操作
如
GET、
POST、
PUT
和
DELETE
用
Zephyr
的
网络
栈。
它
也
包括
内置
shell
命令
直接
从
Zephyr
shell
与
HTTP(S)
端点
交互。

.. code-block:: shell

   uart:~$
   requests
   requests
   -
   HTTP
   requests
   commands
   Subcommands:
     get
     :
     Perform
     HTTP
     GET
     request
             Usage:
     get
     <url>
     post
     :
     Perform
     HTTP
     POST
     request
             Usage:
     post
     <url>
     <body>
     put
     :
     Perform
     HTTP
     PUT
     request
             Usage:
     put
     <url>
     <body>
     delete
     :
     Perform
     HTTP
     DELETE
     request
             Usage:
     delete
     <url>
   uart:~$

用
Zephyr
*****************

要
拉入
requests
作为
Zephyr
模块，
要么
在
:file:`west.yaml`
文件
中
添加
它
作为
West
项目
或
通过
添加
一个
submanifest
（例如
``zephyr/submanifests/requests.yaml``）
文件
拉入
它
带
以下
内容
并
运行
:command:`west
update`：

.. code-block:: yaml

   manifest:
     projects:
       -
       name:
       requests
         url:
       https://github.com/walidbadar/requests.git
         revision:
       main
         path:
       modules/lib/requests
       #
       按
       需要
       调整
       路径

参考
``requests``
头
文件
获取
API
细节。

参考
**********

.. target-notes::

.. _requests:
   https://github.com/walidbadar/requests
