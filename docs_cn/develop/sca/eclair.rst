.. _eclair:

ECLAIR
支持
##############

Bugseng
`ECLAIR
<https://www.bugseng.com/eclair/>`__
是
一
个
认证
的
静态
分析
工具
和
软件
验证
平台。
应用
范围
从
编码
规则
验证，
特别
强调
MISRA
和
BARR-C
编码
标准，
到
软件
指标
计算，
到
软件
组件
之间
的
独立性
和
无
干扰
检查，
到
重要
类别
软件
错误
的
自动
检测。

前提
条件
*************

ECLAIR
工具
必须
安装
并
在
操作系统
的
PATH
变量
中
可用。

要
验证
安装，
你
可以
运行：

.. code-block:: shell

   eclair
   -version

使用
ECLAIR
需要
有效
的
许可
或
试用
许可。
要
申请
试用
许可，
访问
`这
页
<https://www.bugseng.com/eclair/free-trial>`__。

运行
ECLAIR
**************

要
运行
ECLAIR，
:ref:`west
build
<west-building>`
应该
被
调用
带
``-DZEPHYR_SCA_VARIANT=eclair``
参数。

.. code-block:: shell

   west
   build
   -b
   mimxrt1064_evk
   samples/basic/blinky
   --
   -DZEPHYR_SCA_VARIANT=eclair

.. note::
   这
   只
   会
   用
   预定义
   规则集
   ``first_analysis``
   调用
   ECLAIR
   分析。
   如果
   你
   想
   用
   不同
   的
   规则集，
   你
   需要
   提供
   一
   个
   配置
   文件。
   参考
   下
   一
   节
   获取
   更多
   信息。

配置
**************

ECLAIR
SCA
环境
的
配置
可以
通过
CMake
选项
文件
或
用
适配
的
选项
作为
命令行
参数
完成。

要
将
CMake
选项
文件
调用
到
ECLAIR
调用
中，
你
可以
定义
``ECLAIR_OPTIONS_FILE``
变量，
例如：

.. code-block:: shell

   west
   build
   -b
   mimxrt1064_evk
   samples/basic/blinky
   --
   -DZEPHYR_SCA_VARIANT=eclair
   -DECLAIR_OPTIONS_FILE=my_options.cmake

默认
（如果
未
给出
配置
文件）
配置
总是
``first_analysis``，
这是
一
个
极
小
的
规则
选择
用
来
验证
一切
正确
工作。

如果
默认
配置
想
通过
命令行
而
非
通过
选项
文件
覆盖，
这
可以
通过
给出
参数
``-DOption=ON|OFF``
实现。

例如：

.. code-block:: shell

   west
   build
   -b
   mimxrt1064_evk
   samples/basic/blinky
   --
   -DZEPHYR_SCA_VARIANT=eclair
   -DECLAIR_REPORTS_SARIF=ON

Zephyr
是
一
个
大
而
复杂
的
项目，
因此
配置
集
被
拆分
成
Zephyr
的
指南
选择
（取自
https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html）
五
个
集
以
使
其
在
私有
机器
上
更
容易
消化
使用：

* first_analysis
  （默认）：
  项目
  编码
  指南
  的
  极
  小
  选择
  用
  来
  验证
  一切
  正确
  工作。

* STU：
  项目
  编码
  指南
  的
  选择，
  可以
  通过
  独立
  分析
  单
  个
  翻译
  单元
  验证。

* STU_heavy：
  复杂
  STU
  项目
  编码
  指南
  的
  选择
  需要
  大量
  时间。

* WP：
  所有
  完整
  程序
  项目
  编码
  指南
  （MISRA
  术语
  中
  的
  "system"）。

* std_lib：
  关于
  C
  标准
  库
  的
  项目
  编码
  指南。

此外，
zephyr_guidelines
规则集
包含
`Coding
Guidelines
<https://docs.zephyrproject.org/latest/contribute/coding_guidelines/index.html>`__
中
列出
的
所有
主要
规则。

相关
CMake
选项：

* ``ECLAIR_RULESET_FIRST_ANALYSIS``
* ``ECLAIR_RULESET_STU``
* ``ECLAIR_RULESET_STU_HEAVY``
* ``ECLAIR_RULESET_WP``
* ``ECLAIR_RULESET_STD_LIB``
* ``ECLAIR_RULESET_ZEPHYR_GUIDELINES``

用户
定义
规则集
====================

如果
你
想
用
自己
定义
的
规则集
而
非
预定义
的
Zephyr
编码
指南
规则集，
你
可以
通过
设置
:code:`ECLAIR_RULESET_USER=ON`
做
到。
用
以下
命名
格式
为
ECLAIR
创建
你
自己
的
规则集
文件：
``analysis_<RULESET>.ecl``。
创建
文件
后，
用
CMake
变量
:code:`ECLAIR_USER_RULESET_NAME`
定义
ECLAIR
的
规则集
名称。
如果
规则集
文件
不
在
应用
源
目录
中，
你
可以
用
CMake
变量
:code:`ECLAIR_USER_RULESET_PATH`
定义
规则集
文件
的
路径。
这
个
配置
接受
相对
路径
和
绝对
路径。

相关
CMake
选项
和
变量：

* ``ECLAIR_RULESET_USER``
* ``ECLAIR_USER_RULESET_NAME``
* ``ECLAIR_USER_RULESET_PATH``

生成
额外
报告
格式
**********************************

ECLAIR
可以
生成
额外
的
报告
格式
（例如
DOC、ODT、XLSX）
和
除
默认
ecd
文件
外
的
不同
报告
变体。
以下
额外
报告
和
报告
格式
可以
被
生成：

* 电子
  表格
  格式
  的
  指标。

* 电子
  表格
  格式
  的
  发现。

* SARIF
  格式
  的
  发现。

* 纯
  文本
  格式
  的
  摘要
  报告。

* DOC
  格式
  的
  摘要
  报告。

* ODT
  格式
  的
  摘要
  报告。

* HTML
  格式
  的
  摘要
  报告。

* txt
  格式
  的
  详细
  报告。

* DOC
  格式
  的
  详细
  报告。

* ODT
  格式
  的
  详细
  报告。

* HTML
  格式
  的
  详细
  报告。

相关
CMake
选项：

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

完整
报告
的
详细
级别
===========================

txt
和
doc
完整
报告
的
详细
级别
也
可以
通过
配置
适配。
这
种
情况
下，
以下
配置
可用：

* 显示
  所有
  区域

* 只
  显示
  第一
  个
  区域

相关
CMake
选项：

* ``ECLAIR_FULL_DOC_ALL_AREAS``
* ``ECLAIR_FULL_DOC_FIRST_AREA``
* ``ECLAIR_FULL_TXT_ALL_AREAS``
* ``ECLAIR_FULL_TXT_FIRST_AREA``
