.. _toolchain_iar_arm:

IAR
Arm
Toolchain
#################

#. 下载
   并
   安装
   `IAR
   Arm
   Toolchain`_
   release
   v9.70
   或
   更新
   版本
   到
   你
   的
   主机
   （IAR
   Embedded
   Workbench
   或
   IAR
   Build
   Tools，
   永久
   或
   订阅
   许可）

#. 确保
   你
   在
   主机
   上
   安装
   了
   :ref:`Zephyr
   SDK
   <toolchain_zephyr_sdk>`。

#. :ref:`Set
   these
   environment
   variables
   <env_vars>`：

   - 设置
     :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
     为
     ``iar``。
   - 设置
     :envvar:`IAR_TOOLCHAIN_PATH`
     为
     工具链
     安装
     目录。

#. IAR
   Toolchain
   的
   cloud
   licensed
   variant
   需要
   设置
   :envvar:`IAR_LMS_BEARER_TOKEN`
   环境
   变量
   为
   有效
   的
   ``license
   bearer
   token``
   （订阅
   许可）。

例如：

.. code-block:: bash

   #
   Linux
   （默认
   安装
   路径）：
   export
   IAR_TOOLCHAIN_PATH=/opt/iar/cxarm-<version>/arm
   export
   ZEPHYR_TOOLCHAIN_VARIANT=iar
   export
   IAR_LMS_BEARER_TOKEN="<BEARER-TOKEN>"

.. code-block:: batch

   #
   Windows:
   set
   IAR_TOOLCHAIN_PATH=c:\<path>\cxarm-<version>\arm
   set
   ZEPHYR_TOOLCHAIN_VARIANT=iar
   set
   IAR_LMS_BEARER_TOKEN="<BEARER-TOKEN>"

.. note::

   已知
   限制：

   - IAR
     Toolchain
     用
     ``ilink``
     链接
     并
     依赖
     Zephyr
     的
     CMAKE_LINKER_GENERATOR。
     ``ilink``
     与
     Zephyr
     的
     链接器
     脚本
     模板
     不
     兼容，
     该
     模板
     与
     GNU
     ld
     工作。

   - Zephyr
     SDK
     分发
     的
     GNU
     Assembler
     用
     于
     ``.S-files``。

   - C
     库
     支持
     仅
     ``Minimal
     libc``。
     C++
     不
     支持。

   - 一些
     Zephyr
     子
     系统
     或
     modules
     可能
     包含
     依赖
     GNU
     intrinsics
     的
     C
     或
     汇编
     代码
     尚未
     更新
     为
     完全
     与
     ``iar``
     工作。

   - TrustedFirmware
     不
     支持

.. _IAR
   Arm
   Toolchain:
   https://www.iar.com/products/architectures/arm/
