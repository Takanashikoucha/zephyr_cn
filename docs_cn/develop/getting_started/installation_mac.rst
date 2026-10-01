.. _mac-setup-alts:

macOS 替代设置说明
##################

.. _mac-gatekeeper:

关于 Gatekeeper 的重要说明
**************************

从 macOS 10.15 Catalina 开始，从 macOS Terminal 应用
（或任何其他终端仿真器）启动的应用程序，
受到与从 Dock 启动的应用程序相同的系统安全策略约束。
这意味着，如果你使用网络浏览器下载可执行二进制文件，
macOS 默认不允许你从 Terminal 执行它们。
要绕过这个问题，你可以采取两种不同的方法：

* 运行 ``xattr -r -d com.apple.quarantine /path/to/folder``，
  其中 ``path/to/folder`` 是存放你想运行的可执行文件的
  外层文件夹的路径。

* 打开 :menuselection:`系统偏好设置 --> 安全性与隐私 --> 隐私`，
  然后向下滚动到 "Developer Tools"。
  接着解锁锁以允许进行更改，
  并勾选对应你所选终端仿真器的复选框。
  这将适用于从该终端程序启动的任何可执行文件。

注意，本节 **不** 适用于使用 Homebrew 安装的可执行文件，
因为 ``brew`` 本身会自动解除它们的隔离状态。
不过，这对大多数 :ref:`工具链` 是适用的。

.. _macOS Gatekeeper: https://en.wikipedia.org/wiki/Gatekeeper_(macOS)

MacPorts 用户的额外说明
**********************

虽然 MacPorts 未被本指南官方支持，
但你可以使用 MacPorts 代替 Homebrew
来获取 macOS 上的所有所需依赖项。
另外注意，你可能需要安装 ``rust`` 和 ``cargo``，
Python 依赖项才能正确安装。
