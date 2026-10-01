.. _python_style:

Python 风格指南
#######################

Python 代码应遵循 `PEP 8`_ 规范进行格式化。Zephyr 使用 `ruff formatter`_ 来实现这一点。该格式化器有明确的主见，旨在保证一致性、通用性、可读性，并减少 git 差异。

要应用格式化器，请运行：

.. code-block:: shell

   ruff check --select I --fix <file> # Sort imports
   ruff format <file>

Ruff 配置
******************

在默认配置之上应用了一组少量选项：

* 行长度不超过 100 列。
* 单引号 ``'`` 和双引号 ``"`` 两种引号风格均被允许。
* 行尾将被转换为 ``\n``，这是 Unix 上的默认行尾。

排除文件
**************

格式化器在 CI 中强制执行，但仅针对新添加的 Python 文件，因为引入该机制时项目已经拥有庞大的 Python 代码库。
:zephyr_file:`.ruff-excludes.toml` 文件中有一个 ``[format]`` 节，列出了当前所有被排除的文件。
鼓励贡献者在修改被排除的文件时，将其从列表中移除，并在单独的提交中对其进行格式化。

.. _PEP 8:
   https://peps.python.org/pep-0008/

.. _ruff formatter:
   https://docs.astral.sh/ruff/formatter/