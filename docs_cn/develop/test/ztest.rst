.. _test-framework:

测试框架
###############

Zephyr 测试框架（Ztest）提供一个简单的测试框架，设计用于在开发期间使用。它提供基本的断言宏和通用的测试结构。

该框架可以以两种方式使用：要么作为集成测试的通用框架，要么用于单元测试特定模块。

.. contents::
   :depth: 1
   :local:
   :backlinks: top

快速入门 - 集成测试
*********************************

一个简单的可运行基础位于 :zephyr_file:`samples/subsys/testsuite/integration`。要为 **foo** 组件的 **bar** 部件创建测试应用，应将该示例文件夹复制到 ``tests/foo/bar``，并编辑其中的文件，使其适应你的测试应用目的。

要构建并执行测试应用中定义的所有适用测试场景，请使用 :ref:`Twister <twister_script>` 工具，例如：

.. code-block:: console

    west twister -T tests/foo/bar/

要只选择一个测试场景，请使用 ``--scenario`` 命令运行 Twister：

.. code-block:: console

   west twister --scenario tests/foo/bar/your.test.scenario.name

在上面的命令行中，``tests/foo/bar`` 是测试应用的路径，``your.test.scenario.name`` 引用 :file:`tests.yaml` 文件中定义的测试场景，其形式类似于样板测试套件示例中的 ``sample.testing.ztest``。

有关 Twister 如何处理 Ztest 应用的更多细节，请参见 :ref:`Twister 测试项目图 <twister_test_project_diagram>`。

该示例包含以下文件：

.. literalinclude:: ../../../samples/subsys/testsuite/integration/CMakeLists.txt
   :language: CMake
   :caption: CMakeLists.txt
   :linenos:

.. literalinclude:: ../../../samples/subsys/testsuite/integration/tests.yaml
   :language: yaml
   :caption: tests.yaml
   :linenos:

.. literalinclude:: ../../../samples/subsys/testsuite/integration/prj.conf
   :language: text
   :caption: prj.conf
   :linenos:

.. literalinclude:: ../../../samples/subsys/testsuite/integration/src/main.c
   :language: c
   :caption: src/main.c
   :linenos:

测试应用可以由多个测试套件组成，这些套件可以测试功能或 API。实现测试用例的函数应遵循以下准则：

* 测试用例函数名应以 **test_** 为前缀
* 测试用例应使用 doxygen 进行文档化
* 测试用例函数名应在被测试的章节或组件中保持唯一

例如：

.. code-block:: C

   /**
    * @brief Test Asserts
    *
    * This test case verifies the zassert_true macro.
    */
   ZTEST(my_suite, test_assert)
   {
           zassert_true(1, "1 was false");
   }

列出测试
=============

Zephyr 代码树中的测试（测试应用）由许多测试场景组成，它们作为项目的一部分运行，测试相似的功能，例如某个 API 或某项功能。``twister`` 脚本可以解析所有测试应用或部分测试应用中的测试场景、套件和用例，并可以生成细粒度级别的报告，即测试用例是通过还是失败，或者被阻止或跳过。

Twister 通过解析源文件来查找测试用例名称，因此例如你可以通过运行以下命令列出所有内核测试用例：

.. code-block:: console

   west twister --list-tests -T tests/kernel

跳过测试
=============

特殊或特定架构的测试无法在所有平台和架构上运行，但我们仍希望统计这些测试并将它们报告为已跳过。由于测试清单和测试列表是从代码中提取的，在测试套件内部添加条件判断并非最优做法。需要针对特定平台或功能跳过的测试，，必须使用 :c:func:`ztest_test_skip` 或 :c:macro:`Z_TEST_SKIP_IFDEF` 显式报告跳过。如果测试运行了，它必须报告通过或失败。例如：

.. code-block:: C

   #ifdef CONFIG_TEST1
   ZTEST(common, test_test1)
   {
        zassert_true(1, "true");
   }
   #else
   ZTEST(common, test_test1)
   {
        ztest_test_skip();
   }
   #endif

   ZTEST(common, test_test2)
   {
        Z_TEST_SKIP_IFDEF(CONFIG_BUGxxxxx);
        zassert_equal(1, 0, NULL);
   }

   ZTEST_SUITE(common, NULL, NULL, NULL, NULL, NULL);

.. _ztest_unit_testing:

快速入门 - 单元测试
**************************

