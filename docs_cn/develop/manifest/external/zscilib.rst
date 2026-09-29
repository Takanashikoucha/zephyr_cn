.. _external_module_zscilib:

Zephyr Scientific Library（zscilib）
###################################

简介
****

Zephyr Scientific Library（`zscilib`_）尝试为资源受限的嵌入式
硬件设备提供一组适用于科学计算、数据分析和数据操作的函数。

它完全用 C 编写。虽然该库的主要开发目标是 Zephyr 项目，但力求
尽可能可移植。包含一个独立的参考项目，用于在非 Zephyr 项目中
使用该库。

在 Zephyr 中使用
****************

要将 zscilib 作为 Zephyr 模块引入，可以将其作为 West 项目添加到
``west.yaml`` 文件，或通过添加子 manifest（例如
``zephyr/submanifests/zscilib.yaml``）文件引入，内容如下，然后
运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: zscilib-
         url: https://github.com/zephyrproject-rtos/zscilib
         revision: master
         path: modules/lib/zscilib # adjust the path as needed

更详细的步骤和 API 文档请参阅 `zscilib 文档`_ 以及提供的
`zscilib 示例`_。

运行示例应用
============

要使用 qemu 运行其中一个示例应用，运行以下命令：

.. code-block:: console

    $ west build -p -b qemu_cortex_a53 \
        samples/matrix/mult -t run
    ...
    *** Booting Zephyr OS build zephyr-v2.6.0-536-g89212a7fbf5f  ***
    zscilib matrix mult demo


    mtx multiply output (4x3 * 3x4 = 4x4):

    14.000000 17.000000 20.000000 23.000000
    35.000000 44.000000 53.000000 62.000000
    56.000000 71.000000 86.000000 101.000000
    7.000000 9.000000 11.000000 13.000000

按 CTRL+A 然后按 x 退出 qemu。

运行单元测试
============

要运行该库的单元测试，运行以下命令：

.. code-block:: console

    $ west twister --inline-logs -p mps2/an521/cpu0 -T tests
    See the tests folder for further details.

参考资料
********

.. _zscilib:
    https://github.com/zephyrproject-rtos/zscilib

.. _zscilib 文档:
    https://zephyrproject-rtos.github.io/zscilib/

.. _zscilib 示例:
    https://github.com/zephyrproject-rtos/zscilib/tree/master/samples
