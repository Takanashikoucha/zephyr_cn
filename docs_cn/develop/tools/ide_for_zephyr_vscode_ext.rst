.. _ide_for_zephyr_vscode_ext:

IDE
for
Zephyr
（VS
Code
扩展）
##################################

`IDE
for
Zephyr`_
是
一
个
Visual
Studio
Code
（VS
Code）
扩展
用于
Zephyr
RTOS
开发。
它
支持
**主机
工具
管理**、
**west
workspace
设置**、
**SDK
管理**、
**项目
创建**、
**build/flash**
和
**调试**。

.. figure::
   img/ide-for-zephyr_main_vscode_ext.webp
   :align:
   center
   :alt:
   IDE
   for
   Zephyr
   main
   page
   showing
   UI
   with
   memory
   report

关键
功能
************

- 与
  Cortex-Debug
  集成
  用于
  ST-Link、
  J-Link、
  OpenOCD、
  Black
  Magic
  Probe
  和
  其他
  probes
  通过
  内置
  的
  ``zephyr-ide-cortex``
  和
  ``zephyr-ide-west``
  debugger
  类型
  自动
  解析
  ELF、
  GDB
  和
  runner
  路径
- 与
  clangd
  或
  C/C++
  集成
  用于
  IntelliSense
- 从
  Build
  Dashboard
  探索
  内存
  使用、
  Kconfig
  和
  devicetree；
  不
  离开
  VS
  Code
  将
  ROM
  和
  RAM
  作为
  sunburst
  chart
  查看
- 用
  内置
  编辑器
  交互式
  编辑
  Kconfig
  选项
- 从
  项目
  面板
  添加、
  运行
  和
  重新
  配置
  Twister
  测试
- 在
  Linux、
  macOS
  和
  Windows
  上
  自动
  安装
  native
  主机
  工具
  （CMake、
  Python
  3、
  Ninja、
  DTC、
  GCC
  等）
- 安装
  和
  管理
  Zephyr
  SDK
  版本
  和
  每
  架构
  工具链
- 从
  现有
  应用
  或
  Zephyr
  samples
  添加
  项目，
  带
  多
  个
  构建
  和
  每
  构建
  board
  和
  配置
  覆盖
- 将
  项目
  配置
  存储
  在
  版本
  可
  控制
  的
  :file:`.vscode/zephyr-ide.json`
  中，
  它
  可以
  指定
  SDKs、
  packages
  和
  blobs

兼容性
*************

- Windows
- Linux
- macOS

开始
***************