Ztest 可用于单元测试。这意味着无需包含整个 Zephyr 操作系统来测试单个函数，你可以将测试精力集中在特定模块上。这会加快测试速度，因为只需编译该模块，并且被测函数将被直接调用。

要设置单元测试，你需要在包含单元测试源文件的目录中添加一个 CMakeLists.txt、一个 tests.yaml 和一个 prj.conf。该目录生成的二进制文件使用 ``-DBOARD=unit_testing`` 构建。调用 Twister 时，脚本 ``zephyr/scripts/pylib/twister/twisterlib/testplan.py`` 会过滤掉所有未设置 ``type: unit`` 的 ``tests.yaml``。只有单元测试会使用 ``BOARD=unit_testing`` 的固件构建来执行。

.. note::
   单元测试作为 **native** 应用在主机上运行，因此与 :ref:`POSIX 架构<Posix arch>` 文档中所述的 :ref:`限制 <posix_arch_limitations>` 类似。因此，运行单元测试仅支持 Linux。要在 Windows 或 macOS 上运行单元测试，必须使用运行 Linux 来宾系统的容器或虚拟机。请遵循与 :ref:`POSIX Arch 依赖<posix_arch_deps>` 相同的说明。

.. _unit_testing_board:

``unit_testing`` 开发板
==========================

单元测试针对特殊的 ``unit_testing`` 开发板（:zephyr_file:`subsys/testsuite/boards/unit_testing`）构建。它不是真实的硬件，也不是模拟目标：它是一个带有 ``arch: unit`` 的伪开发板，使用主机工具链生成一个普通的本地可执行文件。使用 ``-DBOARD=unit_testing`` 选择它（Twister 会自动为标记 ``type: unit`` 的场景这样做）只会构建并链接你添加到 ``testbinary`` 目标的源文件以及 Ztest 单元测试框架。

关键的是，**Zephyr 内核和操作系统根本不会被构建**。没有启动序列、没有调度器、没有由设备树驱动的设备初始化，也没有驱动模型。被测函数被编译到测试二进制文件中并被直接调用。被测模块所依赖的任何内核 API 或其他依赖项都必须由测试本身提供，通常作为桩（stub）或 :ref:`mock <mocking-fff>`。

.. _unit_testing_vs_native_sim:

与 ``native_sim`` 及其他开发板的区别
-----------------------------------------------

很容易将 ``unit_testing`` 开发板与 :zephyr:board:`native_sim` 混淆，因为两者都在主机上运行。它们有着根本性的不同：

* :zephyr:board:`native_sim` 构建 **完整的 Zephyr 操作系统** —— 内核、设备树、Kconfig、驱动和子系统 —— 生成一个主机二进制文件，它像真实硬件上的 Zephyr 镜像一样启动和运行，只是编译目标是主机而非目标 SoC。使用它在主机上运行完整应用和集成测试。这些开发板的测试 **不** 设置 ``type: unit``。

* ``unit_testing`` 不构建 **任何** 上述内容。它只链接被测代码和 Ztest，其他所有内容都被桩化或模拟，并直接调用被测函数。这使得构建和运行速度很快，并保持对单一模块的关注，代价是必须为每个依赖项提供桩。这些测试必须设置 ``type: unit``（参见 :ref:`下文 <tests_yaml_unit>`）。

简而言之，要在运行中的 Zephyr 系统上下文中验证代码，请使用 ``native_sim``；要测试一个隔离模块而不引入内核，请使用 ``unit_testing``。

CMakeLists.txt
=============

要声明源文件夹中存在的单元测试，你需要从 CMake :zephyr_file:`unittest <cmake/modules/unittest.cmake>` 组件将相关源文件添加到 ``testbinary`` 目标。参见下面的最小示例：

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.28.0)

   project(app)
   find_package(Zephyr COMPONENTS unittest REQUIRED HINTS $ENV{ZEPHYR_BASE})
   target_sources(testbinary PRIVATE main.c)

由于你不会包含大多数代码所依赖的基本内核数据结构，因此必须在测试中提供函数桩。Ztest 提供了一些用于模拟函数的辅助功能，如下所示。

在单元测试中，mock 对象可以模拟复杂真实对象的行为，并通过验证与对象的交互是否发生来判断测试是失败还是通过；如有需要，还可以断言该交互的顺序。

.. _tests_yaml_unit:

tests.yaml
==========

你必须在 tests.yaml 中将键 "type" 的值设置为 "unit"

