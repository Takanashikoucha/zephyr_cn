.. _zephyr_doc:

Documentation
Generation
########################

These
instructions
will
walk
you
through
generating
the
Zephyr
Project's
documentation
on
your
local
system
using
the
same
documentation
sources
as
we
use
to
create
the
online
documentation
found
at
https://docs.zephyrproject.org

.. _documentation-overview:

Documentation
overview
**********************

Zephyr
Project
content
is
written
using
the
reStructuredText
markup
language
（.rst
file
extension）
with
Sphinx
extensions
and
processed
using
Sphinx
to
create
a
formatted
stand
alone
website。
Developers
can
view
this
content
either
in
its
raw
form
as
.rst
markup
files
or
you
can
generate
the
HTML
content
and
view
it
with
a
web
browser
directly
on
your
workstation。
This
same
.rst
content
is
also
fed
into
the
Zephyr
Project's
public
website
documentation
area
（with
a
different
theme
applied）。

You
can
read
details
about
`reStructuredText`_
and
`Sphinx`_
from
their
respective
websites。

The
project's
documentation
contains
the
following
items:

*
ReStructuredText
source
files
used
to
generate
documentation
found
at
the
https://docs.zephyrproject.org
website。
Most
of
the
reStructuredText
sources
are
found
in
the
``/doc``
directory
but
others
are
stored
within
the
code
source
tree
near
their
specific
component
（such
as
``/samples``
and
``/boards``）

*
Doxygen
generated
material
used
to
create
all
API
specific
documents
also
found
at
https://docs.zephyrproject.org

*
Script
generated
material
for
kernel
configuration
options
based
on
Kconfig
files
found
in
the
source
code
tree


.. note::

   以下为原文（待翻译）

if generated, the PDF file is available at ``doc/_build/latex/zephyr.pdf``.

If you want to build the documentation from scratch just delete the contents
of the build folder and run ``cmake`` and then ``ninja`` again.

.. note::

   If you add or remove a file from the documentation, you need to re-run CMake.

On Unix platforms a convenience :zephyr_file:`doc/Makefile` can be used to
build the documentation directly from there:

.. code-block:: console

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output
   make html

   # To generate PDF output
   make pdf

Developer-mode Document Building
********************************

When making and testing major changes to the documentation, we provide an option
to temporarily stub-out the auto-generated Devicetree bindings documentation so
the doc build process runs faster.

To enable this mode, set the following option when invoking cmake::

   -DDT_TURBO_MODE=1

Another step that typically takes a long time is the generation of the list of
supported features for each board. This can be disabled by setting the following
option when invoking cmake::

   -DHW_FEATURES_TURBO_MODE=1

Invoking :command:`make` with the following target will build the documentation
without either of the aforementioned features::

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output without detailed Devicetree bindings documentation
   # and supported features index
   make html-fast

For even faster iteration when working on narrative pages, additional
``SKIP_*`` options allow skipping entire categories of auto-generated content:

``SKIP_DOXYGEN``
   Skip running Doxygen and building the C API reference.

``SKIP_KCONFIG``
   Skip generating the Kconfig option reference and its search page.

``SKIP_EXTERNAL_CONTENT``
   Skip copying in the board, sample, and snippet pages that are maintained
   outside of the ``doc/`` folder (i.e. the contents of the
   :zephyr_file:`boards`, :zephyr_file:`samples`, and :zephyr_file:`snippets`
   folders).

Each option can be enabled individually::

   make html SKIP_DOXYGEN=1

The :command:`make html-minimal` target combines all of them on top of
``html-fast``, making it the fastest way to preview a change to a narrative
page::

   make html-minimal

.. warning::

   Content that a skipped generator would have produced is replaced with a
   placeholder, cross-references to it render as plain text, and the related
   warnings are suppressed. A build using any ``SKIP_*`` option is therefore
   only suitable for a local preview: it cannot be used to validate
   cross-references, and its output must not be published.

When working with documentation for boards from a specific vendor, it is also
possible to limit generation of the list of supported features to subset of board
vendors. This can be done by setting the following option when invoking cmake::

   -DHW_FEATURES_VENDOR_FILTER=vendor1,vendor2

This option can also be used with the :command:`make` wrapper::

   cd ~/zephyrproject/zephyr/doc

   # To generate HTML output with supported features limited to a subset of vendors
   make html HW_FEATURES_VENDOR_FILTER=vendor1,vendor2

Viewing generated documentation locally
***************************************

The generated HTML documentation can be hosted locally with python for viewing
with a web browser:

.. code-block:: console

   $ python3 -m http.server -d _build/html

.. note::

   WSL2 users may need to explicitly bind the address to ``127.0.0.1`` in order
   to be accessible from the host machine:

   .. code-block:: console

      $ python3 -m http.server -d _build/html --bind 127.0.0.1

Alternatively, the documentation can be built with the ``make html-live``
(or ``make html-live-fast``) command, which will build the documentation, host
it locally, and watch the documentation directory for changes. When changes are
observed, it will automatically rebuild the documentation and refresh the hosted
files.

Building the Doxygen documentation standalone
*********************************************

The ``doxygen`` build target can be used to only build the Doxygen (API) documentation, which is
much faster than building the full documentation set::

   cd ~/zephyrproject/zephyr/doc
   make doxygen

The output can be found in ``_build/doxygen/html``.

The ``doxygen-xml`` target builds the same documentation with only the XML output enabled, in
``_build/doxygen-xml/xml``.

In the regular documentation build, references made from Doxygen comments to the main
documentation (e.g. ``@kconfig{}``, ``@dtcompatible{}`` or ``@rstref{}``, see
:ref:`doxygen_sphinx_xrefs`) are automatically resolved into hyperlinks. In a standalone Doxygen
build, they are left as plain text since the rest of the documentation is not available.

Linking external Doxygen projects against Zephyr
************************************************

External projects that build upon Zephyr functionality and wish to refer to
Zephyr documentation in Doxygen (through the use of @ref), can utilize the
tag file exported at `zephyr.tag <../../doxygen/html/zephyr.tag>`_

Once downloaded, the tag file can be used in a custom ``doxyfile.in`` as follows::

   TAGFILES = "/path/to/zephyr.tag=https://docs.zephyrproject.org/latest/doxygen/html/"

For additional information refer to `Doxygen External Documentation`_.


.. _reStructuredText: https://sphinx-doc.org/rest.html
.. _Sphinx: https://sphinx-doc.org/
.. _Windows Python Path: https://docs.python.org/3/using/windows.html#finding-the-python-executable
.. _Doxygen External Documentation: https://www.doxygen.nl/manual/external.html
