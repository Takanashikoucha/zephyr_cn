.. _custom_cmake_toolchains:

自定义
CMake
工具链
#######################

要
使用
在
外部
CMake
文件
中
定义
的
自定义
工具链，
:ref:`set
these
environment
variables
<env_vars>`：

- 设置
  :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
  为
  你
  的
  工具链
  名称
- 设置
  ``TOOLCHAIN_ROOT``
  为
  包含
  你
  的
  工具链
  CMake
  配置
  文件
  的
  目录
  路径。

Zephyr
然后
将
包含
位于
:file:`TOOLCHAIN_ROOT`
目录
中
的
toolchain
cmake
文件：

- :file:`cmake/toolchain/<toolchain
  name>/generic.cmake`：
  配置
  工具链
  用于
  "generic"
  使用，
  主要
  意味着
  对
  生成
  的
  :ref:`devicetree`
  文件
  运行
  C
  预
  处理器。
- :file:`cmake/toolchain/<toolchain
  name>/target.cmake`：
  配置
  工具链
  用于
  "target"
  使用，
  即
  构建
  Zephyr
  和
  你
  的
  应用
  源
  代码。

这里
<toolchain
name>
与
:envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
中
提供
的
名称
相同。
参考
zephyr
文件
:zephyr_file:`cmake/modules/FindHostTools.cmake`
和
:zephyr_file:`cmake/modules/FindTargetTools.cmake`
获取
关于
你
的
:file:`generic.cmake`
和
:file:`target.cmake`
文件
应该
包含
什么
的
更多
细节。

你
也
可以
在
为
Zephyr
应用
生成
构建
系统
时
将
``ZEPHYR_TOOLCHAIN_VARIANT``
和
``TOOLCHAIN_ROOT``
设置
为
CMake
变量，
如：

.. code-block:: console

   west
   build
   ...
   --
   -DZEPHYR_TOOLCHAIN_VARIANT=...
   -DTOOLCHAIN_ROOT=...

.. code-block:: console

   cmake
   -DZEPHYR_TOOLCHAIN_VARIANT=...
   -DTOOLCHAIN_ROOT=...
