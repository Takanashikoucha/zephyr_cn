:orphan:

.. _migration_3.6:

Migration
guide
to
Zephyr
v3.6.0
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
v3.5.0
到
Zephyr
v3.6.0
required
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
notes<zephyr_3.6>`。

.. contents::
    :local:
    :depth:
    2

Build
System
************

*
Deprecated
的
``prj_<board>.conf``
Kconfig
file
support
被
removed
projects
use
这
个
的
应该
switch
到
use
board
Kconfig
fragments
instead
（``boards/<board>.conf``）。

*
Until
now
``_POSIX_C_SOURCE``、
``_XOPEN_SOURCE``、
和
``_XOPEN_SOURCE_EXTENDED``
在
building
for
native
（``ARCH_POSIX``）
targets
时
被
globally
defined
且
``_POSIX_C_SOURCE``
在
building
with
PicolibC
时
被
defined。
Since
这
个
release
这些
只
为
需要
它们
的
files
被
set。
如果
你
的
library
或
application
需要
这
个
你
可能
start
get
一
个
"implicit
declaration"
warning
对
functions
它们
的
prototypes
只
在
one
of
these
被
defined
时
exposed。
如果
这样
你
可以
fix
它
通过
在
你
的
C
source
file
中
在
任何
include
之前
define
corresponding
的
macro
或
通过
add
``target_compile_definitions(app
PRIVATE
_POSIX_C_SOURCE=200809L)``
的
equivalent
到
你
的
application
或
``zephyr_library_compile_definitions(_POSIX_C_SOURCE=200809L)``
到
你
的
library。

*
通过
set
``CONF_FILE``
到
``prj_<build>.conf``
的
Build
type
now
被
deprecated
users
应该
instead
use
new
的
``-DFILE_SUFFIX``
feature
:ref:`application-file-suffixes`。

Kernel
******

*
System
heap
的
size
和
它
的
availability
now
由
``K_HEAP_MEM_POOL_SIZE``
determined


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
=============

* The optional :c:func:`setup()` function in the Bluetooth HCI driver API (enabled through
  :kconfig:option:`CONFIG_BT_HCI_SETUP`) has gained a function parameter of type
  :c:struct:`bt_hci_setup_params`. By default, the struct is empty, but drivers can opt-in to
  :kconfig:option:`CONFIG_BT_HCI_SET_PUBLIC_ADDR` if they support setting the controller's public
  identity address, which will then be passed in the ``public_addr`` field.

  (:github:`62994`)

* The :dtcompatible:`st,hci-spi-v1` should be used instead of :dtcompatible:`zephyr,bt-hci-spi`
  for the boards which are based on ST BlueNRG-MS.

Controller Area Network (CAN)
=============================

* The native Linux SocketCAN driver, which can now be used in both ``native_posix``
  and :zephyr:board:`native_sim<native_sim>` with or without an embedded C-library, has been renamed to
  reflect this:

  * The devicetree compatible was renamed from ``zephyr,native-posix-linux-can`` to
    :dtcompatible:`zephyr,native-linux-can`.
  * The main Kconfig option was renamed from ``CONFIG_CAN_NATIVE_POSIX_LINUX`` to
    :kconfig:option:`CONFIG_CAN_NATIVE_LINUX`.

* Two new structures for holding common CAN controller driver configuration (``struct
  can_driver_config``) and data (``struct can_driver_data``) fields were introduced. Out-of-tree CAN
  controller drivers need to be updated to use these new, common configuration and data structures
  along with their initializer macros.

* The optional ``can_get_max_bitrate_t`` CAN controller driver callback was removed in favor of a
  common accessor function. Out-of-tree CAN controller drivers need to be updated to no longer
  supply this callback.

* The CAN transceiver API function :c:func:`can_transceiver_enable` now takes a :c:type:`can_mode_t`
  argument for propagating the CAN controller operational mode to the CAN transceiver. Out-of-tree
  CAN controller and CAN transceiver drivers need to be updated to match this new API function
  signature.

* The ``CAN_FILTER_FDF`` flag for filtering classic CAN/CAN FD frames was removed since no known CAN
  controllers implement support for this. Applications can still filter on classic CAN/CAN FD frames
  in their receive callback functions as needed.

* The ``CAN_FILTER_DATA`` and ``CAN_FILTER_RTR`` flags for filtering between Data and Remote
  Transmission Request (RTR) frames were removed since not all CAN controllers implement support for
  individual RX filtering based on the RTR bit. Applications can now use
  :kconfig:option:`CONFIG_CAN_ACCEPT_RTR` to either accept incoming RTR frames matching CAN filters
  or reject all incoming CAN RTR frames (the default). When :kconfig:option:`CONFIG_CAN_ACCEPT_RTR`
  is enabled, applications can still filter between Data and RTR frames in their receive callback
  functions as needed.

* The :dtcompatible:`st,stm32h7-fdcan` CAN controller driver now supports configuring the
  domain/kernel clock via devicetree. Previously, the driver only supported using the PLL1_Q clock
  for kernel clock, but now it defaults to the HSE clock, which is the chip default. Boards that
  use the PLL1_Q clock for FDCAN will need to override the ``clocks`` property as follows:

  .. code-block:: devicetree

    &fdcan1 {
            clocks = <&rcc STM32_CLOCK_BUS_APB1_2 0x00000100>,
                     <&rcc STM32_SRC_PLL1_Q FDCAN_SEL(1)>;
    };

Display
=======

* ILI9XXX based displays now use the MIPI DBI driver class. These displays
  must now be declared within a MIPI DBI driver wrapper device, which will
  manage interfacing with the display. Note that the `cmd-data-gpios` pin has
  changed polarity with this update, to align better with the new
  `dc-gpios` name. For an example, see below:

  .. code-block:: devicetree

    /* Legacy ILI9XXX display definition */
    &spi2 {
        ili9340: ili9340@0 {
            compatible = "ilitek,ili9340";
            reg = <0>;
            spi-max-frequency = <32000000>;
            reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
            cmd-data-gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;
            rotation = <270>;
            width = <320>;
            height = <240>;
        };
    };

    /* New display definition with MIPI DBI device */

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
        dc-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        spi-dev = <&spi2>;
        #address-cells = <1>;
        #size-cells = <0>;

        ili9340: ili9340@0 {
            compatible = "ilitek,ili9340";
            reg = <0>;
            mipi-max-frequency = <32000000>;
            rotation = <270>;
            width = <320>;
            height = <240>;
        };
    };

Flash
=====

* The :dtcompatible:`st,stm32-ospi-nor` and :dtcompatible:`st,stm32-qspi-nor` give the nor flash
  base address and size (in Bytes) with the **reg** property as follows.
  The <size> property is not used anymore.

  .. code-block:: devicetree

    mx25lm51245: ospi-nor-flash@70000000 {
            compatible = "st,stm32-ospi-nor";
            reg = <0x70000000 DT_SIZE_M(64)>; /* 512 Mbits*/
    };

General Purpose I/O (GPIO)
==========================

* The :dtcompatible:`nxp,pcf8574` driver has been renamed to
  :dtcompatible:`nxp,pcf857x`. (:github:`67054`) to support pcf8574 and pcf8575.
  The Kconfig option has been renamed from :kconfig:option:`CONFIG_GPIO_PCF8574` to
  :kconfig:option:`CONFIG_GPIO_PCF857X`.
  The Device Tree can be configured as follows:

  .. code-block:: devicetree

    &i2c {
      status = "okay";
      pcf8574: pcf857x@20 {
          compatible = "nxp,pcf857x";
          status = "okay";
          reg = <0x20>;
          gpio-controller;
          #gpio-cells = <2>;
          ngpios = <8>;
      };

      pcf8575: pcf857x@21 {
          compatible = "nxp,pcf857x";
          status = "okay";
          reg = <0x21>;
          gpio-controller;
          #gpio-cells = <2>;
          ngpios = <16>;
      };
    };

Input
=====

* Touchscreen drivers :dtcompatible:`focaltech,ft5336` and
  :dtcompatible:`goodix,gt911` were using the incorrect polarity for the
  respective ``reset-gpios``. This has been fixed so those signals now have to
  be flagged as :c:macro:`GPIO_ACTIVE_LOW` in the devicetree. (:github:`64800`)

Interrupt Controller
====================

* The function signature of the ``isr_t`` callback function passed to the ``shared_irq``
  interrupt controller driver API via :c:func:`shared_irq_isr_register()` has changed.
  The callback now takes an additional `irq_number` parameter. Out-of-tree users of
  this API will need to be updated.

  (:github:`66427`)

Renesas RA Series Drivers
=========================

* Several Renesas RA series drivers Kconfig options have been renamed:

  * ``CONFIG_CLOCK_CONTROL_RA`` -> :kconfig:option:`CONFIG_CLOCK_CONTROL_RENESAS_RA`
  * ``CONFIG_GPIO_RA`` -> :kconfig:option:`CONFIG_GPIO_RENESAS_RA`
  * ``CONFIG_PINCTRL_RA`` -> :kconfig:option:`CONFIG_PINCTRL_RENESAS_RA`
  * ``CONFIG_UART_RA`` -> :kconfig:option:`CONFIG_UART_RENESAS_RA`

Sensors
=======

* The :dtcompatible:`st,lsm6dsv16x` sensor driver has been changed to support
  configuration of both int1 and int2 pins. The DT attribute ``irq-gpios`` has been
  removed and substituted by two new attributes, ``int1-gpios`` and ``int2-gpios``.
  These attributes must be configured in the Device Tree similarly to the following
  example:

  .. code-block:: devicetree

    / {
        lsm6dsv16x@0 {
            compatible = "st,lsm6dsv16x";

            int1-gpios = <&gpioa 4 GPIO_ACTIVE_HIGH>;
            int2-gpios = <&gpiod 11 GPIO_ACTIVE_HIGH>;
            drdy-pin = <2>;
        };
    };

Serial
======

* Runtime configuration is now disabled by default for Nordic UART drivers. The motivation for the
  change is that this feature is rarely used and disabling it significantly reduces the memory
  footprint.

Timer
=====

* The :dtcompatible:`st,stm32-lptim` lptim which is selected for counting ticks during
  low power modes is identified by **stm32_lp_tick_source** in the device tree as follows.
  The stm32_lptim_timer driver has been changed to support this.

  .. code-block:: devicetree

    stm32_lp_tick_source: &lptim1 {
            status = "okay";
    };

Bluetooth
*********

* ATT now has its own TX buffer pool.
  If extra ATT buffers were configured using :kconfig:option:`CONFIG_BT_L2CAP_TX_BUF_COUNT`,
  they now instead should be configured through :kconfig:option:`CONFIG_BT_ATT_TX_COUNT`.
* The HCI implementation for both the Host and the Controller sides has been
  renamed for the IPC transport. The ``CONFIG_BT_RPMSG`` Kconfig option is now
  :kconfig:option:`CONFIG_BT_HCI_IPC`, and the ``zephyr,bt-hci-rpmsg-ipc``
  Devicetree chosen is now ``zephyr,bt-hci-ipc``. The existing sample has also
  been renamed, from ``samples/bluetooth/hci_rpmsg`` to
  ``samples/bluetooth/hci_ipc``. (:github:`64391`)
* The BT GATT callback list, appended to by :c:func:`bt_gatt_cb_register`, is no longer
  cleared on :c:func:`bt_enable`. Callbacks can now be registered before the initial
  call to :c:func:`bt_enable`, and should no longer be re-registered after a :c:func:`bt_disable`
  :c:func:`bt_enable` cycle. (:github:`63693`)
* The Bluetooth UUID has been modified to rodata in ``BT_UUID_DECLARE_16``, ``BT_UUID_DECLARE_32``
  and ``BT_UUID_DECLARE_128`` as the return value has been changed to ``const``.
  Any pointer to a UUID must be prefixed with ``const``, otherwise there will be a compilation
  warning. For example change ``struct bt_uuid *uuid = BT_UUID_DECLARE_16(xx)`` to
  ``const struct bt_uuid *uuid = BT_UUID_DECLARE_16(xx)``. (:github:`66136`)
* The :c:func:`bt_l2cap_chan_send` API no longer allocates buffers from the same pool as its `buf`
  parameter when segmenting SDUs into PDUs. In order to reproduce the previous behavior, the
  application should register the `alloc_seg` channel callback and allocate from the same pool as
  `buf`.
* The :c:func:`bt_l2cap_chan_send` API now requires the application to reserve
  enough bytes for the L2CAP headers. Call ``net_buf_reserve(buf,
  BT_L2CAP_SDU_CHAN_SEND_RESERVE);`` at buffer allocation time to do so.
* `BT_ISO_TIMESTAMP_NONE` has been removed and the `ts` parameter of :c:func:`bt_iso_chan_send` has
  as well. :c:func:`bt_iso_chan_send` now always sends without timestamp. To send with a timestamp,
  :c:func:`bt_iso_chan_send_ts` can be used.
* The ``CONFIG_BT_HCI_RESERVE`` and ``CONFIG_BT_HCI_RAW_RESERVE`` Kconfig options were removed. All
  buffers get by default one byte of headroom now, which HCI transport implementations can rely on
  (whether they need it or not).

Bluetooth Mesh
==============

  * The Bluetooth Mesh ``model`` declaration has been changed to add prefix ``const``.
    The ``model->user_data``, ``model->elem_idx`` and ``model->mod_idx`` field has been changed to
    the new runtime structure, replaced by ``model->rt->user_data``, ``model->rt->elem_idx`` and
    ``model->rt->mod_idx`` separately. (:github:`65152`)
  * The Bluetooth Mesh ``element`` declaration has been changed to add prefix ``const``.
    The ``elem->addr`` field has been changed to the new runtime structure, replaced by
    ``elem->rt->addr``. (:github:`65388`)
  * Deprecated :kconfig:option:`CONFIG_BT_MESH_PROV_DEVICE`. This option is
    replaced by new option :kconfig:option:`CONFIG_BT_MESH_PROVISIONEE` to
    be aligned with Mesh Protocol Specification v1.1, section 5.4. (:github:`64252`)
  * Removed the ``CONFIG_BT_MESH_V1d1`` Kconfig option.
  * Removed the ``CONFIG_BT_MESH_TX_SEG_RETRANS_COUNT``,
    ``CONFIG_BT_MESH_TX_SEG_RETRANS_TIMEOUT_UNICAST``,
    ``CONFIG_BT_MESH_TX_SEG_RETRANS_TIMEOUT_GROUP``, ``CONFIG_BT_MESH_SEG_ACK_BASE_TIMEOUT``,
    ``CONFIG_BT_MESH_SEG_ACK_PER_HOP_TIMEOUT``, ``BT_MESH_SEG_ACK_PER_SEGMENT_TIMEOUT``
    Kconfig options. They are superseded by the
    :kconfig:option:`CONFIG_BT_MESH_SAR_TX_SEG_INT_STEP`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_COUNT`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_WITHOUT_PROG_COUNT`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_STEP`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_INC`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_COUNT`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_INT`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_THRESHOLD`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_DELAY_INC`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_INT_STEP`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_RX_DISCARD_TIMEOUT`,
    :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT` Kconfig options.

