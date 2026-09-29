.. _getting_started_with_safety_requirements:

Getting
started
with
Requirements
Management
############################################

Zephyr's
requirements
management
is
powered
by
`StrictDoc
<https://github.com/strictdoc-project/strictdoc>`_
a
lightweight
tool
for
writing、
organizing、
and
publishing
structured
requirements。
This
section
explains
how
to
set
up
and
use
the
toolchain
provided
in
the
`reqmgmt
<https://github.com/zephyrproject-rtos/reqmgmt>`_
repository。

Overview
*********

The
``reqmgmt``
repository
is
Zephyr's
official
requirements
workspace。
It
supports:

-
Authoring
system
and
software
requirements
-
Linking
requirements
to
verification
artifacts
-
Generating
browsable
HTML
documentation
-
Running
a
local
web
interface
for
editing
and
review

Installation
************

StrictDoc
requires
Python
3.7
or
newer。
To
install
（you
might
need
to
use
pip3
instead
of
pip）:

.. code-block::
   bash

   pip
   install
   strictdoc

Clone
the
Zephyr
requirements
repository:

.. code-block::
   bash

   git
   clone
   https://github.com/zephyrproject-rtos/reqmgmt
   cd
   reqmgmt

Usage
*****

To
export
the
requirements
to
HTML:

.. code-block::
   bash
