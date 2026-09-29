.. _build-signing:

签名
二进制
################

二进制
文件
可以
选择
作为
构建
的
一部分
自动
签名，
使用
CMake 代码，
也
可以
使用
``west sign`` 来
签名
二进制
文件，
本页
描述
前者，
后者
在
:ref:`west-sign` 中
记录。

MCUboot / imgtool
*****************

Zephyr 构建
系统
对
使用
`imgtool`_ 程序
（由
其
开发者
提供）
为
`MCUboot`_ 引导
加载器
使用
的
二进制
文件
签名
有
特殊
支持。
你
可以
通过
设置
一些
Kconfig 选项
在
一个
步骤
中
构建
并
签名
这种
类型
的
应用
二进制
文件。
如果
你
这样
做，
``west flash`` 将
使用
签名
的
二进制
文件。

这里
是
一个
示例
工作
流程，
构建
并
烧录
MCUboot，
以及
:zephyr:code-sample:`hello_world` 应用
用于
MCUboot 的
链
加载。
从
你在
:ref:`getting_started` 中
创建
的
:file:`zephyrproject` 工作区
运行
这些
命令：

.. code-block:: console

   west build -b YOUR_BOARD zephyr/samples/hello_world --sysbuild -d build-hello-signed -- \
       -DSB_CONFIG_BOOTLOADER_MCUBOOT=y

   west flash -d build-hello-signed

上面
命令
的
注意
事项：

- ``YOUR_BOARD`` 应该
  更改
  以
  匹配
  你的
  开发板
- 签名
  密钥
  值
  是
  MCUboot
  为
  开发
  和
  测试
  提供
  并
  使用
  的
  不安全
  默认
  值
- 你
  可以
  将
  ``hello_world`` 应用
  目录
  更改
  为
  任何
  可以
  被
  MCUboot
  加载
  的
  其他
  应用，
  例如
  :zephyr:code-sample:`smp-svr` 示例。

关于
这些
和
其他
相关
配置
选项
的
更多
信息，
见：

- :kconfig:option:`SB_CONFIG_BOOTLOADER_MCUBOOT`：
  为
  被
  MCUboot
  加载
  构建
  应用
- :kconfig:option:`SB_CONFIG_BOOT_SIGNATURE_KEY_FILE`：
  签名
  镜像
  时
  使用
  的
  密钥
  文件，
  或
  逗号
  分隔
  的
  密钥
  文件
  列表。
  如果
  你
  有
  自己
  的
  密钥，
  适当
  更改
  这；
  使用
  绝对
  路径
  或
  ``${APP_DIR}`` 这样
  的
  CMake 变量
  见
  :ref:`build-signing-keys`。
  给出
  列表
  时，
  MCUboot
  嵌入
  每个
  密钥
  的
  公钥
  一半
  并
  接受
  用
  其中
  任何
  一个
  签名
  的
  镜像；
  第一个
  条目
  也
  签名
  应用，
  第一个
  之后
  的
  每个
  条目
  必须
  是
  相同
  签名
  类型
  的
  仅
  公钥
  PEM
  供
  ``imgtool`` 使用。
- :kconfig:option:`CONFIG_MCUBOOT_EXTRA_IMGTOOL_ARGS`：
  ``imgtool`` 的
  可选
  附加
  命令行
  参数
- :kconfig:option:`CONFIG_MCUBOOT_GENERATE_CONFIRMED_IMAGE`：
  也
  生成
  一个
  已
  确认
  的
  镜像，
  它
  可能
  比
  可
  OTA 的
  默认
  镜像
  更
  适合
  在
  生产
  环境
  中
  烧录
- 在
  Windows 上，
  如果
  你
  遇到
  "Access denied" 问题，
  推荐
  的
  修复
  是
  运行
  ``pip3 install imgtool``，
  然后
  用
  干净
  的
  构建
  目录
  重试。

关于
多
密钥
引导
加载器
在
QEMU 下
端到
端
验证
的
完整
示例，
见
:zephyr_file:`tests/boot/mcuboot_multiple_keys` 测试。

如果
你的
``west flash`` :ref:`runner <west-runner>` 使用
imgtool 支持
的
镜像
格式，
你
运行
``west flash -d build-hello-signed`` 时
应该
在
设备
的
串口
控制台
上
看到
类似
以下
的
内容：

.. code-block:: none

   *** Booting Zephyr OS build zephyr-v2.3.0-2310-gcebac69c8ae1  ***
   [00:00:00.004,669] <inf> mcuboot: Starting bootloader
   [00:00:00.011,169] <inf> mcuboot: Primary image: magic=unset, swap_type=0x1, copy_done=0x3, image_ok=0x3
   [00:00:00.021,636] <inf> mcuboot: Boot source: none
   [00:00:00.027,374] <inf> mcuboot: Swap type: none
   [00:00:00.115,142] <inf> mcuboot: Bootloader chainload address offset: 0xc000
   [00:00:00.123,168] <inf> mcuboot: Jumping to the first image slot
   *** Booting Zephyr OS build zephyr-v2.3.0-2310-gcebac69c8ae1  ***
   Hello World! nrf52840dk_nrf52840

``west flash``
是否
支持
这个
功能
取决于
你的
runner。
``nrfjprog`` 和
``pyocd`` runner
与
上面
的
流程
配合
工作。
如果
你的
runner 不
支持
这个
流程
且
你
希望
它
支持，
请
发送
补丁
或
提交
issue
以
添加
支持。

.. _build-signing-keys:

