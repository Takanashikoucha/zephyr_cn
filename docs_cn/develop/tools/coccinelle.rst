.. _coccinelle:

..
   Copyright
   2010
   Nicolas
   Palix
   <npalix@diku.dk>
   Copyright
   2010
   Julia
   Lawall
   <julia.lawall@lip6.fr>
   Copyright
   2010
   Gilles
   Muller
   <Gilles.Muller@lip6.fr>

Coccinelle
##########

Coccinelle
是
一
个
模式
匹配
和
文本
转换
工具
在
kernel
开发
中
有
许多
用途，
包括
应用
复杂
的、
树
范围
的
patches
和
检测
问题
编程
模式。

.. note::
   Linux
   和
   macOS
   开发
   环境
   被
   支持，
   但
   不
   支持
   Windows。

获取
Coccinelle
******************

kernel
中
包含
的
semantic
patches
使用
Coccinelle
version
1.0.0-rc11
及
以上
提供
的
功能
和
选项。
使用
较早
版本
会
失败
因为
Coccinelle
文件
和
``coccicheck``
使用
的
选项
名称
已
更新。

Coccinelle
通过
许多
发行版
的
包
管理器
可
用，
例如
：

.. rst-class::
   rst-columns

   * Debian
   * Fedora
   * Ubuntu
   * OpenSUSE
   * Arch
     Linux
   * NetBSD
   * FreeBSD

一些
发行版
包
已
过时
推荐
使用
从
Coccinelle
homepage
发布
的
最新
版本
在
