.. _toolchain_xc32:

MPLAB XC32
##########

#. 下载并安装 `MPLAB XC32 编译器`_ 到你的操作系统。

#. :ref:`设置这些环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``xc32``。
   - 将 :envvar:`XC32_TOOLCHAIN_PATH` 设置为工具链安装目录。

#. 要检查你是否在当前环境中正确设置了这些变量，请参照以下示例 shell 会话（:envvar:`XC32_TOOLCHAIN_PATH` 的值在你的系统上可能不同）：

   .. code-block:: console

      # Linux, macOS:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      xc32
      $ echo $XC32_TOOLCHAIN_PATH
      /opt/microchip/xc32/v5.00

      # Windows:
      > echo %ZEPHYR_TOOLCHAIN_VARIANT%
      xc32
      > echo %XC32_TOOLCHAIN_PATH%
      C:\Microchip\xc32\v5.00

#. 对 Microchip SoCs，将 :envvar:`XC_PACK_DIR` 设置为包含已安装 Microchip Device Family Packs（DFPs）的根目录。

   .. note::

      Zephyr 使用 :envvar:`XC_PACK_DIR` 查找与所选 SoC 匹配的 DFP，并向 XC32 工具链传递所需的 ``-mdfp`` 和 ``-mprocessor`` 标志。

   例如：

   .. code-block:: console

      # Linux, macOS:
      $ export XC_PACK_DIR=/home/path/.packs/microchip

      # Windows:
      > set XC_PACK_DIR=C:\Users\path\.mchp_packs\Microchip

.. _MPLAB XC32 Compiler: https://www.microchip.com/en-us/tools-resources/develop/mplab-xc-compilers
