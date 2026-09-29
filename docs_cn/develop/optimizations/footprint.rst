.. _footprint:

优化
占用
空间
########################

栈
大小
***********

各种
系统
线程
的
栈
大小
被
宽裕
地
指定
以
允许
在
尽可能
多
的
受
支持
平台
上
的
不同
场景
中
使用。
你
应该
通过
审查
所有
栈
大小
并
为
你的
应用
调整
它们
来
开始
优化
过程：

:kconfig:option:`CONFIG_ISR_STACK_SIZE`
   默认
   设置
   为
   2048

:kconfig:option:`CONFIG_MAIN_STACK_SIZE`
   默认
   设置
   为
   1024

:kconfig:option:`CONFIG_IDLE_STACK_SIZE`
   默认
   设置
   为
   320

:kconfig:option:`CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE`
   默认
   设置
   为
   1024

:kconfig:option:`CONFIG_PRIVILEGED_STACK_SIZE`
   默认
   设置
   为
   1024，
   取决于
   userspace
   功能。


未
使用
的
外设
******************

某些
外设
默认
启用。
你
可以
在
项目
配置
中
禁用
未
使用
的
外设，
例如::


        CONFIG_GPIO=n
        CONFIG_SPI=n

各种
调试/
信息
选项
***********************************

以下
选项
输出
更多
关于
运行
中
应用
的
信息
并
提供
调试
和
错误
处理
的
手段：

:kconfig:option:`CONFIG_BOOT_BANNER`
   这个
   选项
   可以
   禁用
   以
   节省
   几
   个
   字节。

:kconfig:option:`CONFIG_DEBUG`
   这个
   选项
   可以
   启用
   用于
   调试
   构建。

注意
boot
banner
默认
启用。


MPU/MMU
支持
***************

取决于
你的
应用
和
平台
需求，
你
可以
禁用
MPU/MMU
支持
以
获得
一些
内存
并
改进
性能。
不过
要
考虑
这个
配置
选择
的
后果，
因为
你
将
失去
高级
栈
检查
和
支持。
