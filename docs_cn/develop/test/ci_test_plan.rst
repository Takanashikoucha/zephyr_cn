.. _ci_test_plan:

CI 测试计划选择器（test_plan_v2）
#####################################

CI 测试计划选择器是一个模块化的 Python 脚本，位于 ``scripts/ci/test_plan_v2.py``。它的目的是分析 Pull Request 中更改的文件集，并生成一个定向的 twister 测试计划——只运行可能受该更改影响的测试，同时避免在每次提交时都进行全树范围运行。

该脚本会写出两个产物：

* ``testplan.json`` —— 通过 ``twister --load-tests`` 传递给 twister。
* ``.testplan`` —— 一个纯 ``KEY=value`` 格式的环境文件，供 CI 编排脚本消费，其中包含 ``TWISTER_TESTS``、``TWISTER_NODES`` 和 ``TWISTER_FULL``。

架构
************

选择器围绕一条*策略管道*构建。每个策略都是一个独立的分析器，它会：

1. 接收更改文件列表（或尚未被前面策略消费的子集）。
2. 按照自身逻辑检查这些文件。
3. 返回 :class:`TwisterCall` 描述符列表，以及它*已处理*的文件集合。

:class:`Orchestrator` 驱动该管道，将所有结果合并到 :class:`PlanAccumulator` 中，对测试套件去重，并写出输出文件。

策略顺序
*****************

策略按固定顺序运行，体现了两个原则：

**特定性优先于通用性。**
最精确的策略最先运行。位于 ``tests/kernel/sched/`` 中的文件会先由 :class:`DirectTestStrategy` 确定性地处理（精确运行那些测试），然后兜底的 :class:`MaintainerAreaStrategy` 才可能添加整个 Kernel 区域的扫描。

**先消费后追加。**
消费型策略先于追加型策略运行。一旦某个消费型策略认领了一个文件，下游策略就永远看不到它。这防止了对某个板文件的更改同时触发驱动兼容性扫描和针对同一路径的 Kconfig 扫描。

当前顺序如下：

.. list-table::
   :header-rows: 1
   :widths: 5 20 10 65

   * - #
     - 策略
     - 是否消费
     - 理由
   * - 0
     - :class:`ComplexityStrategy`
     - 否
     - 使用 pydriller 和 lizard 对补丁集评分。必须最先运行，以便评分可供 :class:`RiskClassifierStrategy` 使用。不发出任何 twister 调用。
   * - 1
     - :class:`IgnoreStrategy`
     - 是
     - 静默丢弃永远不可能影响测试的文件（文档、CI 工作流、工具）。尽早运行，以便后续策略不会在被忽略的路径上浪费精力。
   * - 1b
     - :class:`BoilerplateFilter`
     - 是
     - 消费整个 diff 仅由空白调整、空行变更、SPDX 许可证标识符、版权声明或裸注释定界符组成的文件。此类更改不可能影响运行时行为，因此尽早移除它们可以为实质性策略保持干净的候选池。需要一个 git 提交范围；否则不执行任何操作。
   * - 2
     - :class:`DirectTestStrategy`
     - 是
     - 更改的测试或示例文件必须*只*触发该测试，而不是整个区域范围的扫描。消费该文件可防止 :class:`MaintainerAreaStrategy` 在 ``tests/kernel/sched/main.c`` 被修改时也添加 Kernel 区域中的所有测试。
   * - 3
     - :class:`SnippetStrategy`
     - 是
     - 片段（snippet）更改是自包含的：只有那些在 ``required_snippets`` 中声明了该片段的测试才需要运行。消费可防止下游策略把片段 YAML 当作未知配置文件处理。
   * - 4
     - :class:`BoardStrategy`
     - 是
     - 板相关的更改需要在每个板变体上运行定向集成测试。消费可防止某个板的 ``.yaml`` 文件同时匹配 Kconfig 策略和 Header 策略。
   * - 5
     - :class:`SoCStrategy`
     - 是
     - SoC 级别的更改会影响基于该 SoC 家族构建的所有板。消费可防止同一路径的 ``soc/`` 进入 Kconfig 扫描。
   * - 6
     - :class:`ManifestStrategy`
     - 是
     - 更改的 ``west.yml`` 需要带模块标记的集成测试，而不是通用的维护者区域运行。消费清单文件可防止兜底策略添加不相关的测试。
   * - 7
     - :class:`DriverCompatStrategy`
     - 否
     - 追加型：驱动文件可能同时被区域模式覆盖，因此不消费该文件，:class:`KconfigImpactStrategy` 和 :class:`MaintainerAreaStrategy` 可以进一步补充覆盖。
   * - 8
     - :class:`DtsBindingStrategy`
     - 否
     - 追加型：绑定（binding）更改将基于 overlay 的测试选择与针对特定板的区域调用组合起来。
   * - 9
     - :class:`KconfigImpactStrategy`
     - 否
     - 追加型：Kconfig 更改可能影响许多不相关的文件；只有找到非广泛符号时才消费，把广泛符号对应的文件留给兜底策略。
   * - 10
     - :class:`HeaderImpactStrategy`
     - 否
     - 追加型：头文件更改会追溯 include 使用方回到维护者区域。被包含次数超过配置阈值的广泛头文件会被跳过。
   * - 11
     - :class:`MaintainerAreaStrategy`
     - 否
     - 兜底：将任何剩余文件与 ``MAINTAINERS.yml`` 的区域模式匹配，并为每个 ``tests:`` 列表非空的匹配区域发出 ``--test-pattern`` 调用。

