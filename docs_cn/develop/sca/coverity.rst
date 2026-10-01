.. _coverity:

Coverity
#########

Coverity Scan 是一个由 Black Duck 提供的服务，为已在 Coverity Scan 注册其产品的开源代码开发者提供开源编码项目的分析结果。

这个集成只在 scan.coverity.com 和通过该服务可用的工具分发上测试过。

生成构建数据文件
***************************

要使用这个集成，coverity 工具分发必须在你的 :envvar:`PATH` 环境中找到，并且 :ref:`west build <west-building>` 应该用 ``-DZEPHYR_SCA_VARIANT=coverity`` 参数调用，例如

.. code-block:: shell

    west build -b qemu_cortex_m3 samples/hello_world -- -DZEPHYR_SCA_VARIANT=coverity

扫描的结果将生成为 :file:`build/sca/coverity`。

你也可以设置 :envvar:`COVERITY_OUTPUT_DIR` 作为多个和增量扫描结果的目的地。

结果分析
****************

按照 https://scan.coverity.com 上的说明上传结果。
