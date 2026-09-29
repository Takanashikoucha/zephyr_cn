.. _bluetooth-ctlr-arch:

LE
Controller
#############

Overview
********

.. image::
   img/ctlr_overview.png

#.
HCI

   *
   Host
   Controller
   Interface
   Bluetooth
   standard
   *
   Provides
   Zephyr
   Bluetooth
   HCI
   Driver

#.
HAL

   *
   Hardware
   Abstraction
   Layer
   *
   Vendor
   Specific
   and
   Zephyr
   Driver
   usage

#.
Ticker

   *
   Soft
   real
   time
   radio/resource
   scheduling

#.
LL_SW

   *
   Software
   based
   Link
   Layer
   implementation
   *
   States
   and
   roles
   control
   procedures
   packet
   controller

#.
Util

   *
   Bare
   metal
   memory
   pool
   management
   *
   Queues
   of
   variable
   count
   lockless
   usage
   *
   FIFO
   of
   fixed
   count
   lockless
   usage
   *
   Mayfly
   concept
   based
   deferred
   ISR
   executions


Architecture
************
