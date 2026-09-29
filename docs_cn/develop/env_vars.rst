.. _env_vars:

环境变量
=====================

本文档
中
的
各种
页面
引用
设置
Zephyr
特定
环境变量。
本页
描述
如何
做。

设置
变量
*****************

选项
1：
只
一次
-------------------

要
将
环境变量
``MY_VARIABLE`` 设置
为
``foo``
用于
当前
终端
窗口
的
生命周期：

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         export MY_VARIABLE=foo

   .. group-tab:: Windows

      .. code-block:: console

         set MY_VARIABLE=foo

.. warning::

   这
   最
   适合
   实验。
   如果
   你
   关闭
   终端
   窗口、
   使用
   另一个
   终端
   窗口
   或
   标签、
   重启
   电脑
   等，
   这个
   设置
   将
   永远
   丢失。

   如果
   你
   想
   继续
   使用
   设置，
   推荐
   使用
   选项
   2
   或
   3。

选项
2：
在
所有
终端
中
--------------------------

.. tabs::

   .. group-tab:: Linux/macOS

      将
      ``export MY_VARIABLE=foo`` 行
      添加
      到
      你
      主
      目录
      中
      你
      shell
      的
      启动
      脚本。
      对于
      Bash，
      这
      通常
      是
      Linux
      上
      的
      :file:`~/.bashrc`
      或
      macOS
      上
      的
      :file:`~/.bash_profile`。
      这些
      启动
      脚本
      中
      的
      更改
      不
      影响
      已
      启动
      的
      shell
      实例；
      尝试
      打开
      新
      终端
      窗口
      获取
      新
      设置。

   .. group-tab:: Windows

      你
      可以
      在
      ``cmd.exe`` 中
      使用
      ``setx`` 程序
      或
      第三方
      RapidEE
      程序。

      要
      使用
      ``setx``，
      键入
      这个
      命令，
      然后
      关闭
      终端
      窗口。
      任何
      新
      ``cmd.exe`` 窗口
      将
      有
      ``MY_VARIABLE`` 设置
      为
      ``foo``。

      .. code-block:: console

         setx MY_VARIABLE foo

      要
      安装
      RapidEE，
      一个
      免费
      图形
      环境变量
      编辑器，
      `使用
      Chocolatey`_
      在
      管理员
      命令
      提示符
      中：

      .. code-block:: console

         choco install rapidee

      然后
      你
      可以
      从
      终端
      运行
      ``rapidee`` 启动
      程序
      并
      设置
      环境变量。
      确保
      使用
      "User"
      环境变量
      区域
      --
      否则，
      你
      必须
      以
      管理员
      身份
      运行
      RapidEE。
      退出
      前
      确保
      通过
      点击
      左上
      角
      的
      Save
      按钮
      保存
      你的
      更改。
      你
      在
      RapidEE
      中
      做
      的
      设置
      在
      你
      打开
      新
      终端
      窗口
      时
      将
      可用。

.. _env_vars_zephyrrc:

选项
3：
使用
``zephyr_rc`` 文件
----------------------------------

如果
你
不
想
让
变量
的
设置
对
你的
所有
终端
可用，
但
仍
想
保存
值
用于
使用
Zephyr
时
加载
到
你的
环境
中，
选择
这个
选项。

.. tabs::

   .. group-tab:: Linux/macOS

      Zephyr
      支持
      :file:`zephyrrc` 文件
      的
      多个
      位置，
      在
      可能
      时
      遵循
      XDG
      Base
      Directory
      Specification。
      在
      以下
      位置
      之一
      创建
      zephyrrc
      文件
      （它们
      将
      按
      顺序
      检查）：

      #. :file:`$XDG_CONFIG_HOME/zephyr/zephyrrc`
      #. :file:`$HOME/.config/zephyr/zephyrrc`
      #. :file:`$HOME/.zephyrrc`

      将
      这
      行
      添加
      到
      你
      偏好
      位置
      的
      文件：

      .. code-block:: console

         export MY_VARIABLE=foo

      要
      将
      这个
      值
      取回
      你的
      当前
      终端
      环境，
      **你
      必须
      运行**
      ``source zephyr-env.sh``
      从
      主
      ``zephyr`` 仓库。
      除
      其他
      事情
      外，
      这个
      脚本
      source
      你的
      :file:`zephyrrc`
      （它
      从
      上面
      位置
      列表
      找到
      的
      第一个）。

      如果
      你
      关闭
      窗口
      等，
      值
      将
      丢失；
      重新
      运行
      ``source
      zephyr-env.sh`` 取回
      它。

   .. group-tab:: Windows

      用
      记事本
      这样
      的
      文本
      编辑器
      将
      ``set MY_VARIABLE=foo`` 行
      添加
      到
      文件
      :file:`%userprofile%\\zephyrrc.cmd`
      保存
      值。

      要
      将
      这个
      值
      取回
      你的
      当前
      终端
      环境，
      **你
      必须
      运行**
      ``zephyr-env.cmd``
      在
      ``cmd.exe`` 窗口
      中
      在
      更改
      目录
      到
      主
      ``zephyr`` 仓库
      之后。
      除
      其他
      事情
      外，
      这个
      脚本
      运行
      :file:`%userprofile%\\zephyrrc.cmd`。

      如果
      你
      关闭
      窗口
      等，
      值
      将
      丢失；
      重新
      运行
      ``zephyr-env.cmd`` 取回
      它。

      这些
      脚本：

      - 将
        :envvar:`ZEPHYR_BASE` 设置
        为
        zephyr
        仓库
        的
        位置
      - 向
        你的
        :envvar:`PATH` 环境变量
        添加
        某些
        Zephyr
        特定
        位置
        （如
        zephyr
        的
        :file:`scripts`
        目录）
      - 加载
        上面
        :ref:`env_vars_zephyrrc`
        中
        描述
        的
        ``zephyrrc`` 文件
        中
        的
        任何
        设置。

      因此
      你
      可以
      在
      你
      需要
      任何
      这些
      设置
      的
      任何
      时候
      使用
      它们。

