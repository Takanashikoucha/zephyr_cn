.. _cra_faq:

欧盟网络弹性法案（CRA）
#############################

.. warning::
   本文档仅供参考，不构成法律建议。
   请就与您具体情况相关的合规指导咨询您的法律顾问。

概述
********

网络弹性法案（[CRA24]_）是一项欧盟法规，为投放到欧盟市场的
含数字元素产品（PDE）建立了网络安全要求。
该法案于 2024 年 12 月 10 日生效。

.. admonition:: 关键日期
   :class: important

   * **2026 年 6 月 11 日**：评估机构投入运营
   * **2026 年 9 月 11 日**：制造商必须报告漏洞和事件
   * **2027 年 12 月 11 日**：法规全面适用

本页说明 CRA 如何与使用 Zephyr 的商业产品制造商以及
Zephyr 项目本身（作为开源软件管理方）相关。

对于制造商，CRA 规定了基本网络安全要求（`Annex I Part I`_）
以及漏洞处理和报告义务（`Annex I Part II`_）。
对于 Zephyr 项目作为开源软件管理方，CRA 引入了
一套定制的义务，包括维护网络安全策略、报告正在被
主动利用的漏洞和严重事件，以及与市场监管机构合作。

面向使用 Zephyr 的制造商
******************************

CRA 适用于我的产品吗？
=================================

如果您将含数字元素产品（PDE）投放到欧盟市场用于
商业目的，则 CRA 适用。这包括带嵌入式软件的
硬件设备和独立软件产品。

我的产品属于哪个类别？
=========================================

CRA 根据风险将产品分为类别：**重要产品**（`Annex III`_）和
**关键产品**（`Annex IV`_）。未列入任一类别的产品被视为
**默认**产品，要求较低。

例如，默认产品通常可依赖自我评估（参见 :ref:`compliance_path`），
文档和保证要求较少。

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - 类别
     - 简要描述
     - Zephyr 用例示例
   * - 默认
     - 未列为"重要"或"关键"的含数字元素产品。
     - - Wi-Fi 智能灯泡或开关（例如运行 Matter over Thread/Wi-Fi）。
       - 用于个人健康的可穿戴活动追踪器或智能手表。
       - 蓝牙 LE 音频配件或无线传感器标签。
   * - 重要（I 类）
     - 较高风险的产品，通常面向消费者，执行安全或
       访问相关功能。
     - - 用于住宅的智能门锁或门禁读卡器。
       - 管理网络流量的智能家居中枢或路由器。
       - 联网报警系统或安全传感器。
   * - 重要（II 类）
     - 用于企业/工业/基础设施环境或具有特权
       网络角色的较高风险产品。
     - - 工业可编程逻辑控制器（PLC）或机器人控制器。
       - 用于设备身份的带安全飞地/TEE 的微控制器。
       - 执行边缘处理的工业物联网网关。
   * - 关键
     - 其被攻破可能严重影响关键基础设施或
       基本服务的产品。
     - - 支持远程关断的智能电表或水表。
       - 硬件安全模块（HSM）或智能卡固件。
       - 用于能源或交通电网的安全关键传感器。

.. admonition:: 核心功能与集成
   :class: important

   分类由最终产品的**核心功能**决定，而非其集成的
   各个组件（`Article 7`_）。

   * 将重要或关键组件（例如安全元件、嵌入式浏览器）
     集成到另一产品中，**不会**自动使该产品
     成为重要或关键产品。
   * 能够执行重要/关键类别功能但核心功能
     不同的产品，**不**被认为具有该核心功能。

   **示例：**

   * 如果您使用 Zephyr 构建网络防火墙，核心功能是
     安全，使产品成为重要产品（II 类）。
   * 如果您使用 Zephyr 构建咖啡机，并利用 Zephyr 的
     网络栈功能保护设备，核心功能仍然是
     制作咖啡。这是一个"默认"产品。

   简而言之，在设备中使用安全关键的 Zephyr 功能
     （如加密或安全启动）**不会**将该设备
     提升至更高风险类别。

   有关详细分类，参见 `Annex III`_ 和 `Annex IV`_。
   带技术描述的产品类别完整列表在
   `Implementing Regulation (EU) 2025/2392`_ 中提供。

.. _compliance_path:

我必须选择哪条合规路径？
==================================

CRA 根据产品类别定义了不同的合格评定程序。
您必须选择与您的分类和对协调标准的依赖
相对应的路径。