.. code-block:: yaml

   tests:
      testscenario.testsuite:
         tags: your_tag
         type: unit

prj.conf
========

对于单元测试，该文件通常只包含

.. code-block:: kconfig

   CONFIG_ZTEST=y

如果你的单元测试需要额外的库（例如 math-lib），你必须通过 CMakeLists.txt 或在 tests.yaml 中添加它们：

.. code-block:: yaml

   tests:
      testscenario.testsuite:
         tags: your_tag
         type: unit
         extra_args:
            - EXTRA_LDFLAGS="-lm"

单元测试的示例可以在 :zephyr_file:`tests/unit/` 文件夹中找到。


创建测试套件
*********************

使用 Ztest 创建测试套件就像调用 :c:macro:`ZTEST_SUITE` 一样简单。该宏接受以下参数：

* ``suite_name`` - 套件名称。该名称在单个二进制文件中必须唯一。
* :c:type:`ztest_suite_predicate_t` - 一个可选的谓词函数，用于决定测试何时运行。谓词函数会收到通过 :c:func:`ztest_run_all` 传入的全局状态指针，并应返回布尔值以决定是否运行该套件。
* :c:type:`ztest_suite_setup_t` - 一个可选的 setup（设置）函数，返回一个测试 fixture。每次运行测试套件时，它会调用并执行一次。
* :c:type:`ztest_suite_before_t` - 一个可选的 before（前置）函数，在该套件中每个测试运行之前执行。
* :c:type:`ztest_suite_after_t` - 一个可选的 after（后置）函数，在该套件中每个测试运行之后执行。
* :c:type:`ztest_suite_teardown_t` - 一个可选的 teardown（拆卸）函数，在该套件所有测试结束时执行。

下面是使用谓词函数的测试套件示例：

.. code-block:: C

   #include <zephyr/ztest.h>
   #include "test_state.h"

   static bool predicate(const void *global_state)
   {
        return ((const struct test_state*)global_state)->x == 5;
   }

   ZTEST_SUITE(alternating_suite, predicate, NULL, NULL, NULL, NULL);

向套件添加测试
***********************

有 5 个宏用于向套件添加测试，它们是：

* :c:macro:`ZTEST` ``(suite_name, test_name)`` - 可用于按 ``test_name`` 向 ``suite_name`` 指定的套件添加测试。
* :c:macro:`ZTEST_P` ``(suite_name, test_name)`` - 向指定套件添加值参数化测试。测试体对每个注册的参数值执行一次。在测试体内，调用 :c:func:`ztest_get_current_param` 或使用 :c:macro:`ZTEST_GET_PARAM` 类型化辅助函数获取当前值。套件 fixture（``data`` 参数）与参数相互独立，永远不会被参数值覆盖。有关完整 API，请参见 `值参数化测试`_。
* :c:macro:`ZTEST_USER` ``(suite_name, test_name)`` - 行为与 :c:macro:`ZTEST` 相同，只是当 :kconfig:option:`CONFIG_USERSPACE` 启用时，测试将在用户空间线程中运行。
* :c:macro:`ZTEST_F` ``(suite_name, test_name)`` - 行为与 :c:macro:`ZTEST` 相同，只是测试函数中已包含一个名为 ``fixture`` 的变量，其类型为 ``<suite_name>_fixture``。
* :c:macro:`ZTEST_USER_F` ``(suite_name, test_name)`` - 将 :c:macro:`ZTEST_F` 的 fixture 功能与测试的用户空间线程功能相结合。

测试 fixtures
=============

测试 fixture 可用于帮助简化重复的测试设置操作。在许多情况下，同一套件中的测试需要先进行某种初始设置，然后在每个测试之间进行某种形式的重置。通过 fixture 可以按以下方式实现：

.. code-block:: C

   #include <zephyr/ztest.h>

   struct my_suite_fixture {
        size_t max_size;
        size_t size;
        uint8_t buff[1];
   };

   static void *my_suite_setup(void)
   {
        /* Allocate the fixture with 256 byte buffer */
        struct my_suite_fixture *fixture = malloc(sizeof(struct my_suite_fixture) + 255);

        zassume_not_null(fixture, NULL);
        fixture->max_size = 256;

        return fixture;
   }

   static void my_suite_before(void *f)
   {
        struct my_suite_fixture *fixture = (struct my_suite_fixture *)f;
        memset(fixture->buff, 0, fixture->max_size);
        fixture->size = 0;
   }

   static void my_suite_teardown(void *f)
   {
        free(f);
   }

   ZTEST_SUITE(my_suite, NULL, my_suite_setup, my_suite_before, NULL, my_suite_teardown);

   ZTEST_F(my_suite, test_feature_x)
   {
        zassert_equal(0, fixture->size);
        zassert_equal(256, fixture->max_size);
   }

