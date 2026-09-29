.. _toolchain_zephyr_sdk:

Zephyr
SDK
##########

Zephyr
Software
Development
Kit
（SDK）
包含
GNU
和
LLVM
工具链
用于
Zephyr
的
每个
支持
架构。
它
还
包括
额外
的
主机
工具，
如
自定义
QEMU
和
OpenOCD。

高度
推荐
使用
Zephyr
SDK，
在
某些
条件
下
甚至
可能
是
必需
的
（例如
为
某些
架构
在
QEMU
中
运行
测试）。

支持
的
架构
***********************

Zephyr
SDK
支持
以下
目标
架构：

* ARC
  （32
  位
  和
  64
  位；
  ARCv1、
  ARCv2、
  ARCv3）
* ARM
  （32
  位
  和
  64
  位；
  ARMv6、
  ARMv7、
  ARMv8；
  A/R/M
  Profiles）
* Microblaze
  （32
  位）
* MIPS
  （32
  位
  和
  64
  位）
* RISC-V
  （32
  位
  和
  64
  位；
  RV32I、
  RV32E、
  RV64I）
* RX
* SPARC
  （32
  位
  和
  64
  位；
  SPARC
  V8、
  SPARC
  V9）
* x86
  （32
  位
  和
  64
  位）
* Xtensa

.. _toolchain_zephyr_sdk_bundle_variables:

安装
bundle
和
变量
*********************************

Zephyr
SDK
bundle
支持
所有
主要
操作系统
（Linux、
macOS
和
Windows）
并
作为
压缩
文件
交付。

为
了
方便
分发，
SDK
被
预
打包
成
三
个
不同
的
变体
你
可以
下载：

.. list-table::
   SDK
   Bundle
   Variants
   :widths:
   20
   20
   60
   :header-rows:
   1

   * - Variant
     - Host
       Tools
     - Toolchains
       Included
   * - ``gnu``
     - Yes
     - GNU
       （Binutils、
       GCC
       和
       GDB）
       用于
       所有
       支持
       架构
   * - ``llvm``
     - Yes
     - LLVM/Clang
   * - ``minimal``
     - Yes
     - None

安装
过程
包括
解压
下载
的
bundle
文件
并
运行
包含
的
setup
脚本。

不管
你
下载
哪
个
bundle，
安装
期间
你
会
被
提示
选择
要
安装
的
工具链
哪个，
如果
它
不
在
setup
脚本
执行
的
本地
目录
中
找到
它
将
在
安装
期间
被
下载。
也
可以
下载
并
解压
GNU
和
LLVM
SDK
bundles
到
同一
个
目录
树
中
并
用
这
种
方式
安装
两
个
而
不
需要
在
setup
脚本
执行
期间
下载
任何
一
个。

额外
的
OS
特定
说明
在
下面
的
节
中
描述。

如果
没有
选择
工具链，
构建
系统
搜索
Zephyr
SDK
并
使用
从
那里
的
工具链。
你
可以
通过
设置
环境
变量
:envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
为
``zephyr``
强制
这。

如果
你
在
默认
位置
（列出
在
下面
的
操作
系统
特定
说明
中）
之外
安装
Zephyr
SDK
并
你
想要
Zephyr
SDK
的
自动
发现，
那么
你
必须
通过
运行
setup
脚本
将
Zephyr
SDK
注册
到
CMake
package
registry
中。
如果
你
决定
不
将
Zephyr
SDK
注册
到
CMake
registry
中，
那么
:envvar:`ZEPHYR_SDK_INSTALL_DIR`
可以
用
来
指向
Zephyr
SDK
安装
目录。

你
也
可以
设置
:envvar:`ZEPHYR_SDK_INSTALL_DIR`
指向
包含
多
个
Zephyr
SDKs
的
目录，
允许
自动
工具链
选择。
例如，
你
可以
设置
``ZEPHYR_SDK_INSTALL_DIR``
为
``/company/tools``，
其中
``company/tools``
文件夹
包含
以下
子
文件夹：

* ``/company/tools/zephyr-sdk-0.13.2``
* ``/company/tools/zephyr-sdk-a.b.c``
* ``/company/tools/zephyr-sdk-x.y.z``

这
允许
Zephyr
构建
系统
选择
正确
版本
的
SDK，
同时
允许
多
个
Zephyr
SDKs
被
分组
在
特定
路径
下。

.. _toolchain_zephyr_sdk_compatibility:

Zephyr
SDK
版本
兼容性
********************************

一般
情况
下，
这
页
引用
的
Zephyr
SDK
版本
应该
被
考虑
为
对应
Zephyr
版本
的
推荐
版本。

对
完整
的
兼容
Zephyr
和
Zephyr
SDK
版本
列表，
参考
`Zephyr
SDK
Version
Compatibility
Matrix`_。

.. _toolchain_zephyr_sdk_install:

Zephyr
SDK
安装
***********************

.. toolchain_zephyr_sdk_install_start

.. note::
   你
   可以
   更改
   |sdk-version-literal|
   为
   下面
   说明
   中
   的
   另一
   个
   版本
   如果
   需要；
   `Zephyr
   SDK
   Releases`_
   页
   包含
   所有
   可用
   的
   SDK
   releases。

.. note::
   下面
   的
   说明
   是
   为
   了
   用
   Zephyr
   GNU
   SDK
   bundle
   安装，
   它
   包括
   所有
   支持
   架构
   的
   GNU
   工具链
   和
   主机
   工具。
   要
   用
   Zephyr
   LLVM
   SDK
   bundle
   安装，
   在
   SDK
   bundle
   文件
   名
   中
   将
   ``_gnu``
   后缀
   替换
   为
   ``_llvm``。

.. note::
   如果
   你
   想
   卸载
   SDK，
   你
   可以
   简单
   删除
   你
   安装
   它
   的
   目录。

.. tabs::

   .. group-tab::
      Linux

      .. _linux_zephyr_sdk:

      #. 下载
         并
         验证
         `Zephyr
         SDK
         bundle`_：

         .. parsed-literal::

            cd
            ~
            wget
            |sdk-url-linux|
            wget
            -O
            -
            |sdk-url-linux-sha|
            |
            shasum
            --check
            --ignore-missing

         如果
         你
         的
         主机
         架构
         是
         64
         位
         ARM
         （例如
         Raspberry
         Pi），
         将
         ``x86_64``
         替换
         为
         ``aarch64``
         以
         下载
         64
         位
         ARM
         Linux
         SDK。

      #. 解压
         Zephyr
         SDK
         bundle
         归档：

         .. parsed-literal::
