.. _coding_style:


编码风格指南
#######################

.. toctree::
   :maxdepth: 1

   naming.rst
   code.rst
   doxygen.rst
   cmake.rst
   devicetree.rst
   kconfig.rst
   python.rst


风格工具
***********

Checkpatch
==========

Linux 内核的 GPL 许可工具 ``checkpatch`` 用于检查编码风格
是否符合规范。

.. note::
   checkpatch 目前无法在 Windows 上运行。

Checkpatch 位于 scripts 目录中。要在提交代码时调用它，
将文件 *$ZEPHYR_BASE/.git/hooks/pre-commit* 设为可执行，
并将其编辑为包含以下内容：

.. code-block:: bash

    #!/bin/sh
    set -e exec
    exec git diff --cached | ${ZEPHYR_BASE}/scripts/checkpatch.pl -

与其在每次提交时都运行 checkpatch，你可能更倾向于
只在向 zephyr 仓库推送前运行它。要做到这一点，
将文件 *$ZEPHYR_BASE/.git/hooks/pre-push* 设为可执行，
并将其编辑为包含以下内容：

.. code-block:: bash

    #!/bin/sh
    remote="$1"
    url="$2"

    z40=0000000000000000000000000000000000000000

    echo "Run push hook"

    while read local_ref local_sha remote_ref remote_sha
    do
        args="$remote $url $local_ref $local_sha $remote_ref $remote_sha"
        exec ${ZEPHYR_BASE}/scripts/series-push-hook.sh $args
    done

    exit 0

如果你想无视 checkpatch 的检查结论，即使报告了问题
也要推送分支，可以在 git push 命令中添加 --no-verify 选项。

运行 ``checkpatch`` 的另一种方式是使用 :ref:`check_compliance_py`
脚本，它会执行额外的风格与合规性检查。

clang-format
=============

`clang-format 工具 <https://clang.llvm.org/docs/ClangFormat.html>`_
可以帮助快速将大量新源代码重新格式化为符合
`编码风格指南`_ 的标准，配合仓库中提供的
``.clang-format`` 配置文件使用。``clang-format`` 与大多数
编辑器都有良好的集成，你也可以像这样手动运行它：

.. code-block:: bash

   clang-format -i my_source_file.c

``clang-format`` 是 LLVM 的一部分，可以从项目的
`发布页面 <https://github.com/llvm/llvm-project/releases>`_ 下载。
注意，如果你是 Linux 用户，``clang-format`` 很可能
已经作为包存在于你的发行版软件仓库中。

当 `编码风格指南`_ 的规范与代码格式化工具生成的
格式存在差异时，以 `编码风格指南`_ 的规范为准。
如果格式化工具与指南之间存在歧义，由维护者决定
应采用哪种风格。

dts-linter
=============

`dts-linter <https://www.npmjs.com/package/dts-linter>`_
可以帮助快速将大量设备树文件重新格式化为符合
`编码风格指南`_ 的标准。你也可以像这样手动运行它：

对于单个文件

.. code-block:: bash

   npx --ignore-scripts --prefix ./scripts/ci dts-linter --format --file board.dts --file board_pinctrl.dtsi --patchFile diff.patch
   git apply diff.patch

你可以省略 ``--file``，这样将格式化命令调用目录下
的所有文件。或者也可以传递 ``--cwd`` 来设置工具
查找文件的基础目录。此选项还用于使补丁文件中的
路径变为相对路径。

你也可以使用以下命令就地修复：

.. code-block:: bash

   npx --ignore-scripts --prefix ./scripts/ci dts-linter --formatFixAll


编辑器集成
~~~~~~~~~~~~~~~~~~

* 对于 VS Code：从 `VS Code Marketplace <https://marketplace.visualstudio.com/items?itemName=KyleMicallefBonnici.dts-lsp>`_ 或 `Open VSIX <https://open-vsx.org/extension/KyleMicallefBonnici/dts-lsp>`_ 安装扩展
* 对于其他支持 LSP 客户端的编辑器：使用 devicetree-language-server `devicetree-language-server <https://www.npmjs.com/package/devicetree-language-server>`_

请确保按照 `Devicetree 风格指南 <https://docs.zephyrproject.org/latest/contribute/style/devicetree.html>`_
的要求正确配置编辑器。
