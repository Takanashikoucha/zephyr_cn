.. _external_module_canopennode:

CANopenNode 协议栈
##################

简介
****

`CANopenNode`_ 是一个自由且开源的 CANopen 协议栈。用于将该协议栈与 Zephyr 集成的胶水代码位于专门的 `CANopenNodeZephyr`_ 仓库中，该仓库将 CANopenNode 作为 Git 子模块包含。

CANopenNode 和 CANopenNodeZephyr 均采用 Apache-2.0 许可。

在 Zephyr 中使用
****************

要将 CANopenNodeZephyr 作为 Zephyr :ref:`模块 <modules>` 引入，可以将其作为 West 项目添加到 ``west.yaml`` 文件，或通过添加子 manifest（例如 ``zephyr/submanifests/canopennodezephyr.yaml``）文件引入，内容如下，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: canopennodezephyr
         url: https://github.com/zephyrproject-rtos/CANopenNodeZephyr.git
         revision: main
         submodules:
           - path: CANopenNode
         path: custom/canopennodezephyr # adjust the path as needed

.. _CANopenNode:
   https://github.com/CANopenNode/CANopenNode

.. _CANopenNodeZephyr:
   https://github.com/zephyrproject-rtos/CANopenNodeZephyr