签名
密钥
文件
*****************

使用
sysbuild
构建
时，
:kconfig:option:`SB_CONFIG_BOOT_SIGNATURE_KEY_FILE`
选择
用于
签名
镜像
的
密钥。
其
值
传播
到
两个
镜像：

- 应用
  镜像，
  作为
  :kconfig:option:`CONFIG_MCUBOOT_SIGNATURE_KEY_FILE`，
  ``imgtool``
  使用
  它
  签名
  应用；
  且
- MCUboot 镜像，
  作为
  ``CONFIG_BOOT_SIGNATURE_KEY_FILE``，
  其
  公钥
  部分
  被
  构建
  到
  引导
  加载器
  中
  以
  验证
  该
  签名。

.. warning::

   默认
   值
   指向
   与
   MCUboot
   捆绑
   的
   不安全
   开发
   密钥
   之一
   （例如
   :file:`root-ec-p256.pem`）。
   这些
   密钥
   是
   公开
   的
   —
   它们
   随
   每个
   Zephyr 和
   MCUboot
   checkout
   一起
   分发
   —
   因此
   只
   适合
   开发
   和
   测试。
   对于
   其他
   任何
   用途，
   生成
   你
   自己
   的
   密钥
   并
   将
   私钥
   保持
   在
   你
   不
   控制
   的
   任何
   仓库
   或
   构建
   目录
   之外。

sysbuild
如何
解析
密钥
文件
路径
=======================================

:kconfig:option:`SB_CONFIG_BOOT_SIGNATURE_KEY_FILE` 的
值
用
CMake 的
``string(CONFIGURE)`` 命令
处理，
因此
其中
包含
的
任何
``${VARIABLE}`` 引用
在
使用
路径
前
作为
CMake 变量
展开。
展开
后，
绝对
路径
按
原样
使用；
相对
路径
由
每个
镜像
独立
解析：

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 镜像
     - 相对
     路径
     的
     搜索
     顺序
   * - 应用
     （:kconfig:option:`CONFIG_MCUBOOT_SIGNATURE_KEY_FILE`）
     - ``APPLICATION_CONFIG_DIR``，
       然后
       west
       工作区
       topdir
       （``WEST_TOPDIR``）
   * - MCUboot
     （``CONFIG_BOOT_SIGNATURE_KEY_FILE``）
     - ``APPLICATION_CONFIG_DIR``，
       然后
       MCUboot
       模块
       目录

.. warning::

   每个
   镜像
   相对
   于
   不同
   的
   基础
   解析
   相对
   路径，
   因此
   裸
   相对
   路径
   对
   每个
   镜像
   指向
   不同
   的
   文件
   并
   通常
   构建
   失败。
   不要
   使用
   一个：
   给出
   绝对
   路径，
   或
   用
   CMake 变量
   锚定
   路径。

``${APP_DIR}``（主
应用
的
源
目录）
是
推荐
的
锚点：
它
将
密钥
保持
在
你
自己
的
应用
内，
且
两个
镜像
都
将其
解析
为
相同
的
文件。
值
展开
时
可用
的
任何
CMake 变量
都
可以
使用：

.. code-block:: cfg

   # sysbuild.conf
   SB_CONFIG_BOOT_SIGNATURE_KEY_FILE="${APP_DIR}/keys/my-signing-key.pem"

相同
的
解析
规则
适用
于
可选
的
加密
密钥
文件
（:kconfig:option:`CONFIG_MCUBOOT_ENCRYPTION_KEY_FILE`）。

.. _west-extending-signing:

外部
扩展
签名
****************************

运行
``west flash`` 时
使用
的
签名
脚本
可以
被
扩展
或
替换
以
更改
功能
或
引入
不同
的
签名
机制。
默认
启用
MCUboot
时，
签名
由
Zephyr 中
的
:file:`cmake/mcuboot.cmake` 文件
设置，
它
添加
额外
的
构建
后
命令
以
生成
签名
镜像。
用于
签名
的
文件
可以
从
sysbuild
作用域
（如果
使用）
或
从
zephyr/zephyr
模块
作用域
替换，
其
优先级
为：

* Sysbuild
* Zephyr
  属性
* 默认
  MCUboot
  脚本
  （如果
  启用）

从
sysbuild，
``-D<target>_SIGNING_SCRIPT``
可以
用于
为
特定
镜像
设置
签名
脚本，
或
``-DSIGNING_SCRIPT``
可以
用于
为
所有
镜像
设置
签名
脚本，
例如：

.. code-block:: console

   west build -b <board> <application> -DSIGNING_SCRIPT=<file>

zephyr
属性
方法
通过
调整
``zephyr_property_target`` 上
的
``SIGNING_SCRIPT`` 属性
实现，
理想
情况
下
由
模块
通过
使用
以下
方式
完成：

.. code-block:: cmake

   if(CONFIG_BOOTLOADER_MCUBOOT)
     set_target_properties(zephyr_property_target PROPERTIES SIGNING_SCRIPT ${CMAKE_CURRENT_LIST_DIR}/custom_signing.cmake)
   endif()

当
项目
在
启用
MCUboot
签名
支持
的
情况
下
构建
时，
这
将
包含
自定义
签名
CMake 文件
而非
默认
的
Zephyr 文件。
基础
Zephyr MCUboot
签名
文件
可以
作为
创建
新
签名
系统
或
扩展
默认
行为
的
参考。

.. _MCUboot:
   https://mcuboot.com/

.. _imgtool:
   https://pypi.org/project/imgtool/
