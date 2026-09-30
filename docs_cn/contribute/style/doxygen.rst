.. _doxygen_style:

Doxygen
Style
Guidelines
########################

The
Zephyr
Project
uses
`Doxygen`_
to
generate
API
documentation
from
source
code
comments。
This
guide
defines
the
conventions
for
documenting
Zephyr
public
APIs
consistently。

All
the
`Doxygen
commands`_
are
available
for
use
even
if
they
don't
explicitly
appear
in
this
document。

.. _Doxygen:
   https://www.doxygen.nl/
.. _Doxygen
   commands:
   https://www.doxygen.nl/manual/commands.html

To
build
and
preview
Zephyr's
Doxygen
documentation
locally
refer
to
:ref:`zephyr_doc`。

General
Rules
*************

All
:term:`public
header
files
and
their
public
API
symbols
<public
API>`
（functions、
structs、
enums、
unions、
typedefs、
macros、
and
global
variables）:

-
Must
be
fully
documented
（see
:ref:`doxygen_internals`
for
exceptions）
-
Must
belong
to
at
least
one
Doxygen
group
（see
:ref:`doxygen_groups`）

You
must
use
the
following
syntax
when
documenting
public
APIs:

-
Use
``/**``
to
start
a
block
comment
and
``*/``
to
end
it。
-
Use
``/**<``
for
trailing
comments
on
the
same
line
as
a
symbol。
-
Use
``@``
（not
``\``）
for
Doxygen
commands
（e.g.、
``@param``
not
``\param``）。
-
The
``@brief``
command
is
optional。
If
not
used
the
first
sentence
（ending
with
a
period）
is
treated
as
the
brief
description。

Constructs
meant
only
for
internal
use
must
be
hidden
from
the
public
documentation
as
described
in
:ref:`doxygen_internals`。

What
to
document
================

For
any
API
element
that
accepts、
returns、
or
stores
a
value
（function
parameters、
return
values、


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
==========

- Document parameters with ``@param`` in declaration order
- Use ``@param[out]`` for pointers the function writes to.
- Use ``@param[in,out]`` for pointers the function both reads and writes.
- You may omit direction specifiers for const pointers and scalars (implicitly input-only).

Return Values
=============

- Use ``@return <description>`` for general descriptions (e.g., boolean or computed values).
- Use ``@retval <value> <description>`` for specific, discrete return values (typically error
  codes), starting with the success case (when applicable). The ``<value>`` must be provided as the
  first word, followed by the description (e.g., ``@retval -EINVAL Invalid arguments``, not
  ``@retval -EINVAL if invalid arguments``).

  .. note::

     Since there might be multiple reasons for the same discrete value to be returned, it is
     allowed to use the same value in multiple ``@retval`` statements.

Example:

.. code-block:: c
   :caption: Examples of fully documented functions.

   /**
    * @brief Write data to the TX queue from a provided buffer
    *
    * @param dev Pointer to the device structure for the driver instance.
    * @param buf Pointer to a buffer containing the data to transmit.
    * @param size Number of bytes to write. This value has to be equal or smaller
    *        than the size of the channel's TX memory block configuration.
    *
    * @retval 0 on success.
    * @retval -EIO The interface is not in READY or RUNNING state.
    * @retval -EBUSY Returned without waiting.
    * @retval -EAGAIN Waiting period timed out.
    * @retval -ENOMEM No memory in TX slab queue.
    * @retval -EINVAL Size parameter larger than TX queue memory block.
    */
   int i2s_buf_write(const struct device *dev, void *buf, size_t size);

   /**
    * @brief Add an application callback.
    *
    * @param port Pointer to the device structure for the driver instance.
    * @param callback A valid application's callback structure pointer.
    *
    * @return 0 on success, negative errno value on failure.
    * @retval -ENOSYS Driver does not implement the operation.
    */
   int gpio_add_callback(const struct device *port, struct gpio_callback *callback);

   /**
    * @brief Helper function for converting struct sensor_value to float.
    *
    * @param val A pointer to a sensor_value struct.
    * @return The converted value.
    */
   static inline float sensor_value_to_float(const struct sensor_value *val)
   {
       return (float)val->val1 + (float)val->val2 / 1000000;
   }


