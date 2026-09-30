:orphan:

.. _migration_3.5:

Migration
guide
to
Zephyr
v3.5.0
################################

这
个
document
describe
migrating
你
的
application
从
Zephyr
v3.4.0
到
Zephyr
v3.5.0
required
或
recommended
的
changes。

其他
changes
（不
directly
related
to
migrating
applications）
可以
found
在
:ref:`release
notes<zephyr_3.5>`。

Required
changes
****************

Kernel
======

*
Kernel
:c:func:`k_mem_slab_free`
function
changed
它
的
signature
now
take
一
个
``void
*mem``
pointer
而
不
是
``void
**mem``
double
pointer。
New
的
signature
将
不
immediately
trigger
一
个
compiler
error
或
warning
instead
likely
cause
一
个
invalid
的
memory
access
在
runtime。
一
个
new
的
``_ASSERT``
statement
你
可以
用
:kconfig:option:`CONFIG_ASSERT`
enable
它
将
detect
如果
你
pass
该
function
memory
不
belonging
to
slab
中
的
memory
blocks。

*
:c:macro:`CONTAINER_OF`
now
perform
type
checking
这
very
commonly
被
misused
用于
从
:c:struct:`k_work`
pointers
obtain
user
structure
而
不
passing
from
:c:struct:`k_work_delayable`。
这
now
result
在
一
个
build
error
且
必须
被
properly
done
用
:c:func:`k_work_delayable_from_work`。

C
Library
=========

*
Default
的
C
library
used
在
most
targets
上
changed
从
built
in
的
minimal
C
library
到
Picolibc。
Both
provide
standard
C
library
interfaces
且
shouldn't
cause
any
behavioral
regressions
for
applications
但
有
a
few
side
effects
需要
aware
of
在
migrating
到
Picolibc
时。


.. note::

   以下为原文（待翻译）


* The LPC55XXX series SOC (except LPC55S06) default main clock has been
  updated to PLL1 source from XTAL32K running at 144MHZ. If the new
  kconfig option :kconfig:option:`CONFIG_INIT_PLL1`
  is disabled then the main clock is muxed to FRO_HR as before.

* The Kconfig option ``CONFIG_GPIO_NCT38XX_INTERRUPT`` has been renamed to
  :kconfig:option:`CONFIG_GPIO_NCT38XX_ALERT`.

* The CAN controller timing API functions :c:func:`can_set_timing` and :c:func:`can_set_timing_data`
  no longer fallback to the (Re-)Synchronization Jump Width (SJW) value set in the devicetree
  properties for the given CAN controller upon encountering an SJW value corresponding to
  ``CAN_SJW_NO_CHANGE`` (which is no longer available). The caller will therefore need to fill in
  the ``sjw`` field in :c:struct:`can_timing`. To aid in this, the :c:func:`can_calc_timing` and
  :c:func:`can_calc_timing_data` functions now automatically calculate a suitable SJW. The
  calculated SJW can be overwritten by the caller if needed. The CAN controller API functions
  :c:func:`can_set_bitrate` and :c:func:`can_set_bitrate_data` now also automatically calculate a
  suitable SJW, but their SJW cannot be overwritten by the caller.

* The CAN ISO-TP message configuration in :c:struct:`isotp_msg_id` is changed to use the following
  flags instead of bit fields:

  * :c:macro:`ISOTP_MSG_EXT_ADDR` to enable ISO-TP extended addressing
  * :c:macro:`ISOTP_MSG_FIXED_ADDR` to enable ISO-TP fixed addressing
  * :c:macro:`ISOTP_MSG_IDE` to use extended (29-bit) CAN IDs

  The two new flags :c:macro:`ISOTP_MSG_FDF` and :c:macro:`ISOTP_MSG_BRS` were added for CAN FD
  mode.

* NXP i.MX RT based boards should now enable
  :kconfig:option:`CONFIG_DEVICE_CONFIGURATION_DATA` at the board level when
  using a DCD with the RT bootrom, and enable
  :kconfig:option:`CONFIG_NXP_IMX_EXTERNAL_SDRAM` when using external SDRAM
  via the SEMC

