.. _posix_aep:

POSIX
Application
Environment
Profiles
（AEP）
############################################

虽然
inactive
`IEEE
1003.13
2003`_
defined
一
系列
AEP
它们
inspired
`IEEE
1003.1
2017`_
的
modern
subprofiling
options。
Single
purpose
的
realtime
system
profiles
在
下面
被
listed
用于
reference
用
与
当前
POSIX
1
standard
agree
的
terms。
PSE54
当前
不
被
considered。

System
Interfaces
=================

Required
的
POSIX
:ref:`System
Interfaces<posix_system_interfaces_required>`
对
每个
Application
Environment
Profile
被
supported。

..
   figure::
   si.svg
   :align:
   center
   :scale:
   150%
   :alt:
   Required
   System
   Interfaces

   System
   Interfaces

.. _posix_aep_pse51:

Minimal
Realtime
System
Profile
（PSE51）
=======================================

*Minimal
Realtime
System
Profile*
（PSE51）
include
所有
的
:ref:`System
Interfaces<posix_system_interfaces_required>`
以及
several
additional
的
features。

..
   figure::
   aep-pse51.svg
   :align:
   center
   :scale:
   150%
   :alt:
   Minimal
   Realtime
   System
   Profile
   （PSE51）

   Minimal
   Realtime
   System
   Profile
   （PSE51）

..
   Conforming
   implementations
   shall
   define
   _POSIX_AEP_REALTIME_MINIMAL
   to
   the
   value
   200312L