Macros
******

For function-like macros, document parameters like you would for functions.

.. code-block:: c
   :caption: Example of a fully documented function-like macro.

   /**
    * @brief Get a node's (only) register block size
    *
    * Equivalent to DT_REG_SIZE_BY_IDX(node_id, 0).
    *
    * @param node_id node identifier
    * @return node's only register block's size
    */
   #define DT_REG_SIZE(node_id) DT_REG_SIZE_BY_IDX(node_id, 0)

.. _doxygen_sphinx_xrefs:

Referencing the main documentation
**********************************

API documentation can reference content from the main, Sphinx-based documentation using the
commands described below. In the generated API documentation pages, these references are rendered
as hyperlinks pointing back to the corresponding page of the main documentation.

``@kconfig{<option>}``
  Reference a Kconfig option by its full name (including the ``CONFIG_`` prefix). This is the
  Doxygen counterpart of the :rst:role:`kconfig:option` role.

  Example: ``@kconfig{CONFIG_GPIO}``

``@kconfig_regex{<regex>}``
  Reference all the Kconfig options matching a regular expression, as a link to the Kconfig search
  page with the pattern pre-filled. This is the Doxygen counterpart of the
  :rst:role:`kconfig:option-regex` role. As commas have a special meaning in Doxygen commands, they
  must be escaped with a backslash.

  Example: ``@kconfig_regex{CONFIG_SECURE_STORAGE_ITS_.*_CUSTOM}``

``@dtcompatible{<compatible>}``
  Reference a Devicetree binding by its compatible string. This is the Doxygen counterpart of the
  :rst:role:`dtcompatible` role. As commas have a special meaning in Doxygen commands, they must be
  escaped with a backslash.

  Example: ``@dtcompatible{zephyr\,input-longpress}``

``@rstref{<target>}`` or ``@rstref{<text> <target>}``
  Reference any documentation page or section by its reference label (or document name), similar to
  the Sphinx :rst:role:`ref` role. When no custom text is provided, the title of the referenced
  page or section is used as the link text.

  Example: ``@rstref{zephyr_licensing}`` or ``@rstref{the licensing page <zephyr_licensing>}``

References are checked when the documentation is built: a reference to a Kconfig option, binding,
or label that does not exist causes a documentation build warning.

.. note::

   These commands expand to plain text when the Doxygen documentation is built standalone, i.e.
   without the rest of the documentation. See :ref:`zephyr_doc` for more details.

.. _doxygen_rfc_refs:

Referencing IETF RFCs
*********************

``@rfc{<number>}`` or ``@rfc{<number>,<anchor>}``
  Reference an IETF RFC by number, optionally pointing to an anchor within it. This is the
  Doxygen counterpart of the :rst:role:`rfc` role and renders as a hyperlink to the RFC on the
  IETF Datatracker.

  The anchor is passed through verbatim, so it can target anything the Datatracker defines for
  that RFC, such as ``section-3.1``, ``appendix-B.1.2``, ``figure-2``, or ``table-1``. Which
  anchors exist depends on the RFC: figures and tables are only anchored on RFCs rendered from
  their XML source.

  Do not put whitespace after the comma: Doxygen keeps it as part of the argument, where it ends
  up inside the URL fragment. The rendered link text still looks correct, so a broken anchor is
  only noticeable when following the link.

  Example: ``@rfc{7519}``, ``@rfc{8613,section-3.1}`` or ``@rfc{8613,appendix-B.1.2}``

.. _doxygen_internals:

Hiding internal details
***********************

Use ``@cond INTERNAL_HIDDEN`` / ``@endcond`` to hide internal details from generated documentation.

You may still optionally document these internal symbols to provide a useful reference to internal
users.

