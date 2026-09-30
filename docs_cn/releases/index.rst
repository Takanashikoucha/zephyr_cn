.. _zephyr_release_notes:

Releases
########

Zephyr
被
distributed
作为
source
code
和
build
scripts
而
不
是
binary
image。
Use
:ref:`west`
:ref:`get
the
code
<get_the_code>`
用于
specific
的
version
并
see
`GitHub
repository`_
获取
tagged
releases
的
full
history。

当前
和
past
releases
的
technical
documentation
available
在
https://docs.zephyrproject.org/
（use
version
selector
select
你
的
release
of
interest）。

.. _supported_releases:

Supported
Releases
******************

下面
的
table
list
所有
actively
supported
的
releases。
对
most
users
recommended
的
starting
point
是
**latest
stable
release**
或
**current
LTS
release**。

.. toctree::
   :hidden:
   :maxdepth:
   1
   :glob:
   :reversed:

   release-notes-3.7
   release-notes-4.[3-5]
   migration-guide-3.7
   migration-guide-4.[3-5]

.. note::
   |
   Next
   planned
   的
   release
   是
   **Zephyr
   4.5**
   targeted
   for
   **October
   2026**。
   |
   Associated
   的
   :doc:`Release
   Notes
   <release-notes-4.5>`
   和
   :doc:`Migration
   Guide
   <migration-guide-4.5>`
   的
   working
   drafts
   已
   available。

.. list-table::
   :header-rows:
   1


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
| 4.6     | April 2027        | LTS4                |
+---------+-------------------+---------------------+
| 5.0     | October 2027      | Start of 5.x cycle  |
+---------+-------------------+---------------------+
| 5.1     | April 2028        |                     |
+---------+-------------------+---------------------+
| 5.2     | October 2028      |                     |
+---------+-------------------+---------------------+
| 5.3     | April 2029        |                     |
+---------+-------------------+---------------------+
| 5.4     | October 2029      | LTS5                |
+---------+-------------------+---------------------+

Starting with the 5.x release cycle, all releases will follow the new six-month
cadence from the beginning.


Security Fixes
==============

Each security issue fixed within Zephyr is backported or submitted to the
following releases:

- Currently supported Long Term Support (LTS) release.

- The most recent two releases.

For more information, see  :ref:`Security Vulnerability Reporting <reporting>`.

Release documentation
*********************

Each release includes two companion documents:

- Release notes summarize changes made across the project during the release cycle.
- Migration guides describe changes that require action when moving an application from one major
  release to the next.

Release Notes
=============

Release notes contain a list of changes that have been made to the different
areas of the project during the development cycle of the release.
Changes that require the user to modify their own application to support the new
release may be mentioned in the release notes, but the details regarding *what*
needs to be changed are to be detailed in the release's migration guide.

Updates to the release notes post release cycle is permitted but limited to
style, typographical fixes and to upmerge the notes from maintenance release
branches with the sole purpose of keeping the latest documentation consistent
with the changes in the project.

Migration Guides
================

Zephyr provides migration guides for all major releases, in order to assist
users transition from the previous release.

As mentioned in the previous section, changes in the code that require an action
(i.e. a modification of the source code or configuration files) on the part of
the user in order to keep the existing behavior of their application belong in
in the migration guide. This includes:

- Breaking API changes
- Deprecations
- Devicetree or Kconfig changes that affect the user (changes to defaults,
  renames, etc)
- Treewide changes that have an effect (e.g. changing the include path or
  defaulting to a different C standard library)
- Anything else that can affect the compilation or runtime behavior of an
  existing application

Each entry in the migration guide must include a brief explanation of the change
as well as refer to the Pull Request that introduced it, in order for the user
to be able to understand the context of the change.

.. _`GitHub repository`: https://github.com/zephyrproject-rtos/zephyr
.. _`GitHub tagged releases`: https://github.com/zephyrproject-rtos/zephyr/tags
.. _`Zephyr 1.14.1 (LTS1)`: https://docs.zephyrproject.org/1.14.1/
.. _`Zephyr 2.7.6 (LTS2)`: https://docs.zephyrproject.org/2.7.6/
.. _`Zephyr 3.7.0 (LTS3)`: https://docs.zephyrproject.org/3.7.0/
.. _`Zephyr 4.3.0`: https://docs.zephyrproject.org/4.3.0/
.. _`Zephyr 4.4.0`: https://docs.zephyrproject.org/4.4.0/