.. _cra_faq:

欧盟《网络弹性法案》（CRA）
#############################

.. warning::
   本文档仅供参考，不构成法律建议。
   请咨询您的法律顾问，以获取针对您特定情况的合规指导。
   您也可以咨询欧盟认可的实验室（见 `CRA 公告机构列表`_），它们可以提供帮助。

概述
********

《网络弹性法案》（[CRA24]_）是一项欧盟法规，为投放欧盟市场的含数字元素产品（PDE）确立了网络安全要求。
该法规于 2024 年 12 月 10 日生效。

.. admonition:: 关键日期
   :class: important

   * **2026 年 6 月 11 日**：评估机构投入运营；市场监督机构定义明确
   * **2026 年 9 月 11 日**：制造商必须报告正在被积极利用的漏洞和严重事件
   * **2027 年 12 月 11 日**：法规全面适用于自该日期起投放市场的产品，
     或在该日期之前投放市场但之后经过重大修改的产品。

本页说明 CRA 如何同时关联两类主体：在商业产品中使用 Zephyr 的制造商，
以及作为开源软件管理方（steward）的 Zephyr 项目本身。

对于制造商，CRA 施加基本网络安全要求（`Annex I Part I`_），
以及漏洞处理与报告义务（`Annex I Part II`_）。对于作为开源软件管理方的 Zephyr 项目，
CRA 引入了一套量身定制的义务，包括维护网络安全策略、报告被积极利用的漏洞和严重事件，
以及与市场监督机构合作。

对于使用 Zephyr 的制造商
******************************

CRA 适用于我的产品吗？
=================================

如果您将含数字元素产品（PDE）投放欧盟市场用于商业目的，CRA 即适用。
这包括带有嵌入式软件的硬件设备，以及独立软件产品。

含数字元素的产品是与其他设备或网络相连的硬件和/或软件。
产品范围包括远程数据处理解决方案（RDPS）：
不属于产品本身但产品功能所必需的软件
（例如，手机应用或云服务）。

CRA 适用于在欧盟市场投放的终端产品或组件。
根据 `Blue Guide`_ 和 `EU CRA 指南`_ 中的定义：
当产品首次可供欧盟市场使用时，即被视为投放市场。
当产品在商业活动中被供应到欧盟市场用于分发、消费或使用，
无论是否收费，即被视为在欧盟市场可供使用。
投放市场适用于产品系列中的每个单独单元；
开发或设计日期无关紧要。
有关“投放市场”的更多信息，请参见 `EU CRA 指南`_。
该指南详细说明了独立软件、源代码发布和复杂产品等特定情形。

法律中定义了几项市场例外（医疗、汽车、航空、军事、备件）。
这些例外有严格条件；请参见 CRA 正文（`Article 2`_）。

我的产品属于哪个类别？
=========================================

CRA 基于风险将产品分为若干类别：**重要产品**（`Annex III`_）和
**关键产品**（`Annex IV`_）。未列入任一类别的产品被视为
**默认**产品，要求较低。

例如，默认产品通常可以依赖自我评估（见 :ref:`compliance_path`），
且文档和保证要求较少。

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - 类别
     - 简短描述
     - 示例 Zephyr 用例
   * - 默认
     - 未被列为"重要"或"关键"的含数字元素产品。
     - - Wi-Fi 智能灯泡或开关（例如，通过 Thread/Wi-Fi 运行 Matter）。
       - 用于个人健康的可穿戴活动追踪器或智能手表。
       - 蓝牙 LE 音频配件或无线传感器标签。
       - 连接到 CAN 总线的温度传感器。
   * - 重要（I 类）
     - 较高风险产品，通常面向消费者，执行与安全或访问相关的功能。
     - - 用于住宅的智能门锁或门禁读卡器。
       - 管理网络流量的路由器。
       - 联网报警系统或安全传感器。
       - 具有 AVA_VAN.1 保护级别的微控制器。
   * - 重要（II 类）
     - 用于企业/工业/基础设施环境，或具有特权网络角色的较高风险产品。
     - - 具有 AVA_VAN.2 或 AVA_VAN.3 保护级别的微控制器。
   * - 关键
     - 一旦失陷可能严重影响关键基础设施或基本服务的产品。
     - - 智能电表网关。
       - 硬件安全模块（HSM）或智能卡固件。
.. admonition:: 核心功能 vs. 集成
   :class: important

   分类由最终产品的**核心功能**决定，而非其集成的各个组件（`Article 7`_）。

   * 将重要或关键组件（例如，安全元件、嵌入式浏览器）集成到另一产品中，
     **不会**自动使该产品变为重要或关键。
   * 一个产品*能够*执行重要/关键类别的功能，但其核心功能不同，
     则**不**被视为具有该核心功能。

   **示例：**

   * 如果您使用 Zephyr 构建网络防火墙，其核心功能是安全，
     因此该产品为重要产品（II 类）。
   * 如果您使用 Zephyr 构建咖啡机，并利用 Zephyr 的网络栈功能保护该设备，
     其核心功能仍然是制作咖啡。这是一个"默认"产品。

   简而言之，在设备中使用安全关键的 Zephyr 功能（如加密或安全启动），
     **不会**将该设备提升到更高的风险类别。

