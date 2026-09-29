.. _west-zephyr-ext-cmds:

额外
的
Zephyr
extension
commands
####################################

本
页
记录
杂项
:ref:`west-zephyr-extensions`。

.. _west-boards:

列出
boards：
``west
boards``
*******************************

``boards``
命令
可以
用
来
列出
Zephyr
支持
的
boards
而
不
需要
求助
于
额外
的
信息
来源。

它
可以
通过
输入
运行::

  west
  boards

这
个
命令
用
默认
格式
列出
所有
支持
的
boards。
如果
你
偏好
自己
指定
显示
格式
你
可以
用
``--format``
（或
``-f``）
标志::

  west
  boards
  -f
  "{arch}:{name}"

关于
格式化
选项
的
额外
帮助
可以
通过
运行
找到::

  west
  boards
  -h

.. _west-completion:

Shell
completion
scripts：
``west
completion``
*********************************************

``completion``
extension
命令
输出
shell
completion
scripts
然后
可以
直接
用
来
为
支持
的
shells
启用
shell
completion。

它
当前
支持
以下
shells：

- bash