* NXP i.MX RT11xx series SNVS pin control name identifiers have been updated to
  match with the source data for these SOCs. The pin names have had the
  suffix ``dig`` added. For example, ``iomuxc_snvs_wakeup_gpio13_io00`` has
  been renamed to ``iomuxc_snvs_wakeup_dig_gpio13_io00``

Power Management
================

* Platforms that implement power management hooks must explicitly select
  :kconfig:option:`CONFIG_HAS_PM` in Kconfig. This is now a dependency of
  :kconfig:option:`CONFIG_PM`. Before this change all platforms could enable
  :kconfig:option:`CONFIG_PM` because empty weak stubs were provided, however,
  this is no longer supported. As a result of this change, power management
  hooks are no longer defined as weaks.

* Multiple platforms no longer support powering the system off using
  :c:func:`pm_state_force`. The new :c:func:`sys_poweroff` API must be used.
  Migrated platforms include Nordic nRF, STM32, ESP32 and TI CC13XX/26XX. The
  new API is independent from :kconfig:option:`CONFIG_PM`. It requires
  :kconfig:option:`CONFIG_POWEROFF` to be enabled, which depends on
  :kconfig:option:`CONFIG_HAS_POWEROFF`, an option selected by platforms
  implementing the required new hooks.

Bootloader
==========

* The :kconfig:option:`CONFIG_BOOTLOADER_SRAM_SIZE` default value is now ``0`` (was
  ``16``). Bootloaders that use a part of the SRAM should set this value to an
  appropriate size. :github:`60371`

Bluetooth
=========

* The ``accept()`` callback's signature in :c:struct:`bt_l2cap_server` has
  changed to ``int (*accept)(struct bt_conn *conn, struct bt_l2cap_server
  *server, struct bt_l2cap_chan **chan)``,
  adding a new ``server`` parameter pointing to the :c:struct:`bt_l2cap_server`
  structure instance the callback relates to. :github:`60536`

Networking
==========

* A new networking Kconfig option :kconfig:option:`CONFIG_NET_INTERFACE_NAME`
  defaults to ``y``. The option allows user to set a name to a network interface.
  During system startup a default name is assigned to the network interface like
  ``eth0`` to the first Ethernet network interface. The option affects the behavior
  of ``SO_BINDTODEVICE`` BSD socket option. If the Kconfig option is set to ``n``,
  which is how the system worked earlier, then the name of the device assigned
  to the network interface is used by the ``SO_BINDTODEVICE`` socket option.
  If the Kconfig option is set to ``y`` (current default), then the network
  interface name is used by the ``SO_BINDTODEVICE`` socket option.

* Ethernet PHY devicetree bindings were updated to use the standard ``reg``
  property for the PHY address instead of a custom ``address`` property. As a
  result, MDIO controller nodes now require ``#address-cells`` and
  ``#size-cells`` properties. Similarly, Ethernet PHY devicetree nodes and
  corresponding driver were updated to consistently use the node name
  ``ethernet-phy`` instead of ``phy``. Devicetrees and overlays must be updated
  accordingly:

  .. code-block:: devicetree

     mdio {
         compatible = "mdio-controller";
         #address-cells = <1>;
         #size-cells = <0>;

         ethernet-phy@0 {
             compatible = "ethernet-phy";
             reg = <0>;
         };
     };

Other Subsystems
================

