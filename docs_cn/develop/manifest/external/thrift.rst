.. _external_module_thrift:

Thrift
######

简介
****

`Apache Thrift`_ 是一种 `IDL`_ 规范、`RPC`_ 框架和 `代码生成器`_。它适用于所有主流操作系统，支持 27 种以上编程语言、7 种协议和 6 种底层传输。Thrift 最初于 `2006 年在 Facebook`_ 开发，之后共享给 `Apache Software Foundation`_。Thrift 支持丰富的类型和数据结构，并屏蔽传输和协议细节，使开发者可以专注于应用逻辑。

在 Zephyr 中使用
****************

要将 Thrift 作为 Zephyr 模块引入，可以将其作为 West 项目添加到 ``west.yaml`` 文件，或通过添加子 manifest（例如 ``zephyr/submanifests/thrift.yaml``）文件引入，内容如下，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: Thrift
         path: modules/lib/thrift
         revision: zephyr
         url: https://github.com/zephyrproject-rtos/thrift

该模块在 ``zephyr/`` 目录下包含示例应用和测试。

.. target-notes::

.. _Apache Thrift: https://github.com/apache/thrift
.. _IDL: https://en.wikipedia.org/wiki/Interface_description_language
.. _RPC: https://en.wikipedia.org/wiki/Remote_procedure_call
.. _代码生成器: https://en.wikipedia.org/wiki/Automatic_programming
.. _2006 年在 Facebook: https://thrift.apache.org/static/files/thrift-20070401.pdf
.. _Apache Software Foundation: https://www.apache.org
