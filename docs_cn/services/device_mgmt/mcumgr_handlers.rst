.. _mcumgr_handlers:

MCUmgr 处理器
###############

概述
********

MCUmgr 通过组处理器来运作，组处理器标识与
特定管理领域相关的一组功能，该领域通过一个 16 位标识值
寻址，:c:enum:`mcumgr_group_t` 包含 Zephyr 中可用的管理组及其
对应的组 ID 值。组 ID 包含在 SMP 头中，用于标识
一条命令属于哪个组，此外还有一个 8 位命令 ID，用于标识
该组要执行的功能 - 关于 SMP
协议和头的细节参见 :ref:`mcumgr_smp_protocol_specification`。每个唯一 ID 只能注册一个组。

实现
**************

MCUmgr 处理器可以由应用程序代码或模块代码从外部添加，它们
不需要驻留在上游 Zephyr 树中即可使用。创建处理器的第一步
是
为其创建目录结构，典型的 Zephyr MCUmgr 组布局如下：

.. code-block:: none

   <dir>/grp/<grp_name>_mgmt/
   ├── CMakeLists.txt
   ├── Kconfig
   ├── include
   ├──── <grp_name>_mgmt.h
   ├──── <grp_name>_mgmt_callbacks.h
   ├── src
   └──── <grp_name>_mgmt.c

注意上游 Zephyr MCUmgr 处理器中的头文件驻留在
``zephyr/include/zephyr/mgmt/mcumgr/grp/<grp_name>_mgmt`` 目录中，以使
这些文件
可被应用程序全局包含。

初始头文件 <grp_name>_mgmt.h
================

头文件的用途是提供 MCUmgr 处理器
本身和应用程序代码可使用的定义，例如引用执行
功能的命令 ID。一个示例
文件类似：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/include/example_mgmt.h
   :language: c
   :linenos:

这提供了 2 个命令 ``test`` 和 ``other`` 的定义，并设置
了 SMP 版本 2 错误
响应（其有每组唯一的错误码，而遗留 SMP 版本 1 错误
响应返回 :c:enum:`mcumgr_err_t` - 应始终有一个值为 0 的 OK 错误码
和一个值为 1 的未知错误码。上述示例添加了一个值为 2 的
``not wanted`` 错误码。另外，组 ID 被设为
:c:enumerator:`MGMT_GROUP_ID_PERUSER`，它是用户定义组的起始组 ID，注意
组 ID 必须唯一，因此其他自定义组应使用不同的值，一个
中央索引
头文件（如上游 Zephyr 所拥有的）可用于更
容易地分配组 ID。

初始头文件 <grp_name>_mgmt_callbacks.h
========================================

头文件的用途是提供 MCUmgr 处理器
本身和应用程序代码可使用的定义，例如引用执行
功能的命令 ID。一个示例
文件类似：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/include/example_mgmt_callbacks.h
   :language: c
   :linenos:

这设置了一个单一事件，应用程序（或模块）代码可注册
以在功能处理器执行时接收
回调，这允许改变处理器的流程（即返回
错误而不是继续）。事件组 ID 被设为
:c:enumerator:`MGMT_EVT_GRP_USER_CUSTOM_START`，它是用户定义组的起始事件 ID，注意
事件 ID 必须唯一，因此其他自定义组应使用不同的值，一个
中央索引
头文件（如上游 Zephyr 所拥有的）可用于更
容易地分配事件 ID。

初始源文件 <grp_name>_mgmt.c
================

此源文件的用途是处理传入的 MCUmgr 命令、提供
响应，并
将传输注册到 MCUmgr，使命令被发送到它。一个示例
文件类似：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/src/example_mgmt.c
   :language: c
   :linenos:

上述代码创建了 2 个功能处理器：``test`` 支持读请求且
接受 2
个必需参数，``other`` 支持写请求且
接受 1 个可选参数，
此功能处理器有一个可选的通知回调功能，允许
代码的其他部分监听事件并
采取任何必要的操作，或通过返回
错误来阻止功能进一步执行。关于 MCUmgr 回调
功能的更多细节可在 :ref:`mcumgr_callbacks` 找到。

注意引用自定义 MCUmgr 处理器回调的其他代码须
包含两个
文件：基础 Zephyr 回调包含文件和自定义处理器回调文件，只有
树内 Zephyr
处理器头文件在包含上游 Zephyr 回调头文件时被
包含。

初始 Kconfig
==============

Kconfig 文件的用途是提供用户可启用或更改的与
所实现处理器的功能相关的选项。一个示例
文件类似：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/Kconfig
   :language: kconfig

初始 CMakeLists.txt
====================

CMakeLists.txt 文件由构建系统用于设置要编译的
文件、要添加的包含
目录，并指定可更改的选项。如果 Kconfig 选项启用，基本
文件仅需
包含源文件。一个示例
文件类似：

.. tabs::

   .. group-tab:: Zephyr 模块

     .. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/CMakeLists.txt
        :language: cmake

   .. group-tab:: 应用程序

     .. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/CMakeLists.txt
        :language: cmake
        :start-after: Include handler files

从应用程序包含
**************************

应用程序专用的 MCUmgr 处理器可通过创建/编辑应用程序构建文件添加。
示例
修改如下。

示例 CMakeLists.txt
====================

应用程序的 ``CMakeLists.txt`` 文件可通过添加以下
来加载示例 MCUmgr 处理器的 CMake 文件：

.. code-block:: cmake

    add_subdirectory(mcumgr/grp/<grp_name>)

示例 Kconfig
==============

应用程序的 Kconfig 文件可通过向应用程序目录的 ``Kconfig`` 文件（或
其不存在时创建它）添加以下
来包含示例 MCUmgr 处理器的 Kconfig 文件：

.. code-block:: kconfig

    rsource "mcumgr/grp/<grp_name>/Kconfig"

    # Include Zephyr's Kconfig
    source "Kconfig.zephyr"

从 Zephyr 模块包含
****************************

Zephyr :ref:`modules` 可用于向多个不同的应用程序添加
自定义 MCUmgr 处理器，而无需在每个应用程序的源树中重复
代码，关于如何设置模块文件的细节参见 :ref:`module-yml`。示例
文件如下。

示例 zephyr/module.yml
=========================

这是一个可从模块目录的根加载 Kconfig 和 CMake 文件的示例
文件，将放置于 ``zephyr/module.yml``：

.. code-block:: yaml

    build:
      kconfig: Kconfig
      cmake: .

示例 CMakeLists.txt
====================

这是一个加载示例 MCUmgr 处理器 CMake 文件的示例 CMakeLists.txt 文件，
将放置于 ``CMakeLists.txt``：

.. code-block:: cmake

    add_subdirectory(mcumgr/grp/<grp_name>)

示例 Kconfig
==============

这是一个加载示例 MCUmgr 处理器 Kconfig 文件的示例 Kconfig 文件，
将放置于 ``Kconfig``：

.. code-block:: kconfig

    rsource "mcumgr/grp/<grp_name>/Kconfig"

演示处理器
*********************

有一个演示项目，包含应用程序和 Zephyr
模块 MCUmgr 处理器两者的配置，可作为创建自己的基础，
位于
:zephyr_file:`tests/subsys/mgmt/mcumgr/handler_demo/`。
