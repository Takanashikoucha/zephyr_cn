.. _snippets:

片段
########

片段
是
一种
方式
将
构建
系统
设置
保存
在
一个
地方，
然后
在
构建
任何
Zephyr 应用
时
使用
那些
设置。
这
让
你
可以
在
应用
到
多个
不同
应用
时
单独
保存
通用
配置。

片段
的
一些
示例
使用
场景
是：

- 将
  开发板
  的
  控制台
  后端
  从
  "真实"
  UART
  更改
  为
  USB CDC-ACM UART
- 启用
  经常
  使用
  的
  调试
  选项
- 将
  相互
  关联
  的
  配置
  设置
  应用
  到
  AMP SoC 上
  的
  "主"
  CPU 和
  协
  处理器
  核心

以下
页面
记录
这个
功能。

.. toctree::
   :maxdepth: 1

   using.rst
   /snippets/index.rst
   writing.rst
   design.rst
