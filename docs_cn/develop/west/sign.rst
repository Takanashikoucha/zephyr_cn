.. _west-sign:

签署二进制文件
################

``west sign`` :ref:`extension <west-extensions>` 命令可用于使用外部工具
为引导加载程序使用而签署 Zephyr 应用二进制文件。在某些配置中，``west sign``
还用于调用外部的后处理工具，该工具将镜像的最终组件"缝合"在一起。
运行 ``west sign -h`` 查看命令行帮助。

rimage
******

rimage 配置采用一种不依赖 Kconfig 或 CMake 的方法，而是依赖
:ref:`west config<west-config>`，类似于
:ref:`west-building-cmake-config`。

签署涉及一层层叠加在彼此之上的多个"包装"脚本：``west
flash`` 调用 ``west build``，后者调用 ``cmake`` 和 ``ninja``，
再调用 ``west sign``，最后调用 ``imgtool`` 或 `rimage`_。
只要所需的签署参数是默认值且相对稳定，这些间接层就不是问题。
另一方面，将 ``imgtool`` 或 ``rimage`` 选项穿过所有这些层
可能会导致层没有抽象任何东西时典型的问题。首先，
这通常需要在每一层编写样板代码。通过所有包装器传递
空白或其他特殊字符的引号可能很困难。复现较低层的 ``west sign``
命令以调试某些构建时问题可能非常耗时：它至少需要启用并搜索
冗长的构建日志来找出实际使用了哪些确切选项。从
构建日志中复制这些选项可能不可靠：由于细微的
环境差异，它可能产生不同的结果。最后也是最糟糕的：在每一层
添加更多样板代码之前，新的签署功能和选项
无法使用。

为避免这些问题，可以在 ``west config`` 中设置 ``rimage`` 参数。
下面是一个 ``workspace/.west/config`` 示例：

.. code-block:: ini

   [sign]
   # Not needed when invoked from CMake
   tool = rimage

   [rimage]
   # Quoting is optional and works like in Unix shells
   # Not needed when rimage can be found in the default PATH
   path = "/home/me/zworkspace/build-rimage/rimage"

   # Not needed when using the default development key
   extra-args = -i 4 -k 'keys/key argument with space.pem'

为了支持引号，值会像
:ref:`west-building-cmake-args` 中一样通过 Python 的 ``shlex.split()`` 解析。

``extra-args`` 会直接传递给 ``rimage`` 命令。上面的
示例与在命令行 ``--`` 之后追加它们的效果相同，如下所示：
``west sign --tool rimage -- -i 4 -k 'keys/key argument with space.pem'``。
如果两者都使用，命令行参数放在最后。

.. _rimage:
   https://github.com/thesofproject/rimage


silabs_commander
****************

``silabs_commander`` 工具用于为 Silicon Labs
设备应用签署、MIC 或加密二进制文件。当 ``sign.tool`` 配置设置为
``silabs_commander`` 时，可以由 ``west sign`` 调用；
或者当设置了 ``CONFIG_SIWX91X_SIGN_KEY`` 或
``CONFIG_SIWX91X_MIC_KEY`` 时，可以由 ``west build`` 调用。

如果设置了 ``CONFIG_SIWX91X_SIGN_KEY`` 或 ``CONFIG_SIWX91X_MIC_KEY`` 之一，
``west flash`` 会自动烧录二进制文件的已签署版本。

``silabs_commander`` 需要在主机上安装 `Simplicity Commander`_。
在设备上配置密钥的过程在 `UG574 SiWx917 SoC Manufacturing Utility User Guide`_ 中有描述。

.. _Simplicity Commander:
   https://www.silabs.com/developer-tools/simplicity-studio/simplicity-commander?tab=downloads
.. _UG574 SiWx917 SoC Manufacturing Utility User Guide:
   https://www.silabs.com/documents/public/user-guides/ug574-siwx917-soc-manufacturing-utility-user-guide.pdf
