.. _toolchain_armclang:

Arm Compiler 6
##############

#. 下载并安装适用于你的操作系统的、包含 `Arm Compiler 6`_ 的开发套件。

#. :ref:`设置以下环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``armclang``。
   - 将 :envvar:`ARMCLANG_TOOLCHAIN_PATH` 设置为工具链安装目录。

#. Arm Compiler 6 需要 :envvar:`ARMLMD_LICENSE_FILE` 环境变量指向你的许可证文件或许可证服务器。

例如：

   .. code-block:: bash

      # Linux, macOS, license file:
      export ARMLMD_LICENSE_FILE=/<path>/license_armds.dat
      # Linux, macOS, license server:
      export ARMLMD_LICENSE_FILE=8224@myserver

   .. code-block:: batch

      # Windows, license file:
      set ARMLMD_LICENSE_FILE=c:\<path>\license_armds.dat
      # Windows, license server:
      set ARMLMD_LICENSE_FILE=8224@myserver

#. 如果 Arm Compiler 6 是作为 Arm Development Studio 的一部分安装的，则必须设置 :envvar:`ARM_PRODUCT_DEF` 指向产品定义文件：另请参阅 `产品与工具包配置 <https://developer.arm.com/tools-and-software/software-development-tools/license-management/resources/product-and-toolkit-configuration>`_。例如，如果 Arm Development Studio 安装在 ``/opt/armds-2020-1`` 且使用 Gold 许可证，则将 :envvar:`ARM_PRODUCT_DEF` 设置为指向 ``/opt/armds-2020-1/gold.elmap``。

   .. note::

      Arm Compiler 6 使用 ``armlink`` 进行链接。这与 Zephyr 的链接脚本模板不兼容，因为该模板适用于 GNU ld。Zephyr 的 Arm Compiler 6 支持使用 Zephyr 的 CMake 链接脚本生成器，该生成器支持生成 scatter 文件。基本的 scatter 文件支持已经就位，但 ld 模板中覆盖的一些区域尚未被 CMake 链接脚本生成器完全支持。

      一些 Zephyr 子系统或模块还可能包含依赖 GNU 内置函数（intrinsics）的 C 或汇编代码，这些代码尚未更新为完全适配 ``armclang``。

.. _Arm Compiler 6: https://developer.arm.com/tools-and-software/embedded/arm-compiler/downloads/version-6
