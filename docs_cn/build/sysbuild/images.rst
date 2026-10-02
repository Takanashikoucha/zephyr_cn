.. _sysbuild_images:

Sysbuild 镜像
###############

Sysbuild 可用于向构建添加额外镜像，这些可以由项目或开发板添加，
尽管目前必须是 Zephyr 应用。

添加镜像的方法
************************

镜像可以用多种方式添加到项目或多个项目，多种方式可以同时使用，
它们可以用以下方式添加：

应用
=============

应用可以使用应用目录中的 ``sysbuild.cmake`` 文件添加 sysbuild 镜像，
镜像的包含可以用应用目录中的 ``Kconfig.sysbuild`` 文件控制。

开发板
======

开发板可以使用开发板目录中的 ``sysbuild.cmake`` 文件添加 sysbuild 镜像，
镜像的包含可以用开发板目录中的 ``Kconfig.sysbuild`` 文件控制。

SoC
====

SoC 可以使用 soc 目录中的 ``sysbuild.cmake`` 文件添加 sysbuild 镜像。

模块
=======

:ref:`模块` 可以用 ``module.yml`` 文件中的 ``sysbuild-cmake`` 和
``sysbuild-kconfig`` 选项添加 sysbuild 镜像，细节见 :ref:`sysbuild_module_integration`。

添加镜像
*********************

镜像可以用两种方式之一添加：

单个不可更改镜像
=========================

用这种设置，要添加的镜像固定到特定应用且不能更改
（尽管它不能更改为其他镜像，镜像本身的版本可以通过使用 west 清单
引入应用仓库的不同版本或从替代来源更改，假设镜像在其自己的仓库中）。

.. note::

   只有当镜像锁定到特定接口且没有可扩展性时才应该使用这个方法。

如何创建这种镜像的示例，这假设 :ref:`Zephyr 应用已创建 <application>`：

.. tabs::

   .. group-tab:: ``Kconfig.sysbuild``

      .. code-block:: kconfig

         config MY_IMAGE
                 bool "Include my amazing image"
                 help
                   If enabled, will include my amazing image in the build which does...

      .. note::

         记住如果这应用应用的 ``Kconfig.sysbuild`` 文件中，
         文件中要有 ``source "share/sysbuild/Kconfig"``。


   .. group-tab:: ``sysbuild.cmake``

      .. code-block:: cmake

         if(SB_CONFIG_MY_IMAGE)
           ExternalZephyrProject_Add(
             APPLICATION my_image
             SOURCE_DIR ${ZEPHYR_MY_IMAGE_MODULE_DIR}/path/to/my_image
           )
         endif()

如果需要，这里可以设置额外的依赖顺序，
细节见 :ref:`sysbuild_zephyr_application_dependencies`，镜像配置也可以在这里设置，
细节见 :ref:`sysbuild_images_config`。

这个镜像可以在用 west 构建时像这样启用：

.. zephyr-app-commands::
   :tool: west
   :zephyr-app: <app>
   :board: nrf52840dk/nrf52840
   :goals: build
   :west-args: --sysbuild
   :gen-args: -DSB_CONFIG_MY_IMAGE=y
   :compact:

可扩展可更改镜像
===========================

用这种设置，要添加的镜像可以是用户可以选择的任意数量可能应用之一，
这个选择列表也可以在下游扩展以添加上游 Zephyr 中不可用的
树外特定应用的额外选项。
这创建起来更复杂，但是向上游 Zephyr 添加镜像的首选方法。

.. tabs::

   .. group-tab:: ``Kconfig.sysbuild``

      .. code-block:: kconfig

         config SUPPORT_OTHER_APP
                 bool
                 # 如果这种应用类型只在某些平台可用，条件可以放这里
                 default y

         config SUPPORT_OTHER_APP_MY_IMAGE
                 bool
                 # 如果这个镜像只在某些平台可用，条件可以放这里
                 default y

         choice OTHER_APP
                 prompt "Other app image"
                 # 如果应该在例如支持时加载默认镜像，这里可以指定默认值
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

         记住如果这应用应用的 ``Kconfig.sysbuild`` 文件中，
         文件中要有 ``source "$(ZEPHYR_BASE)/share/sysbuild/Kconfig"``。

   .. group-tab:: ``sysbuild.cmake``

      .. code-block:: cmake

         if(SB_CONFIG_OTHER_APP_IMAGE_PATH)
           ExternalZephyrProject_Add(
             APPLICATION ${SB_CONFIG_OTHER_APP_IMAGE_NAME}
             SOURCE_DIR ${SB_CONFIG_OTHER_APP_IMAGE_PATH}
           )
         endif()