在用户空间线程中使用测试 fixture 分配的内存（例如在 :c:macro:`ZTEST_USER` 或 :c:macro:`ZTEST_USER_F` 执行期间），要求该内存被声明为可被用户空间访问。这是因为 fixture 内存由内核空间拥有并初始化。Ztest 框架提供 :c:macro:`ZTEST_DMEM` 和 :c:macro:`ZTEST_BMEM` 宏，用于此类用户/内核空间共享内存。

高级功能
*****************

.. _value-parameterized-tests:

值参数化测试
=========================

值参数化测试允许单个测试体对给定列表中的每个值执行一次，类似于 GoogleTest 的 ``TEST_P`` / ``INSTANTIATE_TEST_SUITE_P`` 模式。fixture 和参数完全独立：套件 ``setup()`` 的返回值始终作为 ``data`` 传入，永远不会被参数值覆盖。

声明参数化测试体
------------------------------------

使用 :c:macro:`ZTEST_P` 的方式与 :c:macro:`ZTEST` 相同。在测试体内，``data`` 指针携带套件 fixture（与 :c:macro:`ZTEST_F` 相同）。当前参数值通过运行时访问器获取：

.. code-block:: C

   #include <zephyr/ztest.h>

   struct my_suite_fixture {
        int initial_value;
   };

   static void *my_suite_setup(void) {
        static struct my_suite_fixture f = { .initial_value = 42 };
        return &f;
   }

   ZTEST_SUITE(my_suite, NULL, my_suite_setup, NULL, NULL, NULL);

   ZTEST_P(my_suite, test_multiply)
   {
        struct my_suite_fixture *f = (struct my_suite_fixture *)data;
        int factor = ZTEST_GET_PARAM(int);

        /* fixture is always intact, regardless of parameter */
        zassert_equal(f->initial_value, 42, "fixture corrupted");
        zassert_true(f->initial_value * factor > 0, "product must be positive");
   }

声明参数值
---------------------------

使用 :c:macro:`ZTEST_DEFINE_PARAM_VALUES` 从字面值创建一个静态值集：

.. code-block:: C

   ZTEST_DEFINE_PARAM_VALUES(small_factors, int, 1, 2, 3);

对于已存储在数组中的值，使用 :c:macro:`ZTEST_DEFINE_PARAM_VALUES_ARRAY`：

.. code-block:: C

   static const int big_factors[] = { 10, 100, 1000 };
   ZTEST_DEFINE_PARAM_VALUES_ARRAY(big_factor_vals, big_factors);

对于数值范围，使用 :c:macro:`ZTEST_DEFINE_PARAM_RANGE`，它对应 GoogleTest 的 ``testing::Range(begin, end [, step])`` 语义。取值为 ``{begin, begin+step, ...}``，直到但 **不** 包含 ``end``。不会分配后备数组，因此大范围没有任何 RAM 开销：

.. code-block:: C

   /* {0, 2, 4, 6, 8} — 5 values, step is supplied explicitly */
   ZTEST_DEFINE_PARAM_RANGE(even_vals, int, 0, 10, 2);

   /* {1, 2, 3, 4, 5} — step=1 is the common case */
   ZTEST_DEFINE_PARAM_RANGE(one_to_five, int, 1, 6, 1);

.. note::

   ``ZTEST_DEFINE_PARAM_RANGE`` 要求 ``end > begin`` 且 ``step > 0``，两者均通过 :c:macro:`BUILD_ASSERT` 在编译时强制执行。

对于必须 **在运行时计算** 的值——例如随机数、硬件传感器读数，或由自定义算法产生的值——使用 :c:macro:`ZTEST_DEFINE_PARAM_GENERATOR` 或 :c:macro:`ZTEST_DEFINE_PARAM_GENERATOR_WITH_SETUP`。两者都接受一个用户提供的生成器回调，其签名为 ``void gen(size_t index, void *out)``，每次调用写入一个值。与范围一样，不会分配后备数组。

