.. _sysbuild_images:

Sysbuild 镜像
###############

Sysbuild
可以
用于
向
构建
添加
额外
镜像，
这些
可以
由
项目
或
开发板
添加，
尽管
目前
必须
是
Zephyr 应用。

添加
镜像
的
方法
************************

镜像
可以
用
多种
方式
添加
到
项目
或
多个
项目，
多种
方式
可以
同时
使用，
它们
可以
用
以下
方式
添加：

应用
=============

应用
可以
使用
应用
目录
中
的
``sysbuild.cmake`` 文件
添加
sysbuild
镜像，
镜像
的
包含
可以
用
应用
目录
中
的
``Kconfig.sysbuild`` 文件
控制。

开发板
======

开发板
可以
使用
开发板
目录
中
的
``sysbuild.cmake`` 文件
添加
sysbuild
镜像，
镜像
的
包含
可以
用
开发板
目录
中
的
``Kconfig.sysbuild`` 文件
控制。

SoC
====

SoC
可以
使用
soc
目录
中
的
``sysbuild.cmake`` 文件
添加
sysbuild
镜像。

模块
=======

:ref:`模块`
可以
用
``module.yml`` 文件
中
的
``sysbuild-cmake`` 和
``sysbuild-kconfig`` 选项
添加
sysbuild
镜像，
细节
见
:ref:`sysbuild_module_integration`。

添加
镜像
*********************

镜像
可以
用
两种
方式
之一
添加：

单个
不可
更改
镜像
=========================

用
这种
设置，
要
添加
的
镜像
固定
到
特定
应用
且
不
能
更改
（尽管
它
不
能
更改
为
其他
镜像，
镜像
本身
的
版本
可以
通过
使用
west
清单
引入
应用
仓库
的
不同
版本
或
从
替代
来源
更改，
假设
镜像
在
其
自己
的
仓库
中）。

.. note::

   只有
   当
   镜像
   锁定
   到
   特定
   接口
   且
   没有
   可扩展性
   时
   才
   应该
   使用
   这个
   方法。

如何
创建
这种
镜像
的
示例，
这
假设
:ref:`Zephyr 应用
已
创建 <application>`：

.. tabs::

   .. group-tab:: ``Kconfig.sysbuild``

      .. code-block:: kconfig

         config MY_IMAGE
                 bool "Include my amazing image"
                 help
                   If enabled, will include my amazing image in the build which does...

      .. note::

         记住
         如果
         这
         应用
         在
         应用
         ``Kconfig.sysbuild`` 文件
         中，
         文件
         中
         要
         有
         ``source "share/sysbuild/Kconfig"``。


   .. group-tab:: ``sysbuild.cmake``

      .. code-block:: cmake

         if(SB_CONFIG_MY_IMAGE)
           ExternalZephyrProject_Add(
             APPLICATION my_image
             SOURCE_DIR ${ZEPHYR_MY_IMAGE_MODULE_DIR}/path/to/my_image
           )
         endif()

这里
可以
设置
额外
的
依赖
顺序
如果
需要，
细节
见
:ref:`sysbuild_zephyr_application_dependencies`，
镜像
配置
也
可以
在这里
设置，
细节
见
:ref:`sysbuild_images_config`。

这个
镜像
可以
在
用
west
构建
时
像
这样
启用：

.. zephyr-app-commands::
   :tool: west
   :zephyr-app: <app>
   :board: nrf52840dk/nrf52840
   :goals: build
   :west-args: --sysbuild
   :gen-args: -DSB_CONFIG_MY_IMAGE=y
   :compact:

可扩展
可
更改
镜像
===========================

用
这种
设置，
要
添加
的
镜像
可以
是
用户
可以
选择
的
任意
数量
可能
应用
之一，
这个
选择
列表
也
可以
在
下游
扩展
以
添加
上游
Zephyr 中
不
可用
的
树
外
特定
应用
的
额外
选项。
这
更
复杂
创建
但
是
向
上游
Zephyr
添加
镜像
的
首选
方法。

