.. _zephyr_doc:

文档生成
########################

这些说明将指导你在本地系统上使用与创建
https://docs.zephyrproject.org 上在线文档相同的文档源
来生成 Zephyr 项目的文档。

.. _documentation-overview:

文档概览
**********************

Zephyr 项目内容使用 reStructuredText 标记语言
（.rst 文件扩展名）和 Sphinx 扩展编写，
并使用 Sphinx 处理以创建格式化的独立网站。
开发者可以以原始 .rst 标记文件的形式查看这些内容，
也可以生成 HTML 内容并直接在工作站上用
Web 浏览器查看。相同的 .rst 内容也被输入到
Zephyr 项目的公共网站文档区域（应用不同的主题）。

你可以从 `reStructuredText`_ 和 `Sphinx`_ 各自的
网站阅读其详细信息。

项目文档包含以下内容：

* 用于生成 https://docs.zephyrproject.org 网站上
  文档的 reStructuredText 源文件。大部分 reStructuredText
  源文件位于 ``/doc`` 目录中，但其他文件存储
  在代码源树中其特定组件附近（如 ``/samples``
  和 ``/boards``）

* 用于创建所有 API 特定文档的 Doxygen 生成材料，
  同样位于 https://docs.zephyrproject.org

* 基于源代码树中 Kconfig 文件为内核配置选项
  生成的脚本生成材料

.. graphviz::
   :caption: 文档构建流程示意图

   digraph {
      rankdir=LR

      images [shape="rectangle" label=".png, .jpg\nimages"]
      rst [shape="rectangle" label="restructuredText\nfiles"]
      conf [shape="rectangle" label="conf.py\nconfiguration"]
      rtd [shape="rectangle" label="read-the-docs\ntheme"]
      header [shape="rectangle" label="c header\ncomments"]
      xml [shape="rectangle" label="XML"]
      html [shape="rectangle" label="HTML\nweb site"]
      sphinx[shape="ellipse" label="sphinx +\ndocutils"]
      images -> sphinx
      rst -> sphinx
      conf -> sphinx
      header -> doxygen
      doxygen -> xml
      xml-> sphinx
      rtd -> sphinx
      sphinx -> html
   }


reStructuredText 文件由 Sphinx 文档系统处理，
并使用 doxygen 生成的 API 材料。
在本地生成文档需要额外的工具，
如下文各节所述。

.. _documentation-processors:

安装文档处理器
***************************************

我们的文档处理已测试可与以下版本配合运行：

* Doxygen 版本 1.17.0
* Graphviz 2.43
* Latexmk 版本 4.83
* 仓库文件 ``doc/requirements.txt`` 中列出的
  所有 Python 依赖项

要安装文档工具，首先按照 :ref:`getting_started`
中的说明安装 Zephyr。然后安装仅生成文档所需的
额外工具，如下所述：

.. doc_processors_installation_start

.. tabs::

   .. group-tab:: Linux

      所有 Linux 安装的通用步骤，安装构建文档所需的
      Python 依赖项：

      .. code-block:: console

         pip install -U -r ~/zephyrproject/zephyr/doc/requirements.txt

      在 Ubuntu Linux 上：

      .. code-block:: console

         sudo apt-get install --no-install-recommends doxygen graphviz librsvg2-bin \
         texlive-latex-base texlive-latex-extra latexmk texlive-fonts-recommended imagemagick

      在 Fedora Linux 上：

      .. code-block:: console

         sudo dnf install doxygen graphviz texlive-latex latexmk \
         texlive-collection-fontsrecommended librsvg2-tools ImageMagick

      在 Clear Linux 上：

      .. code-block:: console

         sudo swupd bundle-add texlive graphviz ImageMagick

      在 Arch Linux 上：

      .. code-block:: console

         sudo pacman -S graphviz doxygen librsvg texlive-core texlive-bin \
         texlive-latexextra texlive-fontsextra imagemagick

   .. group-tab:: macOS

      安装构建文档所需的 Python 依赖项：

      .. code-block:: console

         pip install -U -r ~/zephyrproject/zephyr/doc/requirements.txt

      使用 ``brew`` 和 ``tlmgr`` 安装工具：

      .. code-block:: console

         brew install doxygen graphviz mactex librsvg imagemagick
         tlmgr install latexmk
         tlmgr install collection-fontsrecommended

   .. group-tab:: Windows

      安装构建文档所需的 Python 依赖项：

      .. code-block:: console

         pip install -U -r %HOMEPATH$\zephyrproject\zephyr\doc\requirements.txt

      以**管理员**身份打开 ``cmd.exe`` 窗口并运行以下命令：

      .. code-block:: console

         choco install doxygen.install graphviz strawberryperl miktex rsvg-convert imagemagick

      .. note::
         在 Windows 上，Sphinx 可执行文件 ``sphinx-build.exe``
         位于 Python 安装路径的 ``Scripts`` 文件夹中。
         根据你的 Python 安装方式，你可能需要将此文件夹
         添加到 ``PATH`` 环境变量中。按照
         `Windows Python Path`_ 中的说明在需要时添加。