``_WITH_SETUP`` 变体会在分派循环之前 **一次** 额外调用 ``void setup(void)`` 钩子。这是为 PRNG 设置种子、重置有状态计数器或打开生成器所需资源的合适位置：

.. code-block:: C

   #include <zephyr/random/random.h>

   /* Seed the RNG before the first iteration so failures are reproducible. */
   static void seed_rng(void)
   {
        sys_rand_seed(MY_FUZZ_SEED);
   }

   static void rand_u32_gen(size_t idx, void *out)
   {
        ARG_UNUSED(idx);
        *(uint32_t *)out = sys_rand32_get();
   }

   ZTEST_DEFINE_PARAM_GENERATOR_WITH_SETUP(fuzz_vals, uint32_t, MY_FUZZ_ITERATIONS,
                                           seed_rng, rand_u32_gen);

当不需要 setup（设置）时，使用更简单的形式：

.. code-block:: C

   static void deterministic_gen(size_t idx, void *out)
   {
        /* Deterministic but computed at runtime (e.g. based on hardware ID). */
        *(uint32_t *)out = get_device_seed() ^ (uint32_t)idx;
   }

   ZTEST_DEFINE_PARAM_GENERATOR(hw_vals, uint32_t, 16U, deterministic_gen);

.. note::

   两个生成器宏的 ``count_`` 参数必须是常量表达式（数字字面量、``#define``，或 ``MY_FUZZ_ITERATIONS`` 之类的 Kconfig 符号）。不支持真正动态的计数。

结构体类型的参数工作方式相同：

.. code-block:: C

   struct point { int x; int y; };

   static const struct point corners[] = { {0,0}, {1,0}, {0,1}, {1,1} };
   ZTEST_DEFINE_PARAM_VALUES_ARRAY(corner_vals, corners);

   ZTEST_P(my_suite, test_in_unit_square)
   {
        const struct point *p = ZTEST_GET_PARAM_PTR(struct point);
        zassert_true(p->x >= 0 && p->x <= 1 && p->y >= 0 && p->y <= 1,
                    "point (%d, %d) outside unit square", p->x, p->y);
   }

实例化参数化测试
------------------------------------

:c:macro:`ZTEST_INSTANTIATE_TEST_SUITE_P` 将一个值集绑定到一个测试体。每次调用创建一个独立的命名实例；同一测试体可以使用不同的值集实例化多次：

.. code-block:: C

   ZTEST_INSTANTIATE_TEST_SUITE_P(small, my_suite, test_multiply, small_factors);
   ZTEST_INSTANTIATE_TEST_SUITE_P(big,   my_suite, test_multiply, big_factor_vals);

第一个参数（如示例中的 ``small`` / ``big``）是编译单元内任意唯一的标识符；它会被记录在测试元数据中，但不影响 Twister 报告的测试命名。

获取当前参数
----------------------------------

在 :c:macro:`ZTEST_P` 测试体内，可以使用以下辅助函数：

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 辅助函数
     - 描述
   * - ``ztest_has_current_param()``
     - 在参数化调用内部调用时返回 ``true``。
   * - ``ztest_get_current_param()``
     - 返回指向当前值的 ``const void *`` 指针。
   * - ``ZTEST_GET_PARAM_PTR(type)``
     - 返回指向当前值的 ``const type *`` 指针。
   * - ``ZTEST_GET_PARAM(type)``
     - 解引用并以 ``type`` 类型返回当前值。
   * - ``ztest_get_current_param_index()``
     - 返回当前值在其集合中的从零开始的索引。
   * - ``ztest_get_current_param_size()``
     - 返回一个参数元素的字节大小。

非参数化测试（:c:macro:`ZTEST`、:c:macro:`ZTEST_F`）总是看到 ``ztest_has_current_param()`` 返回 ``false``，``ztest_get_current_param()`` 返回 ``NULL``。

测试结果期望
========================

有些测试是被故意设计为会失败的。当测试由于代码本身的性质而预期失败或跳过时，可以将其标注为相应类型。例如：

.. code-block:: C

   #include <zephyr/ztest.h>

   ZTEST_SUITE(my_suite, NULL, NULL, NULL, NULL, NULL);

   ZTEST_EXPECT_FAIL(my_suite, test_fail);
   ZTEST(my_suite, test_fail)
   {
     /** This will fail the test */
     zassert_true(false, NULL);
   }

   ZTEST_EXPECT_SKIP(my_suite, test_skip);
   ZTEST(my_suite, test_skip)
   {
     /** This will skip the test */
     zassume_true(false, NULL);
   }

