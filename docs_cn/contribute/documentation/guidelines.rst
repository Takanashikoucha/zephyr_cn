.. _doc_guidelines:

文档指南
########################

.. highlight:: rst

.. note::

   关于构建文档的说明，参见 :ref:`zephyr_doc`。

Zephyr 项目内容使用 `reStructuredText`_ 标记语言（.rst 文件扩展名）和 Sphinx 扩展编写，并使用 Sphinx 处理以创建格式化的独立网站。开发者可以以原始 .rst 标记文件的形式查看这些内容，或者（安装 Sphinx 后）:ref:`在本地构建文档 <zephyr_doc>` 生成 HTML 或 PDF 格式的文档。HTML 内容随后可以用 Web 浏览器查看。相同的 .rst 内容由 `Zephyr 文档`_ 网站提供。

你可以从 `reStructuredText`_ 和 `Sphinx 扩展`_ 各自的网站阅读其详细信息。

.. _Sphinx 扩展: https://www.sphinx-doc.org/en/stable/contents.html
.. _reStructuredText: https://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _Sphinx 内联标记:  https://sphinx-doc.org/markup/inline.html#inline-markup
.. _Zephyr 文档:  https://docs.zephyrproject.org

本文档提供常用 reST 和 Sphinx 定义指令与角色的快速参考，用于创建你正在阅读的文档。

关于编写良好 C API 文档的说明，参见 :ref:`doxygen_style`。

内容结构
*****************

制表符、空格和缩进
===========================

缩进在 reST 文件内容中很重要，推荐使用空格。额外的缩进（可能无意中）也会改变内容的渲染方式。对于列表和指令，将内容文本缩进到前一行第一个非空白字符处。例如::

   * 跨多行的列表项
     显示续行缩进的位置。

   1. 对于编号列表项，续行应与上一行的文本对齐。

   .. code-block::

      指令块内的文本应与指令名称的第一个字符对齐。

参见 Zephyr :ref:`coding_style` 了解额外要求。

.. _headings:

标题
========

虽然 reST 允许使用上划线和匹配的下划线来指示标题，但我们只使用下划线指示符表示标题。

* 文档标题（h1）使用 ``#`` 作为下划线字符
* 第一级节标题（h2）使用 ``*``
* 第二级节标题（h3）使用 ``=``
* 第三级节标题（h4）使用 ``-``

标题下划线必须与标题文本等长。

例如::

   这是一个标题
   #############

   这里有一些内容

   第一级节标题
   *************


列表
=====

对于项目符号列表，在段落开头放置星号（``*``）或连字符（``-``），续行缩进两个空格。

列表（或子列表）中的第一项前面必须有一个空行，并且应与前面的段落缩进在同一级别（本身不缩进）。

对于编号列表，以 1. 或 a. 开始，然后使用 ``#`` 号继续自动编号。续行缩进三个空格::

   * 这是一个项目符号列表。
   * 它有两个项，第二项有多行 reST 文本。额外行
     缩进到项目符号列表文本的第一个字符。

   1. 这是一个新的编号列表。如果前面没有空行，
      它将是前面列表（或段落）的续行。
   #. 它也有两个项。

   a. 这是一个使用字母列表标题的编号列表
   #. 它有三个项（其余列表项使用自动编号）
   #. 这是第三项

   #. 这是一个自动编号列表（默认使用从 1 开始的数字）。

      #. 这是第一项下的第二级列表（同样自动编号）。注意缩进。
      #. 嵌套列表中的第二项。
   #. 回到包含列表的第二项。不需要空行，
      但为了可读性加上也无妨。

定义列表（包含术语及其定义）是记录带有解释的词语或短语的便捷方式。例如此 reST 内容::

   Makefile 包含以下目标：

   html
      构建项目的 HTML 输出

   clean
      删除所有生成的输出，将文件夹恢复到干净状态。

渲染效果为：

   Makefile 包含以下目标：

   html
      构建项目的 HTML 输出

   clean
      删除所有生成的输出，将文件夹恢复到干净状态。

多列列表
==================

如果你有一个很长的项目符号列表，其中每个项都很短，你可以使用特殊的 ``.. rst-class:: rst-columns`` 指令表示列表项应以多列渲染。该指令将应用于下一个非注释元素（例如段落），或应用于指令下方缩进的内容。例如，此无序列表::

   .. rst-class:: rst-columns

   * 一个
   * 短项
   * 应该
   * 横向
   * 显示
   * 这样
   * 就不会
   * 占用
   * 太多
   * 页面
   * 空间

渲染效果为：

.. rst-class:: rst-columns

   * 一个
   * 短项
   * 应该
   * 横向
   * 显示
   * 这样
   * 就不会
   * 占用
   * 太多
   * 页面
   * 空间

最多显示三列，并根据显示窗口的可用宽度变化，在窄（手机）屏幕上必要时减少为一列。我们已弃用 ``hlist`` 指令，因为它在较小屏幕上表现异常。

表格
======

创建表格有几种方式，各有其限制或怪癖。`网格表格
<https://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#grid-tables>`_
在定义合并行和列方面提供最强大的能力，但难以维护::

   +------------------------+------------+----------+----------+
   | 表头行，列 1           | 表头 2     | 表头 3   | 表头 4   |
   | （表头行可选）          |            |          |          |
   +========================+============+==========+==========+
   | 正文行 1，列 1         | 列 2       | 列 3     | 列 4     |
   +------------------------+------------+----------+----------+
   | 正文行 2               | ...        | ...      | 你可以   |
   +------------------------+------------+----------+ 轻松   +
   | 正文行 3，跨两列       | ...        | 跨度     |
   +------------------------+------------+----------+ 行     +
   | 正文行 4               | ...        | ...      | 也是     |
   +------------------------+------------+----------+----------+

此示例渲染效果为：

