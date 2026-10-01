.. _external_module_clutgen:

CLUTGen
#######

简介
****

`CLUTGen <clutgen-zephyr_>`_ 为嵌入式系统自动化创建**查找表（LUT）**，将原始 ADC 读数转换为温度、压力或距离等校准后的物理单位。

给定一组校准样本，CLUTGen 拟合一条插值曲线，并生成可直接用于生产的 ``.c``/``.h`` 文件对，其中完整的 LUT 已为所有可能的 ADC 读数预先计算。运行时转换只需一次数组索引操作，因此可以用恒定且可预测的 ROM 开销，替换 ``math.h`` 等库中代价高昂的 RAM 运算。

该 Zephyr 模块将 CLUTGen 直接集成到 west 构建系统中。LUT 生成在 CMake configure 阶段运行，生成的文件会自动链接到应用中。

在 Zephyr 中使用
****************

在工作区 manifest 中声明该模块，或通过子 manifest 引入。

例如，创建 ``zephyrproject/zephyr/submanifests/clutgen.yaml``，内容如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: clutgen
         url: https://github.com/wkhadgar/clutgen-zephyr
         revision: zephyr
         path: modules/clutgen
         submodules: true

然后更新工作区，并将 Python 依赖安装到 west venv 中：

.. code-block:: sh

   west update
   west packages pip --install

参考资料
********

- `CLUTGen Zephyr 模块 <clutgen-zephyr_>`_
- `CLUTGen CLI 工具 <clutgen-cli_>`_


.. _clutgen-zephyr: https://github.com/wkhadgar/clutgen-zephyr

.. _clutgen-cli: https://github.com/wkhadgar/clutgen
