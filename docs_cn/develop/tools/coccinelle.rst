.. _coccinelle:

..
   Copyright 2010 Nicolas Palix <npalix@diku.dk>
   Copyright 2010 Julia Lawall <julia.lawall@lip6.fr>
   Copyright 2010 Gilles Muller <Gilles.Muller@lip6.fr>

Coccinelle
##########

Coccinelle 是一个用于模式匹配和文本转换的工具，在内核开发中有许多用途，包括应用复杂的、跨整棵树的补丁以及检测有问题的编程模式。

.. note::
   支持 Linux 和 macOS 开发环境，但不支持 Windows。

获取 Coccinelle
******************

内核中包含的语义补丁使用 Coccinelle 版本 1.0.0-rc11 及以上提供的功能和选项。使用更早版本将会失败，因为 Coccinelle 文件和 ``coccicheck`` 使用的选项名称已更新。

Coccinelle 可通过许多发行版的包管理器获得，例如：

.. rst-class:: rst-columns

   * Debian
   * Fedora
   * Ubuntu
   * OpenSUSE
   * Arch Linux
   * NetBSD
   * FreeBSD

一些发行版包已过时，推荐使用从 Coccinelle 主页 https://coccinelle.lip6.fr/ 发布的最新版本。

或从 GitHub 获取：

https://github.com/coccinelle/coccinelle

获得后，运行以下命令：

.. code-block:: console

   ./autogen
   ./configure
   make

以普通用户身份运行，并用以下命令安装：

.. code-block:: console

   sudo make install

更详细的从源代码构建的安装说明可在此处找到：

https://github.com/coccinelle/coccinelle/blob/master/install.txt

补充文档
**************************

关于语义补丁语言（SmPL）语法文档，请参考：

https://coccinelle.gitlabpages.inria.fr/website/documentation.html

在 Zephyr 上使用 Coccinelle
**************************

``coccicheck`` 检查器是 Coccinelle 基础设施的前端，有多种模式：

定义了四个基本模式：``patch``、``report``、``context`` 和 ``org``。要使用的模式通过设置 ``--mode=<mode>`` 或 ``-m=<mode>`` 指定。

* ``patch`` 在可能时提议修复。

* ``report`` 生成以下格式的列表：
  file:line:column-column: message

* ``context`` 以类似 diff 的风格高亮感兴趣的行及其上下文。感兴趣的行用 ``-`` 表示。

* ``org`` 生成 Emacs Org 模式格式的报告。

注意并非所有语义补丁都实现了所有模式。为便于使用 Coccinelle，默认模式是 ``report``。

另外两个模式提供了这些模式的常见组合。

- ``chain`` 按上述顺序依次尝试前面的模式，直到一个成功。

- ``rep+ctxt`` 依次运行 report 模式和 context 模式。应与 C 选项一起使用（后面描述），该选项基于文件检查代码。

示例
********

要为每个语义补丁生成报告，运行以下命令：

.. code-block:: console

   ./scripts/coccicheck --mode=report

要生成补丁，运行：

.. code-block:: console

   ./scripts/coccicheck --mode=patch

``coccicheck`` 目标将 ``scripts/coccinelle`` 子目录中可用的所有语义补丁应用到整个源代码树。

对每个语义补丁，会提议一个提交消息。它给出语义补丁所检查问题的描述，并包含对 Coccinelle 的引用。

作为任何静态代码分析器，Coccinelle 会产生假阳性。因此，报告必须仔细检查，补丁必须经过审查。

要启用详细消息，设置 ``--verbose=1`` 选项，例如：

.. code-block:: console

   ./scripts/coccicheck --mode=report --verbose=1

Coccinelle 并行化
**************************

默认情况下，``coccicheck`` 尝试尽可能并行运行。要更改并行度，设置 ``--jobs=<number>`` 选项。例如，要跨 4 个 CPU 运行：

.. code-block:: console

   ./scripts/coccicheck --mode=report --jobs=4

从 Coccinelle 1.0.2 起，Coccinelle 使用 Ocaml parmap 进行并行化。如果检测到对此的支持，你将受益于 parmap 并行化。