.. _zephyr-env:

Zephyr
环境
脚本
**************************

你
可以
使用
zephyr
仓库
脚本
``zephyr-env.sh``（用于
macOS
和
Linux）
和
``zephyr-env.cmd``（用于
Windows）
将
Zephyr
特定
设置
加载
到
当前
终端
的
环境
中。
要
做到
这，
从
zephyr
仓库
运行
这个
命令：

.. tabs::

   .. group-tab:: Linux/macOS

      .. code-block:: console

         source zephyr-env.sh

   .. group-tab:: Windows

      .. code-block:: console

         zephyr-env.cmd

这些
脚本：

- 将
  :envvar:`ZEPHYR_BASE` 设置
  为
  zephyr
  仓库
  的
  位置
- 向
  你的
  ``PATH`` 环境变量
  添加
  某些
  Zephyr
  特定
  位置
  （如
  zephyr
  的
  :file:`scripts`
  目录）
- 加载
  上面
  :ref:`env_vars_zephyrrc`
  中
  描述
  的
  ``zephyrrc`` 文件
  中
  的
  任何
  设置。

因此
你
可以
在
你
需要
任何
这些
设置
的
任何
时候
使用
它们。

.. _env_vars_important:

重要
环境变量
*******************************

一些
:ref:`important-build-vars`
也
可以
在
环境
中
设置。
这里
是
一些
这些
重要
环境变量
的
描述。
这
不
是
全面
的
列表。

.. envvar:: BOARD

   见
   :ref:`important-build-vars`。

.. envvar:: CONF_FILE

   见
   :ref:`important-build-vars`。

.. envvar:: SHIELD

   见
   :ref:`shields`。

.. envvar:: ZEPHYR_BASE

   见
   :ref:`important-build-vars`。

.. envvar:: EXTRA_ZEPHYR_MODULES

   见
   :ref:`important-build-vars`。

.. envvar:: ZEPHYR_MODULES

   见
   :ref:`important-build-vars`。

.. envvar:: ZEPHYR_BOARD_ALIASES

   见
   :ref:`gs-board-aliases`

以下
额外
环境变量
在
配置
用于
构建
Zephyr
应用
的
:ref:`工具链 <gs_toolchain>` 时
重要。

.. envvar:: ZEPHYR_SDK_INSTALL_DIR

   Zephyr
   SDK
   安装
   的
   路径。

.. envvar:: ZEPHYR_TOOLCHAIN_VARIANT

   要
   使用
   的
   工具链
   的
   名称。

.. envvar:: {TOOLCHAIN}_TOOLCHAIN_PATH

   :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
   指定
   的
   工具链
   的
   路径。
   例如，
   如果
   ``ZEPHYR_TOOLCHAIN_VARIANT=host/llvm``，
   使用
   ``LLVM_TOOLCHAIN_PATH``。
   （注意
   形成
   环境变量
   名称
   时
   的
   大写
   小写。）

你
可能
在
:ref:`更新
Zephyr
SDK
工具链 <gs_toolchain_update>` 时
需要
更新
这些
变量
中
的
某些。

仿真器
和
开发板
可能
也
依赖
额外
的
程序。
构建
系统
将
尝试
自动
定位
这些
程序，
但
可能
依赖
额外
的
CMake
或
环境变量
来
做到
。
请
查阅
你的
仿真器
或
开发板
的
文档
获取
更多
信息。
以下
环境变量
在
这种
情况
下
可能
有用：

.. envvar:: PATH

   ``PATH``
   是
   在
   Unix
   类
   或
   Microsoft
   Windows
   操作
   系统
   上
   使用
   的
   环境变量，
   用于
   指定
   可
   执行
   程序
   位于
   的
   一
   组
   目录。

.. _使用
   Chocolatey: https://chocolatey.org/packages/RapidEE
