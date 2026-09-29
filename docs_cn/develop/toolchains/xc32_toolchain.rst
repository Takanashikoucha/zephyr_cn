.. _toolchain_xc32:

MPLAB
XC32
##########

#. 下载
   并
   安装
   `MPLAB
   XC32
   Compiler`_
   用于
   你
   的
   操作
   系统。

#. :ref:`Set
   these
   environment
   variables
   <env_vars>`：

   - 设置
     :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
     为
     ``xc32``。
   - 设置
     :envvar:`XC32_TOOLCHAIN_PATH`
     为
     工具链
     安装
     目录。

#. 要
   检查
   你
   在
   当前
   环境
   中
   正确
   设置
   了
   这些
   变量，
   遵循
   这些
   示例
   shell
   会话
   （:envvar:`XC32_TOOLCHAIN_PATH`
   值
   在
   你
   的
   系统
   上
   可能
   不同）：

   .. code-block:: console

      #
      Linux,
      macOS:
      $
      echo
      $ZEPHYR_TOOLCHAIN_VARIANT
      xc32
      $
      echo
      $XC32_TOOLCHAIN_PATH
      /opt/microchip/xc32/v5.00

      #
      Windows:
      >
      echo
      %ZEPHYR_TOOLCHAIN_VARIANT%
      xc32
      >
      echo
      %XC32_TOOLCHAIN_PATH%
      C:\Microchip\xc32\v5.00

#. 对
   Microchip
   SoCs，
   设置
   :envvar:`XC_PACK_DIR`
   为
   包含
   安装
   的
   Microchip
   Device
   Family
   Packs
   （DFPs）
   的
   根
   目录。

   .. note::

      Zephyr
      用
      :envvar:`XC_PACK_DIR`
      找到
      匹配
      选择
      SoC
      的
      DFP
      并
      向
      XC32
      工具链
      传递
      必需
      的
      ``-mdfp``
      和
      ``-mprocessor``
      标志。

   例如：

   .. code-block:: console

      #
      Linux,
      macOS:
      $
      export
      XC_PACK_DIR=/home/path/.packs/microchip

      #
      Windows:
      >
      set
      XC_PACK_DIR=C:\Users\path\.mchp_packs\Microchip

.. _MPLAB
   XC32
   Compiler:
   https://www.microchip.com/en-us/tools-resources/develop/mplab-xc-compilers