.. tabs::

   .. group-tab:: ``Kconfig.sysbuild``

      .. code-block:: kconfig

         config SUPPORT_OTHER_APP
                 bool
                 # 如果
                 # 这种
                 # 应用
                 # 类型
                 # 只
                 # 在
                 # 某些
                 # 平台
                 # 可用，
                 # 条件
                 # 可以
                 # 放
                 # 这里
                 default y

         config SUPPORT_OTHER_APP_MY_IMAGE
                 bool
                 # 如果
                 # 这个
                 # 镜像
                 # 只
                 # 在
                 # 某些
                 # 平台
                 # 可用，
                 # 条件
                 # 可以
                 # 放
                 # 这里
                 default y

         choice OTHER_APP
                 prompt "Other app image"
                 # 如果
                 # 应该
                 # 在
                 # 例如
                 # 支持
                 # 时
                 # 加载
                 # 默认
                 # 镜像，
                 # 这里
                 # 可以
                 # 指定
                 # 默认
                 # 值
                 default OTHER_APP_NONE
                 depends on SUPPORT_OTHER_APP

         config OTHER_APP_IMAGE_NONE
                 bool "None"
                 help
                   Do not Include an other app image in the build.

         config OTHER_APP_IMAGE_MY_IMAGE
                 bool "my_image"
                 depends on SUPPORT_OTHER_APP_MY_IMAGE
                 help
                   Include my amazing image as the other app image to use, which does...

         endchoice

         config OTHER_APP_IMAGE_NAME
                 string
                 default "my_image" if OTHER_APP_IMAGE_MY_IMAGE
                 help
                   Name of other app image.

         config OTHER_APP_IMAGE_PATH
                 string
                 default "$(ZEPHYR_MY_IMAGE_MODULE_DIR)/path/to/my_image" if OTHER_APP_IMAGE_MY_IMAGE
                 help
                   Source directory of other app image.

      .. note::

         记住
         如果
         这
         应用
         在
         应用
         ``Kconfig.sysbuild`` 文件
         中，
         文件
         中
         要
         有
         ``source "$(ZEPHYR_BASE)/share/sysbuild/Kconfig"``。

   .. group-tab:: ``sysbuild.cmake``

      .. code-block:: cmake

         if(SB_CONFIG_OTHER_APP_IMAGE_PATH)
           ExternalZephyrProject_Add(
             APPLICATION ${SB_CONFIG_OTHER_APP_IMAGE_NAME}
             SOURCE_DIR ${SB_CONFIG_OTHER_APP_IMAGE_PATH}
           )
         endif()

这里
可以
设置
额外
的
依赖
顺序
如果
需要，
细节
见
:ref:`sysbuild_zephyr_application_dependencies`，
镜像
配置
也
可以
在这里
设置，
细节
见
:ref:`sysbuild_images_config`。

这个
次要
镜像
可以
在
用
west
构建
时
像
这样
启用：

.. zephyr-app-commands::
   :tool: west
   :zephyr-app: <app>
   :board: nrf52840dk/nrf52840
   :goals: build
   :west-args: --sysbuild
   :gen-args: -DSB_CONFIG_MY_IMAGE=y
   :compact:

然后
这
可以
被
:ref:`模块`
像
这样
扩展：

.. tabs::

   .. group-tab:: ``Kconfig.sysbuild``

      .. code-block:: kconfig

         config SUPPORT_OTHER_APP_MY_SECOND_IMAGE
                 bool
                 default y

         choice OTHER_APP

         config OTHER_APP_IMAGE_MY_SECOND_IMAGE
                 bool "my_second_image"
                 depends on SUPPORT_OTHER_APP_MY_SECOND_IMAGE
                 help
                   Include my other amazing image as the other app image to use, which does...

         endchoice

         config OTHER_APP_IMAGE_NAME
                 default "my_second_image" if OTHER_APP_IMAGE_MY_SECOND_IMAGE

         config OTHER_APP_IMAGE_PATH
                 default "$(ZEPHYR_MY_SECOND_IMAGE_MODULE_DIR)/path/to/my_second_image" if OTHER_APP_IMAGE_MY_SECOND_IMAGE

