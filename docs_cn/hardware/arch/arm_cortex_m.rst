.. _arm_cortex_m_developer_guide:

Arm
Cortex-M
Developer
Guide
############################

Overview
********

本
页
包含
关于
Arm
Cortex-M
architecture
在
Zephyr
RTOS
中
移植
状态
的
详细
信息
并
描述
开发
基于
Arm
Cortex-M
platforms
的
Zephyr
应用
时
的
关键
方面。

Key
supported
features
**********************

下面
的
表
总结
不同
Arm
Cortex-M
implementation
variants
中
关键
OS
功能
的
状态。


+---------------------------------+-----------------------------------+-----------------+---------+--------+-----------+--------+---------+------------+------------+------------+
|
                                 |
                                   |
**Processor
families**
                                                                      |
            |
+---------------------------------+-----------------------------------+-----------------+---------+--------+-----------+--------+---------+------------+------------+------------+
|
Architecture
variant
            |
                                   |
Arm
v6-M
                  |
Arm
v7-M
                    |
Arm
v8-M
             |
Arm
v8.1-M
              |
+---------------------------------+-----------------------------------+-----------------+---------+--------+-----------+--------+---------+------------+------------+------------+
|
                                 |
                                   |
**M0/M1**
       |
**M0+**
|
**M3**
|
   **M4**
  |
**M7**
|
**M23**
|
   **M33**
  |
  **M55**
   |
  **M85**
   |
+---------------------------------+-----------------------------------+-----------------+---------+--------+-----------+--------+---------+------------+------------+------------+
|
**OS
Features**
                 |
                                   |
                                                                                             |
            |
+---------------------------------+-----------------------------------+-----------------+---------+--------+-----------+--------+---------+------------+------------+------------+
|
Programmable
fault
              |
                                   |
                 |
         |
        |
           |
        |
         |
            |
            |
            |
|
IRQ
priorities
                  |
                                   |
        N
        |
   N
     |
   Y
    |
    Y
      |
    Y
   |
    N
    |
     Y
      |
   Y
        |
   Y
        |
+---------------------------------+-----------------------------------+-----------------+---------+--------+-----------+--------+---------+------------+------------+------------+
|
Single-thread
kernel
support
    |
                                   |
        Y
        |
   Y
     |
   Y
    |
    Y
      |
    Y
   |
    Y
    |
     Y
      |
   Y
        |
   Y
        |
+---------------------------------+-----------------------------------+-----------------+---------+--------+-----------+--------+---------+------------+------------+------------+
|
Thread
local
storage
support
    |
                                   |
        Y
        |
   Y
     |
   Y
    |
    Y
      |
    Y
   |
    Y
    |
     Y
      |
   Y
        |
   Y
        |
+---------------------------------+-----------------------------------+-----------------+---------+--------+-----------+--------+---------+------------+------------+------------+
|
**Interrupt
handling**
          |
                                   |
                                                                                             |
            |
+---------------------------------+-----------------------------------+-----------------+---------+--------+-----------+--------+---------+------------+------------+------------+
|
                                 |
   Regular
interrupts
              |
        Y
        |
   Y
     |
   Y
    |
    Y
      |
    Y
   |
    Y
    |
     Y
      |
   Y
        |
   Y
        |
+---------------------------------+-----------------------------------+-----------------+---------+--------+-----------+--------+---------+------------+------------+------------+
|
                                 |
   Dynamic
interrupts
              |
        Y
        |
   Y
     |
   Y
    |
    Y
      |
    Y
   |
    Y
    |
     Y
      |
   Y
        |
   Y
        |


.. note::

   以下为原文（待翻译）

* ZLIs are assigned the highest configurable priority level
* SVCs are assigned the second highest configurable priority level
* Regular HW interrupts are assigned priority levels lower than SVC.

The priority level configuration in Cortex-M is implemented in
:file:`include/zephyr/arch/arm/cortex_m/exception.h`.

Locking and unlocking IRQs
--------------------------

In Baseline Cortex-M locking interrupts is implemented using the PRIMASK register.

.. code-block:: c

  arch_irq_lock()

will set the PRIMASK register to 1, eventually, masking all IRQs with configurable
priority. While this fulfils the OS requirement of locking interrupts, the consequence
is that kernel runtime errors (triggering SVCs) will escalate to HardFault.

