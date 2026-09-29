.. _toolchain_atfe:

Arm
Toolchain
for
Embedded
（ATfE）
#################################

Arm
Toolchain
for
Embedded
（ATfE）
是
Arm
的
C
和
C++
工具链
基于
免费
和
开源
的
LLVM
Compiler
Infrastructure
和
用于
baremetal
目标
的
Picolib
C
库。

ATfE
被
精细
调整
特别
关注
性能
用于
较新
的
ARM
产品
（2024
之后）
如
64
位
Arm
Architectures
（AArch64），
或
M-Profile
Vector
Extension
（MVE，
一
个
32
位
Armv8.1-M
扩展）。

安装
************

#. 下载
   并
   安装
   `Arm
   toolchain
   for
   embedded`_
   构建
   用于
   你
   的
   操作
   系统
   并
   解压
   到
   你
   的
   文件
   系统。

#. :ref:`Set
   these
   environment
   variables
   <env_vars>`：

   - 设置
     :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
     为
     ``host/llvm``。
   - 设置
     :envvar:`LLVM_TOOLCHAIN_PATH`
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
   （:envvar:`LLVM_TOOLCHAIN_PATH`
   值
   在
   你
   的
   系统
   上
   可能
   不同）：

   .. tabs::

      .. group-tab::
         Ubuntu

         .. code-block:: bash

            echo
            $ZEPHYR_TOOLCHAIN_VARIANT
            host/llvm
            echo
            $LLVM_TOOLCHAIN_PATH
            /home/you/Downloads/ATfE

      .. group-tab::
         macOS

         .. code-block:: bash

            echo
            $ZEPHYR_TOOLCHAIN_VARIANT
            host/llvm
            echo
            $LLVM_TOOLCHAIN_PATH
            /home/you/Downloads/ATfE

      .. group-tab::
         Windows

         .. code-block:: batch

            echo
            %ZEPHYR_TOOLCHAIN_VARIANT%
            host/llvm
            echo
            %LLVM_TOOLCHAIN_PATH%
            C:\Users\you\Downloads\ATfE