在这个示例中，上述测试应分别被标记为失败和跳过。相反，由于设置了期望，Ztest 会将两者都标记为通过。

测试规则
==========

测试规则是一种对每个测试和每个套件运行相同逻辑的方式。有很多场景你可能想为二进制文件中的每个测试重置某些状态（无论当前运行的是哪个套件）。例如，这可能是重置 mock、重置模拟器、刷新 UART 等：

.. code-block:: C

   #include <zephyr/fff.h>
   #include <zephyr/ztest.h>

   #include "test_mocks.h"

   DEFINE_FFF_GLOBALS;

   DEFINE_FAKE_VOID_FUN(my_weak_func);

   static void fff_reset_rule_before(const struct ztest_unit_test *test, void *fixture)
   {
        ARG_UNUSED(test);
        ARG_UNUSED(fixture);

        RESET_FAKE(my_weak_func);
   }

   ZTEST_RULE(fff_reset_rule, fff_reset_rule_before, NULL);

自定义 ``test_main``
=====================

虽然 Ztest 框架提供了默认的 :c:func:`test_main` 函数，但有些应用可能希望提供自定义行为。如果存在测试所依赖的某些全局状态，且该状态要么无法复制，要么不从头开始就难以复制，这种情况尤其如此。例如，这样一种状态可以是电源序列。假设有一块开发板，其上电序列包含多个步骤，就可以使用 ``predicate`` 控制运行时机来编写测试套件。在这种情况下，:c:func:`test_main` 函数可以如下编写：

.. code-block:: C

   #include <zephyr/ztest.h>

   #include "my_test.h"

   void test_main(void)
   {
        struct power_sequence_state state;

        /* Only suites that use a predicate checking for phase == PWR_PHASE_0 will run. */
        state.phase = PWR_PHASE_0;
        ztest_run_all(&state, false, 1, 1);

        /* Only suites that use a predicate checking for phase == PWR_PHASE_1 will run. */
        state.phase = PWR_PHASE_1;
        ztest_run_all(&state, false, 1, 1);

        /* Only suites that use a predicate checking for phase == PWR_PHASE_2 will run. */
        state.phase = PWR_PHASE_2;
        ztest_run_all(&state, false, 1, 1);

        /* Check that all the suites in this binary ran at least once. */
        ztest_verify_all_test_suites_ran();
   }

:c:func:`ztest_run_all` 的签名为 ``ztest_run_all(const void *state, bool shuffle, int suite_iter, int case_iter)``：

* ``state`` - 传递给每个套件 ``predicate`` 的全局状态指针。
* ``shuffle`` - 当为 ``true`` 时，随机化套件和测试的运行顺序（需要 :kconfig:option:`CONFIG_ZTEST_SHUFFLE`）；``false`` 保持默认的字母数字顺序。
* ``suite_iter`` - 每个测试套件重复执行的次数。
* ``case_iter`` - 每个测试用例重复执行的次数。

在上面的示例中，每次调用按顺序、不洗牌地运行匹配的套件一次。


声明测试套件的最佳实践
*******************************************

*twister* 和其他验证工具需要获取 Zephyr *ztest* 测试镜像将暴露的测试用例列表。

.. admonition:: 理由

   这一切的目的是可追溯性。仅有一个信号量测试应用是不够的。我们还必须证明对所有 API 和功能都有测试点，并能追溯到 API 文档和功能需求。

   其思路是，测试报告应显示每个测试用例的结果：通过、失败、被阻止或跳过。只报告高层测试应用，特别是当测试做了太多事情时，过于笼统。

其他问题：

- 为什么不先用 CPP 预扫描然后解析？或者事后扫描 ELF 文件？

  如果 C 预处理或构建因任何问题而失败，我们就无法识别子用例。

- 为什么不在 YAML 测试配置中声明它们？

  单独的测试用例描述文件比只把信息保留在测试源文件本身中更难维护——更改时只需更新一个文件，消除了重复。

压力测试框架
*********************

Zephyr 压力测试框架（Ztress）提供一个在多个优先级上下文中执行用户函数的环境。它可用于验证代码对抢占具有弹性。该框架跟踪每个上下文的执行次数和抢占次数。执行可以具有各种完成条件，例如超时、执行次数或抢占次数。

