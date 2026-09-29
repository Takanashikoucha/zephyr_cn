.. _win-setup-alts:

Windows
替代
设置
说明
######################################

.. _win-wsl:

Windows
10
WSL
（Windows
子系统
Linux）
********************************************

如果
你
运行
较
新
版本
的
Windows
10，
你
可以
利用
内置
功能
在
标准
命令
提示符
上
直接
本地
运行
Ubuntu
二进制
文件。
这
允许
你
使用
软件
如
:ref:`Zephyr
SDK
<toolchain_zephyr_sdk>`
而
不
需要
设置
虚拟
机。

.. warning::
      Windows
      10
      版本
      1803
      有
      一个
      问题
      会
      导致
      CMake
      不
      能
      正常
      工作，
      在
      版本
      1809
      （及
      之后）
      修复。
      更多
      信息
      可以
      在
      :github:`Zephyr
      Issue
      10420
      <10420>`
      中
      找到。

#. `安装
   Windows
   子系统
   Linux
   （WSL）`_。

   .. note::
         要
         Zephyr
         SDK
         正常
         工作
         你
         需要
         Windows
         10
         build
         15002
         或
         更
         高。
         你
         可以
         在
         系统
         设置
         的
         "关于
         你的
         PC"
         章节
         检查
         你
         运行
         的
         Windows
         10
         build。
         如果
         你
         运行
         旧
         Windows
         10
         build
         你
         可能
         需要
         安装
         Creator's
         Update。

#. 遵循
   :ref:`installation_linux`
   文档
   中
   的
   Ubuntu
   说明。

.. NOTE
   FOR
   DOCS
   AUTHORS:
   提醒，
   *不*
   将
   构建
   文档
   本身
   的
   依赖
   放
   这里。

.. _安装
   Windows
   子系统
   Linux
   （WSL）: https://msdn.microsoft.com/en-us/commandline/wsl/install_guide
