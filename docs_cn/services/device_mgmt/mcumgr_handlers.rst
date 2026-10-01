.. _mcumgr_handlers:

MCUmgr handlers
###############

Overview
********

MCUmgr 通过 group handlers 运作（其识别与
特定 management area 相关的一组 functions（其用 16-bit identification value 寻址（
:c:enum:`mcumgr_group_t` 包含 Zephyr 中可用的 management groups 及其
corresponding group ID values。Group ID 包含在 SMP headers 中（以标识
command 属于哪个 group（还有标识
该 group 要执行的 function 的 8-bit command ID - 关于 SMP
protocol 和 header 的细节参见 :ref:`mcumgr_smp_protocol_specification`。每个唯一 ID 只能有一个注册的 group。

Implementation
**************

MCUmgr handlers 可由 application code 或 module code 从外部添加（其不
须驻留在 upstream Zephyr tree 中即可用。创建 handler 的第一步
是
创建其 folder structure（典型 Zephyr MCUmgr group layout 如下：

.. code-block:: none

   <dir>/grp/<grp_name>_mgmt/
   ├── CMakeLists.txt
   ├── Kconfig
   ├── include
   ├──── <grp_name>_mgmt.h
   ├──── <grp_name>_mgmt_callbacks.h
   ├── src
   └──── <grp_name>_mgmt.c

注意 upstream Zephyr MCUmgr handlers 中的 header files 驻留在
``zephyr/include/zephyr/mgmt/mcumgr/grp/<grp_name>_mgmt`` directory 中（以使
files 可
被 applications 全局 include。

Initial header <grp_name>_mgmt.h
================================

Header file 的用途为提供 MCUmgr handler
本身和 application code 可使用的 defines（如引用执行
functions 的 command IDs。示例
file 类似：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/include/example_mgmt.h
   :language: c
   :linenos:

这提供 2 个 command ``test`` 和 ``other`` 的 defines（并设置
SMP version 2 error
responses（其有每 group 唯一的 error codes（而 legacy SMP version 1 error
responses 返回 :c:enum:`mcumgr_err_t` - 应总有值为 0 的 OK error code
和值为 1 的 unknown error code。上述示例添加值为 2 的
``not wanted`` error code。另外（group ID 设为
:c:enumerator:`MGMT_GROUP_ID_PERUSER`（其为用户定义 groups 的 start group ID（注意
group IDs 须唯一（故其他 custom groups 应用不同 values（
central index
header file（如 upstream Zephyr 有的）可用于更
容易地分配 group IDs。

Initial header <grp_name>_mgmt_callbacks.h
==========================================

Header file 的用途为提供 MCUmgr handler
本身和 application code 可使用的 defines（如引用执行
functions 的 command IDs。示例
file 类似：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/include/example_mgmt_callbacks.h
   :language: c
   :linenos:

这设置单个 event（application（或 module）code 可注册
以在 function handler 执行时接收
callback（这允许改变 handler 的 flow（即返回
error 而非继续。Event group ID 设为
:c:enumerator:`MGMT_EVT_GRP_USER_CUSTOM_START`（其为用户定义 groups 的 start event ID（注意
event IDs 须唯一（故其他 custom groups 应用不同 values（
central index
header file（如 upstream Zephyr 有的）可用于更
容易地分配 event IDs。

Initial source <grp_name>_mgmt.c
================================

此 source file 的用途为处理传入的 MCUmgr commands、提供
responses（并
将 transport 注册到 MCUmgr（使 commands 被发送到它。示例
file 类似：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/src/example_mgmt.c
   :language: c
   :linenos:

上述 code 创建 2 个 function handlers：``test`` 支持 read requests 且
接受 2
个 required parameters（``other`` 支持 write requests 且
接受 1 个 optional parameter（
此 function handler 有可选 notification callback feature（允许
code 其他部分监听 event 并
采取任何必要 actions（或通过返回
error 阻止 function 进一步执行。关于 MCUmgr callback
functionality 的进一步细节可在 :ref:`mcumgr_callbacks` 找到。

注意引用 custom MCUmgr handlers callbacks 的其他 code 须
include 两个
base Zephyr callback include file 和 custom handler callback file（仅
in-tree Zephyr
handler headers 在 include upstream Zephyr callback header file 时被
include。

Initial Kconfig
===============

Kconfig file 的用途为提供用户可启用或更改的与
所实现 handler 的 functionality 相关的 options。示例
file 类似：

.. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/Kconfig
   :language: kconfig

Initial CMakeLists.txt
======================

CMakeLists.txt file 由 build system 用于设置要编译的
files、要添加的 include
directories（并指定可更改的 options。若 Kconfig options 启用（基本
file 仅需
include source files。示例
file 类似：

.. tabs::

   .. group-tab:: Zephyr module

      .. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/example_as_module/CMakeLists.txt
         :language: cmake

   .. group-tab:: Application

      .. literalinclude:: ../../../tests/subsys/mgmt/mcumgr/handler_demo/CMakeLists.txt
         :language: cmake
         :start-after: Include handler files

Including from application
**************************

Application-specific MCUmgr handlers 可通过创建/编辑 application build files 添加。
示例
modifications 如下。

Example CMakeLists.txt
======================

Application 的 ``CMakeLists.txt`` file 可通过添加以下
加载示例 MCUmgr handler 的 CMake file：

.. code-block:: cmake

    add_subdirectory(mcumgr/grp/<grp_name>)

Example Kconfig
===============

Application 的 Kconfig file 可通过向 application directory 的 ``Kconfig`` file（或
其不存在时创建）添加以下
include 示例 MCUmgr handler 的 Kconfig file：

.. code-block:: kconfig

    rsource "mcumgr/grp/<grp_name>/Kconfig"

    # Include Zephyr's Kconfig
    source "Kconfig.zephyr"

Including from Zephyr Module
****************************

Zephyr :ref:`modules` 可用于向多个不同 applications 添加
custom MCUmgr handlers（而无需在每个 application 的 source tree 中重复
code（关于如何设置 module files 的细节参见 :ref:`module-yml`。示例
files 如下。

Example zephyr/module.yml
=========================

此为可从 module directory 的 root 加载 Kconfig 和 CMake files 的示例
file（将放置于 ``zephyr/module.yml``：

.. code-block:: yaml

    build:
      kconfig: Kconfig
      cmake: .

Example CMakeLists.txt
======================

此为加载示例 MCUmgr handler 的 CMake file 的示例 CMakeLists.txt file（
将放置于 ``CMakeLists.txt``：

.. code-block:: cmake

    add_subdirectory(mcumgr/grp/<grp_name>)

Example Kconfig
===============

此为加载示例 MCUmgr handler 的 Kconfig file 的示例 Kconfig file（
将放置于 ``Kconfig``：

.. code-block:: kconfig

    rsource "mcumgr/grp/<grp_name>/Kconfig"

Demonstration handler
*********************

有 demonstration project（包含
application 和 zephyr
module-MCUmgr handlers 两者的 configuration（可作为创建自己的基础（
位于
:zephyr_file:`tests/subsys/mgmt/mcumgr/handler_demo/`。
