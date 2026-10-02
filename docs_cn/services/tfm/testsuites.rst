Test Suites
###########

TF-M 包含两组测试套件：

* tf-m-tests - 标准 TF-M 专属回归测试
* psa-arch-tests - 针对特定 PSA API（安全存储等）的测试套件

这些测试套件可以通过 samples/tfm_integration 文件夹中相应的示例应用从 Zephyr 运行。

TF-M Regression Tests
*********************

回归测试套件可以通过 :zephyr_file:`tests/modules/tf-m/regression` 测试运行。

它通过 PSA API 测试 NS/S 边界之间各种服务和通信机制。它们为 NS RTOS（本例中为 Zephyr）与安全应用（TF-M）之间的正确集成提供了有用的健全性检查。

PSA Arch Tests
**************

PSA Arch Test 套件（可通过 :ref:`tfm_psa_test` 获取）包含多个测试套件，可用于验证安全应用是否遵循 PSA API 规范，TF-M 即是平台安全架构（PSA）的一个实现。

这些套件一次只能运行一个，可用的测试套件通过 ``CONFIG_TFM_PSA_TEST_*`` KConfig 标志描述：

Purpose
*******

这些测试套件的输出是获取你的特定板级、RTOS（此处为 Zephyr）和 PSA 实现（此处为 TF-M）的 PSA 认证所必需的。

它们还为对 TF-M 做出有意义变更的任何 PR（例如启用新的 TF-M 板级目标，或对核心 TF-M 模块进行修改）提供了有用的测试用例。在发布新板级支持等的新 PR 之前，通常应将其作为一致性检查运行。