+------------------------+------------+----------+----------+
| 表头行，列 1           | 表头 2     | 表头 3   | 表头 4   |
| （表头行可选）          |            |          |          |
+========================+============+==========+==========+
| 正文行 1，列 1         | 列 2       | 列 3     | 列 4     |
+------------------------+------------+----------+----------+
| 正文行 2               | ...        | ...      | 你可以   |
+------------------------+------------+----------+ 轻松   +
| 正文行 3，跨两列       | ...        | 跨度     |
+------------------------+------------+----------+ 行     +
| 正文行 4               | ...        | ...      | 也是     |
+------------------------+------------+----------+----------+

`列表表格
<https://docutils.sourceforge.net/docs/ref/rst/directives.html#list-table>`_
维护起来容易得多，但不支持行或列跨度::

   .. list-table:: 表格标题
      :widths: 15 20 40
      :header-rows: 1

      * - 表头 1
        - 表头 2
        - 表头 3
      * - 正文行 1，列 1
        - 正文行 1，列 2
        - 正文行 1，列 3
      * - 正文行 2，列 1
        - 正文行 2，列 2
        - 正文行 2，列 3

此示例渲染效果为：

.. list-table:: 表格标题
   :widths: 15 20 40
   :header-rows: 1

   * - 表头 1
     - 表头 2
     - 表头 3
   * - 正文行 1，列 1
     - 正文行 1，列 2
     - 正文行 1，列 3
   * - 正文行 2，列 1
     - 正文行 2，列 2
     - 正文行 2，列 3

``:widths:`` 参数允许你定义相对列宽。默认是等宽列。如果你有一个三列表格，希望第一列的宽度是其他两个等宽列的一半，可以指定 ``:widths: 1 2 2``。如果希望浏览器根据列内容自动设置列宽，可以使用 ``:widths: auto``。

选项卡内容
=============

如 :ref:`getting_started` 中介绍的，你可以通过选项卡界面为读者提供替代内容。当读者点击选项卡时，显示该选项卡的内容，例如::

   .. tabs::

      .. tab:: 苹果

         苹果是绿色的，有时是红色的。

      .. tab:: 梨

         梨是绿色的。

      .. tab:: 橙子

         橙子是橙色的。

显示效果为：

.. tabs::

   .. tab:: 苹果

      苹果是绿色的，有时是红色的。

   .. tab:: 梨

      梨是绿色的。

   .. tab:: 橙子

      橙子是橙色的。

选项卡也可以分组，使得在一个区域更改当前选项卡会更改整个页面中所有同名的选项卡。例如：

.. tabs::

   .. group-tab:: Linux

      Linux 第 1 行

   .. group-tab:: macOS

      macOS 第 1 行

   .. group-tab:: Windows

      Windows 第 1 行

.. tabs::

   .. group-tab:: Linux

      Linux 第 2 行

   .. group-tab:: macOS

      macOS 第 2 行

   .. group-tab:: Windows

      Windows 第 2 行

在后一种情况下，我们使用 ``.. group-tab::`` 而非简单的 ``.. tab::``。在底层，我们使用 Zephyr 配置中包含的 `sphinx-tabs
<https://github.com/executablebooks/sphinx-tabs>`_ 扩展。在选项卡内，你可以有除*标题*外的几乎所有内容（code-block、有序和无序列表、图片、段落等）。你可以从上面的链接阅读更多关于 sphinx-tabs 的内容。


文本格式
***************

ReSTructuredText 支持多种文本格式选项。本节提供 Zephyr 文档中最常用的一些文本格式选项的快速参考。完整的列表，请参阅 `reStructuredText 快速参考`_、`reStructuredText 解释文本角色`_ 以及 `Sphinx 提供的额外角色`_。

.. _reStructuredText 快速参考: https://docutils.sourceforge.io/docs/user/rst/quickref.html
.. _reStructuredText 解释文本角色: https://docutils.sourceforge.io/docs/ref/rst/roles.html
.. _Sphinx 提供的额外角色: https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html

内容高亮
====================

一些常见的 reST 内联标记示例：

* 一个星号：``*text*`` 表示强调（*斜体*），
* 两个星号：``**text**`` 表示强强调（**粗体**），
* 两个反引号：````text```` 表示 ``内联代码`` 示例。

如果星号或反引号出现在正文中且可能与内联标记分隔符混淆，可以在其前面添加反斜杠（``\``）来消除混淆。

文件名和命令
=====================

Sphinx 通过支持额外的内联标记元素（称为"角色"）扩展了 reST，用于标记具有特殊含义的文本并允许样式输出格式。（完整的列表请参阅 `Sphinx 内联标记`_ 文档）。

虽然双引号可用于将文本渲染为"代码"，但鼓励使用以下角色来标记文件名、命令名和其他"特殊"文本。

* :rst:role:`file` 用于文件名，例如 ``:file:`CMakeLists.txt``` 将渲染为
  :file:`CMakeLists.txt`

  .. note::

     如果要表示"变量"文件路径，可以使用花括号括住路径的变量部分，例如 ``:file:`{boardname}_defconfig``` 将渲染为
     :file:`{boardname}_defconfig`。

* :rst:role:`command` 用于命令名，例如 ``:command:`make``` 将渲染为 :command:`make`

* :rst:role:`envvar` 用于环境变量，例如 ``:envvar:`ZEPHYR_BASE``` 将渲染为
  :envvar:`ZEPHYR_BASE`

要创建对托管在 GitHub 上 Zephyr 组织中文件的引用，请参阅下面的 :ref:`linking_to_zephyr_files` 节。

用户交互
================

在记录用户交互（如按键组合或 GUI 交互）时，使用以下角色以有意义的方式高亮命令：

* :rst:role:`kbd` 用于键盘输入，例如 ``:kbd:`Ctrl-C``` 将渲染为 :kbd:`Ctrl-C`

