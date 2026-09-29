:orphan:

.. _zephyr_3.2:

Zephyr
3.2.0
############

我们
pleased
to
announce
Zephyr
version
3.2.0
的
release。

这
个
release
的
Major
enhancements
包括：

*
Introduced
:ref:`sysbuild`。
*
Added
support
for
:ref:`bin-blobs`
（also
see
:ref:`west-blobs`）。
*
Added
support
for
Picolibc
（see
:kconfig:option:`CONFIG_PICOLIBC`）。
*
Converted
所有
supported
的
boards
from
``pinmux``
to
:ref:`pinctrl-guide`。
*
Initial
的
support
for
:ref:`i3c_api`
controllers。
*
Support
for
:ref:`W1
api<w1_api>`。
*
Improved
的
access
to
Devicetree
compatibles
from
Kconfig
（new
generated
的
``DTS_HAS_..._ENABLED``
configs）。

以下
sections
provide
detailed
的
lists
of
changes
by
component。

Security
Vulnerability
Related
******************************

以下
的
CVEs
被
这
个
release
addressed:

More
detailed
的
information
可以
found
在:
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

*
CVE
2022
2993:
Under
embargo
until
2022
11
03

*
CVE
2022
2741:
Under
embargo
until
2022
10
14

API
Changes
***********

Changes
in
this
release
=======================
