.. _secure code:

安全编码
#############

传统上，基于微控制器的系统并未过分强调安全。它们通常被认为彼此孤立、与外界隔离，并且由于访问难度较高而不太容易被利用。物联网改变了这一现状。如今，运行在小型微控制器上的代码通常可以访问互联网，或至少可以访问其他设备（这些设备本身也可能存在漏洞）。鉴于这些设备通常的部署规模，不受控制的访问可能造成灾难性后果 [#attackf]_。

本文档描述在 Zephyr 项目中确保安全得到处理所需满足的要求和流程。所有提交的代码都应遵守这些原则。

本文档的很大一部分内容来自 [CIIBPB]_。

简介与范围
**********************

本文档从安全视角出发，涵盖 `Zephyr Project`_ 的指南。其中许多想法来自其他开源项目。

.. todo: Reference main document here

.. _Zephyr Project: https://www.zephyrproject.org/

本文首先概述安全设计与 Zephyr 的关系，随后介绍 `Secure development knowledge`_ 一节，说明参与项目开发的人员需要具备的基本能力。本节还会引用其他安全文档；如何编写安全软件的完整细节超出本文档范围。本节同时说明至少一位主要开发者应具备的漏洞知识。这些知识对于下文描述的评审流程是必要的。

随后，本文描述将变更纳入 Zephyr 代码库所采用的评审流程，并说明项目如何处理安全敏感问题。

最后，本文说明如何修改本文档。

安全编码
*************

将 Zephyr 这样的开放软件系统设计为安全系统，需要遵循一组明确的设计标准。[SALT75]_ 定义了以下广泛接受的保护机制原则，以帮助防止安全违规并限制其影响：

- **Open design** 作为设计准则，纳入了这样的至理名言：保护机制无法在任何广泛使用的系统中长期保密。因此，不应依赖秘密的、量身定制的安全措施，而应使用公开接受的加密算法和成熟的加密库。

- **Economy of mechanism** 要求系统的底层设计应尽可能简单和精简。在 Zephyr 项目的语境中，这可以通过模块化代码 [PAUL09]_ 和抽象 API 实现。

- **Complete mediation** 要求对每个对象和每个进程的每次访问都必须先经过认证。应尽可能避免存储访问条件的机制。

- **Fail-safe defaults** 规定访问默认受限，只有在系统保护方案定义的特定条件下才被允许，例如成功认证后。此外，服务的默认设置应以提供最大安全性的方式选择。这对应于 “Secure by Default” 范式 [MS12]_。

- **Separation of privilege** 指在授予访问之前必须满足两个或更多条件。在 Zephyr 项目的语境中，这可能包括分割密钥 [PAUL09]_。

- **Least privilege** 描述了一种访问模型：每个用户、程序和线程都应仅拥有执行其任务所需的最小权限子集。该正向安全模型旨在最小化系统的攻击面。

- **Least common mechanism** 规定供多个用户或进程共用的机制，除非严格必需，否则不应共享。[SALT75]_ 中给出的例子是：某个函数应实现为每个用户各自执行的共享库，而不是所有用户共享的超级过程。

- **Psychological acceptability** 要求安全特性对开发者易于使用，以确保其被实际使用，并且其应用方式是正确的。

除这些一般原则外，以下要点专门适用于安全 RTOS 的开发：

- **Complementary Security/Defense in Depth**：不要依赖单一威胁缓解方法。在互补安全方法中，威胁缓解的一部分由底层平台完成。如果平台未提供此类机制，或不可信，则应使用纵深防御 [MS12]_ 范式。

- **Less commonly used services off by default**：为减少系统对潜在攻击的暴露，如果功能或服务很少被使用，则不应默认启用（[MS12]_ 给出了 80% 的阈值）。对于 Zephyr 项目，这可以通过配置管理实现。每个功能和模块都应表示为配置选项，并需要显式启用。然后，对特定用例不需要的功能、协议和驱动都可以禁用。如果启用了底层选项和 API 但应用未使用，应通知用户。

- **Change management**：为保证系统变更可追溯，每个变更都应遵循指定流程，包括变更请求、影响分析、批准、实施和验证阶段。在每个阶段，都应提供适当文档。所有提交都应关联到 issue tracker 中的 bug 报告或变更请求。没有有效引用的提交应被拒绝。

安全开发知识
****************************

安全设计者
================

Zephyr 项目必须至少拥有一位知道如何设计安全软件的主要开发者。

这需要理解以下设计原则，包括 [SALT75]_ 中的 8 个原则：

- economy of mechanism（尽可能保持设计简单和精简，例如通过采用大幅简化）

- fail-safe defaults（访问决策应默认拒绝，且项目的安装应默认安全）

- complete mediation（每个可能被限制的访问都必须检查权限且不可绕过）

.. todo: Explain better the constraints of embedded devices, and that
   we typically do edge detection, not at each function. Perhaps
   relate this to input validation below.

- open design（安全机制不应依赖攻击者对其设计的无知，而应依赖更容易保护和更改的信息，例如密钥和密码）

- separation of privilege（理想情况下，对重要对象的访问应依赖多个条件，因此击败一个保护系统不会导致完全访问。例如，多因素认证，例如同时要求密码和硬件令牌，比单因素认证更强）

- least privilege（进程应以必要的最小权限运行）

- least common mechanism（设计应最小化多个用户共用且所有用户依赖的机制，例如临时文件目录）

- psychological acceptability（人机界面必须为易用性设计——为 “least astonishment” 设计会有所帮助）

- limited attack surface（攻击者可尝试进入或提取数据的不同入口点的集合）

- input validation with allowlists（输入通常应在接收前检查，以确定其是否有效；该验证应使用允许列表，即仅接受已知良好值，而不是阻止列表，即尝试列出已知不良值）

漏洞知识
=======================

项目中的 “primary developer” 是指任何熟悉项目代码库、能够从容对其进行变更，并被项目大多数其他参与者如此认可的人。主要开发者通常在过去一年中通过代码、文档或回答问题等方式做出若干贡献。如果开发者启动了项目（且未在项目超过三年前离开）、有资格接收私有漏洞报告渠道的信息（如果存在该渠道）、能代表项目接受提交，或能执行项目软件的最终发布，则通常被视为主要开发者。如果只有一位开发者，该个人就是主要开发者。

至少一位主要开发者**必须**知道导致此类软件漏洞的常见错误类型，以及对抗或缓解每种错误的至少一种方法。

示例（取决于软件类型）包括 SQL 注入、操作系统注入、经典缓冲区溢出、跨站脚本、缺失认证和缺失授权。参见 `CWE/SANS top 25`_ 或 `OWASP Top 10`_ 获取常用列表。

非营利组织 OpenSecurityTraining2 为 C/C++ 开发者提供的免费课程可在 `OST2_1001`_ 获取。它教授如何防止、检测和缓解线性栈/堆缓冲区溢出、非线性越界写入、整数溢出及其他整数问题。后续课程 `OST2_1002`_ 涵盖未初始化数据访问、竞态条件、释放后使用、类型混淆和信息泄露漏洞。

.. Turn this into something specific. Can we find examples of
   mistakes.  Perhaps an example of things static analysis tool has sent us.

.. _CWE/SANS top 25: https://cwe.mitre.org/top25/

.. _OWASP Top 10: https://owasp.org/www-project-top-ten/

.. _OST2_1001: https://ost2.fyi/Vulns1001

.. _OST2_1002: https://ost2.fyi/Vulns1002

Zephyr 安全小组委员会
============================

应有一个 “Zephyr Security Subcommittee”，负责执行本指南、监控评审并改进这些指南。

该团队将根据 Zephyr Project 章程建立。

代码评审
***********

Zephyr 项目应使用一个代码评审系统，所有变更都必须经过该系统。每个变更都应至少由一位不是变更作者的主要开发者评审。该开发者应基于其对安全的一般理解，确定该变更是否影响系统安全；如果是，应请求具有漏洞知识的开发者或安全设计者也评审代码。这些人员中的任何一人都应有能力阻止该变更被合并到主线代码中，直到安全问题得到解决。

问题与 Bug 跟踪
***********************

Zephyr 项目应有一个 issue 跟踪系统（例如 GitHub_），可用于记录和跟踪系统中发现的缺陷。

.. _GitHub: https://www.github.com

由于安全问题通常是敏感的，该 issue 跟踪系统应有一个字段以指示安全问题。设置该字段应使该 issue 仅对 Zephyr Security Subcommittee 可见。此外，应有一个字段允许 Zephyr Security Subcommittee 添加对特定 issue 具有可见性的额外用户。

该禁运期，或有限可见性，应仅持续固定时长，默认值由项目决定。然而，由于安全考虑通常位于 Zephyr 项目本身之外，可能需要延长该禁运期。所需时间应在 issue 本身中清晰标注。

Zephyr Security Subcommittee 应至少每月审查一次 issue 列表。该审查应聚焦于跟踪修复、确定是否需要通知或让外部方参与，以及确定何时解除该 issue 的禁运。禁运**不应**通过自动化手段解除，但评审团队应避免在解除已解决问题上造成不必要的延迟。

对本文档的修改
******************************

对本文档的变更应由 Zephyr Security Subcommittee 评审，并以共识批准。

.. [#attackf]  一次攻击_ 导致相当一部分 DNS 基础设施被关闭。

.. _attack: https://www.theverge.com/2016/10/21/13362354/dyn-dns-ddos-attack-cause-outage-status-explained