启用 parmap 时，``coccicheck`` 通过使用 ``--chunksize 1`` 参数启用动态负载均衡。这确保我们逐个向线程分配工作，从而避免大部分工作仅由少数线程完成的情况。在动态负载均衡下，如果一个线程提前完成，我们会继续向它分配更多工作。

启用 parmap 时，如果 Coccinelle 中发生错误，该错误值会被传播回来，``coccicheck`` 命令的返回值会捕获此返回值。

使用单个语义补丁
*********************************************

``--cocci`` 选项可用于检查单个语义补丁。在这种情况下，变量必须初始化为要应用的语义补丁名称。

例如：

.. code-block:: console

   ./scripts/coccicheck --mode=report --cocci=<example.cocci>

或：

.. code-block:: console

   ./scripts/coccicheck --mode=report --cocci=./path/to/<example.cocci>

控制 Coccinelle 处理的文件
***************************************************

默认情况下，会检查整个源代码树。

要将 Coccinelle 应用到特定目录，将特定目录的路径作为参数传入。

例如，要检查 ``drivers/usb/``，可以写：

.. code-block:: console

   ./scripts/coccicheck --mode=patch drivers/usb/

``report`` 模式是默认模式。你可以用上面说明的 ``--mode=<mode>`` 选项选择其他模式。

调试 Coccinelle SmPL 补丁
*********************************

使用 ``coccicheck`` 最佳，因为它在 spatch 命令行中提供与编译内核时使用的选项相匹配的包含选项。你可以通过使用 verbose 选项来了解这些选项是什么，然后手动运行 Coccinelle 并添加调试选项。

或者，你可以通过请求将 stderr 重定向到 stderr 来调试针对 SmPL 补丁运行 Coccinelle。默认情况下 stderr 被重定向到 /dev/null。如果你想捕获 stderr，可以指定 ``--debug=file.err`` 选项给 ``coccicheck``。例如：

.. code-block:: console

   rm -f cocci.err
   ./scripts/coccicheck --mode=patch --debug=cocci.err
   cat cocci.err

调试支持仅在使用 Coccinelle >= 1.0.2 时可用。

附加标志
****************

可以通过 SPFLAGS 变量向 spatch 传递附加标志。这在 Coccinelle 尊重冲突选项中最后给出的标志时有效。

.. code-block:: console

   ./scripts/coccicheck --sp-flag="--use-glimpse"

Coccinelle 也支持 idutils，但要求 coccinelle >= 1.0.6。当未指定 ID 文件时，coccinelle 假设你的 ID 数据库文件位于内核顶层的 .id-utils.index 文件中。coccinelle 附带一个脚本 scripts/idutils_index.sh，用于创建数据库：

.. code-block:: console

   mkid -i C --output .id-utils.index

如果你有另一个数据库文件名，也可以直接用该名称创建符号链接。

.. code-block:: console

   ./scripts/coccicheck --sp-flag="--use-idutils"

或者，你可以显式指定数据库文件名，例如：

.. code-block:: console

   ./scripts/coccicheck --sp-flag="--use-idutils /full-path/to/ID"

有时 coccinelle 无法识别或解析复杂宏变量，因为定义不充分。因此，要使其可解析，我们使用 ``---macro-file-builtins <headerfile.h>`` 标志显式提供复杂宏的原型。

``<headerfile.h>`` 应包含复杂宏的完整原型，spatch 引擎可以从中提取转换期间所需的类型信息。

例如：

``Z_SYSCALL_HANDLER`` 不被 coccinelle 识别。因此，我们将它的原型放在一个头文件中，例如 ``mymacros.h``。

.. code-block:: console

   $ cat mymacros.h
   #define Z_SYSCALL_HANDLER int xxx

现在我们在转换期间传入头文件 ``mymacros.h``：

.. code-block:: console

   ./scripts/coccicheck --sp-flag="---macro-file-builtins mymacros.h"

查看 ``spatch --help`` 以了解更多关于 spatch 选项的信息。

注意 ``--use-glimpse`` 和 ``--use-idutils`` 选项需要外部工具来索引代码。因此它们默认都不激活。但是，通过使用其中一个工具索引代码，并根据所使用的 cocci 文件，spatch 可以更快地处理整个代码库。

