.. _i3c_api:

Improved
Inter-Integrated
Circuit
（I3C）
Bus
###########################################

I3C
（Improved
Inter-Integrated
Circuit）
是
two-signal
shared
peripheral
interface
bus。
Bus
上
的
devices
可以
在
两
个
roles
中
工作：
作为
"controller"
发起
transactions
并
控制
clock
或
作为
"target"
响应
transaction
commands。

当前，
API
基于
`I3C
Specification`_
version
1.1.1。

.. contents::
   :local:
   :depth:
   2

.. _i3c-controller-api:

I3C
Controller
API
******************

Zephyr
的
I3C
controller
API
在
I3C
controller
控制
bus
时
使用
特别
是
start
和
stop
conditions
和
clock。
这
是
最
常见
的
mode
用
于
与
I3C
target
devices
如
sensors
交互。

由于
I3C
的
性质，
bus
上
有
devices
它们
在
上电
时
可能
没有
addresses。
因此，
I3C
controller
需要
执行
额外
的
dynamic
address
assignment。
因为
这
个
原因，
controller
需要
维护
分开
的
structures
跟踪
device
status。
这
可以
在
build
time
做
例如
通过
为
I3C
和
I
:sup:`2`
C
devices
创建
device
descriptors
的
arrays：

.. code-block:: c

   static
   struct
   i3c_device_desc
   i3c_device_array[]
   =
   I3C_DEVICE_ARRAY_DT_INST(inst);
   static
   struct
   i3c_i2c_device_desc
   i2c_device_array[]
   =
   I3C_I2C_DEVICE_ARRAY_DT_INST(inst);


.. note::

   以下为原文（待翻译）


   i3c0: i3c@10000 {
           compatible = "vendor,i3c";

           #address-cells = <0x3>;
           #size-cells = <0x0>;

           reg = <0x10000 0x1000>;
           interrupts = <0x1F 0x0>;

           pinctrl-0 = <&pinmux-i3c>;
           pinctrl-names = "default";

           i2c-scl-hz = <400000>;

           i3c-scl-hz = <12000000>;

           status = "okay";

           i3c-dev0: i3c-dev0@420000ABCD12345678 {
                   compatible = "vendor,i3c-dev";

                   reg = <0x42 0xABCD 0x12345678>;

                   status = "okay";
           };

           i2c-dev0: i2c-dev0@380000000000000050 {
                   compatible = "vendor-i2c-dev";

                   reg = <0x38 0x0 0x50>;

                   status = "okay";
           };
   };

I3C Devices
-----------

For I3C devices, the ``reg`` property has 3 elements:

* The first one is the static address of the device.

  * Can be zero if static address is not used. Address will be
    assigned during DAA (Dynamic Address Assignment).

  * If non-zero and property ``assigned-address`` is not set,
    this will be the address of the device after SETDASA
    (Set Dynamic Address from Static Address) is issued.

* Second element is the upper 16-bit of the Provisioned ID (PID)
  which contains the manufacturer ID left-shifted by 1. This is
  the bits 33-47 (zero-based) of the 48-bit Provisioned ID.

  * Must be non-zero. A zero second element marks the node as an
    I\ :sup:`2`\ C device, as described below, so the helper macros
    create a legacy I\ :sup:`2`\ C descriptor for it instead of an
    I3C one. Specify the PID even when the device is addressed by
    SETDASA and the PID is otherwise unused.

* Third element contains the lower 32-bit of the Provisioned ID
  which is a combination of the part ID (left-shifted by 16,
  bits 16-31 of the PID) and the instance ID (left-shifted by 12,
  bits 12-15 of the PID).

Note that the unit-address (the part after ``@``) must match
the ``reg`` property fully where each element is treated as
32-bit integer, combining to form a 96-bit integer. This is
required for properly generating device tree macros.

I\ :sup:`2`\ C Devices
----------------------

