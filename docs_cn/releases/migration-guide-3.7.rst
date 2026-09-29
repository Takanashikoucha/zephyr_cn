:orphan:

.. _migration_3.7:

Migration
guide
to
Zephyr
v3.7.0
################################

这
个
document
describe
migrating
你
的
application
从
Zephyr
v3.6.0
到
Zephyr
v3.7.0
required
的
changes。

其他
changes
（不
directly
related
to
migrating
applications）
可以
found
在
:ref:`release
notes<zephyr_3.7>`。

.. contents::
    :local:
    :depth:
    2

Build
System
************

*
Completely
overhauled
SoCs
和
boards
被
defined
的
way。
这
require
所有
out
of
tree
的
SoCs
和
boards
被
ported
到
new
的
model。
See
:ref:`hw_model_v2`
获取
更
detailed
的
information。
(:github:`69607`)

*
以下
build
time
generated
的
headers:

   .. list-table::
      :header-rows:
      1

      *
      -
      Affected
      header
      files
      *
      -
      ``app_version.h``
      *
      -
      ``autoconf.h``
      *
      -
      ``cmake_intdef.h``
      *
      -
      ``core-isa-dM.h``
      *
      -
      ``devicetree_generated.h``
      *
      -
      ``driver-validation.h``
      *
      -
      ``kobj-types-enum.h``
      *
      -
      ``linker-kobject-prebuilt-data.h``
      *
      -
      ``linker-kobject-prebuilt-priv-stacks.h``
      *
      -
      ``linker-kobject-prebuilt-rodata.h``