SmPL 补丁特定选项
***************************

SmPL 补丁可以对其传递给 Coccinelle 的选项有自己的要求。SmPL 补丁特定选项可以通过在 SmPL 补丁顶部提供来给出，例如：

.. code-block:: console

   // Options: --no-includes --include-headers

提议新的语义补丁
******************************

新的语义补丁可以由内核开发者提议并提交。为清晰起见，它们应组织在 ``scripts/coccinelle/`` 的子目录中。

cocci 脚本应具有以下属性：

* 脚本**必须**具有 ``report`` 模式。

* 前几行应使用 ``///`` 注释说明脚本的目的。通常，该消息在基于脚本提议补丁时用作提交日志。

示例
=======

.. code-block:: console

   /// Use ARRAY_SIZE instead of dividing sizeof array with sizeof an element

* 关于脚本的更详细信息，包括特殊情况或假阳性（如果有），可以使用 ``//#`` 注释列出。

示例
=======

.. code-block:: console

   //# This makes an effort to find cases where ARRAY_SIZE can be used such as
   //# where there is a division of sizeof the array by the sizeof its first
   //# element or by any indexed element or the element type. It replaces the
   //# division of the two sizeofs by ARRAY_SIZE.

* 置信度：它是一个用于指定脚本准确度的属性。根据观察到的假阳性数量，可以是 ``High``、``Moderate`` 或 ``Low``。

示例
=======

.. code-block:: console

   // Confidence: High

* 虚拟规则：这些是支持脚本中定义的各种模式所必需的。脚本中指定的虚拟规则应具有对应的模式处理规则。

示例
=======

.. code-block:: console

   virtual context

   @depends on context@
   type T;
   T[] E;
   @@
   (
   * (sizeof(E)/sizeof(*E))
   |
   * (sizeof(E)/sizeof(E[...]))
   |
   * (sizeof(E)/sizeof(T))
   )

``report`` 模式的详细描述
*******************************************

``report`` 生成以下格式的列表：

.. code-block:: console

   file:line:column-column: message

示例
=======

运行：

.. code-block:: console

   ./scripts/coccicheck --mode=report --cocci=scripts/coccinelle/array_size.cocci

将执行以下 SmPL 脚本部分：

.. code-block:: console

   <smpl>

   @r depends on (org || report)@
   type T;
   T[] E;
   position p;
   @@
   (
   (sizeof(E)@p /sizeof(*E))
   |
   (sizeof(E)@p /sizeof(E[...]))
   |
   (sizeof(E)@p /sizeof(T))
   )

   @script:python depends on report@
   p << r.p;
   @@

   msg="WARNING: Use ARRAY_SIZE"
   coccilib.report.print_report(p[0], msg)

   </smpl>

此 SmPL 片段在标准输出上生成条目，如下所示：

.. code-block:: console

   ext/hal/nxp/mcux/drivers/lpc/fsl_wwdt.c:66:49-50: WARNING: Use ARRAY_SIZE
   ext/hal/nxp/mcux/drivers/lpc/fsl_ctimer.c:74:53-54: WARNING: Use ARRAY_SIZE
   ext/hal/nxp/mcux/drivers/imx/fsl_dcp.c:944:45-46: WARNING: Use ARRAY_SIZE

``patch`` 模式的详细描述
******************************************

当 ``patch`` 模式可用时，它为每个识别出的问题提议修复。

示例
=======

运行：

.. code-block:: console

   ./scripts/coccicheck --mode=patch --cocci=scripts/coccinelle/misc/array_size.cocci

将执行以下 SmPL 脚本部分：

.. code-block:: console

   <smpl>

   @depends on patch@
   type T;
   T[] E;
   @@
   (
   - (sizeof(E)/sizeof(*E))
   + ARRAY_SIZE(E)
   |
   - (sizeof(E)/sizeof(E[...]))
   + ARRAY_SIZE(E)
   |
   - (sizeof(E)/sizeof(T))
   + ARRAY_SIZE(E)
   )

   </smpl>

