.. _code-documentation:

代码文档
###################

API 文档
******************

编写良好的 API 文档能提升开发者的体验，也是定义 API 成功与否的基本要求。Doxygen 是一种通用文档工具，Zephyr 项目用它来编写 API 文档。它生成在线文档浏览器（HTML 形式），和/或为其他工具提供输入，这些工具用于从有文档的源文件生成参考手册。特别是，Doxygen 的 XML 输出被用作生成 Zephyr 项目在线文档的输入。

需求引用
**************************

API 大部分文档描述的是需求的实现或所宣传的特性，并且可以追溯到这些特性。我们使用 API 文档作为将实现追溯到已记录特性的主要接口。这通过 Doxygen 原生的需求可追溯性命令（``@satisfies`` 和 ``@verifies``）完成，这些命令引用在需求目录（requirement catalogue）其他位置维护的需求。

测试文档
*******************

为了帮助理解每个测试做了什么、测试了哪些功能，我们还使用相同的工具和相同的上下文来记录所有测试代码，并为在同一环境中维护的所有单元测试和集成测试生成文档。测试通过引用其验证的 API 或功能来记录：创建指向 API 的链接，并添加对原始需求的引用。


文档指南
*************************

测试代码
=========

Zephyr 项目使用多种测试方法，最常见的是 :ref:`Ztest 框架 <test-framework>`。测试文档应只对入口测试函数（通常以 test\_ 为前缀）以及被 Ztest 框架直接调用的函数编写。这些测试会出现在测试报告中，使用它们的名称和标识符是识别它们并从需求追溯回它们的最佳方式。

测试文档不应干扰实际的 API 文档，需要遵循新的结构以避免混淆。使用一致的命名方案并遵循定义良好的结构，我们就能将这部分文档归入其独立的模块，并在解析测试数据用于可追溯性报告时唯一地识别它。以下是应遵循的若干指南：

- 所有测试代码文档应归入 ``all_tests`` Doxygen 组下
- 所有测试文档应位于以 tests\_ 为前缀的 Doxygen 组下

记录一个需求
=========================

一个需求用 Doxygen 的 ``@requirement`` 命令记录，该命令接受一个唯一标识符和一个可选标题。Doxygen 将所有需求收集到一个页面上，并允许通过标识符从任何地方引用它们。使用专门用于该需求的注释块，通常维护在需求目录中::

    /**
    * @requirement ZEPH-015 (Give a semaphore)
    *
    * The kernel shall provide a mechanism to give a semaphore, increasing its
    * count up to its configured maximum.
    */

这里使用的标识符（例如 ``ZEPH-015``）与下面 ``@satisfies`` 和 ``@verifies`` 命令所引用的相同，正是它将实现和测试链接回该需求。

Doxygen 的 ``@verifies`` 命令表示某个测试验证了一个需求::

    /**
    * @brief Tests for the Semaphore kernel object
    * @defgroup kernel_semaphore_tests Semaphore
    * @ingroup all_tests
    * @{
    */

    ...
    /**
    * @brief A brief description of the tests
    * Some details about the test
    * more details
    *
    * @verifies ZEPH-015
    */
    void test_sema_thread2thread(void)
    {
    ...
    }
    ...

    /**
    * @}
    */

要获得某个实现或某段代码如何满足一个需求的覆盖情况，我们使用 Doxygen 的 ``@satisfies`` 命令::

    /**
    * @brief Give a semaphore.
    *
    * This routine gives @a sem, unless the semaphore is already at its maximum
    * permitted count.
    *
    * @note Can be called by ISRs.
    *
    * @param sem Address of the semaphore.
    *
    * @satisfies ZEPH-015
    */
    __syscall void k_sem_give(struct k_sem *sem);



要生成矩阵，首先需要构建文档，特别是需要构建 Doxygen 的 XML 输出::

   $ make doxygen

解析 Doxygen 生成的 XML 数据以生成可追溯性矩阵。