* :rst:role:`menuselection` 用于菜单选择，例如 ``:menuselection:`文件 --> 打开``` 将
  渲染为 :menuselection:`文件 --> 打开`

* :rst:role:`guilabel` 用于 GUI 标签，例如 ``:guilabel:`取消``` 将渲染为 :guilabel:`取消`

数学公式
=====================

你可以使用 :rst:role:`math` 角色或 :rst:dir:`math` 指令包含数学公式。对于更复杂的公式，指令提供更多灵活性。

数学的输入语言是 LaTeX 标记。示例::

   生命、宇宙以及一切的答案是 :math:`30 + 2^2 + \sqrt{64} = 42`。

渲染效果为：

   生命、宇宙以及一切的答案是 :math:`30 + 2^2 + \sqrt{64} = 42`。

非 ASCII 字符
====================

除非特定符号对正确性或传统排版是必需的（例如 µ 这样的单位，或 ™ 这样的知名标记），否则优先使用纯 ASCII。

避免纯粹出于美观目的添加非 ASCII 字符。

文件 :zephyr_file:`doc/substitutions.txt` 包含一些基本的 HTML 替换定义用于特殊格式需求（例如强制换行），但 Unicode 字符可以且应该在文档源文件中直接使用。

代码块和命令示例
==================

使用 reST :rst:dir:`code-block` 指令创建高亮的等宽文本块，通常用于显示格式化代码或控制台命令和输出。也支持智能语法高亮（使用 Pygments 包）。你也可以直接指定高亮语言。例如::

   .. code-block:: c

      struct k_object {
         char *name;
         uint8_t perms[CONFIG_MAX_THREAD_BYTES];
         uint8_t type;
         uint8_t flags;
         uint32_t data;
      } __packed;

注意 :rst:dir:`code-block` 指令和 code-block 主体第一行之间的空行，主体内容缩进三个空格（到指令名称的第一个非空白字符处）。

渲染效果为：

   .. code-block:: c

      struct k_object {
         char *name;
         uint8_t perms[CONFIG_MAX_THREAD_BYTES];
         uint8_t type;
         uint8_t flags;
         uint32_t data;
      } __packed;


当然也支持其他语言（参见 `Pygments 支持的语言`_），特别是，鼓励在适当时使用以下语言：

.. _`Pygments 支持的语言`: https://pygments.org/languages/

* ``c`` 用于 C 代码
* ``cpp`` 用于 C++ 代码
* ``python`` 用于 Python 代码
* ``console`` 用于控制台输出，即交互式 shell 会话，命令前面有提示符（例如 Linux 用 ``$``，Zephyr 的 shell 用 ``uart:~$``），并且也显示输出。命令会被高亮，输出不会。此外，使用"复制"按钮复制代码块时会自动仅复制命令，不包括提示符和命令的输出。
* ``shell`` 或 ``bash`` 用于 shell 命令。两种语言的高亮效果相同，但你可以使用 ``bash`` 表示命令是 bash 特定的，``shell`` 表示通用 shell 命令。

  .. note::

     如果代码块包含提示符，不要使用 ``bash`` 或 ``shell``，改用 ``console``。

     反之，如果代码块不包含提示符且不是展示带命令及其输出的交互式会话，不要使用 ``console``。

     .. list-table:: 何时使用 ``bash``/``shell`` 对比 ``console``
        :class: wrap-normal
        :header-rows: 1
        :widths: 20,40,40

        * - 使用场景
          - ``code-block`` 片段
          - 预期输出

        * - 一个或多个命令，无输出

          - .. code-block:: rst

               .. code-block:: shell

                 echo "Hello World!"

          - .. code-block:: shell

               echo "Hello World!"

        * - 带命令及其输出的交互式 shell 会话

          - .. code-block:: rst

               .. code-block:: console

                 $ echo "Hello World!"
                 Hello World!

          - .. code-block:: console

               $ echo "Hello World!"
               Hello World!

        * - 带命令及其输出的交互式 Zephyr shell 会话

          - .. code-block:: rst

               .. code-block:: console

                 uart:~$ version
                 Zephyr version 3.5.99
                 uart:~$ kernel uptime
                 Uptime: 20970 ms

          - .. code-block:: console

               uart:~$ version
               Zephyr version 3.5.99
               uart:~$ kernel uptime
               Uptime: 20970 ms

* ``bat`` 用于 Windows 批处理文件
* ``cfg`` 用于包含 "KEY=value" 条目的配置文件（例如 Kconfig ``.conf`` 文件）
* ``cmake`` 用于 CMake
* ``devicetree`` 用于 Devicetree
* ``kconfig`` 用于 Kconfig
* ``yaml`` 用于 YAML
* ``rst`` 用于 reStructuredText

当未指定语言时，语言设置为 ``none``，代码块不高亮。你也可以显式使用 ``none`` 达到相同效果；例如::

   .. code-block:: none

      这将是一个带有背景和边框样式的文本块，但没有语法高亮。

显示效果为：

   .. code-block:: none

      这将是一个带有背景和边框样式的文本块，但没有语法高亮。

编写代码块也有简写方式：在介绍段落末尾用双冒号（``::``）结尾，将紧随其后的代码块内容缩进三个空格。输出时只显示一个冒号。代码块将无高亮（即 ``none``）。不过你可以使用 :rst:dir:`highlight` 指令自定义文档中使用的默认语言（例如参见本文档开头如何做的）。


链接和交叉引用
**************************

.. _internal-linking:

交叉引用内部内容
==================================

传统 ReST 链接仅支持在当前文件内使用以下表示法::

   参见 `internal-linking`_ 页面

渲染效果为，

   参见 `internal-linking`_ 页面

注意使用尾随下划线表示出站链接。在此示例中，标签添加在标题正前方，所以显示的文字就是标题文本本身。你可以将链接显示的文字更改为::

   参见 `显示此文本 <internal-linking_>`_ 页面