此 SmPL 片段在标准输出上生成补丁块，如下所示：

.. code-block:: console

   diff -u -p a/ext/lib/encoding/tinycbor/src/cborvalidation.c b/ext/lib/encoding/tinycbor/src/cborvalidation.c
   --- a/ext/lib/encoding/tinycbor/src/cborvalidation.c
   +++ b/ext/lib/encoding/tinycbor/src/cborvalidation.c
   @@ -325,7 +325,7 @@ static inline CborError validate_number(
   static inline CborError validate_tag(CborValue *it, CborTag tag, int flags, int recursionLeft)
   {
     CborType type = cbor_value_get_type(it);
   -    const size_t knownTagCount = sizeof(knownTagData) / sizeof(knownTagData[0]);
   +    const size_t knownTagCount = ARRAY_SIZE(knownTagData);
      const struct KnownTagData *tagData = knownTagData;
      const struct KnownTagData * const knownTagDataEnd = knownTagData + knownTagCount;

``context`` 模式的详细描述
********************************************

``context`` 以类似 diff 的风格高亮感兴趣的行及其上下文。

.. note::
  生成的类似 diff 的输出**不是**可应用的补丁。``context`` 模式的意图是高亮重要行（用减号 ``-`` 标注）并给出一些周围的上下文行。此输出可以与 Emacs 的 diff 模式一起使用来审查代码。

示例
=======

运行：

.. code-block:: console

   ./scripts/coccicheck --mode=context --cocci=scripts/coccinelle/array_size.cocci

将执行以下 SmPL 脚本部分：

.. code-block:: console

   <smpl>

   @depends on context@
   type T;
   T[] E;
   @@
   (
   * (sizeof(E)/sizeof(*E))
   |
   * (sizeof(E)/sizeof(E[...]))
   |
   * (sizeof(E)/sizeof(T))
   )

   </smpl>

此 SmPL 片段在标准输出上生成 diff 块，如下所示：

.. code-block:: console

   diff -u -p ext/lib/encoding/tinycbor/src/cborvalidation.c /tmp/nothing/ext/lib/encoding/tinycbor/src/cborvalidation.c
   --- ext/lib/encoding/tinycbor/src/cborvalidation.c
   +++ /tmp/nothing/ext/lib/encoding/tinycbor/src/cborvalidation.c
   @@ -325,7 +325,6 @@ static inline CborError validate_number(
   static inline CborError validate_tag(CborValue *it, CborTag tag, int flags, int recursionLeft)
   {
     CborType type = cbor_value_get_type(it);
   -    const size_t knownTagCount = sizeof(knownTagData) / sizeof(knownTagData[0]);
      const struct KnownTagData *tagData = knownTagData;
      const struct KnownTagData * const knownTagDataEnd = knownTagData + knownTagCount;

``org`` 模式的详细描述
****************************************

``org`` 生成 Emacs Org 模式格式的报告。

示例
=======

运行：

.. code-block:: console

   ./scripts/coccicheck --mode=org --cocci=scripts/coccinelle/misc/array_size.cocci

将执行以下 SmPL 脚本部分：

.. code-block:: console

   <smpl>

   @r depends on (org || report)@
   type T;
   T[] E;
   position p;
   @@
   (
   (sizeof(E)@p /sizeof(*E))
   |
   (sizeof(E)@p /sizeof(E[...]))
   |
   (sizeof(E)@p /sizeof(T))
   )

   @script:python depends on org@
   p << r.p;
   @@
   coccilib.org.print_todo(p[0], "WARNING should use ARRAY_SIZE")

   </smpl>

此 SmPL 片段在标准输出上生成 Org 条目，如下所示：

.. code-block:: console

   * TODO [[view:ext/lib/encoding/tinycbor/src/cborvalidation.c::face=ovl-face1::linb=328::colb=52::cole=53][WARNING should use ARRAY_SIZE]]

Coccinelle 邮件列表
***********************

订阅 coccinelle 邮件列表：

* https://systeme.lip6.fr/mailman/listinfo/cocci

存档：

* https://lore.kernel.org/cocci/
* https://systeme.lip6.fr/pipermail/cocci/
