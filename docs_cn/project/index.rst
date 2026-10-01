.. _development_model:

项目与治理
#######################


.. toctree::
   :maxdepth: 1

   tsc
   project_roles
   working_groups
   release_process
   proposals
   code_flow
   dev_env_and_tools
   issues
   communication
   documentation



Zephyr 项目定义了一个开发流程工作流：使用 GitHub **Issues** 跟踪特性、增强和错误报告，并使用 GitHub **Pull Requests**（PR）提交和审查更改。Zephyr 社区成员协同工作，审查这些 Issue 和 PR，通过定期发布来管理 Zephyr 的特性增强和质量改进，如 :ref:`release_process` 所述。

我们只能通过要求社区和贡献者对初始提交以及后续问题和澄清提供及时的审查、反馈和响应，来管理 Issue 和 PR 的数量。请阅读项目的 :ref:`开发流程与工具 <dev-environment-and-tools>` 以及 :ref:`审查时间表 <review_time>` 的细节，以了解我们活跃开发者社区的项目目标和指南。

:ref:`project_roles` 详细描述了 Zephyr 项目角色，以及与开发流程工作流相关的相应权限。


术语
***********

- mainline（主线）：核心功能和核心特性正在开发的主代码树。
- 子系统/特性分支：同一仓库内的一个分支。在我们的情况下，当引用不在同一仓库、但共享相同历史的仓库副本的分支时，也会使用"分支"一词。
- upstream（上游）：源代码所基于的父分支。这是你从中拉取（pull）并向其推送（push）的分支，基本上就是你的上游。
- LTS：长期支持（Long Term Support）