Bluetooth Audio
===============

  * The ``BT_AUDIO_CODEC_LC3_*`` values from ``<zephyr/bluetooth/audio/lc3.h>`` have moved to
    ``<zephyr/bluetooth/audio/audio.h>`` and have the ``LC3`` part of their names replaced by a
    more semantically correct name: e.g.
    ``BT_AUDIO_CODEC_LC3_CHAN_COUNT`` is now ``BT_AUDIO_CODEC_CAP_TYPE_CHAN_COUNT``,
    ``BT_AUDIO_CODEC_LC3_FREQ`` is now ``BT_AUDIO_CODEC_CAP_TYPE_FREQ``, and
    ``BT_AUDIO_CODEC_CONFIG_LC3_FREQ`` is now ``BT_AUDIO_CODEC_CFG_FREQ``, etc.
    Similarly the enumerations have also been renamed.
    E.g. ``bt_audio_codec_config_freq`` is now ``bt_audio_codec_cfg_freq``,
    ``bt_audio_codec_capability_type`` is now ``bt_audio_codec_cap_type``,
    ``bt_audio_codec_config_type`` is now ``bt_audio_codec_cfg_type``, etc. (:github:`67024`)
  * The `ts` parameter of :c:func:`bt_bap_stream_send` has been removed.
    :c:func:`bt_bap_stream_send` now always sends without timestamp.
    To send with a timestamp, :c:func:`bt_bap_stream_send_ts` can be used.
  * The `ts` parameter of :c:func:`bt_cap_stream_send` has been removed.
    :c:func:`bt_cap_stream_send` now always sends without timestamp.
    To send with a timestamp, :c:func:`bt_cap_stream_send_ts` can be used.