如
可
见，
添加
替代
镜像
不
需要
额外
的
CMake
更改，
因为
基础
CMake 代码
将
添加
替代
镜像
而非
原始
镜像，
如果
被
选择。

这个
替代
次要
镜像
可以
在
用
west
构建
时
像
这样
启用：

.. zephyr-app-commands::
   :tool: west
   :zephyr-app: <app>
   :board: nrf52840dk/nrf52840
   :goals: build
   :west-args: --sysbuild
   :gen-args: -DSB_CONFIG_MY_SECOND_IMAGE=y
   :compact:

.. _sysbuild_images_config:

镜像
配置
*******************

Sysbuild
支持
能够
设置
镜像
配置
（Kconfig 选项）
并
支持
读取
镜像
配置
（Kconfig）
的
输出，
这
可以
用于
允许
添加
选项
到
sysbuild
本身
然后
全局
或
选择性地
配置
它。

设置
镜像
配置
===========================

Kconfig
-------

Sysbuild
可以
用于
**在
镜像
的
CMake 配置
发生
之前**
设置
镜像
配置。
关于
在
镜像
中
设置
Kconfig 选项
的
重要
注意
是
这些
是
持久
的
且
不
能
被
镜像
更改。
以下
函数
可以
用于
设置
镜像
上
的
配置：

.. code-block:: cmake

   set_config_bool(<image> CONFIG_<setting> <value>)
   set_config_string(<image> CONFIG_<setting> <value>)
   set_config_int(<image> CONFIG_<setting> <value>)

例如，
要
更改
默认
镜像
以
输出
hex 文件：

.. code-block:: cmake

   set_config_bool(${DEFAULT_IMAGE} CONFIG_BUILD_OUTPUT_HEX y)

这些
可以
安全
地
用于
应用、
开发板
或
SoC
``sysbuild.cmake`` 文件，
因为
该
文件
在
镜像
CMake 过程
被
调用
之前
被
包含。
扩展
:ref:`sysbuild
使用
模块 <sysbuild_module_integration>` 时
应该
使用
pre-CMake
钩子
而非
这个，
例如：

.. code-block:: cmake

   function(${SYSBUILD_CURRENT_MODULE_NAME}_pre_cmake)
     cmake_parse_arguments(PRE_CMAKE "" "" "IMAGES" ${ARGN})

     foreach(image ${PRE_CMAKE_IMAGES})
       set_config_bool(${image} CONFIG_BUILD_OUTPUT_HEX y)
     endforeach()
   endfunction()

镜像
配置
脚本
=========================

镜像
配置
脚本
是
一个
CMake 文件，
可以
用于
用
通用
配置
值
配置
镜像，
每个
镜像
可以
使用
多个，
配置
应该
可以
转移
到
不同
镜像
以
基于
sysbuild 中
设置
的
选项
正确
配置
它们。
MCUboot
配置
选项
用
这个
方法
在
MCUboot 应用
和
镜像
中
配置，
这
允许
sysbuild
成为
签名
密钥
等
的
中心
位置，
然后
在
主
应用
引导
加载器
镜像
中
保持
同步。
设置
密钥
到
绝对
路径
或
``${APP_DIR}`` 这样
的
CMake 变量
见
:ref:`build-signing-keys`。

镜像
配置
脚本
内部，
``ZCMAKE_APPLICATION`` 变量
设置
为
正在
配置
的
应用
名称，
``set_config_*`` sysbuild
CMake 函数
可以
用于
设置
配置
并
可以
读取
sysbuild
Kconfig，
例如：

