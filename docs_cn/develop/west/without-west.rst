.. _no-west:

不使用 west 使用 Zephyr
#########################

本页提供不使用 west 而使用 Zephyr 的信息。
由于涉及额外的工作量，不建议初学者这样做。
特别是，你将不得不"手工"完成以下工作来替代这些功能：

- 克隆 Zephyr 使用的主 zephyr 仓库之外的额外源代码仓库，
  并保持它们处于最新状态
- 向 Zephyr 构建系统指定这些仓库的位置
- 在不了解相关主机工具详细用法的烧录和调试

.. note::

   如果你之前安装过 west 并希望停止使用它，
   请先卸载它：

   .. code-block:: console

      pip3 uninstall west

   否则，Zephyr 的构建系统会找到它并可能尝试使用它。

获取源代码
----------

除了下载 zephyr 源代码仓库本身之外，
你还需要手动克隆该仓库内 :term:`west manifest` 文件中列出的额外项目。

.. code-block:: console

   mkdir zephyrproject
   cd zephyrproject
   git clone https://github.com/zephyrproject-rtos/zephyr
   # clone additional repositories listed in zephyr/west.yml,
   # and check out the specified revisions as well.

当你拉取 zephyr 仓库的变更时，
你也需要维护这些额外仓库，在必要时添加新的仓库，
并将现有仓库保持在最新的修订版。

构建应用
--------

如果你手动指定任何模块，
可以在未安装 west 的情况下直接使用 CMake 和 Ninja（或 make）构建 Zephyr 应用。

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :tool: cmake
   :goals: build
   :gen-args: -DZEPHYR_MODULES=module1;module2;...
   :compact:

安装 west 时进行构建，Zephyr 构建系统会使用它来设置
:ref:`ZEPHYR_MODULES <important-build-vars>`。

如果你没有安装 west，且你的应用不需要这些仓库中的任何一个，
构建仍然可以工作。

如果你没有安装 west，且你的应用*确实*需要这些仓库中的某一个，
你必须按上面所示自己设置 :makevar:`ZEPHYR_MODULES`。

更多细节请参见 :ref:`modules`。

类似地，如果你的应用需要二进制 blob，而你未使用 west，
你需要下载并将这些 blob 放到正确的位置，
而不是使用 ``west blobs``。更多细节请参见 :ref:`bin-blobs`。

烧录与调试
----------

烧录和调试通过 ``west flash``、``west debug``、
``west debugserver``、``west attach`` 和 ``west rtt`` 命令完成，
这些命令记录在 :ref:`west-build-flash-debug` 中。
这些命令需要 west，因此如果你在不使用 west 的情况下使用 Zephyr，
它们就不可用。

没有 west 时，你仍然可以使用适用于你的板卡的任何
:ref:`flash-debug-host-tools`（这些 west 命令所包装的工具）
进行烧录和调试，但你必须自己调用它们，
并使用适用于你的板卡和应用的正确选项。