渲染效果为，

   参见 `显示此文本 <internal-linking_>`_ 页面


交叉引用外部内容
==================================

借助 Sphinx 的帮助，我们可以创建对 Zephyr 项目文档中任何标记文本的链接引用。

文档中的目标位置用标签指令定义::

      .. _我的标签名:

      标题
      ======

注意前导下划线表示入站链接。此标签后紧跟的内容必须是标题，并且是从 Zephyr 文档任何位置 ``:ref:`我的标签名``` 引用的目标。引用此标签时显示标题文本。你也可以更改此链接显示的文字，例如::

   :ref:`其他文本 <我的标签名>`


为了便于站点内的跨页链接，每个文件应在其标题前有一个引用标签，以便从另一个文件引用。这些引用标签必须在整个站点中唯一，因此应避免使用 "samples" 这样的通用名称。例如本文档 .rst 文件的顶部是::

   .. _doc_guidelines:

   Zephyr 项目文档指南
   ###############################


其他 .rst 文档可以使用 ``:ref:`doc_guidelines``` 标签链接到本文档，显示为 :ref:`doc_guidelines`。这种内部交叉引用可以跨多个文件工作，链接文本从文档源获取，因此如果标题更改，链接文本也会更新。

你还可以定义到任何 URL 的链接，然后在文档中引用它。例如，在文档中定义此标签::

   .. _Zephyr 维基百科页面:
      https://en.wikipedia.org/wiki/Zephyr_(operating_system)

你可以用::

   阅读 `Zephyr 维基百科页面`_ 了解关于此项目的更多信息。

来引用它。

.. tip::

   当文档包含许多外部链接时，在文档末尾的单个"参考"节中列出它们可能很有用。这可以通过 :rst:dir:`target-notes` 指令实现。示例::

     参考
     =====

     .. target-notes::

     .. _external_link1: https://example.com
     .. _external_link2: https://example.org

交叉引用 C 文档
================================

.. rst:role:: c:member
              c:data
              c:var
              c:func
              c:macro
              c:struct
              c:union
              c:enum
              c:enumerator
              c:type

   你可以使用这些角色交叉引用 C 函数、宏、类型等的 Doxygen 文档。

   它们在 HTML 输出中渲染为指向对应项 Doxygen 文档的链接。例如::

     查看 :c:func:`gpio_pin_configure` 了解更多信息。

   渲染效果为：

     查看 :c:func:`gpio_pin_configure` 了解更多信息。

   你可以提供自定义链接文本，类似于内置的 :rst:role:`ref` 角色。

交叉引用 CMake 文档
=====================================

你可以使用以下角色交叉引用 Zephyr CMake 模块、命令和变量的文档。

.. rst:role:: cmake:module

   此角色用于引用 CMake 模块。例如::

     参见 :cmake:module:`extensions` 了解更多信息。

   渲染效果为：

     参见 :cmake:module:`extensions` 了解更多信息。

.. rst:role:: cmake:command

   此角色用于引用 CMake 命令。例如::

     参见 :cmake:command:`yaml_load` 了解更多信息。

   渲染效果为：

     参见 :cmake:command:`yaml_load` 了解更多信息。

   CMake 自身记录的命令通过其完全限定名引用，作为显式链接目标给出::

     参见 :cmake:command:`target_sources <command:target_sources>` 了解更多信息。

   渲染效果为：

     参见 :cmake:command:`target_sources <command:target_sources>` 了解更多信息。

.. rst:role:: cmake:variable

   此角色用于引用 CMake 变量。例如::

     参见 :cmake:variable:`CMAKE_C_COMPILER` 了解更多信息。

   渲染效果为：

     参见 :cmake:variable:`CMAKE_C_COMPILER` 了解更多信息。

视觉元素
***************

.. _doc_images:

图像
======

图像通过使用 :rst:dir:`image` 指令包含在文档中::

   .. image:: ../../images/doc-gen-flow.png
      :align: center
      :alt: 图像的替代文本

或者如果你想添加图像标题，使用::

    .. figure:: ../../images/doc-gen-flow.png
       :alt: 图像描述

       插图的标题

指定的文件名相对于文档源文件，我们建议将图像放在文档源所在目录的 ``images`` 文件夹中。

支持 Web 浏览器通常处理的图像格式：WebP、PNG、GIF、JPEG 和 SVG。

图像大小只保留到需要的程度，通常至少 500 px 宽但不超过 1000 px，且不超过 100 KB，除非需要特别大的图像以提高清晰度。

基于内容推荐的图像格式
------------------------------------------

* **屏幕截图**：WebP 或 PNG。
* **图表**：考虑使用 Graphviz 创建简单图表（参见下面的 `专门章节 <graphviz_diagrams>`_。如果使用外部工具，优先使用 SVG。
* **照片**（例如板级）：WebP，最大维度不超过 600 px。只要主体可以从背景中分离出来（通常是板级照片的情况），以透明背景保存图像，使其在浅色和深色文档主题中都能融合。

  你可以使用 `cwebp`_ 或 `ImageMagick`_ 将现有图像转换为正确尺寸的 WebP。例如::

     # 使用 cwebp（宽度缩放到 600 px，高度自动，约 80% 质量）。
     # 对于竖版图像，改用 "-resize 0 600" 来限制高度。
     cwebp -resize 600 0 board_name.png -o board_name.webp

     # 使用 ImageMagick
     magick board_name.png -resize 600x600 -quality 80 board_name.webp

  当源已经有透明背景（例如带 alpha 通道的 PNG）时，两个工具都会保留结果 WebP 中的透明性。``-resize 600 0`` / ``600x600`` 参数仅缩小图像，保持其宽高比。

.. _cwebp: https://developers.google.com/speed/webp/download
.. _ImageMagick: https://imagemagick.org/