.. code-block:: cmake

   if(SB_CONFIG_BOOTLOADER_MCUBOOT AND "${SB_CONFIG_SIGNATURE_TYPE}" STREQUAL "NONE")
     set_config_bool(${ZCMAKE_APPLICATION} CONFIG_MCUBOOT_GENERATE_UNSIGNED_IMAGE y)
   endif()

镜像
配置
脚本
（模块/应用）
-----------------------------------------------

模块/应用
镜像
配置
脚本
可以
从
模块
或
应用
代码
设置，
这
必须
在
应用
的
``sysbuild.cmake`` 文件
中
完成。
这
可以
用于
添加
镜像
配置
脚本
如下：

.. tabs::

   .. group-tab:: ``sysbuild.cmake``

      .. code-block:: cmake

         # 这
         # 将
         # 镜像
         # 配置
         # 脚本
         # 应用
         # 到
         # 默认
         # 镜像
         # 只
         get_property(tmp_conf_scripts TARGET ${DEFAULT_IMAGE} PROPERTY IMAGE_CONF_SCRIPT)
         list(APPEND tmp_conf_scripts "${CMAKE_SOURCE_DIR}/image_configurations/MY_CUSTOM_TYPE_image_default.cmake")
         set_target_properties(${DEFAULT_IMAGE} PROPERTIES IMAGE_CONF_SCRIPT "${tmp_conf_scripts}")


   .. group-tab:: 模块
   CMake

      .. code-block:: cmake

         function(${SYSBUILD_CURRENT_MODULE_NAME}_pre_cmake)
           cmake_parse_arguments(PRE_CMAKE "" "" "IMAGES" ${ARGN})

           # 这
           # 将
           # 镜像
           # 配置
           # 脚本
           # 应用
           # 到
           # 所有
           # 镜像
           foreach(image ${PRE_CMAKE_IMAGES})
             get_property(tmp_conf_scripts TARGET ${image} PROPERTY IMAGE_CONF_SCRIPT)
             list(APPEND tmp_conf_scripts "${CMAKE_SOURCE_DIR}/image_configurations/MY_CUSTOM_TYPE_image_default.cmake")
             set_target_properties(${image} PROPERTIES IMAGE_CONF_SCRIPT "${tmp_conf_scripts}")
           endforeach()
         endfunction(${SYSBUILD_CURRENT_MODULE_NAME}_pre_cmake)

镜像
配置
脚本
（Zephyr
全局）
----------------------------------------

全局
Zephyr 提供
的
镜像
配置
脚本，
允许
在
使用
:cmake:command:`ExternalZephyrProject_Add` 时
指定
类型
需要
更改
Zephyr 中
的
sysbuild
代码。
这
应该
只在
添加
任何
项目
都
应该
能
选择
的
新
类型
时
添加，
通常
这
应该
只
需要
于
上游
Zephyr，
尽管
Zephyr 的
fork 版本
可能
使用
这个
无
限制
地
添加
额外
类型。

镜像
配置
有
名称
允许
列表，
必须
在
Zephyr
文件
:zephyr_file:`share/sysbuild/cmake/modules/sysbuild_extensions.cmake` 中
的
:cmake:command:`ExternalZephyrProject_Add` 函数
中
设置。
添加
新
类型
后，
它
可以
在
添加
sysbuild
镜像
时
使用，
例如：

