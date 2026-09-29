.. _getting_started:

入门
指南
#####################

按
本
指南
做：

- 在
  Ubuntu、macOS 或
  Windows
  上
  设置
  命令行
  Zephyr
  开发
  环境
  （其他
  Linux
  发行版
  的
  说明
  在
  :ref:`installation_linux`
  中
  讨论）
- 获取
  源
  代码
- 构建、
  烧录
  和
  运行
  示例
  应用

.. _host_setup:

选择
并
更新
OS
********************

点击
你
正在
使用
的
操作
系统。

.. tabs::

   .. group-tab:: Ubuntu

      本
      指南
      涵盖
      Ubuntu
      版本
      24.04
      LTS
      及
      之后。
      如果
      你
      使用
      不同
      的
      Linux
      发行版
      见
      :ref:`installation_linux`。

      .. code-block:: bash

         sudo apt update
         sudo apt upgrade

   .. group-tab:: macOS

      选择
      :menuselection:`系统
      设置
      -->
      通用
      -->
      软件
      更新`
      并
      安装
      任何
      可用
      的
      更新。
      更多
      细节
      见
      `这个
      Apple
      支持
      主题
      <https://support.apple.com/en-us/HT201541>`_。

      .. note::

         不
         支持
         x86-64
         macOS。

   .. group-tab:: Windows

      选择
      :menuselection:`开始
      -->
      设置
      -->
      更新
      和
      安全
      -->
      Windows
      Update`。
      点击
      :guilabel:`检查
      更新`
      并
      安装
      任何
      可用
      的
      更新。

.. _install-required-tools:

安装
依赖
********************

接下来，
安装
Zephyr
需要
来
配置
和
构建
应用
的
主机
工具。
下面
的
说明
使用
每个
操作
系统
推荐
的
包
管理器，
使
工具
从
你的
终端
可用。

当前
主要
依赖
的
最低
要求
版本
是：

.. list-table::
   :header-rows: 1

   * - 工具
     - 最低
     版本

   * - `CMake <https://cmake.org/>`_
     - 3.28.0

   * - `Python <https://www.python.org/>`_
     - 3.12

   * - `Devicetree
      编译器
      <https://www.devicetree.org/>`_
     - 1.4.6

.. note::

   强烈
   推荐
   Python
   3.12。
   使用
   更
   新
   的
   Python
   发布
   版本
   可能
   在
   某些
   系统
   上
   失败，
   例如
   在
   Windows
   上
   安装
   需要
   的
   包
   时。

