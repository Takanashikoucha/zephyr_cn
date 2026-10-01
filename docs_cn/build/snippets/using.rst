.. _using-snippets:

使用片段
##############

.. tip::

   Zephyr 提供的片段列表见 :ref:`built-in-snippets`。

片段有名称。你通过向构建系统给出片段名称来使用片段。

用 west build
***************

构建应用 ``app`` 时使用名为 ``foo`` 的片段：

.. code-block:: console

   west build -S foo app

使用多个片段：

.. code-block:: console

   west build -S snippet1 -S snippet2 [...] app

用 cmake
**********

如果你直接运行 CMake 而非使用 ``west build``，使用
``SNIPPET`` 变量。这是一个空白或分号分隔的片段名称列表，
列出你想要使用的那些片段。例如：

.. code-block:: console

   cmake -Sapp -Bbuild -DSNIPPET="snippet1;snippet2" [...]
   cmake --build build
