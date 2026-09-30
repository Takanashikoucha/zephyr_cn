.. _twister_statuses:

Twister
Status
##############

什么
是
Twister
Status？
=========================

Twister
Status
用
综合
和
容易
理解
的
方式
表述
当前
状态
of

- ``Harness``
- ``TestCase``
- ``TestSuite``
- ``TestInstance``

在
实践
中，
大多数
用户
将
对
他们
的
Twister
运行
结束
后
的
Instances
和
Cases
的
Statuses
感兴趣。

.. tip::

   Nomenclature
   reminder:

   .. tabs::

      .. tab::
         ``Harness``

         ``Harness``
         是
         Twister
         内部
         的
         Python
         class
         允许
         我们
         捕获
         和
         分析
         Twister
         外部
         程序
         的
         输出。
         它
         被
         从
         这
         页
         移除
         以
         清晰，
         因为
         它
         不
         出现
         在
         最终
         报告
         中。

      .. tab::
         ``TestCase``

         ``TestCase``，
         也
         称为
         Case，
         是
         一
         段
         旨在
         验证
         某
         个
         assertion
         的
         代码。
         它
         是
         Zephyr
         中
         测试
         的
         最小
         细分。

      .. tab::
         ``TestSuite``

         ``TestSuite``，
         也
         称为
         Suite，
         是
         Cases
         的
         分组。


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
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

✕ indicates that such a combination should not happen in a proper Twister run. In other words,
no Suite of a status indicated by the table column should contain any Cases of a status indicated
by the table row.

✓ indicates a proper combination.

Detailed explanation, per Suite Status
-------------------------------------------

``FILTER``:
  This status indicates that the whole Suite has been statically filtered
  out of a given Twister run. Thus, any Case within it should also have such a status.

``ERROR``:
  Suite encountered a problem when running the test. It requires at least one case with
  ``ERROR`` or ``BLOCK`` status. As this takes precedence over all other Case statuses, all valid
  terminal Case statuses can be within such a Suite.

``FAIL``:
  Suite has at least one Case that did not meet its assertions. This takes precedence over
  all other Case statuses, given that the conditions for an ERROR status have not been met.

``PASS``:
  Suite has passed properly. It cannot contain any Cases with ``BLOCK``, ``ERROR``, or ``FAIL``
  statuses, as those indicate a problem when running the Suite.

``NOTRUN``:
  Whole suite was not run, but only built. It requires than all Cases within were not run.
  As runnability is decided on a per-Suite basis, only ``NOTRUN`` is applicable for its Cases.

``SKIP``:
  Whole Suite has been skipped at runtime. All Cases need to have ``SKIP`` status as well.