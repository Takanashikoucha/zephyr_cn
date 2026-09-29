.. _flashing-soc-board-config:

烧录配置
######################

Zephyr 支持为烧录器（flash runner，
从 :ref:`west flash<west-flashing>` 调用）
设置配置，
允许
自定义
烧录
开发板
时
命令
的
使用
方式。
此
配置
用于
:ref:`sysbuild` 项目，
允许
为
开发板
目标
组
配置
何时
运行
命令。
例如：
多核
SoC
可能
希望
只
允许
对所有
核心
使用
一次
``--erase`` 参数，
这会
防止
在
单次
``west flash`` 调用
中
运行
多个
擦除
任务，
这
可能
错误
地
清除
其他
正在
烧录
的
镜像
使用
的
内存。

优先级
********

烧录
配置
是
单一的，
它
只
会
从
单个
位置
读取，
此
配置
可以
位于
以下
文件
中，
按
最高
优先级
开始：

 * ``soc.yml``（在
   soc
   文件夹
   中）
 * ``board.yml``（在
   board
   文件夹
   中）

配置
*************

配置
通过
使用
带有
单个
``run_once`` 子项
的
``runners`` 映射
在
yml 文件
中
应用，
这
然后
包含
一个
命令
映射，
如
提供
给
烧录器
的
那样，
例如
``--reset`` 后
跟
一个
指定
每个
这些
命令
设置
的
列表
（这些
按
烧录器
分组，
并
按
限定符/开发板
分组）。
命令
使用
``runners`` 列表
值
有
关联
的
烧录器
它们
应用
于，
这
可以
包含
``all`` 如果
它
应用
于
所有
烧录器，
否则
必须
包含
每个
它
应用
于
的
烧录器
使用
烧录器
特定
名称。
开发板
目标
组
可以
使用
``groups`` 键
指定，
它
有
一个
开发板
目标
集合
的
列表。
开发板
目标
是
正则
表达式
匹配，
对于
``soc.yml`` 文件
每个
开发板
目标
集合
必须
在
``qualifiers`` 键
中
（只
允许
开发板
限定符
的
正则
表达式
匹配，
开发板
名称
必须
从
这些
条目
中
省略）。
对于
``board.yml`` 文件
每个
开发板
目标
集合
必须
在
``boards`` 键
中，
这些
是
包含
形成
单一
组
的
匹配
的
列表。
最后
一个
参数
``run`` 可以
设置
为
``first``，
意味着
命令
将
在
每个
开发板
目标
集合
的
第一个
镜像
烧录
过程
中
运行
一次，
或
设置
为
``last``，
将
在
每个
开发板
目标
集合
的
最终
镜像
烧录
中
运行
一次。

``soc.yml`` 的
示例
烧录
配置
显示
如下，
其中
``--recover`` 命令
只
会
对
使用
nRF5340 SoC 应用
或
网络
CPU 核心
的
任何
开发板
目标
使用
一次，
并
只
会在
所有
相应
核心
的
镜像
烧录
后
重置
网络
或
应用
核心。

.. code-block:: yaml

  runners:
    run_once:
      '--recover':
        - run: first
          runners:
            - nrfjprog
          groups:
            - qualifiers:
                - nrf5340/cpunet
                - nrf5340/cpuapp
                - nrf5340/cpuapp/ns
      '--reset':
        - run: last
          runners:
            - nrfjprog
            - jlink
          groups:
            - qualifiers:
                - nrf5340/cpunet
            - qualifiers:
                - nrf5340/cpuapp
                - nrf5340/cpuapp/ns
        # 虚构的
        # 非
        # 现实
        # 世界
        # 示例
        # 展示
        # 如何
        # 为
        # 不同
        # 烧录器
        # 指定
        # 不同
        # 选项
        - run: first
          runners:
            - some_other_runner
          groups:
            - qualifiers:
                - nrf5340/cpunet
            - qualifiers:
                - nrf5340/cpuapp
                - nrf5340/cpuapp/ns

使用
*****

烧录器
支持
的
命令
在
烧录
非
sysbuild
应用
时
可以
正常
使用，
run
once
配置
不会
被
使用。
烧录
带
多个
镜像
的
sysbuild
项目
时，
将
应用
烧录器
run
once
配置。

例如，
为
nrf5340dk
构建
:zephyr:code-sample:`smp-svr` 示例
将
包含
MCUboot 作为
次要
镜像：

.. code-block:: console

   cmake -GNinja -Sshare/sysbuild/ -Bbuild -DBOARD=nrf5340dk/nrf5340/cpuapp -DAPP_DIR=samples/subsys/mgmt/mcumgr/smp_svr
   cmake --build build

用
nrf5340dk
连接
构建
后，
以下
命令
可以
用于
烧录
开发板
的
两个
应用，
并
只
会
在
烧录
第一个
镜像
时
执行
单次
设备
恢复
操作：

.. code-block:: console

   west flash --recover

如果
上面
在
没有
烧录
配置
的
情况
下
运行，
恢复
过程
将
运行
两次，
设备
将
无法
启动。
