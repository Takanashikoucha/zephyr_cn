.. _index:

Zephyr 中文文档
###############

欢迎来到 Zephyr 实时操作系统的中文文档。

本仓库是 Zephyr RTOS 的中文文档与源代码阅读指南，帮助你：

- **理解 Zephyr 架构**：从内核到子系统的完整技术文档
- **阅读源代码**：系统化的源码导读，带你走读关键代码
- **上手开发**：从入门到进阶的完整开发指南

.. toctree::
   :maxdepth: 2
   :caption: 文档目录

   introduction/index
   kernel/index
   develop/index
   build/index
   hardware/index

.. toctree::
   :maxdepth: 1
   :caption: 源码阅读指南

   源码阅读指南

.. note::

   本仓库的文档基于 Zephyr 官方英文文档翻译与改编，
   源代码阅读指南为原创内容。
   上游英文文档请访问 https://docs.zephyrproject.org/


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
.. only:: development

   .. admonition:: Welcome to Zephyr Project Documentation for the ``main`` tree (|version|).
      :class: welcome

      .. raw:: html

         <p>
           Use the <a href="#" onclick="openVersionSelector(); return false;">version selector</a>
           for the documentation of previously released versions.
         </p>

.. raw:: html
   :file: index.html

.. toctree::
   :maxdepth: 1
   :hidden:

   introduction/index.rst
   develop/index.rst
   kernel/index.rst
   services/index.rst
   build/index.rst
   hardware/index.rst
   contribute/index.rst
   project/index.rst
   security/index.rst
   safety/index.rst
   samples/index.rst
   boards/index.rst
   releases/index.rst