In Mainline Cortex-M locking interrupts is implemented using the BASEPRI register (Mainline
Cortex-M builds select :kconfig:option:`CONFIG_CPU_CORTEX_M_HAS_BASEPRI` to signify that BASEPRI register is
implemented.). By modifying BASEPRI (or BASEPRI_MAX) arch_irq_lock() masks all system and HW
interrupts with the exception of

* SVCs
* processor faults
* ZLIs

This allows zero latency interrupts to be triggered inside OS critical sections.
Additionally, this allows system (processor and kernel) faults to be handled by Zephyr
in *exactly the same way*, regardless of whether IRQs have been locked or not when the
error occurs. It also allows for system calls to be dispatched while IRQs are locked.

.. note::

   Mainline Cortex-M fault handling is designed and configured in a way that all processor
   and kernel faults are handled by the corresponding exception handlers and never result
   in HardFault escalation. In other words, a HardFault may only occur in Zephyr applications
   that have modified the default fault handling configurations. The main reason for this
   design was to reserve the HardFault exception for handling exceptional error conditions
   in safety critical applications.

Dynamic direct interrupts
-------------------------

Cortex-M builds support the installation of direct interrupt service routines during
runtime. Direct interrupts are designed for performance-critical interrupt
handling and do not go through all of the common Zephyr interrupt handling
code.

Direct dynamic interrupts are enabled via switching on
:kconfig:option:`CONFIG_DYNAMIC_DIRECT_INTERRUPTS`.

Note that enabling direct dynamic interrupts requires enabling support for
dynamic interrupts in the kernel, as well (see :kconfig:option:`CONFIG_DYNAMIC_INTERRUPTS`).

Zero Latency interrupts
-----------------------

As described above, in Mainline Cortex-M applications, the Zephyr kernel reserves
the highest configurable interrupt priority level for its own use (SVC). SVCs will
not be masked by interrupt locking. Zero-latency interrupt can be used to set up
an interrupt at the highest interrupt priority which will not be blocked by interrupt
locking. To use the ZLI feature :kconfig:option:`CONFIG_ZERO_LATENCY_IRQS` needs to be enabled.

Zero latency IRQs have minimal interrupt latency, as they will always preempt regular HW
or system interrupts.

Note, however, that since ZLI ISRs will run at a priority level higher than the kernel
exceptions they **cannot use** any kernel functionality. Additionally, since the ZLI
interrupt priority level is equal to processor fault priority level, faults occurring
in ZLI ISRs will escalate to HardFault and will not be handled in the same way as regular
processor faults. Developers need to be aware of this limitation.

CPU Idling
==========

The Cortex-M architecture port implements both k_cpu_idle()
and k_cpu_atomic_idle(). The implementation is present in
:file:`arch/arm/core/cortex_m/cpu_idle.c`.

In both implementations, the processor
will attempt to put the core to low power mode.
In k_cpu_idle() the processor ends up executing WFI (Wait For Interrupt)
instruction, while in k_cpu_atomic_idle() the processor will
execute a WFE (Wait For Event) instruction.

When using the CPU idling API in Cortex-M it is important to note the
following:

* Both k_cpu_idle() and k_cpu_atomic_idle() are *assumed* to be invoked
  with interrupts locked. This is taken care of by the kernel if the APIs
  are called by the idle thread.
* After waking up from low power mode, both functions will *restore*
  interrupts unconditionally, that is, regardless of the interrupt lock
  status before the CPU idle API was called.

The Zephyr CPU Idling mechanism is detailed in :ref:`cpu_idle`.

Memory protection features
==========================

This section describes certain aspects around memory protection features
in Arm Cortex-M applications.

User mode system calls
----------------------

User mode is supported in Cortex-M platforms that implement the standard (Arm) MPU
or a similar core peripheral logic for memory access policy configuration and
control, such as the NXP MPU for Kinetis platforms. (Currently,
:kconfig:option:`CONFIG_ARCH_HAS_USERSPACE` is selected if :kconfig:option:`CONFIG_ARM_MPU` is enabled
by the user in the board default Kconfig settings).

A thread performs a system call by triggering a (synchronous) SVC exception, where

* up to 5 arguments are placed on registers R1 - R5
* system call ID is placed on register R6.

The SVC Handler will branch to the system call preparation logic, which will perform
the following operations