该框架通过创建所请求数量的线程（每个线程具有不同优先级）来搭建环境，并可选地启动一个定时器。对于每个上下文，调用一个用户函数（每个上下文各不相同），然后该上下文睡眠随机的系统 tick 数。该框架跟踪 CPU 负载并调整睡眠时长，以达到更高的 CPU 负载。为了提高抢占概率，系统时钟频率应相对较高。QEMU x86 上默认的 100 Hz 太低，建议将其提高到 100 kHz。

压力测试环境使用 :c:macro:`ZTRESS_EXECUTE` 搭建并执行，该宏接受可变数量的参数。每个参数是一个上下文，由 :c:macro:`ZTRESS_TIMER` 或 :c:macro:`ZTRESS_THREAD` 宏指定。上下文按优先级降序排列。每个上下文通过提供最小执行次数和抢占次数来指定完成条件。当所有条件满足且执行完成时，会打印执行报告，宏随即返回。注意，测试执行期间会定期打印进度报告。

可以通过指定测试超时（:c:func:`ztress_set_timeout`）或显式中止（:c:func:`ztress_abort`）来提前结束执行。

用户函数的参数包含一个执行计数器和一个指示是否为最后一次执行的标志。

下面的示例展示了如何搭建并运行 3 个上下文（其中之一是 k_timer 中断处理程序上下文）。完成标准设置为每个上下文至少执行 10000 次，最低优先级上下文被抢占 1000 次。此外，超时被配置为如果条件未满足，则在 10 秒后结束。每个上下文的最后一个参数是初始睡眠时间，它会在整个测试过程中被调整，以达到最高的 CPU 负载。

.. code-block:: C

   ztress_set_timeout(K_MSEC(10000));
   ZTRESS_EXECUTE(ZTRESS_TIMER(foo_0, user_data_0, 10000, Z_TIMEOUT_TICKS(20)),
                  ZTRESS_THREAD(foo_1, user_data_1, 10000, 0, Z_TIMEOUT_TICKS(20)),
                  ZTRESS_THREAD(foo_2, user_data_2, 10000, 1000, Z_TIMEOUT_TICKS(20)));

配置
=============

Ztress 的静态配置包含：

 - :kconfig:option:`CONFIG_ZTRESS_MAX_THREADS` - 支持的线程数量。
 - :kconfig:option:`CONFIG_ZTRESS_STACK_SIZE` - 所创建线程的栈大小。
 - :kconfig:option:`CONFIG_ZTRESS_REPORT_PROGRESS_MS` - 测试进度报告间隔。

API 参考
*************

运行测试
=============

.. doxygengroup:: ztest_test

断言
==========

这些宏会在相关断言失败时立即使测试失败。断言失败时，会打印当前文件、行号和函数，以及失败原因和可选消息。如果配置项 :kconfig:option:`CONFIG_ZTEST_ASSERT_VERBOSE` 为 0，断言只会打印文件和行号，从而减小测试的二进制文件体积。

``zassert_equal(buf->ref, 2, "Invalid refcount")`` 失败宏的示例输出（字符串字面量保留原文）：

.. code-block:: none

    Assertion failed at main.c:62: test_get_single_buffer: Invalid refcount (buf->ref not equal to 2)
    Aborted at unit test function

.. doxygengroup:: ztest_assert


期望
============

这些宏会在相关期望失败时继续测试执行，并在测试执行结束时使测试失败。期望失败时，会打印当前文件、行号和函数，以及失败原因和可选消息，但会继续执行测试。如果配置项 :kconfig:option:`CONFIG_ZTEST_ASSERT_VERBOSE` 为 0，期望只会打印文件和行号，从而减小测试的二进制文件体积。

例如，如果以下期望失败：

.. code-block:: C

   zexpect_equal(buf->ref, 2, "Invalid refcount");
   zexpect_equal(buf->ref, 1337, "Invalid refcount");

输出将类似于：

.. code-block:: none

   START - test_get_single_buffer
       Expectation failed at main.c:62: test_get_single_buffer: Invalid refcount (buf->ref not equal to 2)
       Expectation failed at main.c:63: test_get_single_buffer: Invalid refcount (buf->ref not equal to 1337)
    FAIL - test_get_single_buffer in 0.0 seconds

.. doxygengroup:: ztest_expect

假设
===========

