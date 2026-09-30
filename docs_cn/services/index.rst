.. _os_services:

Services
########

Zephyr
provide
一
个
comprehensive
的
subsystems
和
associated
services
set
applications
可以
leverage
它们。
这些
services
expose
standardized
的
APIs
它们
abstract
away
hardware
implementation
details
使
applications
portable
跨
不同
的
platforms。

.. grid::
   1
   :class-container:
   sd-index-grid
   :gutter:
   0

   .. grid-item-card::
   :ref:`Connectivity
   <connectivity_services>`
   :class-card:
   sd-index-card

   .. rst-class::
   sd-index-watermark

   :material-twotone:`hub;7em`

   .. toctree::
      :maxdepth:
      2

      connectivity/index

   .. grid-item-card::
   :ref:`Input
   /
   Output
   <io_services>`
   :class-card:
   sd-index-card

   .. rst-class::
   sd-index-watermark

   :material-twotone:`swap_horiz;7em`

   .. toctree::
      :maxdepth:
      2

      io

   .. grid-item-card::
   :ref:`Inter
   Process
   Communication
   <ipc_services>`
   :class-card:
   sd-index-card


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
      .. toctree::
         :maxdepth: 2

         power_management

   .. grid-item-card:: :ref:`Security <security_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`security;7em`

      .. toctree::
         :maxdepth: 2

         security

   .. grid-item-card:: :ref:`Device Management <device_mgmt>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`devices;7em`

      .. toctree::
         :maxdepth: 2

         device_mgmt/index

   .. grid-item-card:: :ref:`Algorithms & Data <algorithms_services>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`functions;7em`

      .. toctree::
         :maxdepth: 2

         algorithms

   .. grid-item-card:: :ref:`Frameworks <frameworks>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`widgets;7em`

      .. toctree::
         :maxdepth: 2

         frameworks

   .. grid-item-card:: :ref:`OS Abstraction <osal>`
      :class-card: sd-index-card

      .. rst-class:: sd-index-watermark

      :material-twotone:`layers;7em`

      .. toctree::
         :maxdepth: 2

         portability/index