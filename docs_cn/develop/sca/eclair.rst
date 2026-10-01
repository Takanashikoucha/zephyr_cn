.. _eclair:

ECLAIR 支持
##############

Bugseng `ECLAIR <https://www.bugseng.com/eclair/>`__ 是一款经过认证的静态分析工具和软件验证平台。
其应用范围涵盖编码规则验证（尤其侧重于 MISRA 和 BARR-C 编码标准）、软件度量计算、
软件组件间独立性与无干扰性检查，以及重要类别软件错误的自动检测。

先决条件
*************

ECLAIR 工具必须已安装，并在操作系统的 PATH 变量中可用。

要验证安装，可以运行：

.. code-block:: shell

   eclair -version

使用 ECLAIR 需要有效的许可证或试用许可证。要申请试用许可证，请访问`此页面 <https://www.bugseng.com/eclair/free-trial>`__。

运行 ECLAIR
**************

要运行 ECLAIR，:ref:`west build <west-building>` 应带上 ``-DZEPHYR_SCA_VARIANT=eclair`` 参数调用。

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=eclair

.. note::
   这将仅使用预定义规则集 ``first_analysis`` 调用 ECLAIR 分析。
   如果想使用其他规则集，需要提供配置文件。更多信息参见下一节。

配置
**************

ECLAIR SCA 环境的配置可以通过 CMake 选项文件完成，也可以以适配后的选项作为命令行参数传入。

要在 ECLAIR 调用中引入 CMake 选项文件，可以定义 ``ECLAIR_OPTIONS_FILE`` 变量，例如：

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=eclair -DECLAIR_OPTIONS_FILE=my_options.cmake

默认配置（在未给出配置文件时）始终是 ``first_analysis``，
这是一组很小的规则，用于验证一切正确工作。

如果要通过命令行而非选项文件覆盖默认配置，
可以给出 ``-DOption=ON|OFF`` 参数实现。

例如：

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=eclair -DECLAIR_REPORTS_SARIF=ON

Zephyr 是一个大型且复杂的项目，因此配置集被拆分为五个集合，
以便在个人机器上更易使用——这些集合取自 Zephyr 的编码指南
（参见 https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html）：

* first_analysis（默认）：项目编码指南的一小部分内容，用于验证一切正确工作。

* STU：项目编码指南中可以通过独立分析单个翻译单元来验证的部分。

* STU_heavy：需要大量运行时间的复杂 STU 项目编码指南部分。

* WP：所有全程序（whole program）级别的项目编码指南（即 MISRA 术语中的"系统"）。

* std_lib：关于 C 标准库的项目编码指南。

此外，zephyr_guidelines 规则集包含 `编码指南 <https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html>`__
中列出的所有主要规则。

相关 CMake 选项：

* ``ECLAIR_RULESET_FIRST_ANALYSIS``
* ``ECLAIR_RULESET_STU``
* ``ECLAIR_RULESET_STU_HEAVY``
* ``ECLAIR_RULESET_WP``
* ``ECLAIR_RULESET_STD_LIB``
* ``ECLAIR_RULESET_ZEPHYR_GUIDELINES``

用户自定义规则集
====================

如果想使用自己定义的规则集，而非预定义的 Zephyr 编码指南规则集，
可以设置 :code:`ECLAIR_RULESET_USER=ON`。
按以下命名格式为 ECLAIR 创建自己的规则集文件：
``analysis_<RULESET>.ecl``。
创建文件后，用 CMake 变量 :code:`ECLAIR_USER_RULESET_NAME` 为 ECLAIR 指定规则集名称。
如果规则集文件不在应用源目录中，
可以用 CMake 变量 :code:`ECLAIR_USER_RULESET_PATH` 定义规则集文件的路径。
该配置接受相对路径和绝对路径。

相关 CMake 选项和变量：

* ``ECLAIR_RULESET_USER``
* ``ECLAIR_USER_RULESET_NAME``
* ``ECLAIR_USER_RULESET_PATH``

生成附加报告格式
**********************************

除默认的 ecd 文件外，ECLAIR 还能生成附加的报告格式（例如 DOC、ODT、XLSX）
以及报告的不同变体。可生成的附加报告及格式如下：

* 电子表格格式的度量数据。

* 电子表格格式的检测结果。

* SARIF 格式的检测结果。

* 纯文本格式的摘要报告。

* DOC 格式的摘要报告。

* ODT 格式的摘要报告。

* HTML 格式的摘要报告。

* txt 格式的详细报告。

* DOC 格式的详细报告。

* ODT 格式的详细报告。

* HTML 格式的详细报告。

相关 CMake 选项：

* ``ECLAIR_METRICS_TAB``
* ``ECLAIR_REPORTS_TAB``
* ``ECLAIR_REPORTS_SARIF``
* ``ECLAIR_SUMMARY_TXT``
* ``ECLAIR_SUMMARY_DOC``
* ``ECLAIR_SUMMARY_ODT``
* ``ECLAIR_SUMMARY_HTML``
* ``ECLAIR_FULL_TXT``
* ``ECLAIR_FULL_DOC``
* ``ECLAIR_FULL_ODT``
* ``ECLAIR_FULL_HTML``

完整报告的详细级别
============================

txt 和 doc 完整报告的详细级别也可以通过配置进行调节。
此时可用的配置如下：

* 显示所有区域

* 仅显示第一个区域

相关 CMake 选项：

* ``ECLAIR_FULL_DOC_ALL_AREAS``
* ``ECLAIR_FULL_DOC_FIRST_AREA``
* ``ECLAIR_FULL_TXT_ALL_AREAS``
* ``ECLAIR_FULL_TXT_FIRST_AREA``