.. doc_processors_installation_end

文档展示主题
********************************

Sphinx 通过使用主题支持轻松定制生成的文档
外观。替换主题文件并再次运行 ``make html``，
输出布局和样式就会改变。``read-the-docs`` 主题
作为 :ref:`install_py_requirements` 步骤的一部分
安装在入门指南中。

运行文档处理器
************************************

你在 Zephyr 项目 git 仓库克隆副本中的 ``/doc`` 目录
包含所有 .rst 源文件、额外工具和用于生成 Zephyr
项目技术文档本地副本的 Makefile。假设本地 Zephyr
项目副本位于主文件夹中的 ``zephyr`` 文件夹中，
以下是本地生成 html 内容的命令：

.. code-block:: console

   # On Linux/macOS
   cd ~/zephyrproject/zephyr/doc
   # On Windows
   cd %userprofile%\zephyrproject\zephyr\doc

   # Use cmake to configure a Ninja-based build system:
   cmake -GNinja -B_build .

   # Enter the build directory
   cd _build

   # To generate HTML output, run ninja on the generated build system:
   ninja html
   # If you modify or add .rst files, run ninja again:
   ninja html

   # To generate PDF output, run ninja on the generated build system:
   ninja pdf

.. warning::

   文档构建系统会在构建目录中创建用于生成文档的
   每个 .rst 文件的副本，以及这些 .rst 文件引用的
   依赖项。

   这意味着 Sphinx 警告和错误指的是**副本**，
   而**不是 Zephyr 中版本控制的原文件**。
   请务必小心，不要意外编辑错误消息中
   文件的副本，因为这些更改不会被保存。

根据你的开发系统，收集和生成 HTML 内容最多
需要 15 分钟。完成后，你可以在
``doc/_build/html/index.html`` 启动浏览器查看 HTML
输出，如果生成了 PDF 文件，则位于
``doc/_build/latex/zephyr.pdf``。

如果你想从头构建文档，只需删除构建文件夹的内容
并再次运行 ``cmake`` 和 ``ninja``。

.. note::

   如果你从文档中添加或删除文件，需要重新运行 CMake。

在 Unix 平台上，可以使用便捷的 :zephyr_file:`doc/Makefile`
直接从中构建文档：

.. code-block:: console

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output
   make html

   # To generate PDF output
   make pdf

开发者模式文档构建
********************************

在对文档进行主要更改和测试时，我们提供了一个选项
来临时存根自动生成的设备树绑定文档，
使文档构建过程运行更快。

要启用此模式，在调用 cmake 时设置以下选项::

   -DDT_TURBO_MODE=1

另一个通常耗时较长的步骤是为每个板级生成
支持功能列表。可以通过在调用 cmake 时设置以下
选项来禁用::

   -DHW_FEATURES_TURBO_MODE=1

