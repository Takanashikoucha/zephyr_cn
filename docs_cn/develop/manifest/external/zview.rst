.. _external_module_zview:

ZView
#####

简介
****

`ZView <zview_>`_ 是 Zephyr RTOS 应用的运行时可视化工具，通过
SWD 调试探针提供实时的全系统线程和 heap 统计。

它读取内核对象位置，并通过 APB 总线"不停机"地检查内存，
使 target 上的占用几乎为零——无需 UART、无需 Shell、除标准
线程内省选项外无额外 Kconfig 开销。

该工具完全在主机上作为 TUI 应用运行，显示实时栈水位、
每个线程的 CPU 使用率和 heap 运行时统计。

在 Zephyr 中使用
****************

在工作区 manifest 中声明该模块，或通过子 manifest 引入。
例如，创建 ``zephyrproject/zephyr/submanifests/zview.yaml``，
内容如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: zview
         url: https://github.com/wkhadgar/zview
         revision: main
         path: modules/tools/zview
         west-commands: scripts/west-commands.yml

应用必须使用相应的 Kconfig 选项编译并运行。最低要求：

.. code-block:: cfg

   CONFIG_INIT_STACKS=y
   CONFIG_THREAD_MONITOR=y
   CONFIG_THREAD_STACK_INFO=y

然后更新工作区，并通过集成的 west 命令运行 ZView：

.. code-block:: sh

   west update
   west zview

支持的完整选项列表和 CLI 用法请参见 `ZView 仓库 <zview_>`_。

参考资料
********

- `ZView 仓库 <zview_>`_

.. _zview: https://github.com/wkhadgar/zview
