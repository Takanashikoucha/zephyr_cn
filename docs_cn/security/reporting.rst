.. _reporting:

安全漏洞报告
################################

简介
============

Zephyr 项目中的漏洞应优先通过在 Zephyr 仓库的
`安全通告页面`_ 上创建草稿 `安全通告`_ 来报告。
或者，可通过电子邮件 vulnerabilities@zephyrproject.org
向项目安全事件响应团队提交报告。
这些报告将在 1 周内由安全响应团队确认并分析。

所有漏洞都通过 Zephyr 项目在 GitHub 上的
`安全通告页面`_ 进行跟踪和管理，原始提交者将被授予
查看其所报告问题的权限。

.. _security advisory: https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability#privately-reporting-a-security-vulnerability
.. _security advisories page: https://github.com/zephyrproject-rtos/zephyr/security/advisories

漏洞报告指南
==================================

安全研究和漏洞报告是对 Zephyr 项目的宝贵贡献。
为使该过程对所有人安全且高效，所有报告和相关活动
都必须遵守 Zephyr 项目`行为准则`_。

以下指南描述了在研究和报告 Zephyr 安全漏洞时的期望。

.. _Code of Conduct: https://github.com/zephyrproject-rtos/zephyr/blob/main/CODE_OF_CONDUCT.md

报告期望
----------------------

为帮助安全响应团队高效地分诊和解决问题，报告应：

- 描述受影响的组件、版本、板卡或平台，
  以及重现问题所需的配置。

- 包含清晰的逐步重现说明，尽可能附上最小概念验证。

- 解释安全影响（例如，机密性、完整性或可用性损失）
  以及任何已知缓解措施。

- 避免包含破坏性载荷或可能在报告被意外披露时
  对用户或系统造成伤害的组件。

期望报告者本着善意努力，在任何公开披露之前，
给予项目合理的机会调查和修复问题，
与以下章节所述的禁运和披露流程一致。

安全问题管理
=========================

该 bug 跟踪系统中的问题将根据此图过渡到
若干状态：

.. graphviz::

   digraph {
      node [style = rounded];
      init [shape = point];
      New [shape = box];
      Triage [shape = box];
      {
        rank = same;
        rankdir = LR;
        Assigned [shape = box];
        Rejected [shape = box];
      }
      Review [shape = box];
      Accepted [shape = box];
      Public [shape = box];

      init -> New;
      New -> Triage;
      Triage -> Rejected [dir = both];
      Triage -> Assigned;
      Assigned -> Review [dir = both];
      Review -> Accepted;
      Review -> Rejected;
      Accepted -> Public;

   }

- New（新建）：该状态代表由报告者直接输入的新报告。
  当由响应团队响应电子邮件输入时，
  问题应直接过渡到 Triage 状态。

- Triage（分诊）：该问题正在等待响应团队分诊。
  响应团队将分析问题、确定责任实体、
  将其分配给该个人，并将问题
  移到 Assigned 状态。分诊的一部分是设置
  问题的优先级。

- Assigned（已分配）：问题已分配，正在等待
  被分配者修复。

- Review（评审）：一旦有针对该问题的 Zephyr 拉取请求，
  PR 链接将被添加到问题中的评论，
  问题移到 Review 状态。

- Accepted（已接受）：表示该问题已合并到
  Zephyr 中的相应分支。

- Public（公开）：禁运期已结束。
  问题将被公开可见，关联的 CVE 被更新，
  文档中的漏洞页面被更新以包含详细信息。

创建的安全通告保持私有，
由于安全报告的敏感性。问题仅对
特定方可见：

- PSIRT 邮件列表成员

- 报告者

- 其他方，由 Zephyr 安全
  小组委员会提议并批准。一般情况下，这将包括：

  - 负责修复的代码所有者。

  - 受该漏洞影响的
    相关发布的 Zephyr 发布负责人。

Zephyr 安全小组委员会应在任何有超过三人出席的
会议上审查所报告的漏洞。在审查期间，
他们应确定是否需要对新问题进行禁运。

禁运指南将基于：1. 问题的严重程度，
以及 2. 问题的可利用性。小组委员会
决定不需要禁运的问题将在常规
Zephyr 项目 bug 跟踪系统中重现。

.. _vulnerability_timeline:

安全敏感漏洞应在至多 90 天的禁运期后
公开。其意图是允许在 Zephyr 项目内 30 天
修复问题，以及 60 天供使用 Zephyr 构建产品的外部
方应用和分发这些修复。

.. _vulnerability_fix_recommendations:

对代码的修复应通过 Zephyr 项目 github 中的拉取请求 PR 进行。
开发者应尝试不透露所修复内容的敏感性质，
且不应引用已分配给该问题的 CVE 编号。
开发者应仅描述所修复的内容。

安全小组委员会将维护将禁运 CVE 映射到
这些 PR 的信息（该信息在 Github 安全
通告内），并定期生成安全问题状态报告。

每个被视为安全漏洞的问题都应
分配一个 CVE 编号。随着修复的创建，
可能需要分配额外的 CVE 编号，
或退役已分配的编号。

漏洞通知
==========================

每个 Zephyr 发布都应包含该发布中修复的 CVE 报告。
由于这些漏洞的敏感性，发布应仅包含
已修复 CVE 的列表。禁运期后，
漏洞页面应更新以包含这些漏洞的额外细节。
漏洞页面应对报告者给予署名，
除非报告者特别要求匿名。

Zephyr 项目应维护一个 vulnerability-alerts 邮件列表。
该列表初始将包含来自每个项目成员的联系人。
其他方可通过填写 `漏洞登记`_ 处的表单
请求加入该列表。这些方将由项目总监审核，
以确定他们在禁运期间了解安全漏洞有
合法利益。

.. _Vulnerability Registry: https://www.zephyrproject.org/vulnerability-registry/

定期地，安全小组委员会将向该邮件列表发送信息，
描述已知禁运问题及其在项目内的
回溯状态。该信息旨在使他们能够确定
是否需要将这些变更回溯到任何内部树。

当问题已分诊后，该列表将获知：

- Zephyr 项目安全通告链接（GitHub）。

- 分配的 CVE 编号。

- 涉及的子系统。

- 问题的严重程度。

在接受修复该问题的 PR（合并）后，
除上述外，该列表还将获知：

- CVE 编号与修复它的 PR 之间的关联。

- Zephyr 项目内的回溯计划。

安全漏洞回溯
=======================================

zephyr 内修复的每个安全问题都应回溯到
以下发布：

- 当前长期稳定（LTS）发布。

- 最近两个发布。

修复的开发者应负责任何必要的
回溯，并将其应用到上述任何发布分支，
除非修复不适用（漏洞是在
该发布制作后引入的）。所有
:ref:`漏洞修复 <vulnerability_fix_recommendations>` 建议
都适用于回溯拉取请求（及关联问题）。此外，
建议开发者私下通知负责的
发布经理，该回溯拉取请求和问题
正在处理一个漏洞。

回溯将在安全通告上跟踪。

需要知道
============

由于安全漏洞的敏感性，
仅与有需要知道的方分享细节和修复
很重要。以下方在禁运期结束前
需要知道安全漏洞的细节：

- 维护者仅在其领域区域内
  访问所有信息。

- 当前发布负责人，以及受该漏洞影响的
  历史发布的发布负责人（见上文回溯）。

- 项目安全事件响应（PSIRT）团队将
  完全访问信息。PSIRT 由
  白金成员的代表，以及从事来自其他
  成员分诊工作的志愿者组成。

- 根据需要，发布负责人和维护者可被邀请
  参加额外的安全会议以讨论漏洞。