* switch the thread's PSP to point to the beginning of the thread's privileged
  stack area, optionally reprogramming the PSPLIM if stack limit checking is enabled
* modify CONTROL register to switch to privileged mode
* modify the return address in the SVC exception stack frame, so that after exception
  return the system call dispatcher is executed (in thread privileged mode)

Once the system call execution is completed the system call dispatcher will restore the
user's original PSP and PSPLIM and switch the CONTROL register back to unprivileged mode
before returning back to the caller of the system call.

System calls execute in thread mode and can be preempted by interrupts at any time. A
thread may also be context-switched-out while doing a system call; the system call will
resume as soon as the thread is switched-in again.

The system call dispatcher executes at SVC priority, therefore it cannot be preempted
by HW interrupts (with the exception of ZLIs), which may observe some additional interrupt
latency if they occur during a system call preparation.

MPU-assisted stack overflow detection
-------------------------------------

Cortex-M platforms with MPU may enable :kconfig:option:`CONFIG_MPU_STACK_GUARD` to enable the MPU-based
stack overflow detection mechanism. The following points need to be considered when enabling the
MPU stack guards

* stack overflows are triggering processor faults as soon as they occur
* the mechanism is essential for detecting stack overflows in supervisor threads, or
  user threads in privileged mode; stack overflows in threads in user mode will always be
  detected regardless of :kconfig:option:`CONFIG_MPU_STACK_GUARD` being set.
* stack overflows are always detected, however, the mechanism does not guarantee that
  no memory corruption occurs when supervisor threads overflow their stack memory
* :kconfig:option:`CONFIG_MPU_STACK_GUARD` will normally reserve one MPU region for programming
  the stack guard (in certain Arm v8-M configurations with :kconfig:option:`CONFIG_MPU_GAP_FILLING`
  enabled 2 MPU regions are required to implement the guard feature)
* MPU guards are re-programmed at every context-switch, adding a small overhead to the
  thread swap routine. Compared, however, to the :kconfig:option:`CONFIG_BUILTIN_STACK_GUARD` feature,
  no re-programming occurs during system calls.
* When :kconfig:option:`CONFIG_HW_STACK_PROTECTION` is enabled on Arm v8-M platforms the native
  stack limit checking mechanism is used by default instead of the MPU-based stack overflow
  detection mechanism; users may override this setting by manually enabling :kconfig:option:`CONFIG_MPU_STACK_GUARD`
  in these scenarios.

Pointer Authentication and Branch Target Identification (PACBTI)
================================================================

The Armv8.1-M Pointer Authentication and Branch Target Identification (PACBTI) extension is an
optional extension for the Armv8.1-M architecture profile and consists of the implementation of the
following control-flow integrity approaches:

* Return address signing and authentication (PAC-RET) as a mitigation for Return Oriented Programming (ROP) style attack.
* BTI instruction placement (BTI) as a mitigation for Jump Oriented Programming (JOP) style attacks.

When hardware support is present (e.g., Cortex-M85) and compiler support is available, PACBTI can be
enabled at build time in Zephyr by selecting one of the below configs:

- :kconfig:option:`CONFIG_ARM_PACBTI_STANDARD`
- :kconfig:option:`CONFIG_ARM_PACBTI_PACRET`
- :kconfig:option:`CONFIG_ARM_PACBTI_PACRET_LEAF`
- :kconfig:option:`CONFIG_ARM_PACBTI_BTI`
- :kconfig:option:`CONFIG_ARM_PACBTI_PACRET_BTI`
- :kconfig:option:`CONFIG_ARM_PACBTI_PACRET_LEAF_BTI`
- :kconfig:option:`CONFIG_ARM_PACBTI_NONE`

The config options ensures that compiler flags enabling PACBTI instructions are added to the build,
specifically:

- ``-mbranch-protection=`` for GCC toolchains.

Further, :kconfig:option:`CONFIG_ARM_PAC` and :kconfig:option:`CONFIG_ARM_BTI` are
automatically selected based on the branch protection option chosen for
:kconfig:option:`CONFIG_ARM_PACBTI`. These configuration options enforce PACBTI by enabling
corresponding PACBTI bits in CONTROL register and in the FVP.

To further enhance pointer authentication, Zephyr supports using cryptographically secure,
per-thread PAC keys by enabling :kconfig:option:`CONFIG_ARM_PAC_PER_THREAD`.
For more details on key generation sources and configuration, refer to the Kconfig help for
:kconfig:option:`CONFIG_ARM_PAC_PER_THREAD`.

