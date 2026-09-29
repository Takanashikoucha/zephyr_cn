.. _external_module_dtsh:

DTSh
####

简介
****

`DTSh <DTSh-Handbook_>`_ 是一个交互式 DTS 文件查看器，带有
shell 风格的命令行界面：

- 轻松*导航*和*可视化* devicetree
- 根据支持的总线协议、binding、生成的 IRQ、内存大小，或
  "sensor"、"PWM" 等关键字查找节点
- 将命令输出重定向到文件（文本、HTML、SVG），
  用于记录硬件配置或简单记笔记
- 上下文自动补全、命令历史、语义高亮、用户配置
- 可脚本化（即批处理模式）

该 Zephyr 模块将 DTSh 作为 West 扩展添加到您的 Zephyr 工作区。

在 Zephyr 中使用
****************

要安装 DTSh 模块，需要定义自己的 manifest 文件，
或通过添加子 manifest 引入。

例如，假设与 `Zephyr 入门指南`_ 相同的路径，
创建 ``zephyrproject/zephyr/submanifests/dtsh.yaml``，内容如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: dtsh
         url: https://github.com/dottspina/dtsh.git
         revision: zephyr
         path: modules/tools/dtsh
         west-commands: scripts/west-commands.yml

然后更新工作区并安装 DTSh 依赖：

.. code-block:: sh

   west update dtsh
   west packages -m dtsh pip --install

.. note::

   ``west update dtsh`` 会从 `DTSh 项目 <DTSh-project_>`_ 拉取所有
   tags：请忽略它们，它们不对应该 Zephyr 模块的版本，与此处完全无关。

West 命令
*********

安装完成后，该项目/模块应提供 ``west dtsh`` 命令。

.. code-block:: console

   $ west build
   $ west dtsh
   dtsh (0.2.5-zephyr): Shell-like interface with Devicetree
   How to exit: q, or quit, or exit, or press Ctrl-D

   /
   > cd &flash_controller

   /soc/flash-controller@4001e000
   > find -E --also-known-as (image|storage).* --format NKd -T
                               Also Known As               Description
                               ───────────────────────────────────────────────────────────────────────────────────
   flash-controller@4001e000    flash_controller            Nordic NVMC (Non-Volatile Memory Controller)
   └── flash@0                  flash0                      Flash node
       └── partitions                                       This binding is used to describe fixed partitions…
           ├── partition@c000   image-0, slot0_partition    Each child node of the fixed-partitions node represents…
           ├── partition@82000  image-1, slot1_partition    Each child node of the fixed-partitions node represents…
           └── partition@f8000  storage, storage_partition  Each child node of the fixed-partitions node represents…

完整的 West 命令概要请运行 ``west dtsh -h``。

.. note::

   建议将模块安装到默认位置 ``modules/tools/dtsh``。
   否则，运行 ``west dtsh`` 之前务必设置 ``ZEPHYR_BASE`` 环境变量。

参考资料
********

- `DTSh 项目 <DTSh-project_>`_
- `DTSh 手册 <DTSh-Handbook_>`_
- `dtsh 模块 <dtsh-module_>`_

.. _DTSh-project: https://github.com/dottspina/dtsh

.. _DTSh-Handbook: https://dottspina.github.io/dtsh/handbook.html

.. _dtsh-module: https://github.com/dottspina/dtsh/tree/zephyr

.. _Zephyr 入门指南: https://docs.zephyrproject.org/latest/develop/getting_started/
