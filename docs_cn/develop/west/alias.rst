.. _west-aliases:

West
aliases
############

West
允许
添加
alias
命令
到
本地、
全局
或
系统
配置
文件。
这些
aliases
使
添加
快捷
方式
变
得
简单
用于
常
用
的
或
难以
记忆
的
命令
以
方便
开发。

类似
于
``git``
aliases
如何
工作，
alias
命令
被
替换
为
alias
的
完整
文本
并
解析
为
新
的
shell
参数
列表
（内部
用
Python
函数
`shlex.split()`_
拆分
值）。
这
使
添加
参数
参数
成为
可能
如
它们
被
传递
给
原始
命令。
空格
被
考虑
为
参数
分隔符；
如果
参数
不
应该
被
拆分
用
适当
的
转义。

.. _shlex.split():
   https://docs.python.org/3/library/shlex.html#shlex.split

要
添加
新
的
alias
简单
调用
``west
config``
命令：

.. code-block:: shell

   west
   config
   alias.mylist
   "list
   -f
   '{name}
   {revision}'"

要
列出
aliases，
用
:samp:`west
help
{some_alias}`。

递归
aliases
被
允许
因为
alias
命令
可以
包含
其他
aliases，
有效
地
构建
更
复杂
但
容易
记忆
的
命令。

可以
覆盖
现有
命令，
例如
传递
默认
参数：

.. code-block:: shell

   west
   config
   alias.update
   "update
   -o=--depth=1
   -n"

.. warning::

   覆盖/
   遮蔽
   其他
   或
   内置
   命令
   是
   高级
   用例，
   它
   可以
   导致
   奇怪
   的
   副作用
   并
   应该
   非常
   小心
   地
   做。

Examples