使用以下目标调用 :command:`make` 将在不启用
上述任何功能的情况下构建文档::

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output without detailed Devicetree bindings documentation
   # and supported features index
   make html-fast

在编写叙述页面时为了更快的迭代，额外的
``SKIP_*`` 选项允许跳过整个类别的自动生成内容：

``SKIP_DOXYGEN``
   跳过运行 Doxygen 和构建 C API 参考。

``SKIP_KCONFIG``
   跳过生成 Kconfig 选项参考及其搜索页面。

``SKIP_EXTERNAL_CONTENT``
   跳过复制在 ``doc/`` 文件夹外部维护的
   板级、示例和片段页面（即
   :zephyr_file:`boards`、:zephyr_file:`samples`
   和 :zephyr_file:`snippets` 文件夹的内容）。

每个选项可以单独启用::

   make html SKIP_DOXYGEN=1

:command:`make html-minimal` 目标在 ``html-fast`` 之上
组合了所有选项，使其成为预览叙述页面更改的最快方式::

   make html-minimal

.. warning::

   被跳过的生成器本应产生的内容会被占位符替换，
   对它的交叉引用渲染为纯文本，相关警告被抑制。
   因此使用任何 ``SKIP_*`` 选项的构建仅适用于
   本地预览：不能用于验证交叉引用，
   其输出不得发布。

在处理特定供应商的板级文档时，也可以将
支持功能列表的生成限制为板级供应商的子集。
这可以通过在调用 cmake 时设置以下选项实现::

   -DHW_FEATURES_VENDOR_FILTER=vendor1,vendor2

此选项也可以与 :command:`make` 包装器一起使用::

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output with supported features limited to a subset of vendors
   make html HW_FEATURES_VENDOR_FILTER=vendor1,vendor2

本地查看生成的文档
***************************************

生成的 HTML 文档可以用 python 在本地托管，
用 Web 浏览器查看：

.. code-block:: console

   $ python3 -m http.server -d _build/html

.. note::

   WSL2 用户可能需要显式将地址绑定到 ``127.0.0.1``
   才能从主机访问：

   .. code-block:: console

      $ python3 -m http.server -d _build/html --bind 127.0.0.1

或者，可以使用 ``make html-live``（或 ``make html-live-fast``）
命令构建文档，该命令会构建文档、在本地托管它，
并监视文档目录的更改。观察到更改时，
它会自动重新构建文档并刷新托管的文件。

独立构建 Doxygen 文档
*********************************************

``doxygen`` 构建目标可用于仅构建 Doxygen（API）文档，
这比构建完整文档集快得多::

   cd ~/zephyrproject/zephyr/doc
   make doxygen

输出可在 ``_build/doxygen/html`` 中找到。

``doxygen-xml`` 目标构建相同的文档，仅启用 XML 输出，
位于 ``_build/doxygen-xml/xml``。

在常规文档构建中，从 Doxygen 注释到主文档的引用
（例如 ``@kconfig{}``、``@dtcompatible{}`` 或 ``@rstref{}``，
参见 :ref:`doxygen_sphinx_xrefs`）会自动解析为超链接。
在独立 Doxygen 构建中，由于其余文档不可用，
它们保持为纯文本。

将外部 Doxygen 项目链接到 Zephyr
************************************************

基于 Zephyr 功能构建并希望通过 Doxygen 中的
@ref 引用 Zephyr 文档的外部项目，可以利用
在 `zephyr.tag <../../doxygen/html/zephyr.tag>`_
导出的标签文件。

下载后，标签文件可以在自定义 ``doxyfile.in``
中如下使用::

   TAGFILES = "/path/to/zephyr.tag=https://docs.zephyrproject.org/latest/doxygen/html/"

更多信息请参阅 `Doxygen External Documentation`_。


.. _reStructuredText: https://sphinx-doc.org/rest.html
.. _Sphinx: https://sphinx-doc.org/
.. _Windows Python Path: https://docs.python.org/3/using/windows.html#finding-the-python-executable
.. _Doxygen External Documentation: https://www.doxygen.nl/manual/external.html
