.. _external_module_grvl:

grvl
####

简介
****

`Graphics Rendering Visual Library`_（grvl）是一个面向基于 Zephyr 的
MCU 的轻量级 GUI 库，提供既适合资源受限设备、又具备现代响应式用户体验
的可移植方案。

内部实现上，grvl 链接一个名为 `tinyxml`_ 的标准 XML 库，用于解析
GUI 配置（代替代码）。UI 交互可使用集成的 `Duktape`_ JavaScript
引擎以 JavaScript 脚本化。

grvl 特性：

* 原生支持 PNG 和 JPEG 图形
* Simple DirectMedia Layer 兼容
* POSIX 合规和 Zephyr 支持
* 一组内置组件

  * 弹窗
  * 字体
  * 标签
  * 按钮
  * 滑块

* 用户自定义 prefab，可用于在运行时实例化复杂结构
* 基于 XML 的布局和 JavaScript 引擎

grvl 采用 Apache License 2.0。
tinyxml 采用 Zlib 许可。
Duktape 采用 MIT 许可。

在 Zephyr 中使用
****************

要将 grvl 作为 Zephyr :ref:`module <modules>` 使用，在 Zephyr 子
manifest（例如 ``zephyr/submanifests/grvl.yaml``）中添加以下条目，
然后运行 ``west update``，或者将其作为 West 项目添加到项目的
``west.yaml`` manifest：

.. code-block:: yaml

   manifest:
     projects:
       - name: grvl
         url: https://github.com/antmicro/grvl
         revision: main
         path: modules/grvl # adjust the path as needed

更多信息请参见 `grvl 文档`_ 或 `grvl 博客文章`_。

您还可以尝试交互式 `Zephyr 日历演示`_。

参考资料
********

.. target-notes::

.. _Graphics Rendering Visual Library:
   https://github.com/antmicro/grvl

.. _tinyxml:
   https://github.com/leethomason/tinyxml2

.. _Duktape:
   https://github.com/svaarala/duktape

.. _grvl 文档:
   https://antmicro.github.io/grvl/

.. _Zephyr 日历演示:
   https://github.com/antmicro/grvl-zephyr-calendar-demo

.. _grvl 博客文章:
  https://antmicro.com/blog/2025/12/grvl-a-lightweight-gui-library-for-zephyr-based-mcus
