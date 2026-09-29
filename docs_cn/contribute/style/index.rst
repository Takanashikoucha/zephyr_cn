.. _coding_style:


Coding
Style
Guidelines
#######################

.. toctree::
   :maxdepth:
   1

   naming.rst
   code.rst
   doxygen.rst
   cmake.rst
   devicetree.rst
   kconfig.rst
   python.rst


Style
Tools
***********

Checkpatch
==========

The
Linux
kernel
GPL
licensed
tool
``checkpatch``
is
used
to
check
coding
style
conformity。

.. note::
   checkpatch
   does
   not
   currently
   run
   on
   Windows。

Checkpatch
is
available
in
the
scripts
directory。
To
invoke
it
when
committing
code
make
the
file
*$ZEPHYR_BASE/.git/hooks/pre
commit*
executable
and
edit
it
to
contain:

.. code-block::
   bash

   #!/bin/sh
   set
   -e
   exec
   exec
   git
   diff
   --cached
   |
   ${ZEPHYR_BASE}/scripts/checkpatch.pl
   -