.. tabs::

   .. group-tab:: ``sysbuild_extensions.cmake``

      完整
      文件
      路径：
      ``share/sysbuild/cmake/modules/sysbuild_extensions.cmake``

      .. code-block:: cmake

         # ...
         # Usage:
         #   ExternalZephyrProject_Add(APPLICATION <name>
         #                             SOURCE_DIR <dir>
         #                             [BOARD <board> [BOARD_REVISION <revision>]]
         #                             [APP_TYPE <MAIN|BOOTLOADER|MY_CUSTOM_TYPE>]
         #   )
         # ...
         # APP_TYPE <MAIN|BOOTLOADER|MY_CUSTOM_TYPE>: Application type.
         #                                            MAIN indicates this application is the main application
         #                                            and where user defined settings should be passed on as-is
         #                                            except for multi image build flags.
         #                                            For example, -DCONF_FILES=<files> will be passed on to the
         #                                            MAIN_APP unmodified.
         #                                            BOOTLOADER indicates this app is a bootloader
         #                                            MY_CUSTOM_TYPE indicates this app is...
         # ...
         function(ExternalZephyrProject_Add)
           set(app_types MAIN BOOTLOADER MY_CUSTOM_TYPE)
         # ...

   .. group-tab:: ``sysbuild.cmake``

      .. code-block:: cmake

         if(SB_CONFIG_OTHER_APP_IMAGE_PATH)
           ExternalZephyrProject_Add(
             APPLICATION ${SB_CONFIG_OTHER_APP_IMAGE_NAME}
             SOURCE_DIR ${SB_CONFIG_OTHER_APP_IMAGE_PATH}
             APP_TYPE MY_CUSTOM_TYPE
           )
         endif()


   .. group-tab:: ``MY_CUSTOM_TYPE_image_default.cmake``

      完整
      文件
      路径：
      ``share/sysbuild/image_configurations/MY_CUSTOM_TYPE_image_default.cmake``

      .. code-block:: cmake

         # 这里，
         # ZCMAKE_APPLICATION
         # 变量
         # 将
         # 被
         # 替换
         # 为
         # 正在
         # 配置
         # 的
         # 镜像
         set_config_bool(${ZCMAKE_APPLICATION} CONFIG_BUILD_OUTPUT_HEX y)

读取
镜像
配置
===========================

Kconfig
-------

镜像
的
Kconfig 值
可以
被
sysbuild
**在
镜像
的
CMake 配置
已
发生
之后**
读取。
这
可以
用于
检查
配置
或
根据
配置
调整
额外
的
sysbuild
任务。
以下
函数
可以
用于
这个
目的：

.. code-block:: cmake

   sysbuild_get(<variable> IMAGE <image> [VAR <image-variable>] KCONFIG)

这个
函数
只能
在
:ref:`sysbuild
被
模块
扩展 <sysbuild_module_integration>` 时
或
在
``sysbuild/CMakeLists.txt`` 文件
内部
在
使用
``find_package(Sysbuild)`` 之后
使用。
显示
输出
所有
镜像
值
的
示例：

.. tabs::

   .. group-tab:: 模块
   CMake

      .. code-block:: cmake

         function(${SYSBUILD_CURRENT_MODULE_NAME}_post_cmake)
           cmake_parse_arguments(POST_CMAKE "" "" "IMAGES" ${ARGN})

           foreach(image ${POST_CMAKE_IMAGES})
             # 注意
             # 要
             # 读取
             # 的
             # 变量
             # 在
             # 使用
             # sysbuild_get()
             # 函数
             # 之前
             # 不
             # 能
             # 被
             # 设置
             set(tmp_val)
             sysbuild_get(tmp_val IMAGE ${image} VAR CONFIG_BUILD_OUTPUT_HEX KCONFIG)
             message(STATUS "Image ${image} build hex: ${tmp_val}")
           endforeach()
         endfunction()

   .. group-tab:: ``sysbuild/CMakeLists.txt``

      .. code-block:: cmake

         find_package(Sysbuild REQUIRED HINTS $ENV{ZEPHYR_BASE})

         project(sysbuild LANGUAGES)

         sysbuild_get(tmp_val IMAGE ${DEFAULT_IMAGE} VAR CONFIG_BUILD_OUTPUT_HEX KCONFIG)
         message(STATUS "Image ${DEFAULT_IMAGE} build hex: ${tmp_val}")
