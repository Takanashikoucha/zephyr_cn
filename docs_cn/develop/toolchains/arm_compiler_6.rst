.. _toolchain_armclang:

Arm
Compiler
6
##############

#. 下载
   并
   安装
   包含
   `Arm
   Compiler
   6`_
   的
   开发
   套件
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
     ``armclang``。
   - 设置
     :envvar:`ARMCLANG_TOOLCHAIN_PATH`
     为
     工具链
     安装
     目录。

#. Arm
   Compiler
   6
   需要
   :envvar:`ARMLMD_LICENSE_FILE`
   环境
   变量
   指向
   你
   的
   许可
   文件
   或
   服务器。

例如：

   .. code-block:: bash

      #
      Linux,
      macOS,
      license
      file:
      export
      ARMLMD_LICENSE_FILE=/<path>/license_armds.dat
      #
      Linux,
      macOS,
      license
      server:
      export
      ARMLMD_LICENSE_FILE=8224@myserver

   .. code-block:: batch

      #
      Windows,
      license
      file:
      set
      ARMLMD_LICENSE_FILE=c:\<path>\license_armds.dat
      #
      Windows,
      license
      server:
      set
      ARMLMD_LICENSE_FILE=8224@myserver

#. 如果
   Arm
   Compiler
   6
   作为
   Arm
   Development
   Studio
   的
   部分
   安装，
   那么
   你
   必须
   设置
   :envvar:`ARM_PRODUCT_DEF`
   指向
   产品
   定义
   文件：
   参考
   也：
   `Product
   and
   toolkit
   configuration
   <https://developer.arm.com/tools-and-software/software-development-tools/license-management/resources/product-and-toolkit-configuration>`_。
   例如
   如果
   Arm
   Development
   Studio
   安装
   在：
   ``/opt/armds-2020-1``
   带
   Gold
   许可，
   那么
   设置
   :envvar:`ARM_PRODUCT_DEF`
   指向
   ``/opt/armds-2020-1/gold.elmap``。