这些宏会在相关假设失败时立即跳过测试或套件。假设失败时，会打印当前文件、行号和函数，以及失败原因和可选消息。如果配置项 :kconfig:option:`CONFIG_ZTEST_ASSERT_VERBOSE` 为 0，假设只会打印文件和行号，从而减小测试的二进制文件体积。

``zassume_equal(buf->ref, 2, "Invalid refcount")`` 失败宏的示例输出（字符串字面量保留原文）：

.. code-block:: none

    START - test_get_single_buffer
        Assumption failed at main.c:62: test_get_single_buffer: Invalid refcount (buf->ref not equal to 2)
     SKIP - test_get_single_buffer in 0.0 seconds

.. doxygengroup:: ztest_assume


Ztress
======

.. doxygengroup:: ztest_ztress


.. _mocking-fff:

通过 FFF 进行模拟
==================

Zephyr 已集成 FFF 用于模拟。有关文档请参见 `FFF`_。要使用它，请包含相关头文件：

.. code-block:: C

   #include <zephyr/fff.h>

Zephyr 提供了一些基于 FFF 的伪（fake）驱动，可用作桩或 mock。伪驱动实例通过 :ref:`devicetree` 和 :ref:`kconfig` 进行配置。有关更多信息，请参见以下设备树绑定：

.. zephyr-keep-sorted-start

* :dtcompatible:`zephyr,fake-can`
* :dtcompatible:`zephyr,fake-comp`
* :dtcompatible:`zephyr,fake-eeprom`
* :dtcompatible:`zephyr,fake-leds`
* :dtcompatible:`zephyr,fake-pwm`
* :dtcompatible:`zephyr,fake-regulator`
* :dtcompatible:`zephyr,fake-rtc`
* :dtcompatible:`zephyr,fake-stepper-ctrl`
* :dtcompatible:`zephyr,fake-stepper-driver`

.. zephyr-keep-sorted-stop

Zephyr 还为 FFF 定义了扩展，用于简化伪（fake）函数的声明。请参见 :ref:`FFF 扩展 <fff-extensions>`。

自定义测试输出
***********************
通过设置 :kconfig:option:`CONFIG_ZTEST_TC_UTIL_USER_OVERRIDE` 为 "y"，并添加一个包含你的覆盖项的 :file:`tc_util_user_override.h` 文件，即可启用自定义。

在你的项目 :file:`CMakeLists.txt` 中添加一行 ``zephyr_include_directories(my_folder)``，以便 Zephyr 在构建时找到你的头文件。

参见文件 :zephyr_file:`subsys/testsuite/include/zephyr/tc_util.h`，了解哪些宏和/或定义可以被覆盖。这些将被如下代码块包围：

.. code-block:: C

   #ifndef SOMETHING
   #define SOMETHING <default implementation>
   #endif /* SOMETHING */

.. _ztest_shuffle:

打乱测试顺序
***********************
默认情况下，测试按字母数字顺序排序并运行。测试用例可能依赖于该顺序。启用 :kconfig:option:`CONFIG_ZTEST_SHUFFLE` 以随机化顺序。测试输出会为失败的测试显示种子。对于本地模拟器构建，你可以通过 ``--seed`` 将种子作为参数提供给 twister。


重复测试
***********************
默认情况下，测试只执行一次。测试用例和测试套件可以执行多次。启用 :kconfig:option:`CONFIG_ZTEST_REPEAT` 以多次执行测试。默认乘法因子为 3，意味着每个测试套件执行 3 次，每个测试用例执行 3 次。这可以通过 :kconfig:option:`CONFIG_ZTEST_SUITE_REPEAT_COUNT` 和 :kconfig:option:`CONFIG_ZTEST_TEST_REPEAT_COUNT` Kconfig 选项更改。

测试选择
**************
对于为本地模拟器构建的测试，使用命令行参数来列出或选择要运行的测试。测试参数期望一个由 ``suite::test`` 组成的逗号分隔列表。你可以用 ``*`` 替代测试名，以运行套件内的所有测试。

例如

.. code-block:: bash

    $ zephyr.exe -list
    $ zephyr.exe -test="fixture_tests::test_fixture_pointer,framework_tests::test_assert_mem_equal"
    $ zephyr.exe -test="framework_tests::*"


.. _fff-extensions:

FFF 扩展
**************

.. doxygengroup:: fff_extensions


.. _FFF: https://github.com/meekrosoft/fff