如果需要，这里可以设置额外的依赖顺序，
细节见 :ref:`sysbuild_zephyr_application_dependencies`，镜像配置也可以在这里设置，
细节见 :ref:`sysbuild_images_config`。

这个次要镜像可以在用 west 构建时像这样启用：

.. zephyr-app-commands::
   :tool: west
   :zephyr-app: <app>
   :board: nrf52840dk/nrf52840
   :goals: build
   :west-args: --sysbuild
   :gen-args: -DSB_CONFIG_MY_IMAGE=y
   :compact:

然后这可以被 :ref:`模块` 像这样扩展：

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

如可见，添加替代镜像不需要额外的 CMake 更改，
因为基础 CMake 代码将添加替代镜像而非原始镜像，如果被选择。

这个替代次要镜像可以在用 west 构建时像这样启用：

.. zephyr-app-commands::
   :tool: west
   :zephyr-app: <app>
   :board: nrf52840dk/nrf52840
   :goals: build
   :west-args: --sysbuild
   :gen-args: -DSB_CONFIG_MY_SECOND_IMAGE=y
   :compact:

.. _sysbuild_images_config:

镜像配置
*******************

Sysbuild 支持设置镜像配置（Kconfig 选项），
并支持读取镜像配置（Kconfig）的输出，
这可以用于允许添加选项到 sysbuild 本身，然后全局或选择性地配置它。

设置镜像配置
===========================

Kconfig
-------

Sysbuild 可以用于**在镜像的 CMake 配置发生之前**设置镜像配置。
关于在镜像中设置 Kconfig 选项的重要注意是这些是持久的且不能被镜像更改。
以下函数可以用于设置镜像上的配置：

.. code-block:: cmake

   set_config_bool(<image> CONFIG_<setting> <value>)
   set_config_string(<image> CONFIG_<setting> <value>)
   set_config_int(<image> CONFIG_<setting> <value>)

例如，要更改默认镜像以输出 hex 文件：

.. code-block:: cmake

   set_config_bool(${DEFAULT_IMAGE} CONFIG_BUILD_OUTPUT_HEX y)

这些可以安全地用于应用、开发板或 SoC ``sysbuild.cmake`` 文件，
因为该文件在镜像 CMake 过程被调用之前被包含。
扩展 :ref:`sysbuild 使用模块 <sysbuild_module_integration>` 时应该使用
pre-CMake 钩子而非这个，例如：

.. code-block:: cmake

   function(${SYSBUILD_CURRENT_MODULE_NAME}_pre_cmake)
     cmake_parse_arguments(PRE_CMAKE "" "" "IMAGES" ${ARGN})

     foreach(image ${PRE_CMAKE_IMAGES})
       set_config_bool(${image} CONFIG_BUILD_OUTPUT_HEX y)
     endforeach()
   endfunction()

镜像配置脚本
=========================

镜像配置脚本是一个 CMake 文件，可以用于用通用配置值配置镜像，
每个镜像可以使用多个，配置应该可以转移到不同镜像
以基于 sysbuild 中设置的选项正确配置它们。
MCUboot 配置选项用这个方法在应用和 MCUboot 镜像中配置，
这允许 sysbuild 成为签名密钥等的中心位置，
然后在主应用引导加载器镜像中保持同步。
设置密钥到绝对路径或 ``${APP_DIR}`` 这样的 CMake 变量见 :ref:`build-signing-keys`。

镜像配置脚本内部，``ZCMAKE_APPLICATION`` 变量设置为正在配置的应用名称，
``set_config_*`` sysbuild CMake 函数可以用于设置配置并可以读取 sysbuild Kconfig，
例如：

.. code-block:: cmake

   if(SB_CONFIG_BOOTLOADER_MCUBOOT AND "${SB_CONFIG_SIGNATURE_TYPE}" STREQUAL "NONE")
     set_config_bool(${ZCMAKE_APPLICATION} CONFIG_MCUBOOT_GENERATE_UNSIGNED_IMAGE y)
   endif()

