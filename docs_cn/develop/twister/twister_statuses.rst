.. _twister_statuses:

Twister 状态
##############

什么是 Twister 状态？
=========================

Twister 状态以全面且易于理解的方式表述以下对象的当前状态：

- ``Harness``
- ``TestCase``
- ``TestSuite``
- ``TestInstance``

在实际使用中，大多数用户在 Twister 运行结束后会关注 Instance 和 Case 的状态。

.. tip::

   术语提醒：

   .. tabs::

      .. tab:: ``Harness``

         ``Harness`` 是 Twister 内部的一个 Python 类，用于捕获并分析 Twister 外部程序的输出。为便于阅读，本页不再展开介绍它，因为它不会出现在最终报告中。

      .. tab:: ``TestCase``

         ``TestCase``（也称 Case）是一段旨在验证某个断言的代码，是 Zephyr 中测试的最小细分单元。

      .. tab:: ``TestSuite``

         ``TestSuite``（也称 Suite）是若干 Case 的分组。可以通过 ``testcase.yaml`` 文件按 Suite 粒度调整 Twister 的行为。被这样分组的 Case 之间应当有足够的共同点，使得 Twister 将它们一视同仁地处理是合理的。

      .. tab:: ``TestInstance``

         ``TestInstance``（也称 Instance）是某个平台上的 Suite。Twister 通常按 Instance 汇报结果，尽管在那里的措辞是 "Suites"。如果某个状态被标记为适用于 Suite，那么它同样适用于 Instance。由于二者的区别在本节没有实际意义，因此每当你读到 "Suite" 时，请默认 Instance 也同样适用。

   更详细的解释可以在 :ref:`这里 <twister_tests_long_version>` 找到。

可能的 Twister 状态
=========================

.. list-table:: Twister 状态
   :widths: 10 10 66 7 7
   :header-rows: 1

   * - 代码内
     - 文本内
     - 描述
     - Suite
     - Case
   * - FILTER
     - filtered
     - 静态或运行时过滤器已将该测试从待运行的测试列表中排除。
     - ✓
     - ✓
   * - NOTRUN
     - not run
     - 该测试在当前配置下不可运行，因此未被执行，但构建本身是正确的。
     - ✓
     - ✓
   * - BLOCK
     - blocked
     - 由于测试套件中出现错误或崩溃，该测试未被运行。
     - ✕
     - ✓
   * - SKIP
     - skipped
     - 该测试因前述之外的其他原因被跳过。
     - ✓
     - ✓
   * - ERROR
     - error
     - 该测试在运行自身时产生了错误。
     - ✓
     - ✓
   * - FAIL
     - failed
     - 该测试产生的结果与预期不符。
     - ✓
     - ✓
   * - PASS
     - passed
     - 该测试产生了与预期一致的结果。
     - ✓
     - ✓

**代码内** 和 **文本内** 是某个状态的两种命名语境：前者更偏向 Twister 内部使用，出现在日志中；后者则用于 JSON 报告。

.. note::

   还有两个状态是 Twister 内部使用的：``NONE``（Case 和 Suite 的起始状态）和 ``STARTED``（表示某个 Case 正在执行中）。它们不应出现在最终的 Twister 报告中。如果这些非终态状态出现在报告文件中，说明 Twister 存在问题。


Case 和 Suite 状态组合
============================================

.. list-table:: Case 和 Suite 状态组合
   :widths: 22 13 13 13 13 13 13
   :align: center
   :header-rows: 1
   :stub-columns: 1

   * - ↓ Case\Suite →
     - FILTER
     - ERROR
     - FAIL
     - PASS
     - NOTRUN
     - SKIP
   * - FILTER
     - ✓
     - ✕
     - ✕
     - ✕
     - ✕
     - ✕
   * - ERROR
     - ✕
     - ✓
     - ✕
     - ✕
     - ✕
     - ✕
   * - BLOCK
     - ✕
     - ✓
     - ✓
     - ✕
     - ✕
     - ✕
   * - FAIL
     - ✕
     - ✓
     - ✓
     - ✕
     - ✕
     - ✕
   * - PASS
     - ✕
     - ✓
     - ✓
     - ✓
     - ✕
     - ✕
   * - NOTRUN
     - ✕
     - ✕
     - ✕
     - ✕
     - ✓
     - ✕
   * - SKIP
     - ✕
     - ✓
     - ✓
     - ✓
     - ✕
     - ✓

✕ 表示这样的组合不应在正常的 Twister 运行中出现。换句话说，状态如表列所示的 Suite 中不应包含任何状态如表行所示的 Case。

✓ 表示正确的组合。

按 Suite 状态的详细说明
-------------------------------------------

``FILTER``:
  该状态表示整个 Suite 已被静态过滤，排除在某个 Twister 运行之外。因此，其中的每个 Case 也应具有同样的状态。

``ERROR``:
  Suite 在运行测试时遇到了问题。它要求至少有一个 Case 带有 ``ERROR`` 或 ``BLOCK`` 状态。由于该状态优先于所有其他 Case 状态，所有合法的终态 Case 状态都可以出现在这样的 Suite 中。

``FAIL``:
  Suite 中至少有一个 Case 未能满足其断言。在 ERROR 状态的条件未被满足的前提下，该状态优先于所有其他 Case 状态。

``PASS``:
  Suite 已正常通过。它不能包含任何带有 ``BLOCK``、``ERROR`` 或 ``FAIL`` 状态的 Case，因为这些状态表明 Suite 运行过程中存在问题。

``NOTRUN``:
  整个 Suite 未被运行，仅被构建。它要求其中的所有 Case 都未被运行。由于可运行性按 Suite 粒度决定，其 Case 只适用 ``NOTRUN`` 状态。

``SKIP``:
  整个 Suite 在运行时被跳过。所有 Case 也必须具有 ``SKIP`` 状态。