.. tabs::

   .. group-tab:: Ubuntu

      .. _install_dependencies_ubuntu:

      #. 使用
         ``apt``
         安装
         需要
         的
         依赖：

         .. code-block:: bash

            sudo apt install --no-install-recommends git cmake ninja-build gperf \
              ccache dfu-util device-tree-compiler wget python3-dev python3-venv python3-tk \
              xz-utils file make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

         .. note::

            由于
            AArch64
            （ARM64）
            系统
            上
            ``gcc-multilib``
            和
            ``g++-multilib``
            不
            可用，
            你
            可能
            需要
            从
            要
            安装
            的
            包
            列表
            中
            省略
            它们。

      #. 通过
         键入
         以下
         内容
         验证
         系统
         上
         安装
         的
         主要
         依赖
         的
         版本：

         .. code-block:: bash

            cmake --version
            python3 --version
            dtc --version

         对照
         本
         节
         开头
         表格
         中
         的
         版本
         检查
         它们。
         关于
         手动
         更新
         依赖
         的
         额外
         信息
         参见
         :ref:`installation_linux`
         页面。

   .. group-tab:: macOS

      .. _install_dependencies_macos:

      #. 安装
         `Homebrew <https://brew.sh/>`_：

         .. code-block:: bash

            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

      #. Homebrew
         安装
         脚本
         完成
         后，
         按
         屏幕
         上
         的
         说明
         将
         Homebrew
         安装
         添加
         到
         路径。

         .. code-block:: bash

            (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> ~/.zprofile
            source ~/.zprofile

      #. 使用
         ``brew``
         安装
         需要
         的
         依赖：

         .. code-block:: bash

            brew install cmake ninja gperf python3 python-tk ccache qemu dtc libmagic wget openocd

      #. 将
         Homebrew
         Python
         文件夹
         添加
         到
         路径，
         使
         你
         可以
         执行
         ``python``
         和
         ``pip``
         以及
         ``python3``
         和
         ``pip3``。

            .. code-block:: bash

               (echo; echo 'export PATH="'$(brew --prefix)'/opt/python/libexec/bin:$PATH"') >> ~/.zprofile
               source ~/.zprofile

   .. group-tab:: Windows

      .. note::

         这些
         说明
         涵盖
         本地
         Windows
         环境。
         你
         也
         可以
         通过
         遵循
         本
         指南
         中
         的
         Ubuntu
         说明
         使用
         `Windows
         子系统
         Linux
         （WSL）
         <https://learn.microsoft.com/windows/wsl/install>`_。
         在
         这种
         情况
         下，
         注意
         从
         WSL
         内部
         烧录
         和
         调试
         硬件
         需要
         首先
         使
         USB
         设备
         对
         WSL
         可见，
         例如
         使用
         `usbipd-win <https://github.com/dorssel/usbipd-win>`_。

      在
      现代
      Windows
      版本
      （10
      及
      之后）
      上，
      从
      Microsoft
      Store
      安装
      Windows
      Terminal。
      下面
      的
      说明
      在
      ``cmd.exe``
      或
      PowerShell
      中
      都
      有效。

      这些
      说明
      使用
      Windows
      的
      官方
      包
      管理器
      `winget`_。
      如果
      winget
      不
      是
      选项，
      从
      其
      各自
      网站
      安装
      依赖
      并
      确保
      其
      命令行
      工具
      在
      你的
      :envvar:`PATH`
      :ref:`环境变量 <env_vars>`
      中。

      |p|

      .. _install_dependencies_windows:

      #. 在
         现代
         Windows
         版本
         中，
         winget
         已
         默认
         预
         安装。
         你
         可以
         在
         终端
         窗口
         中
         键入
         ``winget``
         验证
         是
         这样
         的。
         如果
         失败，
         你
         可以
         `安装
         winget`_。

      #. 打开
         命令
         提示符
         （``cmd.exe``）
         或
         PowerShell
         终端
         窗口。
         要
         做到
         这，
         按
         Windows
         键，
         键入
         ``cmd.exe``
         或
         PowerShell
         并
         点击
         结果。

      #. 使用
         ``winget``
         安装
         需要
         的
         依赖：

         .. code-block:: bat

            winget install Kitware.CMake Ninja-build.Ninja oss-winget.gperf Python.Python.3.12 Git.Git oss-winget.dtc wget 7zip.7zip

      #. 关闭
         终端
         窗口。

      .. note::

         你
         可能
         需要
         将
         7zip
         安装
         文件夹
         添加
         到
         你的
         ``PATH``。


.. _winget: https://learn.microsoft.com/en-us/windows/package-manager/
.. _安装
   winget: https://aka.ms/getwinget

.. _get_the_code:
.. _clone-zephyr:
.. _install_py_requirements:
.. _gs_python_deps:

获取
Zephyr
并
安装
Python
依赖
******************************************

接下来，
使用
:ref:`west <west>` 创建
工作区
并
获取
Zephyr
连同
其
:ref:`模块 <modules>`。

这些
命令
使用
:file:`zephyrproject` 作为
工作区
名称；
你
可以
选择
其他
名称
和
位置。
你
还
将
在
`Python
虚拟
环境`_
中
安装
Zephyr
的
Python
依赖
使
它们
与
你的
系统
Python
安装
保持
分离。

.. _Python
   虚拟
   环境: https://docs.python.org/3/library/venv.html

#. 创建
   新
   虚拟
   环境：

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            python3 -m venv ~/zephyrproject/.venv

      .. group-tab:: macOS

         .. code-block:: bash

            python3 -m venv ~/zephyrproject/.venv

      .. group-tab:: Windows

         以
         **普通
         用户**
         身份
         打开
         ``cmd.exe``
         或
         PowerShell
         终端
         窗口。

         .. tabs::

            .. code-tab:: bat

               cd %HOMEPATH%
               py -3.12 -m venv zephyrproject\.venv

            .. code-tab:: powershell

               cd $Env:HOMEPATH
               py -3.12 -m venv zephyrproject\.venv

#. 激活
   虚拟
   环境：

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            source ~/zephyrproject/.venv/bin/activate

      .. group-tab:: macOS

         .. code-block:: bash

            source ~/zephyrproject/.venv/bin/activate

      .. group-tab:: Windows

         .. note::

            Python
            的
            虚拟
            环境
            在
            PowerShell
            中
            激活
            需要
            运行
            脚本
            本身，
            它
            需要
            被
            允许。

            .. code-block:: powershell

               Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

         .. tabs::

            .. code-tab:: bat

               zephyrproject\.venv\Scripts\activate.bat

            .. code-tab:: powershell

               zephyrproject\.venv\Scripts\Activate.ps1

   激活
   后
   你的
   shell
   将
   有
   ``(.venv)`` 前缀。
   虚拟
   环境
   可以
   通过
   运行
   ``deactivate``
   随时
   取消
   激活。

   .. note::

      记住
      每次
      你
      开始
      新
      终端
      会话
      后
      在
      使用
      Zephyr
      前
      激活
      虚拟
      环境。
      如果
      不
      这样
      做，
      像
      ``west``
      这样
      的
      命令
      将
      找不到，
      或
      可能
      针对
      不同
      的
      Python
      环境
      运行，
      导致
      令人
      困惑
      的
      错误。

#. 安装
   west：

   West
   是
   Zephyr
   的
   工作区
   管理器；
   下一
   命令
   使用
   它
   创建
   和
   更新
   工作区。

   .. code-block:: shell

      pip install west

#. 获取
   Zephyr
   源
   代码：

   ``west init``
   创建
   :term:`west
   工作区`
   并
   克隆
   ``https://github.com/zephyrproject-rtos/zephyr``
   作为
   其
   :term:`清单
   仓库
   <west
   manifest
   repository>`。

   ``west update``
   然后
   获取
   Zephyr
   :term:`west
   清单`
   中
   列出
   的
   各种
   :term:`west
   项目
   <west
   project>`
   （模块）
   （硬件
   抽象
   层
   （HAL）、
   库
   等）。

   .. tabs::

      .. group-tab:: Ubuntu

         .. only:: not release

            .. code-block:: bash

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject
               cd ~/zephyrproject
               west update

         .. only:: release

            .. parsed-literal::

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject --mr v |zephyr-version-ltrim|
               cd ~/zephyrproject
               west update

      .. group-tab:: macOS

         .. only:: not release

            .. code-block:: bash

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject
               cd ~/zephyrproject
               west update

         .. only:: release

            .. parsed-literal::

               west init -m https://github.com/zephyrproject-rtos/zephyr ~/zephyrproject --mr v |zephyr-version-ltrim|
               cd ~/zephyrproject
               west update

      .. group-tab:: Windows

         .. only:: not release

            .. code-block:: bat

               west init -m https://github.com/zephyrproject-rtos/zephyr zephyrproject
               cd zephyrproject
               west update

         .. only:: release

            .. parsed-literal::

               west init -m https://github.com/zephyrproject-rtos/zephyr zephyrproject --mr v |zephyr-version-ltrim|
               cd zephyrproject
               west update

   .. tip::

      要
      减少
      磁盘
      空间
      使用
      并
      避免
      在
      设置
      期间
      下载
      不必要
      的
      模块
      或
      厂商
      HAL，
      你
      可以
      在
      运行
      ``west update``
      前
      配置
      :ref:`west-manifest-groups`。

#. 安装
   Zephyr
   的
   Python
   依赖：

   ``west packages``
   从
   检出
   的
   Zephyr
   工作区
   （包括
   其
   模块）
   读取
   Python
   要求，
   因此
   安装
   的
   包
   与
   你
   获取
   的
   Zephyr
   版本
   匹配。

   .. tabs::

      .. group-tab:: Ubuntu

         .. code-block:: bash

            west packages pip --install

      .. group-tab:: macOS

         .. code-block:: bash

            west packages pip --install

      .. group-tab:: Windows

         .. tabs::

            .. code-tab:: bat

               cmd /c zephyr\scripts\utils\west-packages-pip-install.cmd

            .. code-tab:: powershell

               python -m pip install @((west packages pip) -split ' ')

   .. note::

      安装
      这些
      依赖
      可以
      降级
      或
      升级
      west
      本身。

#. 导出
   :ref:`Zephyr
   CMake
   包 <cmake_pkg>`。
   这
   将
   当前
   Zephyr
   checkout
   注册
   到
   CMake
   的
   用户
   包
   注册表
   使
   ``find_package(Zephyr)``
   在
   构建
   应用
   时
   可以
   自动
   定位
   它。

   .. code-block:: shell

      west zephyr-export

安装
Zephyr
SDK
**********************

:ref:`Zephyr
软件
开发
套件
（SDK）
<toolchain_zephyr_sdk>`
包含
Zephyr
每个
受
支持
架构
的
工具链。
这些
工具链
包括
编译器、
汇编器、
链接器
和
构建
Zephyr
应用
用于
你的
目标
硬件
所需
的
其他
程序。

它
还
包含
额外
的
主机
工具，
如
自定义
QEMU
和
OpenOCD
构建，
用于
仿真、
烧录
和
调试
Zephyr
应用。

从
Zephyr
仓库
用
``west sdk install``
安装
Zephyr
SDK：

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west sdk install

   .. group-tab:: macOS

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west sdk install

   .. group-tab:: Windows

      .. tabs::

         .. code-tab:: bat

            cd %HOMEPATH%\zephyrproject\zephyr
            west sdk install

         .. code-tab:: powershell

            cd $Env:HOMEPATH\zephyrproject\zephyr
            west sdk install

.. tip::

   使用
   命令
   选项
   选择
   SDK
   安装
   目标
   或
   只
   安装
   选定
   架构
   工具链。
   细节
   见
   ``west sdk install --help``。

.. note::

    如果
    你
    想
    不
    使用
    ``west sdk``
    命令
    安装
    Zephyr
    SDK，
    请
    见
    :ref:`toolchain_zephyr_sdk_install`。

.. _getting_started_run_sample:

构建
Blinky
示例
***********************

.. note::

   :zephyr:code-sample:`blinky`
   与
   大多数
   但
   不
   是
   所有
   :ref:`开发板`
   兼容。
   如果
   你的
   开发板
   不
   满足
   Blinky
   的
   :ref:`blinky-sample-requirements`，
   那么
   :zephyr:code-sample:`hello_world`
   是
   好
   的
   替代
   方案。

   如果
   你
   不
   确定
   west
   用
   什么
   名称
   指
   你的
   开发板，
   使用
   ``west boards``
   列出
   Zephyr
   支持
   的
   所有
   开发板。
   你的
   开发板
   的
   :zephyr:board-catalog:`文档
   页面`
   也
   显示
   要
   传递
   给
   ``west build``
   的
   精确
   开发板
   目标
   名称。

用
:ref:`west
build <west-building>`
构建
:zephyr:code-sample:`blinky`。
将
``<your-board-name>``
替换
为
你的
开发板
名称：

.. tabs::

   .. group-tab:: Ubuntu

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west build -p always -b <your-board-name> samples/basic/blinky

   .. group-tab:: macOS

      .. code-block:: bash

         cd ~/zephyrproject/zephyr
         west build -p always -b <your-board-name> samples/basic/blinky

   .. group-tab:: Windows

      .. tabs::

         .. code-tab:: bat

            cd %HOMEPATH%\zephyrproject\zephyr
            west build -p always -b <your-board-name> samples\basic\blinky

         .. code-tab:: powershell

            cd $Env:HOMEPATH\zephyrproject\zephyr
            west build -p always -b <your-board-name> samples\basic\blinky

``-p always``
选项
强制
干净
构建，
删除
之前
任何
配置
的
构建
输出。
这
避免
你
入门
时
的
过期
文件。
之后，
你
可以
使用
``-p auto``
让
``west build``
启发式
方法
决定
何时
可能
需要
干净
构建。
细节
见
``west build -h``。

.. note::

   开发板
   可能
   包含
   一个
   或多个
   SoC，
   每个
   SoC
   可能
   包含
   一个
   或多个
   CPU
   簇。
   为
   这种
   开发板
   构建
   时，
   指定
   示例
   必须
   构建
   的
   SoC
   或
   CPU
   簇。
   例如
   为
   :zephyr:board:`nrf5340dk`
   上
   的
   ``cpuapp``
   核心
   构建
   :zephyr:code-sample:`blinky`，
   开发板
   必须
   提供
   为：
   ``nrf5340dk/nrf5340/cpuapp``。
   更多
   细节
   也
   见
   :ref:`board_terminology`。

烧录
示例
****************

连接
你的
开发板，
通常
通过
USB，
如果
有
电源
开关
就
打开
它。
如果
不
确定
要
做
什么，
检查
:ref:`boards`
中
你的
开发板
的
页面，
因为
某些
开发板
需要
特定
设置
或
流程
才能
烧录。

用
:ref:`west
flash <west-flashing>`
烧录
示例。
这
将
你
刚
构建
的
应用
编程
到
连接
的
开发板
上：

.. code-block:: shell

   west flash

.. note::

    你
    可能
    需要
    安装
    你的
    开发板
    需要
    的
    额外
    :ref:`主机
    工具 <flash-debug-host-tools>`。
    如果
    缺少
    任何
    需要
    的
    依赖，
    ``west flash``
    命令
    将
    打印
    错误。

.. note::

    在
    Linux
    上，
    你
    可能
    在
    首次
    用
    调试
    探针
    烧录
    前
    需要
    配置
    udev
    规则。
    见
    :ref:`setting-udev-rules`。

如果
你
使用
blinky，
LED
将
开始
闪烁，
如
此
图
所示：

.. figure:: img/ReelBoard-Blinky.webp
   :width: 400px
   :name: reelboard-blinky

   Phytec
   :zephyr:board:`reel_board <reel_board>`
   运行
   blinky

下一步
**********

这里
是
一些
探索
Zephyr
的
下一步：

* 尝试
  其他
  :zephyr:code-sample-category:`samples`
* 了解
  :ref:`应用`
  和
  :ref:`west <west>`
  工具
* 了解
  west
  的
  :ref:`烧录
  和
  调试 <west-build-flash-debug>`
  功能，
  或
  更
  多
  了解
  :ref:`flashing_and_debugging`
  的
  一般
  情况
* 查看
  :ref:`beyond-GSG`
  获取
  额外
  设置
  替代
  方案
  和
  想法
* 发现
  :ref:`project-resources`
  从
  Zephyr
  社区
  获取
  帮助

.. _help:

请求
帮助
***************

在
请求
帮助
前，
搜索
本
文档、
Zephyr
项目
的
GitHub
讨论
和
issue，
以及
Discord
聊天
历史。
你的
问题
可能
已经
在
那里
有
答案。
你
也
可以
询问
从
本
文档
每个
页面
可用
的
:ref:`聊天
机器人 <kapa_ai>`。

* **邮件
  列表**：
  users@lists.zephyrproject.org
  通常
  是
  请求
  帮助
  的
  正确
  列表。
  `搜索
  存档
  和
  在这里
  注册`_。
* **GitHub**：
  用
  `GitHub
  讨论`_
  提问，
  用
  `GitHub
  issues`_
  报告
  bug
  和
  功能
  请求。
* **Discord**：
  你
  可以
  用
  这个
  `Discord
  邀请`_
  加入。

请求
帮助
时，
包括：

#. 你
   想
   做
   什么
#. 你
   尝试
   了
   什么，
   包括
   你
   运行
   的
   命令
#. 发生
   了
   什么，
   包括
   完整
   文本
   输出

复制
粘贴
文本
而非
分享
截图。
对于
Discord
或
GitHub
上
超过
5
行
的
终端
输出、
源
代码
或
日志，
用
三个
反
引号
创建
一个
代码
片段。

.. _搜索
   存档
   和
   在这里
   注册: https://lists.zephyrproject.org/g/users
.. _GitHub
   讨论: https://github.com/zephyrproject-rtos/zephyr/discussions
.. _Discord
   邀请: https://chat.zephyrproject.org
.. _GitHub
   issues: https://github.com/zephyrproject-rtos/zephyr/issues