.. _graphviz_diagrams:

Graphviz
=========

`Graphviz`_ 是用于创建以简单文本语言指定的图表的工具。由于文档中使用的图表需要易于维护，我们鼓励使用 Graphviz 创建图表。Graphviz 特别适合创建状态图、流程图以及可以表示为图的其他类型图表。

要在文档中包含 Graphviz 图表，使用 :rst:dir:`graphviz` 指令。例如::

   .. graphviz::
      :caption: 使用 Graphviz 的示例图

      digraph G {
         rankdir=LR;
         A -> B;
         B -> C;
         C -> D;
      }

渲染效果为：

   .. graphviz::
      :caption: 使用 Graphviz 的示例图

      digraph G {
         rankdir=LR;
         A -> B;
         B -> C;
         C -> D;
      }

更多如何使用 Graphviz 的 DOT 语言创建图表的信息，请参阅 `Graphviz 文档`_。

.. _Graphviz: https://graphviz.org
.. _Graphviz 文档: https://graphviz.org/documentation

Mermaid
=======

`Mermaid`_ 是用于使用简单基于文本的语法创建图表和可视化的工具。它特别适合创建流程图、时序图、类图和状态转换图。

要在文档中包含 mermaid 图表，使用 :rst:dir:`mermaid` 指令。例如::

   .. mermaid::
      :caption: GPIO 去抖的状态转换图
      :alt: GPIO 去抖状态图，显示从不活动状态到活动状态的转换，经过 maybe_active 和 maybe_inactive 中间状态，直到每个状态变得稳定。

      ---
      config:
        state:
          useMaxWidth: false
      ---
      stateDiagram-v2

          State inactive {
              [*] --> stable_inactive
              stable_inactive --> maybe_active : 到活动状态的边
              maybe_active --> stable_inactive : 到不活动状态的边
          }

          State active {
              [*] --> stable_active
              stable_active --> maybe_inactive : 到不活动状态的边
              maybe_inactive --> stable_active : 到活动状态的边
          }

          [*] --> inactive

          maybe_active --> active : After(x ms)
          maybe_inactive --> inactive : After(x ms)


渲染效果为：

.. mermaid::
   :caption: GPIO 去抖的状态转换图
   :alt: GPIO 去抖状态图，显示从不活动状态到活动状态的转换，经过 maybe_active 和 maybe_inactive 中间状态，直到每个状态变得稳定。

   ---
   config:
     state:
       useMaxWidth: false
   ---
   stateDiagram-v2

       State inactive {
           [*] --> stable_inactive
           stable_inactive --> maybe_active : 到活动状态的边
           maybe_active --> stable_inactive : 到不活动状态的边
       }

       State active {
           [*] --> stable_active
           stable_active --> maybe_inactive : 到不活动状态的边
           maybe_inactive --> stable_active : 到活动状态的边
       }

       [*] --> inactive

       maybe_active --> active : After(x ms)
       maybe_inactive --> inactive : After(x ms)


图表在页面宽度范围内绘制，其高度取决于其宽高比，因此比宽度高的图表最终会比需要的尺寸大得多。关闭 ``useMaxWidth``（如上面的示例），使图表保持 Mermaid 计算的尺寸；它仍然会缩小以适应窄屏幕。此设置属于图表类型，此处为 ``state``，其他位置为 ``flowchart``、``sequence`` 或另一种类型。

关于支持的图表、语法和示例的参考，请参阅 `Mermaid 文档`_。创建或更新图表时为了快速迭代，你可以使用 `Mermaid 在线编辑器`_。

.. _Mermaid: https://mermaid.js.org/
.. _Mermaid 文档: https://mermaid.js.org/intro/
.. _Mermaid 在线编辑器: https://mermaid.live/

自定义 Sphinx 角色和指令
**********************************

Zephyr 文档使用自定义 Sphinx 角色和指令提供额外功能，并便于编写和维护一致的文档。

应用构建命令
==========================

