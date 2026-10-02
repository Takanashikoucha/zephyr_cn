.. _kconfig:

配置系统（Kconfig）
*******************************

Zephyr 内核和子系统可以在构建时配置，以适应特定应用和平台需求。配置通过
Kconfig 处理，这是 Linux 内核使用的相同配置系统。目标是支持配置而无需更改
任何源代码。

配置选项（通常称为 *符号*）定义在 :file:`Kconfig` 文件中，这些文件还指定
确定哪些配置有效的符号之间的依赖关系。符号可以分组到菜单和子菜单，以保持
交互式配置接口有序。

Kconfig 的输出是一个头文件 :file:`autoconf.h`，带有可以在构建时测试的宏。
未使用功能的代码可以被编译掉以节省空间。

以下章节解释如何设置 Kconfig 配置选项，深入介绍 Kconfig 在 Zephyr 项目中
如何使用，并提供一些编写 :file:`Kconfig` 文件的技巧和最佳实践。

.. toctree::
   :maxdepth: 1

   menuconfig.rst
   tracing.rst
   setting.rst
   tips.rst
   preprocessor-functions.rst
   extensions.rst

对优化其配置以获得安全性感兴趣的用户应参考 Zephyr 安全指南中关于
:ref:`hardening` 的章节。
