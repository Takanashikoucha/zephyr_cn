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


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
.. code-block:: console

   ./scripts/coccicheck --mode=report --cocci=<example.cocci>

or:

.. code-block:: console

   ./scripts/coccicheck --mode=report --cocci=./path/to/<example.cocci>


Controlling which files are processed by Coccinelle
***************************************************

By default the entire source tree is checked.

To apply Coccinelle to a specific directory, pass the path of specific
directory as an argument.

For example, to check ``drivers/usb/`` one may write:

.. code-block:: console

   ./scripts/coccicheck --mode=patch drivers/usb/

The ``report`` mode is the default. You can select another one with the
``--mode=<mode>`` option explained above.

Debugging Coccinelle SmPL patches
*********************************

Using ``coccicheck`` is best as it provides in the spatch command line
include options matching the options used when we compile the kernel.
You can learn what these options are by using verbose option, you could
then manually run Coccinelle with debug options added.

Alternatively you can debug running Coccinelle against SmPL patches
by asking for stderr to be redirected to stderr, by default stderr
is redirected to /dev/null, if you'd like to capture stderr you
can specify the ``--debug=file.err`` option to ``coccicheck``. For
instance:

.. code-block:: console

   rm -f cocci.err
   ./scripts/coccicheck --mode=patch --debug=cocci.err
   cat cocci.err

Debugging support is only supported when using Coccinelle >= 1.0.2.

Additional Flags
****************

Additional flags can be passed to spatch through the SPFLAGS
variable. This works as Coccinelle respects the last flags
given to it when options are in conflict.

.. code-block:: console

   ./scripts/coccicheck --sp-flag="--use-glimpse"

Coccinelle supports idutils as well but requires coccinelle >= 1.0.6.
When no ID file is specified coccinelle assumes your ID database file
is in the file .id-utils.index on the top level of the kernel, coccinelle
carries a script scripts/idutils_index.sh which creates the database with:

.. code-block:: console

   mkid -i C --output .id-utils.index

If you have another database filename you can also just symlink with this
name.

.. code-block:: console

   ./scripts/coccicheck --sp-flag="--use-idutils"

Alternatively you can specify the database filename explicitly, for
instance:

.. code-block:: console

   ./scripts/coccicheck --sp-flag="--use-idutils /full-path/to/ID"

Sometimes coccinelle doesn't recognize or parse complex macro variables
due to insufficient definition. Therefore, to make it parsable we
explicitly provide the prototype of the complex macro using the
``---macro-file-builtins <headerfile.h>`` flag.

The ``<headerfile.h>`` should contain the complete prototype of
the complex macro from which spatch engine can extract the type
information required during transformation.

For example:

``Z_SYSCALL_HANDLER`` is not recognized by coccinelle. Therefore, we
put its prototype in a header file, say for example ``mymacros.h``.

.. code-block:: console

   $ cat mymacros.h
   #define Z_SYSCALL_HANDLER int xxx

Now we pass the header file ``mymacros.h`` during transformation:

.. code-block:: console

   ./scripts/coccicheck --sp-flag="---macro-file-builtins mymacros.h"

See ``spatch --help`` to learn more about spatch options.

Note that the ``--use-glimpse`` and ``--use-idutils`` options
require external tools for indexing the code. None of them is
thus active by default. However, by indexing the code with
one of these tools, and according to the cocci file used,
spatch could proceed the entire code base more quickly.


SmPL patch specific options
***************************

SmPL patches can have their own requirements for options passed
to Coccinelle. SmPL patch specific options can be provided by
providing them at the top of the SmPL patch, for instance:

.. code-block:: console

   // Options: --no-includes --include-headers

Proposing new semantic patches
******************************

New semantic patches can be proposed and submitted by kernel
developers. For sake of clarity, they should be organized in the
sub-directories of ``scripts/coccinelle/``.

The cocci script should have the following properties:

* The script **must** have ``report`` mode.

* The first few lines should state the purpose of the script
  using ``///`` comments . Usually, this message would be used as the
  commit log when proposing a patch based on the script.

Example
=======

.. code-block:: console

   /// Use ARRAY_SIZE instead of dividing sizeof array with sizeof an element

* A more detailed information about the script with exceptional cases
  or false positives (if any) can be listed using ``//#`` comments.

Example
=======

.. code-block:: console

   //# This makes an effort to find cases where ARRAY_SIZE can be used such as
   //# where there is a division of sizeof the array by the sizeof its first
   //# element or by any indexed element or the element type. It replaces the
   //# division of the two sizeofs by ARRAY_SIZE.

* Confidence: It is a property defined to specify the accuracy level of
  the script. It can be either ``High``, ``Moderate`` or ``Low`` depending
  upon the number of false positives observed.

Example
=======

.. code-block:: console

   // Confidence: High

* Virtual rules: These are required to support the various modes framed
  in the script. The virtual rule specified in the script should have
  the corresponding mode handling rule.

Example
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

Detailed description of the ``report`` mode
*******************************************

``report`` generates a list in the following format:

.. code-block:: console

   file:line:column-column: message

Example
=======

Running:

.. code-block:: console

   ./scripts/coccicheck --mode=report --cocci=scripts/coccinelle/array_size.cocci

will execute the following part of the SmPL script:

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

This SmPL excerpt generates entries on the standard output, as
illustrated below:

.. code-block:: console

   ext/hal/nxp/mcux/drivers/lpc/fsl_wwdt.c:66:49-50: WARNING: Use ARRAY_SIZE
   ext/hal/nxp/mcux/drivers/lpc/fsl_ctimer.c:74:53-54: WARNING: Use ARRAY_SIZE
   ext/hal/nxp/mcux/drivers/imx/fsl_dcp.c:944:45-46: WARNING: Use ARRAY_SIZE


Detailed description of the ``patch`` mode
******************************************

When the ``patch`` mode is available, it proposes a fix for each problem
identified.

Example
=======

Running:

.. code-block:: console

   ./scripts/coccicheck --mode=patch --cocci=scripts/coccinelle/misc/array_size.cocci

will execute the following part of the SmPL script:

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

This SmPL excerpt generates patch hunks on the standard output, as
illustrated below:

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

Detailed description of the ``context`` mode
********************************************

``context`` highlights lines of interest and their context
in a diff-like style.

.. note::
 The diff-like output generated is NOT an applicable patch. The
 intent of the ``context`` mode is to highlight the important lines
 (annotated with minus, ``-``) and gives some surrounding context
 lines around. This output can be used with the diff mode of
 Emacs to review the code.

Example
=======

Running:

.. code-block:: console

   ./scripts/coccicheck --mode=context --cocci=scripts/coccinelle/array_size.cocci

will execute the following part of the SmPL script:

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

This SmPL excerpt generates diff hunks on the standard output, as
illustrated below:

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

Detailed description of the ``org`` mode
****************************************

``org`` generates a report in the Org mode format of Emacs.

Example
=======

Running:

.. code-block:: console

   ./scripts/coccicheck --mode=org --cocci=scripts/coccinelle/misc/array_size.cocci

will execute the following part of the SmPL script:

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

This SmPL excerpt generates Org entries on the standard output, as
illustrated below:

.. code-block:: console

   * TODO [[view:ext/lib/encoding/tinycbor/src/cborvalidation.c::face=ovl-face1::linb=328::colb=52::cole=53][WARNING should use ARRAY_SIZE]]

Coccinelle Mailing List
***********************

Subscribe to the coccinelle mailing list:

* https://systeme.lip6.fr/mailman/listinfo/cocci

Archives:

* https://lore.kernel.org/cocci/
* https://systeme.lip6.fr/pipermail/cocci/