.. _board_porting_guide:

Board
Porting
Guide
###################

要
为
新
的
:term:`board`
添加
Zephyr
支持
你
至少
需要
一
个
*board
directory*
带
各种
files。
Board
directory
中
的
files
继承
至少
一
个
SoC
和
其
所有
features
的
支持。
因此
Zephyr
必须
也
支持
你的
:term:`SoC`。

.. _hw_model_v2:

Transition
to
the
current
hardware
model
****************************************

在
Zephyr
3.6.0
发布
后
不久
新
的
hardware
model
被
引入
Zephyr。
这
个
新
model
overhaul
了
SoCs
和
boards
被
命名
和
defined
的
方式
并
添加
对
多年来
被
识别
为
重要
的
features
的
支持。
其中
包括：

- 支持
  multi
  core、
  multi
  arch
  AMP
  （Asymmetrical
  Multi
  Processing）
  SoCs
- 支持
  multi
  SoC
  boards
- 支持
  在
  Zephyr
  build
  system
  外
  复用
  SoC
  和
  board
  Kconfig
  trees
- 支持
  用
  :ref:`sysbuild`
  的
  advanced
  use
  cases
- 移除
  所有
  现有
  的
  arbitrary
  和
  inconsistent
  的
  Kconfig
  和
  folder
  names
  使用

这
页
上
的
所有
documentation
都
参考
当前
的
hardware
model。
请
参考
Zephyr
v3.6.0
（或
更早
）
的
documentation
获取
之前
的
现在
已
obsolete
的
hardware
model
的
信息。

关于
新
model
背后
的
rationale、
development
和
concepts
的
更多
信息
可以
在
:github:`original
issue
<51831>`、
:github:`original
Pull
Request
<50305>`
以及
关于
引入
的
完整
changes
set
的
`hardware
model
v2
commit`_
中
找到。

新
hardware
model
的
一些
non
critical
的
features、
enhancements
和
improvements
仍
在
development
中。
参考
:github:`hardware
model
v2
enhancements
issue
<69546>`
获取
完整
列表。


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
.. note::

  The board directory name does not need to match the name of the board.
  Multiple boards can even be defined in one directory.

Your board directory should look like this:

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.yml
   ├── board.cmake
   ├── CMakeLists.txt
   ├── doc
   │   ├── plank.webp
   │   └── index.rst
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   ├── plank_<qualifiers>_defconfig
   ├── plank_<qualifiers>.dts
   └── plank_<qualifiers>.yaml

Replace ``plank`` with your board's name, of course.

The mandatory files are:

#. :file:`board.yml`: a YAML file describing the high-level meta data of the
   boards such as the boards names, their SoCs, and variants.
   CPU clusters for multi-core SoCs are not described in this file as they are
   inherited from the SoC's YAML description.

#. :file:`plank_<qualifiers>.dts`: a hardware description
   in :ref:`devicetree <dt-guide>` format. This declares your SoC, connectors,
   and any other hardware components such as LEDs, buttons, sensors, or
   communication peripherals (USB, Bluetooth controller, etc).

#. :file:`Kconfig.plank`: the base software configuration for selecting SoC and
   other board and SoC related settings. Kconfig settings outside of the board
   and SoC tree must not be selected. To select general Zephyr Kconfig settings
   the :file:`Kconfig` file must be used.


The optional files are:

- :file:`Kconfig`, :file:`Kconfig.defconfig` software configuration in
  :ref:`kconfig` formats. This provides default settings for software features
  and peripheral drivers.
- :file:`plank_defconfig` and :file:`plank_<qualifiers>_defconfig`: software
  configuration in Kconfig ``.conf`` format.
- :file:`board.cmake`: used for :ref:`flash-and-debug-support`
- :file:`CMakeLists.txt`: if you need to add additional source files to
  your build.
- :file:`doc/index.rst`, :file:`doc/plank.webp`: documentation for and a picture
  of your board. You only need this if you're :ref:`contributing-your-board` to
  Zephyr.
- :file:`plank_<qualifiers>.yaml`: a YAML file with miscellaneous metadata used
  by the :ref:`twister_script`.

Board qualifiers of the form ``<soc>/<cpucluster>/<variant>`` are normalized so
that ``/`` is replaced with ``_`` when used for filenames, for example:
``soc1/foo`` becomes ``soc1_foo`` when used in filenames.

.. _board_description:

Write your board YAML
*********************