**Limitations:**

- Only builds targeting Armv8.1-M Mainline processors with PACBTI hardware support (e.g.,
  Cortex-M85) are able to fully use this feature.
- Zephyr’s integrated SDK currently includes GCC 12.2 which does not support PACBTI so external GCC
  toolchains (14.3 or later recommended) must be used for PACBTI support.
  Refer to `this document <https://docs.zephyrproject.org/latest/develop/toolchains/index.html>`_ on how to set up
  toolchains.

For more information about PACBTI, refer to the official `Arm documentation <https://developer.arm.com/documentation/109576/latest/>`_
and also `Arm community blog <https://community.arm.com/arm-community-blogs/b/architectures-and-processors-blog/posts/armv8-1-m-pointer-authentication-and-branch-target-identification-extension>`_

.. _arm_cortex_m_mpu_considerations:

Memory map and MPU considerations
=================================

Fixed MPU regions
-----------------

By default, when :kconfig:option:`CONFIG_ARM_MPU` is enabled a set of *fixed* MPU regions
are programmed during system boot.

* One MPU region programs the entire flash area as read-execute.
  User can override this setting by enabling :kconfig:option:`CONFIG_MPU_ALLOW_FLASH_WRITE`,
  which programs the flash with RWX permissions. If :kconfig:option:`CONFIG_USERSPACE` is
  enabled unprivileged access on the entire flash area is allowed.
* One MPU region programs the entire SRAM area with privileged-only
  RW permissions. That is, an  MPU region is utilized to disallow execute permissions on
  SRAM. (An exception to this setting is when :kconfig:option:`CONFIG_MPU_GAP_FILLING` is disabled (Arm v8-M only);
  in that case no SRAM MPU programming is done so the access is determined by the default
  Arm memory map policies, allowing for privileged-only RWX permissions on SRAM).
* All the memory regions defined in the devicetree with the property
  ``zephyr,memory-attr`` defining the MPU permissions for the memory region.
  See the next section for more details.

The above MPU regions are defined in :file:`arch/arm/core/mpu/arm_mpu_regions.c`.
Alternative MPU configurations are allowed by enabling :kconfig:option:`CONFIG_CPU_HAS_CUSTOM_FIXED_SOC_MPU_REGIONS`.
When enabled, this option signifies that the Cortex-M SoC will define and
configure its own fixed MPU regions in the SoC definition.

Fixed MPU regions defined in devicetree
---------------------------------------

When the property ``zephyr,memory-attr`` is present in a memory node, a new MPU
region will be allocated and programmed during system boot. When used with the
:dtcompatible:`zephyr,memory-region` devicetree compatible, it will result in a
linker section being generated associated to that MPU region.

For example, to define a new non-cacheable memory region in devicetree:

.. code-block:: devicetree

   sram_no_cache: memory@20300000 {
        compatible = "zephyr,memory-region", "mmio-sram";
        reg = <0x20300000 0x100000>;
        zephyr,memory-region = "SRAM_NO_CACHE";
        zephyr,memory-attr = <DT_MEM_ARM_MPU_RAM_NOCACHE>;
   };

This will automatically create a new MPU entry in with the correct name, base,
size and attributes gathered directly from the devicetree. See :ref:`cache_guide`
and :ref:`mem_mgmt_api` for more details.

Static MPU regions
------------------

Additional *static* MPU regions may be programmed once during system boot. These regions
are required to enable certain features. See :ref:`cache_guide` for more details.

* a RX region to allow execution from SRAM, when :kconfig:option:`CONFIG_ARCH_HAS_RAMFUNC_SUPPORT` is
  enabled and users have defined functions to execute from SRAM.
* a RX region for relocating text sections to SRAM, when :kconfig:option:`CONFIG_CODE_DATA_RELOCATION_SRAM` is enabled
* a ``nocache`` region to allow for a non-cacheable SRAM area, when :kconfig:option:`CONFIG_NOCACHE_MEMORY` is enabled
* a possibly unprivileged RW region for GCOV code coverage accounting area, when :kconfig:option:`CONFIG_COVERAGE_GCOV` is enabled
* a no-access region to implement null pointer dereference detection, when :kconfig:option:`CONFIG_NULL_POINTER_EXCEPTION_DETECTION_MPU` is enabled

