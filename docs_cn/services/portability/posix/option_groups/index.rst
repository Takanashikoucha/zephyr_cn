POSIX
Option
and
Option
Group
Details
#####################################

.. _posix_option_groups:

POSIX
Option
Groups
==================

.. _posix_option_group_barriers:

POSIX_BARRIERS
++++++++++++++++

用
:kconfig:option:`CONFIG_POSIX_BARRIERS`
enable
这
个
option
group。

..
   csv-table::
   POSIX_BARRIERS
   :header:
   API,
   Supported
   :widths:
   50,10

   pthread_barrier_destroy(),yes
   pthread_barrier_init(),yes
   pthread_barrier_wait(),yes
   pthread_barrierattr_destroy(),yes
   pthread_barrierattr_init(),yes

.. _posix_option_group_c_lang_jump:

POSIX_C_LANG_JUMP
+++++++++++++++++

``POSIX_C_LANG_JUMP``
Option
Group
被
included
在
ISO
C
standard
中。

.. note::
   当
   use
   Newlib、
   Picolibc、
   或
   其他
   与
   ISO
   C
   Standard
   conforming
   的
   C
   libraries
   时
   ``POSIX_C_LANG_JUMP``
   Option
   Group
   被
   considered
   supported。

..
   csv-table::
   POSIX_C_LANG_JUMP
   :header:
   API,
   Supported
   :widths:
   50,10
