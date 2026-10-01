.. _twister_blackbox:

Twister 黑盒测试
######################

本指南旨在解释测试文件的结构，使读者能够理解现有文件并创建自己的文件。
所有开发人员都应修复他们弄坏的任何测试，并在引入新功能时创建新测试，
因此这些知识对任何 Twister 开发人员都很重要。

基础
******

Twister 黑盒测试用 Python 编写，使用 ``pytest`` 库。
:ref:`在此处 <integration_with_pytest>` 阅读相关内容。
辅助测试数据沿用其原始格式。测试和数据完全包含在
:zephyr_file:`scripts/tests/twister_blackbox` 目录中，并以 ``test_`` 作为前缀。

黑盒测试不应了解 Twister 的内部代码。相反，它们应像用户一样调用 Twister
并检查结果。

示例测试文件
****************

.. literalinclude:: ./sample_blackbox_test.py
   :language: python
   :linenos:

与 CLI 的比较
*******************

上面的测试运行以下命令：

.. code-block:: console

    twister -i --outdir $OUTDIR -T $TEST_DATA/tests -y --level $LEVEL
    --test-config $TEST_DATA/test_config.yaml -p qemu_x86 -p frdm_k64f

它假设 CLI 中已经运行了 ``zephyr-env.sh`` 或 ``zephyr-env.cmd``。

得益于 ``importlib`` 的 ``exec_module()`` [#f1]_，这样的测试
为我们提供了通常期望的 Twister 运行的所有输出。
我们可以通过 ``args`` 变量轻松设置从 Twister 调用期望的所有标志 [#f2]_。
我们可以在 ``out`` 和 ``err`` 变量中检查标准输出或 stderr。

除了标准输出，我们还可以检查文件输出，这些文件通常放在
``twister-out`` 目录中。大多数时候，我们会将 ``out_path`` 夹具与
``--outdir`` 标志（L52）配合使用，以保持测试生成的文件位于临时目录中。
黑盒测试中通常读取的文件是 ``testplan.json``、``twister.xml`` 和 ``twister.log``。

其他功能
*********************

装饰器
==========

* ``@pytest.mark.usefixtures('clear_log')``
    - 允许我们使用 ``conftest.py`` 中的 ``clear_log`` 夹具。
      该夹具将来将变为 ``autouse``。之后，可以移除此装饰器。
* ``@pytest.mark.parametrize('level, expected_tests', TESTDATA_X, ids=['smoke', 'acceptance'])``
    - 这是 ``pytest`` 测试参数化的示例。
      `在此处 <https://docs.pytest.org/en/7.1.x/example/parametrize.html#different-options-for-test-ids>`__ 阅读相关内容。
      TESTDATA 最常声明为类字段。
* ``@mock.patch.object(TestPlan, 'TEST_DEFINITION_FILENAME', test_filename_mock)``
    - 此装饰器允许我们只使用 ``test_data`` 中定义的测试，
      并忽略 ``tests`` 目录中的 Zephyr 测试用例。**注意所有 ``test_data``
      测试使用** ``test_data.yaml`` **作为文件名，而不是** ``testcase.yaml`` **！**
      `在此处 <https://docs.python.org/3/library/unittest.mock.html>`__ 阅读 ``mock`` 库。

夹具（Fixtures）
========

黑盒测试使用 ``pytest`` 的夹具，进一步阅读可参考
`此处 <https://docs.pytest.org/en/6.2.x/fixture.html>`__。

如果你想添加自己的夹具，请考虑它们将只在一个测试文件中使用，
还是在多个文件中使用。

* 如果在多个文件中使用，请在
  :zephyr_file:`scripts/tests/twister_blackbox/conftest.py` 文件中创建这样的夹具。

    - :zephyr_file:`scripts/tests/twister_blackbox/conftest.py` 已包含一些夹具 -
      参见该文件获取示例。
* 如果只在一个文件中使用，请在该文件中声明它。

    - 考虑改用类字段 - 参见 TESTDATA 获取示例。

如何……
***********

如何在一个测试中多次调用 Twister？
========================================

有时我们想测试需要先前 Twister 使用才能完成的内容。
``--test-only`` 标志是典型示例，因为它需要与先前的 ``--build-only``
Twister 调用配合使用。我们应该如何处理？

如果我们只是两次调用 ``importlib`` 的 ``exec_module``，
我们会遇到日志重复的问题。``twister.log`` 会重复每一行
（如果调用三次则重复三倍，等等），而不是覆盖日志或追加到日志末尾。

这是由 Twister 文件中使用 logger 模块变量导致的。
因此再次执行模块会导致 logger 拥有多个句柄。

为了克服这个问题，在调用之间应当使用：

.. code:: python

    capfd.readouterr()   # 从缓冲区移除输出
                         # 注意：如果你希望所有运行的输出依次出现，
                         # 请跳过这一行。
    clear_log_in_test()  # 移除日志重复


------

.. rubric:: 脚注

.. [#f1] 注意 ``setup_class()`` 类函数，它允许我们运行 ``twister`` Python 文件
          就像直接调用一样（绕过 ``__name__ == '__main__'`` 检查）。

.. [#f2] 我们建议你在几乎所有测试中保持 ``args`` 定义的第一部分完整不变，
          因为它用于通用测试设置。
