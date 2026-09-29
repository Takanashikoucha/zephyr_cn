.. _west-build-flash-debug:

构建、
烧录
和
调试
################################

Zephyr
提供
多
个
:ref:`west
extension
commands
<west-extensions>`
用于
构建、
烧录
和
与
运行
在
board
上
的
Zephyr
程序
交互：
``build``、
``flash``、
``debug``、
``debugserver``、
``rtt``
和
``attach``。

对
添加
board
支持
给
烧录
和
调试
命令
的
信息，
参考
:ref:`flash-and-debug-support`
在
board
移植
指南
中。

.. Add
   a
   per-page
   contents
   at
   the
   top
   of
   the
   page.
   This
   page
   is
   nested
   deeply
   enough
   that
   it
   doesn't
   have
   any
   subheadings
   in
   the
   main
   nav.

.. only::
   html

   .. contents::
      :local:

.. _west-building:

构建：
``west
build``
************************

.. tip::
   运行
   ``west
   build
   -h``
   获取
   快速
   概览。

``build``
命令
帮助
你
从
源
构建
Zephyr
应用。
你
可以
用
:ref:`west
config
<west-config-cmd>`
配置
其
行为。

其
默认
行为
尝试
"做
你
意思
的"：

- 如果
  当前
  工作
  目录
  中
  有
  命名
  为
  :file:`build`
  的
  Zephyr
  构建
  目录，
  它
  被
  增量
  重新
  编译。
  如果
  你
  从
  Zephyr
  构建
  目录
  运行
  ``west
  build``
  同样
  为
  真。

- 否则，
  如果
  你
  从
  Zephyr
  应用
  的
  源
  目录
  运行
  ``west
  build``
  且
  没
  有
  找到
  构建
  目录，
  新
  的
  被
  创建
  且
  应用
  在
  它
  中
  被
  编译。
