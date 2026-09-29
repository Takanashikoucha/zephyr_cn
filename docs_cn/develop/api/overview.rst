.. _api_overview:

API
概览
############

表格
列出
Zephyr
的
API
和
关于
它们
的
信息，
包括
它们
当前
的
:ref:`稳定性
级别 <api_lifecycle>`。
关于
主要
发布
版本
之间
API
更改
的
更多
细节
可以
在
:ref:`zephyr_release_notes`
中
找到。

版本
列
使用
`语义
版本
<https://semver.org/>`_，
并
有
以下
期望：

 * 主要
   版本
   零
   （0.y.z）
   用于
   初始
   开发。
   任何
   东西
   可以
   随时
   更改。
   公共
   API
   不
   应该
   被
   认为
   稳定。

    * 如果
      次要
      版本
      到
      一
      （0.1.z），
      API
      被
      认为
      :ref:`实验性
      <api_lifecycle_experimental>`。
    * 如果
      次要
      版本
      大于
      一
      （0.y.z
      |
      y
      >
      1），
      API
      被
      认为
      :ref:`不稳定
      <api_lifecycle_unstable>`。

 * 版本
   1.0.0
   定义
   公共
   API。
   这个
   发布
   之后
   版本
   号
   递增
   的
   方式
   取决于
   这个
   公共
   API
   和
   它
   如何
   更改。

    * 主要
      版本
      等于
      或
      大于
      一
      （x.y.z
      |
      x
      >=
      1）
      的
      API
      被
      认为
      :ref:`稳定
      <api_lifecycle_stable>`。
    * Zephyr
      中
      所有
      现有
      稳定
      API
      将
      从
      版本
      1.0.0
      开始。

 * 补丁
   版本
   Z
   （x.y.Z
   |
   x
   >
   0）
   如果
   只
   引入
   向后
   兼容
   的
   bug
   修复
   必须
   递增。
   bug
   修复
   定义
   为
   修复
   错误
   行为
   的
   内部
   更改。

 * 次要
   版本
   Y
   （x.Y.z
   |
   x
   >
   0）
   如果
   向
   公共
   API
   引入
   新
   的
   向后
   兼容
   功能
   必须
   递增。
   如果
   任何
   公共
   API
   功能
   被
   标记
   为
   已
   弃用，
   它
   必须
   递增。
   如果
   在
   私有
   代码
   内
   引入
   大量
   新
   功能
   或
   改进，
   它
   可以
   递增。
   它
   可以
   包括
   补丁
   级
   更改。
   次要
   版本
   递增
   时
   补丁
   版本
   必须
   重置
   为
   0。

 * 主要
   版本
   X
   （x.Y.z
   |
   x
   >
   0）
   如果
   对
   API
   做
   了
   兼容性
   破坏
   更改
   必须
   递增。

.. note::
   现有
   API
   的
   版本
   初始
   设置
   基于
   API
   的
   当前
   状态：

    - 0.1.0
      表示
      :ref:`实验性
      <api_lifecycle_experimental>`
      API
    - 0.8.0
      表示
      :ref:`不稳定
      <api_lifecycle_unstable>`
      API，
    - 最后
      1.0.0
      表示
      :ref:`稳定
      <api_lifecycle_stable>`
      API。

   未来
   对
   API
   的
   更改
   将
   需要
   按
   上面
   指南
   调整
   版本。


.. api-overview-table::
