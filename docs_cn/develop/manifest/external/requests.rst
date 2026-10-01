.. _external_module_requests:

requests
########

简介
****

`requests`_ 项目提供了一个易于使用的接口，用于借助 Zephyr 网络栈执行常见的 HTTP(S) 操作，如 GET、POST、PUT 和 DELETE。它还包含内置的 shell 命令，可直接从 Zephyr shell 与 HTTP(S) 端点交互。

.. code-block:: shell

   uart:~$ requests
   requests - HTTP requests commands
   Subcommands:
     get     : Perform HTTP GET request
               Usage: get <url>
     post    : Perform HTTP POST request
               Usage: post <url> <body>
     put     : Perform HTTP PUT request
               Usage: put <url> <body>
     delete  : Perform HTTP DELETE request
               Usage: delete <url>
   uart:~$

在 Zephyr 中使用
****************

要将 requests 作为 Zephyr 模块引入，可以将其作为 West 项目添加到 :file:`west.yaml` 文件，或通过添加子 manifest（例如 ``zephyr/submanifests/requests.yaml``）文件引入，内容如下，然后运行 :command:`west update`：

.. code-block:: yaml

   manifest:
     projects:
       - name: requests
         url: https://github.com/walidbadar/requests.git
         revision: main
         path: modules/lib/requests # 根据需要调整路径

API 细节请参阅 ``requests`` 头文件。

参考资料
********

.. target-notes::

.. _requests: https://github.com/walidbadar/requests