样板过滤器
******************

:class:`BoilerplateFilter` 紧跟在 :class:`IgnoreStrategy` 之后、在任何测试选择策略之前运行。它检查每个更改文件的实际 diff（通过 ``git diff``），并消费那些整个内容变更都不具实质性的文件：

* **空白和空行变更** —— 通过 ``git diff -w --ignore-blank-lines`` 检测：如果该命令对某个文件没有产生任何输出，则说明该文件的每一处更改行都是空白或空行。

* **SPDX 和版权头编辑** —— 以 ``SPDX-License-Identifier:``、``SPDX-FileCopyrightText:`` 或单词 ``Copyright`` 开头的行。

* **仅注释定界符的行** —— 非空白内容完全由 ``/*``、``*/``、``//``、``#`` 或 ``*`` 字符组成的行（例如重新排版后的块注释边框）。

只有当 diff 中**所有**新增或删除的行都落入上述某一类时，该文件才会被消费。哪怕只有一行实质性变更（一条改动的语句、宏或声明），该文件就会原样传递给下游策略。

在未提供 ``--commits`` 时（例如使用 ``--modified-files`` 时），该过滤器不执行任何操作，因为没有提交范围就无法计算 diff。在这种情况下所有文件都保留在候选池中。

消费与追加行为
*******************************

每个策略子类都带有一个类属性 ``consumes: bool``。

当 ``consumes = True`` 时：
  在*已处理*集合中返回的文件会在下一个策略运行之前从 ``remaining`` 候选池中移除。当该策略对其文件类型是*权威*（authoritative）时使用——即如果在后续策略中再次看到该文件会产生冗余或错误结果时。

当 ``consumes = False``（默认值）时：
  无论策略返回什么，文件都保留在候选池中。所有下游策略接收相同的文件列表。对贡献*额外*测试覆盖、但不声明独占所有权的追加型策略使用。

.. note::

   当 ``remaining`` 候选池为空时，:class:`Orchestrator` 会完全跳过策略。由于非消费型策略会看到所有文件，"remaining" 只会通过消费型策略而缩小。一旦候选池为空，编排器就停止调用策略。

全量运行与回退条件
**********************************

当以下任一条件成立时，编排器会在 ``.testplan`` 中置 ``TWISTER_FULL=True``：

1. **未解决的文件。** 所有策略运行完毕后，至少有一个更改文件未被任何策略*处理*。与其静默跳过对未知路径的覆盖，不如回退到请求一次全量运行，以免有回归溜过去。

2. **显式的全量运行信号。** 某个策略返回了一个带 ``full_run=True`` 的 :class:`TwisterCall`。当编排器遇到这样的调用时，会立即置 ``TWISTER_FULL=True``、清空剩余候选池，并停止执行后续调用。该机制允许策略退出定向选择（例如当被整棵代码树使用的核心子系统头文件被修改时）。

当 ``TWISTER_FULL=True`` 时，CI 脚本预期会丢弃 ``testplan.json``，并在不带 ``--load-tests`` 的情况下运行 twister。

节点数计算
**********************

``.testplan`` 中的 ``TWISTER_NODES`` 按如下方式计算：

* ``0`` —— 未选择任何测试。
* ``1`` —— 所选测试数少于 ``--tests-per-builder``（可容纳在一个 builder 中）。
* ``ceil(total / tests_per_builder)`` —— 其余情况。向上取整确保在除法不能整除时没有任何 builder 超容量。

``--tests-per-builder`` 的默认值为 ``900``。

添加新策略
*********************

1. **子类化** :class:`SelectionStrategy`，并实现两个抽象成员：

   .. code-block:: python

      class MyStrategy(SelectionStrategy):

          consumes: bool = False  # 如果是权威策略则为 True

          @property
          def name(self):
              return "MyStrategy"

          def analyze(self, changed_files):
              # 检查 changed_files
              calls = [...]       # TwisterCall 列表
              handled = {...}     # 该策略负责的 changed_files 子集
              return calls, handled