.. rst:directive:: .. zephyr-app-commands::

   生成管理（构建、烧录等）应用所需的 shell 命令的一致文档

   例如，要为 ``qemu_x86`` 生成构建 ``samples/hello_world`` 的命令，使用::

     .. zephyr-app-commands::
        :zephyr-app: samples/hello_world
        :board: qemu_x86
        :goals: build

   渲染效果为：

     .. zephyr-app-commands::
        :zephyr-app: samples/hello_world
        :board: qemu_x86
        :goals: build

   .. rubric::  选项

   .. rst:directive:option:: tool
      :type: string

      使用哪个工具。当前有效选项为 ``cmake``、``west`` 和 ``all``。默认为 ``west``。

   .. rst:directive:option:: app
      :type: string

      要构建的应用路径。

   .. rst:directive:option:: zephyr-app
      :type: string

      要构建的应用路径，这是上游 zephyr 仓库中存在的
      应用。与 ``:app:`` 互斥。

   .. rst:directive:option:: cd-into
      :type: no value

      如果设置，构建说明从 ``:app:`` 文件夹内部给出，而非外部。

   .. rst:directive:option:: generator
      :type: string

      生成哪个构建系统。

      当前有效选项为 ``ninja`` 和 ``make``。默认为 ``ninja``。此选项不区分大小写。

   .. rst:directive:option:: host-os

      说明针对哪个宿主操作系统。

      有效选项为 ``unix``、``win`` 和 ``all``。默认为 ``all``。

   .. rst:directive:option:: board
      :type: string

      如果设置，构建命令将针对给定的板级。

   .. rst:directive:option:: shield
      :type: string

      如果设置，构建命令将针对给定的 shield。

      可以用逗号分隔的列表提供多个 shield。

   .. rst:directive:option:: conf

      如果设置，构建命令将使用给定的配置文件。

      如果提供多个配置文件，用双引号括住空格分隔的文件列表，例如 `"a.conf b.conf"`。

   .. rst:directive:option:: gen-args
      :type: string

      如果设置，表示 CMake 调用的额外参数。

   .. rst:directive:option:: build-args
      :type: string

      如果设置，表示构建调用的额外参数。

   .. rst:directive:option:: west-args
      :type: string

      如果设置，west 调用的额外参数（对 ``:tool: cmake`` 忽略）。

   .. rst:directive:option:: flash-args
      :type: string

      如果设置，烧录调用的额外参数。

   .. rst:directive:option:: debug-args
      :type: string

      如果设置，调试调用的额外参数。

   .. rst:directive:option:: debugserver-args
      :type: string

      如果设置，debugserver 调用的额外参数。

   .. rst:directive:option:: attach-args
      :type: string

      如果设置，attach 调用的额外参数。

   .. rst:directive:option:: snippets
      :type: string

      如果设置，表示应用应使用列出的片段编译。

      可以用逗号分隔的列表提供多个片段。

   .. rst:directive:option:: build-dir
      :type: string

      如果设置，应用构建目录将*追加*此相对 Unix 分隔路径到标准构建目录。这主要用于在单个页面中区分一个应用的构建。

   .. rst:directive:option:: build-dir-fmt
      :type: string

      如果设置，假设 `west config build.dir-fmt`` 已设置为此路径。

      与 ``:build-dir:`` 互斥，并依赖于 ``:tool: west``。

   .. rst:directive:option:: goals
      :type: string

      对应用做什么的空格分隔列表（``build``、``flash``、``debug``、``debugserver``、``run`` 中任意组合）。

      完成这些任务的命令将按正确顺序生成。

   .. rst:directive:option:: maybe-skip-config
      :type: no value

      如果设置，表示读者可能已经创建了构建目录并进入其中，将调整文本以说明无需再次执行。

   .. rst:directive:option:: compact
      :type: no value

      如果设置，生成的输出是单个代码块，无额外注释行。


.. _linking_to_zephyr_files:

交叉引用 Zephyr 树中的文件
==========================================

有特殊的角色可用于引用 Zephyr 树中的文件。例如，引用本文档本身可以使用 :rst:role:`zephyr_file` 角色。

.. rst:role:: zephyr_file

   此角色用于引用 Zephyr 树中的文件。例如::

     查看 :zephyr_file:`doc/contribute/documentation/guidelines.rst` 了解更多信息。

   渲染效果为：

     查看 :zephyr_file:`doc/contribute/documentation/guidelines.rst` 了解更多信息。

   通过在文件路径后追加 :samp:`#L{line_number}` 或 :samp:`#L{start_line}-L{end_line}` 可以引用文件中的特定行或行范围::

     参见 :zephyr_file:`doc/contribute/documentation/guidelines.rst#L3` 查看本文档的主标题。

   渲染效果为：

     参见 :zephyr_file:`doc/contribute/documentation/guidelines.rst#L3` 查看本文档的主标题。

   该角色自动验证引用的文件存在于 Zephyr 树中，如果文件未找到，将在文档构建期间生成警告。

   .. note::

      谨慎使用行引用，因为随着链接文件内容的变化，随时间保持其准确性可能具有挑战性。

   如果你想引用"原始"内容，可以改用 :rst:role:`zephyr_raw` 角色。

.. rst:role:: zephyr_raw

   此角色用于引用 Zephyr 树中文件的原始内容。例如::

     查看 :zephyr_raw:`doc/contribute/documentation/guidelines.rst` 了解更多信息。

   渲染效果为：

     查看 :zephyr_raw:`doc/contribute/documentation/guidelines.rst` 了解更多信息。

.. rst:role:: module_file

   此角色用于引用 Zephyr 树中的模块。例如::

        查看 :module_file:`hal_stm32:CMakeLists.txt` 了解更多信息。

   渲染效果为：

        查看 :module_file:`hal_stm32:CMakeLists.txt` 了解更多信息。

   与 :rst:role:`zephyr_file` 类似，你可以引用文件中的特定行或行范围。

交叉引用 GitHub issue 和 pull request
==================================================

.. rst:role:: github

   此角色用于引用 GitHub issue 或 pull request。

   例如，要引用 issue #1234::

     查看 :github:`1234` 了解此已知 issue 的更多背景。

   渲染效果为：

     查看 :github:`1234` 了解此已知 issue 的更多背景。

Doxygen API 文档
=========================

.. app.add_directive("doxygengroup", DoxygenGroupDirective)
.. app.add_role_to_domain("c", "group", CXRefRole())

.. rst:directive:: .. doxygengroup:: name

   此指令用于输出 Doxygen 组的简短描述和指向相应 Doxygen 生成文档的链接。

   所有使用 :rst:dir:`zephyr:code-sample` 指令声明并标记该组为相关的代码示例将自动列出并在渲染输出中引用。

   例如::

     .. doxygengroup:: can_interface

   渲染效果为：

     .. doxygengroup:: can_interface


   .. rubric:: 选项

   .. rst:directive:option:: project
      :type: project name (optional)

      关联的 Doxygen 项目。当配置了多个 Doxygen 项目时这可能很有用。

.. rst:role:: c:group

   此角色用于引用 Zephyr 树中的 Doxygen 组。在 HTML 文档中，它们渲染为指向该组对应 Doxygen 生成文档的链接。例如::

     查看 :c:group:`gpio_interface` 了解更多信息。

   渲染效果为：

     查看 :c:group:`gpio_interface` 了解更多信息。

   你可以提供自定义链接文本，类似于内置的 :rst:role:`ref` 角色。


Kconfig 选项
================

如果你想从文档中引用 Kconfig 选项，可以使用 :rst:role:`kconfig:option` 角色并提供要引用的选项名称。该角色在构建 HTML 输出时会自动生成指向 Kconfig 选项文档的链接。

