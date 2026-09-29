.. _kconfig:

配置系统（Kconfig）
*******************************

Zephyr
内核
和
子系统
可以
在
构建
时
配置
以
适应
特定
应用
和
平台
需求。
配置
通过
Kconfig 处理，
这
是
Linux
内核
使用
的
相同
配置
系统。
目标
是
支持
配置
而
无需
更改
任何
源
代码。

配置
选项
（通常
称为
*符号*）
定义
在
:file:`Kconfig` 文件
中，
这些
文件
还
指定
确定
哪些
配置
有效
的
符号
之间
的
依赖
关系。
符号
可以
分组
到
菜单
和
子
菜单
以
保持
交互式
配置
接口
有序。

Kconfig 的
输出
是
一个
头
文件
:file:`autoconf.h`，
带有
可以
在
构建
时
测试
的
宏。
未
使用
功能
的
代码
可以
被
编译
掉
以
节省
空间。

以下
章节
解释
如何
设置
Kconfig 配置
选项，
深入
介绍
Kconfig 在
Zephyr 项目
中
如何
使用，
并
提供
一些
编写
:file:`Kconfig` 文件
的
技巧
和
最佳
实践。

.. toctree::
   :maxdepth: 1

   menuconfig.rst
   tracing.rst
   setting.rst
   tips.rst
   preprocessor-functions.rst
   extensions.rst

对
优化
其
配置
以
获得
安全
性
感兴趣
的
用户
应
参考
Zephyr
安全
指南
中
关于
:ref:`hardening` 的
章节。
