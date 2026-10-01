.. _sca:

静态代码分析（SCA）
##########################

Zephyr 对静态代码分析工具的支持通过 CMake 实现。

构建设置 :makevar:`ZEPHYR_SCA_VARIANT` 可用于指定要使用的 SCA 工具。
:envvar:`ZEPHYR_SCA_VARIANT` 也作为 :ref:`环境变量 <env_vars>` 受支持。

使用 ``-DZEPHYR_SCA_VARIANT=<tool>``，例如 ``-DZEPHYR_SCA_VARIANT=sparse``，
即可启用静态分析工具 ``sparse``。

.. _sca_infrastructure:

SCA 工具基础设施
***********************

SCA 工具的支持在 :file:`sca.cmake` 文件中实现。
:file:`sca.cmake` 必须放在 :file:`{SCA_ROOT}/cmake/sca/{tool}/sca.cmake` 下。
Zephyr 本身始终被添加到 :makevar:`SCA_ROOT`，
但构建系统允许向 :makevar:`SCA_ROOT` 设置中添加额外的文件夹。

你可以通过创建以下结构为树外 SCA 工具提供支持：

.. code-block:: none

   <sca_root>/                 # Custom SCA root
   └── cmake/
       └── sca/
           └── <tool>/         # Name of SCA tool, this is the value given to ZEPHYR_SCA_VARIANT
               └── sca.cmake   # CMake code that configures the tool to be used with Zephyr

要在 ``/path/to/my_tools/cmake/sca`` 下添加 ``foo``，创建以下结构：

.. code-block:: none

   /path/to/my_tools
           └── cmake/
               └── sca/
                   └── foo/
                       └── sca.cmake

要将 ``foo`` 用作 SCA 工具，必须指定 ``-DZEPHYR_SCA_VARIANT=foo``。

记得将 ``/path/to/my_tools`` 添加到 :makevar:`SCA_ROOT`。

:makevar:`SCA_TOOL` 可以用 ``-DSCA_ROOT=<sca_root>`` 作为普通 CMake 设置，
也可以由 Zephyr 模块在其 :file:`module.yml` 文件中添加，
参见 :ref:`Zephyr 模块 - 构建设置 <modules_build_settings>`

编译器与链接器启动器
=============================

需要观察或包装编译和链接命令的 SCA 工具，
通过在其 :file:`sca.cmake` 中设置 ``CMAKE_<LANG>_COMPILER_LAUNCHER`` 和
``CMAKE_<LANG>_LINKER_LAUNCHER`` 变量来实现。
它们必须作为普通变量设置，而非缓存条目。

以这种方式设置的启动器会替换任何已配置的启动器，``ccache`` 也包括在内。
如果一个工具是透明包装器（即它原样运行所接收的命令），
则可以通过追加的方式保留前一个启动器：

.. code-block:: cmake

   set(CMAKE_C_COMPILER_LAUNCHER ${my_wrapper} ${CMAKE_C_COMPILER_LAUNCHER})

.. _sca_native_tools:

原生 SCA 工具支持
***********************

以下是 Zephyr 构建系统原生支持的 SCA 工具列表。

.. toctree::
   :maxdepth: 1
   :glob:

   *