The boundaries of these static MPU regions are derived from symbols exposed by the linker, in
:file:`include/linker/linker-defs.h`.

Dynamic MPU regions
-------------------

Certain thread-specific MPU regions may be re-programmed dynamically, at each thread context switch:

* an unprivileged RW region for the current thread's stack area (for user threads)
* a read-only region for the MPU stack guard
* unprivileged RW regions for the partitions of the current thread's application memory
  domain.


Considerations
--------------

The number of available MPU regions for a Cortex-M platform is a limited resource.
Most platforms have 8 MPU regions, while some Cortex-M33 or Cortex-M7 platforms may
have up to 16 MPU regions. Therefore there is a relatively strict limitation on how
many fixed, static and dynamic MPU regions may be programmed simultaneously. For platforms
with 8 available MPU regions it might not be possible to enable all the aforementioned
features that require MPU region programming. In most practical applications, however,
only a certain set of features is required and 8 MPU regions are, in many cases, sufficient.

In Arm v8-M processors the MPU architecture does not allow programmed MPU regions to
overlap. :kconfig:option:`CONFIG_MPU_GAP_FILLING` controls whether the fixed MPU region
covering the entire SRAM is programmed. When it does, a full SRAM area partitioning
is required, in order to program the  static and the dynamic MPU regions. This increases
the total number of required MPU regions. When :kconfig:option:`CONFIG_MPU_GAP_FILLING` is not
enabled the fixed MPU region covering the entire SRAM is not programmed, thus, the static
and dynamic regions are simply programmed on top of the always-existing background region
(full-SRAM partitioning is not required).
Note, however, that the background SRAM region allows execution from SRAM, so when
:kconfig:option:`CONFIG_MPU_GAP_FILLING` is not set Zephyr is not protected against attacks
that attempt to execute malicious code from SRAM.


Floating point Services
=======================

Both unshared and shared FP registers mode are supported in Cortex-M (see
:ref:`float_v2` for more details).

When FPU support is enabled in the build
(:kconfig:option:`CONFIG_FPU` is enabled), the
sharing FP registers mode (:kconfig:option:`CONFIG_FPU_SHARING`)
is enabled by default. This is done as some compiler configurations
may activate a floating point context by generating FP instructions
for any thread, regardless of whether floating point calculations are
performed, and that context must be preserved when switching such
threads in and out.

The developers can still disable the FP sharing mode in their
application projects, and switch to Unshared FP registers mode,
if it is guaranteed that the image code does not generate FP
instructions outside the single thread context that is allowed
(and supposed) to do so.

Under FPU sharing mode, the callee-saved FPU registers are saved
and restored in context-switch, if the corresponding threads have
an active FP context. This adds some runtime overhead on the swap
routine. In addition to the runtime overhead, the sharing FPU mode

* requires additional memory for each thread to save the callee-saved
  FP registers
* requires additional stack memory for each thread, to stack the caller-saved
  FP registers, upon exception entry, if an FP context is active. Note, however,
  that since lazy stacking is enabled, there is no runtime overhead of FP context
  stacking in regular interrupts (FP state preservation is only activated in the
  swap routine in PendSV interrupt).


Misc
****

Chain-loadable images
=====================

Cortex-M applications may either be standalone images or chain-loadable, for instance,
by a bootloader. Application images chain-loadable by bootloaders (or other applications)
normally occupy a specific area in the flash denoted as their *code partition*.
:kconfig:option:`CONFIG_USE_DT_CODE_PARTITION` will ensure that a Zephyr chain-loadable image
will be linked into its code partition, specified in DeviceTree.

HW initialization at boot
-------------------------

In order to boot properly, chain-loaded applications may require that the core Arm
hardware registers and peripherals are initialized in their reset values. Enabling
:kconfig:option:`CONFIG_INIT_ARCH_HW_AT_BOOT` Zephyr to force the initialization of the
internal Cortex-M architectural state during boot to the reset values as specified
by the corresponding Arm architecture manual.

Software vector relaying
------------------------

In Cortex-M platforms that implement the VTOR register (see :kconfig:option:`CONFIG_CPU_CORTEX_M_HAS_VTOR`),
chain-loadable images relocate the Cortex-M vector table by updating the VTOR register with the offset
of the image vector table.

