.. _using-snippets:

使用
片段
##############

.. tip::

   Zephyr
   提供
   的
   片段
   列表
   见
   :ref:`built-in-snippets`。

片段
有
名称。
你
通过
将
名称
给出
构建
系统
来
使用
片段。

用
west build
***************

构建
应用
``app`` 时
使用
名为
``foo`` 的
片段：

.. code-block:: console

   west build -S foo app

使用
多个
片段：

.. code-block:: console

   west build -S snippet1 -S snippet2 [...] app

用
cmake
**********

如果
你
直接
运行
CMake
而非
使用
``west build``，
使用
``SNIPPET`` 变量。
这
是
一个
空白
或
分号
分隔
的
片段
名称
列表，
你
想要
使用
的
那些。
例如：

.. code-block:: console

   cmake -Sapp -Bbuild -DSNIPPET="snippet1;snippet2" [...]
   cmake --build build