Networking
**********

* The CoAP public API has some minor changes to take into account. The
  :c:func:`coap_remove_observer` now returns a result if the observer was removed. This
  change is used by the newly introduced :ref:`coap_server_interface` subsystem. Also, the
  ``request`` argument for :c:func:`coap_well_known_core_get` is made ``const``.
  (:github:`64265`)

* CoAP observer events have moved from a callback function in a CoAP resource to the Network Events
  subsystem. The ``CONFIG_COAP_OBSERVER_EVENTS`` configuration option has been removed.
  (:github:`65936`)

* The CoAP public API function :c:func:`coap_pending_init` has changed. The parameter
  ``retries`` is replaced with a pointer to :c:struct:`coap_transmission_parameters`. This allows to
  specify retransmission parameters of the confirmable message. It is safe to pass a NULL pointer to
  use default values.
  (:github:`66482`)

* The CoAP public API functions :c:func:`coap_service_send` and :c:func:`coap_resource_send` have
  changed. An additional parameter pointer to :c:struct:`coap_transmission_parameters` has been
  added. It is safe to pass a NULL pointer to use default values. (:github:`66540`)

* The IGMP multicast library now supports IGMPv3. This results in a minor change to the existing
  api. The :c:func:`net_ipv4_igmp_join` now takes an additional argument of the type
  ``const struct igmp_param *param``. This allows IGMPv3 to exclude/include certain groups of
  addresses. If this functionality is not used or available (when using IGMPv2), you can safely pass
  a NULL pointer. IGMPv3 can be enabled using the Kconfig ``CONFIG_NET_IPV4_IGMPV3``.
  (:github:`65293`)

