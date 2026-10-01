.. _cra_faq:

欧盟网络弹性法案（CRA）
#############################

.. warning::
   本文档仅供参考，不构成法律建议。
   请咨询您的法律顾问，获取针对您特定情况的合规指导。

概述
********

网络弹性法案（[CRA24]_）是一项欧盟法规，
为投放欧盟市场的含数字元素产品（PDE）
建立网络安全要求。
它于 2024 年 12 月 10 日生效。

.. admonition:: 关键日期
   :class: important

   * **2026 年 6 月 11 日**：评估机构投入运营
   * **2026 年 9 月 11 日**：制造商必须报告漏洞和事件
   * **2027 年 12 月 11 日**：法规全面适用

本页解释了 CRA 如何同时关联
使用 Zephyr 的商业产品制造商，
以及作为开源软件管理者的 Zephyr 项目本身。

对于制造商，CRA 施加基本网络安全要求
（`附录 I 第一部分`_）
以及漏洞处理和报告义务
（`附录 I 第二部分`_）。对于作为
开源软件管理者的 Zephyr 项目，
CRA 引入了一套量身定制的义务，
包括维护网络安全策略、
报告被积极利用的漏洞和
严重事件，以及与市场监督
机构合作。

对于使用 Zephyr 的制造商
******************************

CRA 适用于我的产品吗？
=================================

如果您将含数字元素产品（PDE）
投放欧盟市场用于商业目的，
则 CRA 适用。
这包括带有嵌入式软件的硬件设备，
以及独立软件产品。

我的产品属于哪个类别？
=========================================

CRA 基于风险将产品
分类为：**重要产品**（`附录 III`_）
和**关键产品**（`附录 IV`_）。
未列入任一类别的产品被视为
**默认**产品，具有较低要求。

例如，默认产品通常可以
依赖自我评估（见 :ref:`compliance_path`）
，具有较少的文档和
保证要求。

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - 类别
     - 简短描述
     - 示例 Zephyr 用例
   * - 默认
     - 未列为"重要"或"关键"的
       含数字元素产品。
     - - Wi-Fi 智能灯泡或开关
       （例如，运行 Matter over
       Thread/Wi-Fi）。
       - 可穿戴活动追踪器或
       个人健康智能手表。
       - 蓝牙 LE 音频配件或
       无线传感器标签。
   * - 重要（I 类）
     - 较高风险产品，通常面向
       消费者，执行安全或
       访问相关功能。
     - - 用于住宅的智能门锁或
       门禁读卡器。
       - 管理网络流量的
       智能家居中枢或路由器。
       - 联网报警系统或
       安全传感器。
   * - 重要（II 类）
     - 用于企业/工业/基础设施
       环境或具有特权网络
       角色的较高风险产品。
     - - 工业可编程逻辑控制器
       （PLC）或机器人控制器。
       - 用于设备身份的
       带安全飞地/TEE 的
       微控制器。
       - 执行边缘处理的
       工业物联网网关。
   * - 关键
     - 一旦失陷可能严重影响
       关键基础设施或
       基本服务的产品。
     - - 带远程关闭功能的
       智能电表或水表。
       - 硬件安全模块（HSM）
       或智能卡固件。
       - 用于能源或
       交通电网的安全关键
       传感器。

.. admonition:: 核心功能 vs. 集成
   :class: important

   分类由最终产品的**核心功能**
   决定，而非其集成的
   各个组件（`第 7 条`_）。

   * 将重要或关键组件
     （例如，安全元件、
     嵌入式浏览器）
     集成到另一产品中
     **不会**自动使该产品
     变为重要或关键。
   * 一个**能够**执行
     重要或关键产品功能的产品，
     仅当该功能是其
     核心功能时，才被视为
     重要或关键。

我的产品需要哪些文档？
=========================================

这取决于产品类别。默认产品通常
需要较少的文档。重要和关键产品
需要更多文档，包括
技术文档、合规声明、
以及（对于关键产品）
第三方评估。

谁负责合规？
=========================================

制造商负责确保其产品
符合 CRA。对于使用
Zephyr 的产品，制造商
应确保 Zephyr 配置
和定制符合适用要求。

对于 Zephyr 项目
**********************

CRA 对 Zephyr 项目意味着什么？
=========================================

作为开源软件管理者，
Zephyr 项目承担 CRA 引入的
一套量身定制的义务，
包括：

* 维护网络安全策略
* 报告被积极利用的漏洞
  和严重事件
* 与市场监督机构合作

Zephyr 项目需要做什么？
=========================================

Zephyr 项目应：

* 维护并更新网络安全策略
* 建立漏洞报告流程
* 及时发布安全更新
* 与市场监督机构合作

Zephyr 项目如何帮助制造商合规？
=========================================

Zephyr 项目通过提供
安全更新、漏洞信息和
合规指导，
帮助制造商满足
CRA 要求。

.. _`Article 7`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_7
.. _`Article 14`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_14
.. _`Article 15`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_15
.. _`Article 16`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_16
.. _`Article 17`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_17
.. _`Article 18`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_18
.. _`Article 19`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_19
.. _`Article 20`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_20
.. _`Article 21`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_21
.. _`Article 22`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_22
.. _`Article 23`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_23
.. _`Article 24`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_24
.. _`Article 25`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_25
.. _`Article 26`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_26
.. _`Article 27`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_27
.. _`Article 28`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_28
.. _`Article 29`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_29
.. _`Article 30`: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202402847#art_30
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
