.. _test-framework:

Test
Framework
###############

Zephyr
Test
Framework
（Ztest）
提供
一
个
简单
的
测试
框架
旨在
在
开发
期间
使用。
它
提供
基本
的
assertion
macros
和
通用
的
测试
结构。

框架
可以
用
两
种
方式
使用，
要么
作为
集成
测试
的
通用
框架，
要么
用于
单元
测试
特定
modules。

.. contents::
   :depth:
   1
   :local:
   :backlinks:
   top

快速
开始
-
集成
测试
*********************************

简单
的
工作
基础
位于
:zephyr_file:`samples/subsys/testsuite/integration`。
要
为
**foo**
的
**bar**
组件
做
一
个
测试
应用，
你
应该
复制
sample
文件夹
到
``tests/foo/bar``
并
编辑
那里
的
文件
调整
用于
你
的
测试
应用
的
目的。

要
构建
和
执行
你
的
测试
应用
中
定义
的
所有
适用
的
测试
scenario
用
:ref:`Twister
<twister_script>`
工具，
例如：

.. code-block:: console

   west
   twister
   -T
   tests/foo/bar/

要
只
选择
一
个
测试
scenario，
用
``--scenario``
命令
运行
Twister：

.. code-block:: console

   west
   twister
   --scenario
   tests/foo/bar/your.test.scenario.name

上面
命令
行
中
``tests/foo/bar``
是
你
的
测试
应用
的
路径
而
``your.test.scenario.name``
引用
:file:`tests.yaml`
中
定义
的
测试
scenario