* The network stack now uses a separate IPv4 TTL (time-to-live) value for multicast packets.
  Before, the same TTL value was used for unicast and multicast packets.
  The IPv6 hop limit value is also changed so that unicast and multicast packets can have a
  different one. (:github:`65886`)

* The Ethernet phy APIs defined in ``<zephyr/net/phy.h>`` are removed from syscall list.
  The APIs were marked as callable from usermode but in practice this does not work as the device
  cannot be accessed from usermode thread. This means that the API calls will need to made
  from supervisor mode thread.

* The zperf ratio between mbps and kbps, kbps and bps is changed to 1000, instead of 1024,
  to align with iperf ratios.

* For network buffer pools maximum allocation size was added to a common structure
  ``struct net_buf_data_alloc`` as a new field ``max_alloc_size``. Similar member ``data_size`` of
  ``struct net_buf_pool_fixed`` that was specific only for buffer pools with a fixed size was
  removed.

Other Subsystems
****************

LoRaWAN
=======

* The API to register a callback to provide battery level information to the LoRaWAN stack has been
  renamed from ``lorawan_set_battery_level_callback`` to
  :c:func:`lorawan_register_battery_level_callback` and the return type is now ``void``. This
  is more consistent with similar functions for downlink and data rate changed callbacks.
  (:github:`65103`)

