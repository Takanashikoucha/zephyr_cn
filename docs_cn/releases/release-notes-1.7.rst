.. _zephyr_1.7:

Zephyr
Kernel
1.7.0
####################

我们
pleased
to
announce
Zephyr
kernel
version
1.7.0
的
release。
这
个
release
continue
refinement
of
unified
的
kernel
它
在
1.6.0
kernel
release
中
被
introduced
simplify
overall
的
Zephyr
architecture
和
programming
interfaces。
这
是
last
个
support
deprecated
的
legacy
nano
和
micro
kernel
APIs
的
release
它们
在
1.5.0
release
及
更早
中
found。

这
个
release
introduce
一
个
new
的
native
IP
stack
replacing
legacy
的
uIP
stack
maintain
legacy
的
functionality
add
additional
的
capabilities
并
allow
future
的
improvements。

我们
introduced
support
for
the
RISC
V
和
Xtensa
architectures
且
now
support
6
个
architectures
in
total。

Device
tree
support
for
ARM
based
的
boards
被
added。
Initial
的
device
tree
support
包括
flash/sram
base
address
和
UART
devices。
Board
support
包括
NXP
Kinetis
based
的
SoCs、
ARM
Beetle、
TI
CC3200
LaunchXL、
和
STML32L476
based
的
SoCs。
Plan
是
add
support
for
其他
architectures
且
在
upcoming
的
Zephyr
releases
中
expand
device
support。

以下
sections
provide
detailed
的
lists
of
changes
by
component
自
kernel
version
1.6.0
以来。

Kernel
******

*
Introduction
of
k_poll
API:
k_poll()
在
spirit
上
similar
于
POSIX
poll()
API
它
allow
single
的
thread
monitor
multiple
的
events
而
不
actively
polling
它们
相反
pending
for
一
个
或
多
个
become
ready。
*
Optimized
的
memory
use
of
some
thread
fields
*
Remove
micro/nano
kernel
terminology
的
usage
from
kernel
code
并
introduced
一
个
legacy
option
用于
enable/disable
legacy
APIs。
（using
legacy.h）


