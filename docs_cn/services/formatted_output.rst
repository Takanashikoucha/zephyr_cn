.. _formatted_output:

Formatted Output
################

Applications 以及
Zephyr 本身需
格式化
values 供
user 消费的
infrastructure。标准
C99 library ``*printf()``
functionality 满足
streaming output devices 或
memory
buffers 的
此
需求（但
embedded system 中
devices 可能
不接受
streamed
data（且
memory 可能
不可
用于
存储
格式化
output。

Internal Zephyr API 传统上
为
:c:func:`printk` 和
Zephyr 的
internal minimal libc 提供
此
功能（但
用
separate internal interfaces。Logging、
tracing、
shell 和
其他
applications 基于
build options 使用
这些
APIs 或
标准
libc
routines。

:c:func:`cbprintf` public APIs 转换
C99 format strings 和
arguments（提供
逐
character 通过
callback
mechanism 产生的
output（替代
原始
internal
functions（并提供
几乎
所有
C99 format
specifications 的
支持。Zephyr 中
``s*printf()`` C
libraries 的
既有
使用
可
转换
为
:c:func:`snprintfcb()` 以
避免
pull in
libc
implementations。

若干
Kconfig options 控制
启用的
features 集合（
允许
对
features 和
memory
usage 的
某些
控制：

* :kconfig:option:`CONFIG_CBPRINTF_FULL_INTEGRAL`
  或 :kconfig:option:`CONFIG_CBPRINTF_REDUCED_INTEGRAL`
* :kconfig:option:`CONFIG_CBPRINTF_FP_SUPPORT`
* :kconfig:option:`CONFIG_CBPRINTF_FP_A_SUPPORT`
* :kconfig:option:`CONFIG_CBPRINTF_FP_ALWAYS_A`
* :kconfig:option:`CONFIG_CBPRINTF_N_SPECIFIER`

:kconfig:option:`CONFIG_CBPRINTF_LIBC_SUBSTS` 可用于
提供
行为
类似
标准
libc
functions 的
functions（但
用
选择的
cbprintf
formatter（而非
pull in
libc 的
另一
formatter。

另外
:kconfig:option:`CONFIG_CBPRINTF_NANO` 可用于
回退
到
添加
此
capability
前
用于
:c:func:`printk` 的
非常
space-optimized
但
有限的
formatter。

.. _cbprintf_packaging:

Cbprintf Packaging
******************

通常（调用
``printf``
family 的
function 时
strings
同步
格式化。然而（有
formatting
延迟
更
有益
的
cases。此
情况下（须
捕获
state（format
string 和
arguments。此
state 形成
self-contained
package（包含
format
string 和
arguments。另外（package 可
包含
format
string
一部分
的
strings 的
copies（format
string 或
任何
``%s``
argument）。Package
primary
content 类似
va_list
stack
frame（故
标准
formatting
functions 用于
处理
package。由于
package
包含
作为
va_list
frame 处理的
data（须
维持
strict
alignment。由于
所需
padding（package
的
size
取决于
alignment。复制
package 时（应
复制到
与
origin 相同
alignment 的
memory
block。

Package 可有
以下
variants：

* **Self-contained** - 非
  read-only
  strings 追加
  到
  package。只要
  有
  对
  read-only
  string
  locations 的
  访问（即可
  从
  此
  package
  格式化
  string。Package
  可
  包含
  read-only
  strings
  在
  package
  中
  位置
  的
  information。该
  information
  可
  用于
  将
  packet
  转换
  为
  fully
  self-contained
  package。
* **Fully self-contained** - 所有
  strings
  追加
  到
  package。无需
  任何
  external
  data 即可
  从
  此
  package
  格式化
  string。
* **Transient**- 仅
  存储
  arguments。Package
  包含
  非
  read-only
  strings 的
  pointers
  在
  package
  中
  位置
  的
  information。可选（
  其
  可
  包含
  read-only
  string
  location
  information。只要
  非
  read-only
  strings
  仍
  有效
  且
  read-only
  strings
  可
  访问（即可
  从
  此
  package
  格式化
  string。或者（若
  package
  中
  有
  read-only
  string
  locations 的
  information（package
  可
  转换
  为
  **self-contained**
  package 或
  **fully self-contained**
  package。

Package 可用
两种
methods 创建：

* runtime - 用
  :c:func:`cbprintf_package` 或
  :c:func:`cbvprintf_package`。此
  method
  扫描
  format
  string（并
  基于
  检测
  到的
  format
  specifiers
  构建
  package。
* static - arguments 的
  types
  由
  preprocessor
  在
  compile
  time
  检测（且
  package
  创建
  为
  向
  提供
  memory 的
  简单
  assignments。此
  method
  显著
  快于
  runtime（超过
  15
  倍）（但
  有
  显著
  限制：char
  pointer
  使用时
  不能
  区分
  ``%p`` 和
  ``%s``。其
  将
  所有
  (unsigned)
  char
  pointers
  视为
  ``%s``（故
  将
  尝试
  将
  string
  追加
  到
  package。用
  :c:macro:`CBPRINTF_PACKAGE_CONVERT_PTR_CHECK`
  flag
  从
  **transient**
  package
  转换
  为
  **self-contained**
  package
  时
  可
  正确
  处理。然而（其
  需
  访问
  format
  string（且
  并非
  总是
  可能（故
  建议
  将
  用于
  ``%p`` 的
  char
  pointers
  cast
  为
  ``void *``。用
  :c:macro:`CBPRINTF_PACKAGE_CONVERT_PTR_CHECK`
  flag
  调用
  的
  :c:func:`cbprintf_package_convert`
  在
  char
  pointer
  与
  ``%p``
  一起
  使用时
  生成
  logging
  warning。