有关详细分类，请参见 `Annex III`_ 和 `Annex IV`_。
带技术描述的产品类别完整清单见 `Implementing Regulation (EU) 2025/2392`_。

.. _compliance_path:

我必须选择哪条合规路径？
===================================

CRA 根据产品类别定义了不同的合格评定程序。
您必须选择与您的分类以及对协调标准的依赖程度相对应的路径。

.. list-table:: CRA 产品类别与评定路径
  :widths: 20 55 25
  :header-rows: 1

  * - 类别
    - 合格评定程序
    - 公告机构参与？
  * - 默认
    - 模块 A（制造商自我评估）或模块 B + 模块 C，或模块 H。
    - 模块 A 非强制。
  * - 重要 I 类
    - **仅在**完全应用欧盟官方公报中引用的协调标准时采用模块 A。
      否则：模块 B + 模块 C，或模块 H。
    - 模块 A 非强制。
  * - 重要 II 类
    - 模块 B + 模块 C，或模块 H。（**不允许**自我评估）。
    - 是（强制）
  * - 关键
    - **欧洲网络安全认证**（例如 EUCC），或模块 B + 模块 C + 模块 H
      （待授权法案确定）。
    - 是（强制）

"模块"指 `Decision No 768/2008/EC`_（"新立法框架"）中定义的特定评定程序，
并由 CRA 在 `Annex VIII`_ 中加以调整：

* `Module A`_（内部生产控制）：您自行编制技术文档、开展风险评估并作出合格声明。
  无需外部审计方。