.. code-block:: c
   :emphasize-lines: 7,11

   /** Timer structure.
    *
    * Opaque type for a timer object. All the fields in this structure are internal and should not
    * be accessed outside of kernel code.
    */
   struct k_timer {
       /** @cond INTERNAL_HIDDEN */

       /* ... internal members ... */

       /** @endcond */
   };

.. _doxygen_driver_backend:

Driver Backend API
******************

Driver subsystems expose a public API for applications and a "backend" API for driver implementers.

While the backend API is not intended to be used directly by applications, it still constitutes a
public contract between the subsystem and driver implementers and must therefore be properly
documented. It typically includes the driver operations structure, typedefs defining the signature
of each operation, and, in some cases, additional helper types or macros that are useful for driver
implementation.

Backend API Doxygen group
=========================

Use ``@def_driverbackendgroup`` to create a subgroup that is a child of the main API group and that
will contain all the symbols associated with the backend API. This command takes two arguments: a
human-readable name for the backend API (typically the same as the parent group) and the parent
group identifier.

.. code-block:: c

   /**
    * @def_driverbackendgroup{Haptics,haptics_interface}
    * @{
    */

   /* callback typedefs, driver ops struct, helpers ... */

   /** @} */

Driver operations typedefs
==========================

Define a ``typedef`` for each driver operation. The detailed description may reference the
corresponding public API function as it often has a similar signature.

.. code-block:: c

   /**
    * @brief Set the haptic device to stop output.
    * See haptics_stop_output() for argument description.
    */
   typedef int (*haptics_stop_output_t)(const struct device *dev);

Driver operations structure
===========================

Annotate the struct with ``@driver_ops{Name}`` (where *Name* matches the name passed to
``@def_driverbackendgroup``). For each member, use ``@driver_ops_mandatory`` or
``@driver_ops_optional`` to indicate whether the driver must implement it, and ``@copybrief`` to
inherit the brief from the public API function:

.. code-block:: c

   /**
    * @driver_ops{Haptics}
    */
   __subsystem struct haptics_driver_api {
       /**
        * @driver_ops_mandatory @copybrief haptics_start_output
        */
       haptics_start_output_t start_output;
       /**
        * @driver_ops_mandatory @copybrief haptics_stop_output
        */
       haptics_stop_output_t stop_output;
       /**
        * @driver_ops_optional @copybrief haptics_register_error_callback
        */
       haptics_register_error_callback_t register_error_callback;
   };

.. _doxygen_conditional_code:

Conditional code
****************

To ensure conditionally-compiled code appears in documentation, use either of the following
approaches:

1. Add the Kconfig macro (``CONFIG_...``) that is gating the code to the ``PREDEFINED`` list in
   :zephyr_file:`doc/zephyr.doxyfile.in`. This makes the code visible to Doxygen during
   documentation generation.

#. Alternatively, you can rely on the ``__DOXYGEN__`` macro being set to make the conditional code
   visible to Doxygen, as this macro is automatically defined by Doxygen.

.. code-block:: c
   :emphasize-lines: 3,9

   struct coap_packet {
       uint8_t *data;  /**< User allocated buffer. */
   #if defined(CONFIG_COAP_KEEP_USER_DATA) || defined(__DOXYGEN__)
       /**
        * Application-specific user data.
        * @kconfig_dep{CONFIG_COAP_KEEP_USER_DATA}
        */
       void *user_data;
   #endif
   };

.. _doxygen_kconfig_dep:

Kconfig Dependencies
====================

The ``@kconfig_dep`` command can be used to document the Kconfig option(s) that are required in
order for an API symbol to be available to the user. The command can be used with one, two or three
Kconfig options.

For example, adding ``@kconfig_dep{CONFIG_PM,CONFIG_SMP}`` to the Doxygen documentation of an API
symbol will cause the generated documentation to include a note reading: "Available only when the
following Kconfig options are enabled: ``CONFIG_PM``, ``CONFIG_SMP``.".

You can see an example of ``@kconfig_dep`` usage in the documentation of :c:struct:`coap_packet`.