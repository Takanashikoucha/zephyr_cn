.. _sparse:

Sparse 支持
##############

`Sparse <https://www.kernel.org/doc/html/latest/dev-tools/sparse.html>`__
是一款静态代码分析工具。
除了执行常见的代码分析任务外，它还支持一个
``address_space`` 属性，允许在 C 代码中引入不同的地址
空间，随后验证指向不同地址空间的指针
不会相互混淆。此外它还支持一个 ``force``
属性，应使用它来在不同地址空间
之间转换指针。目前 Zephyr 引入了一个自定义地址空间
``__cache``，用于标识 Xtensa 架构上来自缓存地址范围的指针。
这有助于识别缓存地址与非缓存地址
被混淆的情况。

使用 Sparse 运行
*******************

要运行 sparse 验证构建，应使用 ``-DZEPHYR_SCA_VARIANT=sparse`` 参数
调用 :ref:`west build <west-building>`，例如：

.. code-block:: shell

    west build -d hello -b intel_adsp/cavs25 zephyr/samples/hello_world -- -DZEPHYR_SCA_VARIANT=sparse
