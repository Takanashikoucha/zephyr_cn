.. _dt-bindings:

设备树绑定
###################

单凭设备树只能描述硬件的一半，因为它是一种
相对非结构化的格式。*设备树绑定*（devicetree bindings）提供了
另一半。

设备树绑定声明对节点内容的要求，
并提供关于有效节点内容的语义信息。Zephyr
设备树绑定是自定义格式的 YAML 文件（Zephyr 不使用
Linux 内核所用的 dt-schema 工具）。

这些页面介绍绑定、描述其作用、说明其所在位置，
并解释其数据格式。

.. note::

   关于 Zephyr 内置绑定的参考信息，
   参见 :ref:`devicetree_binding_index`。

.. toctree::
   :maxdepth: 2

   bindings-intro.rst
   bindings-syntax.rst
   bindings-upstream.rst
