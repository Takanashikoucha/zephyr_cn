.. _win-setup-alts:

Windows 替代设置说明
####################

.. _win-wsl:

Windows 10 WSL（Windows 子系统 Linux）
**************************************

如果你运行的是较新版本的 Windows 10，
你可以利用其内置功能，
在标准命令提示符上直接本地运行 Ubuntu 二进制文件。
这样你就可以使用 :ref:`Zephyr SDK <toolchain_zephyr_sdk>` 等软件，
而无需搭建虚拟机。

.. warning::
      Windows 10 版本 1803 存在一个问题，
      会导致 CMake 无法正常工作，
      该问题已在版本 1809（及更高版本）中修复。
      更多信息见 :github:`Zephyr Issue 10420 <10420>`。

#. `安装 Windows 子系统 Linux（WSL）`_。

   .. note::
         为了让 Zephyr SDK 正常工作，
         你需要 Windows 10 构建版本 15002 或更高。
         你可以在系统设置的"关于你的电脑"部分
         查看当前运行的 Windows 10 构建版本。
         如果你运行的是较旧的 Windows 10 构建版本，
         可能需要安装 Creator's Update。

#. 按照 :ref:`installation_linux` 文档中的 Ubuntu 说明操作。

.. NOTE FOR DOCS AUTHORS: 提醒：*不要* 将构建文档本身所需的
   依赖项放在这里。

.. _Install the Windows Subsystem for Linux (WSL): https://msdn.microsoft.com/en-us/commandline/wsl/install_guide
