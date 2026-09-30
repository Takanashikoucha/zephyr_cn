.. _project_roles:

TSC
Project
Roles
*****************

Project
Roles
#############

You
can
participate
in
the
Zephyr
Project
as
a
*Contributor*、
*Collaborator*、
or
*Maintainer*。

**Contributor**:
Any
community
member
who
contributes
code、
documentation、
or
other
assets
to
the
project。

**Collaborator**:
An
active
Contributor
who
is
involved
in
one
or
more
areas
of
the
project。

**Maintainer**:
A
lead
Collaborator
responsible
for
a
specific
area
or
subsystem
within
the
project。
Maintainers
also
serve
as
representatives
for
their
area
on
the
Technical
Steering
Committee
（TSC）
as
needed。

Areas
in
this
context
refer
to
specific
subsystems、
components、
or
modules
within
the
Zephyr
Project
codebase。
Examples
of
areas
include
but
are
not
limited
to
networking、
file
systems、
device
drivers、
architecture
support、
and
board
support
packages
（boards
and
SoC
definitions）。

Areas
in
the
project
should
at
least
have
one
Maintainer
and
may
have
multiple
Collaborators。
Depending
on
the
size
and
complexity
of
the
area
there
may
be
multiple
Maintainers
as
well
however
the
number
of
maintainers
should
be
kept
to
a
practical
minimum
to
ensure
effective
management
and
decision
making。

.. _contributor:

Contributor
+++++++++++

A
*Contributor*
is
a
developer
who
wishes
to
contribute
to
the
project
at
any
level。

Contributors
are
granted
the
following
rights
and
responsibilities:

*
Right
to
contribute
code、
documentation、
translations、
artwork、
etc。


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
* Right to close any stale changes after <N> months of no activity
* Responsibility to take directions from the TSC and follow them.
* Responsibility to coordinate code merges with maintainers.
* Responsibility to merge all contributions regardless of their
  origin and area if they have been approved by the respective
  maintainers and follow the merge criteria of a change.
* Responsibility to keep the Zephyr code base in a working and passing state
  (as per CI)

Joining the Release Engineering team

* Maintainers highly involved in the project may be nominated
  by a TSC voting member to join the Release Engineering team.
  Nominees may become members of the team by approval of the
  existing TSC voting members.
* To ensure a functional Release Engineering team the TSC shall
  periodically review the team’s followed processes,
  the appropriate size, and the membership
  composition (ensure, for example, that team members are
  geographically distributed across multiple locations and
  time-zones).


Release Manager
+++++++++++++++

A *Maintainer* responsible for driving a specific release to
completion following the milestones and the roadmap of the
project for this specific release.

* TSC has to approve a release manager.

A Release Manager is a member of the Release Engineering team and has
the rights and responsibilities of that team in addition to
the following:

* Right to manage and coordinate all code merges after the
  code freeze milestone (M3, see `program management overview <https://wiki.zephyrproject.org/Program-Management>`_.)
* Responsibility to drive and coordinate the triaging process
  for the release
* Responsibility to create the release notes of the release
* Responsibility to notify all stakeholders of the project,
  including the community at large about the status of the
  release in a timely manner.
* Responsibility to coordinate with QA and validation and
  verify changes either directly or through QA before major
  changes and major milestones.

Roles / Permissions
+++++++++++++++++++

.. table:: Project Roles vs GitHub Permissions
    :widths: 20 20 10 10 10 10 10
    :align: center

    ================ =================== =========== ================ =========== =========== ============
          ..             ..               **Admin**  **Merge Rights**   Member      Owner     Collaborator
    ---------------- ------------------- ----------- ---------------- ----------- ----------- ------------
    Main Roles       Contributor                                                                 x
    ---------------- ------------------- ----------- ---------------- ----------- ----------- ------------
        ..           Collaborator                                       x
    ---------------- ------------------- ----------- ---------------- ----------- ----------- ------------
        ..           Maintainer                                         x
    Supportive Roles QA/Validation                                      x                        x
        ..           DevOps                   **x**
        ..           System Admin             **x**                                      x
        ..           Release Engineering                 **x**          x

    ================ =================== =========== ================ =========== =========== ============

Role Retirement
###############

Individuals approved by the TSC or representatives of the TSC to fill a project
role who are no longer actively fulfilling the rights and responsibilities
associated with their role may be requested by the TSC to retire from that role.

Retirements of inactive maintainers or collaborators are reflected by removing the
individual's GitHub user name from the relevant sections of the
:ref:`maintainers_file` in the Zephyr repository and may be initiated by the
TSC, representatives of the TSC or by the individuals themselves. Maintainers
may also initiate the removal of inactive collaborators in their area.

A maintainer may object to being retired, and request a decision by the TSC.

.. _maintainers_file:

MAINTAINERS File
################

The following guidelines apply to the structure, scope, and maintenance of the
MAINTAINERS file.

- The MAINTAINERS file shall have designated individuals responsible for the
  accuracy, structure, and upkeep of the file, in accordance with the Zephyr
  Project Charter. These individuals shall be appointed by the TSC.
- The granularity of maintainership should remain practical and manageable.
- The TSC, in collaboration with existing maintainers and contributors, should
  actively identify and encourage contributors to step up as maintainers for
  orphaned areas of the codebase and should facilitate the assignment of
  maintainers to those components.
- Unmaintained areas shall be clearly marked as such in the MAINTAINERS file.
- Updates to the MAINTAINERS file should:

  - Generally be included as standalone commits when introducing new files or
    directories.
  - Major changes, including the addition of new areas and new maintainers,
    should be submitted as separate pull requests, requiring approval by the
    MAINTAINERS file’s maintainers. Such activities might be the result of splitting
    existing large areas into smaller ones or merging smaller areas.

Guidelines for assigning maintainers to different areas of the codebase:

Architectures, core components, subsystems, samples, and tests:
  Each area shall have an explicitly assigned maintainer.

Boards (including related samples and tests) and SoCs (including DTS definitions)
  Each board and SoC should have an explicitly assigned maintainer through a
  platform area covering the boards, SoCs, and their related components and
  drivers.

Drivers / Backends
  The area of the API level shall have a maintainer and specific driver
  implementations or backends shall also be covered through a platform area covering
  the driver implementation. The driver area or the subsystem maintainers are
  assigned in case of changes to driver instances or backends.

.. _Zephyr Contributor Badge form: https://forms.gle/oCw9iAPLhUsHTapc8