若干
Kconfig
options
控制
packaging
的
behavior：

* :kconfig:option:`CONFIG_CBPRINTF_PACKAGE_LONGDOUBLE`
* :kconfig:option:`CONFIG_CBPRINTF_STATIC_PACKAGE_CHECK_ALIGNMENT`

Cbprintf package conversion
===========================

可
将
package
转换
为
包含
更多
information 的
variant（如
**transient**
package
可
转换
为
**self-contained**。若
package
创建
时
用了
:c:macro:`CBPRINTF_PACKAGE_ADD_RO_STR_POS`
flag（则
可
转换
为
**fully self-contained**
package。

:c:func:`cbprintf_package_copy` 用于
计算
新
package
所需
space（并
复制
并
转换
package。

Cbprintf package format
=======================

Package
的
format
包含
platform
specific 的
paddings。Package
由
header
组成（其
包含
package
的
size（不含
追加
strings）和
追加
strings
的
数量。其后为
arguments（包含
alignment
paddings（并
类似
*va_list*
stack
frame。其后为
与
string
使用
的
character
pointer
arguments 关联的
data（其
未
追加
到
string（但
之后
可
由
:c:func:`cbprinf_package_convert`
追加。最后（package（
可选（
包含
追加
strings。每
string
包含
1
byte
header（其
包含
存储
address
argument
位置
的
index。Packaging
期间
address
设为
null（且
string
格式化
前
更新
为
指向
package
中
当前
string
location。更新
address
argument
须
在
string
格式化
前
立即
发生（因为
address
在
package
每次
复制
时
变更。

+------------------+-------------------------------------------------------------------------+
| Header           | 1 byte: Argument list size including header and *fmt* (in 32 bit words) |
|                  +-------------------------------------------------------------------------+
| sizeof(void \*)  | 1 byte: Number of strings appended to the package                       |
|                  +-------------------------------------------------------------------------+
|                  | 1 byte: Number of read-only string argument locations                   |
|                  +-------------------------------------------------------------------------+
|                  | 1 byte: Number of transient string argument locations                   |
|                  +-------------------------------------------------------------------------+
|                  | platform specific padding to sizeof(void \*)                            |
+------------------+-------------------------------------------------------------------------+
| Arguments        | Pointer to *fmt* (or null if *fmt* is appended to the package)          |
|                  +-------------------------------------------------------------------------+
|                  | (optional padding for platform specific alignment)                      |
|                  +-------------------------------------------------------------------------+
|                  | argument 0                                                              |
|                  +-------------------------------------------------------------------------+
|                  | (optional padding for platform specific alignment)                      |
|                  +-------------------------------------------------------------------------+
|                  | argument 1                                                              |
|                  +-------------------------------------------------------------------------+
|                  | ...                                                                     |
+------------------+-------------------------------------------------------------------------+
| String location  | Indexes of words within the package where read-only strings are located |
| information      +-------------------------------------------------------------------------+
| (optional)       | Pairs of argument index and argument location index where transient     |
|                  | strings are located                                                     |
+------------------+-------------------------------------------------------------------------+
| Appended         | 1 byte: Index within the package to the location of associated argument |
| strings          +-------------------------------------------------------------------------+
| (optional)       | Null terminated string                                                  |
|                  +-------------------------------------------------------------------------+
|                  | ...                                                                     |
+------------------+-------------------------------------------------------------------------+

.. warning::

  若
  :kconfig:option:`CONFIG_MINIMAL_LIBC`
  与
  :kconfig:option:`CONFIG_CBPRINTF_NANO`
  组合
  选择（用
  C
  standard
  library
  functions（如
  ``printf`` 或
  ``snprintf``）的
  formatting
  有限。除
  其他
  外（``%n``
  specifier、
  大多数
  format
  flags、
  precision
  control 和
  floating
  point
  不
  支持。

.. _cbprintf_packaging_limitations:

Limitations and recommendations
===============================

* 建议
  将
  与
  ``%p``
  format
  specifier
  一起
  使用
  的
  任何
  character
  pointer
  cast
  为
  其他
  pointer
  type（如
  ``void *``）。若
  format
  string
  不
  可
  访问（则
  仅
  可
  static
  packaging（且
  其
  将
  追加
  所有
  检测
  到的
  strings。用于
  ``%p`` 的
  Character
  pointer
  将
  被
  视为
  string
  pointer。从
  非预期
  location
  复制
  可
  有
  严重
  后果（如
  memory
  fault
  或
  security
  violation）。

API Reference
*************

.. doxygengroup:: cbprintf_apis
