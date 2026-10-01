.. _external_module_lz4:

LZ4 - 极快的压缩算法
################################

简介
************

LZ4 是一种无损压缩算法，提供每核心大于 500 MB/s 的压缩速度，可随多核 CPU 扩展。它拥有一个极快的解码器，速度达每核心多个 GB/s，通常在多核系统上达到 RAM 速度极限。

速度可以通过选择“加速”因子动态调整，以压缩比换取更快的速度。另一方面，也提供了一个高压缩比的衍生版本 LZ4_HC，以 CPU 时间换取更高的压缩比。所有版本都具有相同的解压速度。

LZ4 也兼容字典压缩，在 API 和 CLI 级别均如此。它可以摄取任何输入文件作为字典，尽管只有最后 64KB 会被使用。这个能力可以与其他能力组合使用。

在 Zephyr 中使用
*****************

要将 lz4 作为 Zephyr 模块引入，可以将其作为 West 项目添加到 ``west.yaml`` 文件，或通过添加一个子 manifest 文件（例如 ``zephyr/submanifests/lz4.yaml``，内容如下）引入，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: lz4
         url: https://github.com/zephyrproject-rtos/lz4
         revision: zephyr
         path: modules/lib/lz4 # 按需调整路径

更详细的操作步骤和 API 文档请参阅 `lz4 文档`_ 以及提供的 `lz4 示例`_。

参考资料
*********

.. _lz4 文档:
   https://github.com/lz4/lz4/tree/dev/doc

.. _lz4 示例:
   https://github.com/zephyrproject-rtos/lz4/tree/zephyr/zephyr/samples