镜像配置脚本（模块/应用）
-----------------------------------------------

模块/应用镜像配置脚本可以从模块或应用代码设置，
这必须在应用的 ``sysbuild.cmake`` 文件中完成。
这可以用于添加镜像配置脚本如下：

.. tabs::

   .. group-tab:: ``sysbuild.cmake``

      .. code-block:: cmake

         # 这将镜像配置脚本应用到默认镜像
         get_property(tmp_conf_scripts TARGET ${DEFAULT_IMAGE} PROPERTY IMAGE_CONF_SCRIPT)
         list(APPEND tmp_conf_scripts "${CMAKE_SOURCE_DIR}/image_configurations/MY_CUSTOM_TYPE_image_default.cmake")
         set_target_properties(${DEFAULT_IMAGE} PROPERTIES IMAGE_CONF_SCRIPT "${tmp_conf_scripts}")


   .. group-tab:: 模块 CMake

      .. code-block:: cmake

         function(${SYSBUILD_CURRENT_MODULE_NAME}_pre_cmake)
           cmake_parse_arguments(PRE_CMAKE "" "" "IMAGES" ${ARGN})

           # 这将镜像配置脚本应用到所有镜像
           foreach(image ${PRE_CMAKE_IMAGES})
             get_property(tmp_conf_scripts TARGET ${image} PROPERTY IMAGE_CONF_SCRIPT)
             list(APPEND tmp_conf_scripts "${CMAKE_SOURCE_DIR}/image_configurations/MY_CUSTOM_TYPE_image_default.cmake")
             set_target_properties(${image} PROPERTIES IMAGE_CONF_SCRIPT "${tmp_conf_scripts}")
           endforeach()
         endfunction(${SYSBUILD_CURRENT_MODULE_NAME}_pre_cmake)

镜像配置脚本（Zephyr 全局）
----------------------------------------

全局 Zephyr 提供的镜像配置脚本，允许在使用
:cmake:command:`ExternalZephyrProject_Add` 时指定类型，
需要更改 Zephyr 中的 sysbuild 代码。
这应该只在添加任何项目都应该能选择的新类型时添加，
通常这应该只用于上游 Zephyr，
尽管 Zephyr 的 fork 版本可能使用这个无限制地添加额外类型。

镜像配置有名称允许列表，必须在 Zephyr 文件
:zephyr_file:`share/sysbuild/cmake/modules/sysbuild_extensions.cmake` 中的
:cmake:command:`ExternalZephyrProject_Add` 函数中设置。
添加新类型后，它可以在添加 sysbuild 镜像时使用，例如：

.. tabs::

   .. group-tab:: ``sysbuild_extensions.cmake``

      完整文件路径：``share/sysbuild/cmake/modules/sysbuild_extensions.cmake``

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

      完整文件路径：``share/sysbuild/image_configurations/MY_CUSTOM_TYPE_image_default.cmake``

      .. code-block:: cmake

         # 这里，ZCMAKE_APPLICATION 变量将被替换为正在配置的镜像
         set_config_bool(${ZCMAKE_APPLICATION} CONFIG_BUILD_OUTPUT_HEX y)

读取镜像配置
===========================

Kconfig
-------

镜像的 Kconfig 值可以被 sysbuild **在镜像的 CMake 配置已发生之后**读取。
这可以用于检查配置或根据配置调整额外的 sysbuild 任务。
以下函数可以用于这个目的：

.. code-block:: cmake

   sysbuild_get(<variable> IMAGE <image> [VAR <image-variable>] KCONFIG)

这个函数只能在 :ref:`sysbuild 被模块扩展 <sysbuild_module_integration>` 时
或在 ``sysbuild/CMakeLists.txt`` 文件内部在使用 ``find_package(Sysbuild)`` 之后使用。
显示输出所有镜像值的示例：

.. tabs::

   .. group-tab:: 模块 CMake

      .. code-block:: cmake

         function(${SYSBUILD_CURRENT_MODULE_NAME}_post_cmake)
           cmake_parse_arguments(POST_CMAKE "" "" "IMAGES" ${ARGN})

           foreach(image ${POST_CMAKE_IMAGES})
             # 注意要读取的变量在使用 sysbuild_get() 函数之前不能被设置
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