.. list-table:: CRA 产品类别与评估路径
  :widths: 20 55 25
  :header-rows: 1

  * - 类别
    - 合格评定程序
    - 是否需要第三方审计？
  * - 默认
    - 模块 A（内部控制）。制造商自我评估。
    - 否
  * - 重要 I 类
    - **仅当**完全应用协调标准时才用模块 A。
      否则：模块 B + 模块 C，或模块 H。
    - 是（若未完全使用标准）
  * - 重要 II 类
    - 模块 B + 模块 C，或模块 H。（**不**允许
      自我评估）。
    - 是（强制）
  * - 关键
    - **欧洲网络安全认证**（如 EUCC）或
      模块 B + 模块 C + 模块 H（待授权法案）。
    - 是（强制）

"模块"指 `Decision No 768/2008/EC`_
（"新立法框架"）中定义的特定评估程序，
由 CRA 在 `Annex VIII`_ 中改编：

* `Module A`_（内部生产控制）：您创建技术文档、
  执行风险评估并自行声明合格。无需外部审计员。
* `Module B`_（EC 类型检验）+ `Module C`_（类型合格）：
  通报机构 [#nb]_ 检验技术设计（模块 B）
  并发出证书。然后您确保生产符合
  该类型（模块 C）。
* `Module H`_（全面质量保证）：通报机构 [#nb]_
  审计您管理设计、生产和测试的
  质量管理体系（QMS）。

.. [#nb]  通报机构将于 **2026 年 6 月 11 日**前投入运营。

我作为制造商的主要义务是什么？
===============================================

CRA 主要在 `Article 13`_（产品要求和尽职调查）
和 `Article 14`_（漏洞处理和报告）中定义
制造商义务。无论产品如何分类，
以下核心义务适用于所有含数字元素产品的
制造商。

**风险评估**
  在整个产品生命周期中评估和记录网络安全风险。

**尽职调查**
  在集成第三方组件（包括 Zephyr 等开源软件）时
  进行尽职调查。

**漏洞处理**
  至少处理漏洞 5 年（支持期），包括
  接收报告和应用更新。

**事件报告**
  报告正在被主动利用的、影响 Zephyr 的漏洞，
  以及影响项目基础设施的严重事件。

**技术文档**
  按 `Article 31`_ 和 `Annex VII`_ 创建文档。

**合格评定**
  按 `Article 32`_ 和 `Annex VIII`_ 评估合格性。

**CE 标志**
  加贴 CE 标志并起草欧盟合格声明。

不合规的处罚是什么？
==========================================

* 最高 15,000,000 欧元或全球年营业额的 2.5%
  （违反 `Article 13`_ 和 `Article 14`_）。
* 最高 10,000,000 欧元或营业额的 2%
  （违反其他义务）。

.. _cra_vulnerability_reporting_obligations:

漏洞报告义务是什么？
=================================================

CRA 区分"普通"漏洞（通过您的正常漏洞管理
流程处理）和触发 `Article 14`_ 严格
通知时间线的情况：**正在被主动利用的漏洞**
和**严重事件**。

下表总结了最低报告步骤。

.. list-table:: 正在被主动利用的漏洞（`Article 14`_ (1) 和 (2)）
   :header-rows: 1
   :widths: 20 20 60

   * - 步骤
     - 期限
     - 内容（最低要求）
   * - 早期预警
     - 知悉后 24 小时内
     - 通过单一报告平台通知您的 CSIRT 协调员和
       ENISA，您产品存在正在被主动利用的漏洞。
       在已知情况下，指明产品在哪些成员国
       可获取。
   * - 漏洞通知
     - 知悉后 72 小时内
     - 提供受影响产品的一般信息、利用和漏洞的
       一般性质、已采取的纠正或缓解措施，
       以及用户可采取的措施。在适用情况下，
       指明您认为所通知信息的敏感程度。
   * - 最终报告
     - 纠正或缓解措施可用后 14 天内
     - 描述漏洞、其严重性和影响、任何利用该漏洞
       的恶意行为者信息（如有），以及已发布的
       安全更新或其他纠正措施的详细信息。

.. list-table:: 严重事件（`Article 14`_ (3) 至 (6)）
   :header-rows: 1
   :widths: 20 20 60

   * - 步骤
     - 期限
     - 内容（最低要求）
   * - 早期预警
     - 知悉后 24 小时内
     - 通过单一报告平台通知您的 CSIRT 协调员和
       ENISA，严重事件影响了您产品的安全。
       指明是否怀疑由非法或恶意行为引起，
       在已知情况下指明产品在哪些成员国
       可获取。
   * - 事件通知
     - 知悉后 72 小时内
     - 提供事件性质的一般信息、初步评估
       （包括当时已知的影响/严重程度）、
       已采取的纠正或缓解措施，以及用户
       可采取的措施。在适用情况下，
       指明您认为所通知信息的敏感程度。
   * - 最终报告
     - 事件通知后 1 个月内
     - 提供事件的详细描述，包括严重性和影响、
       威胁类型或可能的根本原因，
       以及已实施和正在进行的缓解措施。

如何获取 SBOM（软件物料清单）？
=====================================================

Zephyr 可使用 ``west spdx`` 命令为您的应用
自动生成 SBOM。

有关如何配置和使用该工具的详细信息，
参见 :ref:`west-spdx`。

我应如何处理 Zephyr 漏洞？
==========================================

作为将 Zephyr 集成到产品中的制造商，您仍然
负责漏洞管理，并在适用情况下负责 CRA 报告。
Zephyr 提供漏洞信息，但您必须针对
您自己的产品进行评估和处理。

一个实用工作流是：

1. **保持知情**。注册 `Zephyr Vulnerability Alert Registry`_
   以在漏洞披露时接收通知。

2. **评估影响**。对于每条公告，使用您的 SBOM
   和配置来确定受影响的 Zephyr 组件是否
   存在于您的产品中、是否可访问且与安全相关。

3. **制定修复计划**。决定适当的响应
   （例如应用补丁、调整配置等）。

4. **部署修复**。集成、测试并推出所选的
   修复，并按需更新您的 SBOM 和产品
   文档。

5. **满足报告义务**。如果漏洞影响您的产品
   且正在被主动利用，或导致严重事件，
   请按 `Article 14`_ 时间线和前一节
   :ref:`cra_vulnerability_reporting_obligations`
   的要求进行报告。

Zephyr 处理漏洞遵循什么时间线？
=============================================================

Zephyr 运行自己的 PSIRT 流程，具有分诊、
通知和披露的目标时间线。这些是*项目*
时间线，不是制造商的法律期限。

您按 `Article 14`_ 的 CRA 报告义务
由*您*知悉您的产品受到正在被主动利用的
漏洞或严重事件影响的时间触发。
这可能**早于**下面的一些 Zephyr 里程碑，
意味着您可能需要在 Zephyr 修复可用之前
或公开披露之前发送早期预警或事件报告。

Zephyr 使用私有 GitHub 安全公告和禁运期
（最多 90 天）来协调修复和披露。
虽然完整流程在 :ref:`reporting` 中有描述，
但关键里程碑是：

* **7 天内**：PSIRT 对初始报告者的反馈。
* **30 天内**：通过警报注册中心通知制造商，
  且项目发布修复。
* **总共最多 90 天**：安全敏感的漏洞在
  禁运期后公开。

我需要报告我在 Zephyr 中发现的漏洞吗？
=====================================================

**需要**，根据 `Article 13(6)`_，
如果您发现集成到您产品中的组件（包括 Zephyr）
存在漏洞，您**必须**报告它。此外，
如果您为该漏洞开发了修复，您还必须
分享相关代码或文档。参见 :ref:`reporting`。

此外，考虑按 `Article 15`_ 自愿向
CSIRT 或 ENISA 报告。

面向作为开源管理方的 Zephyr
************************************

Zephyr 在 CRA 下的角色是什么？
==================================

Zephyr 是 `Article 3`_ (14) 下的**"开源软件管理方"**：
一个系统性地为旨在用于商业活动的 PDE 开发
提供持续支持的法律实体。

Zephyr 在 Article 24 下的义务：

**网络安全策略**
  记录安全策略和漏洞处理。

**合作**
  与市场监管机构合作以缓解风险。

**事件报告**
  报告项目中正在被主动利用的漏洞以及影响
  Zephyr 基础设施的严重事件（在 Zephyr
  涉及的范围内）。

CRA 适用于 Zephyr 贡献者吗？
==========================================

**不适用。** CRA 不适用于 Zephyr 的
个人贡献者（`Recital 18`_）。

开发功能或修复 bug 的贡献者不受
CRA 义务约束。

Zephyr 如何履行其管理方义务？
=============================================

`Article 24(1)`_：安全策略（已完成）
  * 已记录于 :ref:`security-overview`
  * 漏洞报告流程：:ref:`reporting`
  * 安全编码指南：:ref:`secure code`

`Article 24(2)`_：与当局合作（进行中）
  * 自 2017 年起注册为 CVE 编号机构（CNA）
  * 活跃的 Zephyr 项目安全事件响应团队（PSIRT）
  * **进行中**：确定欧盟的 CSIRT 协调员

`Article 14(1)`_ 和 `Article 14(3)`_：事件报告（进行中）
  * **进行中**：确定 NVD 流程是否适用于
    CSIRT/ENISA 报告
  * 计划与欧盟报告要求对齐

`Article 14(8)`_：用户通知（已完成）
  * 面向制造商和集成商的漏洞警报注册中心
  * CVE 发布和安全公告

`Article 52(3)`_：纠正措施（已完成）
  * 已建立与 CVE 机构的流程
  * 通过 PSIRT 及时响应

外部资源
******************

CRA 官方文档
==========================

* `EU CRA Regulation 2024/2847
  <https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847>`_
* `Implementing Regulation (EU) 2025/2392`_
  （重要和关键产品类别的技术描述）
* `ENISA CRA Requirements-Standards Mapping
  <https://www.enisa.europa.eu/publications/cyber-resilience-act-requirements-standards-mapping>`_
* `European Commission CRA FAQ
  <https://digital-strategy.ec.europa.eu/en/faqs/cyber-resilience-act-questions-and-answers>`_

标准和技术规范
=====================================

相关的现有标准：

* `ETSI EN 303 645 <https://www.etsi.org/deliver/etsi_en/303600_303699/303645/>`_
  - 消费者物联网网络安全：基本要求

ETSI 正在响应 `CRA Standardisation Request (M/606)
<https://ec.europa.eu/growth/tools-databases/enorm/mandate/606_en>`_
制定协调标准。公开的标准草案包括
以下产品特定要求：

* 操作系统（prEN 304 626）
* 浏览器（prEN 304 617）
* 密码管理器（prEN 304 618）
* 防火墙（prEN 304 636）

有关标准草案完整列表和参与公开咨询，
参见 `ETSI Cyber Resilience Act Portal
<https://docbox.etsi.org/cyber/CYBER/Open>`_。

教育资源
=====================

* `Linux Foundation: Understanding the EU CRA
  <https://training.linuxfoundation.org/express-learning/understanding-the-eu-cyber-resilience-act-cra-lfel1001>`_
* `Linux Foundation CRA Readiness Report
  <https://www.linuxfoundation.org/research/cra-readiness>`_
* `Linux Foundation CRA Compliance Best Practices
  <https://www.linuxfoundation.org/research/cra-compliance-best-practices>`_
* `OpenSSF CRA Guidance
  <https://openssf.org/public-policy/eu-cyber-resilience-act/>`_

Zephyr 专属资源
=========================

* :ref:`security-overview`
* :ref:`reporting`
* `Zephyr Vulnerability Alert Registry`_
* :ref:`Zephyr Vulnerabilities <vulnerabilities>`

..

.. _`Decision No 768/2008/EC`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008D0768
.. _`Module A`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008D0768#d1e41-98-1
.. _`Module B`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008D0768#d1e288-98-1
.. _`Module C`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008D0768#d1e439-98-1
.. _`Module H`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008D0768#d1e1719-98-1

.. _`CRA Requirements-Standards Mapping`: https://www.enisa.europa.eu/publications/cyber-resilience-act-requirements-standards-mapping

.. _`Recital 18`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#rct_18

.. _`Article 3`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_3
.. _`Article 7`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_7
.. _`Article 13`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_13
.. _`Article 13(6)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#013.006
.. _`Article 13(14)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#013.014
.. _`Article 14`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_14
.. _`Article 14(1)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#014.001
.. _`Article 14(3)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#014.003
.. _`Article 14(8)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#014.008
.. _`Article 15`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_15
.. _`Article 24(1)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#024.001
.. _`Article 24(2)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#024.002
.. _`Article 31`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_31
.. _`Article 32`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_32
.. _`Article 52(3)`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#052.003

.. _`Annex I Part I`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_I
.. _`Annex I Part II`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_I
.. _`Annex III`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_III
.. _`Annex IV`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_IV
.. _`Annex VII`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_VII
.. _`Annex VIII`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#anx_VIII

.. _`Implementing Regulation (EU) 2025/2392`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R2392

.. _`Zephyr Vulnerability Alert Registry`: https://www.zephyrproject.org/vulnerability-registry/