Architectures
*************


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
* ``ZEP-1307`` - Plumbing the DTS configuration
* ``ZEP-1308`` - zephyr thread function k_sleep doesn't work with nrf51822
* ``ZEP-1320`` - Update Architecture Porting Guide
* ``ZEP-1321`` - Glossary of Terms needs updating
* ``ZEP-1323`` - Eliminate references to fiber, task, and nanokernel under ./include
* ``ZEP-1324`` - Get rid of references to CONFIG_NANOKERNEL
* ``ZEP-1325`` - Eliminate TICKLESS_IDLE_SUPPORTED option
* ``ZEP-1327`` - Eliminate obsolete kernel directories
* ``ZEP-1329`` - Rename kernel APIs that have nano\_ prefixes
* ``ZEP-1334`` - Add make debug support for QEMU-based boards
* ``ZEP-1337`` - Relocate event logger files
* ``ZEP-1338`` - Update external fs with new FATFS revision 0.12b
* ``ZEP-1342`` - legacy/kernel/test_early_sleep/ fails on EMSK
* ``ZEP-1347`` - sys_bitfield_*() take unsigned long* vs memaddr_t
* ``ZEP-1351`` - FDRM k64f SPI does not work
* ``ZEP-1355`` - Connection Failed to be Established
* ``ZEP-1357`` - iot/dns: Client is broken
* ``ZEP-1358`` - BMI160 accelerometer gives 0 on all axes
* ``ZEP-1361`` - IP stack is broken
* ``ZEP-1363`` - Missing wiki board support page for arm/arduino_101_ble
* ``ZEP-1365`` - Missing wiki board support page for arm/c3200_launchxl
* ``ZEP-1370`` - There's a wiki page for arduino_due but no zephyr/boards support folder
* ``ZEP-1374`` - Add ksdk spi shim driver
* ``ZEP-1387`` - Add a driver for Atmel ataes132a  HW Crypto module
* ``ZEP-1389`` - Add support for KW41 SoC
* ``ZEP-1390`` - Add support for FRDM-KW41Z
* ``ZEP-1393`` - Add ksdk pinmux driver
* ``ZEP-1394`` - Add ksdk gpio driver
* ``ZEP-1395`` - Add data ready trigger to FXOS8700 driver
* ``ZEP-1401`` - Enhance ready queue cache and interrupt exit code to reduce interrupt latency.
* ``ZEP-1403`` - remove CONFIG_OMIT_FRAME_POINTER from ARC boards
* ``ZEP-1405`` - function l2cap_br_conn_req in /subsys/bluetooth/host/l2cap_br.c references uninitialized pointer
* ``ZEP-1406`` - Update sensor driver paths in wiki
* ``ZEP-1408`` - quark_se_c1000_ss enter_arc_state() might need cc and memory clobber
* ``ZEP-1411`` - Deprecate device_sync_call API and use semaphore directly
* ``ZEP-1413`` - [ARC] test/legacy/kernel/test_tickless/microkernel fails to build
* ``ZEP-1415`` - drivers/timer/* code comments still refer to micro/nano kernel
* ``ZEP-1418`` - Add support for Nordic nRF52840 and its DK
* ``ZEP-1419`` - SYS_LOG macros cause potentially bad behavior due to printk/printf selection
* ``ZEP-1420`` - Make the time spent with interrupts disabled deterministic
* ``ZEP-1421`` - BMI160 gyroscope driver stops reporting after 1-5 minutes
* ``ZEP-1422`` - Arduino_101 doesn't response ipv6 ping request after enable echo_client ipv6
* ``ZEP-1427`` - wpanusb dongle / 15.4 communication instability
* ``ZEP-1429`` - NXP MCR20A Driver
* ``ZEP-1432`` - ksdk pinmux driver should expose the public pinmux API
* ``ZEP-1434`` - menuconfig screen shots show nanokernel options
* ``ZEP-1437`` - AIO: Fail to retrieve pending interrupt in ISR
* ``ZEP-1440`` - Kconfig choice for MINIMAL_LIBC vs NEWLIB_LIBC is not selectable
* ``ZEP-1442`` - Samples/net/dhcpv4_client: Build fail as No rule to make target prj\_.conf
* ``ZEP-1443`` - Samples/net/zperf: Build fail as net_private.h can not be found
* ``ZEP-1448`` - Samples/net/mbedtls_sslclient:Build fail as net/ip_buf.h can not be found
* ``ZEP-1449`` - samples: logger_hook
* ``ZEP-1456`` - Asserts on nrf51 running Bluetooth hci_uart sample
* ``ZEP-1457`` - Add SPDX Tags to Zephyr license boilerplate
* ``ZEP-1460`` - Sanity check reports some qemu step failures as 'build_error'
* ``ZEP-1461`` - Add zephyr support to openocd upstream
* ``ZEP-1467`` - Cleanup misc/ and move features to subsystems in subsys/
* ``ZEP-1473`` - ARP cache confused by use of gateway.
* ``ZEP-1474`` - BLE Connection Parameter Request/Response Processing
* ``ZEP-1475`` - k_free documentation should specify that NULL is valid
* ``ZEP-1476`` - echo_client display port unreachable
* ``ZEP-1480`` - Update supported distros in getting started guide
* ``ZEP-1481`` - Bluetooth fails to init
* ``ZEP-1483`` - H:4 HCI driver (h4.c) should rely on UART flow control to avoid dropping packets
* ``ZEP-1487`` - I2C_SS: I2C doesn't set device busy before starting data transfer
* ``ZEP-1488`` - SPI_SS: SPI doesn't set device busy before starting data transfer
* ``ZEP-1489`` - [GATT] Nested Long Characteristic Value Reliable Writes
* ``ZEP-1490`` - [PTS] TC_CONN_CPUP_BV_04_C test case is failing
* ``ZEP-1492`` - Add Atmel SAM family GMAC Ethernet driver
* ``ZEP-1493`` - Zephyr project documentation copyright
* ``ZEP-1495`` - Networking API details documentation is missing
* ``ZEP-1496`` - gpio_pin_enable_callback error
* ``ZEP-1497`` - Cortex-M0 port exception and interrupt priority setting and getting is broken
* ``ZEP-1507`` - fxos8700 broken gpio_callback implementation
* ``ZEP-1512`` - doc-theme has its own conf.py
* ``ZEP-1514`` - samples/bluetooth/ipsp build fail: net/ip_buf.h No such file or directory
* ``ZEP-1525`` - driver: gpio: GPIO driver still uses  nano_timer
* ``ZEP-1532`` - Wrong accelerometer readings
* ``ZEP-1536`` - Convert documentation of PWM samples to RST
* ``ZEP-1537`` - Convert documentation of power management samples to RST
* ``ZEP-1538`` - Convert documentation of zoap samples to RST
* ``ZEP-1539`` - Create documentation in RST for all networking samples
* ``ZEP-1540`` - Convert Bluetooth samples to RST
* ``ZEP-1542`` - Multi Sessions HTTP Server sample
* ``ZEP-1543`` - HTTP Server sample with basic authentication
* ``ZEP-1544`` - Arduino_101 doesn't respond to ipv6 ping request after enable echo_server ipv6
* ``ZEP-1545`` - AON Counter : ISR triggered twice on ARC
* ``ZEP-1546`` - Bug in Zephyr OS high-precision timings sub-system (function sys_cycle_get_32())
* ``ZEP-1547`` - Add support for H7 crypto function and CT2 SMP auth flag
* ``ZEP-1548`` - Python script invocation is inconsistent
* ``ZEP-1549`` - k_cpu_sleep_mode unaligned byte address
* ``ZEP-1554`` - Xtensa integration
* ``ZEP-1557`` - RISC V Port
* ``ZEP-1558`` - Support of user private data pointer in Timer expiry function
* ``ZEP-1559`` - Implement _tsc_read  for ARC architecture
* ``ZEP-1562`` - echo_server/echo_client examples hang randomly after some time of operation
* ``ZEP-1563`` - move board documentation for NRF51/NRF52 back to git tree
* ``ZEP-1564`` - 6lo uncompress_IPHC_header overwrites IPHC fields
* ``ZEP-1566`` - WDT: Interrupt is triggered multiple times
* ``ZEP-1569`` - net/tcp: TCP in server mode doesn't support multiple concurrent connections
* ``ZEP-1570`` - net/tcp: TCP in server mode is unable to close client connections
* ``ZEP-1571`` - Update "Changes from Version 1 Kernel" to include a "How-To Port Apps" section
* ``ZEP-1572`` - Update QMSI to 1.4
* ``ZEP-1573`` - net/tcp: User provided data in net_context_recv is not passed to callback
* ``ZEP-1574`` - Samples/net/dhcpv4_client: Build fail as undefined reference to net_mgmt_add_event_callback
* ``ZEP-1579`` - external links to zephyr technical docs are broken
* ``ZEP-1581`` - [nRF52832] Blinky hangs after some minutes
* ``ZEP-1583`` - ARC: warning: unmet direct dependencies (SOC_RISCV32_PULPINO || SOC_RISCV32_QEMU)
* ``ZEP-1585`` - legacy.h should be disabled in kernel.h with CONFIG_LEGACY_KERNEL=n
* ``ZEP-1587`` - sensor.h still uses legacy APIs and structs
* ``ZEP-1588`` - I2C doesn't work on Arduino 101
* ``ZEP-1589`` - Define yaml descriptions for UART devices
* ``ZEP-1590`` - echo_server run on FRDM-K64F displays BUS FAULT
* ``ZEP-1591`` - wiki: add Networking section and point https://wiki.zephyrproject.org/view/Network_Interfaces
* ``ZEP-1592`` - echo-server does not build with newlib
* ``ZEP-1593`` - /scripts/sysgen should create output using SPDX licensing tag
* ``ZEP-1598`` - samples/philosophers build failed unexpectedly @quark_d2000  section noinit will not fit in region RAM
* ``ZEP-1601`` - Console over Telnet
* ``ZEP-1602`` - IPv6 ping fails using sample application echo_server on FRDM-K64F
* ``ZEP-1611`` - Hardfault after a few echo requests (IPv6 over BLE)
* ``ZEP-1614`` - Use correct i2c device driver name
* ``ZEP-1616`` - Mix up between "network address" and "socket address" concepts in declaration of net_addr_pton()
* ``ZEP-1617`` - mbedTLS server/client failing to run on qemu
* ``ZEP-1619`` - Default value of NET_NBUF_RX_COUNT is too low, causes lock up on startup
* ``ZEP-1623`` - (Parts) of Networking docs still refer to 1.5 world model (with fibers and tasks) and otherwise not up to date
* ``ZEP-1626`` - SPI: spi cannot work in CPHA mode @ ARC
* ``ZEP-1632`` - TCP ACK packet should not be forwarded to application recv cb.
* ``ZEP-1635`` - MCR20A driver unstable
* ``ZEP-1638`` - No (public) analog of inet_ntop()
* ``ZEP-1644`` - Incoming connection handling for UDP is not exactly correct
* ``ZEP-1645`` - API to wait on multiple kernel objects
* ``ZEP-1648`` - Update links to wiki pages for board info back into the web docs
* ``ZEP-1650`` - make clean (or pristine) is not removing all artifacts of document generation
* ``ZEP-1651`` - i2c_dw malfunctioning due to various changes.
* ``ZEP-1653`` - build issue when compiling with LLVM in ISSM (altmacro)
* ``ZEP-1654`` - Build issues when compiling with LLVM(unknown attribute '_alloc_align_)
* ``ZEP-1655`` - Build issues when compiling with LLVM(memory pool)
* ``ZEP-1656`` - IPv6 over BLE no longer works after commit 2e9fd88
* ``ZEP-1657`` - Zoap doxygen documentation needs to be perfected
* ``ZEP-1658`` - IPv6 TCP low on buffers, stops responding after about 5 requests
* ``ZEP-1662`` - zoap_packet_get_payload() should return the payload length
* ``ZEP-1663`` - sanitycheck overrides user's environment for CCACHE
* ``ZEP-1665`` - pinmux: missing default pinmux driver config for quark_se_ss
* ``ZEP-1669`` - API documentation does not follow in-code documentation style
* ``ZEP-1672`` - flash: Flash device binding failed on Arduino_101_sss
* ``ZEP-1674`` - frdm_k64f: With Ethernet driver enabled, application can't start up without connected network cable
* ``ZEP-1677`` - SDK: BLE cannot be initialized/advertised with CONFIG_ARC_INIT=y on Arduino 101
* ``ZEP-1681`` - Save/restore debug registers during soc_sleep/soc_deep_sleep in c1000
* ``ZEP-1692`` - [PTS] GATT/SR/GPA/BV-11-C fails
* ``ZEP-1701`` - Provide an HTTP API
* ``ZEP-1704`` - BMI160 samples fails to run
* ``ZEP-1706`` - Barebone Panther board support
* ``ZEP-1707`` - [PTS] 7 SM/MAS cases fail
* ``ZEP-1708`` - [PTS] SM/MAS/PKE/BI-01-C fails
* ``ZEP-1709`` - [PTS] SM/MAS/PKE/BI-02-C fails
* ``ZEP-1710`` - Add TinyTILE board support
* ``ZEP-1713`` - xtensa: correct all checkpatch issues
* ``ZEP-1716`` - HTTP server sample that does not support up to 10 concurrent sessions.
* ``ZEP-1717`` - GPIO: GPIO LEVEL interrupt cannot work well in deep sleep mode
* ``ZEP-1723`` - Warnings in Network code/ MACROS, when built with ISSM's  llvm/icx compiler
* ``ZEP-1732`` - sample of zoap_server runs error.
* ``ZEP-1733`` - Work on ZEP-686 led to regressions in docs on integration with 3rd-party code
* ``ZEP-1745`` - Bluetooth samples build failure
* ``ZEP-1753`` - sample of dhcpv4_client runs error on Arduino 101
* ``ZEP-1754`` - sample of coaps_server was tested failed on qemu
* ``ZEP-1756`` - net apps: [-Wpointer-sign] build warning raised when built with ISSM's  llvm/icx compiler
* ``ZEP-1758`` - PLL2 is not correctly enabled in STM32F10x connectivity line SoC
* ``ZEP-1763`` - Nordic RTC timer driver not correct with tickless idle
* ``ZEP-1764`` - samples: sample cases use hard code device name, such as "GPIOB" "I2C_0"
* ``ZEP-1768`` - samples: cases miss testcase.ini
* ``ZEP-1774`` - Malformed packet included with IPv6 over 802.15.4
* ``ZEP-1778`` - tests/power: multicore case won't work as expected
* ``ZEP-1786`` - TCP does not work on Arduino 101 board.
* ``ZEP-1787`` - kernel event logger build failed with "CONFIG_LEGACY_KERNEL=n"
* ``ZEP-1789`` - ARC: "samples/logger-hook" crashed __memory_error from sys_ring_buf_get
* ``ZEP-1799`` - timeout_order_test _ASSERT_VALID_PRIO failed
* ``ZEP-1803`` - Error occurs when exercising dma_transfer_stop
* ``ZEP-1806`` - Build warnings with LLVM/icx (gdb_server)
* ``ZEP-1809`` - Build error in net/ip with LLVM/icx
* ``ZEP-1810`` - Build failure in net/lib/zoap with LLVM/icx
* ``ZEP-1811`` - Build error in net/ip/net_mgmt.c with LLVM/icx
* ``ZEP-1839`` - LL_ASSERT in event_common_prepareA
* ``ZEP-1851`` - Build warnings with obj_tracing
* ``ZEP-1852`` - LL_ASSERT in isr_radio_state_close()
* ``ZEP-1855`` - IP stack buffer allocation fails over time
* ``ZEP-1858`` - Zephyr NATS client fails to respond to  server MSG
* ``ZEP-1864`` - llvm icx build warning in tests/drivers/uart/*
* ``ZEP-1872`` - samples/net: the HTTP client sample app must run on QEMU x86
* ``ZEP-1877`` - samples/net: the coaps_server sample app runs failed on Arduino 101
* ``ZEP-1883`` - Enabling Console on ARC Genuino 101
* ``ZEP-1890`` - Bluetooth IPSP sample: Too small user data size