MCUmgr
======

* MCUmgr applications that make use of serial transports (shell or UART) must now select
  :kconfig:option:`CONFIG_CRC`, this was previously erroneously selected if MCUmgr was enabled,
  when for non-serial transports it was not needed. (:github:`64078`)

Shell
=====

* The following subsystem and driver shell modules are now disabled by default. Each required shell
  module must now be explicitly enabled via Kconfig (:github:`65307`):

  * :kconfig:option:`CONFIG_ACPI_SHELL`
  * :kconfig:option:`CONFIG_ADC_SHELL`
  * :kconfig:option:`CONFIG_AUDIO_CODEC_SHELL`
  * :kconfig:option:`CONFIG_CAN_SHELL`
  * :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_SHELL`
  * :kconfig:option:`CONFIG_DAC_SHELL`
  * :kconfig:option:`CONFIG_DEBUG_COREDUMP_SHELL`
  * :kconfig:option:`CONFIG_EDAC_SHELL`
  * :kconfig:option:`CONFIG_EEPROM_SHELL`
  * :kconfig:option:`CONFIG_FLASH_SHELL`
  * :kconfig:option:`CONFIG_HWINFO_SHELL`
  * :kconfig:option:`CONFIG_I2C_SHELL`
  * :kconfig:option:`CONFIG_LOG_CMDS`
  * :kconfig:option:`CONFIG_LORA_SHELL`
  * :kconfig:option:`CONFIG_MCUBOOT_SHELL`
  * :kconfig:option:`CONFIG_MDIO_SHELL`
  * :kconfig:option:`CONFIG_OPENTHREAD_SHELL`
  * :kconfig:option:`CONFIG_PCIE_SHELL`
  * :kconfig:option:`CONFIG_PSCI_SHELL`
  * :kconfig:option:`CONFIG_PWM_SHELL`
  * :kconfig:option:`CONFIG_REGULATOR_SHELL`
  * :kconfig:option:`CONFIG_SENSOR_SHELL`
  * :kconfig:option:`CONFIG_SMBUS_SHELL`
  * :kconfig:option:`CONFIG_STATS_SHELL`
  * :kconfig:option:`CONFIG_USBD_SHELL`
  * :kconfig:option:`CONFIG_USBH_SHELL`
  * :kconfig:option:`CONFIG_W1_SHELL`
  * :kconfig:option:`CONFIG_WDT_SHELL`

* The ``SHELL_UART_DEFINE`` macro now only requires a ``_name`` argument. In the meantime, the
  macro accepts additional arguments (ring buffer TX & RX size arguments) for compatibility with
  previous Zephyr version, but they are ignored, and will be removed in future release.

* :kconfig:option:`CONFIG_SHELL_BACKEND_SERIAL_API` now does not automatically default to
  :kconfig:option:`CONFIG_SHELL_BACKEND_SERIAL_API_ASYNC` when
  :kconfig:option:`CONFIG_UART_ASYNC_API` is enabled, :kconfig:option:`CONFIG_SHELL_ASYNC_API`
  also has to be enabled in order to use the asynchronous serial shell (:github:`68475`).

ZBus
====

* The ``CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_DYNAMIC`` and
  ``CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_STATIC`` zbus options are renamed. Instead, the new
  :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_BUF_ALLOC_DYNAMIC` and
  :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_BUF_ALLOC_STATIC` options should be used.
  (:github:`65632`)

* To enable the zbus HLP priority boost, the developer must call the
  :c:func:`zbus_obs_attach_to_thread` inside the attaching thread. The observer will then assume the
  attached thread priority which will be used by zbus to calculate HLP priority. (:github:`63183`)

Userspace
*********

* A number of userspace related functions have been moved out of the ``z_`` namespace
  and into the kernel namespace.

  * ``Z_OOPS`` to :c:macro:`K_OOPS`
  * ``Z_SYSCALL_MEMORY`` to :c:macro:`K_SYSCALL_MEMORY`
  * ``Z_SYSCALL_MEMORY_READ`` to :c:macro:`K_SYSCALL_MEMORY_READ`
  * ``Z_SYSCALL_MEMORY_WRITE`` to :c:macro:`K_SYSCALL_MEMORY_WRITE`
  * ``Z_SYSCALL_DRIVER_OP`` to :c:macro:`K_SYSCALL_DRIVER_OP`
  * ``Z_SYSCALL_SPECIFIC_DRIVER`` to :c:macro:`K_SYSCALL_SPECIFIC_DRIVER`
  * ``Z_SYSCALL_OBJ`` to :c:macro:`K_SYSCALL_OBJ`
  * ``Z_SYSCALL_OBJ_INIT`` to :c:macro:`K_SYSCALL_OBJ_INIT`
  * ``Z_SYSCALL_OBJ_NEVER_INIT`` to :c:macro:`K_SYSCALL_OBJ_NEVER_INIT`
  * ``z_user_from_copy`` to :c:func:`k_usermode_from_copy`
  * ``z_user_to_copy`` to :c:func:`k_usermode_to_copy`
  * ``z_user_string_copy`` to :c:func:`k_usermode_string_copy`
  * ``z_user_string_alloc_copy`` to :c:func:`k_usermode_string_alloc_copy`
  * ``z_user_alloc_from_copy`` to :c:func:`k_usermode_alloc_from_copy`
  * ``z_user_string_nlen`` to :c:func:`k_usermode_string_nlen`
  * ``z_dump_object_error`` to :c:func:`k_object_dump_error`
  * ``z_object_validate`` to :c:func:`k_object_validate`
  * ``z_object_find`` to :c:func:`k_object_find`
  * ``z_object_wordlist_foreach`` to :c:func:`k_object_wordlist_foreach`
  * ``z_thread_perms_inherit`` to :c:func:`k_thread_perms_inherit`
  * ``z_thread_perms_set`` to :c:func:`k_thread_perms_set`
  * ``z_thread_perms_clear`` to :c:func:`k_thread_perms_clear`
  * ``z_thread_perms_all_clear`` to :c:func:`k_thread_perms_all_clear`
  * ``z_object_uninit`` to :c:func:`k_object_uninit`
  * ``z_object_recycle`` to :c:func:`k_object_recycle`
  * ``z_obj_validation_check`` to :c:func:`k_object_validation_check`
  * ``Z_SYSCALL_VERIFY_MSG`` to :c:macro:`K_SYSCALL_VERIFY_MSG`
  * ``z_object`` to :c:struct:`k_object`
  * ``z_object_init`` to :c:func:`k_object_init`
  * ``z_dynamic_object_aligned_create`` to :c:func:`k_object_create_dynamic_aligned`

Architectures
*************

Xtensa
======

* :kconfig:option:`CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC` no longer has a default in
  the architecture layer. Instead, SoCs or boards will need to define it.

* Scratch registers ``ZSR_ALLOCA`` has been renamed to ``ZSR_A0SAVE``.

* Renamed files with hyhphens to underscores:

  * ``xtensa-asm2-context.h`` to ``xtensa_asm2_context.h``

  * ``xtensa-asm2-s.h`` to ``xtensa_asm2_s.h``

* ``xtensa_asm2.h`` has been removed. Use ``xtensa_asm2_context.h`` instead for
  stack frame structs.

* Renamed functions out of ``z_`` namespace into ``xtensa_`` namespace.

  * ``z_xtensa_irq_enable`` to :c:func:`xtensa_irq_enable`

  * ``z_xtensa_irq_disable`` to :c:func:`xtensa_irq_disable`

  * ``z_xtensa_irq_is_enabled`` to :c:func:`xtensa_irq_is_enabled`