务必使用 Kconfig 选项的完整名称，包括 ``CONFIG_`` 前缀。

.. rst:role:: kconfig:option

   此角色用于引用 Zephyr 树中的 Kconfig 选项。例如::

     查看 :kconfig:option:`CONFIG_GPIO` 了解更多信息。

   渲染效果为：

     查看 :kconfig:option:`CONFIG_GPIO` 了解更多信息。

.. rst:role:: kconfig:option-regex

   此角色用于创建到 Kconfig 选项正则表达式搜索的链接。它生成指向 Kconfig 搜索页面的链接，提供的正则表达式模式自动填入作为搜索查询。它适用于引用共享公共前缀的多个 Kconfig 选项，或属于公共类别的选项。例如::

     查看 :kconfig:option-regex:`CONFIG_SECURE_STORAGE_ITS_(STORE|TRANSFORM)_.*_CUSTOM` 了解各种自定义可能性。

   渲染效果为：

     查看 :kconfig:option-regex:`CONFIG_SECURE_STORAGE_ITS_(STORE|TRANSFORM)_.*_CUSTOM` 了解各种自定义可能性。

   鼓励提供自定义链接文本使引用更易读。例如::

     查看 :kconfig:option-regex:`ITS Kconfig 选项 <CONFIG_SECURE_STORAGE_ITS_.*>` 了解更多信息。

   渲染效果为：

     查看 :kconfig:option-regex:`ITS Kconfig 选项 <CONFIG_SECURE_STORAGE_ITS_.*>` 了解更多信息。

设备树绑定
==================

如果你想从文档中引用设备树绑定，可以使用 :rst:role:`dtcompatible` 角色并提供要引用的绑定的 compatible 字符串。该角色在构建 HTML 输出时会自动生成指向绑定文档的链接。

.. rst:role:: dtcompatible

   此角色可用于内联引用作为参数给出的设备树 compatible 的生成文档。

   单个 compatible 可能有多于一个页面。例如，当绑定根据节点所在的总线表现不同时就会发生这种情况。如果发生，引用指向一个"消歧"页面，链接到所有可能性，类似于 Wikipedia 消歧页面的工作方式。示例::

     查看 :dtcompatible:`zephyr,input-longpress` 了解更多信息。

   渲染效果为：

     查看 :dtcompatible:`zephyr,input-longpress` 了解更多信息。

代码示例
============

.. rst:directive:: .. zephyr:code-sample:: id

   此指令用于描述代码示例，包括它可能使用哪些值得注意的 API。

   例如::

     .. zephyr:code-sample:: blinky
        :name: Blinky
        :relevant-api: gpio_interface

        使用 GPIO API 永久闪烁一个 LED。

   指令的内容用作代码示例的描述。

   .. rubric:: 选项

   .. rst:directive:option:: name
      :type: text

      表示示例的人类可读短名称。

   .. rst:directive:option:: relevant-api
      :type: text

      可选的空格分隔的 Doxygen 组名称列表，对应代码示例使用的 API。

.. rst:role:: zephyr:code-sample

   此角色用于引用使用 :rst:dir:`zephyr:code-sample` 描述的代码示例。

   例如::

     查看 :zephyr:code-sample:`blinky` 了解更多信息。

   渲染效果为：

     查看 :zephyr:code-sample:`blinky` 了解更多信息。

   它可以完全像内置的 :rst:role:`ref` 角色一样使用，即你可以提供自定义链接文本。例如::

     查看 :zephyr:code-sample:`blinky 代码示例 <blinky>` 了解更多信息。

   渲染效果为：

     查看 :zephyr:code-sample:`blinky 代码示例 <blinky>` 了解更多信息。

.. rst:directive:: .. zephyr:code-sample-category:: id

   此指令用于定义用于分组代码示例的类别。

   例如::

     .. zephyr:code-sample-category:: gpio
        :name: GPIO
        :show-listing:

        与 GPIO 子系统相关的示例。

   指令的内容用作类别的描述。它可以包含任何有效的 reStructuredText 内容。

   .. rubric:: 选项

   .. rst:directive:option:: name
      :type: text

      表示类别的人类可读名称。

   .. rst:directive:option:: show-listing
      :type: flag

      如果设置，将显示类别中代码示例的列表。列表基于当前文档子目录中发现的所有代码示例自动生成。

   .. rst:directive:option:: glob
      :type: text

      匹配要包含在列表中的文件的 glob 模式。默认为 `*/*`，但可以覆盖，例如当示例可能位于不直接在类别目录下的目录中时。

.. rst:role:: zephyr:code-sample-category

   此角色用于引用使用 :rst:dir:`zephyr:code-sample-category` 描述的代码示例类别。

   例如::

     查看 :zephyr:code-sample-category:`cloud` 示例了解更多信息。

   渲染效果为：

     查看 :zephyr:code-sample-category:`cloud` 示例了解更多信息。

.. rst:directive:: .. zephyr:code-sample-listing::

   此指令用于显示一个或多个类别中发现的所有代码示例的列表。

   例如::

     .. zephyr:code-sample-listing::
        :categories: cloud

   渲染效果为：

     .. zephyr:code-sample-listing::
        :categories: cloud

   .. rubric:: 选项

   .. rst:directive:option:: categories
      :type: text

      要显示列表的类别 ID 的空格分隔列表。

   .. rst:directive:option:: live-search
      :type: flag

      在列表正上方包含搜索框的标志。搜索框允许用户按代码示例名称/描述过滤列表，这对于包含大量示例的类别可能很有用。此选项仅在 HTML 构建器中可用。

板级
======

.. rst:directive:: .. zephyr:board:: name

   此指令用于在文档开头表示它是名称作为指令参数给出的板级的主文档页面。

   例如::

     .. zephyr:board:: wio_terminal

   板级的元数据从各种配置文件读取，用于自动填充板级文档的某些部分。使用此指令的板级文档页面可以使用 :rst:role:`zephyr:board` 角色链接。

