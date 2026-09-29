.. _west-release-notes:

West
Release
Notes
##################

v1.5.0
******

Major
changes:

- 添加
  auto-caching
  支持。
  将
  ``--auto-cache
  <directory>``
  参数
  传递
  给
  ``west
  update``。

Other
changes:

- 允许
  组合
  ``--name-cache``
  和
  ``--path-cache``
  用于
  ``west
  update``。

- 在
  manifest
  schema
  中
  记录
  默认
  revision
  值。

Bug
fixes:

- 允许
  空
  或
  缺失
  的
  manifest
  projects
  列表。

- 使
  ``manifest.group-filter``
  列表
  顺序
  在
  冻结
  或
  解析
  manifest
  文件
  时
  确定。

v1.4.0
******

Changes:

- 允许
  追加
  数据
  到
  配置
  字符串。
  要
  追加
  到
  ``<name>``
  的
  值，
  输入：
  ``west
  config
  -a
  <name>
  <value>``。

- 添加
  ``--untracked``
  参数
  选项
  到
  ``west
  manifest``。
  在
  workspace
  中
  运行
  ``west
  manifest
  --untracked``
  打印
  所有
  不
  被
  west
  跟踪
  或
  管理
  的
  文件
  和
  目录。

- 添加
  ``--inactive``
  参数
  选项
  到
  ``west
  list``
  支持
  打印
  inactive
  projects。

- 支持
  ``--active-only``
  参数
  选项
  用于
  ``west
  manifest
  --resolve``
  和