* ZBus runtime observers implementation now relies on the HEAP memory instead of a memory slab.
  Thus, zbus' configuration (kconfig) related to runtime observers has changed. To keep your runtime
  observers code working correctly, you need to:

  - Replace the integer ``CONFIG_ZBUS_RUNTIME_OBSERVERS_POOL_SIZE`` with the boolean
    :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS`;
  - Set the HEAP size with the :kconfig:option:`CONFIG_HEAP_MEM_POOL_SIZE`.

* The zbus VDED delivery sequence has changed. Check the :ref:`documentation<zbus delivery
  sequence>` to verify if it will affect your code.

* MCUmgr SMP version 2 error codes entry has changed due to a collision with an
  existing response in shell_mgmt. Previously, these errors had the entry ``ret``
  but now have the entry ``err``. ``smp_add_cmd_ret()`` is now deprecated and
  :c:func:`smp_add_cmd_err` should be used instead, ``MGMT_CB_ERROR_RET`` is
  now deprecated and :c:enumerator:`MGMT_CB_ERROR_ERR` should be used instead.
  SMP version 2 error code defines for in-tree modules have been updated to
  replace the ``*_RET_RC_*`` parts with ``*_ERR_*``.

* MCUmgr SMP version 2 error translation (to legacy MCUmgr error code) is now
  handled in function handlers by setting the ``mg_translate_error`` function
  pointer of :c:struct:`mgmt_group` when registering a group. See
  :c:type:`smp_translate_error_fn` for function details. Any SMP version 2
  handlers made for Zephyr 3.4 need to be updated to include these translation
  functions when the groups are registered.

ARM
===

* ARM SoC initialization routines no longer need to call `NMI_INIT()`. The
  macro call has been removed as it was not doing anything useful.

RISC V
======

* The :kconfig:option:`CONFIG_RISCV_MTVEC_VECTORED_MODE` Kconfig option was renamed to
  :kconfig:option:`CONFIG_RISCV_VECTORED_MODE`.

Recommended Changes
*******************

* Setting the GIC architecture version by selecting
  :kconfig:option:`CONFIG_GIC_V1`, :kconfig:option:`CONFIG_GIC_V2` and
  :kconfig:option:`CONFIG_GIC_V3` directly in Kconfig has been deprecated.
  The GIC version should now be specified by adding the appropriate compatible, for
  example :dtcompatible:`arm,gic-v2`, to the GIC node in the device tree.

* Nordic nRF based boards using :kconfig:option:`CONFIG_NFCT_PINS_AS_GPIOS`
  to configure NFCT pins as GPIOs, should instead set the new UICR
  ``nfct-pins-as-gpios`` property in devicetree. It can be set like this in the
  board devicetree files:

  .. code-block:: devicetree

     &uicr {
         nfct-pins-as-gpios;
     };

* Nordic nRF based boards using :kconfig:option:`CONFIG_GPIO_AS_PINRESET`
  to configure reset GPIO as nRESET, should instead set the new UICR
  ``gpio-as-nreset`` property in devicetree. It can be set like this in the
  board devicetree files:

  .. code-block:: devicetree

     &uicr {
         gpio-as-nreset;
     };

* The :kconfig:option:`CONFIG_MODEM_GSM_PPP` modem driver is obsolete.
  Instead the new :kconfig:option:`CONFIG_MODEM_CELLULAR` driver should be used.
  As part of this :kconfig:option:`CONFIG_GSM_MUX` and :kconfig:option:`CONFIG_UART_MUX` are being
  marked as deprecated as well. The new modem subsystem :kconfig:option:`CONFIG_MODEM_CMUX`
  and :kconfig:option:`CONFIG_MODEM_PPP` should be used instead.

* Device drivers should now be restricted to ``PRE_KERNEL_1``, ``PRE_KERNEL_2``
  and ``POST_KERNEL`` initialization levels. Other device initialization levels,
  including ``EARLY``, ``APPLICATION``, and ``SMP``, have been deprecated and
  will be removed in future releases. Note that these changes do not apply to
  initialization levels used in the context of the ``init.h`` API,
  e.g. :c:macro:`SYS_INIT`.

* The following CAN controller devicetree properties are now deprecated in favor specifying the
  initial CAN bitrate using the ``bus-speed``, ``sample-point``, ``bus-speed-data``, and
  ``sample-point-data`` properties:

  * ``sjw``
  * ``prop-seg``
  * ``phase-seg1``
  * ``phase-seg1``
  * ``sjw-data``
  * ``prop-seg-data``
  * ``phase-seg1-data``
  * ``phase-seg1-data``

* ``<zephyr/arch/arm/aarch32/cortex_a_r/cmsis.h>`` and
  ``<zephyr/arch/arm/aarch32/cortex_m/cmsis.h>`` are now deprecated in favor of
  including ``<cmsis_core.h>`` instead. The new header is part of the CMSIS glue
  code in the ``modules`` directory.

* Random API header ``<zephyr/random/rand32.h>`` is deprecated in favor of
  ``<zephyr/random/random.h>``. The old header will be removed in future releases
  and its usage should be avoided.
