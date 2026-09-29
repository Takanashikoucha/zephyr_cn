:orphan:

.. _west-apis:
.. _west-apis-west:

West
APIs
#########

本
页
记录
:ref:`west
<west>`
提供
的
Python
APIs，
以及
zephyr
仓库
中
:ref:`west
extensions
<west-extensions>`
使用
的
一些
额外
APIs。

**Contents**:

.. contents::
   :local:

.. NOTE:
   documentation
   authors:

   1. keep
      these
      sorted
      by
      package/module
      name.
   2. if
      you
      add
      a
      :ref:
      target
      here,
      add
      it
      to
      west-not-found.rst
      too.

.. _west-apis-commands:

west.commands
*************

.. module::
   west.commands

所有
内置
和
extension
命令
被
实现
为
这里
定义
的
:py:class:`WestCommand`
类
的
子类。
一些
exception
类型
也
被
提供。

WestCommand
============

.. autoclass::
   west.commands.WestCommand

   Instance
   attributes:
