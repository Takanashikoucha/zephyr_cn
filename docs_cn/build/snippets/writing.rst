编写片段
################

.. contents::
   :local:

基础
******

片段使用名为 :file:`snippet.yml` 的 YAML 文件定义。

一个 :file:`snippet.yml` 文件包含片段名称，连同额外的构建系统设置，像这样：

.. code-block:: yaml

   name: snippet-name
   # ... 构建系统设置放在这里 ...

构建系统设置放在文件中的其他键中，如本页后面所述。

只要设置出现在相同的键下，就可以组合设置。例如，你可以像这样组合片段特定的
设备树覆盖和 ``.conf`` 文件：

.. code-block:: yaml

   name: foo
   append:
     EXTRA_DTC_OVERLAY_FILE: foo.overlay
     EXTRA_CONF_FILE: foo.conf

此外，片段也可以像这样应用到 sysbuild 配置：

.. code-block:: yaml

   name: foo
   append:
     SB_EXTRA_CONF_FILE: sb.conf
     EXTRA_CONF_FILE: app.conf

命名空间
***********

在片段中编写设备树覆盖时，选择节点标签、节点名称等的名称时，
使用 ``snippet_<name>`` 或 ``snippet-<name>`` 作为命名空间前缀。
这避免命名空间冲突。

例如，如果你的片段名为 ``foo-bar``，像这样编写你的设备树覆盖：

.. code-block:: DTS

   chosen {
           zephyr,baz = &snippet_foo_bar_dev;
   };

   snippet_foo_bar_dev: device@12345678 {
           /* ... */
   };

片段位于哪里
**************************

构建系统在这些地方查找片段：

#. 在 :makevar:`SNIPPET_ROOT` CMake 变量配置的目录中。
   这始终包含 zephyr 仓库（因此 :zephyr_file:`snippets/` 始终是片段的来源）。

   额外的目录可以在 CMake 时手动添加。

   该变量是空白或分号分隔的目录列表，可能包含片段定义。

   对于列表中的每个目录，构建系统查找名为 :file:`snippets/` 的子目录下
   的 :file:`snippet.yml` 文件（如果存在）。

   例如，如果 :makevar:`SNIPPET_ROOT` 设置为 ``/foo;/bar``，构建系统将查找
   以下子目录下的 :file:`snippet.yml` 文件：

   - :file:`/foo/snippets/`
   - :file:`/bar/snippets/`

   :file:`snippet.yml` 文件可以嵌套在这些位置下的任何地方。

#. 在任何 :ref:`模块 <modules>` 的 :file:`module.yml` 文件提供
   ``snippet_root`` 设置的地方。

   例如，在名为 ``baz`` 的 zephyr 模块中，你可以将这添加到你的
   :file:`module.yml` 文件：

   .. code-block:: yaml

      settings:
        snippet_root: .

   然后 ``baz/snippets`` 中的任何 :file:`snippet.yml` 文件将被构建系统
   自动发现，就像 ``baz`` 的路径出现在 :makevar:`SNIPPET_ROOT` 中一样。

处理顺序
****************

片段按它们在 :makevar:`SNIPPET` 变量中列出的顺序处理，
或使用 west 时 ``-S`` 参数的顺序。

要在 ``foo`` 之后应用 ``bar``：

.. code-block:: console

   cmake -Sapp -Bbuild -DSNIPPET="foo;bar" [...]
   cmake --build build

用 west 可以用以下方式达到相同效果：

.. code-block:: console

   west build -S foo -S bar [...] app

当多个片段设置相同的配置时，最后处理的片段设置的配置值最终出现在最终配置中。

例如，如果上面示例中 ``foo`` 设置 ``CONFIG_FOO=1`` 且 ``bar`` 设置
``CONFIG_FOO=2``，结果最终配置将是 ``CONFIG_FOO=2``，因为 ``bar`` 在 ``foo`` 之后处理。

这个原则适用于 Kconfig 片段（``.conf`` 文件）和设备树覆盖（``.overlay`` 文件）两者。

.. _snippets-devicetree-overlays:

设备树覆盖（``.overlay``）
**********************************

这个 :file:`snippet.yml` 将 :file:`foo.overlay` 添加到构建：