For I\ :sup:`2`\ C devices where the device driver has support for
working under I3C bus, the device node can be described as
a child of the I3C controller. If the device driver is written to
only work with I\ :sup:`2`\ C controllers, define the node under
the I\ :sup:`2`\ C virtual controller as described below.
Otherwise, the ``reg`` property, similar to I3C devices,
has 3 elements:

* The first one is the static address of the device. This must be
  a valid address as I\ :sup:`2`\ C devices do not support
  dynamic address assignment.

* Second element is always zero.

  * This is used by various helper macros to determine whether
    the device tree entry corresponds to a I\ :sup:`2`\ C device.

* Third element is the LVR (Legacy Virtual Register):

  * bit[31:8] are unused.

  * bit[7:5] are the I\ :sup:`2`\ C device index:

    * Index ``0``

      * I3C device has a 50 ns spike filter where it is not
        affected by high frequency on SCL.

    * Index ``1``

      * I\ :sup:`2`\ C device does not have a 50 ns spike filter but
        can work with high frequency on SCL.

    * Index ``2``

      * I3C device does not have a 50 ns spike filter and
        cannot work with high frequency on SCL.

  * bit[4] is the I\ :sup:`2`\ C mode indicator:

    * ``0`` is FM+ mode.

    * ``1`` is FM mode.

Similar to I3C devices, the unit-address must match the ``reg``
property fully where each element is treated as 32-bit integer,
combining to form a 96-bit integer.

Device Drivers for I3C Devices
==============================

All of the transfer functions of I3C controller API require
the use of device descriptors, :c:struct:`i3c_device_desc`.
This struct contains runtime information about a I3C device,
such as, its dynamic address, BCR, DCR, MRL and MWL. Therefore,
the device driver of a I3C device should grab a pointer to
this device descriptor from the controller using
:c:func:`i3c_device_find`. This function takes an ID parameter
of type :c:struct:`i3c_device_id` for matching. The returned
pointer can then be used in subsequent API calls to
the controller.

I\ :sup:`2`\ C Devices under I3C Bus
====================================

Since I3C is backward compatible with I\ :sup:`2`\ C, the I3C controller
API can accommodate I2C API calls without modifications if the controller
device driver implements the I2C API. This has the advantage of using
existing I2C devices without any modifications to their device drivers.
However, since the I3C controller API works on device descriptors,
any calls to I2C API will need to look up the corresponding device
descriptor from the I2C device address. This adds a bit of processing
cost to any I2C API calls.

On the other hand, a device driver can be extended to utilize native
I2C device support via the I3C controller API. During device
initialization, :c:func:`i3c_i2c_device_find` needs to be called to
retrieve the pointer to the device descriptor. This pointer can be used
in subsequent API calls.

Note that, with either methods mentioned above, the devicetree node of
the I2C device must be declared according to I3C standard:

The I\ :sup:`2`\ C virtual controller device driver provides a way to
interface I\ :sup:`2`\ C devices on the I3C bus where the associated
device drivers can be used as-is without modifications. This requires
adding an intermediate node in the device tree:

.. code-block:: devicetree

   i3c0: i3c@10000 {
           <... I3C controller related properties ...>
           <... Nodes of I3C devices, if any ...>

           i2c-dev0: i2c-dev0@420000000000000050 {
                   compatible = "vendor-i2c-dev";

                   reg = <0x42 0x0 0x50>;

                   status = "okay";
           };
   };

Configuration Options
*********************

Related configuration options:

* :kconfig:option:`CONFIG_I3C`
* :kconfig:option:`CONFIG_I3C_USE_IBI`
* :kconfig:option:`CONFIG_I3C_IBI_MAX_PAYLOAD_SIZE`
* :kconfig:option:`CONFIG_I3C_CONTROLLER_INIT_PRIORITY`

API Reference
*************

.. doxygengroup:: i3c_interface
.. doxygengroup:: i3c_ccc
.. doxygengroup:: i3c_addresses
.. doxygengroup:: i3c_target_device

.. _I3C Specification: https://www.mipi.org/specifications/i3c-sensor-specification
