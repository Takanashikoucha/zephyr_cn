.. _menuconfig:

交互式 Kconfig 接口
##############################

有两个交互式配置接口可用于探索可用的 Kconfig 选项并进行临时更改：``menuconfig``
和 ``guiconfig``。``menuconfig`` 是基于 curses 的接口，在终端中运行，而
``guiconfig`` 是图形配置接口。

.. note::

   配置也可以通过手动编辑应用构建目录中的 :file:`zephyr/.config` 来更改。
   使用配置接口之一通常更方便，因为它们正确处理配置符号之间的依赖关系。

   如果你尝试在 :file:`zephyr/.config` 中启用一个依赖未满足的符号，赋值将被
   忽略并在重新配置时被覆盖。

要使设置永久化，你应该在 :file:`*.conf` 文件中设置它，如
:ref:`setting_configuration_values` 中所述。

.. tip::

   保存最小配置文件（在 menuconfig 中例如使用 :kbd:`D`）并检查它在使设置
   永久化时可能很有用。最小配置文件只列出与其默认值不同的符号。

要运行配置接口之一，做以下事情：

#. 使用 ``west`` 或 ``cmake`` 按通常方式构建你的应用：

   .. zephyr-app-commands::
      :tool: all
      :cd-into:
      :board: <board>
      :goals: build
      :compact:

#. 要运行基于终端的 ``menuconfig`` 接口，使用以下命令之一：

   .. code-block:: bash

      west build -t menuconfig

   .. code-block:: bash

      ninja menuconfig

   要运行图形 ``guiconfig``，使用以下命令之一：

   .. code-block:: bash

      west build -t guiconfig

   .. code-block:: bash

      ninja guiconfig

   .. note::

      如果你尝试运行 ``guiconfig`` 时得到 ``tkinter`` 的导入错误，你缺少必需的
      包。见 :ref:`installation_linux`。你需要的包通常叫类似
      ``python3-tk``/``python3-tkinter`` 的名字。

      尽管 ``tkinter`` 是标准库的一部分，许多 Python 安装默认不包含它。

   两个接口显示如下：

   .. figure:: menuconfig.png
      :alt: menuconfig 接口

   .. figure:: guiconfig.png
      :alt: guiconfig 接口

   ``guiconfig`` 始终在底部窗口窗格中显示帮助文本和与当前选中项相关的其他信息。
   在终端接口中，按 :kbd:`?` 查看相同信息。

   .. note::

      如果你偏好在 ``guiconfig`` 接口中工作，那么在 *单菜单模式* 中检查你对
      Kconfig 文件做的任何更改是一个好主意，这通过顶部的复选框切换。与完整树
      模式不同，单菜单模式会区分使用 ``config`` 定义的符号和使用
      ``menuconfig`` 定义的符号，显示在 ``menuconfig`` 接口中看起来是什么样子。

#. 在 ``menuconfig`` 接口中按如下方式更改配置值：

   * 使用箭头键导航菜单。也支持常用 `Vim <https://www.vim.org>`__ 键绑定。

   * 使用 :kbd:`Space` 和 :kbd:`Enter` 进入菜单并切换值。菜单旁边显示
     ``--->``。按 :kbd:`ESC` 返回父菜单。

     布尔配置选项用 :guilabel:`[ ]` 括号显示，而数值和字符串值的配置符号用
     :guilabel:`( )` 括号显示。不能更改的符号值显示为 :guilabel:`- -` 或
     :guilabel:`*-*`。

     .. note::

        你也可以按 :kbd:`Y` 或 :kbd:`N` 将布尔配置符号设置为对应值。

   * 按 :kbd:`?` 显示当前选中符号的信息，包括其帮助文本。按 :kbd:`ESC` 或
     :kbd:`Q` 从信息显示返回菜单。

   在 ``guiconfig`` 接口中，要么点击符号旁边的图像来更改其值，要么双击带符号
   的行（这只有在符号没有子项时才有效，因为双击带子项的符号打开/关闭其菜单
   而不是更改值）。

   ``guiconfig`` 也支持键盘控制，与 ``menuconfig`` 类似。

#. 在 ``menuconfig`` 接口中按 :kbd:`Q` 会带出保存并退出对话框（如果有更改要
   保存）：

   .. figure:: menuconfig-quit.png
      :alt: 保存并退出对话框

   按 :kbd:`Y` 将内核配置选项保存到默认文件名（:file:`zephyr/.config`）。除非
   你在实验不同配置，你通常会保存到默认文件名。

   ``guiconfig`` 接口在退出时如果已修改也会提示保存配置。

   .. note::

      构建期间使用的配置文件始终是 :file:`zephyr/.config`。如果你有另一个保存的
      配置想用它构建，复制它到 :file:`zephyr/.config`。确保备份你的原始配置文件。

      也注意在 Linux 和 macOS 上，以 ``.`` 开头的文件名默认不被 ``ls`` 列出。
      使用 ``-a`` 标志查看它们。

在菜单树中查找符号并导航到它可能很麻烦。要直接跳转到符号，按 :kbd:`/` 键
（这在 ``guiconfig`` 中也有效）。这会带出以下对话框，你可以按名称搜索符号并
跳转到它们。在 ``guiconfig`` 中，你也可以直接在对话框中更改符号值。

.. figure:: menuconfig-jump-to.png
   :alt: menuconfig 跳转对话框

.. figure:: guiconfig-jump-to.png
   :alt: guiconfig 跳转对话框

如果你跳转到一个当前不可见的符号（例如，由于依赖未满足），那么 *显示全部模式*
将被启用。在显示全部模式中，所有符号都被显示，包括当前不可见的符号。要关闭
显示全部模式，在 ``menuconfig`` 中按 :kbd:`A` 或在 ``guiconfig`` 中按
:kbd:`Ctrl-A`。

.. note::

   如果当前菜单中没有可见项，显示全部模式不能被关闭。

要弄清楚你跳转到的符号为什么不可见，检查其依赖，要么在 ``menuconfig`` 中按
:kbd:`?`，要么在 ``guiconfig`` 底部的信息窗格中。如果你发现符号依赖另一个未
启用的符号，你可以依次跳转到那个符号查看它是否可以被启用。

.. note::

   在 ``menuconfig`` 中，你可以按 :kbd:`Ctrl-F` 在跳转对话框中查看当前选中项的
   帮助而不离开对话框。

关于 ``menuconfig`` 和 ``guiconfig`` 的更多信息，见
:zephyr_file:`menuconfig.py <scripts/kconfig/menuconfig.py>` 和
:zephyr_file:`guiconfig.py <scripts/kconfig/guiconfig.py>` 顶部的 Python
docstring。