* `Module B`_（欧盟类型检验）+ `Module C`_（与类型的一致性）：公告机构 [#nb]_
  对技术设计进行检验（模块 B）并颁发证书。随后您须确保生产与该类型一致（模块 C）。
* `Module H`_（全面质量保证）：公告机构 [#nb]_ 审计您管理设计、生产和测试的质量管理体系（QMS）。

.. [#nb]  公告机构将于 **2026 年 6 月 11 日**前投入运营。

作为制造商，我的主要义务是什么？
==============================================

CRA 主要在 `Article 13`_（产品要求与尽职调查）和 `Article 14`_（漏洞处理与报告）
中规定了制造商义务。无论产品如何分类，以下核心义务适用于所有含数字元素产品的制造商。

**风险评估**
  在整个产品生命周期中评估并记录网络安全风险。

**尽职调查**
  在集成第三方组件（包括 Zephyr 等开源软件）时履行尽职调查义务。

**漏洞处理**
  在投放产品到市场时处理漏洞。
  在支持期（生命周期或至少 5 年）内监控漏洞。
  漏洞处理意味着识别硬件和软件漏洞（例如，通过 SBOM），
  针对您的产品进行风险评估，并在风险不可接受时提供软件更新。

**事件报告**
  报告影响您产品的正在被积极利用的漏洞，
  以及影响项目基础设施的严重事件。
  该义务在支持期结束后继续。

**技术文档**
  按 `Article 31`_ 和 `Annex VII`_ 编制文档。

**合格评定**
  按 `Article 32`_ 和 `Annex VIII`_ 评定合格性。

**CE 标志**
  加贴 CE 标志并起草欧盟合格声明。

不合规的处罚是什么？
=========================================

* 最高 15,000,000 欧元或全球年营业额的 2.5%（违反 `Article 13`_ 和 `Article 14`_）。
* 最高 10,000,000 欧元或营业额的 2%（违反其他义务）。

.. _cra_vulnerability_reporting_obligations:

漏洞报告义务是什么？
=================================================

CRA 区分"一般"漏洞（通过您的常规漏洞管理流程处理）
和触发 `Article 14`_ 严格通知时限的情形：**被积极利用的漏洞**和**严重事件**。

下表总结了最低报告步骤。

.. list-table:: 被积极利用的漏洞（`Article 14`_ (1) 和 (2)）
   :header-rows: 1
   :widths: 20 20 60

   * - 步骤
     - 时限
     - 内容（最低要求）
   * - 早期预警
     - 知悉后 24 小时内
     - 通过单一报告平台向您的 CSIRT 协调机构和 ENISA 通报：
       有被积极利用的漏洞影响您的产品。如已知，须说明该产品在哪些成员国可获得。
   * - 漏洞通知
     - 知悉后 72 小时内
     - 提供受影响产品的一般信息、漏洞利用和漏洞的一般性质、
       已采取的纠正或缓解措施，以及用户可采取的措施。如适用，
       须说明您认为所通报信息的敏感程度如何。
   * - 最终报告
     - 不迟于纠正或缓解措施可用后 14 天
     - 描述该漏洞、其严重程度和影响、利用该漏洞的恶意行为者信息（如可获得），
       以及已提供的安全更新或其他纠正措施详情。

.. list-table:: 严重事件（`Article 14`_ (3) 至 (6)）
   :header-rows: 1
   :widths: 20 20 60

   * - 步骤
     - 时限
     - 内容（最低要求）
   * - 早期预警
     - 知悉后 24 小时内
     - 通过单一报告平台向您的 CSIRT 协调机构和 ENISA 通报：
       严重事件影响您产品的安全。须说明是否疑似由非法或恶意行为导致，
       如已知，须说明该产品在哪些成员国可获得。
   * - 事件通知
     - 知悉后 72 小时内
     - 提供事件性质的一般信息、初步评估（包括当时已知的
       影响/严重程度）、已采取的纠正或缓解措施，以及用户可采取的措施。
       如适用，须说明您认为所通报信息的敏感程度如何。
   * - 最终报告
     - 事件通知后 1 个月内
     - 提供事件的详细描述，包括严重程度和影响、威胁类型或可能的根本原因，
       以及已采取和正在进行的缓解措施。

如何获取 SBOM（软件物料清单）？
=====================================================

Zephyr 可使用 ``west spdx`` 命令为您的应用程序自动生成 SBOM。

有关如何配置和使用该工具的详细信息，请参见 :ref:`west-spdx`。

我应如何处理 Zephyr 的漏洞？
==========================================

作为将 Zephyr 集成到产品中的制造商，您仍须负责漏洞管理，
并在适用情况下履行 CRA 报告义务。
Zephyr 提供漏洞信息，但您必须针对自己的产品进行评估并采取行动。

一个实用的工作流程如下：

1. **保持信息畅通**。注册 `Zephyr Vulnerability Alert Registry`_，
   在漏洞披露时接收通知。

2. **评估影响**。针对每条公告，使用您的 SBOM 和配置，
   判断受影响的 Zephyr 组件是否存在于您的产品中、是否可达、以及是否具有安全相关性。

3. **制定修复计划**。决定适当的响应方式（例如，应用补丁、调整配置等）。

4. **部署修复**。集成、测试并推出所选修复方案，
   并按需更新您的 SBOM 和产品文档。

5. **履行报告义务**。如果该漏洞影响您的产品且正被积极利用，
   或导致严重事件，请按 `Article 14`_ 时限以及前述章节
   :ref:`cra_vulnerability_reporting_obligations` 的要求进行报告。

Zephyr 处理漏洞遵循什么时间表？
============================================================

Zephyr 运营自己的 PSIRT 流程，针对分诊、通知和披露设有目标时间表。
这些是*项目*时间表，不是制造商的法律期限。

您按 `Article 14`_ 承担的 CRA 报告义务，由*您*知悉自己的产品
受到被积极利用的漏洞或严重事件影响的时间触发。
这可能**早于**下面列出的某些 Zephyr 里程碑，
意味着您可能必须在 Zephyr 修复方案可用或公开披露之前，
就发送早期预警或事件报告。

Zephyr 使用私有 GitHub 安全公告和禁运期（最多 90 天）来协调修复与披露。
完整流程在 :ref:`reporting` 中有描述，关键里程碑如下：

* **7 天内**：PSIRT 向最初报告者反馈。
* **30 天内**：通过警报注册表通知制造商，项目提供修复方案。
* **总计最多 90 天**：安全敏感的漏洞在禁运期结束后公开。

我需要报告我在 Zephyr 中发现的漏洞吗？
=====================================================

**是的**，根据 `Article 13(6)`_，如果您发现集成在您产品中的组件（包括 Zephyr）
存在漏洞，您**必须**报告它。此外，如果您为该漏洞开发了修复方案，
您还必须分享相关代码或文档。参见 :ref:`reporting`。

此外，可考虑按 `Article 15`_ 自愿向 CSIRT 或 ENISA 报告。

对于作为开源软件管理方的 Zephyr
************************************

Zephyr 在 CRA 下的角色是什么？
==================================

Zephyr 是 `Article 3`_ (14) 下的**"开源软件管理方"**：
一个为面向商业活动的 PDE 开发系统性提供持续支持的法律实体。

Zephyr 在 Article 24 下的义务：

**网络安全策略**
  记录安全策略和漏洞处理流程。

**合作**
  与市场监督机构合作以缓解风险。

**事件报告**
  报告项目中被积极利用的漏洞，以及影响 Zephyr 基础设施的严重事件
  （在 Zephyr 涉及的范围内）。

CRA 适用于 Zephyr 的贡献者吗？
=========================================

**不适用。** CRA 不适用于 Zephyr 的个别贡献者（`Recital 18`_）。

开发功能或修复漏洞的贡献者不受 CRA 义务约束。

Zephyr 如何履行其管理方义务？
=============================================

`Article 24(1)`_：安全策略（已完成）
  * 已记录于 :ref:`security-overview`
  * 漏洞报告流程：:ref:`reporting`
  * 安全编码指南：:ref:`secure code`

`Article 24(2)`_：与机构合作（进行中）
  * 自 2017 年起注册为 CVE 编号机构（CNA）
  * 活跃的 Zephyr 项目安全事件响应团队（PSIRT）
  * **进行中**：确定欧盟的 CSIRT 协调机构

`Article 14(1)`_ 和 `Article 14(3)`_：事件报告（进行中）
  * **进行中**：确定 NVD 处理流程是否适用于向 CSIRT/ENISA 的报告
  * 计划与欧盟报告要求保持一致

`Article 14(8)`_：用户通知（已完成）
  * 面向制造商和集成商的漏洞警报注册表
  * CVE 发布和安全公告

`Article 52(3)`_：纠正措施（已完成）
  * 已与 CVE 机构建立流程
  * 通过 PSIRT 及时响应

外部资源
******************

CRA 官方文档
==========================

* `EU CRA Regulation 2024/2847
  <https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847>`_
* `Implementing Regulation (EU) 2025/2392`_（重要和关键产品类别的技术描述）
* `ENISA CRA Requirements-Standards Mapping
  <https://www.enisa.europa.eu/publications/cyber-resilience-act-requirements-standards-mapping>`_
* `European Commission CRA FAQ
  <https://digital-strategy.ec.europa.eu/en/faqs/cyber-resilience-act-questions-and-answers>`_
* `European Commission CRA 指南（解答了许多关于解释的问题）
  <https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation>`_

标准与技术规范
=====================================

相关现有标准：

ETSI 和 CEN/CENELC 正在响应 `CRA 标准化请求 (M/606)
<https://ec.europa.eu/growth/tools-databases/enorm/mandate/606_en>`_ 制定协调标准。

CEN/CENELEC 制定的 CRA 横向标准：

* EN40000-1-1：术语定义
* EN40000-1-2：安全设计产品的质量流程。包括风险评估、采购尽职调查、开发、测试、验证、制造、退役等。
* EN40000-1-3：漏洞处理流程
* EN40000-1-4：安全控制：降低网络安全风险的技术解决方案。
  基于为 CE RED 授权法案开发的 hEN18031-x 标准。

EN40000-1-4 早期草案的介绍可在 CEN/CENELEC 网站获取：`安全控制
<https://www.cencenelec.eu/news-events/events/2026/2026-03-05-cra-standards-unlocked-deep-dive-session-security-controls-generic-security-requirements/>`_。

ETSI 公开草案标准
包括以下产品类别的特定要求：

* 操作系统（prEN 304 626）
* 浏览器（prEN 304 617）
* 密码管理器（prEN 304 618）
* 防火墙（prEN 304 636）

有关草案标准的完整清单以及公众咨询参与方式，请参见
`ETSI Cyber Resilience Act Portal <https://docbox.etsi.org/cyber/CYBER/Open>`_。

* 一旦协调完成，这些标准可通过 `协调标准 <https://harmonized.standards.eu/>`_
  向欧盟、欧洲自由贸易联盟和英国公民免费开放。

教育资源
=====================

* `Linux Foundation: Understanding the EU CRA
  <https://training.linuxfoundation.org/express-learning/understanding-the-eu-cyber-resilience-act-cra-lfel1001>`_
* `Linux Foundation CRA Readiness Report <https://www.linuxfoundation.org/research/cra-readiness>`_
* `Linux Foundation CRA Compliance Best Practices
  <https://www.linuxfoundation.org/research/cra-compliance-best-practices>`_
* `OpenSSF CRA Guidance <https://openssf.org/public-policy/eu-cyber-resilience-act/>`_

Zephyr 特定资源
=========================

* :ref:`security-overview`
* :ref:`reporting`
* `Zephyr Vulnerability Alert Registry`_
* :ref:`Zephyr 漏洞 <vulnerabilities>`

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

.. _`CRA 公告机构列表`: https://webgate.ec.europa.eu/single-market-compliance-space/notified-bodies/free-search?filter=notificationStatus:1,legislation:167953
.. _`Blue Guide`: https://single-market-economy.ec.europa.eu/news/blue-guide-implementation-product-rules-2022-published-2022-06-29_en
.. _`EU CRA 指南`: https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation
.. _`Article 2`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_2
