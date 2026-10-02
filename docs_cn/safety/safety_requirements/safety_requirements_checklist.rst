.. _safety_requirements_checklist:

安全需求检查清单
#############################

引言
************

所创建、修改或更新的需求必须适格。这意味着它们必须无歧义、可唯一识别、可行、可验证等。
为确保这一点，每个需求都需要在其拉取请求（pull request）中接受审查，以确认其是否满足成为一条需求的基本要求。
本清单将作为审查需求 PR 时必须考虑的最低标准。

需求结构与指南
*************************************

Zephyr 项目所采用的方法可参见 :ref:`safety_requirements`

审查说明
*******************

本清单列出了在审查中批准需求时应考虑的主题和问题。
审查结果必须以明确表明已使用本清单、以及审查中关于未决问题、发现或批准情况之实际结果的方式，记录在 PR 审查中。
在安全范围（safety scope）发布之前，本清单至少应对其范围内的新增或变更需求应用一次。


需求汇集于单独的仓库：
`Requirement repository
<https://github.com/zephyrproject-rtos/reqmgmt>`__

审查可以在两个层面进行——针对单个需求或针对一组需求。检查点如下：

针对每条需求的审查检查点
*************************************************

每个新增或变更的需求都需要被分析，以确保其适格，并识别其是否以任何方式影响 Zephyr 的安全性。

.. list-table:: 需求审查检查点
   :widths: 20 80 80 120
   :header-rows: 1

   * - ID
     - 问题
     - 说明
     - 示例

   * - VerReq_1_0
     - 该需求是否清晰易懂且无歧义？
     - 为确保需求可被分析，它必须易于理解且不留下（功能上的）解释空间。
     - 避免使用诸如 **some、sufficient、typical、many、several、few、...** 等模糊表述。
       类似 **The Zephyr Kernel should provide functionality xyz where possible（Zephyr 内核应在可能的情况下提供 xyz 功能）** 的表述不够精确，
       留有解释空间。此外，**should** 必须替换为无歧义的 **shall**，**where possible** 必须替换为需求作者希望该功能被提供的具体定义。
       这可以是一个用例列表、系统状态或其他条件，只要它们被明确定义即可。

   * - VerReq_1_1
     - 该需求是否具有原子性？
     - 需求真正只能描述一件需要满足的事情。否则，诸如安全分析、
       与架构组件及实现的唯一关联、可验证性等方面都会受到影响。
     - 类似 **The signal a shall switch on and off the yellow LED and the error state shall be indicated by switching on the red LED（信号 a 应点亮并熄灭黄色 LED，错误状态应通过点亮红色 LED 来指示）**
       的表述不是原子的。这应拆分为两条需求——**REQ1: 信号 a 应点亮并熄灭黄色 LED。** 以及 **REQ2: 错误状态应通过点亮红色 LED 来指示。**
       这还可以补充一条 **REQ3（变体 a）: 黄色 LED 与红色错误 LED 必须相互独立** 或
       **REQ3（变体 b）: 黄色 LED 与红色错误 LED 在 TBD 情况下可以合并**。

   * - VerReq_1_2
     - 该需求内部是否一致？
     - 需求本身必须在其内部完全一致。
     - 类似 **The system shall use a preemtpive RTOS to guarantee deterministic task scheduling.
       The system also need to ensure that all tasks, including low-priority background logging tasks, complete without preemption to preserve data integrity.（系统应使用抢占式 RTOS 来保证确定性的任务调度。
       系统还必须确保所有任务（包括低优先级后台日志任务）能够不被抢占地完成，以维护数据完整性。）** 的表述是相互矛盾的。
       必须避免此类情况。如果两种选项都应可用，则必须定义这些选项的条件以及如何配置这些选项。

   * - VerReq_1_3
     - 该需求是否可行、可实现且可验证？
     - 需求不是幻想愿望清单，它们必须能够以合理的方式达成（当然，什么是合理在不同项目之间可能有所不同）。
       因此，这通常意味着某件事在纸面上听起来不错，但技术上不可行、内部自相矛盾，或违反了系统的基本约束。
       这里所说的可验证，是指必须能够通过测试、（代码）审查、分析或其他手段来验证该需求已被满足。
     - 一个反例例如 **The RTOS shall guarantee zero‑latency interrupt handling for all devices under all conditions.（RTOS 应在所有条件下为所有设备保证零延迟的中断处理。）**，
       这在物理上是不可能的，因为没有任何硬件能够在字面意义上的零时间内作出响应。
       更好的做法是给出更具体的表述，例如
       **The RTOS shall guarantee an interrupt latency of ≤ 5 µs on the target HW architecture at 80 MHz under maximum system load.（RTOS 应在目标硬件架构上、80 MHz 频率下、最大系统负载时，保证中断延迟 ≤ 5 µs。）**

   * - VerReq_1_4
     - 该需求是否完整？
     - 为清晰表述需求意图所需的全部信息是否都已具备？
     - 表述必须要么清晰地列出所有所需的数据和信息，要么给出可找到这些数据之可靠引用。
       这意味着被引用的数据来源必须处于需求作者或利益相关方的控制之下，
       可能随时间变化的引用（例如指向外部来源的互联网 URL）是不合适的。

   * - VerReq_1_5
     - 该需求的定义是否完全不含实现细节？
     - 需求必须描述某件事"做什么"，而不是"怎么做"。存在一些边界情况，需求有意限制实现变体，
       通常出于某些设计原因，这些原因必须在需求的 rationale（理由）或注释（无论使用哪种形式）中说明。
     - 避免类似 **The RTOS shall use a priority-based preemptive scheduler implemented with a round-robin algorithm for tasks of equal priority（RTOS 应使用基于优先级的抢占式调度器，对同等优先级任务采用轮转（round-robin）算法实现）** 的表述，
       而应聚焦于功能需求
       **The RTOS shall support task scheduling that ensures higher-priority tasks can preempt lower-priority tasks, and tasks of equal priority are scheduled in a manner that prevents starvation.（RTOS 应支持任务调度，确保高优先级任务可抢占低优先级任务，同等优先级任务以不致饥饿的方式被调度。）**

   * - VerReq_1_6
     - 需求的安全（/安全）关键性是否已定义？
     - 所有影响可能损害 Zephyr 安全（或信息安全）完整性的功能的需求，都必须被标记为安全（/信息安全）关键，以便得到相应处理。
     - 目前尚未定义标记某功能为安全或信息安全相关的特定方式，需求或功能的相关性基于其定义的范围。

   * - VerReq_1_7
     - 每条需求是否都定义了验证和/或验收准则？
     - 每条需求都必须可验证。如果你无法为需求定义验收准则，则该需求需要重新考虑并可能以不同方式重新定义。
       验收准则至少必须能从需求的措辞中推导出来。
     - 确保已有可用测试，或已计划创建测试。评估测试覆盖对该需求是否充分。
       如果不充分，请联系安全工作组（Safety Working Group）或测试工作组（Testing Working Group）来解决。

   * - VerReq_1_8
     - 本需求中使用的所有术语对目标受众是否清晰？
     - 这同时针对需求的精确性和可理解性。必须明确本需求中使用的术语指的是什么。对项目有特殊含义的术语
       必须在术语表或随需求一起明确定义。
     - 表述 **The RTOS shall support IPC mechanisms such as mailboxes and semaphores for task synchronization（RTOS 应支持用于任务同步的 IPC 机制，如邮箱和信号量）** 可能存在问题，
       因为受众（测试人员、管理人员、PO 等）可能不熟悉 IPC，甚至不了解在 RTOS 语境下 mailbox 或 semaphore 指什么。
       如果没有向所有利益相关方解释这些术语的术语表，考虑将该需求改写为更类似于
       **The RTOS shall provide mechanisms that allow tasks to exchange data and coordinate their execution, such as message-passing and signaling features.（RTOS 应提供让任务交换数据并协调其执行的机制，例如消息传递和信号功能。）**