2. **决定消费还是追加。** 问自己："如果下游策略也看到这个文件，它会产生有用的额外覆盖，还是冗余/错误的结果？" 如果是冗余/错误：``consumes = True``。

3. **在 :func:`build_strategies` 中的正确位置插入。** 经验法则：

   * 消费型策略应位于所有追加型策略之前。
   * 更特定的策略应位于较不特定的策略之前。
   * 对文件候选池没有副作用的策略（追加型）可以按成本排序——最便宜的放前面。

4. **用延迟导入保护可选依赖**：在 ``analyze`` 内部延迟导入，并在依赖缺失时优雅地返回 ``[], set()``。使用 ``# noqa: PLC0415`` 注释来消除延迟导入警告。

5. **在 ``scripts/tests/ci/test_test_plan_v2.py`` 中编写单元测试**，覆盖：

   * 正常路径（文件被正确识别并路由）。
   * 无操作路径（不相关文件不产生任何调用，也没有已处理集合）。
   * 边界情况（磁盘上缺少文件、格式错误的 YAML、空输入）。

共享管道上下文
***********************

:class:`PipelineContext` 是一个 dataclass，通过 :func:`build_strategies` 贯穿所有策略。它当前携带：

* ``complexity_score`` —— 由 :class:`ComplexityStrategy` 写入、由 :class:`RiskClassifierStrategy` 读取的补丁集综合评分。
* ``file_metrics`` —— 逐文件的 :class:`ComplexityMetrics` 映射，用于详细日志记录和下游决策。

新的跨策略状态应作为 :class:`PipelineContext` 上的带类型字段添加，而不是作为策略级的实例变量。

用于验证选择行为的测试策略
*************************************************

测试套件位于 ``scripts/tests/ci/test_test_plan_v2.py``，用 pytest 运行：

.. code-block:: bash

   pytest scripts/tests/ci/test_test_plan_v2.py -v

测试按每个策略或共享组件一个类来组织。每个新策略预期包含以下类别的测试：

**单元测试（不需要 Zephyr 代码树）**
  使用 ``tmp_path`` fixture 创建运行每个代码路径所需的最小文件系统结构（``board.yml``、``snippet.yml``、``testcase.yaml`` 等）。这些测试应当快速且封闭（hermetic）。

**辅助方法测试**
  隔离测试内部方法（路径遍历、YAML 解析、正则提取）。传入合成的内容，而不是依赖仓库中的真实文件。

**编排器集成测试**
  使用 mock 策略和 mock :class:`TwisterExecutor` 来测试编排器的消费-追加逻辑、全量运行信号以及 ``.testplan`` 输出，而不调用 twister。

**真实代码树集成测试**（可选，``@pytest.mark.integration``）
  可以添加并标记 ``@pytest.mark.integration``，从而从默认运行中排除。这些测试只有在完整的 Zephyr 检出中才有意义。

新策略的最小测试清单
==========================================

* 当输入列表中没有相关文件时，策略不返回任何调用，也不返回任何已处理文件。
* 对于已知的良好输入，策略能正确识别并返回预期的 :class:`TwisterCall`。
* 当文件系统中缺少必需文件时，策略不会崩溃。
* 对消费型策略：已处理集合恰好等于匹配到的文件，不含其他。
* 对追加型策略：已处理集合为空，或仅等于该策略作为权威的文件。

CLI 参考
*************

.. code-block:: text

   usage: test_plan_v2.py [-c A..B] [-m FILE] [-f PATH]
                          [-o FILE] [-p PLATFORM] [--maintainers-file FILE]
                          [-T DIR] [--quarantine-list FILE]
                          [--tests-per-builder N] [--disable-strategy NAME]
                          [--detailed-test-id]

   -c A..B              Git 提交范围（例如 ``main..HEAD``）。更改文件
                        由 ``git diff --name-only A..B`` 导出。
   -m FILE              包含更改文件路径列表的 JSON 文件。
   -f PATH              将 PATH 视为一个更改文件（可重复）。
   -o FILE              输出 JSON 文件（默认：``testplan.json``）。
   -p PLATFORM          将所有选择限制到该平台（可重复）。
   --maintainers-file   ``MAINTAINERS.yml`` 的路径。
   -T DIR               转发给每个 twister 调用的额外测试套件根目录。
   --quarantine-list    转发给 twister 的隔离 YAML。
   --tests-per-builder  每个 CI builder 节点的测试数（默认：900）。
   --disable-strategy   按名称跳过某个策略（可重复）。
   --detailed-test-id   向 twister 传递 ``--detailed-test-id``。