.. rst:role:: zephyr:board

   此角色用于引用使用 :rst:dir:`zephyr:board` 文档化的板级。

   例如::

     查看 :zephyr:board:`wio_terminal` 了解更多信息。

   渲染效果为：

     查看 :zephyr:board:`wio_terminal` 了解更多信息。

.. rst:directive:: .. zephyr:board-catalog::

   此指令用于生成 Zephyr 支持板级的目录，可用于快速浏览所有支持板级的列表并根据各种标准过滤。

.. rst:role:: zephyr:board-catalog

   此角色用于引用板级目录页面，可选带过滤参数。例如::

     查看 :zephyr:board-catalog:`` 了解更多信息。

   渲染效果为：

     查看 :zephyr:board-catalog:`` 了解更多信息。

   此角色可以完全像内置的 :rst:role:`ref` 角色一样使用，即你可以提供自定义链接文本。例如::

     查看 :zephyr:board-catalog:`使用此 compatible 的板级 <#compatibles=ti,hdc2080>` 了解更多信息。

   渲染效果为：

     查看 :zephyr:board-catalog:`使用此 compatible 的板级 <#compatibles=ti,hdc2080>` 了解更多信息。

.. rst:directive:: .. zephyr:board-supported-hw::

   此指令用于显示当前页文档化板级的所有目标的支持硬件特性。表格基于板级的设备树自动生成。

   此指令必须用于也包含 :rst:dir:`zephyr:board` 指令的文档，因为它依赖板级信息生成表格。

   .. note::

      此指令要求文档在启用硬件特性生成的情况下构建（``zephyr_generate_hw_features`` 配置选项设为 ``True``）。如果禁用，将显示警告消息而非硬件特性表格。

      可以将硬件特性生成限制为来自特定供应商列表的板级，以加快文档构建速度而不完全禁用硬件特性表格。将配置选项 ``zephyr_hw_features_vendor_filter`` 设为要生成特性的供应商列表。如果选项为空，为所有供应商的所有板级生成硬件特性。

      配置选项 ``zephyr_hw_features_twister_extra_flags`` 可用于为 twister 命令提供额外标志。

.. rst:directive:: .. zephyr:board-supported-runners::

   此指令用于显示当前页文档化板级的支持 runner，包括哪个 runner 是烧录和调试的默认。

   此指令必须用于也包含 :rst:dir:`zephyr:board` 指令的文档，因为它依赖板级信息生成表格。

   .. note::

      与 :rst:dir:`zephyr:board-supported-hw` 类似，此指令需要启用硬件特性生成（``zephyr_generate_hw_features`` 配置选项设为 ``True``）才能生成完整表格。如果禁用，将显示警告消息而非 runner 表格。

可访问性指南
************************

可访问性是文档的重要方面，确保所有用户（包括残障人士）都能访问和理解内容。

在编写和维护 Zephyr 项目文档时，请遵循以下指南以提高所有人的可访问性。

图像和插图
==================

所有图像和插图必须包含适当的替代文本（alt 文本），向依赖屏幕阅读器或无法查看图像的用户传达视觉内容的含义。

* 使用 :rst:dir:`image` 指令包含图像时，使用 ``:alt:`` 属性。示例：

  .. code-block:: rst
     :emphasize-lines: 2

     .. image:: image/doc-gen-flow.png
        :alt: 文档生成流程概览

* 如果图像包含文本，确保 alt 文本逐字包含此文本。

* 使用允许标题的 :rst:dir:`figure` 指令时，``:alt:`` 文本仍然重要。alt 文本应描述图像本身，而标题提供额外的上下文或解释。示例：

  .. code-block:: rst
     :emphasize-lines: 4

     .. figure:: ../../images/arch-diagram.png
        :alt: Zephyr 操作系统架构的高层概览，显示层次和组件。

        Zephyr 操作系统架构的高层概览。

- 避免将图像作为传达可以用文字清楚解释的信息的唯一方法。

.. admonition:: 编写 alt 文本的最佳实践
   :class: tip

   * **准确且等价**：呈现与图像相同的本质信息。
   * **简洁**：简洁地传达图像的核心信息。
   * **避免冗余**：不要使用 "Image of..." 或 "Picture of..." 这样的短语，因为屏幕阅读器通常会将元素宣布为图像。
   * **描述，而非解释**：坚持描述图像上视觉呈现的内容。
   * **复杂图像**：对于图表、示意图或其他复杂视觉，在 alt 文本中提供摘要。如果完全理解需要更多细节，考虑在周围文本中或作为插图标题的一部分提供更详细的描述。使用 :ref:`Graphviz <graphviz_diagrams>` 等基于文本的图表工具也可以提高可访问性。


标题和结构
====================

使用 :ref:`headings <headings>` 逻辑地组织文档。这允许辅助技术用户理解文档的组织并高效地导航。

表格
======

表格应仅用于表格数据，且必须对屏幕阅读器可访问。

* 始终为行和列定义标题。

* 尽可能使用 :rst:dir:`list-table` 指令以获得更好的响应性和可访问性。

* 在上下文不那么明显的表格中包含标题。示例：

  .. code-block:: rst
     :emphasize-lines: 1

     .. list-table:: GPIO 引脚配置选项
        :widths: 15 30
        :header-rows: 1

        * - 字段
          - 描述
        * - GPIO_INPUT
          - 将引脚配置为输入
        * - GPIO_OUTPUT
          - 将引脚配置为输出

额外资源
==================

关于 Web 可访问性的更多一般性指导，请参阅 W3C 的 `Web 内容可访问性指南 (WCAG)`_

.. _`Web 内容可访问性指南 (WCAG)`: https://www.w3.org/WAI/standards-guidelines/wcag/

参考
**********

.. target-notes::
