.. _toolchain_iar_arm:

IAR Arm 工具链
#################

#. 在你的主机上下载并安装 `IAR Arm Toolchain`_ 的 v9.70 或更高版本
   （IAR Embedded Workbench 或 IAR Build Tools，永久许可或订阅许可均可）

#. 确保你的主机上已安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>`。

#. :ref:`设置以下环境变量 <env_vars>`：

    - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``iar``。
    - 将 :envvar:`IAR_TOOLCHAIN_PATH` 设置为工具链的安装目录。

#. IAR 工具链的云端许可变体需要将 :envvar:`IAR_LMS_BEARER_TOKEN`
   环境变量设置为有效的 ``license bearer token``（订阅许可）。

例如：

.. code-block:: bash

    # Linux (default installation path):
    export IAR_TOOLCHAIN_PATH=/opt/iar/cxarm-<version>/arm
    export ZEPHYR_TOOLCHAIN_VARIANT=iar
    export IAR_LMS_BEARER_TOKEN="<BEARER-TOKEN>"

.. code-block:: batch

    # Windows:
    set IAR_TOOLCHAIN_PATH=c:\<path>\cxarm-<version>\arm
    set ZEPHYR_TOOLCHAIN_VARIANT=iar
    set IAR_LMS_BEARER_TOKEN="<BEARER-TOKEN>"

.. note::

    已知限制：

    - IAR 工具链使用 ``ilink`` 进行链接，并依赖 Zephyr 的 CMAKE_LINKER_GENERATOR。
      ``ilink`` 与 Zephyr 的链接脚本模板不兼容，该模板是为 GNU ld 设计的。

    - Zephyr SDK 附带的 GNU 汇编器用于 ``.S 文件``。

    - C 库仅支持 ``Minimal libc``。不支持 C++。

    - 部分 Zephyr 子系统或模块可能包含依赖 GNU 内建函数（intrinsics）
      的 C 代码或汇编代码，尚未更新为可完全在 ``iar`` 下工作。

    - 不支持 TrustedFirmware

.. _IAR Arm Toolchain: https://www.iar.com/products/architectures/arm/