.. code-block:: yaml

   name: foo
   append:
     EXTRA_DTC_OVERLAY_FILE: foo.overlay

:file:`foo.overlay` 的路径相对于包含 :file:`snippet.yml` 的目录。
多个 ``.overlay`` 文件也可以作为列表提供：

.. code-block:: yaml

   name: foo
   append:
     EXTRA_DTC_OVERLAY_FILE:
       - foo.overlay
       - bar.overlay

.. _snippets-conf-files:

``.conf`` 文件
***************

这个 :file:`snippet.yml` 将 :file:`foo.conf` 添加到构建：

.. code-block:: yaml

   name: foo
   append:
     EXTRA_CONF_FILE: foo.conf

:file:`foo.conf` 的路径相对于包含 :file:`snippet.yml` 的目录。
多个 ``.conf`` 文件也可以作为列表提供。

Sysbuild ``.conf`` 文件
************************

这个 :file:`snippet.yml` 将 :file:`foo.conf` 添加到 sysbuild 配置：

.. code-block:: yaml

   name: foo
   append:
     SB_EXTRA_CONF_FILE: foo.conf

:file:`foo.conf` 的路径相对于包含 :file:`snippet.yml` 的目录。
多个 sysbuild ``.conf`` 文件也可以作为列表提供。

``DTS_EXTRA_CPPFLAGS``
**********************

这个 :file:`snippet.yml` 将 ``DTS_EXTRA_CPPFLAGS`` CMake 缓存变量添加到构建：

.. code-block:: yaml

   name: foo
   append:
     DTS_EXTRA_CPPFLAGS: -DMY_DTS_CONFIGURE

添加这些标志使控制设备树文件的内容成为可能。

开发板特定设置
***********************

你可以编写只应用于某些开发板的设置。

这里描述的设置**除了**应用于所有开发板的片段设置**之外**被应用。
（这类似于例如一个同时有 :file:`prj.conf` 和 :file:`boards/foo.conf` 文件的应用，
在为开发板 ``foo`` 构建时将在构建中使用两个 ``.conf`` 文件，而非只使用
:file:`boards/foo.conf`）

按名称
=======

.. code-block:: yaml

   name: ...
   boards:
     bar: # 开发板 "bar" 的设置放在这里
       append:
         EXTRA_DTC_OVERLAY_FILE: bar.overlay
     baz: # 开发板 "baz" 的设置放在这里
       append:
         EXTRA_DTC_OVERLAY_FILE: baz.overlay

上面示例在为开发板 ``bar`` 构建时使用 :file:`bar.overlay`，
为 ``baz`` 构建时使用 :file:`baz.overlay`。

按正则表达式
=====================

你可以将开发板名称包围在斜杠（``/``）中，以按 `CMake 语法`_ 中的正则表达式
匹配名称。正则表达式必须匹配整个开发板名称。

.. _CMake 语法:
   https://cmake.org/cmake/help/latest/command/string.html#regex-specification

例如：

.. code-block:: yaml

   name: foo
   boards:
     /my_vendor_.*/:
       append:
         EXTRA_DTC_OVERLAY_FILE: my_vendor.overlay

上面示例在为开发板 ``my_vendor_board1`` 或 ``my_vendor_board2`` 构建时
使用设备树覆盖 :file:`my_vendor.overlay`。为 ``another_vendor_board`` 或
``x_my_vendor_board`` 构建时它不会使用该覆盖。

开发板修订版本
====================

开发板修订版本的特定配置也被支持，将在通用文件之后应用：

.. code-block:: yaml

   name: foo
   boards:
     bar:
       append:
         # 基础文件先应用
         EXTRA_DTC_OVERLAY_FILE: first.overlay
       revisions:
         "0.7.0":
           append:
             # 将在通用开发板文件之上应用
             EXTRA_DTC_OVERLAY_FILE: extra_0_7_0.overlay

上面示例将对 ``bar`` 开发板的所有修订版本使用 :file:`first.overlay`，
并为 ``bar`` 开发板的修订版本 ``0.7.0``（``bar@0.7.0``）构建时
也包含 :file:`extra_0_7_0.overlay`。
