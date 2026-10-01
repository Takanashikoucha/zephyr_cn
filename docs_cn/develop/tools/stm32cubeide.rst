.. _stm32cube_ide:

STM32CubeIDE
############

STM32CubeIDE_ 是 STMicroelectronics 推出的基于 Eclipse 的集成开发环境，专为 STM32 系列
MCU（微控制器）和 MPU（微处理器）设计。

本指南介绍如何使用该 IDE 设置、构建和调试 Zephyr 应用程序。

在使用本指南之前，项目必须已经通过 Zephyr 和 west 创建完成。

本指南中的步骤已在 Linux 上使用 IDE 1.16.0 版本验证可用。

项目设置
*************

#. 开始之前，请确保你拥有一个可用的 Zephyr 开发环境，
   参见 :ref:`getting_started` 中的说明。

#. 在你的 Zephyr 环境中运行 STM32CubeIDE。示例：

   .. code-block::

      $ /opt/st/stm32cubeide_1.16.0/stm32cubeide

#. 通过 :menuselection:`File --> New --> STM32 CMake Project` 打开你已有的项目：

   .. figure:: img/stm32cube_new_cmake.webp
      :align: center
      :alt: 创建新的 CMake 项目

#. 选择 :guilabel:`Project with existing CMake sources`，然后点击 :guilabel:`Next`。

#. 选择 :menuselection:`Next`，并浏览到源代码所在位置。
   打开的文件夹中应包含 ``CMakeLists.txt`` 和 ``prj.conf`` 文件。

#. 选择 :menuselection:`Next`，并选择合适的 MCU。
   按 :guilabel:`Finish` 后，你的项目即可使用了。
   不过，要正确配置项目，仍需要执行更多操作。

#. 在工作区（workspace）中右键点击新建的项目，选择 :guilabel:`Properties`。

#. 转到 :guilabel:`C/C++ Build` 页面，将生成器（Generator）设置为 ``Ninja``。
   在 :guilabel:`Other Options` 中，以 CMake 参数格式指定目标 ``BOARD``。
   如果目标是树外开发板（out-of-tree board），还必须设置 ``BOARD_ROOT`` 选项。
   最终得到的设置页面应类似如下所示：

   .. figure:: img/stm32cube_project_properties.webp
      :align: center
      :alt: 项目属性对话框

   是否需要这些选项，取决于你的项目是否为树外项目。

#. 转到 :menuselection:`C/C++ General --> Preprocessor Include` 页面。
   选择 :guilabel:`GNU C` 语言，然后点击 :menuselection:`CDT User Settings Entries` 选项。

   .. figure:: img/stm32cube_preprocessor_include.webp
      :align: center
      :alt: 预处理器选项的属性对话框

   点击 :guilabel:`Add`，添加一个 :guilabel:`Include File`，
   指向 Zephyr 的 ``autoconf.h`` 文件，其位置在
   ``<build dir>/zephyr/include/generated/autoconf.h``。这样可以确保
   STM32CubeIDE 能获取 Zephyr 的配置选项。
   随后会显示如下对话框，请按以下方式填写：

   .. figure:: img/stm32cube_add_include.webp
      :align: center
      :alt: 添加包含文件对话框

   添加包含文件后，你的属性页面应类似如下所示：

   .. figure:: img/stm32cube_autoconf_h.webp
      :align: center
      :alt: 添加 autoconf.h 文件后的属性页面

#. 点击 :guilabel:`Apply and Close`

#. 现在你可以使用工具栏上的 :guilabel:`Build` 按钮构建项目。
   项目可以使用 :guilabel:`Run` 按钮运行，也可以使用 :guilabel:`Debug` 按钮调试。

仅调试
**************

如果你只想使用 STM32CubeIDE 调试项目，可以按以下步骤操作：

#. 首先，确保你的项目已编译完成，并且 ``zephyr.elf`` 文件可用。

#. 运行 STM32CubeIDE，通过 :menuselection:`File --> Import...` 导入你的项目：

   .. figure:: img/stm32cube_menu_import.webp
      :align: center
      :alt: 导入项目

#. 选择 :menuselection:`C/C++ --> STM32 Cortex-M Executable`，然后点击 :guilabel:`Next`：

   .. figure:: img/stm32cube_import_project.webp
      :align: center
      :alt: 导入项目选择界面

#. 点击 :guilabel:`Browse`，浏览到你的构建（build）文件夹，并选择 ``zephyr.elf``。

#. 点击 :guilabel:`Select` 选择你的 MCU。如有需要，还可以选择 CPU 和/或核心（core）。

#. 点击 :guilabel:`Finish`。

#. 现在可以使用 :guilabel:`Debug` 按钮调试项目。

.. _STM32CubeIDE: https://www.st.com/en/development-tools/stm32cubeide.html