针对一组需求的审查检查点
*****************************************************

.. list-table:: 需求审查检查点
   :widths: 20 80 80 120
   :header-rows: 0

   * - ID
     - 问题
     - 说明
     - 示例

   * - VerReq_2_0
     - 需求是否被适当分组和结构化？
     - 通常合适的组织结构遵循层级顺序，在层级内部需求按
       例如功能、关键性、父需求来源等维度分组。
     - 分组不当的需求例如位于错误的章节，或位于错误的层级
       （例如需求定义的是内核组件的特定属性，因此必须位于软件组件层级，却被放在了系统需求中），
       章节也可能过载，需要在子章节中进一步结构化。

   * - VerReq_2_1
     - 每条需求外部是否一致？
     - 需求之间不得相互冲突或矛盾。
     - 假设有两条需求：**Requirement A: RTOS 应支持最多 10 个并发任务。Requirement B: RTOS 应为高性能应用支持多达 20 个并发任务。** -
       这两条需求显然相互矛盾，但对各自撰写它们的人来说可能都是正确的。通常这类需求需要需求作者之间进行沟通，
       可能的解决方案如下：**RTOS 应支持多达 20 个并发任务，标准应用的默认配置为 10 个任务。**

   * - VerReq_2_2
     - 每条需求是否可适当地追溯？
     - 每条需求都需要有清晰的来源（它从何而来、为什么在这里……）、关联的验证和/或验收准则，以及下级需求或架构元素。
     - 除最高层级需求外，每条需求都必须关联一个父需求，但仍需在 Requirement rationale（理由）、note 或注释中给出解释。

   * - VerReq_2_3
     - 该需求是否唯一？
     - 需求不得重复。如果你需要在多处澄清同一需求，请确保其中一条是"主需求"，其余只是关联信息。
     - 这一点不言自明，必须避免两条相同或相似的需求。