The board YAML file describes the board at a high level.
This includes the SoC, board variants, and board revisions.

Detailed configurations, such as hardware description and configuration are done
in devicetree and Kconfig.

The skeleton of the board YAML file is:

.. code-block:: yaml

   board:
     name: <board-name>
     full_name: <board-full-name>
     vendor: <board-vendor>
     revision:
       format: <major.minor.patch|letter|number|custom>
       default: <default-revision-value>
       exact: <true|false>
       revisions:
       - name: <revA>
       - name: <revB>
         ...
     socs:
     - name: <soc-1>
       variants:
       - name: <variant-1>
       - name: <variant-2>
         variants:
         - name: <sub-variant-2-1>
           ...
     - name: <soc-2>
       ...

It is possible to have multiple boards located in the board folder.
If multiple boards are placed in the same board folder, then the file
:file:`board.yml` must describe those in a list as:

.. code-block:: yaml

   boards:
   - name: <board-name-1>
     vendor: <board-vendor>
     full_name: <board-full-name>
     ...
   - name: <board-name-2>
     vendor: <board-vendor>
     full_name: <board-full-name>
     ...
   ...


.. _default_board_configuration:

Write your devicetree
*********************

The devicetree file :file:`boards/<vendor>/plank/plank_<qualifiers>.dts` describes your board
hardware in the Devicetree Source (DTS) format (as usual, change ``plank`` to
your board's name). If you're new to devicetree, see :ref:`devicetree-intro`.

In general, :file:`plank_<qualifiers>.dts` should look like this:

.. code-block:: devicetree

   /dts-v1/;
   #include <your_soc_vendor/your_soc.dtsi>

   / {
           model = "A human readable name";
           compatible = "yourcompany,plank";

           chosen {
                   zephyr,console = &your_uart_console;
                   zephyr,sram = &your_memory_node;
                   /* other chosen settings  for your hardware */
           };

           /*
            * Your board-specific hardware: buttons, LEDs, sensors, etc.
            */

           leds {
                   compatible = "gpio-leds";
                   led0: led_0 {
                           gpios = </* GPIO your LED is hooked up to */>;
                           label = "LED 0";
                   };
                   /* ... other LEDs ... */
           };

           buttons {
                   compatible = "gpio-keys";
                   /* ... your button definitions ... */
           };

           /* These aliases are provided for compatibility with samples */
           aliases {
                   led0 = &led0; /* now you support the blinky sample! */
                   /* other aliases go here */
           };
   };

   &some_peripheral_you_want_to_enable { /* like a GPIO or SPI controller */
           status = "okay";
   };

   &another_peripheral_you_want {
           status = "okay";
   };

In the case a board has only a single SoC, without any board variants then the dts file can be
named :file:`<plank>.dts` instead, however this is not recommended due to the file silently be
unused if a variant or other SoC is added to the board.

If you're in a hurry, simple hardware can usually be supported by copy/paste
followed by trial and error. If you want to understand details, you will need
to read the rest of the devicetree documentation and the devicetree
specification.

.. _dt_k6x_example:

Example: FRDM-K64F and Hexiwear K64
===================================

.. Give the filenames instead of the full paths below, as it's easier to read.
   The cramped 'foo.dts<path>' style avoids extra spaces before commas.

This section contains concrete examples related to writing your board's
devicetree.

The FRDM-K64F and Hexiwear K64 board devicetrees are defined in
:zephyr_file:`frdm_k64fs.dts <boards/nxp/frdm_k64f/frdm_k64f.dts>` and
:zephyr_file:`hexiwear_k64.dts <boards/mikroe/hexiwear/hexiwear_mk64f12.dts>`
respectively. Both boards have NXP SoCs from the same Kinetis SoC family, the
K6X.

Common devicetree definitions for K6X are stored in :zephyr_file:`nxp_k6x.dtsi
<dts/arm/nxp/kinetis/k6x/nxp_k6x.dtsi>`, which is included by both board
:file:`.dts` files. :zephyr_file:`nxp_k6x.dtsi<dts/arm/nxp/kinetis/k6x/nxp_k6x.dtsi>`
in turn includes
:zephyr_file:`armv7-m.dtsi<dts/arm/armv7-m.dtsi>`, which has common definitions
for Arm v7-M cores.

Since :zephyr_file:`nxp_k6x.dtsi<dts/arm/nxp/kinetis/k6x/nxp_k6x.dtsi>` is meant to be
generic across K6X-based boards, it leaves many devices disabled by default
using ``status`` properties.  For example, there is a CAN controller defined as
follows (with unimportant parts skipped):

.. code-block:: devicetree

   can0: can@40024000 {
        ...
        status = "disabled";
        ...
   };

It is up to the board :file:`.dts` or application overlay files to enable these
devices as desired, by setting ``status = "okay"``. The board :file:`.dts`
files are also responsible for any board-specific configuration of the device,
such as adding nodes for on-board sensors, LEDs, buttons, etc.

For example, FRDM-K64 (but not Hexiwear K64) :file:`.dts` enables the CAN
controller and sets the bus speed:

.. code-block:: devicetree

   &can0 {
        status = "okay";
   };

The ``&can0 { ... };`` syntax adds/overrides properties on the node with label
``can0``, i.e. the ``can@4002400`` node defined in the :file:`.dtsi` file.

Other examples of board-specific customization is pointing properties in
``aliases`` and ``chosen`` to the right nodes (see :ref:`dt-alias-chosen`), and
making GPIO/pinmux assignments.

.. _board_kconfig_files:

Write Kconfig files
*******************

Zephyr uses the Kconfig language to configure software features. Your board
needs to provide some Kconfig settings before you can compile a Zephyr
application for it.

Setting Kconfig configuration values is documented in detail in
:ref:`setting_configuration_values`.

There is one mandatory Kconfig file in the board directory, and several optional
files for a board named ``plank``:

.. code-block:: none

   boards/<vendor>/plank
   ├── Kconfig
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   └── plank_<qualifiers>_defconfig

:file:`Kconfig.plank`
  A shared Kconfig file which can be sourced both in Zephyr Kconfig and sysbuild
  Kconfig trees.

  This file selects the SoC in the Kconfig tree and potential other SoC related
  Kconfig settings. This file must not select anything outside the reusable
  Kconfig board and SoC trees.

  A :file:`Kconfig.plank` may look like this:

  .. code-block:: kconfig

     config BOARD_PLANK
             select SOC_SOC1

  The Kconfig symbols :samp:`BOARD_{board}` and
  :samp:`BOARD_{normalized_board_target}` are constructed by the build
  system, therefore no type shall be defined in above code snippet.

:file:`Kconfig`
  Included by :zephyr_file:`boards/Kconfig`.

  This file can add Kconfig settings which are specific to the current board.

  Not all boards have a :file:`Kconfig` file.

  A board specific setting should be defining a custom setting and usually with
  a prompt, like this:

  .. code-block:: kconfig

     config BOARD_FEATURE
             bool "Board specific feature"

  If the setting name is identical to an existing Kconfig setting in Zephyr and
  only modifies the default value of said setting, then
  :file:`Kconfig.defconfig` should be used  instead.

:file:`Kconfig.defconfig`
  Board-specific default values for Kconfig options.

  Not all boards have a :file:`Kconfig.defconfig` file.

  The entire file should be inside an ``if BOARD_PLANK`` / ``endif`` pair of
  lines, like this:

  .. code-block:: kconfig

     if BOARD_PLANK

     config FOO
             default y

     if NETWORKING

     config SOC_ETHERNET_DRIVER
             default y

     endif # NETWORKING

     endif # BOARD_PLANK

:file:`plank_<qualifiers>_defconfig` (or :file:`plank_defconfig` in limited circumstances)
  A Kconfig fragment that is merged as-is into the final build directory
  :file:`.config` whenever an application is compiled for your board.

  :file:`plank_defconfig` can only be used with boards that have no qualifiers, no variants and a
  single SoC present, though this style of naming is not recommended due to samples/tests or
  downstream usage breaking suddenly without warning if a new SoC or board variant/qualifier is
  added to an board in upstream Zephyr.

.. note::
  Multiple files are not merged and there is no fallback mechanism for files, this means if there
  is a board with 2 different SoCs and each one has 2 board variants, a :file:`plank_defconfig`
  file would be wholly unused, for the first qualifier and variant
  :file:`plank_<soc1>_<variant1>_defconfig` will be used, it will not include other file.

  The ``_defconfig`` should contain mandatory settings for your UART,
  console, etc. The results are architecture-specific, but typically look
  something like this:

  .. code-block:: cfg

     CONFIG_GPIO=y
     CONFIG_CONSOLE=y
     CONFIG_UART_CONSOLE=y
     CONFIG_SERIAL=y

:file:`plank_x_y_z_defconfig` / :file:`plank_<qualifiers>_x_y_z_defconfig`
  A Kconfig fragment that is merged as-is into the final build directory
  :file:`.config` whenever an application is compiled for your board revision
  ``x.y.z``.

Build, test, and fix
********************

Now it's time to build and test the application(s) you want to run on your
board until you're satisfied.

For example:

.. code-block:: console

   west build -b plank samples/hello_world
   west flash

For ``west flash`` to work, see :ref:`flash-and-debug-support` below. You can
also just flash :file:`build/zephyr/zephyr.elf`, :file:`zephyr.hex`, or
:file:`zephyr.bin` with any other tools you prefer.

Before submitting a board upstream, verify that every board target you add can
pass the project's minimum open source test suite using only code from the
mainline Zephyr repository and its modules. The suite currently consists of:

- :file:`samples/philosophers`
- :file:`tests/kernel`

For example, build the suite for a board target with:

.. code-block:: console

   west twister -p plank -T samples/philosophers -T tests/kernel

For boards with multiple SoCs, CPU clusters, variants, or revisions, repeat the
test suite for each new board target. A :zephyr:code-sample:`hello_world` build
is also recommended as a quick smoke check, for example:

.. code-block:: console

   west build -p always -b plank/soc1/foo samples/hello_world
   west build -p always -b plank@1.0.0/soc1/foo samples/hello_world

Use :ref:`sysbuild` if the board target requires it. When using board testing
metadata, such as ``testing: only_tags`` in the board target YAML file, make
sure the target is still validated against the minimum test suite in local
testing or CI.

.. _porting-general-recommendations:

General recommendations
***********************

For consistency and to make it easier for users to build applications which remain board agnostic,
please follow these guidelines when porting a board you intend to contribute to Zephyr:

Enable valuable components in Devicetree
  Devicetree nodes for valuable onboard components (LEDs, buttons, sensors, onboard
  USB/Ethernet/BLE/Wi-Fi, etc.) must be **enabled by default** and have correct pin control and
  driver configuration so that they work out of the box.

Keep subsystems disabled by default (Kconfig)
  Do not enable subsystems in the board defconfig unless they are strictly required for basic board
  operation, or are explicitly listed as exceptions in these recommendations.

Configure system clock and tick source
  Set up a functioning system clock and tick source.

Provide a default console
  Use the ``zephyr,console`` chosen node to point to the UART controller used for console output.

  Boards with built-in debug or a USB-to-UART adapter should set the console to the UART controller
  connected to that adapter.

  USB-only boards without any debug adapter must include the common USB CDC-ACM
  :zephyr_file:`Kconfig <boards/common/usb/Kconfig.cdc_acm_serial.defconfig>` and :zephyr_file:`DTS
  <boards/common/usb/cdc_acm_serial.dtsi>` fragments to enable CDC-ACM UART as a default backend
  for logging and shell.

Add :ref:`shield interface <shield-interfaces>` definitions
  For boards exposing standard expansion headers, add connector nodes and pin-muxing. Enable only
  the peripherals needed for the expected/standard connector functionality.

Configure pins and peripheral instances
  Map peripherals to the correct pins (e.g., SPI on Arduino SPI pins) and provide default pinmux
  entries supporting the board's features.

Enable networking interfaces
  If networking hardware is present, configure default interfaces for each supported technology so
  that networking samples work out of the box.

Enable GPIO controllers
  All GPIO ports connected to onboard components or expansion headers should be enabled.

Enable MPU and stack protection
  It is recommended to enable the MPU when available (unless memory resources are too limited).
  When the MPU is enabled, it is recommended to also enable hardware stack protection
  (:kconfig:option:`CONFIG_HW_STACK_PROTECTION`) to ease debugging by allowing the kernel to detect stack overflows.

.. _flash-and-debug-support:

Flash and debug support
***********************

Zephyr supports :ref:`west-build-flash-debug` via west extension commands.

To add ``west flash`` and ``west debug`` support for your board, you need to
create a :file:`board.cmake` file in your board directory. This file's job is
to configure a "runner" for your board. (There's nothing special you need to
do to get ``west build`` support for your board.)

"Runners" are Zephyr-specific Python classes that wrap :ref:`flash and debug
host tools <flash-debug-host-tools>` and integrate with west and the zephyr build
system to support ``west flash`` and related commands. Each runner supports
flashing, debugging, or both. You need to configure the arguments to these
Python scripts in your :file:`board.cmake` to support those commands like this
example :file:`board.cmake`:

.. code-block:: cmake

   board_runner_args(jlink "--device=nrf52" "--speed=4000")
   board_runner_args(pyocd "--target=nrf52" "--frequency=4000000")

   include(${ZEPHYR_BASE}/boards/common/nrfutil.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/nrfjprog.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/pyocd.board.cmake)

This example configures the ``nrfutil``, ``nrfjprog``, ``jlink``, and ``pyocd``
runners.

.. warning::

   Runners usually have names which match the tools they wrap, so the ``jlink``
   runner wraps Segger's J-Link tools, and so on. But the runner command line
   options like ``--speed`` etc. are specific to the Python scripts.

.. note::

   Runners and board configuration should be created without being targeted to
   a single operating system if the tool supports multiple operating systems,
   nor should it rely upon special system setup/configuration. For example; do
   not assume that a user will have prior knowledge/configuration or (if using
   Linux) special udev rules installed, do not assume one specific ``/dev/X``
   device for all platforms as this will not be compatible with Windows or
   macOS, and allow for overriding of the selected device so that multiple
   boards can be connected to a single system and flashed/debugged at the
   choice of the user.

For more details:

- Run ``west flash --context`` to see a list of available runners which support
  flashing, and ``west flash --context -r <RUNNER>`` to view the specific options
  available for an individual runner.
- Run ``west debug --context`` and ``west debug --context <RUNNER>`` to get
  the same output for runners which support debugging.
- Run ``west flash --help`` and ``west debug --help`` for top-level options
  for flashing and debugging.
- See :ref:`west-runner` for Python APIs.
- Look for :file:`board.cmake` files for other boards similar to your own for
  more examples.

To see what a ``west flash`` or ``west debug`` command is doing exactly, run it
in verbose mode:

.. code-block:: sh

   west --verbose flash
   west --verbose debug

Verbose mode prints any host tool commands the runner uses.

The order of the ``include()`` calls in your :file:`board.cmake` matters. The
first ``include`` sets the default runner if it's not already set. For example,
including ``nrfjprog.board.cmake`` first means that ``nrfjprog`` is the default
flash runner for this board. Since ``nrfjprog`` does not support debugging,
``jlink`` is the default debug runner.

.. _porting_board_revisions:

Multiple board revisions
************************

See :ref:`application_board_version` for basics on this feature from the user
perspective.

Board revisions are described in the ``revision`` entry of the
:file:`board.yml`.

.. code-block:: yaml

   board:
     revision:
       format: <major.minor.patch|letter|number|custom>
       default: <default-revision-value>
       exact: <true|false>
       revisions:
       - name: <revA>
       - name: <revB>

Zephyr natively supports the following revision formats:

- ``major.minor.patch``: match a three digit revision, such as ``1.2.3``.
- ``number``: matches integer revisions
- ``letter``: matches single letter revisions from ``A`` to ``Z`` only

.. _board_fuzzy_revision_matching:

Fuzzy revision matching
=======================

Fuzzy revision matching is enabled per default.

If the user selects a revision between those available, the closest revision
number that is not larger than the user's choice is used. For example, if the
board ``plank`` defines revisions ``0.5.0``, and ``1.5.0`` and the user builds
for ``plank@0.7.0``, the build system will target revision ``0.5.0``.

The build system will print this at CMake configuration time:

.. code-block:: console

   -- Board: plank, Revision: 0.7.0 (Active: 0.5.0)

This allows you to only create revision configuration files for board revision
numbers that introduce incompatible changes.

Similarly for ``letter`` revision format, if revisions ``A``, ``D``, and ``F``
are defined and the user builds for ``plank@E``, the build system will target
revision ``D``.

Exact revision matching
=======================

Exact revision matching is enabled when ``exact: true`` is specified in the
revision section in :file:`board.yml`.

When exact is defined then building for ``plank@0.7.0`` in the above example
will result in the following error message:

.. code-block:: console

   Board revision `0.7.0` not found.  Please specify a valid board revision.

Board revision configuration adjustment
=======================================

When the user builds for board ``plank@<revision>`` it is possible to make
adjustments to the board's normal configuration.

As described in the :ref:`default_board_configuration` and
:ref:`board_kconfig_files` sections the board default configuration is created
from the files :file:`<board>.dts` / :file:`<board>_<qualifiers>.dts` and
:file:`<board>_defconfig` / :file:`<board>_<qualifiers>_defconfig`.
When building for a specific board revision, the above files are used as a
starting point and the following board files will be used in addition:

- :file:`<board>_<qualifiers>_<revision>_defconfig`: a specific revision
  defconfig which is only used for the board and SOC / variants identified by
  ``<board>_<qualifiers>``.

- :file:`<board>_<qualifiers>_<revision>.overlay`: a specific revision dts
  overlay which is only used for the board and SOC / variants identified by
  ``<board>_<qualifiers>``.

This split allows boards with multiple SoCs, multi-core SoCs, or variants to
place common revision adjustments which apply to all SoCs and variants in a
single file, while still providing the ability to place SoC or variant specific
adjustments in a dedicated revision file.

Using the ``plank`` board from previous sections, then we could have the following
revision adjustments:

.. code-block:: none

   boards/zephyr/plank
   ├── plank_soc1_foo_1_5_0.overlay   # DTS overlay for plank board when building for soc1 variant foo on revision 1.5.0
   └── plank_soc1_foo_1_5_0_defconfig # Kconfig adjustment for plank board when building for soc1 variant foo on revision 1.5.0

Custom revision.cmake files
***************************

Some boards may not use board revisions supported natively by Zephyr.
For example string revisions.

One reason why Zephyr doesn't support string revisions is that strings can take
many forms and it's not always clear if the given strings are just strings, such
as ``blue``, ``green``, ``red``, etc. or if they provide an order which can be
matched against higher or lower revisions, such as ``alpha``, ``beta```,
``gamma``.

Due to the sheer number of possibilities with strings, including the possibility
of doing regex matches internally, then string revisions must be done using
``custom`` revision type.

To indicate to the build system that ``custom`` revisions are used, the format
field in the ``revision`` section of the :file:`board.yml` must be written as:

.. code-block:: yaml

   board:
     revision:
       format: custom

When using custom revisions then a :file:`revision.cmake` must be created in the
board directory.

The :file:`revision.cmake` will be included by the build system when building
for the board and it is the responsibility of the file to validate the revision
specified by the user.

The :makevar:`BOARD_REVISION` variable holds the revision value specified by the
user.

To signal to the build system that it should use a different revision than the
one specified by the user, :file:`revision.cmake` can set the CMake variable
:cmake:variable:`ACTIVE_BOARD_REVISION` to the revision to use instead. The corresponding
Kconfig files and devicetree overlays must be named
:file:`<board>_<ACTIVE_BOARD_REVISION>_defconfig` and
:file:`<board>_<ACTIVE_BOARD_REVISION>.overlay`.

.. _contributing-your-board:

Contributing your board
***********************

If you want to contribute your board to Zephyr, first -- thanks!

There are some extra things you'll need to do:

#. Make sure you've followed all the :ref:`porting-general-recommendations`.
   They are requirements for boards included with Zephyr.

#. Add documentation for your board using the template file
   :zephyr_file:`doc/templates/board.tmpl`. See :ref:`zephyr_doc` for
   information on how to build your documentation before submitting
   your pull request.

#. Prepare a pull request adding your board which follows the
   :ref:`contribute_guidelines`.

.. _extend-board:

Board extensions
****************

The board hardware model in Zephyr allows you to extend an existing board with
new board variants. Such board extensions can be done in your custom repository
and thus outside of the Zephyr repository.

Extending an existing board with an extra variant allows you to adjust an
existing board and thereby during build to select building for the existing,
unmodified board, or the new variant.

To extend an existing board, first create a :file:`board.yml` in your extended
board. Make sure to use the directory structure described in
:ref:`create-your-board-directory`.

The skeleton of the board YAML file for extending a board is:

.. code-block:: yaml

   board:
     extend: <existing-board-name>
     variants:
       - name: <new-variant>
         qualifier: <existing-qualifier>

When extending a board, your board directory should look like:

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.yml
   ├── plank_<new-qualifiers>_defconfig
   └── plank_<new-qualifiers>.dts

Replace ``plank`` with the real name of the board you extend.

In some cases you might want to also adjust additional settings, like the
:file:`Kconfig.defconfig` or :file:`Kconfig.{board}`.
Therefore it is also possible to provide the following in addition when
extending a board.

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.cmake
   ├── Kconfig
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   └── plank_<new-qualifiers>.yaml