Baseline Cortex-M platforms without VTOR register might not be able to relocate their
vector table which remains at a fixed location. Therefore, a chain-loadable image will
require an alternative way to route HW interrupts and system exceptions to its own vector
table; this is achieved with software vector relaying.

When a bootloader image enables :kconfig:option:`CONFIG_SW_VECTOR_RELAY`
it is able to relay exceptions and interrupts based on a vector table
pointer that is set by the chain-loadable application. The latter sets
the :kconfig:option:`CONFIG_SW_VECTOR_RELAY_CLIENT` option to instruct the boot
sequence to set the vector table pointer in SRAM so that the bootloader can
forward the exceptions and interrupts to the chain-loadable image's software
vector table.

While this feature is intended for processors without VTOR register, it
may also be used in Mainline Cortex-M platforms.

Code relocation
===============

Cortex-M support the code relocation feature. When
:kconfig:option:`CONFIG_CODE_DATA_RELOCATION_SRAM` is selected,
Zephyr will relocate .text, data and .bss sections
from the specified files and place it in SRAM. It is
possible to relocate only parts of the code sections
into SRAM, without relocating the whole image text
and data sections. More details on the code relocation
feature can be found in :ref:`code_data_relocation`.


Linking Cortex-M applications
*****************************

Most Cortex-M platforms make use of the default Cortex-M
GCC linker script in :file:`include/zephyr/arch/arm/cortex_m/scripts/linker.ld`,
although it is possible for platforms to use a custom linker
script as well.


CMSIS
*****

Cortex-M CMSIS headers are provided through standalone module repositories:

- **CMSIS 5**: `zephyrproject-rtos/cmsis <https://github.com/zephyrproject-rtos/cmsis>`_
- **CMSIS 6**: `zephyrproject-rtos/CMSIS_6 <https://github.com/zephyrproject-rtos/CMSIS_6>`_

Zephyr has begun transitioning to **CMSIS 6** as the default source for Cortex-M core headers.
However, at present, Zephyr includes headers from **both** the CMSIS 6 and legacy CMSIS 5 modules.

The legacy CMSIS 5 headers remain available primarily for compatibility with vendor HALs, while all
new architecture-level development should use **CMSIS 6** headers whenever possible.

:kconfig:option:`CONFIG_CPU_CORTEX_M` selects :kconfig:option:`CONFIG_HAS_CMSIS_CORE` to signify that
CMSIS headers are available for all supported Cortex-M variants.

Testing
*******

A list of unit tests for the Cortex-M porting and miscellaneous features
is present in :file:`tests/arch/arm/`. The tests suites are continuously
extended and new test suites are added, in an effort to increase the coverage
of the Cortex-M architecture support in Zephyr.

QEMU
****

We use QEMU to verify the implemented features of the Cortex-M architecture port in Zephyr.
Adequate coverage is achieved by defining and utilizing a list of QEMU targets,
each with a specific architecture variant and Arm peripheral support list.

The table below lists the QEMU platform targets defined in Zephyr
along with the corresponding Cortex-M implementation variant and the peripherals
these targets emulate.

+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
|                                 | **QEMU target**                                                                                              |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
| Architecture variant            | Arm v6-M           | Arm v7-M                            | Arm v8-M             | Arm v8.1-M                 |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
|                                 | **qemu_cortex_m0** | **qemu_cortex_m3** | **mps2/an385** | **mps2/an521/cpu0**  | **mps3/corstone300/an547** |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
| **Emulated features**           |                                                                                                              |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
| NVIC                            | Y                  | Y                  | Y              | Y                    | Y                          |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
| BASEPRI                         | N                  | Y                  | Y              | Y                    | Y                          |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
| SysTick                         | N                  | Y                  | Y              | Y                    | Y                          |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
| MPU                             | N                  | N                  | Y              | Y                    | Y                          |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
| FPU                             | N                  | N                  | N              | Y                    | N                          |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
| SPLIM                           | N                  | N                  | N              | Y                    | Y                          |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+
| TrustZone-M                     | N                  | N                  | N              | Y                    | N                          |
+---------------------------------+--------------------+--------------------+----------------+----------------------+----------------------------+

Maintainers & Collaborators
***************************

The status of the Arm Cortex-M architecture port in Zephyr is: *maintained*.
The updated list of maintainers and collaborators for Cortex-M can be found
in :file:`MAINTAINERS.yml`.
