.. _west-aliases:

West 别名
############

West 允许在本地、全局或系统配置文件中添加别名命令。这些别名为常用或难以记住的命令提供快捷方式，便于开发。

与 ``git`` 别名的工作方式类似，别名命令会被替换为其完整文本，并作为新的 shell 参数列表进行解析（内部使用 Python 函数 `shlex.split()`_ 拆分该值）。这使得可以像传递给原始命令一样添加参数。空格被视为参数分隔符；如果参数不应被拆分，请使用正确的转义。

.. _shlex.split(): https://docs.python.org/3/library/shlex.html#shlex.split

要添加新别名，只需调用 ``west config`` 命令：

.. code-block:: shell

   west config alias.mylist "list -f '{name} {revision}'"

要列出别名，使用 :samp:`west help {some_alias}`。

允许递归别名，因为别名命令可以包含其他别名，从而有效地构建出更复杂但更易记住的命令。

也可以覆盖已有命令，例如传递默认参数：

.. code-block:: shell

   west config alias.update "update -o=--depth=1 -n"

.. warning::

   覆盖/遮蔽其他命令或内置命令属于高级用法，可能导致奇怪的副作用，应谨慎操作。

示例
--------

向全局配置添加 ``west run`` 和 ``west menuconfig`` 快捷方式，以调用 ``west build`` 的对应 CMake 目标：

.. code-block:: shell

   west config --global alias.run "build --pristine=never --target run"
   west config --global alias.menuconfig "build --pristine=never --target menuconfig"

为正在积极开发的示例（sample）创建一个带额外选项的别名：

.. code-block:: shell

   west config alias.sample "build -b native_sim samples/hello_world -t run -- -DCONFIG_ASSERT=y"

覆盖 ``west update`` 以检查本地缓存：

.. code-block:: shell

   west config alias.update "update --path-cache $HOME/.cache/zephyrproject"

通过 west 运行 :ref:`Twister <twister_script>` 时，自动排除 32 位 native 模拟器目标。这在没有 32 位主机 C 库的主机系统上（例如 Linux/AArch64）尤其有用：

.. code-block:: shell

   west config alias.twister "twister --exclude-platform native_sim/native"
